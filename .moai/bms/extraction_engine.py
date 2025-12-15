#!/usr/bin/env python3
"""
PARVIS Extraction Engine - Requirement extraction from C source code
Extracts requirements from Doxygen, state machines, assertions, and configs
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ExtractionType(Enum):
    """Types of requirement extractions"""
    DOXYGEN = "doxygen"
    STATE_MACHINE = "state_machine"
    ASSERTION = "assertion"
    CONFIG = "config"


class ConfidenceLevel(Enum):
    """Confidence levels for extracted requirements"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ExtractedRequirement:
    """Extracted requirement object"""
    extraction_type: str
    content: str
    source_file: str
    source_line: int
    confidence: str
    req_id: Optional[str] = None
    suggested_type: str = "SWE"
    suggested_module: str = "BMS"
    traceability_hints: List[str] = None
    rationale: str = ""

    def __post_init__(self):
        """Initialize default values"""
        if self.traceability_hints is None:
            self.traceability_hints = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "req_id": self.req_id,
            "suggested_type": self.suggested_type,
            "suggested_module": self.suggested_module,
            "extraction_type": self.extraction_type,
            "content": self.content,
            "source_line": self.source_line,
            "source_file": self.source_file,
            "confidence": self.confidence,
            "traceability_hints": self.traceability_hints,
            "rationale": self.rationale
        }


class DoxygenParser:
    """Parses Doxygen documentation from C source files"""

    DOXYGEN_BLOCK_START = re.compile(r'/\*\*')
    DOXYGEN_BLOCK_END = re.compile(r'\*/')
    DOXYGEN_TAG = re.compile(r'@(\w+)\s+(.+?)(?=@\w+|\*\/|$)', re.DOTALL)
    TAG_PATTERN = re.compile(r'@(brief|details|param|return|pre|post|file|ingroup|prefix)')

    def extract_doxygen_blocks(self, content: str, filepath: str) -> List[Tuple[int, str]]:
        """Extract Doxygen blocks from content with line numbers"""
        lines = content.split('\n')
        blocks = []
        in_block = False
        block_start = 0
        block_content = []

        for i, line in enumerate(lines, 1):
            if self.DOXYGEN_BLOCK_START.search(line):
                in_block = True
                block_start = i
                block_content = [line]
            elif in_block:
                block_content.append(line)
                if self.DOXYGEN_BLOCK_END.search(line):
                    in_block = False
                    full_block = '\n'.join(block_content)
                    blocks.append((block_start, full_block))
                    block_content = []

        return blocks

    def parse_block(self, block: str) -> Dict[str, str]:
        """Parse a Doxygen block into tags"""
        tags = {}
        lines = block.split('\n')
        current_tag = None
        current_content = []

        for line in lines:
            # Remove comment markers
            line = re.sub(r'^\s*\*\s?', '', line)
            line = re.sub(r'^/\*\*\s*', '', line)
            line = re.sub(r'\*/$', '', line)

            # Check for tag
            tag_match = self.TAG_PATTERN.search(line)
            if tag_match:
                # Save previous tag
                if current_tag:
                    tags[current_tag] = ' '.join(current_content).strip()
                current_tag = tag_match.group(1)
                # Extract content after tag
                content_start = tag_match.end()
                content = line[content_start:].strip()
                current_content = [content] if content else []
            elif current_tag and line.strip():
                current_content.append(line.strip())

        # Save last tag
        if current_tag:
            tags[current_tag] = ' '.join(current_content).strip()

        return tags

    def extract_requirements(self, content: str, filepath: str) -> List[ExtractedRequirement]:
        """Extract Doxygen-based requirements"""
        requirements = []
        blocks = self.extract_doxygen_blocks(content, filepath)

        for line_num, block in blocks:
            tags = self.parse_block(block)

            # Determine confidence
            confidence = ConfidenceLevel.LOW.value
            if 'brief' in tags and 'details' in tags:
                confidence = ConfidenceLevel.HIGH.value
            elif 'brief' in tags or 'details' in tags:
                confidence = ConfidenceLevel.MEDIUM.value

            # Create requirement from brief and details
            brief = tags.get('brief', '')
            details = tags.get('details', '')
            content_text = f"{brief} {details}".strip()

            if content_text:
                traceability = []
                if 'file' in tags:
                    traceability.append(tags['file'])
                if 'ingroup' in tags:
                    traceability.append(tags['ingroup'])

                req = ExtractedRequirement(
                    extraction_type=ExtractionType.DOXYGEN.value,
                    content=content_text,
                    source_file=filepath,
                    source_line=line_num,
                    confidence=confidence,
                    traceability_hints=traceability,
                    rationale="Extracted from Doxygen documentation"
                )
                requirements.append(req)

        return requirements


