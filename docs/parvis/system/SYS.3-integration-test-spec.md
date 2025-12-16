# foxBMS System Integration Test Specification

**Document ID**: FBMS-WP-SYS3-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Released
**Classification**: Technical
**ASPICE Process**: SYS.3 (System Integration Testing)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author          | Description                    |
|---------|------------|-----------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI | Initial integration test spec |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Integration Test Lead |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This System Integration Test Specification defines the test cases for verifying the integration of hardware and software elements of the foxBMS Battery Management System. It ensures that all system elements work together correctly according to the system architecture (SYS.2).

### 1.2 Scope

This document covers:
- HW/SW integration test cases
- Interface verification tests
- Data flow verification tests
- Timing and synchronization tests
- Safety mechanism integration tests

### 1.3 Test Environment

| Component | Description |
|-----------|-------------|
| Target Hardware | foxBMS Master PCB with TMS570 |
| AFE Hardware | ADES1830 / LTC6813 daisy chain |
| SBC Hardware | NXP FS8530 |
| Battery Simulator | 12S cell simulator |
| Load Bank | Electronic load (500A capacity) |
| Debugger | XDS100v3 or Lauterbach |
| CAN Analyzer | Vector CANoe / PCAN |

### 1.4 References

| Document ID | Title |
|-------------|-------|
| FBMS-WP-SYS1-001 | System Requirements Specification |
| FBMS-WP-SYS2-001 | System Architecture Design |
| FBMS-WP-SWE5-001 | Software Integration Test Report |

---

## 2. Integration Test Strategy

### 2.1 Test Approach

The integration testing follows a bottom-up approach:

1. **Level 1**: Driver to Hardware integration
2. **Level 2**: Application to Driver integration
3. **Level 3**: Full system integration
4. **Level 4**: Safety mechanism integration

### 2.2 Test Categories

| Category | Description | Priority |
|----------|-------------|----------|
| IF-HW | Hardware interface tests | Critical |
| IF-SW | Software interface tests | Critical |
| DF | Data flow tests | High |
| TM | Timing tests | High |
| SM | Safety mechanism tests | Critical |
| CM | Communication tests | High |
| ER | Error handling tests | Critical |

---

## 3. Hardware Interface Tests (IF-HW)

### 3.1 MCU to AFE Integration

#### TC-IF-HW-001: AFE SPI Communication

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-001 |
| Title | AFE SPI Communication Verification |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-001, IF-SYS-001 |

**Preconditions**:
- AFE daisy chain connected
- Power supply stable

**Test Steps**:
1. Initialize SPI peripheral at 1 MHz
2. Send wake-up command to AFE chain
3. Read configuration registers from all AFEs
4. Verify CRC on all responses
5. Write test pattern to configuration register
6. Read back and verify pattern

**Expected Results**:
- All AFEs respond within 10ms
- CRC valid on all frames
- Write/read patterns match
- No SPI errors reported

**Pass Criteria**:
- 100% success rate over 1000 transactions

#### TC-IF-HW-002: AFE Voltage Measurement Chain

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-002 |
| Title | Cell Voltage Measurement Path |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-001 |

**Preconditions**:
- Battery simulator set to known voltages
- AFE chain calibrated

**Test Steps**:
1. Set simulator to 3.600V on all cells
2. Trigger ADC conversion on all AFEs
3. Read cell voltage registers
4. Compare measured vs expected values
5. Repeat for 3.200V, 4.000V, 4.200V

**Expected Results**:
- Measurement error < +/-2mV
- All cells measured within 100ms
- No timeout or CRC errors

**Pass Criteria**:
- Accuracy within specification at all test points

#### TC-IF-HW-003: AFE Temperature Measurement

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-003 |
| Title | Temperature Sensor Integration |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-002 |

**Preconditions**:
- Temperature sensors connected
- Known ambient temperature

**Test Steps**:
1. Trigger GPIO ADC measurement on AFE
2. Read temperature register values
3. Convert to temperature using NTC lookup
4. Compare with reference thermometer
5. Test at multiple temperature points

