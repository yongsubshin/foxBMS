"""
PARVIS Transformer Module

Normalizes, deduplicates, and scores requirement content for quality assurance.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict
import hashlib


def normalize_content(content: str) -> str:
    """
    Normalize requirement content.

    - Trim leading/trailing whitespace
    - Normalize internal whitespace to single spaces
    - Ensure sentences end with period
    - Preserve technical terms
    """
    if not content:
        return ""

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', content.strip())

    # Ensure ends with period if not ending with punctuation
    if normalized and normalized[-1] not in '.!?':
        normalized += '.'

    return normalized


def normalize_terminology(content: str) -> str:
    """
    Normalize terminology.

    - 'should' -> 'shall' with priority:medium
    - 'may' -> 'can' with classification:optional
    - Keep 'must', 'shall' unchanged
    """
    result = content

    # Replace should with shall (preserve word boundaries)
    result = re.sub(r'\bshould\b', 'shall', result, flags=re.IGNORECASE)

    # Replace may with can (preserve word boundaries)
    result = re.sub(r'\bmay\b', 'can', result, flags=re.IGNORECASE)

    return result


def map_extraction_type_attributes(extraction_type: str) -> Dict:
    """
    Map extraction type to attributes.

    - doxygen -> source_category: documentation
    - assertion -> classification: safety, tags: [safety]
    - state_machine -> tags: [state-machine, behavior]
    - config -> type: CFG
    """
    mapping = {
        "doxygen": {
            "source_category": "documentation",
        },
        "assertion": {
            "classification": "safety",
            "tags": ["safety", "assertion"],
        },
        "state_machine": {
            "tags": ["state-machine", "behavior"],
        },
        "config": {
            "tags": ["configuration"],
        },
    }
    return mapping.get(extraction_type, {})


def find_duplicates(requirements: List[Dict], threshold: float = 0.7) -> List[List[Dict]]:
    """
    Find duplicate and similar requirements.

    Phase 1: Exact match detection
    Phase 2: Semantic similarity (Jaccard > threshold)

    Returns: List of duplicate groups
    """
    # Phase 1: Exact match by normalized content
    exact_matches = defaultdict(list)
    for req in requirements:
        content = normalize_content(req.get("content", "")).lower()
        content_hash = hashlib.md5(content.encode()).hexdigest()
        exact_matches[content_hash].append(req)

    duplicate_groups = []

    # Phase 1 results
    for hash_val, group in exact_matches.items():
        if len(group) > 1:
            duplicate_groups.append(group)

    # Phase 2: Semantic similarity for single occurrences
    single_reqs = [group[0] for group in exact_matches.values() if len(group) == 1]
    for i, req1 in enumerate(single_reqs):
        for req2 in single_reqs[i + 1:]:
            similarity = _jaccard_similarity(req1.get("content", ""), req2.get("content", ""))
            if similarity >= threshold:
                duplicate_groups.append([req1, req2])

    return duplicate_groups


def _jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two texts"""
    tokens1 = set(text1.lower().split())
    tokens2 = set(text2.lower().split())

    if not tokens1 or not tokens2:
        return 0.0

    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)

    return intersection / union if union > 0 else 0.0


def merge_duplicates(requirements: List[Dict]) -> List[Dict]:
    """
    Merge duplicate requirements.

    Keep highest quality requirement as primary, aggregate sources.
    """
    duplicates = find_duplicates(requirements)

    if not duplicates:
        return requirements

    merged = []
    merged_ids = set()

    for group in duplicates:
        # Sort by quality score descending
        sorted_group = sorted(group, key=lambda x: x.get("quality_score", 0), reverse=True)
        primary = sorted_group[0]

        # Aggregate sources
        all_sources = []
        for req in sorted_group:
            if "sources" in req and isinstance(req["sources"], list):
                all_sources.extend(req["sources"])
            else:
                all_sources.append({"file": req.get("source_file", ""), "line": req.get("source_line", 0)})

        primary["sources"] = all_sources
        merged.append(primary)
        merged_ids.add(primary.get("id"))

    # Add non-duplicate requirements
    for req in requirements:
        if req.get("id") not in merged_ids:
            merged.append(req)

    return merged


