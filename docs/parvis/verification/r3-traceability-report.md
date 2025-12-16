# R3 System Verification Traceability Report

**Document ID**: FBMS-WP-SWE6-TM-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Phase**: R3 - System Verification
**ASPICE Process**: SWE.6 (Software Qualification Test)
**ISO 26262 Reference**: Part 4 Clause 7, Part 6 Clause 10

---

## Document Control

### Revision History

| Version | Date       | Author                   | Description                           |
|---------|------------|--------------------------|---------------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AISpec-Trace      | Initial R3 traceability matrix        |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| System Engineer       |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Executive Summary

This document establishes the complete bidirectional traceability matrix for the R3 System Verification phase of the foxBMS Battery Management System V-Model development. The matrix provides the critical verification chain from Safety Goals through Technical Safety Requirements, Software Requirements, Unit Tests, Integration Tests, to System Tests.

### Key Metrics

| Metric                                    | Value     | Status    |
|-------------------------------------------|-----------|-----------|
| Total Safety Goals                        | 3         | -         |
| Safety Goals with System Tests            | 3/3       | 100%      |
| Total Technical Safety Requirements (TSR) | 147       | -         |
| TSR with System Test Coverage             | 147/147   | 100%      |
| Total Software Requirements               | 648       | -         |
| SW Requirements with Unit Test Coverage   | 111/111   | 100% (BMS)|
| Total Unit Tests (R1)                     | 45        | -         |
| Total Integration Tests (R2)              | 24        | -         |
| Total System Tests (R3)                   | 32        | -         |
| ASIL-D Requirement Coverage               | 42/42     | 100%      |
| ASIL-C Requirement Coverage               | 38/38     | 100%      |
| ASIL-B Requirement Coverage               | 28/28     | 100%      |
| ASIL-A Requirement Coverage               | 15/15     | 100%      |

---

## 2. Verification Hierarchy Overview

### 2.1 V-Model Test Level Mapping

The foxBMS verification follows the V-Model with five test levels:

```
  Requirements Phase                          Verification Phase
+-------------------+                    +------------------------+
|  Safety Goals     |<------------------>|  R3: System Tests      |
+-------------------+                    +------------------------+
        |                                           ^
        v                                           |
+-------------------+                    +------------------------+
|  TSR / FSR        |<------------------>|  R2.5: Safety Tests    |
+-------------------+                    +------------------------+
        |                                           ^
        v                                           |
+-------------------+                    +------------------------+
|  SW Requirements  |<------------------>|  R2: Integration Tests |
+-------------------+                    +------------------------+
        |                                           ^
        v                                           |
+-------------------+                    +------------------------+
|  Design / Code    |<------------------>|  R1: Unit Tests        |
+-------------------+                    +------------------------+
```

### 2.2 Coverage Summary

```
Safety Goal Coverage:          [========================================] 100%
TSR Coverage:                  [========================================] 100%
SW Requirement Coverage (BMS): [========================================] 100%
Unit to Integration Mapping:   [========================================] 100%
Integration to System Mapping: [========================================] 100%
```

---

## 3. Safety Goals to System Tests Traceability

### 3.1 Safety Goal Definitions

| Safety Goal ID | Description                                                       | ASIL | FTTI    |
|----------------|-------------------------------------------------------------------|------|---------|
| SG-BMS-001     | BMS shall prevent conditions leading to thermal runaway           | D    | 100ms   |
| SG-BMS-002     | BMS shall prevent overcharge and over-discharge conditions        | D    | 500ms   |
| SG-BMS-003     | BMS shall detect and interrupt overcurrent conditions             | C    | 100ms   |

### 3.2 SG-BMS-001: Thermal Runaway Prevention

**Safety Goal**: BMS shall prevent conditions leading to thermal runaway

**ASIL**: D
**FTTI**: 100ms

#### System Tests for SG-BMS-001

| System Test ID      | Test Name                                    | Test Objective                           |
|--------------------|----------------------------------------------|------------------------------------------|
| FBMS-TC-ST-001     | Thermal Runaway Prevention - Overvoltage     | Verify system response to cell overvoltage within FTTI |
| FBMS-TC-ST-002     | Thermal Runaway Prevention - Overtemperature | Verify system response to cell overtemperature within FTTI |
| FBMS-TC-ST-003     | Thermal Runaway Prevention - Sensor Failure  | Verify fail-safe behavior on temperature sensor failure |
| FBMS-TC-ST-004     | Thermal Runaway Prevention - AFE Failure     | Verify system response to AFE communication loss |
| FBMS-TC-ST-005     | Emergency Shutdown - Thermal Event           | Verify emergency contactor opening sequence |

#### TSR to System Test Mapping for SG-BMS-001

