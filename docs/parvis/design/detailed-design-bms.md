# BMS Control Module Detailed Design Document

**Document ID**: FBMS-WP-SWE3-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D
**Component ID**: COMP-APP-BMS

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

This document provides the detailed design specification for the BMS Control Module (COMP-APP-BMS) of the foxBMS Battery Management System. It specifies the state machine design, function specifications, data structures, and safety mechanisms required for ASIL-D compliance.

### 1.2 Scope

This document covers:
- BMS state machine detailed design
- State transition conditions and timing
- Function specifications with pre/post conditions
- Data structure definitions
- Safety mechanism implementation (FAS_ASSERT, FAS_TRAP)
- Error handling procedures

### 1.3 References

| Document ID          | Title                                       |
|---------------------|---------------------------------------------|
| FBMS-WP-SWE1-001    | Software Requirements Specification         |
| FBMS-WP-SWE2-001    | Software Architecture Design                |
| ISO 26262-6:2018    | Product development at the software level   |

### 1.4 Source Files

| File                                | Description                    |
|------------------------------------|--------------------------------|
| src/app/application/bms/bms.c      | BMS module implementation      |
| src/app/application/bms/bms.h      | BMS module header              |
| src/app/application/config/bms_cfg.h | BMS configuration header     |

---

## 2. State Machine Design

### 2.1 Main State Machine (BMS_STATEMACH_e)

The BMS module implements a hierarchical state machine with main states and substates.

#### 2.1.1 State Enumeration

```c
typedef enum {
    BMS_STATEMACH_UNINITIALIZED,  /* Initial state after power-on */
    BMS_STATEMACH_INITIALIZATION, /* System initialization in progress */
    BMS_STATEMACH_INITIALIZED,    /* Initialization complete, waiting */
    BMS_STATEMACH_IDLE,           /* Idle state, contactors open */
    BMS_STATEMACH_OPEN_CONTACTORS,/* Opening all contactors */
    BMS_STATEMACH_STANDBY,        /* Standby mode, ready for operation */
    BMS_STATEMACH_PRECHARGE,      /* Precharge sequence active */
    BMS_STATEMACH_NORMAL,         /* Normal discharge operation */
    BMS_STATEMACH_DISCHARGE,      /* Discharge mode active */
    BMS_STATEMACH_CHARGE,         /* Charge mode active */
    BMS_STATEMACH_ERROR,          /* Error state, safe state */
    BMS_STATEMACH_UNDEFINED,      /* Undefined state (trap condition) */
    BMS_STATEMACH_RESERVED1,      /* Reserved for future use */
} BMS_STATEMACH_e;
```

#### 2.1.2 State Transition Conditions

| From State        | To State            | Condition                                    |
|-------------------|---------------------|----------------------------------------------|
| UNINITIALIZED     | INITIALIZATION      | BMS_STATE_INIT_REQUEST received              |
| INITIALIZATION    | INITIALIZED         | Init sequence complete                       |
| INITIALIZED       | IDLE                | IMD initialization complete                  |
| IDLE              | OPEN_CONTACTORS     | STANDBY request via CAN                      |
| IDLE              | OPEN_CONTACTORS     | Fatal error detected                         |
| OPEN_CONTACTORS   | STANDBY             | All contactors opened (normal request)       |
| OPEN_CONTACTORS   | ERROR               | All contactors opened (error condition)      |
| STANDBY           | PRECHARGE           | NORMAL or CHARGE request via CAN             |
| STANDBY           | OPEN_CONTACTORS     | Fatal error detected                         |
| PRECHARGE         | NORMAL/DISCHARGE    | Precharge successful (NORMAL request)        |
| PRECHARGE         | CHARGE              | Precharge successful (CHARGE request)        |
| PRECHARGE         | STANDBY             | Precharge failed, max retries exceeded       |
| NORMAL            | STANDBY             | STANDBY request via CAN                      |
| NORMAL            | ERROR               | Fatal error detected                         |
| DISCHARGE         | STANDBY             | STANDBY request via CAN                      |
| CHARGE            | STANDBY             | STANDBY request via CAN                      |
| ERROR             | (none)              | Requires power cycle                         |

### 2.2 Substate Machine (BMS_STATEMACH_SUB_e)

#### 2.2.1 Substate Enumeration