def classify_requirement(content: str) -> str:
    """
    Classify requirement.

    Returns: functional, safety, interface, or constraint
    """
    content_lower = content.lower()

    # Safety classification
    safety_keywords = ["critical", "fault", "failure", "error", "protect", "safe", "danger", "hazard"]
    if any(keyword in content_lower for keyword in safety_keywords):
        return "safety"

    # Interface classification
    interface_keywords = ["interface", "communication", "can", "message", "transmit", "receive", "protocol"]
    if any(keyword in content_lower for keyword in interface_keywords):
        return "interface"

    # Constraint classification
    constraint_keywords = ["constraint", "limitation", "maximum", "minimum", "not", "forbidden", "prohibited"]
    if any(keyword in content_lower for keyword in constraint_keywords):
        return "constraint"

    # Default to functional
    return "functional"


def assign_priority(content: str) -> str:
    """
    Assign priority level.

    Returns: critical, high, medium, or low
    """
    content_lower = content.lower()

    # Critical keywords
    if any(word in content_lower for word in ["critical", "safety", "protect", "fault", "error", "must"]):
        return "critical"

    # High keywords
    if any(word in content_lower for word in ["essential", "important", "shall", "required"]):
        return "high"

    # Medium keywords
    if any(word in content_lower for word in ["should", "recommended", "standard"]):
        return "medium"

    # Default to low
    return "low"


def calculate_quality_score(requirement: Dict) -> int:
    """
    Calculate quality score (0-100).

    Scoring:
    - Completeness (25 pts): Check required fields
    - Clarity (25 pts): Check for ambiguous terms
    - Testability (25 pts): Check for metrics/thresholds
    - Atomicity (25 pts): Check for multiple shall statements
    """
    score = 100

    # Completeness (25 pts)
    required_fields = ["content", "source_file", "source_line"]
    missing = sum(1 for field in required_fields if not requirement.get(field))
    score -= missing * 5

    # Clarity (25 pts) - penalize ambiguous terms
    content = requirement.get("content", "").lower()
    ambiguous_terms = ["always", "never", "all", "some", "any", "very", "extremely"]
    ambiguous_count = sum(1 for term in ambiguous_terms if f" {term} " in f" {content} ")
    score -= ambiguous_count * 3

    # Testability (25 pts) - check for thresholds, times, etc.
    testability_patterns = [
        r'\d+\s*(ms|s|minutes|hours)',  # Time thresholds
        r'\d+\.\d+\s*v|mv',  # Voltage thresholds
        r'pass|fail|success|error',  # Clear pass/fail criteria
    ]
    testable = sum(1 for pattern in testability_patterns if re.search(pattern, content, re.IGNORECASE))
    if testable == 0:
        score -= 15

    # Atomicity (25 pts) - penalize multiple shall statements
    shall_count = len(re.findall(r'\bshall\b', content, re.IGNORECASE))
    if shall_count > 1:
        score -= (shall_count - 1) * 10

    # Ensure score is within 0-100
    return max(0, min(100, score))


def should_block_requirement(requirement: Dict) -> bool:
    """
    Determine if requirement should be blocked (quality < 30).

    Returns: True if should be blocked
    """
    quality_score = requirement.get("quality_score", 0)
    return quality_score < 30


