# PARVIS - Pattern-based Requirements Verification and Implementation System

## Overview

PARVIS is an AI-powered BMS documentation and code generation system designed for the foxBMS project. It provides automated requirements extraction, MISRA C:2012 compliance verification, and intelligent code generation from requirements specifications.

## System Architecture

```
parvis/
├── requirements/          # BMS Requirements Data (648 requirements)
│   ├── config/           # System configuration
│   ├── requirements/     # Extracted and normalized requirements
│   ├── quality/          # Quality metrics and MISRA reports
│   ├── safety/           # ASIL-B safety analysis
│   └── traceability/     # Requirement traceability indexes
├── templates/            # Jinja2 Code Generation Templates
│   ├── state-machine/   # State machine templates
│   ├── configuration/   # Configuration header templates
│   ├── interface/       # API interface templates
│   └── safety/          # Safety assertion templates
├── patterns/            # MISRA C:2012 Patterns
│   └── misra-patterns.json  # 81 MISRA rules and patterns
├── tools/               # Code Generation Tools
│   └── parvis_codegen.py    # Main code generator
└── README.md            # This file
```

## Key Components

### 1. Requirements Database (requirements/)

**Purpose**: Central repository for BMS requirements extracted from foxBMS documentation

**Key Files**:
- `requirements/normalized/master-normalized.json` - All 648 normalized requirements
- `requirements/registry/id-registry.json` - Requirement ID tracking
- `requirements/extracted/*.json` - Module-specific extracted requirements
- `quality/l2-quality-report.md` - Quality metrics report

**Modules Covered**:
- BMS Core (75 requirements)
- Algorithm (110 requirements)
- Drivers (160 requirements)
- Configuration (142 requirements)
- AFE (Analog Front End) (78 requirements)
- SBC (System Basis Chip) (45 requirements)
- Temperature Sensors (38 requirements)

### 2. Code Generation Templates (templates/)

**Purpose**: Jinja2 templates for generating MISRA C:2012 compliant code

**Template Categories**:

#### State Machine Templates
- `state-machine/enum-template.c.jinja` - State enumeration definitions
- `state-machine/transition-template.c.jinja` - State transition logic

#### Configuration Templates
- `configuration/define-template.c.jinja` - Configuration header defines

#### Interface Templates
- `interface/api-template.c.jinja` - API function signatures

#### Safety Templates
- `safety/assertion-template.c.jinja` - FAS_ASSERT safety checks

### 3. MISRA Patterns (patterns/)

**Purpose**: Knowledge base of 81 MISRA C:2012 rules and patterns

**Contents**:
- Rule definitions and rationale
- Code examples (compliant and non-compliant)
- Pattern matching rules for validation
- FAS_ASSERT usage patterns

**Categories**:
- Pointer Safety (11.9, 17.7, 18.1-18.3)
- Type Safety (10.3, 10.4, 10.8)
- Control Flow (15.1-15.7, 16.1-16.7)
- Declarations (8.2-8.14)
- Expressions (12.1-12.5, 13.1-13.6)
- Literals (7.1-7.4)
- Functions (17.1-17.8)
- Side Effects (13.5)

### 4. Code Generator Tool (tools/)

**Purpose**: Python-based code generator with MISRA validation

**Features**:
- Requirement-driven code generation
- Automatic FAS_ASSERT insertion
- MISRA C:2012 pattern validation
- Template selection based on requirement type
- Batch generation support

**Usage**:
```bash
cd parvis/tools
python parvis_codegen.py
```

## Requirements Data Statistics

**Total Requirements**: 648
- Extracted: 648 (100%)
- Normalized: 648 (100%)
- With IDs: 648 (100%)
- Quality Checked: 648 (100%)

**ASIL Coverage**:
- ASIL-B: 485 requirements (74.8%)
- ASIL-A: 98 requirements (15.1%)
- QM: 65 requirements (10.0%)

**Requirement Types**:
- Functional: 412 (63.6%)
- Performance: 98 (15.1%)
- Safety: 85 (13.1%)
- Configuration: 53 (8.2%)

## MISRA C:2012 Compliance

**Total Rules Covered**: 81
**Categories**: 9

**Compliance Focus Areas**:
1. Pointer Safety and NULL checks
2. Unsigned literal suffixes
3. Switch statement default cases
4. Function parameter validation
5. Type conversions and casts
6. Dead code elimination
7. Control flow restrictions

## Code Generation Workflow

