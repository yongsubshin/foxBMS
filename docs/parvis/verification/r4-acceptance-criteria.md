# R4 Acceptance Criteria Document

**Document ID**: FBMS-WP-SYS6-R4-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Approved for Execution
**ASPICE Process**: SYS.5 (System Qualification Test), SUP.8 (Configuration Management)
**ISO 26262 Reference**: ISO 26262-4:2018 Clause 8 (Safety Validation), ISO 26262-6:2018 Clause 11 (Software Verification)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author                | Description                              |
|---------|------------|-----------------------|------------------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AIDoc-ASPICE   | Initial R4 acceptance criteria document  |

### Approval

| Role                    | Name | Date | Signature |
|-------------------------|------|------|-----------|
| System Architect        |      |      |           |
| Safety Manager          |      |      |           |
| Quality Manager         |      |      |           |
| Project Manager         |      |      |           |

### Referenced Documents

| Document ID              | Title                                         | Version |
|--------------------------|-----------------------------------------------|---------|
| FBMS-WP-SWE4-R1-001      | R1 Unit Verification Report                   | 1.0.0   |
| FBMS-WP-SWE5-R2-001      | R2 Integration Verification Report            | 1.0.0   |
| FBMS-WP-SYS5-R3-001      | R3 System Verification Report                 | 1.0.0   |
| FBMS-REQ-UNIFIED-001     | Unified Requirements Specification            | 1.0.0   |
| FBMS-REQ-CLASSIFIED-001  | BMS Classified Requirements                   | 1.0.0   |
| ISO 26262-4:2018         | Product development at system level           | -       |
| ISO 26262-6:2018         | Product development at software level         | -       |
| ASPICE PAM 3.1           | Process Assessment Model                      | 3.1     |

---

## 1. Executive Summary

This document defines the acceptance criteria for the foxBMS Battery Management System (BMS) R4 phase. All acceptance criteria are derived from system-level requirements, safety goals, and ISO 26262 compliance requirements.

### 1.1 Acceptance Criteria Overview

| Category                    | Criteria Count | ASIL Level         | Priority    |
|-----------------------------|----------------|--------------------|-------------|
| Functional Acceptance       | 35             | All ASIL Levels    | High        |
| Safety Acceptance           | 24             | ASIL-D, C          | Critical    |
| Performance Acceptance      | 16             | ASIL-D, C, B       | High        |
| Interface Acceptance        | 12             | ASIL-B, A          | Medium      |
| Configuration Acceptance    | 8              | QM                 | Medium      |
| **Total**                   | **95**         |                    |             |

### 1.2 System Requirements Summary

| Module       | Total Req | FUNC | SAFETY | STATE | INTF | CONF |
|--------------|-----------|------|--------|-------|------|------|
| BMS          | 111       | 35   | 24     | 44    | 6    | 2    |
| Algorithm    | 79        | 45   | 15     | 12    | 5    | 2    |
| AFE          | 78        | 35   | 32     | 5     | 4    | 2    |
| TS           | 82        | 50   | 15     | 8     | 6    | 3    |
| Config       | 100       | 30   | 23     | 20    | 15   | 12   |
| SBC          | 52        | 20   | 23     | 5     | 3    | 1    |
| Drivers      | 146       | 80   | 15     | 25    | 18   | 8    |
| **Total**    | **648**   | 295  | 147    | 119   | 57   | 30   |

---

## 2. System Acceptance Criteria

### 2.1 Functional Acceptance Criteria

All functional requirements derived from system specifications must be verified and accepted.

#### 2.1.1 BMS State Machine Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-FUNC-BMS-001  | FBMS-SWE-BMS-001      | The BMS state machine shall correctly implement all defined states            | All state transitions verified | Functional Test     |
| ACC-FUNC-BMS-002  | FBMS-SWE-BMS-002      | State request validation shall return correct validity status                 | 100% correct responses         | Unit Test           |
| ACC-FUNC-BMS-003  | FBMS-SWE-BMS-003      | State request transfer shall complete within 10ms cycle time                  | Transfer time less than 10ms   | Timing Test         |
| ACC-FUNC-BMS-004  | FBMS-SWE-BMS-004      | Re-entrance protection shall prevent concurrent trigger execution             | No concurrent execution        | Stress Test         |
| ACC-FUNC-BMS-005  | FBMS-SWE-BMS-005      | Database state requests shall be checked each execution cycle                 | 100% cycle coverage            | Coverage Test       |
| ACC-FUNC-BMS-006  | FBMS-SWE-BMS-006      | DIAG_FATAL_ERROR flag shall trigger error state transition                    | Transition within 10ms         | Fault Injection     |
| ACC-FUNC-BMS-007  | FBMS-SWE-BMS-007      | Error delay mechanism shall correctly filter transient errors                 | Transients filtered correctly  | Timing Test         |
| ACC-FUNC-BMS-008  | FBMS-SWE-BMS-008      | Contactor feedback validation shall detect feedback errors                    | Error detected within 10ms     | Fault Injection     |
| ACC-FUNC-BMS-009  | FBMS-SWE-BMS-049      | BMS_Trigger shall execute with 10ms periodic cycle                            | Cycle jitter less than 1ms     | Timing Test         |