class StateMachineExtractor:
    """Extracts state machine requirements from C source"""

    ENUM_PATTERN = re.compile(r'typedef\s+enum\s*{([^}]+)}\s*(\w+)\s*;', re.MULTILINE | re.DOTALL)
    STATE_VAR_PATTERN = re.compile(r'static\s+(\w+_STATE_s)\s*\*?\s*(\w+)\s*[=;]')
    SWITCH_PATTERN = re.compile(r'switch\s*\(\s*(\w+(?:\->\w+)?)\s*\)\s*{', re.MULTILINE)
    CASE_PATTERN = re.compile(r'case\s+(\w+)\s*:', re.MULTILINE)

    def extract_state_enums(self, content: str, filepath: str) -> List[Tuple[str, List[str], int]]:
        """Extract state machine enums"""
        enums = []
        for match in self.ENUM_PATTERN.finditer(content):
            enum_body = match.group(1)
            enum_name = match.group(2)
            line_num = content[:match.start()].count('\n') + 1

            # Extract state names
            states = []
            for state_line in enum_body.split(','):
                state_name = state_line.split('{')[0].strip()
                if state_name and not state_name.startswith('/*'):
                    states.append(state_name)

            enums.append((enum_name, states, line_num))

        return enums

    def extract_requirements(self, content: str, filepath: str) -> List[ExtractedRequirement]:
        """Extract state machine-based requirements"""
        requirements = []
        enums = self.extract_state_enums(content, filepath)

        for enum_name, states, line_num in enums:
            if 'STATEMACH' in enum_name or 'STATE' in enum_name:
                # Create requirement for state machine existence
                confidence = ConfidenceLevel.HIGH.value if len(states) > 2 else ConfidenceLevel.MEDIUM.value

                req = ExtractedRequirement(
                    extraction_type=ExtractionType.STATE_MACHINE.value,
                    content=f"State machine {enum_name} with states: {', '.join(states[:3])}{'...' if len(states) > 3 else ''}",
                    source_file=filepath,
                    source_line=line_num,
                    confidence=confidence,
                    suggested_type="FSR",  # Functional Safety Requirement
                    traceability_hints=[enum_name],
                    rationale=f"State machine pattern detected in {enum_name}"
                )
                requirements.append(req)

                # Create requirements for each state
                for i, state in enumerate(states):
                    state_req = ExtractedRequirement(
                        extraction_type=ExtractionType.STATE_MACHINE.value,
                        content=f"State {state} exists in {enum_name}",
                        source_file=filepath,
                        source_line=line_num + i,
                        confidence=ConfidenceLevel.HIGH.value,
                        suggested_type="FSR",
                        traceability_hints=[enum_name, state],
                        rationale=f"State {state} is defined in state machine"
                    )
                    requirements.append(state_req)

        return requirements