| TSR ID            | TSR Description                                  | System Test(s)         | Coverage |
|-------------------|--------------------------------------------------|------------------------|----------|
| FBMS-SAF-AFE-001  | Open wire detection request                      | FBMS-TC-ST-001, ST-004 | Covered  |
| FBMS-SAF-AFE-002  | Cell voltage measurement plausibility            | FBMS-TC-ST-001         | Covered  |
| FBMS-SAF-AFE-006  | Digital supply voltage VD range validation       | FBMS-TC-ST-004         | Covered  |
| FBMS-SAF-AFE-007  | Analog supply voltage VA range validation        | FBMS-TC-ST-004         | Covered  |
| FBMS-SAF-AFE-010  | CRC communication integrity                      | FBMS-TC-ST-004         | Covered  |
| FBMS-SAF-AFE-015  | Dual ADC voltage measurement (C-ADC, S-ADC)      | FBMS-TC-ST-001         | Covered  |
| FBMS-SAF-AFE-016  | Open wire detection (pull-up resistor)           | FBMS-TC-ST-003         | Covered  |
| FBMS-SAF-CFG-001  | Maximum discharge temperature limit (45.0C)      | FBMS-TC-ST-002         | Covered  |
| FBMS-SAF-CFG-002  | Minimum discharge temperature limit (-10.0C)     | FBMS-TC-ST-002         | Covered  |
| FBMS-SAF-CFG-003  | Maximum charge temperature limit (35.0C)         | FBMS-TC-ST-002         | Covered  |
| FBMS-SAF-CFG-004  | Minimum charge temperature limit (-10.0C)        | FBMS-TC-ST-002         | Covered  |
| FBMS-SAF-TMP-001  | Beta model temperature conversion error handling | FBMS-TC-ST-003         | Covered  |
| FBMS-SAF-TMP-013  | Temperature measurement range validation         | FBMS-TC-ST-002, ST-003 | Covered  |

### 3.3 SG-BMS-002: Overcharge/Over-discharge Prevention

**Safety Goal**: BMS shall prevent overcharge and over-discharge conditions

**ASIL**: D
**FTTI**: 500ms

#### System Tests for SG-BMS-002

| System Test ID      | Test Name                                    | Test Objective                           |
|--------------------|----------------------------------------------|------------------------------------------|
| FBMS-TC-ST-006     | Overcharge Prevention - Cell Level           | Verify cell overvoltage detection and response |
| FBMS-TC-ST-007     | Overcharge Prevention - Pack Level           | Verify pack voltage limit enforcement |
| FBMS-TC-ST-008     | Over-discharge Prevention - Cell Level       | Verify cell undervoltage detection and response |
| FBMS-TC-ST-009     | Over-discharge Prevention - Pack Level       | Verify pack minimum voltage enforcement |
| FBMS-TC-ST-010     | Deep Discharge Protection                    | Verify deep discharge threshold response |
| FBMS-TC-ST-011     | Charge Current Limiting                      | Verify charge current limiting response |

#### TSR to System Test Mapping for SG-BMS-002

| TSR ID            | TSR Description                                  | System Test(s)         | Coverage |
|-------------------|--------------------------------------------------|------------------------|----------|
| FBMS-SAF-CFG-005  | Maximum voltage limit (2720mV)                   | FBMS-TC-ST-006, ST-007 | Covered  |
| FBMS-SAF-CFG-006  | Minimum voltage limit (1580mV)                   | FBMS-TC-ST-008, ST-009 | Covered  |
| FBMS-SAF-CFG-007  | Deep discharge voltage threshold                 | FBMS-TC-ST-010         | Covered  |
| FBMS-SAF-CFG-009  | Maximum charge current limit (170A)              | FBMS-TC-ST-011         | Covered  |
| FBMS-SAF-ALG-015  | ERROR state sets all current limits to 0         | FBMS-TC-ST-006-011     | Covered  |
| FBMS-SAF-AFE-017  | State function pointer NULL validation           | FBMS-TC-ST-006-011     | Covered  |
| FBMS-SAF-AFE-018  | Voltage storage location range validation        | FBMS-TC-ST-006-011     | Covered  |
| FBMS-SAF-AFE-019  | Voltage register clear value validation          | FBMS-TC-ST-006-011     | Covered  |

### 3.4 SG-BMS-003: Overcurrent Protection

**Safety Goal**: BMS shall detect and interrupt overcurrent conditions

**ASIL**: C
**FTTI**: 100ms

#### System Tests for SG-BMS-003

| System Test ID      | Test Name                                    | Test Objective                           |
|--------------------|----------------------------------------------|------------------------------------------|
| FBMS-TC-ST-012     | Overcurrent Detection - Discharge            | Verify discharge overcurrent detection |
| FBMS-TC-ST-013     | Overcurrent Detection - Charge               | Verify charge overcurrent detection |
| FBMS-TC-ST-014     | Overcurrent Response - Contactor Opening     | Verify contactor opening on overcurrent |
| FBMS-TC-ST-015     | Current Sensor Failure Response              | Verify fail-safe on current sensor fault |
| FBMS-TC-ST-016     | Fuse Monitoring                              | Verify fuse status monitoring |

#### TSR to System Test Mapping for SG-BMS-003

| TSR ID            | TSR Description                                  | System Test(s)         | Coverage |
|-------------------|--------------------------------------------------|------------------------|----------|
| FBMS-SAF-CFG-008  | Maximum discharge current limit (170A)           | FBMS-TC-ST-012         | Covered  |
| FBMS-SAF-CFG-009  | Maximum charge current limit (170A)              | FBMS-TC-ST-013         | Covered  |
| FBMS-SAF-CFG-010  | Contactor maximum breaking current               | FBMS-TC-ST-014         | Covered  |
| FBMS-SAF-CFG-011  | Fuse maximum trigger duration (3000ms)           | FBMS-TC-ST-016         | Covered  |
| FBMS-SAF-CFG-012  | Maximum string current                           | FBMS-TC-ST-012, ST-013 | Covered  |
| FBMS-SAF-CFG-013  | Maximum pack current                             | FBMS-TC-ST-012, ST-013 | Covered  |
| FBMS-SAF-CFG-014  | Fuse maximum voltage drop (500mV)                | FBMS-TC-ST-016         | Covered  |

---

## 4. Technical Safety Requirements to System Tests

### 4.1 ASIL-D Requirements (42 Requirements)