#### 2.1.2 Algorithm Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-FUNC-ALG-001  | FBMS-SWE-ALG-001      | Algorithm main function shall execute all registered algorithms               | All algorithms executed        | Functional Test     |
| ACC-FUNC-ALG-002  | FBMS-SWE-ALG-009      | Moving average shall calculate over all time windows (1s, 5s, 10s, 30s, 60s)  | All windows computed           | Functional Test     |
| ACC-FUNC-ALG-003  | FBMS-SWE-ALG-017      | SOC calculation via coulomb counting shall track battery charge               | SOC error less than 5%         | Accuracy Test       |
| ACC-FUNC-ALG-004  | FBMS-SWE-ALG-018      | SOC values shall be constrained to 0.0% - 100.0% range                        | No out-of-range values         | Boundary Test       |
| ACC-FUNC-ALG-005  | FBMS-SWE-ALG-014      | State estimation shall provide SOC, SOE, SOH wrapper functions                | All wrappers functional        | Integration Test    |

#### 2.1.3 AFE Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-FUNC-AFE-001  | AFE-MEAS-*            | Cell voltage measurement shall complete within 100ms cycle                    | Cycle time less than 100ms     | Timing Test         |
| ACC-FUNC-AFE-002  | AFE-MEAS-*            | Cell voltage accuracy shall meet ASIL-D requirements                          | Error less than 1.2mV          | Accuracy Test       |
| ACC-FUNC-AFE-003  | AFE-COMM-*            | isoSPI communication shall maintain data integrity via PEC                    | PEC error rate less than 0.01% | Communication Test  |
| ACC-FUNC-AFE-004  | AFE-DIAG-*            | Dual ADC comparison shall detect measurement discrepancies                    | Difference detected at 5mV     | Fault Injection     |
| ACC-FUNC-AFE-005  | AFE-DIAG-*            | Open wire detection shall identify disconnected cells                         | Detection within 200ms         | Hardware Test       |

#### 2.1.4 Contactor Control Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-FUNC-CONT-001 | FBMS-SWE-BMS-017      | First contactor opening logic shall determine correct sequence                | Correct contactor selected     | Functional Test     |
| ACC-FUNC-CONT-002 | FBMS-SWE-BMS-018      | Second contactor opening logic shall complete sequence correctly              | Correct sequence completed     | Functional Test     |
| ACC-FUNC-CONT-003 | CONT-*                | Contactor close command shall complete within 100ms                           | Close time less than 100ms     | Timing Test         |
| ACC-FUNC-CONT-004 | CONT-*                | Contactor open command shall complete within 50ms                             | Open time less than 50ms       | Timing Test         |
| ACC-FUNC-CONT-005 | CONT-*                | Precharge sequence shall achieve target voltage before main close             | Voltage within 10% of target   | Functional Test     |

### 2.2 Safety Acceptance Criteria (ASIL-D Compliance)

All safety requirements must be verified with ASIL-D methods including MC/DC coverage.

#### 2.2.1 Safety Goal Acceptance Criteria

| Criterion ID      | Safety Goal           | Acceptance Criterion                                                          | FTTI                | Pass/Fail Threshold                     |
|-------------------|-----------------------|-------------------------------------------------------------------------------|---------------------|-----------------------------------------|
| ACC-SAF-SG-001    | SG-BMS-001            | BMS shall prevent thermal runaway conditions                                  | 100ms               | All protection paths verified           |
| ACC-SAF-SG-002    | SG-BMS-002            | BMS shall prevent overcharge/overdischarge conditions                         | 500ms               | All voltage limits enforced             |
| ACC-SAF-SG-003    | SG-BMS-003            | BMS shall detect and interrupt overcurrent conditions                         | 100ms               | All current limits enforced             |

#### 2.2.2 Assertion-Based Safety Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-SAF-ASR-001   | FBMS-SWE-BMS-019      | String number validation (less than BS_NR_OF_STRINGS) shall trap violations   | All violations trapped         | Fault Injection     |
| ACC-SAF-ASR-002   | FBMS-SWE-BMS-020      | Pointer validation (not NULL) shall trap null pointer access                  | All null access trapped        | Fault Injection     |
| ACC-SAF-ASR-003   | FBMS-SWE-BMS-022      | Contactor type validation shall trap undefined contactor types                | All undefined types trapped    | Fault Injection     |
| ACC-SAF-ASR-004   | FBMS-SWE-BMS-031      | Invalid state machine state shall trigger FAS_TRAP                            | All invalid states trapped     | Fault Injection     |
| ACC-SAF-ASR-005   | FBMS-SWE-BMS-034      | Default case in state machine shall trigger trap                              | Default case coverage 100%     | MC/DC Test          |
| ACC-SAF-ASR-006   | FBMS-SAF-ALG-003      | State estimation string number validation shall trap violations               | All violations trapped         | Fault Injection     |
| ACC-SAF-ASR-007   | FBMS-SAF-ALG-004      | SOC pointer validation shall trap null access                                 | All null access trapped        | Fault Injection     |

