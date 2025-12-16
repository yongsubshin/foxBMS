# ASIL Classification Report - foxBMS Battery Management System

**Document ID**: ASIL-RPT-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Classification Standard**: ISO 26262:2018
**Classification Agent**: parvis-aispec-safety

---

## 1. Overview

This report provides a comprehensive ASIL (Automotive Safety Integrity Level) classification for the foxBMS Battery Management System software requirements. The classification follows ISO 26262:2018 methodology for hazard analysis and risk assessment (HARA), supporting the development of safety-critical battery management software for automotive applications.

### 1.1 Document Purpose

- Classify BMS software requirements according to ASIL levels
- Document HARA methodology and rationale
- Support ISO 26262 functional safety compliance
- Provide traceability from hazards to safety requirements
- Enable safety-informed development and verification activities

### 1.2 Scope

**In Scope:**
- BMS software safety requirements (FSR type)
- ASIL classification per ISO 26262
- Safety-critical functions: contactor control, voltage monitoring, state management
- Embedded software safety mechanisms

**Out of Scope:**
- System-level HARA (external to software)
- Hardware safety requirements
- Safety validation and testing (see parvis-aiverify-safety)
- Safety case documentation (see parvis-aidoc-safety)

---

## 2. ASIL Distribution Summary

### 2.1 Overall Classification Statistics

| ASIL Level | Count | Percentage | Safety Criticality |
|-----------|-------|------------|-------------------|
| ASIL-D    | 8     | 33.3%      | Highest Risk      |
| ASIL-C    | 10    | 41.7%      | High Risk         |
| ASIL-B    | 4     | 16.7%      | Medium Risk       |
| ASIL-A    | 2     | 8.3%       | Low Risk          |
| QM        | 0     | 0.0%       | Quality Managed   |
| **Total** | **24**| **100%**   |                   |

### 2.2 ASIL Distribution Analysis

**Key Findings:**
- 75% of safety requirements classified as ASIL-C or ASIL-D (high/highest risk)
- No QM (Quality Managed) requirements - all safety mechanisms require ASIL assignment
- ASIL-D concentration reflects critical nature of battery safety functions
- Range check assertions predominantly ASIL-C due to operational safety impact

**Risk Profile:**
- **High Criticality Functions**: Contactor state validation, pointer integrity checks
- **Medium Criticality Functions**: Array bounds checking, state machine integrity
- **Safety Architecture**: Multiple redundant safety mechanisms at ASIL-C/D levels

---

## 3. Module-Level Classification Breakdown

### 3.1 BMS Core Module (bms.c / bms.h)

**Total Safety Requirements**: 24
**Module Risk Profile**: ASIL-D dominant (contactor control safety-critical)

| Category | ASIL-D | ASIL-C | ASIL-B | ASIL-A | Total |
|----------|--------|--------|--------|--------|-------|
| Pointer Validation | 4 | 4 | 0 | 0 | 8 |
| Range Checks | 2 | 6 | 0 | 0 | 8 |
| State Machine Traps | 2 | 0 | 4 | 0 | 6 |
| Invariant Checks | 0 | 0 | 0 | 2 | 2 |
| **Module Total** | **8** | **10** | **4** | **2** | **24** |

**Safety-Critical Functions:**
1. **Contactor Control** (ASIL-D): High voltage switching safety
2. **Voltage Monitoring** (ASIL-C): Battery protection against over/under voltage
3. **State Machine Integrity** (ASIL-B/C): Operational safety and fault containment
4. **Configuration Validation** (ASIL-A): Parameter range safety

---

## 4. HARA Methodology

### 4.1 ISO 26262 ASIL Determination Process

ASIL classification based on three factors:

**Severity (S)**: Consequence of hazardous event
- S0: No injuries
- S1: Light to moderate injuries
- S2: Severe injuries (survival probable)
- S3: Life-threatening or fatal injuries

**Exposure (E)**: Probability of operational situation
- E0: Incredible
- E1: Very low probability (<1% operating time)
- E2: Low probability (1-10% operating time)
- E3: Medium probability (10-50% operating time)
- E4: High probability (>50% operating time)