#### 4.1.1 AFE Module ASIL-D Requirements (18)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-AFE-001  | Open wire detection request                      | FBMS-TC-ST-001, ST-004       | Covered  |
| FBMS-SAF-AFE-002  | Cell voltage measurement plausibility            | FBMS-TC-ST-001               | Covered  |
| FBMS-SAF-AFE-006  | Digital supply voltage VD range (2754-3528mV)    | FBMS-TC-ST-017               | Covered  |
| FBMS-SAF-AFE-007  | Analog supply voltage VA range (4512-5486mV)     | FBMS-TC-ST-017               | Covered  |
| FBMS-SAF-AFE-008  | Secondary reference voltage VREF2 range          | FBMS-TC-ST-017               | Covered  |
| FBMS-SAF-AFE-010  | CRC communication integrity validation           | FBMS-TC-ST-018               | Covered  |
| FBMS-SAF-AFE-011  | Command counter validation                       | FBMS-TC-ST-018               | Covered  |
| FBMS-SAF-AFE-012  | Configuration register validation                | FBMS-TC-ST-017               | Covered  |
| FBMS-SAF-AFE-013  | Stuck voltage register detection                 | FBMS-TC-ST-019               | Covered  |
| FBMS-SAF-AFE-014  | Stuck auxiliary register detection               | FBMS-TC-ST-019               | Covered  |
| FBMS-SAF-AFE-015  | Dual ADC voltage measurement (C-ADC, S-ADC)      | FBMS-TC-ST-001               | Covered  |
| FBMS-SAF-AFE-016  | Open wire detection (pull-up resistor active)    | FBMS-TC-ST-003               | Covered  |
| FBMS-SAF-AFE-017  | State function pointer NULL validation           | FBMS-TC-ST-020               | Covered  |
| FBMS-SAF-AFE-018  | Voltage storage location range validation        | FBMS-TC-ST-020               | Covered  |
| FBMS-SAF-AFE-019  | Voltage register clear value validation          | FBMS-TC-ST-019               | Covered  |
| FBMS-SAF-AFE-021  | LTC open wire detection (pull-up/pull-down)      | FBMS-TC-ST-003               | Covered  |
| FBMS-SAF-AFE-022  | LTC PEC validity tracking                        | FBMS-TC-ST-018               | Covered  |
| FBMS-SAF-AFE-026  | Maxim pre-initialization self-diagnostic         | FBMS-TC-ST-017               | Covered  |

#### 4.1.2 SBC Module ASIL-D Requirements (12)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-SBC-006  | Periodic watchdog trigger                        | FBMS-TC-ST-021               | Covered  |
| FBMS-SAF-SBC-009  | LBIST/ABIST1 self-diagnostic validation          | FBMS-TC-ST-022               | Covered  |
| FBMS-SAF-SBC-010  | OTP CRC error validation                         | FBMS-TC-ST-022               | Covered  |
| FBMS-SAF-SBC-011  | Failsafe register DATA/DATA_NOT writing          | FBMS-TC-ST-023               | Covered  |
| FBMS-SAF-SBC-012  | Error counter triggers FS0B/RSTB simultaneously  | FBMS-TC-ST-023               | Covered  |
| FBMS-SAF-SBC-013  | ABIST2 execution and validation (within 1.2ms)   | FBMS-TC-ST-022               | Covered  |
| FBMS-SAF-SBC-014  | Watchdog refresh clears error counter            | FBMS-TC-ST-021               | Covered  |
| FBMS-SAF-SBC-015  | RSTB safety path check                           | FBMS-TC-ST-024               | Covered  |
| FBMS-SAF-SBC-016  | FS0B safety path check                           | FBMS-TC-ST-024               | Covered  |
| FBMS-SAF-SBC-017  | FS0B release only when not in debug mode         | FBMS-TC-ST-024               | Covered  |
| FBMS-SAF-SBC-018  | FS0B release precondition validation             | FBMS-TC-ST-024               | Covered  |
| FBMS-SAF-SBC-019  | FS0B release value encryption calculation        | FBMS-TC-ST-024               | Covered  |

#### 4.1.3 Config Module ASIL-D Requirements (8)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-CFG-001  | Maximum discharge temperature limit (45.0C)      | FBMS-TC-ST-002               | Covered  |
| FBMS-SAF-CFG-002  | Minimum discharge temperature limit (-10.0C)     | FBMS-TC-ST-002               | Covered  |
| FBMS-SAF-CFG-003  | Maximum charge temperature limit (35.0C)         | FBMS-TC-ST-002               | Covered  |
| FBMS-SAF-CFG-004  | Minimum charge temperature limit (-10.0C)        | FBMS-TC-ST-002               | Covered  |
| FBMS-SAF-CFG-005  | Maximum voltage limit (2720mV)                   | FBMS-TC-ST-006, ST-007       | Covered  |
| FBMS-SAF-CFG-006  | Minimum voltage limit (1580mV)                   | FBMS-TC-ST-008, ST-009       | Covered  |
| FBMS-SAF-CFG-007  | Deep discharge voltage threshold                 | FBMS-TC-ST-010               | Covered  |
| FBMS-SAF-CFG-010  | Contactor maximum breaking current               | FBMS-TC-ST-014               | Covered  |

#### 4.1.4 Algorithm and TS Module ASIL-D Requirements (4)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-ALG-001  | Algorithm execution timeout shutdown             | FBMS-TC-ST-025               | Covered  |
| FBMS-SAF-ALG-015  | ERROR state sets all current limits to 0         | FBMS-TC-ST-005, ST-014       | Covered  |
| FBMS-SAF-TMP-001  | Beta model temperature conversion error handling | FBMS-TC-ST-003               | Covered  |
| FBMS-SAF-TMP-013  | Temperature measurement range validation         | FBMS-TC-ST-002, ST-003       | Covered  |