```c
typedef enum {
    BMS_ENTRY,                        /* Substate entry point */
    BMS_CHECK_ERROR_FLAGS_INTERLOCK,  /* Check errors after interlock */
    BMS_INTERLOCK_CHECKED,            /* Interlock verification done */
    BMS_CHECK_STATE_REQUESTS,         /* Check CAN state requests */
    BMS_CHECK_BALANCING_REQUESTS,     /* Check balancing requests */
    BMS_CHECK_ERROR_FLAGS,            /* Check diagnostic flags */
    BMS_CHECK_CONTACTOR_NORMAL_STATE, /* Verify contactor feedback */
    BMS_CHECK_CONTACTOR_CHARGE_STATE, /* Verify charge contactor */
    BMS_PRECHARGE_CLOSE_MINUS,        /* Close minus contactor */
    BMS_PRECHARGE_CLOSE_PRECHARGE,    /* Close precharge contactor */
    BMS_PRECHARGE_CHECK_VOLTAGES,     /* Monitor voltage rise */
    BMS_PRECHARGE_OPEN_PRECHARGE,     /* Open precharge contactor */
    BMS_PRECHARGE_CHECK_OPEN_PRECHARGE,/* Verify precharge opened */
    BMS_OPEN_FIRST_CONTACTOR,         /* Open first string contactor */
    BMS_OPEN_SECOND_CONTACTOR_MINUS,  /* Open minus contactor */
    BMS_OPEN_SECOND_CONTACTOR_PLUS,   /* Open plus contactor */
    BMS_OPEN_ALL_PRECHARGE_CONTACTORS,/* Open all precharge */
    BMS_CHECK_ALL_PRECHARGE_CONTACTORS_OPEN, /* Verify opened */
    BMS_OPEN_STRINGS_ENTRY,           /* Begin string opening */
    BMS_OPEN_FIRST_STRING_CONTACTOR,  /* Open first contactor */
    BMS_OPEN_SECOND_STRING_CONTACTOR, /* Open second contactor */
    BMS_CHECK_SECOND_STRING_CONTACTOR,/* Verify second opened */
    BMS_HANDLE_SUPPLY_VOLTAGE_30C_LOSS,/* Handle power loss */
    BMS_OPEN_STRINGS_EXIT,            /* Complete opening sequence */
    /* Additional substates... */
} BMS_STATEMACH_SUB_e;
```

### 2.3 Timing Parameters

| Parameter                               | Value    | Unit | Description                           |
|-----------------------------------------|----------|------|---------------------------------------|
| BMS_STATEMACH_SHORTTIME                 | 1        | x10ms| Short delay between states           |
| BMS_STATEMACH_MEDIUM_TIME               | 5        | x10ms| Medium delay between states          |
| BMS_STATEMACH_LONGTIME                  | 10       | x10ms| Long delay between states            |
| BMS_STRING_CLOSE_TIMEOUT                | 500      | x10ms| String close timeout                 |
| BMS_STRING_OPEN_TIMEOUT                 | 1000     | x10ms| String open timeout                  |
| BMS_PRECHARGE_CLOSE_TIMEOUT             | 500      | x10ms| Precharge close timeout              |
| BMS_PRECHARGE_OPEN_TIMEOUT              | 500      | x10ms| Precharge open timeout               |
| BMS_OSCILLATION_TIMEOUT                 | 1000     | x10ms| Anti-oscillation timeout             |
| BMS_PRECHARGE_TRIES                     | 3        | -    | Max precharge attempts               |
| BMS_TIME_WAIT_AFTER_CLOSING_PRECHARGE   | 200      | x10ms| Delay after precharge close          |
| BMS_TIME_WAIT_AFTER_OPENING_PRECHARGE   | 50       | x10ms| Delay after precharge open           |

---

## 3. Data Structures

### 3.1 BMS State Variable (BMS_STATE_s)