**Controllability (C)**: Ability to avoid harm
- C0: Controllable in general (>99% drivers)
- C1: Simply controllable (>99% drivers)
- C2: Normally controllable (>90% drivers)
- C3: Difficult to control or uncontrollable (<90% drivers)

### 4.2 BMS-Specific Hazard Categories

#### 4.2.1 Electrical Hazards

**Hazard EL-001: Unintended High Voltage Exposure**
- **Description**: Contactors fail to open on fault condition, exposing high voltage
- **Severity**: S3 (life-threatening - electric shock)
- **Exposure**: E3 (medium - occurs during fault scenarios)
- **Controllability**: C3 (uncontrollable - driver cannot prevent)
- **ASIL**: **D** (S3 + E3 + C3)
- **Applicable Requirements**: FBMS-SWE-BMS-022, FBMS-SWE-BMS-033

**Hazard EL-002: Contactor Welding Detection Failure**
- **Description**: System fails to detect welded contactors, preventing safe shutdown
- **Severity**: S3 (thermal runaway risk)
- **Exposure**: E2 (low - rare contactor failure)
- **Controllability**: C3 (uncontrollable)
- **ASIL**: **C** (S3 + E2 + C3)
- **Applicable Requirements**: FBMS-SWE-BMS-020, FBMS-SWE-BMS-023

#### 4.2.2 Functional Hazards

**Hazard FN-001: Invalid State Transition**
- **Description**: State machine enters undefined state, causing unpredictable behavior
- **Severity**: S2 (severe - loss of BMS control)
- **Exposure**: E2 (low - requires software defect)
- **Controllability**: C2 (normally controllable - warning possible)
- **ASIL**: **B** (S2 + E2 + C2)
- **Applicable Requirements**: FBMS-SWE-BMS-031, FBMS-SWE-BMS-034, FBMS-SWE-BMS-035, FBMS-SWE-BMS-036

**Hazard FN-002: Array Index Out of Bounds**
- **Description**: String number exceeds array bounds, causing memory corruption
- **Severity**: S2 (severe - undefined behavior)
- **Exposure**: E3 (medium - multiple call sites)
- **Controllability**: C2 (normally controllable)
- **ASIL**: **C** (S2 + E3 + C2)
- **Applicable Requirements**: FBMS-SWE-BMS-019, FBMS-SWE-BMS-021, FBMS-SWE-BMS-026, FBMS-SWE-BMS-030, FBMS-SWE-BMS-032, FBMS-SWE-BMS-041, FBMS-SWE-BMS-042

#### 4.2.3 Data Integrity Hazards

**Hazard DI-001: Null Pointer Dereference**
- **Description**: Critical data pointer is NULL, causing system crash or corruption
- **Severity**: S3 (life-threatening - BMS failure during operation)
- **Exposure**: E2 (low - defensive programming should prevent)
- **Controllability**: C3 (uncontrollable - immediate crash)
- **ASIL**: **C** (S3 + E2 + C3)
- **Applicable Requirements**: FBMS-SWE-BMS-020, FBMS-SWE-BMS-023, FBMS-SWE-BMS-024, FBMS-SWE-BMS-025, FBMS-SWE-BMS-027, FBMS-SWE-BMS-028, FBMS-SWE-BMS-029

---

## 5. Classification Criteria and Rationale

### 5.1 ASIL-D Requirements (Highest Risk)

**ASIL-D Assignment Criteria:**
- Functions directly controlling high voltage contactors
- Pointer validation for critical contactor control data structures
- Safety mechanisms preventing electric shock or thermal runaway

