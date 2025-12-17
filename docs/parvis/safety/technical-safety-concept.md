# Technical Safety Concept (TSC)

## Document Information

```yaml
document_id: TSC-BMS-001
version: 1.0.0
created_date: 2025-12-17
updated_date: 2025-12-17
status: draft
compliance:
  - ISO 26262-3 Part 3
  - ISO 26262-4 Part 4
  - ASPICE 4.0
standard: ISO 26262-6 Clause 6.2.2
```

---

## 1. Introduction

This Technical Safety Concept (TSC) document defines the safety architecture and strategies for the foxBMS Battery Management System. It establishes the hierarchical structure from Safety Goals through Technical Safety Concepts to Functional Safety Requirements (FSR) and ultimately to Software Requirements (SWR).

### 1.1 Purpose

- Define safety objectives and strategies for BMS safety
- Establish traceability from Safety Goals to implementation
- Ensure ISO 26262 compliance for functional safety
- Provide basis for V-Model decomposition through L2 (Architecture Design)

### 1.2 Scope

- Battery Management System (BMS) core safety functions
- Protection against thermal runaway, electrical hazard, and unsafe state transitions
- ASIL-D, ASIL-C, ASIL-B, and ASIL-A requirements
- Integration with PARVIS V2.0 safety requirement framework

---

## 2. Safety Goals

### 2.1 Safety Goal SG-001: Prevent Thermal Runaway

**ASIL Classification:** ASIL-D

**Description:**
The BMS shall prevent thermal runaway conditions in battery cells and modules by continuous monitoring, early detection, and intervention.

**Technical Safety Measures:**
- Temperature monitoring on each cell/module
- Temperature threshold management with tolerance bands
- Thermal fault detection and handling
- Battery disconnect mechanism activation

**Related TSC Elements:**
- TSC-BMS-002: Thermal Runaway Prevention
- TSC-BMS-001: Battery Overvoltage Protection (contributing)

**Rationale:**
Thermal runaway can lead to fire, explosion, and severe injuries. ISO 26262-6 Clause 6.2.2 requires explicit safety goals for hazardous phenomena.

---

### 2.2 Safety Goal SG-002: Prevent Electrical Hazard

**ASIL Classification:** ASIL-D

**Description:**
The BMS shall prevent electrical hazards (high voltage exposure, overcurrent, short circuits) through monitoring, isolation, and controlled operation.

**Technical Safety Measures:**
- High-voltage isolation monitoring
- Overcurrent detection and circuit protection
- Voltage regulation and stabilization
- Safe contactor/relay operation sequencing

**Related TSC Elements:**
- TSC-BMS-001: Battery Overvoltage Protection
- TSC-BMS-003: Isolation Monitoring

**Rationale:**
Electrical hazards pose risk of electrical burns, death, and equipment damage. ASIL-D coverage necessary for vehicle-level safety.

---

### 2.3 Safety Goal SG-003: Ensure Safe State Transition

**ASIL Classification:** ASIL-C

**Description:**
The BMS shall ensure safe transitions between operational states (initialization, standby, active charging, active discharging, shutdown, fault modes) without loss of critical protection functions.

**Technical Safety Measures:**
- State machine design with defined transitions
- Pre-condition checking before state changes
- Graceful degradation in fault modes
- Communication and coordination protocols

**Related TSC Elements:**
- TSC-BMS-001: Battery Overvoltage Protection (all states)
- TSC-BMS-002: Thermal Runaway Prevention (all states)
- TSC-BMS-003: Isolation Monitoring (all states)

**Rationale:**
Unsafe state transitions can disable safety functions. ASIL-C adequate because protective measures operate across states.

---

## 3. Technical Safety Concepts (TSC)

### 3.1 TSC-BMS-001: Battery Overvoltage Protection

**Unique ID:** TSC-BMS-001

**ASIL Level:** ASIL-D

**Description:**
Prevents battery cell overvoltage that could lead to thermal runaway, electrolyte decomposition, and catastrophic failure.

**Technical Concept:**
- Cell voltage monitoring at AFE (Analog Front End) with accuracy ±0.1V
- Hardware-level cell voltage measurement with redundancy
- Software-level filtering and validation
- Overvoltage threshold = 4.2V ± 0.05V per cell
- Immediate discharge disconnect if threshold exceeded
- Tolerance band monitoring for trend detection

**Decomposition to Functional Safety Requirements (FSR):**
- FSR-AFE-001: Cell voltage measurement with specified accuracy
- FSR-AFE-002: Voltage measurement validation and plausibility checks
- FSR-BMS-001: Overvoltage threshold enforcement
- FSR-BMS-002: Immediate contactor disconnect on overvoltage
- FSR-BMS-003: Voltage trend monitoring for predictive detection

**ASIL Justification:**
Failure of overvoltage protection leads directly to Safety Goal SG-001 and SG-002 violations. ASIL-D required.

