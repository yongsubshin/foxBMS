# Contactor Driver Module Detailed Design Document

**Document ID**: FBMS-WP-SWE3-004
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D
**Component ID**: COMP-DRV-CONT

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

This document provides the detailed design specification for the Contactor Driver Module (COMP-DRV-CONT) of the foxBMS Battery Management System. It specifies the contactor control logic, feedback validation, and safety mechanisms for high-power switching operations.

### 1.2 Scope

This document covers:
- Contactor state machine design
- Contactor feedback monitoring
- Precharge sequence control
- Safe opening sequence
- Error handling and diagnostics

### 1.3 References

| Document ID          | Title                                       |
|---------------------|---------------------------------------------|
| FBMS-WP-SWE1-001    | Software Requirements Specification         |
| FBMS-WP-SWE2-001    | Software Architecture Design                |
| ISO 26262-6:2018    | Product development at the software level   |

### 1.4 Source Files

| File                                          | Description                    |
|----------------------------------------------|--------------------------------|
| src/app/driver/contactor/contactor.c         | Contactor driver implementation|
| src/app/driver/contactor/contactor.h         | Contactor driver header        |
| src/app/driver/config/contactor_cfg.h        | Configuration header           |
| src/app/driver/config/contactor_cfg.c        | Configuration source           |

---

## 2. Contactor System Overview

### 2.1 Contactor Types

```c
typedef enum {
    CONT_PLUS,      /* Contactor in HV plus path */
    CONT_MINUS,     /* Contactor in HV minus path */
    CONT_PRECHARGE, /* Precharge contactor (plus path) */
    CONT_UNDEFINED, /* Undefined contactor type */
} CONT_TYPE_e;
```

### 2.2 System Topology

```
                    +--[Fuse]--+
                    |          |
        +-----------|----------|----> HV+
        |           |          |
        |    +------+------+   |
        |    | CONT_PLUS   |   |
        |    +-------------+   |
        |           |          |
    String         Load        |
        |           |          |
        |    +------+------+   |
        |    | CONT_MINUS  |   |
        |    +-------------+   |
        |           |          |
        +-----------+----------+----> HV-
                    |
                    +--[Precharge]--+
                    |               |
              +-----+-----+   +-----+-----+
              | Resistor  |   |CONT_PRECH |
              +-----------+   +-----------+
```

### 2.3 Contactor Electrical States

```c
typedef enum {
    CONT_SWITCH_OFF,       /* Contactor open */
    CONT_SWITCH_ON,        /* Contactor closed */
    CONT_SWITCH_UNDEFINED, /* State unknown */
} CONT_ELECTRICAL_STATE_TYPE_e;
```

---

## 3. Data Structures

### 3.1 Contactor State Structure

```c
typedef struct {
    CONT_ELECTRICAL_STATE_TYPE_e currentSet;    /* Commanded state */
    CONT_ELECTRICAL_STATE_TYPE_e feedback;      /* Actual state from feedback */
    const CONT_FEEDBACK_TYPE_e feedbackPinType; /* Feedback source type */
    const BS_STRING_ID_e stringIndex;           /* String number */
    const CONT_TYPE_e type;                     /* Contactor type */
    const SPS_CHANNEL_INDEX spsChannel;         /* SPS channel number */
    const CONT_CURRENT_BREAKING_DIRECTION_e breakingDirection; /* Opening preference */
} CONT_CONTACTOR_STATE_s;
```

### 3.2 Feedback Types

```c
typedef enum {
    CONT_FEEDBACK_NORMALLY_OPEN,   /* Feedback NO contact */
    CONT_FEEDBACK_NORMALLY_CLOSED, /* Feedback NC contact */
    CONT_FEEDBACK_THROUGH_CURRENT, /* Current-based feedback */
    CONT_HAS_NO_FEEDBACK,          /* No feedback available */
} CONT_FEEDBACK_TYPE_e;
```

### 3.3 Current Breaking Direction

```c
typedef enum {
    CONT_CHARGING_DIRECTION,    /* Optimized for charge current */
    CONT_DISCHARGING_DIRECTION, /* Optimized for discharge current */
    CONT_BIDIRECTIONAL,         /* No preferred direction */
} CONT_CURRENT_BREAKING_DIRECTION_e;
```

### 3.4 Contactor Registry

```c
/* Central contactor state registry */
extern CONT_CONTACTOR_STATE_s cont_contactorStates[BS_NR_OF_CONTACTORS];
```

---

## 4. Function Specifications

### 4.1 CONT_Initialize()

