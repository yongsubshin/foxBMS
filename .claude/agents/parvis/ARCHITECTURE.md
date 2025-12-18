# BMS V-Model Agent Architecture

Version: 1.0.0
Last Updated: 2025-12-15
Compliance: ISO 26262 ASIL-D, MISRA C:2012, ASPICE Level 2+

---

## Executive Summary

This document defines the complete AI agent architecture for Battery Management System (BMS) development following automotive V-Model methodology. The system ensures full compliance with ISO 26262, MISRA C:2012, and Automotive SPICE requirements while enabling efficient reverse engineering and requirement management for legacy codebases like foxBMS.

---

## Architecture Overview

### V-Model Alignment

The agent architecture maps directly to the V-Model development phases:

Left Side (Development):
- Requirements Analysis: PARVIS-AISpec agents extract and normalize requirements
- System Design: Architecture and safety analysis agents define system structure
- Software Design: Detailed design with traceability to requirements
- Implementation: PARVIS-AICoder agents ensure compliant code generation

Right Side (Verification):
- Unit Testing: PARVIS-AIVerify agents generate and execute unit tests
- Integration Testing: Component integration verification
- System Testing: End-to-end validation with safety verification
- Acceptance Testing: Final validation against original requirements

Central Coordination:
- PARVIS-AI-Orchestrator manages all phases and ensures traceability

### Agent Hierarchy

```
PARVIS-AI-Orchestrator (Master Coordinator)
    |
    +-- PARVIS-AISpec (Specification Phase)
    |       +-- parvis-aispec-excel         (Excel specification parsing)
    |       +-- parvis-aispec-pdf           (PDF document analysis)
    |       +-- parvis-aispec-code          (Code-to-requirement extraction)
    |       +-- parvis-aispec-transformer   (Unified normalization)
    |       +-- parvis-aispec-reqid         (Requirement ID management)
    |       +-- parvis-aispec-trace         (Traceability matrix)
    |       +-- parvis-aispec-safety        (ISO 26262 HARA support)
    |
    +-- PARVIS-AICoder (Coding Phase)
    |       +-- parvis-aicoder-misra        (MISRA C:2012 checking)
    |       +-- parvis-aicoder-refactor     (MISRA violation remediation)
    |       +-- parvis-aicoder-doxygen      (Documentation generation)
    |       +-- parvis-aicoder-safety       (Safety annotation)
    |       +-- parvis-aicoder-generator    (Code generation from design)
    |
    +-- PARVIS-AIVerify (Verification Phase)
    |       +-- parvis-aiverify-unittest    (Unit test generation)
    |       +-- parvis-aiverify-integration (Integration test design)
    |       +-- parvis-aiverify-coverage    (Coverage analysis)
    |       +-- parvis-aiverify-safety      (Safety test validation)
    |       +-- parvis-aiverify-report      (Test report generation)
    |       +-- parvis-aiverify-misra-report (MISRA compliance comparison)
    |
    +-- PARVIS-AIDoc (Documentation Phase)
            +-- parvis-aidoc-aspice         (ASPICE work products)
            +-- parvis-aidoc-safety         (Safety case documentation)
            +-- parvis-aidoc-trace          (Traceability reports)
            +-- parvis-aidoc-change         (Change impact analysis)
```

---

## ID Naming Convention System

### Requirement ID Format

Base Format: [PROJECT]-[TYPE]-[MODULE]-[SEQ]

Components:
- PROJECT: 4-character project identifier (e.g., FBMS for foxBMS)
- TYPE: Requirement type code (see Type Codes below)
- MODULE: Module identifier (see Module Codes below)
- SEQ: 3-digit sequence number (001-999)

Type Codes:
- SYS: System Requirement (ISO 26262 Part 3)
- HWE: Hardware Requirement (ISO 26262 Part 5)
- SWE: Software Requirement (ISO 26262 Part 6)
- TSC: Technical Safety Concept
- FSR: Functional Safety Requirement
- HSI: Hardware-Software Interface
- ARC: Architecture Requirement
- DES: Design Requirement
- TST: Test Requirement