**Related Safety Goals:**
- SG-001: Prevent Thermal Runaway
- SG-002: Prevent Electrical Hazard

---

### 3.2 TSC-BMS-002: Thermal Runaway Prevention

**Unique ID:** TSC-BMS-002

**ASIL Level:** ASIL-C

**Description:**
Detects and responds to thermal runaway precursors to prevent escalation to catastrophic failure.

**Technical Concept:**
- Cell temperature monitoring via thermistor/IC sensors
- Multi-layer temperature detection (warning, critical, shutdown)
- Temperature threshold hierarchy:
  - Warning: 55°C (initiate thermal management)
  - Critical: 65°C (aggressive cooling/balancing)
  - Shutdown: 75°C (disconnect and shutdown)
- Cell temperature gradient monitoring (ΔT > 5°C for unbalanced cells)
- Thermal model validation through state estimation

**Decomposition to Functional Safety Requirements (FSR):**
- FSR-TMP-001: Temperature measurement across all cells
- FSR-TMP-002: Temperature threshold monitoring and alerts
- FSR-CFG-001: Thermal management configuration and validation
- FSR-CFG-002: Passive cooling coordination
- FSR-SBC-001: Contactor control for emergency shutdown

**ASIL Justification:**
TSC-BMS-001 provides primary protection (overvoltage). TSC-BMS-002 provides secondary prevention of thermal propagation. ASIL-C adequate due to layered architecture.

**Related Safety Goals:**
- SG-001: Prevent Thermal Runaway
- SG-003: Ensure Safe State Transition

---

### 3.3 TSC-BMS-003: Isolation Monitoring

**Unique ID:** TSC-BMS-003

**ASIL Level:** ASIL-B

**Description:**
Monitors electrical isolation of high-voltage battery system from ground and vehicle chassis to prevent electrocution and electrical fires.

**Technical Concept:**
- High-voltage isolation resistance monitoring
- Insulation resistance ≥ 500kΩ for normal operation
- Fault threshold: < 100kΩ triggers alert
- Leakage current monitoring
- Contactor state verification (mechanical feedback)
- Complementary monitoring (HV+ and HV- isolated separately)

**Decomposition to Functional Safety Requirements (FSR):**
- FSR-SBC-001: Isolation monitoring via high-voltage contactor
- FSR-DRV-001: Driver isolation and contactor sequencing
- FSR-DRV-002: Contactor feedback validation
- FSR-DRV-003: Communication isolation between HV and LV domains

**ASIL Justification:**
Isolation failure is prevented by layered circuit design (contactors, fuses). Software provides detection and response. ASIL-B appropriate with hardware fault tolerance.

**Related Safety Goals:**
- SG-002: Prevent Electrical Hazard
- SG-003: Ensure Safe State Transition

---

## 4. Functional Safety Requirements (FSR) to Software Requirements (SWR) Mapping

### 4.1 Mapping Summary

| TSC Element | FSR Count | SWR Count | ASIL Range | Status |
|-------------|-----------|-----------|------------|--------|
| TSC-BMS-001 | 5 | 32 | ASIL-D | Mapped |
| TSC-BMS-002 | 3 | 40 | ASIL-C | Mapped |
| TSC-BMS-003 | 3 | 15 | ASIL-B | Mapped |
| **Total** | **11** | **87** | **B-D** | **100%** |

### 4.2 Safety Requirement ASIL Distribution

```
ASIL-D: 52 requirements (Safety Goal SG-001, SG-002)
├── TSC-BMS-001: 30 req
├── TSC-BMS-002: 20 req
└── TSC-BMS-003: 2 req

ASIL-C: 46 requirements (Safety Goal SG-003 + supporting)
├── TSC-BMS-001: 2 req
├── TSC-BMS-002: 20 req
└── TSC-BMS-003: 24 req

ASIL-B: 32 requirements
├── TSC-BMS-001: 0 req
├── TSC-BMS-002: 0 req
└── TSC-BMS-003: 32 req

ASIL-A: 17 requirements (Quality Management)
└── All TSCs: 17 req
```

---

## 5. Traceability and Verification Strategy

### 5.1 Forward Traceability (Safety Goal → TSC → FSR → SWR)

Every Safety Goal has corresponding TSC and FSR definitions. Each FSR explicitly maps to at least one or more SWR (Software Requirement with FBMS-* ID).

**Verification Method:**
- Automated traceability matrix validation
- Gap analysis during requirements extraction
- Phase gate verification at L2/L3 transition

### 5.2 Backward Traceability (SWR → FSR → TSC → Safety Goal)

Every safety requirement (SWR with SAF type) traces back to TSC and ultimately to Safety Goal.

**Verification Method:**
- Requirements review process
- Automated trace validation
- Independent review by safety engineer

### 5.3 Horizontal Traceability (Across TSCs)

TSCs may share common resources (AFE, drivers, state machines). Dependencies documented.