**Purpose**: Initialize the contactor module.

**Prototype**:
```c
extern void CONT_Initialize(void);
```

**Processing**:
1. Call CONT_InitializationCheckOfContactorRegistry()
2. Verify all contactor configurations

**Safety Checks**:
- Verify SPS channel assignments valid
- Verify channel affiliation is SPS_AFF_CONTACTOR

### 4.2 CONT_OpenContactor()

**Purpose**: Request contactor to open.

**Prototype**:
```c
extern STD_RETURN_TYPE_e CONT_OpenContactor(
    uint8_t stringNumber,
    CONT_TYPE_e contactor
);
```

**Parameters**:
| Name         | Type        | Direction | Description            |
|--------------|-------------|-----------|------------------------|
| stringNumber | uint8_t     | In        | String number (0..n-1) |
| contactor    | CONT_TYPE_e | In        | Contactor type to open |

**Return Values**:
| Value      | Description                    |
|------------|--------------------------------|
| STD_OK     | Contactor found and opened     |
| STD_NOT_OK | Contactor not found            |

**Processing**:
```c
extern STD_RETURN_TYPE_e CONT_OpenContactor(uint8_t stringNumber, CONT_TYPE_e contactor) {
    FAS_ASSERT(stringNumber < BS_NR_OF_STRINGS);
    FAS_ASSERT(contactor != CONT_UNDEFINED);
    STD_RETURN_TYPE_e retval = STD_NOT_OK;

    for (uint8_t contactorIndex = 0u; contactorIndex < BS_NR_OF_CONTACTORS; contactorIndex++) {
        if (((BS_STRING_ID_e)stringNumber == cont_contactorStates[contactorIndex].stringIndex) &&
            (contactor == cont_contactorStates[contactorIndex].type)) {
            /* Set state in registry */
            cont_contactorStates[contactorIndex].currentSet = CONT_SWITCH_OFF;
            /* Request via SPS module */
            SPS_RequestContactorState(cont_contactorStates[contactorIndex].spsChannel, SPS_CHANNEL_OFF);
            retval = STD_OK;
            break;
        }
    }
    return retval;
}
```

**Safety Assertions**:
- FAS_ASSERT(stringNumber < BS_NR_OF_STRINGS)
- FAS_ASSERT(contactor != CONT_UNDEFINED)

### 4.3 CONT_CloseContactor()

**Purpose**: Request contactor to close.

**Prototype**:
```c
extern STD_RETURN_TYPE_e CONT_CloseContactor(
    uint8_t stringNumber,
    CONT_TYPE_e contactor
);
```

**Processing**: Similar to CONT_OpenContactor but sets state to CONT_SWITCH_ON.

**Safety Assertions**:
- FAS_ASSERT(stringNumber < BS_NR_OF_STRINGS)
- FAS_ASSERT(contactor != CONT_UNDEFINED)

### 4.4 CONT_ClosePrecharge()

**Purpose**: Close precharge contactor for specified string.

**Prototype**:
```c
extern STD_RETURN_TYPE_e CONT_ClosePrecharge(uint8_t stringNumber);
```

**Processing**:
```c
extern STD_RETURN_TYPE_e CONT_ClosePrecharge(uint8_t stringNumber) {
    FAS_ASSERT(stringNumber < BS_NR_OF_STRINGS);
    STD_RETURN_TYPE_e retVal = STD_NOT_OK;

    /* Check if string has precharge contactor */
    if (bs_stringsWithPrecharge[stringNumber] == BS_STRING_WITH_PRECHARGE) {
        retVal = CONT_CloseContactor(stringNumber, CONT_PRECHARGE);
    }
    return retVal;
}
```

### 4.5 CONT_OpenPrecharge()

**Purpose**: Open precharge contactor for specified string.

**Prototype**:
```c
extern STD_RETURN_TYPE_e CONT_OpenPrecharge(uint8_t stringNumber);
```

### 4.6 CONT_OpenAllPrechargeContactors()

**Purpose**: Open all precharge contactors in system.

**Prototype**:
```c
extern void CONT_OpenAllPrechargeContactors(void);
```

**Processing**:
```c
extern void CONT_OpenAllPrechargeContactors(void) {
    for (uint8_t contactorIndex = 0u; contactorIndex < BS_NR_OF_CONTACTORS; contactorIndex++) {
        if (cont_contactorStates[contactorIndex].type == CONT_PRECHARGE) {
            SPS_RequestContactorState(cont_contactorStates[contactorIndex].spsChannel, SPS_CHANNEL_OFF);
            cont_contactorStates[contactorIndex].currentSet = CONT_SWITCH_OFF;
        }
    }
}
```