```c
typedef struct {
    uint16_t timer;                    /* State machine timer (x10ms) */
    BMS_STATE_REQUEST_e stateRequest;  /* Current state request */
    BMS_STATEMACH_e state;             /* Current main state */
    BMS_STATEMACH_SUB_e substate;      /* Current substate */
    BMS_STATEMACH_e lastState;         /* Previous main state */
    BMS_STATEMACH_SUB_e lastSubstate;  /* Previous substate */
    uint32_t ErrRequestCounter;        /* Illegal request counter */
    STD_RETURN_TYPE_e initFinished;    /* Init completion flag */
    uint8_t triggerentry;              /* Re-entrance protection */
    uint8_t counter;                   /* General purpose counter */
    BMS_CURRENT_FLOW_STATE_e currentFlowState; /* Charge/discharge state */
    uint32_t restTimer_10ms;           /* Rest period timer */
    uint16_t OscillationTimeout;       /* Anti-oscillation timer */
    uint8_t prechargeTryCounter;       /* Precharge attempt counter */
    BMS_POWER_PATH_TYPE_e powerPath;   /* Active power path */
    uint8_t numberOfClosedStrings;     /* Count of closed strings */
    uint16_t stringOpenTimeout;        /* String open timeout */
    uint32_t nextStringClosedTimer;    /* Timer for next string */
    uint16_t stringCloseTimeout;       /* String close timeout */
    BMS_STATEMACH_e nextState;         /* Target state after transition */
    uint8_t firstClosedString;         /* First closed string ID */
    uint16_t prechargeOpenTimeout;     /* Precharge open timeout */
    uint16_t prechargeCloseTimeout;    /* Precharge close timeout */
    uint32_t remainingDelay_ms;        /* Error delay countdown */
    uint32_t minimumActiveDelay_ms;    /* Minimum active error delay */
    uint32_t timeAboveContactorBreakCurrent_ms; /* Overcurrent timer */
    uint8_t stringToBeOpened;          /* String being opened */
    CONT_TYPE_e contactorToBeOpened;   /* Contactor being opened */
    bool transitionToErrorState;       /* Error transition flag */
    uint8_t closedPrechargeContactors[BS_NR_OF_STRINGS]; /* Precharge states */
    uint8_t closedStrings[BS_NR_OF_STRINGS];             /* String states */
    uint8_t deactivatedStrings[BS_NR_OF_STRINGS];        /* Deactivated strings */
} BMS_STATE_s;
```

### 3.2 Current Flow State (BMS_CURRENT_FLOW_STATE_e)

```c
typedef enum {
    BMS_CHARGING,    /* Battery is being charged */
    BMS_DISCHARGING, /* Battery is being discharged */
    BMS_RELAXATION,  /* Battery relaxation in progress */
    BMS_AT_REST,     /* Battery is at rest */
} BMS_CURRENT_FLOW_STATE_e;
```

### 3.3 Power Path Type (BMS_POWER_PATH_TYPE_e)

```c
typedef enum {
    BMS_POWER_PATH_OPEN, /* All contactors open */
    BMS_POWER_PATH_0,    /* Primary power path (discharge) */
    BMS_POWER_PATH_1,    /* Secondary power path (charge) */
} BMS_POWER_PATH_TYPE_e;
```

---

## 4. Function Specifications

### 4.1 BMS_Trigger()

**Purpose**: Main state machine trigger function, called every 10ms.

**Prototype**:
```c
extern void BMS_Trigger(void);
```

**Preconditions**:
- RTOS task scheduler running
- Database module initialized
- Contactor module initialized

**Postconditions**:
- State machine advanced by one step
- Measurement values updated
- SOA checks performed
- Contactor feedback verified

**Processing**:
1. Get latest measurement values from database
2. Update battery system state (charge/discharge/rest)
3. Perform SOA voltage, temperature, current checks
4. Check open sense wire conditions
5. Verify contactor feedback
6. Check re-entrance protection
7. Process state machine timer
8. Execute current state handler

**Safety Mechanisms**:
- Re-entrance check prevents concurrent execution
- Timer decrements with underflow protection
- State validation via switch-case default trap

### 4.2 BMS_SetStateRequest()

**Purpose**: Request a state change in the BMS state machine.

**Prototype**:
```c
extern BMS_RETURN_TYPE_e BMS_SetStateRequest(BMS_STATE_REQUEST_e statereq);
```

**Parameters**:
| Name      | Type                  | Direction | Description         |
|-----------|-----------------------|-----------|---------------------|
| statereq  | BMS_STATE_REQUEST_e   | In        | Requested state     |

**Return Values**:
| Value                  | Description                              |
|------------------------|------------------------------------------|
| BMS_OK                 | Request accepted                         |
| BMS_REQUEST_PENDING    | Another request is pending               |
| BMS_ILLEGAL_REQUEST    | Request not valid in current state       |
| BMS_ALREADY_INITIALIZED| Init requested when already initialized  |

**Critical Section**: Uses OS_EnterTaskCritical/OS_ExitTaskCritical

### 4.3 BMS_IsBatterySystemStateOkay()

**Purpose**: Check if battery system is in safe operating condition.