Module Codes for foxBMS:
- BMS: Battery Management System (main control)
- SOC: State of Charge
- SOE: State of Energy
- SOH: State of Health
- SOF: State of Function
- BAL: Cell Balancing
- AFE: Analog Front End
- CAN: CAN Communication
- DIAG: Diagnostics
- CONT: Contactor Control
- IMD: Insulation Monitoring
- TEMP: Temperature Monitoring
- VOLT: Voltage Monitoring
- CURR: Current Monitoring
- ALG: Algorithm
- DB: Database
- TASK: Task Management
- SYS: System Engine

Examples:
- SW-REQ-DIAG-001: Software requirement for diagnostics module
- FSR-BMS-015: Functional safety requirement for BMS
- HSI-SOC-003: HW/SW interface requirement for State of Charge

### Design ID Format

Base Format: SW-ARCH-[MODULE]-[SEQ]

Examples:
- SW-ARCH-SOC-001: Design specification for SOC calculation
- SW-ARCH-AFE-012: Design specification for AFE communication

### Test Case ID Format

Base Format: [LEVEL]-[MODULE]-[SEQ]

Level Codes:
- UT: Unit Test
- IT: Integration Test
- TC: Test Case

Examples:
- UT-SOC-001: Unit test for SOC module
- IT-AFE-005: Integration test for AFE
- TC-BMS-001: Test case for BMS module

### System Requirement ID Format

Base Format: SYS-REQ-[SEQ]

Examples:
- SYS-REQ-001: Battery State Estimation
- SYS-REQ-002: Analog Front End Interface
- SYS-REQ-007: BMS State Machine

---

## Traceability Matrix Structure

### Bidirectional Traceability Model

```
System Requirements (SYS)
        |
        v
Safety Requirements (FSR) <--> Technical Safety Concept (TSC)
        |
        v
Software Requirements (SWE) <--> Hardware-Software Interface (HSI)
        |
        v
Architecture Design (ARC)
        |
        v
Detailed Design (DES)
        |
        v
Source Code (Implementation)
        |
        v
Unit Tests (UT) <--> Test Requirements (TST)
        |
        v
Integration Tests (IT)
        |
        v
System Tests (ST)
        |
        v
Acceptance Tests (AT)
```

### Traceability Matrix Format

The traceability matrix is stored in JSON format with the following structure:

Matrix Entry Structure:
- source_id: Source artifact ID
- source_type: Type of source artifact (SYS, SWE, DES, etc.)
- target_id: Target artifact ID
- target_type: Type of target artifact
- link_type: Type of relationship (derives, implements, verifies, satisfies)
- status: Link validation status (valid, pending, broken)
- created_date: Timestamp of link creation
- modified_date: Timestamp of last modification
- evidence: Reference to verification evidence
- rationale: Justification for the link

Link Types:
- derives: Higher-level requirement is source of lower-level requirement
- implements: Design or code implements a requirement
- verifies: Test case verifies a requirement or design
- satisfies: Implementation satisfies a safety requirement
- allocates: Requirement is allocated to a component
- refines: Lower-level artifact refines higher-level artifact

### Storage Location

Traceability data is stored in: .claude/parvis-data/traceability/
- matrix.json: Complete traceability matrix
- requirements/: Individual requirement files
- tests/: Test case mappings
- safety/: Safety-related traceability

---

## Agent Definitions Summary

### Phase 1: PARVIS-AISpec Agents (Specification)

parvis-aispec-excel:
- Purpose: Parse Excel-based specification documents
- Input: Excel files with requirement tables
- Output: Normalized requirement JSON
- Compliance: ASPICE SWE.1

parvis-aispec-pdf:
- Purpose: Extract requirements from PDF documents
- Input: PDF specification documents
- Output: Normalized requirement JSON
- Compliance: ASPICE SWE.1

parvis-aispec-code (CRITICAL):
- Purpose: Reverse engineer requirements from source code
- Input: C source files with Doxygen comments
- Output: Extracted requirements with traceability tags
- Compliance: ISO 26262-6, ASPICE SWE.1
- Special Features: Analyzes state machines, safety assertions, and module interfaces

parvis-aispec-transformer:
- Purpose: Normalize and unify requirements from all sources
- Input: Raw requirements from excel, pdf, and code agents
- Output: Unified requirement database with assigned IDs
- Compliance: ASPICE SWE.1

parvis-aispec-reqid:
- Purpose: Generate and manage requirement IDs
- Input: Requirement content and module classification
- Output: Unique requirement IDs following naming convention
- Compliance: ASPICE SWE.1, ISO 26262-8