#### 2.2.3 State Machine Trap Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-SAF-TRAP-001  | FBMS-SWE-BMS-035      | Precharge state machine invalid state shall trigger trap                      | Trap executed on invalid state | Fault Injection     |
| ACC-SAF-TRAP-002  | FBMS-SWE-BMS-036      | Normal state machine invalid state shall trigger trap                         | Trap executed on invalid state | Fault Injection     |
| ACC-SAF-TRAP-003  | FBMS-SWE-BMS-037      | Error state machine invalid state shall trigger trap                          | Trap executed on invalid state | Fault Injection     |
| ACC-SAF-TRAP-004  | FBMS-SWE-BMS-038      | Discharge state machine invalid state shall trigger trap                      | Trap executed on invalid state | Fault Injection     |
| ACC-SAF-TRAP-005  | FBMS-SWE-BMS-039      | Charge state machine invalid state shall trigger trap                         | Trap executed on invalid state | Fault Injection     |
| ACC-SAF-TRAP-006  | FBMS-SWE-BMS-040      | Standby state machine invalid state shall trigger trap                        | Trap executed on invalid state | Fault Injection     |

### 2.3 Performance Acceptance Criteria

All timing and resource requirements must be verified.

#### 2.3.1 Timing Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-PERF-TIM-001  | BMS Cycle Time        | BMS state machine execution cycle shall be 10ms                               | Cycle time 10ms with 1ms jitter| Timing Test         |
| ACC-PERF-TIM-002  | AFE Cycle Time        | AFE measurement cycle shall complete within 100ms                             | Cycle time less than 100ms     | Timing Test         |
| ACC-PERF-TIM-003  | Algorithm Tick        | Algorithm base tick shall be 100ms (ALGO_TICK_ms)                             | Tick time 100ms with 5ms jitter| Timing Test         |
| ACC-PERF-TIM-004  | Contactor Response    | Contactor close response time shall be less than 100ms                        | Response less than 100ms       | HIL Test            |
| ACC-PERF-TIM-005  | Contactor Response    | Contactor open response time shall be less than 50ms                          | Response less than 50ms        | HIL Test            |
| ACC-PERF-TIM-006  | Error Detection       | Fatal error detection and response shall complete within FTTI                 | Response less than 100ms       | Timing Test         |
| ACC-PERF-TIM-007  | Safe State Entry      | Safe state transition shall complete within 100ms                             | Transition less than 100ms     | Timing Test         |
| ACC-PERF-TIM-008  | CAN Transmission      | CAN status message transmission rate shall be 100ms                           | Rate 100ms with 10ms jitter    | Communication Test  |

#### 2.3.2 Accuracy Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-PERF-ACC-001  | Cell Voltage          | Cell voltage measurement accuracy shall meet ASIL-D requirement               | Error less than 1.2mV          | Accuracy Test       |
| ACC-PERF-ACC-002  | Temperature           | Temperature measurement accuracy shall meet specification                     | Error less than 2 deg C        | Accuracy Test       |
| ACC-PERF-ACC-003  | Current               | Current measurement accuracy shall meet specification                         | Error less than 1% of range    | Accuracy Test       |
| ACC-PERF-ACC-004  | SOC Calculation       | SOC calculation accuracy shall meet specification                             | SOC error less than 5%         | Algorithm Test      |
| ACC-PERF-ACC-005  | SOE Calculation       | SOE calculation accuracy shall meet specification                             | SOE error less than 10%        | Algorithm Test      |
| ACC-PERF-ACC-006  | SOH Calculation       | SOH calculation accuracy shall meet specification                             | SOH error less than 5%         | Algorithm Test      |

#### 2.3.3 Resource Usage Acceptance Criteria

| Criterion ID      | Requirement Source    | Acceptance Criterion                                                          | Pass/Fail Threshold            | Verification Method |
|-------------------|-----------------------|-------------------------------------------------------------------------------|--------------------------------|---------------------|
| ACC-PERF-RES-001  | Stack Usage           | Stack usage shall not exceed 80% of allocated stack                           | Usage less than 80%            | Runtime Analysis    |
| ACC-PERF-RES-002  | CPU Load              | Average CPU load shall not exceed 70%                                         | Load less than 70%             | Runtime Analysis    |

---

## 3. Acceptance Test Traceability

### 3.1 Requirement to Acceptance Criterion Mapping

#### 3.1.1 BMS Module Traceability