**Prototype**:
```c
static STD_RETURN_TYPE_e BMS_IsBatterySystemStateOkay(void);
```

**Return Values**:
| Value      | Description                                     |
|------------|-------------------------------------------------|
| STD_OK     | No fatal errors or delay active                 |
| STD_NOT_OK | Fatal error detected and delay elapsed          |

**Processing**:
1. Check all fatal error flags
2. If error detected, start delay countdown
3. Track minimum delay across all active errors
4. Return NOT_OK when delay reaches zero

### 4.4 BMS_CheckPrecharge()

**Purpose**: Verify precharge completion criteria.

**Prototype**:
```c
static STD_RETURN_TYPE_e BMS_CheckPrecharge(
    uint8_t stringNumber,
    const DATA_BLOCK_PACK_VALUES_s *pPackValues
);
```

**Parameters**:
| Name         | Type                         | Direction | Description           |
|--------------|------------------------------|-----------|-----------------------|
| stringNumber | uint8_t                      | In        | String to check       |
| pPackValues  | DATA_BLOCK_PACK_VALUES_s*    | In        | Pack voltage/current  |

**Precharge Success Criteria**:
- Voltage difference < BMS_PRECHARGE_VOLTAGE_THRESHOLD_mV (1000mV)
- Current < BMS_PRECHARGE_CURRENT_THRESHOLD_mA (50mA)

**Safety Assertions**:
- FAS_ASSERT(stringNumber < BS_NR_OF_STRINGS)
- FAS_ASSERT(pPackValues != NULL_PTR)

### 4.5 BMS_GetFirstContactorToBeOpened()

**Purpose**: Determine which contactor to open first based on current flow direction.

**Prototype**:
```c
static CONT_TYPE_e BMS_GetFirstContactorToBeOpened(
    uint8_t stringNumber,
    BMS_CURRENT_FLOW_STATE_e flowDirection
);
```

**Algorithm**:
1. Determine preferred breaking direction from current flow
2. Search for contactor in preferred direction
3. If not found, select PLUS contactor
4. If not found, select MINUS contactor
5. If no contactor found, trigger FAS_ASSERT(FAS_TRAP)

**Safety Consideration**: Opening in preferred direction minimizes arc damage.

---

## 5. Safety Mechanisms

### 5.1 FAS_ASSERT Usage

FAS_ASSERT is used for runtime assertion checking. Violations trigger system halt.

**Usage Locations in bms.c** (24 occurrences):

| Function                        | Assertion                              | Purpose                        |
|---------------------------------|----------------------------------------|--------------------------------|
| BMS_CheckPrecharge              | stringNumber < BS_NR_OF_STRINGS        | Array bounds check             |
| BMS_CheckPrecharge              | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_IsContactorFeedbackValid    | stringNumber < BS_NR_OF_STRINGS        | Array bounds check             |
| BMS_IsContactorFeedbackValid    | contactorType != CONT_UNDEFINED        | Valid contactor type           |
| BMS_GetHighestString            | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_GetClosestString            | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_GetLowestString             | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_GetStringVoltageDifference  | string < BS_NR_OF_STRINGS              | Array bounds check             |
| BMS_GetStringVoltageDifference  | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_GetAverageStringCurrent     | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_UpdateBatterySystemState    | pPackValues != NULL_PTR                | Null pointer check             |
| BMS_GetFirstContactorToBeOpened | stringNumber < BS_NR_OF_STRINGS        | Array bounds check             |
| BMS_GetSecondContactorToBeOpened| stringNumber < BS_NR_OF_STRINGS        | Array bounds check             |
| BMS_GetSecondContactorToBeOpened| firstOpenedContactorType valid         | Valid contactor type           |

### 5.2 FAS_TRAP Usage

FAS_TRAP is used to catch invalid states that should never occur.

**Usage Locations**:

| Location                           | Condition                              |
|------------------------------------|----------------------------------------|
| STANDBY state default case         | Invalid substate reached               |
| OPEN_CONTACTORS default case       | Invalid substate reached               |
| BMS_GetFirstContactorToBeOpened    | No contactor found in string           |
| BMS_GetSecondContactorToBeOpened   | Only one contactor in string           |

### 5.3 Re-entrance Protection

```c
static uint8_t BMS_CheckReEntrance(void) {
    uint8_t retval = 0;
    OS_EnterTaskCritical();
    if (!bms_state.triggerentry) {
        bms_state.triggerentry++;
    } else {
        retval = 0xFF; /* Multiple calls detected */
    }
    OS_ExitTaskCritical();
    return retval;
}
```

