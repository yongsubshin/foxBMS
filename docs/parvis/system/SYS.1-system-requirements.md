# foxBMS System Requirements Specification

**Document ID**: FBMS-WP-SYS1-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Released
**Classification**: Technical
**ASPICE Process**: SYS.1 (System Requirements Analysis)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author          | Description                    |
|---------|------------|-----------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI | Initial system requirements |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| System Engineer       |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This System Requirements Specification (SyRS) defines the system-level requirements for the foxBMS Battery Management System. It establishes the functional, safety, and interface requirements that drive the software and hardware design.

### 1.2 Scope

This document covers:
- System functional requirements
- Safety requirements derived from TSC (Technical Safety Concept)
- Interface requirements with external systems
- Non-functional requirements (performance, reliability)
- Traceability to software requirements (SWE.1)

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|------------|
| ASIL | Automotive Safety Integrity Level |
| BMS | Battery Management System |
| TSC | Technical Safety Concept |
| FSR | Functional Safety Requirement |
| TSR | Technical Safety Requirement |
| EMC | Electromagnetic Compatibility |
| HARA | Hazard Analysis and Risk Assessment |
| HV | High Voltage (>60V DC) |
| IMD | Insulation Monitoring Device |
| SOC | State of Charge |
| SOH | State of Health |

### 1.4 References

| Document ID | Title |
|-------------|-------|
| ISO 26262:2018 | Road vehicles - Functional safety |
| ASPICE v3.1 | Automotive SPICE Process Reference Model |
| IEC 62660-1 | Secondary lithium-ion cells |
| FBMS-WP-SWE1-001 | Software Requirements Specification |

---

## 2. System Overview

### 2.1 System Context

The foxBMS Battery Management System is an embedded electronic control unit designed to monitor, protect, and manage rechargeable lithium-ion battery packs in automotive and industrial applications.

### 2.2 System Boundaries

**In Scope**:
- Cell voltage and temperature monitoring
- Battery pack current measurement
- State estimation (SOC, SOH, SOE, SOF)
- Contactor control and precharge management
- Cell balancing
- Fault detection and safe state management
- External communication (CAN)

**Out of Scope**:
- Battery cells and modules (hardware)
- External power electronics
- Vehicle control logic
- Charging infrastructure

### 2.3 Operating Environment

| Parameter | Specification |
|-----------|--------------|
| Operating Temperature | -40C to +85C |
| Storage Temperature | -40C to +105C |
| Supply Voltage | 10V to 32V DC |
| Humidity | 0% to 95% non-condensing |
| Vibration | ISO 16750-3 |
| EMC | ISO 11452, ISO 7637 |

---

## 3. Safety Requirements (TSC-Derived)

### 3.1 Safety Goals

The following safety goals are derived from HARA (Hazard Analysis and Risk Assessment):

#### SG-001: Prevent Thermal Runaway

| Attribute | Value |
|-----------|-------|
| ID | SG-001 |
| Description | The BMS shall prevent battery thermal runaway under all operating conditions |
| ASIL | ASIL-D |
| Safe State | Open all contactors, inhibit charging/discharging |
| FTTI | 100ms |

#### SG-002: Prevent Overcharge

| Attribute | Value |
|-----------|-------|
| ID | SG-002 |
| Description | The BMS shall prevent cell overcharge above maximum voltage limits |
| ASIL | ASIL-D |
| Safe State | Open contactors, request charge termination |
| FTTI | 1s |

#### SG-003: Prevent Overdischarge

| Attribute | Value |
|-----------|-------|
| ID | SG-003 |
| Description | The BMS shall prevent cell overdischarge below minimum voltage limits |
| ASIL | ASIL-C |
| Safe State | Open contactors, inhibit discharge |
| FTTI | 10s |

#### SG-004: Prevent Overcurrent

| Attribute | Value |
|-----------|-------|
| ID | SG-004 |
| Description | The BMS shall prevent battery overcurrent conditions |
| ASIL | ASIL-D |
| Safe State | Open contactors immediately |
| FTTI | 50ms |

#### SG-005: Prevent High Voltage Hazard

| Attribute | Value |
|-----------|-------|
| ID | SG-005 |
| Description | The BMS shall prevent unintended HV exposure to personnel |
| ASIL | ASIL-D |
| Safe State | Open contactors, verify isolation |
| FTTI | 100ms |

### 3.2 Technical Safety Requirements

#### TSR-001: Cell Voltage Monitoring

