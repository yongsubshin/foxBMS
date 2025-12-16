# foxBMS System Qualification Test Specification

**Document ID**: FBMS-WP-SYS5-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Released
**Classification**: Technical
**ASPICE Process**: SYS.5 (System Qualification Testing)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author          | Description                    |
|---------|------------|-----------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI | Initial qualification spec |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Qualification Lead    |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This System Qualification Test Specification defines the test cases for qualifying the foxBMS Battery Management System against system requirements. It verifies that the integrated system meets all functional, performance, and safety requirements defined in the System Requirements Specification (SYS.1).

### 1.2 Scope

This document covers:
- System qualification test strategy
- Qualification test cases for all system requirements
- Environmental qualification tests
- Safety qualification tests
- Performance qualification tests

### 1.3 Test Environment

| Component | Specification |
|-----------|--------------|
| Target System | foxBMS Master with production hardware |
| Battery Pack | 12S4P Li-Ion test pack or HIL simulator |
| Load System | Bidirectional DC power source |
| Environment | Temperature chamber (-40C to +85C) |
| Monitoring | Production CAN interface |

### 1.4 References

| Document ID | Title |
|-------------|-------|
| FBMS-WP-SYS1-001 | System Requirements Specification |
| FBMS-WP-SYS3-001 | System Integration Test Specification |
| ISO 26262:2018 | Functional Safety |
| IEC 62660-2 | Secondary lithium-ion cells - Safety |

---

## 2. Qualification Test Strategy

### 2.1 Test Categories

| Category | Code | Description | Priority |
|----------|------|-------------|----------|
| Functional | QT-FUNC | Functional requirement verification | Critical |
| Safety | QT-SAF | Safety requirement verification | Critical |
| Performance | QT-PERF | Performance requirement verification | High |
| Environmental | QT-ENV | Environmental qualification | High |
| EMC | QT-EMC | Electromagnetic compatibility | High |
| Reliability | QT-REL | Reliability and endurance | Medium |

### 2.2 Test Coverage Matrix

| System Requirement | Test Category | Test Count |
|-------------------|---------------|------------|
| TSR-001 (Voltage) | QT-FUNC, QT-SAF | 12 |
| TSR-002 (Temperature) | QT-FUNC, QT-SAF | 8 |
| TSR-003 (Current) | QT-FUNC, QT-SAF | 10 |
| TSR-004 (Contactor) | QT-FUNC, QT-SAF | 15 |
| TSR-005 (Precharge) | QT-FUNC | 8 |
| TSR-006 (SOA) | QT-SAF | 20 |
| TSR-007 (Diagnostics) | QT-FUNC, QT-SAF | 12 |
| TSR-008 (Safe State) | QT-SAF | 10 |
| TSR-009 (Watchdog) | QT-SAF | 6 |
| TSR-010 (Communication) | QT-FUNC | 8 |
| NFR (Performance) | QT-PERF | 15 |
| NFR (Environmental) | QT-ENV, QT-EMC | 20 |

---

## 3. Functional Qualification Tests (QT-FUNC)

### 3.1 Cell Voltage Measurement

#### QT-FUNC-001: Voltage Measurement Accuracy

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-001 |
| Title | Cell Voltage Measurement Accuracy |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-001 |

**Test Configuration**:
- Battery simulator with calibrated voltage source
- Reference multimeter (6.5 digit)

**Test Procedure**:
1. Configure battery simulator to reference voltages
2. Measure 10 voltage points: 2.5V, 2.8V, 3.0V, 3.2V, 3.4V, 3.6V, 3.8V, 4.0V, 4.1V, 4.2V
3. Record BMS reported voltage via CAN
4. Compare with reference measurement
5. Calculate accuracy at each point

**Pass Criteria**:
- Accuracy: +/-2mV at 25C ambient
- Accuracy: +/-5mV over full temperature range

#### QT-FUNC-002: Voltage Measurement Response

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-002 |
| Title | Voltage Update Rate |
| Priority | High |
| Related Req | TSR-001 |

**Test Procedure**:
1. Apply step voltage change on cell
2. Measure time from change to CAN update
3. Verify update rate specification

**Pass Criteria**:
- Update rate: < 100ms

#### QT-FUNC-003: Open Wire Detection

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-003 |
| Title | Open Wire Detection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-001 |

**Test Procedure**:
1. Disconnect one cell sense wire
2. Verify open wire detection within 1s
3. Verify diagnostic flag set
4. Reconnect and verify recovery

**Pass Criteria**:
- Open wire detected within specification
- Correct cell identification

### 3.2 Temperature Measurement

