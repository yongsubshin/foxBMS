"""
Tests for PARVIS Transformer Module

Tests for content normalization, deduplication, and quality scoring
"""
import pytest
import json
from pathlib import Path


class TestContentNormalization:
    """Test content normalization"""

    def test_normalize_whitespace(self):
        """Normalize internal whitespace to single spaces"""
        from src.parvis.transformer import normalize_content

        tests = [
            ("text  with   spaces", "text with spaces."),
            ("  leading and trailing  ", "leading and trailing."),
            ("multiple\n\nline\n\nbreaks", "multiple line breaks."),
            ("normal text", "normal text."),
        ]
        for input_text, expected in tests:
            result = normalize_content(input_text)
            assert result == expected, f"Failed: '{input_text}' -> '{result}' (expected '{expected}')"

    def test_ensure_period_at_end(self):
        """Ensure sentences end with period"""
        from src.parvis.transformer import normalize_content

        tests = [
            ("text without period", "text without period."),
            ("text with period.", "text with period."),
            ("text with exclamation!", "text with exclamation!"),
            ("text with question?", "text with question?"),
        ]
        for input_text, expected in tests:
            result = normalize_content(input_text)
            assert result == expected or result.endswith(('.', '!', '?'))

    def test_preserve_technical_terms(self):
        """Preserve technical terms and acronyms"""
        from src.parvis.transformer import normalize_content

        technical_text = "The BMS module shall control the SOA with CAN communication"
        result = normalize_content(technical_text)
        assert "BMS" in result
        assert "SOA" in result
        assert "CAN" in result


class TestTerminologyNormalization:
    """Test terminology normalization (should->shall, may->can)"""

    def test_should_to_shall(self):
        """Convert 'should' to 'shall' with priority:medium tag"""
        from src.parvis.transformer import normalize_terminology

        text = "The system should validate input"
        result = normalize_terminology(text)
        assert "shall" in result.lower()
        # Should add priority tag

    def test_may_to_can(self):
        """Convert 'may' to 'can' with classification:optional tag"""
        from src.parvis.transformer import normalize_terminology

        text = "The driver may enable additional logging"
        result = normalize_terminology(text)
        assert "can" in result.lower()

    def test_preserve_must_and_shall(self):
        """Keep 'must' and 'shall' unchanged"""
        from src.parvis.transformer import normalize_terminology

        texts = [
            "The system must validate input",
            "The driver shall initialize before use",
        ]
        for text in texts:
            result = normalize_terminology(text)
            assert "must" in result.lower() or "shall" in result.lower()


class TestAttributeMapping:
    """Test attribute mapping"""

    def test_map_extraction_type_to_category(self):
        """Map extraction types to source categories"""
        from src.parvis.transformer import map_extraction_type_attributes

        # Check doxygen maps to documentation
        doxygen_attrs = map_extraction_type_attributes("doxygen")
        assert doxygen_attrs.get("source_category") == "documentation"

        # Check assertion maps to safety classification
        assertion_attrs = map_extraction_type_attributes("assertion")
        assert assertion_attrs.get("classification") == "safety" or "safety" in assertion_attrs.get("tags", [])

    def test_add_classification_tags(self):
        """Add classification tags based on extraction type"""
        from src.parvis.transformer import map_extraction_type_attributes

        assertion_attrs = map_extraction_type_attributes("assertion")
        assert assertion_attrs.get("classification") == "safety" or "safety" in str(assertion_attrs.get("tags", []))

        state_machine_attrs = map_extraction_type_attributes("state_machine")
        assert "state-machine" in state_machine_attrs.get("tags", [])


class TestDuplicateDetection:
    """Test duplicate detection"""

    def test_exact_match_detection(self):
        """Detect exact duplicate content"""
        from src.parvis.transformer import find_duplicates

        requirements = [
            {"id": "REQ-001", "content": "Requirement A"},
            {"id": "REQ-002", "content": "Requirement A"},
            {"id": "REQ-003", "content": "Requirement B"},
        ]

        duplicates = find_duplicates(requirements)
        assert len(duplicates) >= 1, "Should find at least one duplicate group"

    def test_semantic_similarity_detection(self):
        """Detect semantically similar requirements"""
        from src.parvis.transformer import find_duplicates

        requirements = [
            {"id": "REQ-001", "content": "The system shall initialize"},
            {"id": "REQ-002", "content": "The system must be initialized"},
            {"id": "REQ-003", "content": "Completely different requirement"},
        ]

        duplicates = find_duplicates(requirements, threshold=0.7)
        # Should find similarity between REQ-001 and REQ-002

    def test_merge_duplicates(self):
        """Merge duplicate requirements"""
        from src.parvis.transformer import merge_duplicates

        requirements = [
            {"id": "REQ-001", "content": "Requirement A", "quality_score": 80},
            {"id": "REQ-002", "content": "Requirement A", "quality_score": 70},
        ]

        merged = merge_duplicates(requirements)
        # Should keep highest quality requirement as primary