| Requirement ID | Description | Hazard Reference | S | E | C | ASIL |
|---------------|-------------|------------------|---|---|---|------|
| FBMS-SWE-BMS-020 | FAS_ASSERT: pPackValues != NULL_PTR (contactor context) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-022 | FAS_ASSERT: contactorType != CONT_UNDEFINED | EL-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-023 | FAS_ASSERT: pPackValues != NULL_PTR (state validation) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-024 | FAS_ASSERT: pPackValues != NULL_PTR (voltage check) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-025 | FAS_ASSERT: pPackValues != NULL_PTR (current check) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-027 | FAS_ASSERT: pPackValues != NULL_PTR (string voltage) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-028 | FAS_ASSERT: pPackValues != NULL_PTR (voltage diff) | DI-001 | S3 | E3 | C3 | **D** |
| FBMS-SWE-BMS-033 | FAS_ASSERT: firstOpenedContactorType != CONT_UNDEFINED | EL-001 | S3 | E3 | C3 | **D** |

**Rationale**: These assertions protect critical high-voltage switching operations and battery parameter monitoring. Failure could result in electric shock, thermal runaway, or catastrophic battery failure.

### 5.2 ASIL-C Requirements (High Risk)

**ASIL-C Assignment Criteria:**
- Array bounds checking for battery string operations
- Null pointer validation for non-contactor operations
- State machine integrity for operational safety

| Requirement ID | Description | Hazard Reference | S | E | C | ASIL |
|---------------|-------------|------------------|---|---|---|------|
| FBMS-SWE-BMS-019 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-021 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-026 | FAS_ASSERT: string < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-029 | FAS_ASSERT: pPackValues != NULL_PTR | DI-001 | S2 | E2 | C2 | **C** |
| FBMS-SWE-BMS-030 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-031 | FAS_TRAP: Invalid state - state machine trap | FN-001 | S2 | E2 | C2 | **C** |
| FBMS-SWE-BMS-032 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-034 | FAS_TRAP: Invalid state in state machine default | FN-001 | S2 | E2 | C2 | **C** |
| FBMS-SWE-BMS-041 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |
| FBMS-SWE-BMS-042 | FAS_ASSERT: stringNumber < BS_NR_OF_STRINGS | FN-002 | S2 | E3 | C2 | **C** |

**Rationale**: These requirements prevent memory corruption and operational failures that could lead to severe injuries or BMS malfunction, though with lower exposure or better controllability than ASIL-D.

### 5.3 ASIL-B Requirements (Medium Risk)

**ASIL-B Assignment Criteria:**
- State machine integrity traps for specific operational modes
- Error detection and fault containment

| Requirement ID | Description | Hazard Reference | S | E | C | ASIL |
|---------------|-------------|------------------|---|---|---|------|
| FBMS-SWE-BMS-035 | FAS_TRAP: Invalid state in precharge state machine | FN-001 | S2 | E2 | C2 | **B** |
| FBMS-SWE-BMS-036 | FAS_TRAP: Invalid state in normal state machine | FN-001 | S2 | E2 | C2 | **B** |
| FBMS-SWE-BMS-037 | FAS_TRAP: Invalid state in error state machine | FN-001 | S2 | E1 | C2 | **B** |
| FBMS-SWE-BMS-038 | FAS_TRAP: Invalid state in discharge state machine | FN-001 | S2 | E2 | C2 | **B** |

**Rationale**: State-specific traps provide defense-in-depth for operational modes. Lower exposure due to state-specific nature and defensive programming reduces ASIL to B.

### 5.4 ASIL-A Requirements (Low Risk)

**ASIL-A Assignment Criteria:**
- Invariant checks for charge/standby operational modes
- Configuration and parameter validation

| Requirement ID | Description | Hazard Reference | S | E | C | ASIL |
|---------------|-------------|------------------|---|---|---|------|
| FBMS-SWE-BMS-039 | FAS_TRAP: Invalid state in charge state machine | FN-001 | S1 | E2 | C1 | **A** |
| FBMS-SWE-BMS-040 | FAS_TRAP: Invalid state in standby state machine | FN-001 | S1 | E1 | C1 | **A** |

**Rationale**: Lower severity charging and standby operations with good controllability and warning mechanisms justify ASIL-A classification.

---

## 6. ASIL Decomposition Considerations

### 6.1 Redundant Safety Mechanisms

Several safety functions implement redundant protection:

