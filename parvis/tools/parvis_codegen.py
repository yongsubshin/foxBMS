#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARVIS Code Generator Engine

Generates MISRA C:2012 compliant C code for foxBMS using Jinja2 templates.
Supports state machines, configuration, interfaces, and safety assertions.

Author: foxBMS Team
Version: 1.0.0
Date: 2025-12-17
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from jinja2 import Environment, FileSystemLoader, TemplateNotFound
except ImportError:
    print("Error: Jinja2 is required. Install with: pip install jinja2")
    sys.exit(1)


class MISRAValidator:
    """Validates generated code against MISRA C:2012 patterns."""

    def __init__(self, patterns_file: str):
        """Initialize validator with MISRA patterns.

        Args:
            patterns_file: Path to misra-patterns.json
        """
        self.patterns: Dict[str, Any] = {}
        self.load_patterns(patterns_file)

    def load_patterns(self, patterns_file: str) -> None:
        """Load MISRA patterns from JSON file.

        Args:
            patterns_file: Path to patterns JSON file
        """
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Patterns file not found: {patterns_file}")
            self.patterns = {"categories": []}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in patterns file: {e}")
            self.patterns = {"categories": []}

    def validate_pointer_null_check(self, code: str) -> List[str]:
        """Check for proper NULL pointer validation.

        Args:
            code: Generated code to validate

        Returns:
            List of validation warnings
        """
        warnings: List[str] = []

        # Check for implicit NULL checks
        if "if (ptr)" in code or "if (!ptr)" in code:
            warnings.append(
                "MISRA Rule 11.9: Use explicit NULL comparison (ptr != NULL)"
            )

        # Check for FAS_ASSERT usage with pointers
        if "FAS_ASSERT(" in code and "!= NULL" not in code:
            # This is a heuristic check - may have false positives
            pass

        return warnings

    def validate_switch_default(self, code: str) -> List[str]:
        """Check for default case in switch statements.

        Args:
            code: Generated code to validate

        Returns:
            List of validation warnings
        """
        warnings: List[str] = []

        # Count switch statements and default cases
        switch_count = code.count("switch (")
        default_count = code.count("default:")

        if switch_count > default_count:
            warnings.append(
                f"MISRA Rule 16.4: {switch_count - default_count} switch "
                "statement(s) missing default case"
            )

        return warnings

    def validate_unsigned_literals(self, code: str) -> List[str]:
        """Check for proper unsigned literal suffixes.

        Args:
            code: Generated code to validate

        Returns:
            List of validation warnings
        """
        warnings: List[str] = []

        # Pattern: assignment to uint type without 'u' suffix
        # This is a simplified check
        import re
        pattern = r'uint\d+_t\s+\w+\s*=\s*\d+[^u\d]'
        matches = re.findall(pattern, code)

        if matches:
            warnings.append(
                f"MISRA Rule 7.2: {len(matches)} unsigned literal(s) "
                "may be missing 'u' suffix"
            )

        return warnings

    def validate(self, code: str) -> Dict[str, Any]:
        """Run all MISRA validations on generated code.

        Args:
            code: Generated code to validate

        Returns:
            Validation result with warnings and status
        """
        all_warnings: List[str] = []

        all_warnings.extend(self.validate_pointer_null_check(code))
        all_warnings.extend(self.validate_switch_default(code))
        all_warnings.extend(self.validate_unsigned_literals(code))

        return {
            "valid": len(all_warnings) == 0,
            "warning_count": len(all_warnings),
            "warnings": all_warnings
        }