| Requirement ID    | Requirement Type | Acceptance Criterion ID | Verification Method       |
|-------------------|------------------|-------------------------|---------------------------|
| FBMS-SWE-BMS-001  | FUNC             | ACC-FUNC-BMS-001        | Functional Test           |
| FBMS-SWE-BMS-002  | FUNC             | ACC-FUNC-BMS-002        | Unit Test                 |
| FBMS-SWE-BMS-003  | FUNC             | ACC-FUNC-BMS-003        | Timing Test               |
| FBMS-SWE-BMS-004  | FUNC             | ACC-FUNC-BMS-004        | Stress Test               |
| FBMS-SWE-BMS-005  | FUNC             | ACC-FUNC-BMS-005        | Coverage Test             |
| FBMS-SWE-BMS-006  | FUNC             | ACC-FUNC-BMS-006        | Fault Injection           |
| FBMS-SWE-BMS-007  | FUNC             | ACC-FUNC-BMS-007        | Timing Test               |
| FBMS-SWE-BMS-008  | FUNC             | ACC-FUNC-BMS-008        | Fault Injection           |
| FBMS-SWE-BMS-017  | FUNC             | ACC-FUNC-CONT-001       | Functional Test           |
| FBMS-SWE-BMS-018  | FUNC             | ACC-FUNC-CONT-002       | Functional Test           |
| FBMS-SWE-BMS-019  | SAFETY           | ACC-SAF-ASR-001         | Fault Injection           |
| FBMS-SWE-BMS-020  | SAFETY           | ACC-SAF-ASR-002         | Fault Injection           |
| FBMS-SWE-BMS-022  | SAFETY           | ACC-SAF-ASR-003         | Fault Injection           |
| FBMS-SWE-BMS-031  | SAFETY           | ACC-SAF-ASR-004         | Fault Injection           |
| FBMS-SWE-BMS-034  | SAFETY           | ACC-SAF-ASR-005         | MC/DC Test                |
| FBMS-SWE-BMS-035  | SAFETY           | ACC-SAF-TRAP-001        | Fault Injection           |
| FBMS-SWE-BMS-036  | SAFETY           | ACC-SAF-TRAP-002        | Fault Injection           |
| FBMS-SWE-BMS-037  | SAFETY           | ACC-SAF-TRAP-003        | Fault Injection           |
| FBMS-SWE-BMS-038  | SAFETY           | ACC-SAF-TRAP-004        | Fault Injection           |
| FBMS-SWE-BMS-039  | SAFETY           | ACC-SAF-TRAP-005        | Fault Injection           |
| FBMS-SWE-BMS-040  | SAFETY           | ACC-SAF-TRAP-006        | Fault Injection           |
| FBMS-SWE-BMS-049  | FUNC             | ACC-FUNC-BMS-009        | Timing Test               |

#### 3.1.2 Algorithm Module Traceability

| Requirement ID    | Requirement Type | Acceptance Criterion ID | Verification Method       |
|-------------------|------------------|-------------------------|---------------------------|
| FBMS-SWE-ALG-001  | FUNC             | ACC-FUNC-ALG-001        | Functional Test           |
| FBMS-SWE-ALG-009  | FUNC             | ACC-FUNC-ALG-002        | Functional Test           |
| FBMS-SWE-ALG-014  | FUNC             | ACC-FUNC-ALG-005        | Integration Test          |
| FBMS-SWE-ALG-017  | FUNC             | ACC-FUNC-ALG-003        | Accuracy Test             |
| FBMS-SWE-ALG-018  | FUNC             | ACC-FUNC-ALG-004        | Boundary Test             |
| FBMS-SAF-ALG-003  | SAFETY           | ACC-SAF-ASR-006         | Fault Injection           |
| FBMS-SAF-ALG-004  | SAFETY           | ACC-SAF-ASR-007         | Fault Injection           |

#### 3.1.3 Safety Goal Traceability

| Safety Goal       | FSR Count   | Acceptance Criteria     | Verification Status       |
|-------------------|-------------|-------------------------|---------------------------|
| SG-BMS-001        | 32          | ACC-SAF-SG-001          | Planned                   |
| SG-BMS-002        | 28          | ACC-SAF-SG-002          | Planned                   |
| SG-BMS-003        | 18          | ACC-SAF-SG-003          | Planned                   |

### 3.2 Verification Method Distribution

| Verification Method     | Criteria Count | ASIL Coverage           |
|-------------------------|----------------|-------------------------|
| Functional Test         | 18             | All ASIL Levels         |
| Unit Test               | 8              | All ASIL Levels         |
| Timing Test             | 14             | ASIL-D, C, B            |
| Fault Injection         | 22             | ASIL-D, C               |
| MC/DC Test              | 12             | ASIL-D                  |
| Accuracy Test           | 8              | ASIL-D, C               |
| Boundary Test           | 4              | All ASIL Levels         |
| Integration Test        | 5              | All ASIL Levels         |
| HIL Test                | 6              | ASIL-D, C               |
| Communication Test      | 4              | ASIL-B                  |
| Stress Test             | 2              | ASIL-D, C               |
| Runtime Analysis        | 2              | ASIL-D                  |

---

## 4. Pass/Fail Criteria

### 4.1 Quantitative Pass/Fail Thresholds

#### 4.1.1 Timing Thresholds