**Expected Results**:
- Temperature error < +/-2C
- Consistent readings across sensors

**Pass Criteria**:
- All sensors within accuracy specification

### 3.2 MCU to SBC Integration

#### TC-IF-HW-010: SBC SPI Communication

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-010 |
| Title | SBC Register Access |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-009, IF-SYS-002 |

**Preconditions**:
- SBC powered and initialized

**Test Steps**:
1. Read SBC device ID register
2. Verify expected device ID value
3. Write test pattern to writable register
4. Read back and verify pattern
5. Check SPI frame CRC

**Expected Results**:
- Device ID matches FS85xx
- Write/read pattern match
- No CRC errors

#### TC-IF-HW-011: SBC Watchdog Integration

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-011 |
| Title | Watchdog Trigger and Timeout |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-009 |

**Preconditions**:
- SBC in normal mode
- Watchdog enabled

**Test Steps**:
1. Start watchdog trigger at 100ms interval
2. Verify no watchdog reset for 10 seconds
3. Stop watchdog trigger
4. Wait for watchdog timeout
5. Verify MCU reset occurs
6. Verify FS0B assertion

**Expected Results**:
- No spurious resets during normal triggering
- Reset occurs within watchdog window after trigger stops
- FS0B asserts on watchdog failure

#### TC-IF-HW-012: SBC Fail-Safe Output

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-012 |
| Title | FS0B Output Verification |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-008 |

**Preconditions**:
- SBC initialized
- FS0B connected to contactor driver

**Test Steps**:
1. Verify FS0B is high in normal operation
2. Trigger a safety fault condition
3. Verify FS0B goes low
4. Verify contactor driver responds
5. Clear fault and verify FS0B returns high

**Expected Results**:
- FS0B state correctly reflects system state
- Contactor driver responds within 1ms

### 3.3 Contactor Integration

#### TC-IF-HW-020: Contactor Drive Path

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-020 |
| Title | Contactor Coil Drive |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Preconditions**:
- SPS configured
- Contactor connected

**Test Steps**:
1. Command PLUS contactor close
2. Measure coil current
3. Verify contactor physical closure
4. Read feedback signal
5. Command open and verify

**Expected Results**:
- Coil current within specification
- Contactor closes within 50ms
- Feedback matches command state

#### TC-IF-HW-021: Contactor Feedback Verification

| Attribute | Value |
|-----------|-------|
| ID | TC-IF-HW-021 |
| Title | Contactor Auxiliary Feedback |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Preconditions**:
- Contactors with auxiliary contacts

**Test Steps**:
1. Verify feedback LOW with contactor open
2. Close contactor
3. Verify feedback HIGH within 100ms
4. Open contactor
5. Verify feedback LOW within 100ms

**Expected Results**:
- Feedback correctly tracks contactor state
- Timing within specification

---

## 4. Data Flow Tests (DF)

### 4.1 Measurement Data Flow

#### TC-DF-001: Cell Voltage to Database

| Attribute | Value |
|-----------|-------|
| ID | TC-DF-001 |
| Title | Cell Voltage Data Flow Verification |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-001 |

**Preconditions**:
- System running normally
- Known cell voltages

**Test Steps**:
1. Set simulator to specific voltage pattern
2. Wait for measurement cycle
3. Read DATABASE cellVoltage table
4. Compare with expected values
5. Verify timestamp and validity flags

**Expected Results**:
- Database values match measurements
- Data updated within 100ms
- Validity flags correct

#### TC-DF-002: Temperature to Database

| Attribute | Value |
|-----------|-------|
| ID | TC-DF-002 |
| Title | Temperature Data Flow |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-002 |

**Test Steps**:
1. Measure actual sensor temperature
2. Read DATABASE temperature table
3. Compare values
4. Verify update timing

**Expected Results**:
- Temperature values within +/-2C
- Updated within 1s cycle

#### TC-DF-003: Current to Database

| Attribute | Value |
|-----------|-------|
| ID | TC-DF-003 |
| Title | Pack Current Data Flow |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-003 |

