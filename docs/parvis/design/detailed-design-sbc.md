# SBC Driver Module Detailed Design Document

**Document ID**: FBMS-WP-SWE3-003
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D
**Component ID**: COMP-DRV-SBC

---

## Document Control

### Revision History

| Version | Date       | Author                   | Description                    |
|---------|------------|--------------------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI-Orchestrator   | Initial detailed design        |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Software Architect    |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This document provides the detailed design specification for the SBC (System Basis Chip) Driver Module (COMP-DRV-SBC) of the foxBMS Battery Management System. It specifies the NXP FS85xx driver implementation, watchdog management, safe state control, and safety mechanisms.

### 1.2 Scope

This document covers:
- SBC state machine design
- Watchdog trigger sequences
- Safe state transition logic (FS0B)
- LBIST/ABIST verification procedures
- Register configuration and verification
- Safety path checking

### 1.3 References

| Document ID          | Title                                       |
|---------------------|---------------------------------------------|
| FBMS-WP-SWE1-001    | Software Requirements Specification         |
| FBMS-WP-SWE2-001    | Software Architecture Design                |
| ISO 26262-6:2018    | Product development at the software level   |
| FS84_FS85 Datasheet | NXP FS84/FS85 SBC Rev. 3.0                  |

### 1.4 Source Files

| File                                     | Description                     |
|------------------------------------------|---------------------------------|
| src/app/driver/sbc/sbc.c                 | SBC state machine               |
| src/app/driver/sbc/sbc.h                 | SBC header file                 |
| src/app/driver/sbc/nxpfs85xx.c           | NXP FS85xx specific driver      |
| src/app/driver/sbc/nxpfs85xx.h           | NXP FS85xx header               |
| src/app/driver/sbc/fs8x_driver/          | Vendor driver files             |

---

## 2. System Basis Chip Overview

### 2.1 NXP FS85xx Features

The FS85xx is a safety System Basis Chip designed for ASIL-D applications:

| Feature                  | Description                              |
|--------------------------|------------------------------------------|
| Power Supply Supervision | Monitors VDD, VDDIO, VCCA voltages       |
| Watchdog                 | Window watchdog with configurable timing |
| Safe State Output        | FS0B pin for external safe state control |
| Reset Control            | RSTB output for MCU reset                |
| Fail-Safe Input          | FIN input for external safe state trigger|
| Diagnostic Functions     | LBIST, ABIST self-tests                  |

### 2.2 Safety Architecture

```
+-------------------+     +------------------+
|  MCU (TMS570)     |     |    FS85xx SBC    |
|                   |     |                  |
|  [SPI]------------|---->| Main Registers   |
|                   |     | Fail-Safe Regs   |
|  [Watchdog Trig]  |---->| WD Logic         |
|                   |     |                  |
|  [GPIO]<----------|----|   FS0B (Safe Out) |
|  [GPIO]<----------|----|   RSTB (Reset)    |
|  [GPIO]-----------|---->|   FIN (Fail In)  |
+-------------------+     +------------------+
          |                       |
          v                       v
    [Contactor Control]     [Hardware Interlock]
```

---

## 3. State Machine Design

### 3.1 State Enumeration

```c
typedef enum {
    SBC_STATEMACHINE_UNINITIALIZED,  /* Initial state */
    SBC_STATEMACHINE_INITIALIZATION, /* Init sequence */
    SBC_STATEMACHINE_RUNNING,        /* Normal operation */
    SBC_STATEMACHINE_ERROR,          /* Error state */
    SBC_STATEMACHINE_UNDEFINED,
} SBC_STATEMACHINE_e;
```

### 3.2 Substate Enumeration

```c
typedef enum {
    SBC_ENTRY,                                /* Entry point */
    SBC_INIT_RESET_FAULT_ERROR_COUNTER_PART1, /* Get WD refresh count */
    SBC_INIT_RESET_FAULT_ERROR_COUNTER_PART2, /* Check FEC is zero */
    SBC_INITIALIZE_SAFETY_PATH_CHECK,         /* Safety path verify */
    SBC_INITIALIZE_VOLTAGE_SUPERVISOR_PART3,  /* Voltage config */
    SBC_INITIALIZE_VOLTAGE_SUPERVISOR_PART4,  /* Voltage verify */
} SBC_STATEMACHINE_SUB_e;
```