**Safety Purpose**: Prevents concurrent execution of state machine from multiple task contexts.

### 5.4 Critical Section Protection

All state request operations use critical sections:

```c
OS_EnterTaskCritical();
retVal = BMS_CheckStateRequest(statereq);
if (retVal == BMS_OK) {
    bms_state.stateRequest = statereq;
}
OS_ExitTaskCritical();
```

---

## 6. Error Handling

### 6.1 Diagnostic Integration

The BMS module integrates with the DIAG module for error reporting:

| Diagnostic ID                          | Condition                            |
|----------------------------------------|--------------------------------------|
| DIAG_ID_AFE_OPEN_WIRE                  | Open wire detected on cell voltage   |
| DIAG_ID_ALERT_MODE                     | Current above break threshold        |
| DIAG_ID_SUPPLY_VOLTAGE_CLAMP_30C_LOST  | 30C supply voltage loss              |
| DIAG_ID_PRECHARGE_ABORT_REASON_VOLTAGE | Precharge voltage threshold exceeded |
| DIAG_ID_PRECHARGE_ABORT_REASON_CURRENT | Precharge current threshold exceeded |

### 6.2 Error Delay Mechanism

Fatal errors trigger a configurable delay before contactor opening:

1. Error detected via DIAG_GetDiagnosisEntryState()
2. Get delay via DIAG_GetDelay()
3. Track minimum delay across all active errors
4. Countdown delay using timestamp difference
5. Open contactors when delay reaches zero

**Safety Rationale**: Allows controlled shutdown instead of immediate contactor opening.

### 6.3 Contactor Break Current Protection

```c
if (MATH_AbsInt32_t(bms_tablePackValues.stringCurrent_mA[stringNumber]) <
    BS_MAIN_CONTACTORS_MAXIMUM_BREAK_CURRENT_mA) {
    /* Safe to open contactor */
} else {
    /* Current too high, wait for fuse or timeout */
    bms_state.timeAboveContactorBreakCurrent_ms += BMS_STATEMACHINE_TASK_CYCLE_CONTEXT_MS;
    if (bms_state.timeAboveContactorBreakCurrent_ms > BS_MAIN_FUSE_MAXIMUM_TRIGGER_DURATION_ms) {
        /* Activate ALERT mode and open anyway */
        DIAG_Handler(DIAG_ID_ALERT_MODE, DIAG_EVENT_NOT_OK, DIAG_SYSTEM, 0u);
    }
}
```

---

## 7. Interface Specifications

### 7.1 External Interfaces

| Interface            | Direction | Function                    | Description                     |
|---------------------|-----------|-----------------------------|---------------------------------|
| CAN State Request   | Input     | BMS_CheckCanRequests()      | Receive state requests via CAN  |
| Database            | Bidirectional | DATA_READ_DATA/WRITE_DATA | Access measurement data         |
| DIAG                | Output    | DIAG_Handler()              | Report diagnostic events        |
| CONTACTOR           | Output    | CONT_OpenContactor/Close    | Control contactor state         |
| SOA                 | Input     | SOA_Check*()                | Perform limit checking          |
| BAL                 | Output    | BAL_SetStateRequest()       | Control balancing               |

### 7.2 Data Block Dependencies

| Data Block ID                  | Access    | Purpose                        |
|--------------------------------|-----------|--------------------------------|
| DATA_BLOCK_ID_MIN_MAX          | Read      | Cell voltage/temperature min/max|
| DATA_BLOCK_ID_OPEN_WIRE_BASE   | Read      | Open wire detection status     |
| DATA_BLOCK_ID_PACK_VALUES      | Read      | Pack voltage, current          |
| DATA_BLOCK_ID_STATE_REQUEST    | Read      | CAN state request              |
| DATA_BLOCK_ID_SYSTEM_STATE     | Read/Write| BMS CAN state reporting        |
| DATA_BLOCK_ID_ERROR_STATE      | Read      | Contactor feedback errors      |

---

## 8. Precharge Sequence

### 8.1 Sequence Description