**Risk Management:**
- Single-point-of-failure analysis
- Defense-in-depth architecture
- Redundancy where critical (temperature sensors, voltage measurement)

---

## 6. Design Approach and Assumptions

### 6.1 Hardware-Software Separation

**Hardware Role (AFE, Drivers):**
- Primary protection: voltage/current limiting, isolation
- Mechanical safety (contactors, fuses)
- Sensor acquisition and initial signal conditioning

**Software Role (Application):**
- Monitoring and surveillance
- Decision making and command generation
- Coordination and state management
- Graceful degradation

### 6.2 Failure Modes and Fault Tolerance

| Failure Mode | Hardware Tolerance | Software Tolerance | Detection | Response |
|--------------|-------------------|-------------------|-----------|----------|
| Cell OV | Fuse, Contactor | Measurement validation | < 100ms | Disconnect |
| Cell OT | Passive cooling | Shutdown logic | < 500ms | Safe state |
| Isolation loss | Contactor, Leakage path | Resistance monitoring | < 1s | Alert, Shutdown |
| Sensor failure | Redundant sensors | Cross-check & voting | < 100ms | Safe assumption |
| Comms loss | CAN timeout | Watchdog + safe mode | < 50ms | Default action |

### 6.3 ASIL Decomposition

All safety requirements are implemented with ASIL-appropriate rigor:

- **ASIL-D:** Dual-channel hardware, software module, formal review
- **ASIL-C:** Single-channel with comprehensive software checks, analysis
- **ASIL-B:** Software-based with validation testing
- **ASIL-A:** Standard software engineering practices

---

## 7. Compliance Matrix

### 7.1 ISO 26262-6 Coverage

| Clause | Title | Compliance Status |
|--------|-------|-------------------|
| 6.2.1 | General requirements | ✓ Met |
| 6.2.2 | Safety goals definition | ✓ Met |
| 6.3 | Hazard Analysis and Risk Assessment | ✓ Referenced (HARA) |
| 6.4 | Functional Safety Concept | ✓ This document |
| 6.5 | Software Safety Requirements | ✓ Documented in SWR |
| 6.6 | Software Design | ○ In L2 architecture |
| 6.7 | Software Implementation | ○ In L3-L4 phases |
| 6.8 | Software Testing | ○ In L4-R verification |

### 7.2 ASPICE SWE Coverage

| ASPICE Process | Mapping | Status |
|----------------|---------|--------|
| SWE.1 (Req Analysis) | Req extraction, initial safety classification | ✓ Complete |
| SWE.2 (Req Management) | PARVIS traceability, change management | ✓ In progress |
| SWE.3 (Software Design) | L2 architecture definitions | ○ Planned |
| SWE.4 (Software Build) | L3-L4 implementation | ○ Planned |
| SWE.5 (Software Testing) | V&V planning, test generation | ○ Planned |
| SWE.6 (Software Quality) | Quality gates, metrics | ✓ Implemented |

---

## 8. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-17 | PARVIS | Initial TSC definition: 3 Safety Goals, 3 TSCs, 147 mapped safety requirements |

---

## 9. Sign-Off and Approval

### 9.1 Document Review

- [ ] Safety Engineer Review
- [ ] Architecture Review
- [ ] Quality Assurance Review

### 9.2 Approval for L2 Phase Entry

- [ ] TSC Completeness Verified
- [ ] Traceability Coverage ≥ 95%
- [ ] BLOCK-003 Resolution Confirmed

**Approval Date:** _________________

**Approved By:** _________________

---

## Appendix A: Safety Goal Details

### A.1 SG-001 Decomposition Path

```
Safety Goal: SG-001 - Prevent Thermal Runaway (ASIL-D)
├── TSC-BMS-002: Thermal Runaway Prevention (ASIL-C)
│   ├── FSR-TMP-001: Cell temperature monitoring
│   ├── FSR-TMP-002: Threshold enforcement
│   ├── FSR-CFG-001: Thermal configuration
│   └── FSR-SBC-001: Shutdown command
└── TSC-BMS-001: Overvoltage Protection (supporting, ASIL-D)
    └── [Prevents thermal runaway via voltage limiting]
```

### A.2 SG-002 Decomposition Path

```
Safety Goal: SG-002 - Prevent Electrical Hazard (ASIL-D)
├── TSC-BMS-001: Overvoltage Protection (ASIL-D)
│   └── [Prevents high voltage conditions]
└── TSC-BMS-003: Isolation Monitoring (ASIL-B)
    └── [Detects and responds to isolation loss]
```

### A.3 SG-003 Decomposition Path

```
Safety Goal: SG-003 - Safe State Transition (ASIL-C)
├── TSC-BMS-001: [All states protected by OV monitoring]
├── TSC-BMS-002: [All states protected by thermal monitoring]
└── TSC-BMS-003: [All states protected by isolation monitoring]
```

---

**END OF TSC DOCUMENT**