### 3.3 State Transition Table

| From State        | To State       | Condition                             |
|-------------------|----------------|---------------------------------------|
| UNINITIALIZED     | INITIALIZATION | SBC_STATE_INIT_REQUEST received       |
| INITIALIZATION    | RUNNING        | All init substates complete           |
| INITIALIZATION    | ERROR          | Init fails after max retries          |
| RUNNING           | ERROR          | Watchdog timeout or critical fault    |
| ERROR             | (none)         | Requires power cycle                  |

### 3.4 State Transition Diagram

```
    +-------------------+
    | UNINITIALIZED     |
    +-------------------+
            |
            | INIT_REQUEST
            v
    +-------------------+
    | INITIALIZATION    |<----+
    +-------------------+     | Retry (max 3)
            |                 |
    +-------+-------+         |
    |               |         |
    | OK            | FAIL----+
    v               |
+-------------------+   +-------------------+
| RUNNING           |   | ERROR             |
+-------------------+   +-------------------+
    |                           ^
    | WD Timeout / Fault        |
    +---------------------------+
```

---

## 4. Data Structures

### 4.1 SBC State Variable (SBC_STATE_s)

```c
typedef struct {
    uint16_t timer;                    /* State machine timer (x10ms) */
    uint16_t watchdogTrigger;          /* Watchdog trigger countdown */
    SBC_STATE_REQUEST_e stateRequest;  /* Current state request */
    SBC_STATEMACHINE_e state;          /* Current main state */
    SBC_STATEMACHINE_SUB_e substate;   /* Current substate */
    SBC_STATEMACHINE_e lastState;      /* Previous main state */
    SBC_STATEMACHINE_SUB_e lastSubstate; /* Previous substate */
    uint32_t illegalRequestsCounter;   /* Illegal request counter */
    uint8_t retryCounter;              /* Init retry counter */
    uint8_t requestWatchdogTrigger;    /* Required WD triggers for init */
    uint8_t triggerEntry;              /* Re-entrance protection */
    SBC_PERIODIC_WATCHDOG_STATE_e watchdogState; /* WD trigger state */
    FS85_STATE_s *pFs85xxInstance;     /* Pointer to FS85xx instance */
    uint16_t watchdogPeriod_10ms;      /* WD trigger period (x10ms) */
    bool useIgnitionForPowerDown;      /* Use ignition for shutdown */
} SBC_STATE_s;
```

### 4.2 FS85xx Instance Structure (FS85_STATE_s)

```c
typedef struct {
    SPI_INTERFACE_CONFIG_s *pSpiInterface; /* SPI configuration */
    fs8x_drv_data_t configValues;      /* Communication config */
    FS85_FIN_CONFIGURATION_s fin;      /* FIN pin configuration */
    FS85_MAIN_REGISTERS_s mainRegister; /* Main register cache */
    FS85_FS_REGISTER_s fsRegister;     /* Fail-safe register cache */
    FS85_NVRAM_INFO_s nvram;           /* NVRAM persistence */
    FS85_OPERATION_MODE_e mode;        /* Operation mode */
} FS85_STATE_s;
```

### 4.3 Fail-Safe Register Structure (FS85_FS_REGISTER_s)