1. **ENTRY**: Initialize precharge state, set CAN state to PRECHARGE
2. **CHECK_ERROR_FLAGS_PRECHARGE**: Verify no fatal errors
3. **PRECHARGE_CLOSE_MINUS**: Close string minus contactor
4. **PRECHARGE_CLOSE_PRECHARGE**: Close precharge contactor
5. **PRECHARGE_CHECK_VOLTAGES**: Monitor voltage rise, check timeout
6. **CHECK_PRECHARGE**: Verify voltage difference and current threshold
7. **PRECHARGE_OPEN_PRECHARGE**: Open precharge contactor
8. **CLOSE_SECOND_CONTACTOR_PLUS**: Close string plus contactor
9. **NORMAL/CHARGE**: Transition to operating state

### 8.2 Precharge Thresholds

| Parameter                        | Value  | Unit |
|----------------------------------|--------|------|
| BMS_PRECHARGE_VOLTAGE_THRESHOLD_mV | 1000 | mV   |
| BMS_PRECHARGE_CURRENT_THRESHOLD_mA | 50   | mA   |
| BMS_PRECHARGE_TRIES              | 3      | -    |

### 8.3 Precharge Failure Handling

- On failure: Increment prechargeTryCounter
- After 3 failures: Transition to STANDBY
- Set prechargeOpenTimeout for controlled opening

---

## 9. Traceability

### 9.1 Requirements Traceability

| Design Element               | Requirement ID        | Description                      |
|-----------------------------|-----------------------|----------------------------------|
| BMS_STATEMACH_e             | FBMS-FUNC-APP-001    | BMS state machine states         |
| BMS_CheckPrecharge()        | FBMS-FUNC-APP-002    | Precharge verification           |
| BMS_IsBatterySystemStateOkay| FBMS-FUNC-APP-003    | System state monitoring          |
| Error delay mechanism       | FBMS-SAFETY-APP-001  | Safe state transition delay      |
| Contactor break protection  | FBMS-SAFETY-APP-002  | Current-based contactor opening  |
| Re-entrance protection      | FBMS-SAFETY-APP-003  | Concurrent execution prevention  |

### 9.2 Architecture Traceability

| Design Element    | Architecture Component | Interface ID  |
|-------------------|----------------------|---------------|
| BMS module        | COMP-APP-BMS         | -             |
| Database access   | COMP-ENG-DB          | IF-INT-001    |
| DIAG integration  | COMP-ENG-DIAG        | IF-INT-004    |
| Contactor control | COMP-DRV-CONT        | IF-INT-005    |

---

## 10. Appendix

### 10.1 State Machine Initialization Values

```c
static BMS_STATE_s bms_state = {
    .timer                             = 0,
    .stateRequest                      = BMS_STATE_NO_REQUEST,
    .state                             = BMS_STATEMACH_UNINITIALIZED,
    .substate                          = BMS_ENTRY,
    .lastState                         = BMS_STATEMACH_UNINITIALIZED,
    .lastSubstate                      = BMS_ENTRY,
    .triggerentry                      = 0u,
    .ErrRequestCounter                 = 0u,
    .initFinished                      = STD_NOT_OK,
    .counter                           = 0u,
    .OscillationTimeout                = 0u,
    .prechargeTryCounter               = 0u,
    .powerPath                         = BMS_POWER_PATH_OPEN,
    .closedStrings                     = {0u},
    .closedPrechargeContactors         = {0u},
    .numberOfClosedStrings             = 0u,
    .deactivatedStrings                = {0},
    .firstClosedString                 = 0u,
    .stringOpenTimeout                 = 0u,
    .nextStringClosedTimer             = 0u,
    .stringCloseTimeout                = 0u,
    .nextState                         = BMS_STATEMACH_STANDBY,
    .restTimer_10ms                    = BS_RELAXATION_PERIOD_10ms,
    .currentFlowState                  = BMS_RELAXATION,
    .remainingDelay_ms                 = BMS_NO_ACTIVE_DELAY_TIME_ms,
    .minimumActiveDelay_ms             = BMS_NO_ACTIVE_DELAY_TIME_ms,
    .transitionToErrorState            = false,
    .timeAboveContactorBreakCurrent_ms = 0u,
    .stringToBeOpened                  = 0u,
    .contactorToBeOpened               = CONT_UNDEFINED,
};
```

### 10.2 Macro Definitions

```c
/* No active delay marker */
#define BMS_NO_ACTIVE_DELAY_TIME_ms (UINT32_MAX)

/* State save macro */
#define BMS_SAVE_LAST_STATES()                \
    bms_state.lastState    = bms_state.state; \
    bms_state.lastSubstate = bms_state.substate
```

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