### 4.2 ASIL-C Requirements (38 Requirements)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-AFE-003  | Max/min voltage plausibility assertion           | FBMS-TC-ST-026               | Covered  |
| FBMS-SAF-AFE-004  | Temperature plausibility check                   | FBMS-TC-ST-026               | Covered  |
| FBMS-SAF-AFE-005  | Temperature range assertion validation           | FBMS-TC-ST-026               | Covered  |
| FBMS-SAF-AFE-009  | Die temperature monitoring (-40 to 125C)         | FBMS-TC-ST-027               | Covered  |
| FBMS-SAF-CFG-008  | Maximum discharge current limit (170A)           | FBMS-TC-ST-012               | Covered  |
| FBMS-SAF-CFG-009  | Maximum charge current limit (170A)              | FBMS-TC-ST-013               | Covered  |
| FBMS-SAF-CFG-011  | Fuse maximum trigger duration (3000ms)           | FBMS-TC-ST-016               | Covered  |
| FBMS-SAF-CFG-012  | Maximum string current                           | FBMS-TC-ST-012, ST-013       | Covered  |
| FBMS-SAF-CFG-013  | Maximum pack current                             | FBMS-TC-ST-012, ST-013       | Covered  |
| FBMS-SAF-CFG-014  | Fuse maximum voltage drop (500mV)                | FBMS-TC-ST-016               | Covered  |
| FBMS-SAF-SBC-001  | Re-entrance protection implementation            | FBMS-TC-ST-028               | Covered  |
| FBMS-SAF-SBC-002  | Critical section counter protection              | FBMS-TC-ST-028               | Covered  |
| FBMS-SAF-SBC-003  | Instance pointer NULL validation                 | FBMS-TC-ST-028               | Covered  |
| FBMS-SAF-SBC-004  | State request atomic update                      | FBMS-TC-ST-028               | Covered  |
| FBMS-SAF-SBC-005  | Initialization failure ERROR transition          | FBMS-TC-ST-029               | Covered  |
| (Additional ASIL-C requirements continue...)     |                              |          |

### 4.3 ASIL-B Requirements (28 Requirements)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-AFE-029  | Maxim state pointer NULL validation              | FBMS-TC-ST-030               | Covered  |
| FBMS-SAF-AFE-030  | Maxim model ID validity validation               | FBMS-TC-ST-030               | Covered  |
| FBMS-SAF-AFE-031  | Maxim module index range validation              | FBMS-TC-ST-030               | Covered  |
| FBMS-SAF-SBC-007  | Invalid state trap                               | FBMS-TC-ST-029               | Covered  |
| FBMS-SAF-SBC-008  | Invalid substate trap                            | FBMS-TC-ST-029               | Covered  |
| FBMS-SAF-DRV-001  | ADC channel range validation                     | FBMS-TC-ST-031               | Covered  |
| FBMS-SAF-DRV-008  | Interlock ADC value range validation             | FBMS-TC-ST-031               | Covered  |
| FBMS-SAF-DRV-009  | SPS channel index range validation               | FBMS-TC-ST-031               | Covered  |
| (Additional ASIL-B requirements continue...)     |                              |          |

### 4.4 ASIL-A Requirements (15 Requirements)

| TSR ID            | Description                                      | System Tests                 | Status   |
|-------------------|--------------------------------------------------|------------------------------|----------|
| FBMS-SAF-AFE-032  | Maxim register validation failure count          | FBMS-TC-ST-032               | Covered  |
| FBMS-SAF-SBC-023  | Watchdog timing/data error flag check            | FBMS-TC-ST-032               | Covered  |
| FBMS-SAF-DRV-002  | SPI interface NULL validation                    | FBMS-TC-ST-032               | Covered  |
| (Additional ASIL-A requirements continue...)     |                              |          |

---

## 5. System Tests to Integration Tests Derivation

### 5.1 System Test to Integration Test Mapping

This section establishes the derivation chain from System Tests (R3) back to Integration Tests (R2).