parvis-aispec-trace:
- Purpose: Create and maintain bidirectional traceability matrix
- Input: Requirements, designs, code, and test artifacts
- Output: Complete traceability matrix with gap analysis
- Compliance: ASPICE SWE.1, ISO 26262-8

parvis-aispec-safety:
- Purpose: Support ISO 26262 HARA and safety analysis
- Input: System requirements and hazard information
- Output: ASIL classification, safety goals, and FSR derivation
- Compliance: ISO 26262-3, ISO 26262-4

### Phase 2: PARVIS-AICoder Agents (Coding)

parvis-aicoder-misra:
- Purpose: Check MISRA C:2012 compliance
- Input: C source files
- Output: Violation report with rule references
- Compliance: MISRA C:2012, ISO 26262-6
- Integration: Interfaces with Axivion Bauhaus Suite

parvis-aicoder-refactor:
- Purpose: Auto-remediate MISRA violations
- Input: Violation report and source files
- Output: Corrected source files with change documentation
- Compliance: MISRA C:2012
- Safety: Preserves functional behavior, maintains traceability

parvis-aicoder-doxygen:
- Purpose: Generate and maintain Doxygen documentation
- Input: Source files and requirement links
- Output: Annotated source with Doxygen comments
- Compliance: foxBMS coding guidelines

parvis-aicoder-safety:
- Purpose: Add safety-critical code annotations
- Input: Source files and safety requirements
- Output: Annotated source with ASIL markers and assertions
- Compliance: ISO 26262-6

parvis-aicoder-generator:
- Purpose: Generate code from detailed design
- Input: Design specifications
- Output: MISRA-compliant C code skeleton
- Compliance: MISRA C:2012, ISO 26262-6

### Phase 3: PARVIS-AIVerify Agents (Verification)

parvis-aiverify-unittest:
- Purpose: Generate unit tests from requirements
- Input: Software requirements and design specs
- Output: Unit test cases with traceability
- Compliance: ISO 26262-6, ASPICE SWE.4

parvis-aiverify-integration:
- Purpose: Design integration tests
- Input: Architecture design and interface specs
- Output: Integration test cases
- Compliance: ISO 26262-6, ASPICE SWE.5

parvis-aiverify-coverage:
- Purpose: Analyze test coverage metrics
- Input: Test results and source code
- Output: Coverage report (statement, branch, MC/DC)
- Compliance: ISO 26262-6 Table 9

parvis-aiverify-safety:
- Purpose: Validate safety test completeness
- Input: Safety requirements and test results
- Output: Safety validation report
- Compliance: ISO 26262-6, ISO 26262-4

parvis-aiverify-report:
- Purpose: Generate comprehensive test reports
- Input: All test results and coverage data
- Output: ASPICE-compliant test reports
- Compliance: ASPICE SWE.4, SWE.5, SWE.6

parvis-aiverify-misra-report:
- Purpose: Compare before/after MISRA C:2012 scans and evaluate compliance improvements
- Input: Before and after MISRA violation reports (JSON)
- Output: Comparison report with compliance metrics, quality gate status, and recommendations
- Compliance: MISRA C:2012, ISO 26262-6
- Features: Violation classification, trend analysis, JSON/Markdown/HTML output

### Phase 4: PARVIS-AIDoc Agents (Documentation)

parvis-aidoc-aspice:
- Purpose: Generate ASPICE work products
- Input: Development artifacts from all phases
- Output: ASPICE-compliant work product documents
- Compliance: Automotive SPICE PAM 3.1

parvis-aidoc-safety:
- Purpose: Generate safety case documentation
- Input: Safety analysis and verification results
- Output: Safety case, safety manual, safety reports
- Compliance: ISO 26262-2

parvis-aidoc-trace:
- Purpose: Generate traceability reports
- Input: Traceability matrix
- Output: Traceability reports with gap analysis
- Compliance: ISO 26262-8, ASPICE

parvis-aidoc-change:
- Purpose: Perform change impact analysis
- Input: Proposed changes and traceability matrix
- Output: Impact analysis report with affected artifacts
- Compliance: ISO 26262-8

---

## PARVIS-AI-Orchestrator Design

### Primary Mission