class FASAssertInserter:
    """Automatically inserts FAS_ASSERT statements for safety validation."""

    def __init__(self):
        """Initialize the assertion inserter."""
        self.insertion_rules = [
            {
                "pattern": "pointer parameter",
                "template": "FAS_ASSERT({param} != NULL);"
            },
            {
                "pattern": "array index",
                "template": "FAS_ASSERT({index} < {size});"
            },
            {
                "pattern": "enum value",
                "template": "FAS_ASSERT((uint8_t){value} < {max});"
            }
        ]

    def generate_pointer_assertions(
        self, parameters: List[Dict[str, str]]
    ) -> List[str]:
        """Generate FAS_ASSERT statements for pointer parameters.

        Args:
            parameters: List of function parameters

        Returns:
            List of assertion statements
        """
        assertions: List[str] = []

        for param in parameters:
            param_type = param.get("type", "")
            param_name = param.get("name", "")

            # Check if parameter is a pointer
            if "*" in param_type and param_name:
                assertions.append(
                    f"    /* FAS_ASSERT: {param_name} must not be NULL */\n"
                    f"    FAS_ASSERT({param_name} != NULL);"
                )

        return assertions

    def generate_range_assertions(
        self,
        variable: str,
        min_value: Union[int, str],
        max_value: Union[int, str],
        var_type: str = "uint32_t"
    ) -> str:
        """Generate FAS_ASSERT for range validation.

        Args:
            variable: Variable name to check
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            var_type: Variable type for casting

        Returns:
            Assertion statement
        """
        return (
            f"    /* FAS_ASSERT: {variable} must be within valid range */\n"
            f"    FAS_ASSERT(({variable} >= ({var_type}){min_value}) && "
            f"({variable} <= ({var_type}){max_value}));"
        )