| Attribute | Value |
|-----------|-------|
| ID | TSR-001 |
| Description | The system shall measure each cell voltage with accuracy of +/-2mV |
| Parent | SG-001, SG-002, SG-003 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Measurement range: 0V to 5V per cell
- Accuracy: +/-2mV at 25C, +/-5mV over temperature
- Update rate: 100ms maximum
- Fault detection: Open wire, short circuit

#### TSR-002: Temperature Monitoring

| Attribute | Value |
|-----------|-------|
| ID | TSR-002 |
| Description | The system shall measure battery temperature with accuracy of +/-2C |
| Parent | SG-001 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Measurement range: -40C to +85C
- Accuracy: +/-2C
- Update rate: 1s maximum
- Minimum sensors: 2 per module

#### TSR-003: Current Measurement

| Attribute | Value |
|-----------|-------|
| ID | TSR-003 |
| Description | The system shall measure pack current with accuracy of +/-1% |
| Parent | SG-004 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Measurement range: -500A to +500A
- Accuracy: +/-1% of full scale
- Update rate: 10ms maximum
- Redundant measurement capability

#### TSR-004: Contactor Control

| Attribute | Value |
|-----------|-------|
| ID | TSR-004 |
| Description | The system shall control battery contactors with feedback verification |
| Parent | SG-001, SG-004, SG-005 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Control outputs: PLUS, MINUS, PRECHARGE contactors
- Feedback monitoring: Auxiliary contacts
- Response time: <10ms command to action
- Welding detection: Required

#### TSR-005: Precharge Sequence

| Attribute | Value |
|-----------|-------|
| ID | TSR-005 |
| Description | The system shall perform controlled precharge before main contactor closing |
| Parent | SG-004 |
| ASIL | ASIL-C |
| Verification | Test |

**Acceptance Criteria**:
- Precharge voltage threshold: 95% of battery voltage
- Maximum precharge time: 5s (configurable)
- Retry attempts: 3 maximum
- Failure action: Abort and safe state

#### TSR-006: Safe Operating Area Monitoring

| Attribute | Value |
|-----------|-------|
| ID | TSR-006 |
| Description | The system shall continuously monitor SOA limits and take protective action |
| Parent | SG-001, SG-002, SG-003, SG-004 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Voltage limits: Min 2.5V, Max 4.2V per cell (configurable)
- Temperature limits: Max 60C (configurable)
- Current limits: Based on cell specification
- Response time: <100ms

#### TSR-007: Fault Detection and Diagnosis

| Attribute | Value |
|-----------|-------|
| ID | TSR-007 |
| Description | The system shall detect, record, and respond to all safety-relevant faults |
| Parent | SG-001, SG-002, SG-003, SG-004, SG-005 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Fault categories: Warning, Error, Fatal
- Fatal fault response: Immediate safe state
- Fault logging: Non-volatile storage
- Diagnostic readout: Via CAN

#### TSR-008: Safe State Transition

| Attribute | Value |
|-----------|-------|
| ID | TSR-008 |
| Description | The system shall transition to safe state upon detecting fatal errors |
| Parent | SG-001, SG-004, SG-005 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Safe state: All contactors open
- Transition time: <100ms
- State persistence: Until reset by external command
- Indication: Via CAN and status output

#### TSR-009: Watchdog Supervision

| Attribute | Value |
|-----------|-------|
| ID | TSR-009 |
| Description | The system shall implement hardware watchdog for MCU supervision |
| Parent | SG-001, SG-004 |
| ASIL | ASIL-D |
| Verification | Test |

**Acceptance Criteria**:
- Watchdog type: External (SBC-based)
- Window time: 100ms nominal
- Failure action: MCU reset, contactors open
- Independence: Hardware path separate from MCU

#### TSR-010: Communication Integrity

| Attribute | Value |
|-----------|-------|
| ID | TSR-010 |
| Description | The system shall ensure communication integrity for safety-relevant data |
| Parent | SG-001, SG-004 |
| ASIL | ASIL-C |
| Verification | Test |

**Acceptance Criteria**:
- AFE communication: CRC validation
- CAN communication: Message counters, timeouts
- Error detection: E2E protection where required

---

## 4. Functional Requirements

### 4.1 Measurement Functions

#### SYS-FUNC-001: Cell Voltage Acquisition

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-001 |
| Description | The system shall acquire voltage measurements from all battery cells |
| Priority | Critical |
| Related TSR | TSR-001 |

**Functional Behavior**:
- Support multiple AFE IC types (ADI, LTC, Maxim, NXP)
- Configurable cell count per string
- Multi-string support (up to 8 strings)
- Automatic open wire detection

#### SYS-FUNC-002: Temperature Acquisition

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-002 |
| Description | The system shall acquire temperature measurements from all sensors |
| Priority | Critical |
| Related TSR | TSR-002 |