class AssertionExtractor:
    """Extracts safety assertions from C source"""

    ASSERT_PATTERN = re.compile(r'FAS_ASSERT\s*\(\s*([^)]+)\s*\)', re.MULTILINE)
    ASSERTION_TYPES = {
        r'.*\s*!=\s*NULL': "pointer_validation",
        r'.*\s*<\s*\w+': "range_check",
        r'.*\s*==\s*\w+': "state_verification",
        r'.*': "invariant_check"
    }

    def categorize_assertion(self, condition: str) -> Tuple[str, str]:
        """Categorize assertion type based on condition"""
        for pattern, category in self.ASSERTION_TYPES.items():
            if re.match(pattern, condition):
                return category, ConfidenceLevel.HIGH.value if category != "invariant_check" else ConfidenceLevel.MEDIUM.value

        return "invariant_check", ConfidenceLevel.LOW.value

    def extract_requirements(self, content: str, filepath: str) -> List[ExtractedRequirement]:
        """Extract assertion-based requirements"""
        requirements = []

        for match in self.ASSERT_PATTERN.finditer(content):
            condition = match.group(1).strip()
            line_num = content[:match.start()].count('\n') + 1

            category, confidence = self.categorize_assertion(condition)

            req = ExtractedRequirement(
                extraction_type=ExtractionType.ASSERTION.value,
                content=f"Assertion requirement: {condition}",
                source_file=filepath,
                source_line=line_num,
                confidence=confidence,
                suggested_type="SAF",  # Safety Requirement
                traceability_hints=["FAS_ASSERT", category],
                rationale=f"Safety assertion extracted ({category})"
            )
            requirements.append(req)

        return requirements


class ConfigExtractor:
    """Extracts configuration parameters from C source"""

    CONFIG_PATTERN = re.compile(r'#define\s+(\w+)\s+\((.+?)\)', re.MULTILINE)
    UNIT_PATTERN = re.compile(r'_(\w+)$')  # Extracts unit suffix like _mV, _Hz, etc.

    def extract_requirements(self, content: str, filepath: str) -> List[ExtractedRequirement]:
        """Extract configuration-based requirements"""
        requirements = []

        for match in self.CONFIG_PATTERN.finditer(content):
            param_name = match.group(1)
            param_value = match.group(2).strip()
            line_num = content[:match.start()].count('\n') + 1

            # Extract unit if present
            unit_match = self.UNIT_PATTERN.search(param_name)
            unit = unit_match.group(1) if unit_match else ""

            # Determine confidence based on naming conventions
            confidence = ConfidenceLevel.HIGH.value if unit else ConfidenceLevel.MEDIUM.value

            req = ExtractedRequirement(
                extraction_type=ExtractionType.CONFIG.value,
                content=f"Configuration parameter {param_name} = {param_value}",
                source_file=filepath,
                source_line=line_num,
                confidence=confidence,
                suggested_type="SWE",
                traceability_hints=[param_name, f"unit:{unit}" if unit else ""],
                rationale=f"Configuration parameter extracted"
            )
            requirements.append(req)

        return requirements