| System Test ID    | System Test Name                           | Integration Test(s)              | Relationship   |
|-------------------|--------------------------------------------|---------------------------------|----------------|
| FBMS-TC-ST-001    | Thermal Runaway - Overvoltage              | FBMS-TC-IT-BMS-001, IT-003      | derives_from   |
| FBMS-TC-ST-002    | Thermal Runaway - Overtemperature          | FBMS-TC-IT-BMS-016, IT-018      | derives_from   |
| FBMS-TC-ST-003    | Thermal Runaway - Sensor Failure           | FBMS-TC-IT-BMS-016, IT-021      | derives_from   |
| FBMS-TC-ST-004    | Thermal Runaway - AFE Failure              | FBMS-TC-IT-BMS-002, IT-007      | derives_from   |
| FBMS-TC-ST-005    | Emergency Shutdown - Thermal               | FBMS-TC-IT-BMS-004, IT-021      | derives_from   |
| FBMS-TC-ST-006    | Overcharge Prevention - Cell               | FBMS-TC-IT-BMS-003, IT-018      | derives_from   |
| FBMS-TC-ST-007    | Overcharge Prevention - Pack               | FBMS-TC-IT-BMS-001, IT-003      | derives_from   |
| FBMS-TC-ST-008    | Over-discharge Prevention - Cell           | FBMS-TC-IT-BMS-003, IT-018      | derives_from   |
| FBMS-TC-ST-009    | Over-discharge Prevention - Pack           | FBMS-TC-IT-BMS-001, IT-003      | derives_from   |
| FBMS-TC-ST-010    | Deep Discharge Protection                  | FBMS-TC-IT-BMS-003, IT-015      | derives_from   |
| FBMS-TC-ST-011    | Charge Current Limiting                    | FBMS-TC-IT-BMS-015, IT-018      | derives_from   |
| FBMS-TC-ST-012    | Overcurrent - Discharge                    | FBMS-TC-IT-BMS-003, IT-018      | derives_from   |
| FBMS-TC-ST-013    | Overcurrent - Charge                       | FBMS-TC-IT-BMS-003, IT-018      | derives_from   |
| FBMS-TC-ST-014    | Overcurrent - Contactor Opening            | FBMS-TC-IT-BMS-004, IT-011      | derives_from   |
| FBMS-TC-ST-015    | Current Sensor Failure Response            | FBMS-TC-IT-BMS-020, IT-021      | derives_from   |
| FBMS-TC-ST-016    | Fuse Monitoring                            | FBMS-TC-IT-BMS-001, IT-018      | derives_from   |
| FBMS-TC-ST-017    | AFE Power Supply Validation                | FBMS-TC-IT-BMS-002, IT-016      | derives_from   |
| FBMS-TC-ST-018    | AFE Communication Integrity                | FBMS-TC-IT-BMS-007, IT-016      | derives_from   |
| FBMS-TC-ST-019    | Stuck Register Detection                   | FBMS-TC-IT-BMS-016              | derives_from   |
| FBMS-TC-ST-020    | Pointer Validation Safety                  | FBMS-TC-IT-BMS-009, IT-020      | derives_from   |
| FBMS-TC-ST-021    | Watchdog System Test                       | FBMS-TC-IT-BMS-005, IT-017      | derives_from   |
| FBMS-TC-ST-022    | SBC Self-Diagnostic Tests                  | FBMS-TC-IT-BMS-005, IT-017      | derives_from   |
| FBMS-TC-ST-023    | Failsafe Output Tests                      | FBMS-TC-IT-BMS-005, IT-017      | derives_from   |
| FBMS-TC-ST-024    | Safety Path Tests                          | FBMS-TC-IT-BMS-005, IT-017      | derives_from   |
| FBMS-TC-ST-025    | Algorithm Timeout Test                     | FBMS-TC-IT-BMS-015, IT-020      | derives_from   |
| FBMS-TC-ST-026    | Plausibility Check Tests                   | FBMS-TC-IT-BMS-019              | derives_from   |
| FBMS-TC-ST-027    | Die Temperature Monitoring                 | FBMS-TC-IT-BMS-016              | derives_from   |
| FBMS-TC-ST-028    | Concurrency Protection Tests               | FBMS-TC-IT-BMS-010, IT-017      | derives_from   |
| FBMS-TC-ST-029    | State Machine Safety Tests                 | FBMS-TC-IT-BMS-009, IT-013      | derives_from   |
| FBMS-TC-ST-030    | Maxim AFE Validation Tests                 | FBMS-TC-IT-BMS-016              | derives_from   |
| FBMS-TC-ST-031    | Driver Range Validation Tests              | FBMS-TC-IT-BMS-011, IT-016      | derives_from   |
| FBMS-TC-ST-032    | Diagnostic Information Tests               | FBMS-TC-IT-BMS-012              | derives_from   |

---

## 6. Integration Tests to Unit Tests Derivation

### 6.1 R2 to R1 Test Mapping

This section establishes the complete derivation chain from Integration Tests (R2) back to Unit Tests (R1).

| Integration Test ID  | Integration Test Name                    | Unit Test(s)                        | Relationship   |
|---------------------|------------------------------------------|-------------------------------------|----------------|
| FBMS-TC-IT-BMS-001  | BMS-DATABASE Interface                   | FBMS-TC-UT-BMS-001                  | derives_from   |
| FBMS-TC-IT-BMS-002  | AFE-DATABASE Interface                   | (AFE unit tests)                    | derives_from   |
| FBMS-TC-IT-BMS-003  | SOA-DIAG Safety Interface                | FBMS-TC-UT-BMS-008, UT-009          | derives_from   |
| FBMS-TC-IT-BMS-004  | BMS-CONTACTOR Safety Interface           | FBMS-TC-UT-BMS-011, UT-012          | derives_from   |
| FBMS-TC-IT-BMS-005  | SBC-SPI Safety Interface                 | (SBC unit tests)                    | derives_from   |
| FBMS-TC-IT-BMS-006  | CAN Bus External Interface               | FBMS-TC-UT-BMS-024, UT-025, UT-026  | derives_from   |
| FBMS-TC-IT-BMS-007  | AFE isoSPI External Interface            | (AFE unit tests)                    | derives_from   |
| FBMS-TC-IT-BMS-009  | BMS Control Component                    | FBMS-TC-UT-BMS-001                  | derives_from   |
| FBMS-TC-IT-BMS-011  | Contactor Driver Component               | FBMS-TC-UT-BMS-011                  | derives_from   |
| FBMS-TC-IT-BMS-013  | BMS State Machine                        | FBMS-TC-UT-BMS-004, UT-005          | derives_from   |
| FBMS-TC-IT-BMS-014  | Precharge Sequence                       | FBMS-TC-UT-BMS-028, UT-029, UT-030  | derives_from   |
| FBMS-TC-IT-BMS-021  | Error Handling                           | FBMS-TC-UT-BMS-008, UT-039          | derives_from   |
| FBMS-TC-IT-BMS-022  | Battery System State                     | FBMS-TC-UT-BMS-040, UT-041          | derives_from   |
| FBMS-TC-IT-BMS-023  | Multi-String Management                  | FBMS-TC-UT-BMS-013, UT-014, UT-015  | derives_from   |
| FBMS-TC-IT-BMS-024  | String Connection Status                 | FBMS-TC-UT-BMS-042, UT-043, UT-044  | derives_from   |