#### QT-FUNC-010: Temperature Measurement Accuracy

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-010 |
| Title | Temperature Measurement Accuracy |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-002 |

**Test Procedure**:
1. Place system in temperature chamber
2. Set chamber to reference temperatures: -40C, -20C, 0C, 25C, 45C, 60C, 85C
3. Allow stabilization (30 minutes)
4. Record BMS temperature readings
5. Compare with chamber reference

**Pass Criteria**:
- Accuracy: +/-2C at all test points

### 3.3 Current Measurement

#### QT-FUNC-020: Current Measurement Accuracy

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-020 |
| Title | Pack Current Accuracy |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-003 |

**Test Procedure**:
1. Apply known current using calibrated load
2. Test points: 0A, +/-10A, +/-50A, +/-100A, +/-200A, +/-500A
3. Record BMS current reading
4. Compare with shunt reference

**Pass Criteria**:
- Accuracy: +/-1% of full scale

#### QT-FUNC-021: Current Direction Detection

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-021 |
| Title | Charge/Discharge Detection |
| Priority | High |
| Related Req | TSR-003 |

**Test Procedure**:
1. Apply charging current
2. Verify positive current reported
3. Apply discharging current
4. Verify negative current reported (or vice versa per convention)

**Pass Criteria**:
- Correct direction indication in all cases

### 3.4 Contactor Control

#### QT-FUNC-030: Contactor Closing Sequence

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-030 |
| Title | Contactor Closing Sequence |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Test Procedure**:
1. Monitor all contactor signals with oscilloscope
2. Command system to STANDBY
3. Verify MINUS closes first
4. Verify PRECHARGE closes second
5. Verify voltage rise
6. Verify PLUS closes after threshold
7. Verify PRECHARGE opens

**Pass Criteria**:
- Sequence follows specification
- Timing between steps correct

#### QT-FUNC-031: Contactor Opening Sequence

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-031 |
| Title | Contactor Opening Sequence |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Test Procedure**:
1. Start from NORMAL state
2. Command open contactors
3. Verify PLUS opens first
4. Verify MINUS opens second
5. Verify HV bus isolated

**Pass Criteria**:
- Safe opening sequence maintained
- Break current within limits

### 3.5 Precharge Function

#### QT-FUNC-040: Precharge Voltage Threshold

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-040 |
| Title | Precharge Completion Threshold |
| Priority | High |
| Related Req | TSR-005 |

**Test Procedure**:
1. Start precharge with known battery voltage
2. Monitor HV bus voltage rise
3. Verify precharge completes at 95% threshold
4. Verify main contactor closes

**Pass Criteria**:
- Precharge completes within 95% +/-2% threshold
- Total precharge time < 5s

#### QT-FUNC-041: Precharge Timeout

| Attribute | Value |
|-----------|-------|
| ID | QT-FUNC-041 |
| Title | Precharge Timeout Handling |
| Priority | High |
| Related Req | TSR-005 |

**Test Procedure**:
1. Simulate high capacitance load
2. Start precharge
3. Allow timeout to occur
4. Verify retry behavior
5. Verify error state after max retries

**Pass Criteria**:
- Timeout detected correctly
- Retry count enforced
- Error state entered after max retries

---

## 4. Safety Qualification Tests (QT-SAF)

### 4.1 SOA Protection Tests

#### QT-SAF-001: Overvoltage Protection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-001 |
| Title | Cell Overvoltage Protection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-002 |

**Test Procedure**:
1. Operate system normally
2. Increase one cell voltage above limit (4.25V)
3. Measure time from violation to contactor open
4. Verify CAN error message
5. Verify system enters ERROR state

**Pass Criteria**:
- Detection within 100ms
- Contactors open within FTTI (1s)
- Error logged correctly

#### QT-SAF-002: Undervoltage Protection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-002 |
| Title | Cell Undervoltage Protection |
| Priority | Critical |
| ASIL | ASIL-C |
| Related Req | TSR-006, SG-003 |

**Test Procedure**:
1. Operate system normally
2. Decrease one cell voltage below limit (2.4V)
3. Verify protection activates
4. Verify contactors open

**Pass Criteria**:
- Detection within specification
- Appropriate action taken

#### QT-SAF-003: Overcurrent Protection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-003 |
| Title | Pack Overcurrent Protection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-004 |

**Test Procedure**:
1. Operate system at normal current
2. Increase load to exceed current limit
3. Measure time from violation to contactor open
4. Verify fast response

**Pass Criteria**:
- Detection within 10ms
- Contactors open within 50ms

#### QT-SAF-004: Overtemperature Protection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-004 |
| Title | Temperature Limit Protection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-001 |