class ParvisCodeGenerator:
    """Main code generator for PARVIS system."""

    TEMPLATE_TYPES = {
        "state_machine_enum": "state-machine/enum-template.c.jinja",
        "state_machine_transition": "state-machine/transition-template.c.jinja",
        "configuration": "configuration/define-template.c.jinja",
        "interface": "interface/api-template.c.jinja",
        "safety": "safety/assertion-template.c.jinja"
    }

    def __init__(
        self,
        templates_dir: str,
        patterns_file: str,
        output_dir: str
    ):
        """Initialize the code generator.

        Args:
            templates_dir: Path to Jinja2 templates directory
            patterns_file: Path to MISRA patterns JSON file
            output_dir: Path for generated output files
        """
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Add custom filters
        self.env.filters["upper"] = str.upper
        self.env.filters["lower"] = str.lower
        self.env.filters["title"] = str.title

        # Initialize components
        self.validator = MISRAValidator(patterns_file)
        self.assert_inserter = FASAssertInserter()

        # Generation statistics
        self.stats = {
            "files_generated": 0,
            "lines_generated": 0,
            "validation_warnings": 0
        }

    def load_requirement(self, requirement_file: str) -> Dict[str, Any]:
        """Load requirement specification from JSON file.

        Args:
            requirement_file: Path to requirement JSON file

        Returns:
            Parsed requirement specification
        """
        try:
            with open(requirement_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Requirement file not found: {requirement_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in requirement file: {e}")

    def select_template(
        self,
        requirement: Dict[str, Any]
    ) -> str:
        """Select appropriate template based on requirement type.

        Args:
            requirement: Requirement specification

        Returns:
            Template file path
        """
        req_type = requirement.get("type", "").lower()

        # Map requirement types to templates
        type_mapping = {
            "state_machine": "state_machine_enum",
            "state_enum": "state_machine_enum",
            "state_transition": "state_machine_transition",
            "configuration": "configuration",
            "config": "configuration",
            "define": "configuration",
            "interface": "interface",
            "api": "interface",
            "safety": "safety",
            "assertion": "safety"
        }

        template_key = type_mapping.get(req_type)
        if template_key is None:
            raise ValueError(f"Unknown requirement type: {req_type}")

        return self.TEMPLATE_TYPES[template_key]

    def prepare_context(
        self,
        requirement: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare template context from requirement.

        Args:
            requirement: Requirement specification

        Returns:
            Template context dictionary
        """
        # Base context with common fields
        context: Dict[str, Any] = {
            "generation_date": datetime.now().strftime("%Y-%m-%d"),
            "version": requirement.get("version", "v1.0.0"),
            "requirement_id": requirement.get("requirement_id", "REQ-XXX-XXX"),
            "asil_level": requirement.get("asil_level", "ASIL-B"),
            "module_group": requirement.get("module_group", "DRIVER"),
            "prefix": requirement.get("prefix", "MOD"),
            "module_name": requirement.get("module_name", "Module"),
            "filename": requirement.get("filename", "module.c"),
            "header_file": requirement.get("header_file", "module.h"),
            "brief_description": requirement.get(
                "brief_description",
                "Auto-generated module"
            ),
            "detailed_description": requirement.get(
                "detailed_description",
                ""
            )
        }

        # Add type-specific fields
        req_type = requirement.get("type", "").lower()

        if req_type in ["state_machine", "state_enum", "state_transition"]:
            context.update({
                "state_machine_name": requirement.get(
                    "state_machine_name",
                    "StateMachine"
                ),
                "states": requirement.get("states", []),
                "transitions": requirement.get("transitions", {}),
                "initial_state": requirement.get("initial_state", "IDLE"),
                "max_state_time_ms": requirement.get("max_state_time_ms", 60000),
                "min_transition_interval_ms": requirement.get(
                    "min_transition_interval_ms", 10
                ),
                "include_validation_functions": requirement.get(
                    "include_validation_functions", True
                )
            })

        elif req_type in ["configuration", "config", "define"]:
            context.update({
                "guard_name": requirement.get(
                    "guard_name",
                    f"{context['prefix'].upper()}_CFG_H_"
                ),
                "version_major": requirement.get("version_major", 1),
                "version_minor": requirement.get("version_minor", 0),
                "version_patch": requirement.get("version_patch", 0),
                "timing_defines": requirement.get("timing_defines", []),
                "size_defines": requirement.get("size_defines", []),
                "threshold_defines": requirement.get("threshold_defines", []),
                "feature_defines": requirement.get("feature_defines", []),
                "include_runtime_validation": requirement.get(
                    "include_runtime_validation", True
                )
            })

        elif req_type in ["interface", "api"]:
            context.update({
                "guard_name": requirement.get(
                    "guard_name",
                    f"{context['prefix'].upper()}_H_"
                ),
                "api_version_major": requirement.get("api_version_major", 1),
                "api_version_minor": requirement.get("api_version_minor", 0),
                "additional_includes": requirement.get("additional_includes", []),
                "constants": requirement.get("constants", []),
                "typedefs": requirement.get("typedefs", []),
                "structures": requirement.get("structures", []),
                "callbacks": requirement.get("callbacks", []),
                "functions": requirement.get("functions", []),
                "include_diagnostics": requirement.get("include_diagnostics", True)
            })

        elif req_type in ["safety", "assertion"]:
            context.update({
                "range_checks": requirement.get("range_checks", []),
                "enum_checks": requirement.get("enum_checks", []),
                "safety_checks": requirement.get("safety_checks", [])
            })

        return context

    def generate(
        self,
        requirement: Union[str, Dict[str, Any]],
        output_file: Optional[str] = None
    ) -> str:
        """Generate code from requirement specification.

        Args:
            requirement: Path to requirement JSON or requirement dict
            output_file: Optional output file path

        Returns:
            Generated code string
        """
        # Load requirement if path provided
        if isinstance(requirement, str):
            requirement = self.load_requirement(requirement)

        # Select template
        template_path = self.select_template(requirement)

        try:
            template = self.env.get_template(template_path)
        except TemplateNotFound:
            raise ValueError(f"Template not found: {template_path}")

        # Prepare context
        context = self.prepare_context(requirement)

        # Render template
        generated_code = template.render(**context)

        # Validate generated code
        validation = self.validator.validate(generated_code)
        if validation["warnings"]:
            print("MISRA Validation Warnings:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")

        # Update statistics
        self.stats["files_generated"] += 1
        self.stats["lines_generated"] += generated_code.count('\n')
        self.stats["validation_warnings"] += validation["warning_count"]

        # Write output file if specified
        if output_file:
            output_path = self.output_dir / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            print(f"Generated: {output_path}")

        return generated_code

    def generate_batch(
        self,
        requirements_dir: str,
        pattern: str = "*.json"
    ) -> Dict[str, str]:
        """Generate code for all requirements in directory.

        Args:
            requirements_dir: Directory containing requirement JSON files
            pattern: Glob pattern for requirement files

        Returns:
            Dictionary mapping requirement files to generated code
        """
        requirements_path = Path(requirements_dir)
        results: Dict[str, str] = {}

        for req_file in requirements_path.glob(pattern):
            try:
                requirement = self.load_requirement(str(req_file))
                output_file = requirement.get(
                    "filename",
                    req_file.stem + ".c"
                )
                code = self.generate(requirement, output_file)
                results[str(req_file)] = code
            except Exception as e:
                print(f"Error processing {req_file}: {e}")
                results[str(req_file)] = f"ERROR: {e}"

        return results

    def get_statistics(self) -> Dict[str, int]:
        """Get generation statistics.

        Returns:
            Statistics dictionary
        """
        return self.stats.copy()


def create_sample_requirement() -> Dict[str, Any]:
    """Create a sample requirement for testing.

    Returns:
        Sample requirement dictionary
    """
    return {
        "type": "state_machine",
        "requirement_id": "REQ-BMS-001",
        "asil_level": "ASIL-B",
        "module_group": "BMS",
        "prefix": "BMS",
        "module_name": "BMS State Machine",
        "filename": "bms_state_machine.c",
        "header_file": "bms_state_machine.h",
        "brief_description": "BMS main state machine implementation",
        "detailed_description": "Implements the battery management system state machine with safety transitions.",
        "state_machine_name": "BMS_StateMachine",
        "version": "v1.0.0",
        "states": [
            {
                "name": "UNINITIALIZED",
                "value": 0,
                "description": "System not yet initialized"
            },
            {
                "name": "INITIALIZATION",
                "value": 1,
                "description": "System initialization in progress"
            },
            {
                "name": "STANDBY",
                "value": 2,
                "description": "System in standby mode"
            },
            {
                "name": "PRECHARGE",
                "value": 3,
                "description": "Precharge sequence active"
            },
            {
                "name": "NORMAL",
                "value": 4,
                "description": "Normal operation mode"
            },
            {
                "name": "ERROR",
                "value": 5,
                "description": "Error state - safe mode"
            }
        ],
        "transitions": {
            "UNINITIALIZED": ["INITIALIZATION"],
            "INITIALIZATION": ["STANDBY", "ERROR"],
            "STANDBY": ["PRECHARGE", "ERROR"],
            "PRECHARGE": ["NORMAL", "STANDBY", "ERROR"],
            "NORMAL": ["STANDBY", "ERROR"],
            "ERROR": ["STANDBY"]
        },
        "initial_state": "UNINITIALIZED",
        "max_state_time_ms": 60000,
        "min_transition_interval_ms": 10
    }


def main():
    """Main entry point for code generator."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    templates_dir = project_root / "parvis" / "templates"
    patterns_file = project_root / "parvis" / "patterns" / "misra-patterns.json"
    output_dir = project_root / "parvis" / "generated"

    print("PARVIS Code Generator")
    print("=" * 50)
    print(f"Templates: {templates_dir}")
    print(f"Patterns:  {patterns_file}")
    print(f"Output:    {output_dir}")
    print()

    # Initialize generator
    generator = ParvisCodeGenerator(
        templates_dir=str(templates_dir),
        patterns_file=str(patterns_file),
        output_dir=str(output_dir)
    )

    # Generate sample code
    print("Generating sample state machine...")
    sample_req = create_sample_requirement()

    # Generate enum template
    sample_req["type"] = "state_enum"
    enum_code = generator.generate(
        sample_req,
        "sample/bms_state_enum.c"
    )

    # Generate transition template
    sample_req["type"] = "state_transition"
    transition_code = generator.generate(
        sample_req,
        "sample/bms_state_transition.c"
    )

    # Print statistics
    stats = generator.get_statistics()
    print()
    print("Generation Statistics:")
    print(f"  Files generated:      {stats['files_generated']}")
    print(f"  Lines generated:      {stats['lines_generated']}")
    print(f"  Validation warnings:  {stats['validation_warnings']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