### 1. Requirement Definition
Create JSON requirement specification:
```json
{
  "type": "state_machine",
  "requirement_id": "REQ-BMS-001",
  "asil_level": "ASIL-B",
  "module_name": "BMS State Machine",
  "states": [...],
  "transitions": {...}
}
```

### 2. Template Selection
Generator automatically selects template based on requirement type:
- `state_machine` → state-machine templates
- `configuration` → configuration templates
- `interface` → API templates
- `safety` → assertion templates

### 3. Code Generation
```bash
python parvis_codegen.py
```

Generates:
- MISRA-compliant C code
- FAS_ASSERT safety checks
- Proper NULL pointer validation
- Switch default cases
- Unsigned literal suffixes

### 4. Validation
Automatic MISRA validation checks:
- Pointer NULL checks (Rule 11.9)
- Switch default cases (Rule 16.4)
- Unsigned literals (Rule 7.2)

## Quality Metrics

**Documentation Coverage**: 94.2%
- Requirements with detailed descriptions: 611/648
- Requirements with rationale: 589/648
- Requirements with safety notes: 485/648 (ASIL-B)

**Traceability**: 100%
- All requirements have unique IDs
- Module-to-requirement mapping complete
- Source documentation references maintained

**MISRA Compliance**: 81 rules documented
- Pattern examples: 162 (2 per rule)
- Validation rules: 81
- FAS_ASSERT patterns: 23

## Integration with foxBMS

### Requirements Mapping
Requirements are organized by foxBMS module structure:
- `src/app/application/` → BMS Core requirements
- `src/app/algorithm/` → Algorithm requirements
- `src/app/driver/` → Driver requirements
- `src/app/engine/config/` → Configuration requirements

### Code Generation Target
Generated code targets foxBMS coding standards:
- MISRA C:2012 compliance
- FAS_ASSERT macro usage
- Module naming conventions
- Header guard patterns
- Doxygen documentation format

## Tools and Dependencies

### Required
- Python 3.8+
- Jinja2 (pip install jinja2)

### Optional
- cppcheck (for additional MISRA checking)
- git (for version control)

## Development Workflow

### Adding New Requirements
1. Extract requirements from documentation
2. Normalize to standard format
3. Assign unique ID via registry
4. Add to appropriate module JSON
5. Run quality checks

### Creating New Templates
1. Identify requirement pattern
2. Create Jinja2 template in appropriate category
3. Add template mapping to TEMPLATE_TYPES
4. Test with sample requirement
5. Validate generated code

### Updating MISRA Patterns
1. Edit `patterns/misra-patterns.json`
2. Add rule definition, examples, and pattern
3. Update validator in `parvis_codegen.py`
4. Test validation with sample code

## Quality Reports

### Latest Quality Report
Location: `requirements/quality/l2-quality-report.md`

**Key Metrics**:
- Requirement completeness: 94.2%
- ID assignment: 100%
- Duplication rate: <1%
- Transformation accuracy: 98.7%

### MISRA Compliance Report
Location: `quality/reports/` (TBD)

**Tracked Metrics**:
- Rules covered: 81/143 (56.6%)
- Validation patterns: 81
- Code examples: 162

## Version History

**v1.0.0** (2025-12-17)
- Initial PARVIS system creation
- 648 requirements extracted and normalized
- 81 MISRA C:2012 patterns documented
- Code generator with 4 template categories
- Automatic FAS_ASSERT insertion
- MISRA validation framework

## Future Enhancements

### Planned Features
1. Interactive requirement editor
2. Web-based code generator UI
3. Extended MISRA rule coverage (143 rules)
4. Automated test case generation
5. Integration with CI/CD pipeline
6. Real-time code validation
7. Requirement-to-code traceability visualization

### Template Expansion
- Unit test templates
- Integration test templates
- Mock object templates
- Documentation templates

## Support and Documentation

**Primary Documentation**:
- `requirements/README.md` - Requirements system details
- `templates/README.md` - Template usage guide (TBD)
- `tools/README.md` - Code generator manual (TBD)

**Quality Documentation**:
- `quality/l2-quality-report.md` - Current quality metrics
- `quality/misra/` - MISRA compliance reports

**Traceability**:
- `traceability/indexes/` - Requirement indexes
- `traceability/README.md` - Traceability system (TBD)

## Contact

**Project**: foxBMS
**System**: PARVIS
**Version**: 1.0.0
**Date**: 2025-12-17

---

**Note**: This directory is tracked in git (unlike `.moai/` which is gitignored). All PARVIS system files should be committed for team collaboration and version control.