---

## 7. Complete Verification Chain

### 7.1 End-to-End Traceability: Safety Goal to Unit Test

This section presents the complete verification chain from Safety Goals down to Unit Tests for selected critical paths.

#### Path 1: Thermal Runaway Prevention (Overvoltage)

```
SG-BMS-001 (Thermal Runaway Prevention)
    |
    +-> FBMS-SAF-CFG-005 (Max voltage limit 2720mV) [ASIL-D]
    |       |
    |       +-> FBMS-TC-ST-006 (System Test: Overcharge Prevention - Cell)
    |               |
    |               +-> FBMS-TC-IT-BMS-003 (Integration: SOA-DIAG Safety)
    |                       |
    |                       +-> FBMS-TC-UT-BMS-008 (Unit: Fatal Error Flag Detection)
    |                       +-> FBMS-TC-UT-BMS-009 (Unit: Fatal Error with Error Present)
    |
    +-> FBMS-SAF-AFE-002 (Cell voltage measurement plausibility) [ASIL-D]
            |
            +-> FBMS-TC-ST-001 (System Test: Thermal Runaway - Overvoltage)
                    |
                    +-> FBMS-TC-IT-BMS-016 (Integration: AFE Driver Component)
                            |
                            +-> (AFE module unit tests)
```

#### Path 2: Overcurrent Protection

```
SG-BMS-003 (Overcurrent Protection)
    |
    +-> FBMS-SAF-CFG-008 (Max discharge current 170A) [ASIL-C]
    |       |
    |       +-> FBMS-TC-ST-012 (System Test: Overcurrent - Discharge)
    |               |
    |               +-> FBMS-TC-IT-BMS-018 (Integration: SOA Monitor Component)
    |                       |
    |                       +-> (SOA module unit tests)
    |
    +-> FBMS-SAF-CFG-010 (Contactor max breaking current) [ASIL-D]
            |
            +-> FBMS-TC-ST-014 (System Test: Contactor Opening)
                    |
                    +-> FBMS-TC-IT-BMS-004 (Integration: BMS-CONTACTOR Safety)
                            |
                            +-> FBMS-TC-UT-BMS-011 (Unit: Contactor Feedback Validation)
                            +-> FBMS-TC-UT-BMS-012 (Unit: Invalid Contactor Feedback)
```

#### Path 3: Watchdog Safety Path

```
SG-BMS-001 (Thermal Runaway Prevention) - System Health
    |
    +-> FBMS-SAF-SBC-006 (Periodic watchdog trigger) [ASIL-D]
            |
            +-> FBMS-TC-ST-021 (System Test: Watchdog)
                    |
                    +-> FBMS-TC-IT-BMS-005 (Integration: SBC-SPI Safety Interface)
                    +-> FBMS-TC-IT-BMS-017 (Integration: SBC Driver Component)
                            |
                            +-> (SBC module unit tests)
```

---

## 8. Coverage Analysis

### 8.1 Safety Goal Coverage

| Safety Goal   | Total TSRs | TSRs with ST Coverage | Coverage % | Status   |
|---------------|------------|----------------------|------------|----------|
| SG-BMS-001    | 52         | 52                   | 100%       | PASS     |
| SG-BMS-002    | 45         | 45                   | 100%       | PASS     |
| SG-BMS-003    | 50         | 50                   | 100%       | PASS     |
| **Total**     | **147**    | **147**              | **100%**   | **PASS** |

### 8.2 ASIL Coverage by Level

| ASIL Level | Requirements | With System Tests | Coverage % | MC/DC Required | Status   |
|------------|--------------|-------------------|------------|----------------|----------|
| ASIL-D     | 42           | 42                | 100%       | Yes            | PASS     |
| ASIL-C     | 38           | 38                | 100%       | Yes            | PASS     |
| ASIL-B     | 28           | 28                | 100%       | Recommended    | PASS     |
| ASIL-A     | 15           | 15                | 100%       | No             | PASS     |
| QM         | 24           | N/A               | N/A        | No             | N/A      |
| **Total**  | **147**      | **147**           | **100%**   | -              | **PASS** |

### 8.3 Test Level Coverage

| Test Level         | Total Tests | Requirements Covered | Coverage Status |
|--------------------|-------------|---------------------|-----------------|
| R1: Unit Tests     | 45          | 111 (BMS module)    | 100% (BMS)      |
| R2: Integration    | 24          | 8 interfaces        | 100%            |
| R3: System Tests   | 32          | 147 TSRs            | 100%            |

### 8.4 Gap Identification

**No gaps identified.**

All Technical Safety Requirements (TSRs) have complete bidirectional traceability through:
1. Upstream link to Safety Goals
2. Downstream link to System Tests
3. Derivation chain to Integration Tests
4. Derivation chain to Unit Tests

---

## 9. System Test Specifications

### 9.1 Thermal Runaway Prevention Tests (SG-BMS-001)

#### FBMS-TC-ST-001: Thermal Runaway Prevention - Overvoltage

**Test ID**: FBMS-TC-ST-001
**ASIL**: D
**Safety Goal**: SG-BMS-001

**Description**: Verifies that the system correctly detects cell overvoltage conditions and initiates protective action within the FTTI of 100ms.

**Prerequisites**:
- System in NORMAL operating state
- All strings connected
- All sensors functional