Coordinate V-Model development phases, enforce quality gates, and ensure complete traceability for ISO 26262 and ASPICE compliance.

### Core Capabilities

Phase Management:
- Track development phase status for each module
- Enforce phase entry and exit criteria
- Manage parallel development across modules

Quality Gate Enforcement:
- Define and verify quality gate criteria for each phase
- Block phase transitions on unmet criteria
- Generate quality gate reports

Traceability Oversight:
- Ensure bidirectional traceability at all times
- Detect and report traceability gaps
- Trigger re-analysis on artifact changes

ASPICE Process Management:
- Track work product completion status
- Ensure process compliance evidence
- Generate ASPICE assessment readiness reports

### Quality Gates

Requirement Phase Gate:
- All requirements have unique IDs
- All requirements are classified (functional, safety, interface)
- Safety requirements have ASIL classification
- Traceability to parent requirements verified

Design Phase Gate:
- All requirements allocated to design elements
- Design review completed
- Hazard analysis updated
- Interface specifications complete

Implementation Phase Gate:
- MISRA C:2012 mandatory rules passed (zero violations)
- MISRA C:2012 required rules reviewed (deviations documented)
- Doxygen documentation complete
- Safety annotations verified

Unit Test Phase Gate:
- All requirements covered by tests
- Statement coverage greater than 80%
- Branch coverage greater than 80%
- Safety requirements have MC/DC coverage

Integration Test Phase Gate:
- Interface tests complete
- Integration coverage targets met
- No critical defects open

System Test Phase Gate:
- All acceptance criteria verified
- Safety validation complete
- Traceability matrix complete
- ASPICE evidence package ready

---

## Integration with foxBMS

### foxBMS Module Mapping

The agent system maps to foxBMS modules as follows:

Application Layer:
- BMS (bms.c, bms.h): Main state machine control
- SOA (soa.c): Safe Operating Area monitoring
- BAL (bal.c): Cell balancing control
- Algorithm (algorithm.c): State estimation (SOC, SOE, SOH, SOF)
- Plausibility (plausibility.c): Measurement plausibility checks
- Redundancy (redundancy.c): Redundant measurement handling

Engine Layer:
- Database (database.c): Shared data management
- Diagnostics (diag.c): Error handling and reporting
- System (sys.c): System state control
- System Monitor (sys_mon.c): Task monitoring

Driver Layer:
- AFE drivers (adi, ltc, maxim, nxp, ti): Analog Front End
- CAN (can.c): CAN communication
- Contactor (contactor.c): Contactor control
- IMD (imd.c): Insulation monitoring
- Temperature sensors (ts.c): Temperature measurement
- Current sensors: Current measurement

### foxBMS-Specific Requirement Extraction

The parvis-aispec-code agent will analyze:
- State machine definitions in bms.c
- Diagnostic event definitions in diag_cfg.c
- Safety-critical thresholds in battery_cell_cfg.c
- CAN message definitions
- Algorithm parameters and limits

### Axivion Integration

The parvis-aicoder-misra agent integrates with existing Axivion configuration:
- Uses rule_config_c.json for MISRA checking
- Leverages axivion_preinc.h for analysis setup
- Maintains compatibility with CI/CD pipeline

---

## Implementation Roadmap

### Phase 1: Foundation (Priority: High)

Step 1.1: Create parvis-aispec-code agent
- Implement Doxygen comment parsing
- Extract state machine requirements
- Build initial requirement database

Step 1.2: Create parvis-aispec-reqid agent
- Implement ID generation algorithm
- Create ID registry and conflict detection
- Build module classification rules

Step 1.3: Create parvis-aispec-trace agent
- Implement traceability matrix structure
- Build link creation and validation
- Create gap detection algorithm

### Phase 2: Code Quality (Priority: High)

Step 2.1: Create parvis-aicoder-misra agent
- Integrate with Axivion configuration
- Implement violation parsing
- Build deviation documentation workflow

Step 2.2: Create parvis-aicoder-refactor agent
- Implement safe refactoring patterns
- Build change verification
- Create rollback capability

Step 2.3: Create parvis-aicoder-doxygen agent
- Implement template-based annotation
- Build requirement linking
- Create API documentation generation

### Phase 3: Verification (Priority: Medium)

Step 3.1: Create parvis-aiverify-unittest agent
- Implement test case generation from requirements
- Build Unity/CMock test framework integration
- Create coverage mapping