**Functional Behavior**:
- Support multiple NTC sensor types
- Configurable sensor count per module
- Temperature averaging and filtering
- Sensor fault detection

#### SYS-FUNC-003: Current Acquisition

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-003 |
| Description | The system shall acquire pack current measurements |
| Priority | Critical |
| Related TSR | TSR-003 |

**Functional Behavior**:
- Hall effect sensor interface
- Current direction detection
- Offset calibration support
- Redundant sensor option

### 4.2 State Estimation Functions

#### SYS-FUNC-010: SOC Estimation

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-010 |
| Description | The system shall estimate State of Charge for each string |
| Priority | High |
| Accuracy | +/-5% |

**Functional Behavior**:
- Coulomb counting algorithm
- OCV-based correction
- Temperature compensation
- Persistent storage of SOC

#### SYS-FUNC-011: SOH Estimation

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-011 |
| Description | The system shall estimate State of Health for the battery pack |
| Priority | Medium |
| Accuracy | +/-10% |

**Functional Behavior**:
- Capacity fade estimation
- Internal resistance estimation
- Trend analysis
- Maintenance indication

#### SYS-FUNC-012: SOE/SOF Estimation

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-012 |
| Description | The system shall estimate State of Energy and State of Function |
| Priority | Medium |

**Functional Behavior**:
- Available energy calculation
- Available power calculation
- Temperature-dependent limits
- Dynamic current limits

### 4.3 Control Functions

#### SYS-FUNC-020: BMS State Machine

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-020 |
| Description | The system shall implement a deterministic state machine for BMS control |
| Priority | Critical |
| Related TSR | TSR-008 |

**States**:
- UNINITIALIZED
- INITIALIZATION
- IDLE
- STANDBY
- PRECHARGE
- NORMAL
- ERROR

#### SYS-FUNC-021: Contactor Sequencing

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-021 |
| Description | The system shall control contactor opening/closing in defined sequence |
| Priority | Critical |
| Related TSR | TSR-004 |

**Functional Behavior**:
- Closing sequence: MINUS -> PRECHARGE -> wait -> PLUS -> open PRECHARGE
- Opening sequence: PLUS -> PRECHARGE (if needed) -> MINUS
- Timing verification between steps
- Feedback validation after each step

#### SYS-FUNC-022: Cell Balancing

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-022 |
| Description | The system shall balance cell voltages during charging |
| Priority | Medium |

**Functional Behavior**:
- Voltage-based balancing threshold
- Passive balancing via AFE
- Temperature limits during balancing
- Balancing status reporting

### 4.4 Communication Functions

#### SYS-FUNC-030: CAN Communication

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-030 |
| Description | The system shall provide CAN interface for external communication |
| Priority | High |
| Protocol | CAN 2.0B, 500 kbps |

**Functional Behavior**:
- Transmit: Pack status, cell voltages, temperatures, SOC, faults
- Receive: Control commands, configuration
- Message period: 10ms to 1s configurable
- Error handling: Bus-off recovery

#### SYS-FUNC-031: Diagnostic Interface

| Attribute | Value |
|-----------|-------|
| ID | SYS-FUNC-031 |
| Description | The system shall provide diagnostic readout capability |
| Priority | Medium |
| Protocol | UDS over CAN |

**Functional Behavior**:
- DTC reading and clearing
- Live data streaming
- Configuration access
- Calibration support

---

## 5. Interface Requirements

### 5.1 Hardware Interfaces

#### IF-HW-001: MCU Interface

| Attribute | Value |
|-----------|-------|
| ID | IF-HW-001 |
| MCU | TMS570LS12x (ARM Cortex-R4F) |
| Clock | 160 MHz |
| Flash | 1.25 MB |
| RAM | 192 KB |

#### IF-HW-002: AFE Interface

| Attribute | Value |
|-----------|-------|
| ID | IF-HW-002 |
| Interface | SPI / isoSPI |
| Speed | 1-2 MHz |
| Devices | ADI ADES183x, LTC6811/6813, Maxim MAX1785x, NXP MC33775A |

#### IF-HW-003: SBC Interface

| Attribute | Value |
|-----------|-------|
| ID | IF-HW-003 |
| Device | NXP FS85xx |
| Interface | SPI |
| Functions | Power supply, watchdog, fail-safe output |

#### IF-HW-004: CAN Interface

| Attribute | Value |
|-----------|-------|
| ID | IF-HW-004 |
| Channels | 2 (CAN1, CAN2) |
| Transceiver | TJA1043/1044 |
| Speed | 500 kbps (configurable) |

### 5.2 Software Interfaces

#### IF-SW-001: RTOS Interface