**Safety Purpose**: Ensures safe state by opening all precharge paths.

### 4.7 CONT_OpenAllContactors()

**Purpose**: Open all contactors in system (safe state).

**Prototype**:
```c
extern void CONT_OpenAllContactors(void);
```

**Processing**:
```c
extern void CONT_OpenAllContactors(void) {
    for (uint8_t contactorIndex = 0u; contactorIndex < BS_NR_OF_CONTACTORS; contactorIndex++) {
        SPS_RequestContactorState(cont_contactorStates[contactorIndex].spsChannel, SPS_CHANNEL_OFF);
        cont_contactorStates[contactorIndex].currentSet = CONT_SWITCH_OFF;
    }
}
```

**Safety Purpose**: Emergency safe state function.

### 4.8 CONT_GetContactorState()

**Purpose**: Get current feedback state of contactor.

**Prototype**:
```c
extern CONT_ELECTRICAL_STATE_TYPE_e CONT_GetContactorState(
    uint8_t stringNumber,
    CONT_TYPE_e contactorType
);
```

**Return Values**:
| Value              | Description              |
|--------------------|--------------------------|
| CONT_SWITCH_OFF    | Contactor is open        |
| CONT_SWITCH_ON     | Contactor is closed      |
| CONT_SWITCH_UNDEFINED | Unknown state         |

### 4.9 CONT_CheckFeedback()

**Purpose**: Check feedback of all contactors and report discrepancies.

**Prototype**:
```c
extern void CONT_CheckFeedback(void);
```

**Processing**:
1. Get feedback from all contactors
2. Compare commanded state vs feedback
3. Report discrepancies to DIAG module

**Diagnostic Events**:
| Contactor Type | Diagnostic ID                          |
|----------------|----------------------------------------|
| CONT_PLUS      | DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK |
| CONT_MINUS     | DIAG_ID_STRING_MINUS_CONTACTOR_FEEDBACK|
| CONT_PRECHARGE | DIAG_ID_PRECHARGE_CONTACTOR_FEEDBACK   |

---

## 5. Feedback Handling

### 5.1 Feedback Source Types

```c
static void CONT_GetFeedbackOfAllContactors(void) {
    for (CONT_CONTACTOR_INDEX contactor = 0; contactor < BS_NR_OF_CONTACTORS; contactor++) {
        if (cont_contactorStates[contactor].feedbackPinType == CONT_HAS_NO_FEEDBACK) {
            /* No feedback: assume commanded state is actual state */
            cont_contactorStates[contactor].feedback = cont_contactorStates[contactor].currentSet;
        }
        else if (cont_contactorStates[contactor].feedbackPinType == CONT_FEEDBACK_THROUGH_CURRENT) {
            /* Get feedback from SPS current measurement */
            cont_contactorStates[contactor].feedback =
                SPS_GetChannelCurrentFeedback(cont_contactorStates[contactor].spsChannel);
        }
        else if (CONT_FEEDBACK_NORMALLY_OPEN == cont_contactorStates[contactor].feedbackPinType) {
            /* Get feedback from PEX (normally open contact) */
            cont_contactorStates[contactor].feedback =
                SPS_GetChannelPexFeedback(cont_contactorStates[contactor].spsChannel, true);
        }
        else {
            /* CONT_FEEDBACK_NORMALLY_CLOSED */
            cont_contactorStates[contactor].feedback =
                SPS_GetChannelPexFeedback(cont_contactorStates[contactor].spsChannel, false);
        }
    }
}
```

### 5.2 Feedback Validation Logic

| Feedback Type         | Open State Detection  | Closed State Detection |
|-----------------------|-----------------------|------------------------|
| NORMALLY_OPEN         | Feedback LOW          | Feedback HIGH          |
| NORMALLY_CLOSED       | Feedback HIGH         | Feedback LOW           |
| THROUGH_CURRENT       | No current flow       | Current flowing        |
| NO_FEEDBACK           | Assume commanded      | Assume commanded       |

---

## 6. Initialization Verification

### 6.1 Registry Check Function