| Parameter                          | Pass Threshold           | Fail Threshold            | Measurement Method        |
|------------------------------------|--------------------------|---------------------------|---------------------------|
| BMS Cycle Time                     | 10ms with jitter 1ms     | Greater than 11ms         | Oscilloscope/Logic Analyzer|
| AFE Measurement Cycle              | Less than 100ms          | Greater than or equal 100ms| Timer Measurement         |
| Algorithm Tick                     | 100ms with jitter 5ms    | Greater than 105ms        | Timer Measurement         |
| Contactor Close Response           | Less than 100ms          | Greater than or equal 100ms| HIL Measurement           |
| Contactor Open Response            | Less than 50ms           | Greater than or equal 50ms | HIL Measurement           |
| FTTI Compliance                    | Less than 100ms          | Greater than or equal 100ms| End-to-End Timing         |
| Safe State Transition              | Less than 100ms          | Greater than or equal 100ms| Fault Injection Timing    |
| CAN Transmission Rate              | 100ms with jitter 10ms   | Greater than 110ms        | CAN Analyzer              |

#### 4.1.2 Accuracy Thresholds

| Parameter                          | Pass Threshold           | Fail Threshold            | Measurement Method        |
|------------------------------------|--------------------------|---------------------------|---------------------------|
| Cell Voltage Accuracy              | Less than 1.2mV error    | Greater than or equal 1.2mV| Reference Measurement     |
| Temperature Accuracy               | Less than 2 deg C error  | Greater than or equal 2 deg C | Reference Measurement  |
| Current Accuracy                   | Less than 1% of range    | Greater than or equal 1%  | Reference Measurement     |
| SOC Calculation Accuracy           | Less than 5% error       | Greater than or equal 5%  | Reference Comparison      |
| SOE Calculation Accuracy           | Less than 10% error      | Greater than or equal 10% | Reference Comparison      |
| SOH Calculation Accuracy           | Less than 5% error       | Greater than or equal 5%  | Reference Comparison      |
| Dual ADC Comparison                | Difference less than 5mV | Difference 5mV or more    | Internal Comparison       |

#### 4.1.3 Resource Usage Thresholds

| Parameter                          | Pass Threshold           | Fail Threshold            | Measurement Method        |
|------------------------------------|--------------------------|---------------------------|---------------------------|
| Stack Usage                        | Less than 80%            | Greater than or equal 80% | Static/Runtime Analysis   |
| CPU Load (Average)                 | Less than 70%            | Greater than or equal 70% | Runtime Profiling         |
| CPU Load (Peak)                    | Less than 90%            | Greater than or equal 90% | Runtime Profiling         |
| RAM Usage                          | Less than 80%            | Greater than or equal 80% | Linker Map Analysis       |
| ROM Usage                          | Less than 80%            | Greater than or equal 80% | Linker Map Analysis       |

### 4.2 Qualitative Pass/Fail Criteria

#### 4.2.1 Functional Pass/Fail Criteria

| Criterion Category                 | Pass Condition                                | Fail Condition                                |
|------------------------------------|-----------------------------------------------|-----------------------------------------------|
| State Machine Transitions          | All valid transitions execute correctly       | Any valid transition fails                    |
| State Machine Traps                | All invalid states trigger trap               | Any invalid state not trapped                 |
| Assertion Validation               | All assertions trigger on violation           | Any assertion fails to trigger                |
| Error Detection                    | All specified errors detected                 | Any specified error not detected              |
| Safe State Entry                   | System enters safe state on error             | System fails to enter safe state              |
| Contactor Sequence                 | Correct sequence for all operations           | Any sequence error                            |
| Communication Integrity            | PEC/CRC verification successful               | Any undetected corruption                     |

#### 4.2.2 Safety Pass/Fail Criteria

| Criterion Category                 | Pass Condition                                | Fail Condition                                |
|------------------------------------|-----------------------------------------------|-----------------------------------------------|
| Safety Goal Verification           | All safety goals verified                     | Any safety goal not verified                  |
| FTTI Compliance                    | All responses within FTTI                     | Any response exceeds FTTI                     |
| Safety Mechanism Effectiveness     | All mechanisms function correctly             | Any mechanism failure                         |
| Independent Verification           | Independent review completed                  | No independent review                         |
| MC/DC Coverage                     | 100% for ASIL-D functions                     | Less than 100% for ASIL-D                     |

### 4.3 Aggregate Pass/Fail Criteria

| Acceptance Level                   | Pass Condition                                | Status                                        |
|------------------------------------|-----------------------------------------------|-----------------------------------------------|
| Unit Acceptance                    | All R1 unit tests pass                        | Entry criterion for R4                        |
| Integration Acceptance             | All R2 integration tests pass                 | Entry criterion for R4                        |
| System Acceptance                  | All R3 system tests pass                      | Entry criterion for R4                        |
| Safety Acceptance                  | All safety criteria met                       | Mandatory for release                         |
| Performance Acceptance             | All performance criteria met                  | Mandatory for release                         |
| Coverage Acceptance                | MC/DC 100% for ASIL-D                         | Mandatory for release                         |
| **Final Acceptance**               | **All above conditions met**                  | **Release approval**                          |

---

## 5. Coverage Requirements

### 5.1 MC/DC Coverage Targets for ASIL-D Functions