```c
typedef struct {
    uint16_t grl_flags;                  /* General flags */
    uint16_t iOvervoltageUndervoltageSafeReaction1; /* OV/UV config 1 */
    uint16_t iOvervoltageUndervoltageSafeReaction2; /* OV/UV config 2 */
    uint16_t iWatchdogConfiguration;     /* Watchdog config */
    uint16_t i_safe_inputs;              /* Safe input config */
    uint16_t iFailSafeSateMachine;       /* FSSM config */
    uint16_t i_svs;                      /* SVS config */
    uint16_t watchdogWindow;             /* WD window timing */
    uint16_t watchdogSeed;               /* WD seed value */
    uint16_t watchdogAnswer;             /* WD answer value */
    uint16_t overvoltageUndervoltageRegisterStatus; /* OV/UV status */
    uint16_t releaseFs0bPin;             /* FS0B release control */
    uint16_t safeIos;                    /* Safe I/O status */
    uint16_t diag_safety;                /* Safety diagnostics */
    uint16_t intb_mask;                  /* Interrupt mask */
    uint16_t states;                     /* State register */
} FS85_FS_REGISTER_s;
```

---

## 5. Timing Parameters

| Parameter                        | Value | Unit | Description                    |
|----------------------------------|-------|------|--------------------------------|
| SBC_STATEMACHINE_SHORTTIME       | 1     | x10ms| Short delay                    |
| SBC_STATEMACHINE_MEDIUMTIME      | 5     | x10ms| Medium delay                   |
| SBC_STATEMACHINE_LONGTIME        | 10    | x10ms| Long delay                     |
| SBC_WINDOW_WATCHDOG_PERIOD_MS    | 100   | ms   | Watchdog trigger period        |
| SBC_STATEMACHINE_TASK_CYCLE_CONTEXT_MS | 10 | ms | State machine task cycle      |

---

## 6. Function Specifications

### 6.1 SBC_Trigger()

**Purpose**: Main state machine trigger function, called every 10ms.

**Prototype**:
```c
extern void SBC_Trigger(SBC_STATE_s *pInstance);
```

**Parameters**:
| Name      | Type         | Direction | Description           |
|-----------|--------------|-----------|------------------------|
| pInstance | SBC_STATE_s* | In/Out    | SBC instance to control|

**Preconditions**:
- pInstance != NULL_PTR (verified by FAS_ASSERT)
- SPI interface configured

**Processing**:
1. Check re-entrance protection
2. Trigger watchdog if required (in RUNNING state)
3. Process state machine timer
4. Execute current state handler
5. Decrement triggerEntry

**Safety Assertions**:
- FAS_ASSERT(pInstance != NULL_PTR)

### 6.2 SBC_SetStateRequest()

**Purpose**: Request a state change in the SBC state machine.

**Prototype**:
```c
extern SBC_RETURN_TYPE_e SBC_SetStateRequest(
    SBC_STATE_s *pInstance,
    SBC_STATE_REQUEST_e stateRequest
);
```

**Return Values**:
| Value                  | Description                              |
|------------------------|------------------------------------------|
| SBC_OK                 | Request accepted                         |
| SBC_REQUEST_PENDING    | Another request is pending               |
| SBC_ILLEGAL_REQUEST    | Request not valid in current state       |
| SBC_ALREADY_INITIALIZED| Init requested when already initialized  |

**Critical Section**: Uses OS_EnterTaskCritical/OS_ExitTaskCritical

### 6.3 FS85_InitializeFsPhase()

**Purpose**: Configure SBC during INIT_FS phase.

**Prototype**:
```c
extern STD_RETURN_TYPE_e FS85_InitializeFsPhase(FS85_STATE_s *pInstance);
```

**Processing**:
1. Check if SBC is in INIT_FS phase
2. If not, transfer SBC back to INIT_FS
3. Perform basic checks (OTP CRC, LBIST)
4. Configure fail-safe registers
5. Close INIT_FS phase

**Safety Checks**:
- OTP CRC verification
- LBIST result verification
- Register configuration verification

### 6.4 FS85_TriggerWatchdog()

**Purpose**: Trigger the SBC watchdog.

**Prototype**:
```c
extern STD_RETURN_TYPE_e FS85_TriggerWatchdog(FS85_STATE_s *pInstance);
```

**Processing**:
1. Read current watchdog seed
2. Calculate watchdog answer
3. Write watchdog answer
4. Verify good watchdog refresh

**Watchdog Answer Calculation**:
```
Answer = NOT(Seed XOR 0x5AB2) for FS_WD_LFSR_B register
```