```c
static void CONT_InitializationCheckOfContactorRegistry(void) {
    for (CONT_CONTACTOR_INDEX contactor = 0u; contactor < BS_NR_OF_CONTACTORS; contactor++) {
        /* Verify SPS channel is valid */
        FAS_ASSERT(cont_contactorStates[contactor].spsChannel < SPS_NR_OF_AVAILABLE_SPS_CHANNELS);

        /* Verify channel is affiliated with contactor */
        const SPS_CHANNEL_AFFILIATION_e channelAffiliation =
            SPS_GetChannelAffiliation(cont_contactorStates[contactor].spsChannel);
        FAS_ASSERT(SPS_AFF_CONTACTOR == channelAffiliation);
    }
}
```

### 6.2 Configuration Validation

| Check                        | Assertion                              |
|------------------------------|----------------------------------------|
| SPS Channel Range            | spsChannel < SPS_NR_OF_AVAILABLE_SPS_CHANNELS |
| Channel Affiliation          | SPS_AFF_CONTACTOR == channelAffiliation |

---

## 7. Safety Mechanisms

### 7.1 FAS_ASSERT Usage

| Function                     | Assertion                        | Purpose                |
|------------------------------|----------------------------------|------------------------|
| CONT_OpenContactor           | stringNumber < BS_NR_OF_STRINGS  | Array bounds           |
| CONT_OpenContactor           | contactor != CONT_UNDEFINED      | Valid type             |
| CONT_CloseContactor          | stringNumber < BS_NR_OF_STRINGS  | Array bounds           |
| CONT_CloseContactor          | contactor != CONT_UNDEFINED      | Valid type             |
| CONT_ClosePrecharge          | stringNumber < BS_NR_OF_STRINGS  | Array bounds           |
| CONT_OpenPrecharge           | stringNumber < BS_NR_OF_STRINGS  | Array bounds           |
| CONT_GetContactorState       | stringNumber < BS_NR_OF_STRINGS  | Array bounds           |
| CONT_GetContactorState       | contactorType != CONT_UNDEFINED  | Valid type             |
| InitializationCheck          | spsChannel valid range           | Configuration          |
| InitializationCheck          | SPS affiliation correct          | Configuration          |

### 7.2 FAS_TRAP Usage

```c
switch (cont_contactorStates[contactor].type) {
    case CONT_PLUS:
        /* Handle plus contactor */
        break;
    case CONT_MINUS:
        /* Handle minus contactor */
        break;
    case CONT_PRECHARGE:
        /* Handle precharge contactor */
        break;
    default:
        /* Type: CONT_UNDEFINED -> trap */
        FAS_ASSERT(FAS_TRAP);
}
```

### 7.3 Feedback Mismatch Handling

When feedback does not match commanded state:
1. Report to DIAG module
2. BMS module receives error flag
3. BMS initiates contactor opening sequence
4. System transitions to ERROR state if persistent

---

## 8. Interface with SPS Module

### 8.1 SPS Interface Functions

| Function                       | Description                      |
|--------------------------------|----------------------------------|
| SPS_RequestContactorState      | Command contactor on/off         |
| SPS_GetChannelCurrentFeedback  | Get current-based feedback       |
| SPS_GetChannelPexFeedback      | Get PEX digital feedback         |
| SPS_GetChannelAffiliation      | Get channel purpose              |

### 8.2 SPS Channel States

```c
typedef enum {
    SPS_CHANNEL_OFF, /* Channel disabled (contactor open) */
    SPS_CHANNEL_ON,  /* Channel enabled (contactor closed) */
} SPS_CHANNEL_STATE_e;
```

---

## 9. Precharge Sequence

### 9.1 Sequence Overview

The precharge sequence is managed by BMS module but uses contactor functions:

```
1. CONT_CloseContactor(string, CONT_MINUS)
   - Close minus contactor first
   - Wait for feedback confirmation

2. CONT_ClosePrecharge(string)
   - Close precharge contactor
   - Wait for capacitor charging

3. [BMS monitors voltage rise]
   - Check voltage difference decreasing
   - Check current below threshold

4. CONT_CloseContactor(string, CONT_PLUS)
   - Close plus contactor
   - Wait for feedback confirmation

5. CONT_OpenPrecharge(string)
   - Open precharge contactor
   - Normal operation begins
```

### 9.2 Precharge Abort Handling

If precharge fails:
1. CONT_OpenPrecharge(string)
2. CONT_OpenContactor(string, CONT_MINUS)
3. Report DIAG_ID_PRECHARGE_ABORT_REASON_*

---

## 10. Contactor Opening Sequence

### 10.1 Safe Opening Order

To minimize arc damage based on current direction:

**Discharge Mode (current flows out)**:
1. Open contactor in discharge direction first
2. Open remaining contactor second

**Charge Mode (current flows in)**:
1. Open contactor in charge direction first
2. Open remaining contactor second