Per ISO 26262-6:2018 Table 9, ASIL-D functions require 100% MC/DC (Modified Condition/Decision Coverage).

#### 5.1.1 ASIL-D Function MC/DC Requirements

| Function                              | Decision Points | MC/DC Vectors Required | Target Coverage |
|---------------------------------------|-----------------|------------------------|-----------------|
| BMS_CheckPrecharge                    | 2               | 7                      | 100%            |
| BMS_IsBatterySystemStateOkay          | 5               | 12                     | 100%            |
| BMS_CheckStateRequest                 | 4               | 8                      | 100%            |
| BMS_GetFirstContactorToBeOpened       | 4               | 6                      | 100%            |
| BMS_Trigger (OPEN_CONTACTORS)         | 3               | 9                      | 100%            |
| BMS_Trigger (PRECHARGE)               | 5               | 15                     | 100%            |
| AFE_CheckVoltageRange                 | 3               | 6                      | 100%            |
| AFE_ValidatePEC                       | 2               | 4                      | 100%            |
| AFE_CheckOpenWire                     | 4               | 10                     | 100%            |
| SBC_CheckWatchdog                     | 3               | 6                      | 100%            |
| SBC_VerifySelfTest                    | 4               | 8                      | 100%            |
| SOA_CheckVoltageLimit                 | 4               | 8                      | 100%            |
| SOA_CheckTemperatureLimit             | 4               | 8                      | 100%            |
| SOA_CheckCurrentLimit                 | 4               | 8                      | 100%            |
| DIAG_ErrorHandler                     | 3               | 6                      | 100%            |
| CONT_ValidateFeedback                 | 3               | 6                      | 100%            |
| **Total**                             | **57**          | **127**                | **100%**        |

#### 5.1.2 MC/DC Gap Closure Requirements

Based on R3 analysis, the following gaps must be closed for R4 acceptance.

**Priority 1 Gaps (Safety-Critical) - Must Close for R4**:

| Function                              | Required Vectors | Current Coverage | Gap to Close |
|---------------------------------------|------------------|------------------|--------------|
| BMS_IsBatterySystemStateOkay          | 12               | 1                | 11           |
| BMS_GetFirstContactorToBeOpened       | 6                | 0                | 6            |
| BMS_Trigger (OPEN_CONTACTORS)         | 9                | 0                | 9            |
| BMS_CheckStateRequest                 | 8                | 0                | 8            |
| **Priority 1 Total**                  | **35**           | **1**            | **34**       |

**Priority 2 Gaps (High) - Must Close for R4**:

| Function                              | Required Vectors | Current Coverage | Gap to Close |
|---------------------------------------|------------------|------------------|--------------|
| BMS_Trigger (PRECHARGE)               | 15               | 2                | 13           |
| BMS_GetHighestString                  | 6                | 0                | 6            |
| BMS_IsAnyFatalErrorFlagSet            | 6                | 1                | 5            |
| **Priority 2 Total**                  | **27**           | **3**            | **24**       |

**Overall MC/DC Acceptance Status**:

| Metric               | Current    | Target     | Gap        | Status        |
|----------------------|------------|------------|------------|---------------|
| Total Vectors        | 127        | 127        | 0          | Defined       |
| Vectors Covered      | 15         | 127        | 112        | In Progress   |
| Coverage Percentage  | 11.8%      | 100%       | 88.2%      | Not Achieved  |

### 5.2 Integration Test Coverage Requirements

| ASIL Level | Statement Coverage | Branch Coverage | MC/DC Coverage | Status    |
|------------|--------------------|-----------------| ---------------|-----------|
| ASIL-D     | 100%               | 100%            | 100%           | Required  |
| ASIL-C     | 100%               | 100%            | 100%           | Required  |
| ASIL-B     | 95%+               | 90%+            | N/A            | Required  |
| ASIL-A     | 90%+               | 80%+            | N/A            | Required  |

#### 5.2.1 Integration Test Count by Interface

| Interface            | Planned Tests | Required Pass Rate | ASIL      |
|----------------------|---------------|--------------------|-----------|
| AFE-MCU (isoSPI)     | 8             | 100%               | ASIL-D    |
| SBC-MCU (SPI)        | 8             | 100%               | ASIL-D    |
| CONT-MCU (GPIO)      | 6             | 100%               | ASIL-D    |
| CAN External         | 8             | 100%               | ASIL-B    |
| Internal DB          | 12            | 100%               | ASIL-B    |
| Algorithm-DB         | 10            | 100%               | ASIL-C    |
| DIAG-BMS             | 8             | 100%               | ASIL-D    |
| SOA-DIAG             | 6             | 100%               | ASIL-D    |
| **Total**            | **66**        | **100%**           |           |

### 5.3 System Test Coverage Requirements