### 6.5 FS85_SafetyPathChecks()

**Purpose**: Perform safety path verification.

**Prototype**:
```c
extern STD_RETURN_TYPE_e FS85_SafetyPathChecks(FS85_STATE_s *pInstance);
```

**Processing**:
1. **FIN Path Check**: Verify FIN input detection
2. **FS0B Path Check**: Verify FS0B output control
3. **RSTB Path Check**: Verify RSTB output control

---

## 7. Watchdog Management

### 7.1 Window Watchdog Concept

The FS85xx uses a window watchdog with configurable timing:

```
     +------------------+------------------+
     |    CLOSED        |      OPEN        |
     |    WINDOW        |      WINDOW      |
     +------------------+------------------+
     0                 T1                 T2
          BAD REFRESH        GOOD REFRESH
```

### 7.2 Watchdog Timing Configuration

| Parameter      | Range            | Default  | Description              |
|----------------|------------------|----------|--------------------------|
| Window Open    | 3.2ms - 500ms    | 100ms    | Good refresh window      |
| Window Closed  | 0 - 500ms        | 0ms      | Bad refresh window       |
| Refresh Period | WD Window        | 100ms    | Software trigger period  |

### 7.3 Fault Error Counter (FEC)

- Incremented on: Bad watchdog refresh, safety violations
- Decremented on: Good watchdog refresh
- Maximum value: Configurable (default 6)
- FEC = Max triggers FS0B assertion

### 7.4 Watchdog Trigger Implementation

```c
static bool SBC_TriggerWatchdogIfRequired(SBC_STATE_s *pInstance) {
    FAS_ASSERT(pInstance != NULL_PTR);
    bool watchdogHasBeenTriggered = false;

    if (pInstance->watchdogTrigger > 0u) {
        pInstance->watchdogTrigger--;
        if (pInstance->watchdogTrigger == 0u) {
            if (STD_OK != FS85_TriggerWatchdog(pInstance->pFs85xxInstance)) {
                /* Watchdog trigger failed */
            } else {
                watchdogHasBeenTriggered = true;
                /* Reset watchdog counter */
                pInstance->watchdogTrigger = pInstance->watchdogPeriod_10ms;
            }
        }
    }
    return watchdogHasBeenTriggered;
}
```

---

## 8. Safe State Control

### 8.1 FS0B Pin Control

The FS0B (Fail-Safe 0B) output controls external safe state hardware:

| FS0B State | Condition                   | Effect                      |
|------------|-----------------------------|-----------------------------|
| HIGH       | Normal operation            | Contactors can be closed    |
| LOW        | Safety fault detected       | Contactors forced open      |

### 8.2 FS0B Release Sequence

To release FS0B after initialization:
1. Clear all fault flags
2. Reset fault error counter to 0
3. Perform safety path checks
4. Write FS0B release command

### 8.3 FS0B Assertion Conditions

| Condition                      | Response                    |
|--------------------------------|-----------------------------|
| Watchdog timeout               | Assert FS0B (LOW)           |
| Fault error counter overflow   | Assert FS0B (LOW)           |
| RSTB assertion                 | Assert FS0B (LOW)           |
| OV/UV detection (configured)   | Assert FS0B (LOW)           |
| External fault (FIN)           | Assert FS0B (LOW)           |

---

## 9. Initialization Sequence

### 9.1 Sequence Overview

```
POWER-ON
    |
    v
+-------------------+
| 1. SPI Init       |
+-------------------+
    |
    v
+-------------------+
| 2. Read OTP CRC   |
| 3. Verify LBIST   |
+-------------------+
    |
    v
+-------------------+
| 4. Configure WD   |
| 5. Configure FSSM |
+-------------------+
    |
    v
+-------------------+
| 6. Close INIT_FS  |
+-------------------+
    |
    v
+-------------------+
| 7. Reset FEC      |
| (WD refreshes)    |
+-------------------+
    |
    v
+-------------------+
| 8. Safety Checks  |
| 9. Release FS0B   |
+-------------------+
    |
    v
RUNNING
```