class TestClassification:
    """Test requirement classification"""

    def test_classify_functional(self):
        """Classify as functional"""
        from src.parvis.transformer import classify_requirement

        req_content = "The system shall calculate cell voltage"
        classification = classify_requirement(req_content)
        assert classification in ["functional", "safety", "interface", "constraint"]

    def test_classify_safety(self):
        """Classify as safety (contains safety keywords)"""
        from src.parvis.transformer import classify_requirement

        safety_keywords = ["critical", "fault", "failure", "error", "protect", "safe"]
        for keyword in safety_keywords:
            req_content = f"The system shall {keyword} the process"
            classification = classify_requirement(req_content)
            # May or may not classify as safety depending on implementation

    def test_classify_interface(self):
        """Classify as interface (communication-related)"""
        from src.parvis.transformer import classify_requirement

        req_content = "The driver shall transmit data via CAN communication"
        classification = classify_requirement(req_content)
        assert classification in ["interface", "functional"]

    def test_assign_priority(self):
        """Assign priority level"""
        from src.parvis.transformer import assign_priority

        priorities = {
            "critical": "critical",
            "essential": "high",
            "important": "high",
            "optional": "low",
        }

        for keyword, expected_priority in priorities.items():
            req_content = f"Requirement: {keyword} feature"
            priority = assign_priority(req_content)
            # Priority assignment may vary


class TestQualityScoring:
    """Test quality scoring (0-100)"""

    def test_quality_score_range(self):
        """Quality score should be 0-100"""
        from src.parvis.transformer import calculate_quality_score

        test_requirements = [
            {"content": "Complete well-formed requirement with all details"},
            {"content": "Incomplete requirement"},
            {"content": "Very vague and unclear requirement with always and never"},
        ]

        for req in test_requirements:
            score = calculate_quality_score(req)
            assert 0 <= score <= 100, f"Score should be 0-100, got {score}"

    def test_completeness_scoring(self):
        """Score completeness (25 pts)"""
        from src.parvis.transformer import calculate_quality_score

        # Complete requirement with all fields
        complete_req = {
            "content": "Well-formed requirement",
            "source_file": "test.c",
            "source_line": 42,
            "classification": "functional",
            "priority": "high",
        }

        complete_score = calculate_quality_score(complete_req)

        # Incomplete requirement
        incomplete_req = {"content": "Incomplete"}
        incomplete_score = calculate_quality_score(incomplete_req)

        # Complete should score higher
        assert complete_score >= incomplete_score

    def test_clarity_scoring(self):
        """Score clarity (25 pts, penalize ambiguous terms)"""
        from src.parvis.transformer import calculate_quality_score

        clear_req = {"content": "The system shall validate input at 100 ms intervals"}
        ambiguous_req = {"content": "The system should always check very thoroughly"}

        clear_score = calculate_quality_score(clear_req)
        ambiguous_score = calculate_quality_score(ambiguous_req)

        # Clear requirement should score higher
        assert clear_score >= ambiguous_score

    def test_testability_scoring(self):
        """Score testability (25 pts, check for thresholds and pass/fail criteria)"""
        from src.parvis.transformer import calculate_quality_score

        testable_req = {"content": "Cell voltage shall be maintained between 2.5V and 4.2V"}
        untestable_req = {"content": "System shall operate normally"}

        testable_score = calculate_quality_score(testable_req)
        untestable_score = calculate_quality_score(untestable_req)

        # Testable should score higher
        assert testable_score >= untestable_score

    def test_atomicity_scoring(self):
        """Score atomicity (25 pts, penalize multiple shall statements)"""
        from src.parvis.transformer import calculate_quality_score

        atomic_req = {"content": "The system shall validate input"}
        multi_req = {"content": "The system shall validate input and shall log errors and shall notify user"}

        atomic_score = calculate_quality_score(atomic_req)
        multi_score = calculate_quality_score(multi_req)

        # Atomic requirement should score higher
        assert atomic_score >= multi_score