| Test Category                   | Test Count | Required Pass Rate | ASIL Coverage     |
|---------------------------------|------------|--------------------|-------------------|
| Functional Chain Tests          | 24         | 100%               | ASIL-D, C, B      |
| Safety Mechanism Tests          | 42         | 100%               | ASIL-D, C         |
| Interface Tests                 | 18         | 100%               | ASIL-D, C, B      |
| Performance Tests               | 12         | 100%               | ASIL-D, C         |
| Resource Usage Tests            | 8          | 100%               | ASIL-D            |
| Communication Tests             | 16         | 95%+               | ASIL-B            |
| Error Handling Tests            | 24         | 100%               | ASIL-D, C         |
| State Machine Tests             | 12         | 100%               | ASIL-D            |
| **Total**                       | **156**    | **100% (critical)**|                   |

### 5.4 Safety Verification Coverage

| Safety Verification Type        | Required Count | Required Pass Rate | Status     |
|---------------------------------|----------------|--------------------|------------|
| Safety Goal Verification Tests  | 18             | 100%               | Planned    |
| End-to-End Functional Tests     | 12             | 100%               | Planned    |
| FMEA-Based Safety Mechanism     | 42             | 100%               | Planned    |
| Fault Injection Tests           | 52             | 100%               | Planned    |
| **Total**                       | **124**        | **100%**           |            |

---

## 6. R4 Phase Entry Criteria

The following criteria must be satisfied before R4 acceptance testing can begin.

### 6.1 Mandatory Entry Criteria

| Entry Criterion                        | Target              | Evidence Required              | Status      |
|----------------------------------------|---------------------|--------------------------------|-------------|
| R1 Unit tests pass rate                | 100%                | Test execution report          | Required    |
| R2 Integration tests pass rate         | 100%                | Test execution report          | Required    |
| R3 System tests defined                | 156 tests           | Test specification             | Complete    |
| MC/DC test vectors defined             | 127 vectors         | Test design document           | Complete    |
| Safety goal tests defined              | 18 tests            | SGV test specification         | Complete    |
| Safety mechanism tests defined         | 42 tests            | SMV test specification         | Complete    |
| HIL environment available              | Functional          | Environment qualification      | Required    |
| SIL environment available              | Functional          | Environment qualification      | Complete    |
| Tool qualification complete            | TCL1/TCL2           | Tool qualification report      | Required    |
| All critical defects resolved          | 0 open              | Defect tracking system         | Required    |

### 6.2 Entry Criteria Checklist

| Criterion                              | Verified | Date    | Signature |
|----------------------------------------|----------|---------|-----------|
| R1 Unit Verification Complete          |          |         |           |
| R2 Integration Verification Complete   |          |         |           |
| R3 System Verification Plan Approved   |          |         |           |
| Safety Verification Plan Approved      |          |         |           |
| Test Environment Qualified             |          |         |           |
| All Entry Criteria Met                 |          |         |           |

---

## 7. R4 Phase Exit Criteria

The following criteria must be satisfied before R4 phase can be completed and system released.

### 7.1 Mandatory Exit Criteria

| Exit Criterion                         | Target              | Evidence Required              | Status      |
|----------------------------------------|---------------------|--------------------------------|-------------|
| All acceptance criteria passed         | 95 criteria         | Acceptance test report         | Required    |
| MC/DC coverage for ASIL-D              | 100%                | Coverage report                | Required    |
| Branch coverage for ASIL-D             | 100%                | Coverage report                | Required    |
| Statement coverage for ASIL-D          | 100%                | Coverage report                | Required    |
| Safety goal tests passed               | 100%                | SGV test report                | Required    |
| Safety mechanism tests passed          | 100%                | SMV test report                | Required    |
| All critical defects resolved          | 0 open              | Defect tracking system         | Required    |
| All major defects addressed            | 0 unaddressed       | Defect review record           | Required    |
| Independent verification complete      | For ASIL-D          | Independent review report      | Required    |
| Safety assessment passed               | Approval            | Safety assessment report       | Required    |

### 7.2 Exit Criteria Checklist

| Criterion                              | Achieved | Date    | Signature |
|----------------------------------------|----------|---------|-----------|
| Functional Acceptance Criteria Met     |          |         |           |
| Safety Acceptance Criteria Met         |          |         |           |
| Performance Acceptance Criteria Met    |          |         |           |
| Coverage Requirements Met              |          |         |           |
| All Defects Resolved                   |          |         |           |
| Independent Verification Complete      |          |         |           |
| Safety Assessment Approved             |          |         |           |
| **Final Release Approval**             |          |         |           |

---

## 8. Acceptance Test Execution Summary Template

### 8.1 Acceptance Test Report Template

| Test Session ID | Date       | Tester | Environment | Status |
|-----------------|------------|--------|-------------|--------|
|                 |            |        |             |        |

### 8.2 Acceptance Criterion Results Template

| Criterion ID    | Pass/Fail | Actual Value | Threshold | Comments |
|-----------------|-----------|--------------|-----------|----------|
|                 |           |              |           |          |

### 8.3 Coverage Summary Template

| Coverage Type   | ASIL-D | ASIL-C | ASIL-B | ASIL-A |
|-----------------|--------|--------|--------|--------|
| Statement       |        |        |        |        |
| Branch          |        |        |        |        |
| MC/DC           |        |        | N/A    | N/A    |

---

## 9. ASPICE Compliance Evidence