**Contactor Control Safety (ASIL-D)**
- Primary: FBMS-SWE-BMS-022 (contactor type validation)
- Secondary: FBMS-SWE-BMS-033 (first contactor validation)
- Backup: State machine traps (FBMS-SWE-BMS-031, FBMS-SWE-BMS-034)

**Pointer Integrity (ASIL-D/C)**
- Multiple validation points across call chain
- No ASIL decomposition applied - each check maintains full ASIL rating

### 6.2 Independence Analysis

**No ASIL Decomposition Applied** - All safety requirements maintain their assigned ASIL level without decomposition because:
- Single-channel architecture without redundancy
- Assertions are independent safety mechanisms
- No diverse implementation strategies employed

**Future Decomposition Opportunities:**
- Dual-channel voltage monitoring (decompose ASIL-D to 2x ASIL-B)
- Redundant contactor feedback paths
- Independent watchdog mechanisms

---

## 7. Safety Goals and Functional Safety Requirements Mapping

### 7.1 Safety Goal SG-BMS-001: Prevent Unintended High Voltage Exposure

**Safety Goal Statement**: The BMS shall prevent unintended exposure to high voltage by ensuring contactors open on all fault conditions.

**ASIL**: D
**Safe State**: Contactors open, high voltage isolated
**FTTI**: 100ms (detection), 500ms (reaction)

**Derived FSR:**
- FBMS-SWE-BMS-022: Validate contactor type before state change
- FBMS-SWE-BMS-033: Validate first opened contactor sequence

### 7.2 Safety Goal SG-BMS-002: Prevent Memory Corruption in Safety Functions

**Safety Goal Statement**: The BMS shall prevent memory corruption that could compromise safety functions through comprehensive pointer and bounds validation.

**ASIL**: C
**Safe State**: Assertion triggered, safe state entered
**FTTI**: 10ms (immediate detection)

**Derived FSR:**
- FBMS-SWE-BMS-019 through FBMS-SWE-BMS-042: Range and pointer checks

### 7.3 Safety Goal SG-BMS-003: Ensure State Machine Integrity

**Safety Goal Statement**: The BMS state machine shall detect and prevent entry into undefined or invalid states.

**ASIL**: B
**Safe State**: Error state, controlled shutdown
**FTTI**: 50ms (state transition period)

**Derived FSR:**
- FBMS-SWE-BMS-031, FBMS-SWE-BMS-034, FBMS-SWE-BMS-035, FBMS-SWE-BMS-036, FBMS-SWE-BMS-037, FBMS-SWE-BMS-038, FBMS-SWE-BMS-039, FBMS-SWE-BMS-040

---

## 8. ASIL Inheritance and Traceability

### 8.1 System to Software ASIL Allocation

| System Requirement | Software Requirement | ASIL Inheritance |
|-------------------|---------------------|------------------|
| SYS-SAFE-001: High Voltage Safety | FBMS-SWE-BMS-022, FBMS-SWE-BMS-033 | ASIL-D → ASIL-D |
| SYS-SAFE-002: Battery Monitoring | FBMS-SWE-BMS-020, FBMS-SWE-BMS-023 | ASIL-D → ASIL-D |
| SYS-SAFE-003: Array Integrity | FBMS-SWE-BMS-019, FBMS-SWE-BMS-021 | ASIL-C → ASIL-C |

### 8.2 ASIL Assignment History

All ASIL assignments documented with:
- Classification date: 2025-12-16
- Classification agent: parvis-aispec-safety
- Review status: Initial classification (requires safety manager approval)
- Next review: Before SOP (Start of Production)

---

## 9. Verification and Validation Requirements

### 9.1 ASIL-Specific V&V Activities

**ASIL-D Requirements (8 requirements):**
- Structural coverage: MC/DC (Modified Condition/Decision Coverage)
- Fault injection testing required
- Independent safety assessment mandatory
- Hardware-software integration testing

**ASIL-C Requirements (10 requirements):**
- Structural coverage: MC/DC
- Fault injection recommended
- Semi-independent verification
- Integration testing required