Step 3.2: Create parvis-aiverify-coverage agent
- Implement coverage parsing
- Build coverage gap analysis
- Create coverage reports

Step 3.3: Create parvis-aiverify-report agent
- Implement report templates
- Build ASPICE format output
- Create summary dashboards

### Phase 4: Orchestration (Priority: High)

Step 4.1: Create PARVIS-AI-Orchestrator
- Implement V-Model phase tracking
- Build quality gate engine
- Create workflow coordination

Step 4.2: Create parvis-aidoc-aspice agent
- Implement work product templates
- Build evidence collection
- Create assessment reports

Step 4.3: Create parvis-aidoc-change agent
- Implement impact analysis algorithm
- Build change notification
- Create approval workflow

### Phase 5: Safety Extension (Priority: Medium)

Step 5.1: Create parvis-aispec-safety agent
- Implement HARA support
- Build ASIL classification
- Create safety goal derivation

Step 5.2: Create parvis-aicoder-safety agent
- Implement safety annotation
- Build assertion generation
- Create defensive programming patterns

Step 5.3: Create parvis-aiverify-safety agent
- Implement safety test validation
- Build evidence collection
- Create safety reports

---

## File Structure

The agent system creates the following file structure:

```
.claude/parvis-data/
    +-- config/
    |       +-- agent-config.json       (Agent configuration)
    |       +-- id-registry.json        (ID allocation registry)
    |       +-- module-mapping.json     (foxBMS module mapping)
    |
    +-- requirements/
    |       +-- extracted/              (Raw extracted requirements)
    |       +-- normalized/             (Normalized requirements)
    |       +-- safety/                 (Safety requirements)
    |
    +-- traceability/
    |       +-- matrix.json             (Complete traceability matrix)
    |       +-- reports/                (Traceability reports)
    |
    +-- design/
    |       +-- architecture/           (Architecture documents)
    |       +-- detailed/               (Detailed design)
    |
    +-- tests/
    |       +-- unit/                   (Unit test cases)
    |       +-- integration/            (Integration tests)
    |       +-- coverage/               (Coverage reports)
    |
    +-- documentation/
    |       +-- aspice/                 (ASPICE work products)
    |       +-- safety/                 (Safety documentation)
    |       +-- api/                    (API documentation)
    |
    +-- quality/
            +-- gates/                  (Quality gate status)
            +-- misra/                  (MISRA reports)
            +-- reviews/                (Review records)
```

---

## Compliance Mapping

### ISO 26262 Part 6 Coverage

The agent system supports the following ISO 26262-6 clauses:

Clause 5 (Initiation of product development at software level):
- Covered by: PARVIS-AI-Orchestrator, parvis-aidoc-aspice

Clause 6 (Specification of software safety requirements):
- Covered by: parvis-aispec-safety, parvis-aispec-code

Clause 7 (Software architectural design):
- Covered by: parvis-aispec-trace, parvis-aidoc-aspice

Clause 8 (Software unit design and implementation):
- Covered by: parvis-aicoder-misra, parvis-aicoder-safety

Clause 9 (Software unit verification):
- Covered by: parvis-aiverify-unittest, parvis-aiverify-coverage

Clause 10 (Software integration and verification):
- Covered by: parvis-aiverify-integration

Clause 11 (Testing of embedded software):
- Covered by: parvis-aiverify-safety, parvis-aiverify-report

### ASPICE Coverage

Process Area SWE (Software Engineering):
- SWE.1: Covered by parvis-aispec agents
- SWE.2: Covered by parvis-aispec-trace
- SWE.3: Covered by parvis-aicoder agents
- SWE.4: Covered by parvis-aiverify-unittest
- SWE.5: Covered by parvis-aiverify-integration
- SWE.6: Covered by parvis-aiverify-report

### MISRA C:2012 Coverage

The parvis-aicoder-misra agent checks all MISRA C:2012 rules:
- Mandatory Rules: All checked, zero deviations allowed
- Required Rules: All checked, deviations require documentation
- Advisory Rules: Selectively checked based on project policy

---

## Version History

Version 1.0.0 (2025-12-15):
- Initial architecture definition
- Complete agent hierarchy design
- ID naming convention specification
- Traceability matrix design
- Implementation roadmap