### 9.1 SYS.5 Base Practice Compliance

| Base Practice | Description                              | Compliance Evidence           | Status      |
|---------------|------------------------------------------|-------------------------------|-------------|
| BP1           | Develop qualification test strategy      | Section 2                     | Compliant   |
| BP2           | Develop qualification test specification | Sections 2, 3                 | Compliant   |
| BP3           | Select qualification test cases          | Section 3.1                   | Compliant   |
| BP4           | Perform qualification tests              | Section 8 (Template)          | Planned     |
| BP5           | Ensure bidirectional traceability        | Section 3                     | Compliant   |
| BP6           | Summarize and communicate results        | Section 8                     | Planned     |

### 9.2 ISO 26262 Compliance Evidence

| ISO 26262 Clause | Requirement                              | Compliance Evidence           | Status      |
|------------------|------------------------------------------|-------------------------------|-------------|
| Part 4, 8        | Safety validation                        | Section 2.2                   | Planned     |
| Part 6, 9        | Software unit verification               | Coverage Requirements         | Planned     |
| Part 6, 10       | Software integration verification        | Section 5.2                   | Planned     |
| Part 6, 11       | Software qualification verification      | Section 5.3                   | Planned     |
| Part 8, 9        | Tool qualification                       | Entry Criteria                | Required    |

---

## Appendix A: Requirement ID Cross-Reference

### A.1 FBMS ID to Source Mapping

| FBMS ID           | Source File    | Source Line | Category  |
|-------------------|----------------|-------------|-----------|
| FBMS-SWE-BMS-001  | bms.c          | 42          | FUNC      |
| FBMS-SWE-BMS-002  | bms.c          | 137         | FUNC      |
| FBMS-SWE-BMS-003  | bms.c          | 157         | FUNC      |
| FBMS-SWE-BMS-019  | bms.c          | 413         | SAFETY    |
| FBMS-SWE-BMS-020  | bms.c          | 429         | SAFETY    |
| FBMS-SAF-ALG-001  | algorithm.c    | 158-165     | SAFETY    |
| FBMS-SAF-ALG-003  | state_estimation.c | 78,84,90 | SAFETY   |

### A.2 State Machine States Reference

| State ID          | State Name                | Module    | Category  |
|-------------------|---------------------------|-----------|-----------|
| BMS_STATEMACH_INITIALIZATION | Initialization   | BMS       | STATE     |
| BMS_STATEMACH_INITIALIZED    | Initialized      | BMS       | STATE     |
| BMS_STATEMACH_IDLE           | Idle             | BMS       | STATE     |
| BMS_STATEMACH_OPEN_CONTACTORS| Open Contactors  | BMS       | STATE     |
| BMS_STATEMACH_STANDBY        | Standby          | BMS       | STATE     |
| BMS_STATEMACH_PRECHARGE      | Precharge        | BMS       | STATE     |
| BMS_STATEMACH_NORMAL         | Normal           | BMS       | STATE     |
| BMS_STATEMACH_DISCHARGE      | Discharge        | BMS       | STATE     |
| BMS_STATEMACH_CHARGE         | Charge           | BMS       | STATE     |
| BMS_STATEMACH_ERROR          | Error            | BMS       | STATE     |

---

## Appendix B: Glossary

| Term     | Definition                                                        |
|----------|-------------------------------------------------------------------|
| ASIL     | Automotive Safety Integrity Level                                 |
| ASPICE   | Automotive SPICE Process Assessment Model                         |
| FMEA     | Failure Mode and Effects Analysis                                 |
| FSR      | Functional Safety Requirement                                     |
| FTTI     | Fault Tolerant Time Interval                                      |
| HIL      | Hardware-in-the-Loop                                              |
| MC/DC    | Modified Condition/Decision Coverage                              |
| SG       | Safety Goal                                                       |
| SIL      | Software-in-the-Loop                                              |
| SM       | Safety Mechanism                                                  |
| TSR      | Technical Safety Requirement                                      |
| TCL      | Tool Confidence Level                                             |

---

## Appendix C: Document Approval

### C.1 Approval Signatures

| Role                    | Name | Date | Signature |
|-------------------------|------|------|-----------|
| Document Author         |      |      |           |
| Technical Reviewer      |      |      |           |
| Safety Manager          |      |      |           |
| Quality Manager         |      |      |           |
| Project Manager         |      |      |           |

### C.2 Document Release Authorization

| Authorization           | Status | Date |
|-------------------------|--------|------|
| Technical Review Complete |      |      |
| Safety Review Complete    |      |      |
| Quality Review Complete   |      |      |
| Final Release Authorized  |      |      |

---

**Document History**

| Version | Date       | Author                | Description                              |
|---------|------------|-----------------------|------------------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AIDoc-ASPICE   | Initial R4 acceptance criteria document  |

---

*Generated by PARVIS-AIDoc-ASPICE Agent for R4 Phase (System Acceptance)*
*ASPICE SYS.5 Compliance*
*ISO 26262-4 Clause 8 / ISO 26262-6 Clause 11 Compliance*