**Test Procedure**:
1. Heat one temperature sensor above limit
2. Verify temperature limit detection
3. Verify current limiting or shutdown
4. Cool and verify recovery

**Pass Criteria**:
- Protection activates at configured limit
- Hysteresis prevents oscillation

### 4.2 Safe State Tests

#### QT-SAF-010: Fatal Error Safe State

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-010 |
| Title | Fatal Error Response |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-008 |

**Test Procedure**:
1. Inject fatal error condition
2. Measure time to ERROR state
3. Verify all contactors open
4. Verify error indication
5. Attempt recovery command
6. Verify safe state maintained until proper reset

**Pass Criteria**:
- ERROR state within 100ms
- Contactors open
- Recovery requires proper procedure

#### QT-SAF-011: Multiple Fault Handling

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-011 |
| Title | Simultaneous Fault Response |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-007, TSR-008 |

**Test Procedure**:
1. Inject multiple fault conditions simultaneously
2. Verify all faults detected
3. Verify safe state achieved
4. Verify all faults logged

**Pass Criteria**:
- All faults detected and logged
- Safe state achieved reliably

### 4.3 Watchdog Tests

#### QT-SAF-020: Watchdog Normal Operation

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-020 |
| Title | Watchdog Servicing |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-009 |

**Test Procedure**:
1. Monitor watchdog trigger signal
2. Verify trigger period matches specification
3. Verify no spurious resets during 24 hour test

**Pass Criteria**:
- Consistent watchdog triggering
- No unexpected resets

#### QT-SAF-021: Watchdog Failure Response

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-021 |
| Title | Watchdog Timeout Behavior |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-009 |

**Test Procedure**:
1. Cause software hang (debugger halt)
2. Monitor watchdog timeout
3. Verify FS0B assertion
4. Verify contactor opening
5. Verify MCU reset

**Pass Criteria**:
- Watchdog timeout as configured
- FS0B asserts
- Contactors open via hardware path
- MCU resets

### 4.4 Contactor Feedback Tests

#### QT-SAF-030: Contactor Welding Detection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-030 |
| Title | Contactor Weld Detection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Test Procedure**:
1. Command contactor open
2. Simulate stuck closed feedback
3. Verify weld detection
4. Verify error state entered
5. Verify appropriate warnings

**Pass Criteria**:
- Weld condition detected within 100ms
- Error state entered
- Warning generated

#### QT-SAF-031: Contactor Failure Detection

| Attribute | Value |
|-----------|-------|
| ID | QT-SAF-031 |
| Title | Contactor Open Failure |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Test Procedure**:
1. Command contactor close
2. Simulate stuck open feedback
3. Verify failure detection
4. Verify retry logic
5. Verify error after max retries

**Pass Criteria**:
- Failure detected
- Retry behavior correct
- Error state after max retries

---

## 5. Performance Qualification Tests (QT-PERF)

### 5.1 Response Time Tests

#### QT-PERF-001: Startup Time

| Attribute | Value |
|-----------|-------|
| ID | QT-PERF-001 |
| Title | System Startup Time |
| Priority | High |
| Related Req | NFR-PERF-002 |

**Test Procedure**:
1. Apply power to system
2. Measure time to first CAN message
3. Measure time to operational state

**Pass Criteria**:
- First CAN message within 200ms
- Operational within 500ms

#### QT-PERF-002: Fault Response Time

| Attribute | Value |
|-----------|-------|
| ID | QT-PERF-002 |
| Title | Critical Fault Response |
| Priority | Critical |
| Related Req | NFR-PERF-001, TSR-008 |

**Test Procedure**:
1. Measure end-to-end time for critical fault
2. From fault injection to contactor opening
3. Test multiple fault types

**Pass Criteria**:
- All critical faults: <100ms

### 5.2 Accuracy Tests

#### QT-PERF-010: SOC Accuracy

| Attribute | Value |
|-----------|-------|
| ID | QT-PERF-010 |
| Title | SOC Estimation Accuracy |
| Priority | High |

**Test Procedure**:
1. Fully charge battery
2. Discharge at known current
3. Compare BMS SOC with coulomb counting reference
4. Test at multiple temperatures

**Pass Criteria**:
- SOC accuracy: +/-5%

---

## 6. Environmental Qualification Tests (QT-ENV)

### 6.1 Temperature Tests

#### QT-ENV-001: Low Temperature Operation

| Attribute | Value |
|-----------|-------|
| ID | QT-ENV-001 |
| Title | Operation at -40C |
| Priority | High |