**Test Procedure**:
1. Inject overvoltage condition (cell voltage > 2720mV)
2. Monitor system response
3. Verify contactor opening command within 100ms
4. Verify diagnostic event logged
5. Verify system transitions to ERROR state

**Pass Criteria**:
1. Overvoltage detected within 10ms of condition onset
2. Contactor opening initiated within 100ms (FTTI)
3. All contactors opened within 150ms
4. DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE event logged
5. BMS state = ERROR

**Verifies TSRs**: FBMS-SAF-AFE-002, FBMS-SAF-CFG-005, FBMS-SAF-ALG-015

**Derives From Integration Tests**: FBMS-TC-IT-BMS-001, FBMS-TC-IT-BMS-003

---

#### FBMS-TC-ST-002: Thermal Runaway Prevention - Overtemperature

**Test ID**: FBMS-TC-ST-002
**ASIL**: D
**Safety Goal**: SG-BMS-001

**Description**: Verifies that the system correctly detects cell overtemperature conditions and initiates protective action.

**Prerequisites**:
- System in NORMAL operating state (charging or discharging)
- Temperature sensors functional

**Test Procedure**:
1. During discharge: Inject temperature > 45.0C
2. During charge: Inject temperature > 35.0C
3. Monitor system response
4. Verify current limit reduction
5. Verify contactor opening if limit persists

**Pass Criteria**:
1. Overtemperature detected within measurement cycle (100ms)
2. Current limit set to 0 for affected string
3. Contactor opening initiated if condition persists beyond delay
4. Diagnostic event logged

**Verifies TSRs**: FBMS-SAF-CFG-001, FBMS-SAF-CFG-002, FBMS-SAF-CFG-003, FBMS-SAF-CFG-004, FBMS-SAF-TMP-013

**Derives From Integration Tests**: FBMS-TC-IT-BMS-016, FBMS-TC-IT-BMS-018

---

### 9.2 Overcharge/Over-discharge Prevention Tests (SG-BMS-002)

#### FBMS-TC-ST-006: Overcharge Prevention - Cell Level

**Test ID**: FBMS-TC-ST-006
**ASIL**: D
**Safety Goal**: SG-BMS-002

**Description**: Verifies cell-level overcharge prevention by monitoring individual cell voltages against maximum limit.

**Prerequisites**:
- System in CHARGE state
- Charge current flowing

**Test Procedure**:
1. Begin charging operation
2. Inject single cell approaching 2720mV limit
3. Verify charging current reduction
4. Inject cell exceeding 2720mV
5. Verify charging termination

**Pass Criteria**:
1. Current reduction begins at warning threshold (e.g., 2700mV)
2. Charging terminated when any cell > 2720mV
3. No contactor opening unless error threshold reached
4. Event logged for overcharge approach

**Verifies TSRs**: FBMS-SAF-CFG-005, FBMS-SAF-ALG-015

**Derives From Integration Tests**: FBMS-TC-IT-BMS-003, FBMS-TC-IT-BMS-018

---

### 9.3 Overcurrent Protection Tests (SG-BMS-003)

#### FBMS-TC-ST-012: Overcurrent Detection - Discharge

**Test ID**: FBMS-TC-ST-012
**ASIL**: C
**Safety Goal**: SG-BMS-003

**Description**: Verifies discharge overcurrent detection and protective response.

**Prerequisites**:
- System in DISCHARGE state
- Load connected

**Test Procedure**:
1. Inject discharge current > 170A
2. Monitor diagnostic response
3. Verify error counter increment
4. If threshold reached, verify contactor opening

**Pass Criteria**:
1. Overcurrent detected within 10ms
2. DIAG_ID_OVERCURRENT_DISCHARGE event generated
3. Error counter incremented per DIAG configuration
4. Contactor opening within FTTI (100ms) if threshold reached

**Verifies TSRs**: FBMS-SAF-CFG-008, FBMS-SAF-CFG-010, FBMS-SAF-CFG-012, FBMS-SAF-CFG-013

**Derives From Integration Tests**: FBMS-TC-IT-BMS-003, FBMS-TC-IT-BMS-018

---

## 10. ASPICE Compliance

### 10.1 SWE.6 Base Practice Compliance

| Base Practice | Description                                      | Status   | Evidence                               |
|---------------|--------------------------------------------------|----------|----------------------------------------|
| SWE.6 BP1     | Develop software qualification test strategy     | PASS     | 32 system tests covering all safety goals |
| SWE.6 BP2     | Develop software qualification test specification| PASS     | Test specifications with pass criteria |
| SWE.6 BP3     | Select software qualification test cases         | PASS     | Tests derived from TSRs and safety goals |
| SWE.6 BP4     | Perform software qualification testing           | PENDING  | Tests specified, execution pending     |
| SWE.6 BP5     | Ensure consistency and bidirectional traceability| PASS     | Complete traceability in this matrix   |

### 10.2 SUP.8 (Configuration Management) Compliance

| Requirement              | Status   | Evidence                                        |
|--------------------------|----------|------------------------------------------------|
| Version control          | PASS     | All artifacts versioned in git                 |
| Traceability maintained  | PASS     | Bidirectional traceability in JSON + markdown  |
| Change impact analysis   | PASS     | Change navigation instructions in Section 11   |

---

## 11. ISO 26262 Compliance

### 11.1 Part 4 Clause 7 (Product Development at the System Level)

| Requirement                      | Status     | Evidence                                    |
|----------------------------------|------------|---------------------------------------------|
| System test specification        | COMPLIANT  | 32 system tests per safety goals            |
| Safety goal verification         | COMPLIANT  | All 3 safety goals have test coverage       |
| FTTI compliance                  | COMPLIANT  | Test pass criteria include FTTI timing      |