### 10.2 Breaking Direction Selection

```c
/* Get preferred opening direction based on current */
if (flowDirection == BMS_CHARGING) {
    breakingDirection = CONT_CHARGING_DIRECTION;
} else {
    breakingDirection = CONT_DISCHARGING_DIRECTION;
}

/* Search for contactor in preferred direction */
for (contactor = 0u; contactor < BS_NR_OF_CONTACTORS; contactor++) {
    if ((cont_contactorStates[contactor].breakingDirection == breakingDirection) ||
        (cont_contactorStates[contactor].breakingDirection == CONT_BIDIRECTIONAL)) {
        /* Found suitable contactor to open first */
        break;
    }
}
```

---

## 11. Error Handling

### 11.1 Contactor Feedback Errors

| Error Condition              | Diagnostic ID                            | Response              |
|------------------------------|------------------------------------------|-----------------------|
| Plus contactor mismatch      | DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK   | Open contactors       |
| Minus contactor mismatch     | DIAG_ID_STRING_MINUS_CONTACTOR_FEEDBACK  | Open contactors       |
| Precharge contactor mismatch | DIAG_ID_PRECHARGE_CONTACTOR_FEEDBACK     | Open contactors       |

### 11.2 Diagnostic Reporting

```c
if (cont_contactorStates[contactor].currentSet != cont_contactorStates[contactor].feedback) {
    feedbackStatus = DIAG_EVENT_NOT_OK;
} else {
    feedbackStatus = DIAG_EVENT_OK;
}

DIAG_Handler(
    DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK,
    feedbackStatus,
    DIAG_STRING,
    (uint8_t)cont_contactorStates[contactor].stringIndex
);
```

---

## 12. Configuration Examples

### 12.1 Single String Configuration

```c
CONT_CONTACTOR_STATE_s cont_contactorStates[BS_NR_OF_CONTACTORS] = {
    {
        .currentSet = CONT_SWITCH_OFF,
        .feedback = CONT_SWITCH_OFF,
        .feedbackPinType = CONT_FEEDBACK_THROUGH_CURRENT,
        .stringIndex = BS_STRING_0,
        .type = CONT_PLUS,
        .spsChannel = SPS_CHANNEL_0,
        .breakingDirection = CONT_DISCHARGING_DIRECTION,
    },
    {
        .currentSet = CONT_SWITCH_OFF,
        .feedback = CONT_SWITCH_OFF,
        .feedbackPinType = CONT_FEEDBACK_THROUGH_CURRENT,
        .stringIndex = BS_STRING_0,
        .type = CONT_MINUS,
        .spsChannel = SPS_CHANNEL_1,
        .breakingDirection = CONT_CHARGING_DIRECTION,
    },
    {
        .currentSet = CONT_SWITCH_OFF,
        .feedback = CONT_SWITCH_OFF,
        .feedbackPinType = CONT_FEEDBACK_THROUGH_CURRENT,
        .stringIndex = BS_STRING_0,
        .type = CONT_PRECHARGE,
        .spsChannel = SPS_CHANNEL_2,
        .breakingDirection = CONT_BIDIRECTIONAL,
    },
};
```

### 12.2 Multi-String Configuration

For multi-string systems, add contactor entries for each string:
- BS_STRING_0: CONT_PLUS, CONT_MINUS, CONT_PRECHARGE
- BS_STRING_1: CONT_PLUS, CONT_MINUS, CONT_PRECHARGE
- etc.

---

## 13. Traceability

### 13.1 Requirements Traceability

| Design Element              | Requirement ID        | Description                   |
|----------------------------|-----------------------|-------------------------------|
| CONT_OpenContactor         | FBMS-FUNC-DRV-020    | Contactor open control        |
| CONT_CloseContactor        | FBMS-FUNC-DRV-021    | Contactor close control       |
| CONT_CheckFeedback         | FBMS-SAFETY-DRV-020  | Feedback validation           |
| Precharge sequence         | FBMS-FUNC-DRV-022    | Precharge control             |
| Breaking direction         | FBMS-SAFETY-DRV-021  | Safe opening sequence         |

### 13.2 Architecture Traceability

| Design Element    | Architecture Component | Interface ID  |
|-------------------|----------------------|---------------|
| Contactor module  | COMP-DRV-CONT        | -             |
| SPS interface     | COMP-DRV-SPS         | -             |
| BMS interface     | COMP-APP-BMS         | IF-INT-005    |
| DIAG interface    | COMP-ENG-DIAG        | -             |

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