class ExtractionEngine:
    """Main extraction engine coordinating all extractors"""

    def __init__(self, module_path: str, module_code: str = "BMS"):
        """Initialize extraction engine"""
        self.module_path = Path(module_path)
        self.module_code = module_code
        self.doxygen = DoxygenParser()
        self.state_machine = StateMachineExtractor()
        self.assertion = AssertionExtractor()
        self.config = ConfigExtractor()
        self.all_requirements = []

    def extract_from_file(self, filepath: Path) -> List[ExtractedRequirement]:
        """Extract requirements from a single file"""
        requirements = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            relative_path = str(filepath.relative_to(self.module_path.parent.parent.parent))

            # Run all extractors
            requirements.extend(self.doxygen.extract_requirements(content, relative_path))
            requirements.extend(self.state_machine.extract_requirements(content, relative_path))
            requirements.extend(self.assertion.extract_requirements(content, relative_path))
            requirements.extend(self.config.extract_requirements(content, relative_path))

            return requirements

        except Exception as e:
            print(f"Error extracting from {filepath}: {e}")
            return []

    def extract_from_module(self) -> Dict[str, Any]:
        """Extract requirements from entire module"""
        requirements = []

        # Find all C/H files in module
        c_files = list(self.module_path.glob("*.c"))
        h_files = list(self.module_path.glob("*.h"))

        for filepath in sorted(c_files + h_files):
            requirements.extend(self.extract_from_file(filepath))

        # Calculate statistics
        high_conf = sum(1 for r in requirements if r.confidence == ConfidenceLevel.HIGH.value)
        medium_conf = sum(1 for r in requirements if r.confidence == ConfidenceLevel.MEDIUM.value)
        low_conf = sum(1 for r in requirements if r.confidence == ConfidenceLevel.LOW.value)

        result = {
            "extraction_id": f"EXT-{self.module_code}-001",
            "module": self.module_code,
            "module_path": str(self.module_path),
            "extracted_at": datetime.now().isoformat() + "Z",
            "requirements": [r.to_dict() for r in requirements],
            "statistics": {
                "total_extracted": len(requirements),
                "high_confidence": high_conf,
                "medium_confidence": medium_conf,
                "low_confidence": low_conf,
                "extraction_types": self._count_by_type(requirements)
            }
        }

        return result

    def _count_by_type(self, requirements: List[ExtractedRequirement]) -> Dict[str, int]:
        """Count requirements by extraction type"""
        counts = {}
        for req in requirements:
            ext_type = req.extraction_type
            counts[ext_type] = counts.get(ext_type, 0) + 1
        return counts

    def generate_report(self, extraction_data: Dict[str, Any]) -> str:
        """Generate markdown extraction report"""
        report = []
        report.append(f"# Extraction Report: {extraction_data['module']}")
        report.append("")
        report.append(f"**Extraction ID**: {extraction_data['extraction_id']}")
        report.append(f"**Module Path**: {extraction_data['module_path']}")
        report.append(f"**Extracted At**: {extraction_data['extracted_at']}")
        report.append("")

        stats = extraction_data['statistics']
        report.append("## Extraction Statistics")
        report.append("")
        report.append(f"- **Total Requirements Extracted**: {stats['total_extracted']}")
        report.append(f"- **High Confidence**: {stats['high_confidence']}")
        report.append(f"- **Medium Confidence**: {stats['medium_confidence']}")
        report.append(f"- **Low Confidence**: {stats['low_confidence']}")
        report.append("")

        report.append("## Extraction by Type")
        report.append("")
        for ext_type, count in stats.get('extraction_types', {}).items():
            report.append(f"- **{ext_type}**: {count}")
        report.append("")

        report.append("## High Confidence Ratio")
        total = stats['total_extracted']
        if total > 0:
            ratio = stats['high_confidence'] / total * 100
            report.append(f"- **{ratio:.1f}%** ({stats['high_confidence']}/{total})")
        report.append("")

        report.append("## Quality Gate Check")
        if total > 0 and stats['high_confidence'] / total >= 0.7:
            report.append("- **PASS**: High confidence ratio >= 70%")
        else:
            report.append("- **FAIL**: High confidence ratio < 70%")

        return '\n'.join(report)


def main():
    """Main entry point for extraction"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: extraction_engine.py <module_path> [module_code] [--report]")
        sys.exit(1)

    module_path = sys.argv[1]
    module_code = sys.argv[2] if len(sys.argv) > 2 else "BMS"
    generate_report = "--report" in sys.argv

    engine = ExtractionEngine(module_path, module_code)
    extraction_data = engine.extract_from_module()

    if generate_report:
        # Output report to stderr, JSON to stdout
        report = engine.generate_report(extraction_data)
        import sys as sys_module
        sys_module.stderr.write(report + "\n")
        print(json.dumps(extraction_data, indent=2))
    else:
        # Output JSON only
        print(json.dumps(extraction_data, indent=2))


if __name__ == "__main__":
    main()