| Attribute | Value |
|-----------|-------|
| ID | IF-SW-001 |
| RTOS | FreeRTOS / SafeRTOS |
| Tasks | 1ms, 10ms, 100ms, Idle |

#### IF-SW-002: Application API

| Attribute | Value |
|-----------|-------|
| ID | IF-SW-002 |
| Style | Function call with struct parameters |
| Thread Safety | Mutex-protected database access |

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

#### NFR-PERF-001: Response Time

| Attribute | Value |
|-----------|-------|
| ID | NFR-PERF-001 |
| Requirement | Safety-critical response within 100ms |

#### NFR-PERF-002: Startup Time

| Attribute | Value |
|-----------|-------|
| ID | NFR-PERF-002 |
| Requirement | System operational within 500ms from power-on |

### 6.2 Reliability Requirements

#### NFR-REL-001: Availability

| Attribute | Value |
|-----------|-------|
| ID | NFR-REL-001 |
| Requirement | 99.99% availability during vehicle operation |

#### NFR-REL-002: Fault Tolerance

| Attribute | Value |
|-----------|-------|
| ID | NFR-REL-002 |
| Requirement | Single fault tolerance for all safety functions |

### 6.3 Safety Requirements

#### NFR-SAF-001: ASIL Compliance

| Attribute | Value |
|-----------|-------|
| ID | NFR-SAF-001 |
| Requirement | System shall achieve ASIL-D compliance per ISO 26262 |

#### NFR-SAF-002: Fail-Safe Design

| Attribute | Value |
|-----------|-------|
| ID | NFR-SAF-002 |
| Requirement | System shall fail to safe state under any single fault |

---

## 7. Traceability

### 7.1 Requirements Traceability Matrix

| System Req | SW Requirements (SWE.1) | Test Cases |
|------------|-------------------------|------------|
| TSR-001 | FBMS-REQ-AFE-001..032 | TC-SYS-001..010 |
| TSR-002 | FBMS-REQ-TS-001..015 | TC-SYS-011..020 |
| TSR-003 | FBMS-REQ-MEAS-001..010 | TC-SYS-021..025 |
| TSR-004 | FBMS-REQ-CONT-001..020 | TC-SYS-026..040 |
| TSR-005 | FBMS-REQ-BMS-001..030 | TC-SYS-041..055 |
| TSR-006 | FBMS-REQ-SOA-001..015 | TC-SYS-056..070 |
| TSR-007 | FBMS-REQ-DIAG-001..025 | TC-SYS-071..085 |
| TSR-008 | FBMS-REQ-BMS-031..050 | TC-SYS-086..095 |
| TSR-009 | FBMS-REQ-SBC-001..023 | TC-SYS-096..105 |
| TSR-010 | FBMS-REQ-CAN-001..015 | TC-SYS-106..115 |

### 7.2 SWE.1 Allocation Summary

| Category | SW Requirement Count |
|----------|---------------------|
| AFE/Measurement | 78 |
| BMS Control | 111 |
| Algorithm | 79 |
| Contactor | 52 |
| Configuration | 100 |
| Drivers | 146 |
| Temperature | 82 |
| **Total** | **648** |

---

## 8. Appendices

### 8.1 Hazard Analysis Summary

| Hazard ID | Description | Severity | ASIL |
|-----------|-------------|----------|------|
| HAZ-001 | Battery thermal runaway | S3 | ASIL-D |
| HAZ-002 | Cell overcharge | S3 | ASIL-D |
| HAZ-003 | Cell overdischarge | S2 | ASIL-C |
| HAZ-004 | Overcurrent | S3 | ASIL-D |
| HAZ-005 | HV exposure | S3 | ASIL-D |
| HAZ-006 | Loss of isolation | S3 | ASIL-D |

### 8.2 Configuration Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| BS_NR_OF_STRINGS | 1-8 | 1 | Number of battery strings |
| BS_NR_OF_MODULES | 1-16 | 8 | Number of modules per string |
| BS_NR_OF_CELLS_PER_MODULE | 1-18 | 12 | Cells per module |
| BC_VOLTAGE_MAX_MSL | 3000-5000 mV | 4200 | Maximum cell voltage |
| BC_VOLTAGE_MIN_MSL | 2000-3500 mV | 2500 | Minimum cell voltage |
| BC_TEMPERATURE_MAX_DISCHARGE | 0-70 C | 60 | Max discharge temperature |

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-12-16 | Initial release |

---

**Generated by**: PARVIS-AI System Requirements Analysis
**Project**: foxBMS Battery Management System
**Compliance**: ISO 26262:2018, ASPICE 3.1 SYS.1