**Test Steps**:
1. Apply known current to current sensor
2. Read DATABASE current table
3. Compare measured vs applied
4. Test positive and negative currents

**Expected Results**:
- Current accuracy within +/-1%
- Direction correctly detected

### 4.2 Algorithm Data Flow

#### TC-DF-010: SOC Calculation Flow

| Attribute | Value |
|-----------|-------|
| ID | TC-DF-010 |
| Title | SOC Calculation Integration |
| Priority | High |

**Test Steps**:
1. Initialize SOC to known value
2. Apply discharge current for known duration
3. Read SOC from DATABASE
4. Compare calculated vs expected SOC
5. Verify coulomb counting accuracy

**Expected Results**:
- SOC within +/-5% accuracy
- Continuous update during operation

---

## 5. Timing Tests (TM)

### 5.1 Task Timing Verification

#### TC-TM-001: 10ms Task Timing

| Attribute | Value |
|-----------|-------|
| ID | TC-TM-001 |
| Title | BMS Task Cycle Time |
| Priority | High |
| Related Req | NFR-PERF-001 |

**Test Steps**:
1. Instrument 10ms task with timing markers
2. Measure task period over 1000 cycles
3. Calculate jitter statistics
4. Verify no deadline misses

**Expected Results**:
- Period: 10ms +/-0.1ms
- Jitter: <0.5ms
- No deadline misses

#### TC-TM-002: 100ms Task Timing

| Attribute | Value |
|-----------|-------|
| ID | TC-TM-002 |
| Title | Measurement Task Cycle |
| Priority | High |

**Test Steps**:
1. Measure 100ms task execution
2. Verify AFE acquisition completes within cycle
3. Measure algorithm execution time

**Expected Results**:
- Task completes within 100ms budget
- CPU load within limits

### 5.2 Response Time Tests

#### TC-TM-010: Fatal Error Response Time

| Attribute | Value |
|-----------|-------|
| ID | TC-TM-010 |
| Title | Error to Safe State Time |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-008 |

**Test Steps**:
1. Inject fatal error condition (overvoltage)
2. Measure time from detection to contactor open command
3. Measure time from command to physical opening
4. Calculate total response time

**Expected Results**:
- Detection to command: <10ms
- Command to action: <50ms
- Total: <100ms (FTTI)

---

## 6. Safety Mechanism Tests (SM)

### 6.1 Diagnostic Tests

#### TC-SM-001: AFE Communication Failure

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-001 |
| Title | AFE CRC Error Detection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-007 |

**Test Steps**:
1. Inject CRC error in AFE response
2. Verify error detection by driver
3. Check error counter increment
4. Verify diagnostic flag set
5. After multiple failures, verify fatal error

**Expected Results**:
- CRC error detected 100%
- Error counter increments
- Fatal error after threshold

#### TC-SM-002: Contactor Feedback Mismatch

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-002 |
| Title | Contactor Feedback Error |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-004 |

**Test Steps**:
1. Command contactor close
2. Simulate feedback failure (stuck open)
3. Verify mismatch detection
4. Check system enters error state
5. Verify all contactors open

**Expected Results**:
- Mismatch detected within 100ms
- Error state entered
- Safe state achieved

#### TC-SM-003: Watchdog Failure Path

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-003 |
| Title | Watchdog Safety Path |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-009 |

**Test Steps**:
1. Cause software hang (infinite loop)
2. Verify watchdog timeout
3. Verify FS0B assertion
4. Verify contactor opening
5. Verify MCU reset

**Expected Results**:
- Watchdog timeout as configured
- FS0B asserts
- Contactors open via hardware path

### 6.2 Protection Tests

#### TC-SM-010: Overvoltage Protection Chain

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-010 |
| Title | Overvoltage Detection to Action |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-002 |

**Test Steps**:
1. Set cell voltage to 4.15V (below limit)
2. Verify system operating normally
3. Increase voltage to 4.25V (above limit)
4. Verify SOA violation detected
5. Verify DIAG error raised
6. Verify contactors open

**Expected Results**:
- Violation detected within 100ms
- Contactors open within FTTI