### 9.2 Fault Error Counter Reset

The fault error counter must be reset by good watchdog refreshes:

```c
/* Get number of required WD refreshes */
uint8_t requiredRefreshes = 0;
FS85_InitializeNumberOfRequiredWatchdogRefreshes(
    pInstance->pFs85xxInstance,
    &requiredRefreshes
);

/* Wait for required refreshes */
pInstance->timer = requiredRefreshes * pInstance->watchdogPeriod_10ms;
```

### 9.3 Safety Path Checks

#### 9.3.1 RSTB Path Check

1. Read RSTB pin state
2. Trigger RSTB assertion via SBC
3. Verify RSTB pin goes LOW
4. Release RSTB
5. Verify RSTB pin goes HIGH

#### 9.3.2 FS0B Path Check

1. Read FS0B pin state
2. Trigger FS0B assertion via SBC
3. Verify FS0B pin goes LOW
4. Release FS0B
5. Verify FS0B pin goes HIGH

---

## 10. Safety Mechanisms

### 10.1 LBIST (Logic Built-In Self-Test)

Performed during SBC power-up to verify logic functionality.

| Check            | Description                    | Pass Criteria         |
|------------------|--------------------------------|-----------------------|
| LBIST Result     | Logic self-test result         | LBIST_OK flag set     |
| ABIST Result     | Analog self-test result        | ABIST_OK flag set     |

### 10.2 OTP CRC Verification

One-Time Programmable memory CRC check:

```c
if (FS85_CheckOtpCrc(pInstance) != STD_OK) {
    /* OTP configuration corrupted */
    return STD_NOT_OK;
}
```

### 10.3 DATA/DATA_NOT Register Verification

Critical registers use DATA and DATA_NOT format for integrity:

```c
/* Read both DATA and DATA_NOT */
uint16_t data = ReadRegister(REG_DATA);
uint16_t dataInv = ReadRegister(REG_DATA_NOT);

/* Verify complement */
if ((data ^ dataInv) != 0xFFFFu) {
    /* Data corruption detected */
    return STD_NOT_OK;
}
```

### 10.4 FAS_ASSERT Usage

| Function                     | Assertion                    | Purpose               |
|------------------------------|------------------------------|-----------------------|
| SBC_Trigger                  | pInstance != NULL_PTR        | Null pointer check    |
| SBC_SetStateRequest          | pInstance != NULL_PTR        | Null pointer check    |
| SBC_CheckStateRequest        | pInstance != NULL_PTR        | Null pointer check    |
| SBC_CheckReEntrance          | pInstance != NULL_PTR        | Null pointer check    |
| SBC_TransferStateRequest     | pInstance != NULL_PTR        | Null pointer check    |
| SBC_TriggerWatchdogIfRequired| pInstance != NULL_PTR        | Null pointer check    |
| SBC_IsIgnitionSignalDetected | pInstance != NULL_PTR        | Null pointer check    |
| Default case in switch       | FAS_TRAP                     | Invalid state catch   |

---

## 11. Error Handling

### 11.1 Initialization Retry Logic

```c
if (STD_NOT_OK == FS85_InitializeFsPhase(pInstance->pFs85xxInstance)) {
    pInstance->retryCounter++;
    if (pInstance->retryCounter > 3u) {
        /* Maximum retries exceeded */
        pInstance->retryCounter = 0u;
        pInstance->state = SBC_STATEMACHINE_ERROR;
        pInstance->substate = SBC_ENTRY;
    }
}
```

### 11.2 Watchdog Failure Handling

Current implementation (TODO noted in code):
```c
if (STD_OK != FS85_TriggerWatchdog(pInstance->pFs85xxInstance)) {
    /* TODO: Define action on watchdog trigger failure */
}
```

**Recommended handling**:
- Increment failure counter
- Report to DIAG module
- Transition to ERROR state after threshold

---

## 12. Ignition Signal Handling

### 12.1 WAKE1 Signal Detection