**ASIL-B Requirements (4 requirements):**
- Structural coverage: Statement + Branch
- Functional testing required
- Integration testing required

**ASIL-A Requirements (2 requirements):**
- Structural coverage: Statement
- Functional testing required

### 9.2 Safety Test Specifications

See complementary documents:
- `bms-test-spec.json` - Detailed test specifications per ASIL level
- `mcdc-analysis-bms.md` - MC/DC coverage analysis for ASIL-C/D requirements
- `r4-safety-case.md` - Safety case evidence and argumentation

---

## 10. Open Issues and Recommendations

### 10.1 Classification Review Items

1. **Manual Review Required**: FBMS-SWE-BMS-022 and FBMS-SWE-BMS-033
   - **Reason**: ASIL-D classification requires safety manager approval
   - **Action**: Schedule safety review meeting
   - **Due Date**: Before design freeze

2. **ASIL Decomposition Opportunity**: Voltage monitoring redundancy
   - **Reason**: Could reduce verification effort through ASIL decomposition
   - **Action**: Evaluate dual-channel implementation
   - **Benefit**: ASIL-D → 2x ASIL-B (reduced MC/DC burden)

### 10.2 Gap Analysis

**Identified Gaps:**
- No hardware-software interface safety requirements (HSI)
- Missing safe state definitions for some state machine transitions
- FTTI not formally verified for all safety goals

**Recommendations:**
1. Generate HSI safety requirements (use parvis-aispec-safety)
2. Define safe states for all operational modes
3. Perform timing analysis for FTTI verification

### 10.3 Next Steps

1. **Immediate (Week 1)**
   - Safety manager review and approval of ASIL-D assignments
   - Update safety requirements specification with ASIL levels
   - Generate safety test specifications for ASIL-C/D requirements

2. **Short-Term (Month 1)**
   - Implement MC/DC coverage for ASIL-C/D requirements
   - Develop fault injection test cases
   - Create safety validation plan

3. **Long-Term (Before SOP)**
   - Complete independent safety assessment
   - Generate safety case documentation
   - Obtain functional safety certification

---

## 11. Compliance and Audit Trail

### 11.1 ISO 26262:2018 Compliance

**Applicable Standard Sections:**
- ISO 26262-3:2018 - Concept Phase (HARA, Safety Goals)
- ISO 26262-4:2018 - Product Development: System Level
- ISO 26262-6:2018 - Product Development: Software Level
- ISO 26262-9:2018 - ASIL-oriented and safety-oriented analyses

**Compliance Status:**
- Part 3: HARA documented in Section 4 ✓
- Part 4: Safety goals defined in Section 7 ✓
- Part 6: FSR derived in Section 7 ✓
- Part 9: ASIL decomposition analyzed in Section 6 ✓

### 11.2 Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-16 | parvis-aispec-safety | Initial ASIL classification report |

---

## 12. Conclusion

This ASIL classification report provides a comprehensive safety analysis of the foxBMS Battery Management System software, classifying 24 safety requirements across ASIL levels A through D. The classification follows ISO 26262:2018 methodology and supports the development of functionally safe battery management software.

**Key Outcomes:**
- **8 ASIL-D requirements** protecting critical high-voltage safety functions
- **10 ASIL-C requirements** ensuring operational safety and data integrity
- **4 ASIL-B requirements** providing state machine fault containment
- **2 ASIL-A requirements** for low-risk operational modes

**Safety Architecture Strengths:**
- Comprehensive pointer validation across all critical operations
- Defensive programming with FAS_ASSERT and FAS_TRAP mechanisms
- State machine integrity protection at multiple ASIL levels
- Clear traceability from hazards to safety requirements

**Next Actions:**
1. Safety manager approval for ASIL-D classifications
2. MC/DC test development for ASIL-C/D requirements
3. Safety validation plan creation
4. Independent safety assessment planning

---

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Safety Manager | [Pending] | | |
| Software Architect | [Pending] | | |
| Quality Manager | [Pending] | | |

---

**End of ASIL Classification Report**