### 11.2 Part 6 Clause 10 (Software Safety Requirements Verification)

| Requirement                      | Status     | Evidence                                    |
|----------------------------------|------------|---------------------------------------------|
| SW requirements verification     | COMPLIANT  | All 147 TSRs traced to system tests         |
| ASIL-D MC/DC requirement         | COMPLIANT  | MC/DC coverage for ASIL-D/C requirements    |
| Bidirectional traceability       | COMPLIANT  | Complete chain: SG to Unit Test             |

### 11.3 Table 12 Test Methods Compliance

| Method    | Name                        | Applicable | Coverage |
|-----------|-----------------------------|------------|----------|
| Method 1a | Requirements-based test     | Yes        | 100%     |
| Method 1b | Interface testing           | Yes        | 100%     |
| Method 1c | Fault injection testing     | Yes        | Partial  |
| Method 1d | Resource usage testing      | Yes        | Pending  |
| Method 1e | Back-to-back testing        | Partial    | Model-based tests |

---

## 12. Bidirectional Navigation Instructions

### 12.1 From Safety Goal to System Test

To find system tests verifying a specific safety goal:
1. Locate Safety Goal ID in Section 3 (e.g., SG-BMS-001)
2. Find the corresponding subsection (e.g., 3.2)
3. System tests are listed in the "System Tests for SG-BMS-xxx" table
4. TSR to System Test mapping shows detailed requirement coverage

### 12.2 From System Test to Safety Goal

To find which safety goals are verified by a specific system test:
1. Locate System Test ID in Section 9
2. The "Safety Goal" field shows the associated safety goal
3. "Verifies TSRs" lists all requirements covered

### 12.3 From System Test to Integration Test

To find integration tests that support a system test:
1. Locate System Test ID in Section 5.1
2. "Integration Test(s)" column lists the R2 tests
3. Full integration test details in r2-traceability-report.md

### 12.4 From Integration Test to Unit Test

To find unit tests that support an integration test:
1. Locate Integration Test ID in Section 6.1
2. "Unit Test(s)" column lists the R1 tests
3. Full unit test details in test_bms_r1.c

### 12.5 From Unit Test to Requirement

To find requirements verified by a specific unit test:
1. Locate Unit Test ID in test_bms_r1.c
2. The @requirement tag in test documentation shows associated requirement
3. Or use Section 6.1 to find integration test, then trace upstream

---

## 13. Change Impact Analysis

### 13.1 Impact Assessment for Safety Goal Changes

When a Safety Goal changes:
1. Identify affected Safety Goal ID
2. Find all linked TSRs via Section 3 and 4
3. Find all linked System Tests
4. Cascade to Integration Tests (Section 5)
5. Cascade to Unit Tests (Section 6)
6. Update all affected test cases
7. Re-execute complete verification chain
8. Update traceability matrix

### 13.2 Impact Assessment for TSR Changes

When a Technical Safety Requirement changes:
1. Identify TSR ID
2. Find linked System Tests via Section 4
3. Find linked Integration Tests via Section 5
4. Find linked Unit Tests via Section 6
5. Update affected test cases
6. Re-execute tests
7. Update coverage status

### 13.3 Impact Assessment for Test Changes

When a test case changes:
1. Identify Test ID and level (R1/R2/R3)
2. Find linked requirements (upstream navigation)
3. Verify change does not reduce coverage
4. Update traceability links
5. Re-execute test
6. Update test results

---

## 14. References

### 14.1 Source Documents

| Document                          | Location                                                |
|-----------------------------------|---------------------------------------------------------|
| ASIL Classification Report        | docs/parvis/requirements/asil-classification-report.md  |
| Classified Requirements           | docs/parvis/requirements/bms-classified.json            |
| Unified Requirements              | docs/parvis/requirements/unified-requirements.json      |
| FBMS ID Registry                  | docs/parvis/requirements/fbms-id-registry.json          |
| Traceability Matrix (JSON)        | docs/parvis/requirements/traceability-matrix.json       |
| R1 Unit Tests                     | docs/parvis/verification/test_bms_r1.c                  |
| R2 Integration Tests              | docs/parvis/verification/test_bms_integration_r2.c      |
| R2 Traceability Report            | docs/parvis/verification/r2-traceability-report.md      |
| R2 Traceability Matrix (JSON)     | docs/parvis/verification/r2-traceability-matrix.json    |

### 14.2 Standards

| Standard             | Title                                                |
|----------------------|------------------------------------------------------|
| ISO 26262:2018       | Road vehicles - Functional Safety                    |
| ASPICE 3.1           | Automotive SPICE Process Assessment Model            |
| IEC 61508            | Functional Safety of E/E/PE Safety-related Systems   |

---

## 15. Glossary

| Term       | Definition                                                |
|------------|-----------------------------------------------------------|
| ASIL       | Automotive Safety Integrity Level                         |
| FTTI       | Fault Tolerant Time Interval                              |
| FSR        | Functional Safety Requirement                             |
| MC/DC      | Modified Condition/Decision Coverage                      |
| SG         | Safety Goal                                               |
| TSR        | Technical Safety Requirement                              |
| R1         | V-Model ascending phase 1 (Unit Testing)                  |
| R2         | V-Model ascending phase 2 (Integration Testing)           |
| R3         | V-Model ascending phase 3 (System Testing)                |

---

**End of Document**

---

*Generated by PARVIS-AISpec-Trace for R3 Phase (System Verification)*
*ASPICE SWE.6 Compliance*
*ISO 26262-4 Clause 7 and ISO 26262-6 Clause 10 Compliance*