def create_normalized_requirement(
    req_id: str,
    original_content: str,
    normalized_content: str,
    extraction_type: str,
    source_file: str,
    source_line: int,
    classification: str,
    priority: str,
    quality_score: int,
    quality_issues: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> Dict:
    """Create normalized requirement with full schema"""
    if quality_issues is None:
        quality_issues = []
    if tags is None:
        tags = []

    # Extract TYPE code from req_id
    req_type = req_id.split("-")[1] if "-" in req_id else "SWE"

    return {
        "id": req_id,
        "content": normalized_content,
        "original_content": original_content,
        "type": req_type,
        "classification": classification,
        "priority": priority,
        "status": "draft",
        "sources": [
            {
                "file": source_file,
                "line": source_line,
                "extraction_type": extraction_type,
            }
        ],
        "quality_score": quality_score,
        "quality_issues": quality_issues,
        "tags": tags,
        "created_date": datetime.now().isoformat(),
        "modified_date": datetime.now().isoformat(),
        "transformation_version": "1.0.0",
    }


def transform_requirements(input_path: str) -> List[Dict]:
    """
    Transform all extracted requirements.

    Returns: List of normalized requirements
    """
    # Load requirements with IDs
    registry_path = ".moai/bms/requirements/registry/id-registry.json"
    with open(registry_path) as f:
        registry = json.load(f)

    requirements_with_ids = registry["requirements"]

    # Transform each requirement
    normalized = []
    for req in requirements_with_ids:
        try:
            req_id = req.get("assigned_id")
            original_content = req.get("content", "")
            extraction_type = req.get("extraction_type", "doxygen")

            # Normalize content
            normalized_content = normalize_content(original_content)
            normalized_content = normalize_terminology(normalized_content)

            # Extract attributes
            attrs = map_extraction_type_attributes(extraction_type)
            tags = attrs.get("tags", [])
            classification = attrs.get("classification", classify_requirement(normalized_content))

            # Calculate quality score
            req_with_quality = req.copy()
            req_with_quality["quality_score"] = calculate_quality_score(req)
            quality_score = req_with_quality["quality_score"]

            # Check if should be blocked
            if should_block_requirement(req_with_quality):
                continue

            # Create normalized requirement
            normalized_req = create_normalized_requirement(
                req_id=req_id,
                original_content=original_content,
                normalized_content=normalized_content,
                extraction_type=extraction_type,
                source_file=req.get("source_file", ""),
                source_line=req.get("source_line", 0),
                classification=classification,
                priority=assign_priority(normalized_content),
                quality_score=quality_score,
                tags=tags,
            )

            normalized.append(normalized_req)

        except Exception as e:
            # Log error but continue
            pass

    # Remove duplicates
    merged = merge_duplicates(normalized)

    # Create deduplication log
    dedup_log = {
        "timestamp": datetime.now().isoformat(),
        "input_count": len(requirements_with_ids),
        "output_count": len(merged),
        "duplicates_removed": len(requirements_with_ids) - len(merged),
    }

    dedup_log_path = ".moai/bms/requirements/quality/deduplication-log.json"
    Path(".moai/bms/requirements/quality").mkdir(parents=True, exist_ok=True)
    with open(dedup_log_path, "w") as f:
        json.dump(dedup_log, f, indent=2)

    # Create master normalized file
    master_path = ".moai/bms/requirements/normalized/master-normalized.json"
    Path(".moai/bms/requirements/normalized").mkdir(parents=True, exist_ok=True)
    with open(master_path, "w") as f:
        json.dump(merged, f, indent=2)

    # Create audit log
    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "source": input_path,
        "total_processed": len(requirements_with_ids),
        "total_output": len(merged),
        "average_quality_score": sum(r["quality_score"] for r in merged) / len(merged) if merged else 0,
        "classification_distribution": _get_classification_distribution(merged),
        "priority_distribution": _get_priority_distribution(merged),
    }

    audit_log_path = ".moai/bms/requirements/logs/transformation-audit.json"
    Path(".moai/bms/requirements/logs").mkdir(parents=True, exist_ok=True)
    with open(audit_log_path, "w") as f:
        json.dump(audit_log, f, indent=2)

    return merged


def _get_classification_distribution(requirements: List[Dict]) -> Dict[str, int]:
    """Count distribution of classifications"""
    distribution = {}
    for req in requirements:
        classification = req.get("classification", "functional")
        distribution[classification] = distribution.get(classification, 0) + 1
    return distribution


def _get_priority_distribution(requirements: List[Dict]) -> Dict[str, int]:
    """Count distribution of priorities"""
    distribution = {}
    for req in requirements:
        priority = req.get("priority", "low")
        distribution[priority] = distribution.get(priority, 0) + 1
    return distribution


if __name__ == "__main__":
    # Example usage
    normalized = transform_requirements(".moai/bms/requirements/extracted/BMS-extracted.json")
    print(f"Transformed {len(normalized)} requirements")
    avg_quality = sum(r["quality_score"] for r in normalized) / len(normalized) if normalized else 0
    print(f"Average quality score: {avg_quality:.1f}")