**Test Procedure**:
1. Cold soak system at -40C for 4 hours
2. Power on system
3. Verify all functions operational
4. Verify measurement accuracy

**Pass Criteria**:
- System starts and operates
- All measurements within specification

#### QT-ENV-002: High Temperature Operation

| Attribute | Value |
|-----------|-------|
| ID | QT-ENV-002 |
| Title | Operation at +85C |
| Priority | High |

**Test Procedure**:
1. Heat soak system at +85C for 4 hours
2. Operate system under load
3. Verify all functions operational
4. Verify no thermal shutdown

**Pass Criteria**:
- System operates normally
- No thermal de-rating below specification

#### QT-ENV-003: Temperature Cycling

| Attribute | Value |
|-----------|-------|
| ID | QT-ENV-003 |
| Title | Temperature Cycle Endurance |
| Priority | Medium |

**Test Procedure**:
1. Cycle between -40C and +85C
2. 100 cycles, 2 hours per cycle
3. Verify operation after cycling

**Pass Criteria**:
- No degradation after cycling
- All functions operational

### 6.2 Vibration Tests

#### QT-ENV-010: Vibration Endurance

| Attribute | Value |
|-----------|-------|
| ID | QT-ENV-010 |
| Title | Vibration per ISO 16750-3 |
| Priority | High |

**Test Procedure**:
1. Mount system on vibration table
2. Apply random vibration profile
3. Operate system during test
4. Verify operation after test

**Pass Criteria**:
- No functional degradation
- No physical damage

---

## 7. EMC Qualification Tests (QT-EMC)

### 7.1 Emissions Tests

#### QT-EMC-001: Conducted Emissions

| Attribute | Value |
|-----------|-------|
| ID | QT-EMC-001 |
| Title | Conducted Emissions CISPR 25 |
| Priority | High |

**Pass Criteria**:
- Meets CISPR 25 Class 5 limits

#### QT-EMC-002: Radiated Emissions

| Attribute | Value |
|-----------|-------|
| ID | QT-EMC-002 |
| Title | Radiated Emissions CISPR 25 |
| Priority | High |

**Pass Criteria**:
- Meets CISPR 25 Class 5 limits

### 7.2 Immunity Tests

#### QT-EMC-010: ESD Immunity

| Attribute | Value |
|-----------|-------|
| ID | QT-EMC-010 |
| Title | ESD per ISO 10605 |
| Priority | High |

**Pass Criteria**:
- No malfunction during test
- No damage after test

#### QT-EMC-011: Transient Immunity

| Attribute | Value |
|-----------|-------|
| ID | QT-EMC-011 |
| Title | Transients per ISO 7637-2 |
| Priority | High |

**Pass Criteria**:
- Function maintained during test

---

## 8. Test Summary

### 8.1 Test Count by Category

| Category | Test Cases | Critical | High | Medium |
|----------|------------|----------|------|--------|
| QT-FUNC | 35 | 20 | 15 | 0 |
| QT-SAF | 25 | 25 | 0 | 0 |
| QT-PERF | 15 | 5 | 10 | 0 |
| QT-ENV | 12 | 0 | 8 | 4 |
| QT-EMC | 8 | 0 | 8 | 0 |
| **Total** | **95** | **50** | **41** | **4** |

### 8.2 ASIL Coverage

| ASIL | Test Count | Coverage |
|------|------------|----------|
| ASIL-D | 45 | 100% |
| ASIL-C | 8 | 100% |
| ASIL-B | 5 | 100% |
| QM | 37 | 100% |

---

## 9. Traceability

### 9.1 Requirement to Test Traceability

| System Requirement | Qualification Tests |
|-------------------|-------------------|
| TSR-001 | QT-FUNC-001..003 |
| TSR-002 | QT-FUNC-010 |
| TSR-003 | QT-FUNC-020..021 |
| TSR-004 | QT-FUNC-030..031, QT-SAF-030..031 |
| TSR-005 | QT-FUNC-040..041 |
| TSR-006 | QT-SAF-001..004 |
| TSR-007 | QT-SAF-010..011 |
| TSR-008 | QT-SAF-010, QT-PERF-002 |
| TSR-009 | QT-SAF-020..021 |
| TSR-010 | (CAN tests) |
| SG-001 | QT-SAF-004 |
| SG-002 | QT-SAF-001 |
| SG-003 | QT-SAF-002 |
| SG-004 | QT-SAF-003 |

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-12-16 | Initial release |

---

**Generated by**: PARVIS-AI System Qualification Testing
**Project**: foxBMS Battery Management System
**Compliance**: ISO 26262:2018, ASPICE 3.1 SYS.5