```c
static bool SBC_IsIgnitionSignalDetected(SBC_STATE_s *pInstance) {
    FAS_ASSERT(pInstance != NULL_PTR);
    return FS85_CheckIgnitionSignal(pInstance->pFs85xxInstance);
}
```

### 12.2 Power-Down Sequence

When ignition signal is lost:
1. Detect falling edge on WAKE1
2. Initiate controlled shutdown
3. Open all contactors (via BMS)
4. Enter low-power mode

---

## 13. SPI Communication

### 13.1 Frame Format

```
+--------+--------+--------+--------+--------+
| ADDR   | DATA   | DATA   | CRC    |        |
| (8-bit)| (8-bit)| (8-bit)| (8-bit)|        |
+--------+--------+--------+--------+--------+
```

### 13.2 Register Access Functions

| Function           | Description                    |
|--------------------|--------------------------------|
| FS85_ReadRegister  | Read single register           |
| FS85_WriteRegister | Write single register          |
| FS85_WriteRegisterInit | Write during INIT_FS phase |
| FS85_ClearFlags    | Clear status/fault flags       |

---

## 14. Traceability

### 14.1 Requirements Traceability

| Design Element           | Requirement ID        | Description                   |
|-------------------------|-----------------------|-------------------------------|
| SBC_Trigger             | FBMS-FUNC-DRV-010    | SBC state machine trigger     |
| FS85_TriggerWatchdog    | FBMS-SAFETY-DRV-010  | Watchdog triggering           |
| FS85_SafetyPathChecks   | FBMS-SAFETY-DRV-011  | Safety path verification      |
| FS0B control            | FBMS-SAFETY-DRV-012  | Safe state output control     |
| LBIST/ABIST             | FBMS-SAFETY-DRV-013  | Self-test verification        |

### 14.2 Architecture Traceability

| Design Element    | Architecture Component | Interface ID  |
|-------------------|----------------------|---------------|
| SBC module        | COMP-DRV-SBC         | -             |
| SPI interface     | COMP-DRV-SPI         | IF-INT-006    |
| GPIO interface    | COMP-HAL-MCU         | -             |

---

## 15. Appendix

### 15.1 State Machine Initial Values

```c
SBC_STATE_s sbc_stateMcuSupervisor = {
    .timer = 0u,
    .stateRequest = SBC_STATE_NO_REQUEST,
    .state = SBC_STATEMACHINE_UNINITIALIZED,
    .substate = SBC_ENTRY,
    .lastState = SBC_STATEMACHINE_UNINITIALIZED,
    .lastSubstate = SBC_ENTRY,
    .illegalRequestsCounter = 0u,
    .retryCounter = 0u,
    .requestWatchdogTrigger = 0u,
    .triggerEntry = 0u,
    .pFs85xxInstance = &fs85xx_mcuSupervisor,
    .watchdogState = SBC_PERIODIC_WATCHDOG_DEACTIVATED,
    .watchdogPeriod_10ms = 10u,
    .useIgnitionForPowerDown = true,
};
```

### 15.2 FS85xx Register Addresses

| Register              | Address | Type      | Description              |
|-----------------------|---------|-----------|--------------------------|
| FS_GRL_FLAGS          | 0x00    | Fail-Safe | General flags            |
| FS_WD_WINDOW          | 0x16    | Fail-Safe | Watchdog window config   |
| FS_WD_SEED            | 0x17    | Fail-Safe | Watchdog seed            |
| FS_WD_ANSWER          | 0x18    | Fail-Safe | Watchdog answer          |
| FS_RELEASE_FS0B       | 0x1A    | Fail-Safe | FS0B release             |
| FS_STATES             | 0x1E    | Fail-Safe | State register           |
| M_FLAG                | 0x00    | Main      | Main flags               |
| M_MODE                | 0x01    | Main      | Mode configuration       |
| M_REG_CTRL1           | 0x02    | Main      | Regulator control 1      |
| M_DEVICEID            | 0x0E    | Main      | Device ID                |

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