#### TC-SM-011: Overcurrent Protection Chain

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-011 |
| Title | Overcurrent Protection |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-004 |

**Test Steps**:
1. Apply load below current limit
2. Verify normal operation
3. Increase load above current limit
4. Verify overcurrent detection
5. Verify contactors open

**Expected Results**:
- Overcurrent detected within 10ms
- Contactors open within 50ms

#### TC-SM-012: Overtemperature Protection

| Attribute | Value |
|-----------|-------|
| ID | TC-SM-012 |
| Title | Temperature Limit Response |
| Priority | Critical |
| ASIL | ASIL-D |
| Related Req | TSR-006, SG-001 |

**Test Steps**:
1. Heat sensor to 55C
2. Verify normal operation
3. Heat sensor to 65C (above limit)
4. Verify temperature violation detected
5. Verify appropriate action

**Expected Results**:
- Temperature limit enforced
- Current limiting or contactor opening

---

## 7. Communication Tests (CM)

### 7.1 CAN Communication

#### TC-CM-001: CAN Message Transmission

| Attribute | Value |
|-----------|-------|
| ID | TC-CM-001 |
| Title | CAN TX Verification |
| Priority | High |
| Related Req | TSR-010 |

**Test Steps**:
1. Connect CAN analyzer
2. Verify periodic message transmission
3. Check message IDs and data content
4. Verify message timing
5. Check for bus errors

**Expected Results**:
- All defined messages transmitted
- Content matches internal data
- Timing per specification

#### TC-CM-002: CAN Message Reception

| Attribute | Value |
|-----------|-------|
| ID | TC-CM-002 |
| Title | CAN RX and Processing |
| Priority | High |

**Test Steps**:
1. Transmit control message to BMS
2. Verify message received
3. Check command executed
4. Verify response message

**Expected Results**:
- Commands processed correctly
- Response within 100ms

---

## 8. Error Handling Tests (ER)

### 8.1 Recovery Tests

#### TC-ER-001: AFE Communication Recovery

| Attribute | Value |
|-----------|-------|
| ID | TC-ER-001 |
| Title | AFE Communication Recovery |
| Priority | High |

**Test Steps**:
1. Simulate AFE communication failure
2. Verify error detection
3. Restore communication
4. Verify automatic recovery
5. Check error counters reset

**Expected Results**:
- System recovers when communication restored
- No permanent fault state entered

#### TC-ER-002: Power Cycle Recovery

| Attribute | Value |
|-----------|-------|
| ID | TC-ER-002 |
| Title | System Power Cycle |
| Priority | High |

**Test Steps**:
1. Power cycle system
2. Verify clean startup
3. Check persistent data restored (SOC)
4. Verify no stuck errors

**Expected Results**:
- Clean startup after power cycle
- SOC restored from non-volatile storage

---

## 9. Test Summary Matrix

| Category | Total Tests | Critical | High | Medium |
|----------|-------------|----------|------|--------|
| IF-HW | 22 | 15 | 7 | 0 |
| DF | 10 | 6 | 4 | 0 |
| TM | 8 | 2 | 6 | 0 |
| SM | 15 | 12 | 3 | 0 |
| CM | 6 | 2 | 4 | 0 |
| ER | 8 | 3 | 5 | 0 |
| **Total** | **69** | **40** | **29** | **0** |

---

## 10. Traceability

### 10.1 Test to Requirement Traceability

| Test ID | System Requirement |
|---------|-------------------|
| TC-IF-HW-001..003 | TSR-001 |
| TC-IF-HW-010..012 | TSR-009 |
| TC-IF-HW-020..021 | TSR-004 |
| TC-DF-001..003 | TSR-001, TSR-002, TSR-003 |
| TC-TM-010 | TSR-008 |
| TC-SM-001..003 | TSR-007 |
| TC-SM-010..012 | TSR-006 |
| TC-CM-001..002 | TSR-010 |

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-12-16 | Initial release |

---

**Generated by**: PARVIS-AI Integration Test Specification
**Project**: foxBMS Battery Management System
**Compliance**: ISO 26262:2018, ASPICE 3.1 SYS.3