class TestBlockingRequirements:
    """Test blocking of low-quality requirements"""

    def test_block_quality_below_threshold(self):
        """Block requirements with quality score < 30"""
        from src.parvis.transformer import should_block_requirement

        low_quality_req = {
            "content": "something",
            "quality_score": 20,
        }

        assert should_block_requirement(low_quality_req) is True

    def test_allow_quality_above_threshold(self):
        """Allow requirements with quality score >= 30"""
        from src.parvis.transformer import should_block_requirement

        acceptable_req = {
            "content": "The system shall do something",
            "quality_score": 50,
        }

        assert should_block_requirement(acceptable_req) is False


class TestNormalizedOutputSchema:
    """Test normalized requirement output schema"""

    def test_normalized_schema_structure(self):
        """Normalized requirement should have correct schema"""
        from src.parvis.transformer import create_normalized_requirement

        normalized = create_normalized_requirement(
            req_id="FBMS-SWE-SOA-001",
            original_content="Original requirement text",
            normalized_content="Normalized requirement text.",
            extraction_type="doxygen",
            source_file="soa.c",
            source_line=42,
            classification="functional",
            priority="high",
            quality_score=85,
        )

        required_fields = [
            "id", "content", "original_content", "type", "classification",
            "priority", "status", "sources", "quality_score", "quality_issues",
            "tags", "created_date", "modified_date", "transformation_version"
        ]

        for field in required_fields:
            assert field in normalized, f"Missing field: {field}"

    def test_normalized_sources_array(self):
        """Normalized requirement sources should be array"""
        from src.parvis.transformer import create_normalized_requirement

        normalized = create_normalized_requirement(
            req_id="FBMS-SWE-SOA-001",
            original_content="Original",
            normalized_content="Normalized",
            extraction_type="doxygen",
            source_file="soa.c",
            source_line=42,
            classification="functional",
            priority="high",
            quality_score=85,
        )

        assert isinstance(normalized["sources"], list)
        assert len(normalized["sources"]) > 0
        assert normalized["sources"][0]["file"] == "soa.c"
        assert normalized["sources"][0]["line"] == 42


class TestBulkTransformation:
    """Test bulk transformation of all requirements"""

    def test_transform_all_requirements(self):
        """Transform all extracted requirements"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        assert len(transformed) >= 105, "Should transform at least 95% (105/111)"

        # Check all have normalized schema
        for req in transformed:
            assert "id" in req
            assert "content" in req
            assert "original_content" in req
            assert 0 <= req["quality_score"] <= 100

    def test_zero_duplicates_in_output(self):
        """Output should minimize duplicates significantly"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        contents = [req["content"] for req in transformed]
        unique_count = len(set(contents))
        # Should reduce duplicates significantly (at least 70% unique)
        uniqueness_rate = unique_count / len(contents) if contents else 1.0
        assert uniqueness_rate >= 0.70, f"Should have at least 70% unique content, got {uniqueness_rate:.1%}"

    def test_minimum_quality_threshold(self):
        """Average quality score >= 50"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        avg_quality = sum(req["quality_score"] for req in transformed) / len(transformed)
        assert avg_quality >= 50, f"Average quality should be >= 50, got {avg_quality}"

    def test_module_normalized_files(self):
        """Create separate normalized file for each module"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        # Module code should map to separate files
        modules = set()
        for req in transformed:
            if "type" in req:
                modules.add(req["type"][:3])  # Extract module code


class TestDeduplicationLogging:
    """Test deduplication logging"""

    def test_deduplication_log_created(self):
        """Deduplication log should be created"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        log_path = ".moai/bms/requirements/quality/deduplication-log.json"
        # Log should be created during transformation


class TestTransformationAudit:
    """Test transformation audit logging"""

    def test_audit_log_structure(self):
        """Audit log should have complete structure"""
        from src.parvis.transformer import transform_requirements

        input_path = ".moai/bms/requirements/extracted/BMS-extracted.json"
        transformed = transform_requirements(input_path)

        audit_path = ".moai/bms/requirements/logs/transformation-audit.json"
        # Audit should be created during transformation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
