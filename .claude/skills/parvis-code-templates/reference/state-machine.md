# State Machine Templates

Templates for generating MISRA-compliant state machine code for foxBMS.

## enum-template.c.jinja

**Purpose:** Generate state enumeration with validation functions.

### Input Schema

```json
{
  "filename": "bms_state.c",
  "prefix": "BMS",
  "state_machine_name": "BMS State Machine",
  "requirement_id": "FBMS-SWE-BMS-001",
  "asil_level": "ASIL-B",
  "states": [
    {"name": "UNINITIALIZED", "value": 0, "description": "Initial state"},
    {"name": "INITIALIZATION", "value": 1, "description": "System init"},
    {"name": "IDLE", "value": 2, "description": "Ready for operation"},
    {"name": "RUNNING", "value": 3, "description": "Normal operation"},
    {"name": "ERROR", "value": 4, "description": "Error condition"}
  ],
  "include_validation_functions": true
}
```

### Generated Output

```c
/**
 * @brief   State enumeration for BMS State Machine
 * @req     FBMS-SWE-BMS-001
 */
typedef enum {
    /** @brief Initial state */
    BMS_STATE_UNINITIALIZED = 0u,
    /** @brief System init */
    BMS_STATE_INITIALIZATION = 1u,
    /** @brief Ready for operation */
    BMS_STATE_IDLE = 2u,
    /** @brief Normal operation */
    BMS_STATE_RUNNING = 3u,
    /** @brief Error condition */
    BMS_STATE_ERROR = 4u
} BMS_STATE_e;

#define BMS_NUMBER_OF_STATES (5u)

typedef enum {
    BMS_TRANSITION_OK = 0u,
    BMS_TRANSITION_INVALID_STATE = 1u,
    BMS_TRANSITION_INVALID_TARGET = 2u,
    BMS_TRANSITION_NOT_ALLOWED = 3u
} BMS_TRANSITION_RESULT_e;

typedef struct {
    BMS_STATE_e currentState;
    BMS_STATE_e previousState;
    uint32_t lastTransitionTimestamp_ms;
    uint32_t transitionCount;
    bool initialized;
} BMS_STATE_CONTEXT_s;

static inline bool BMS_IsValidState(BMS_STATE_e state) {
    bool isValid = false;
    if ((uint8_t)state < BMS_NUMBER_OF_STATES) {
        isValid = true;
    }
    return isValid;
}
```

### Template Variables

| Variable | Type | Description |
|----------|------|-------------|
| `prefix` | string | Module prefix (e.g., "BMS") |
| `states` | array | List of state objects |
| `states[].name` | string | State name |
| `states[].value` | int | State numeric value |
| `states[].description` | string | State description |
| `requirement_id` | string | Traceability ID |
| `asil_level` | string | ASIL level (QM, A, B, C, D) |

## transition-template.c.jinja

**Purpose:** Generate state transition matrix and handler.

### Input Schema

```json
{
  "prefix": "BMS",
  "states": ["INIT", "IDLE", "RUNNING", "ERROR"],
  "transitions": {
    "INIT": ["IDLE", "ERROR"],
    "IDLE": ["RUNNING", "ERROR"],
    "RUNNING": ["IDLE", "ERROR"],
    "ERROR": ["INIT"]
  }
}
```

### Generated Output

```c
static const bool bms_transitionMatrix[BMS_STATE_COUNT][BMS_STATE_COUNT] = {
    /* From INIT */     {false, true,  false, true },
    /* From IDLE */     {false, false, true,  true },
    /* From RUNNING */  {false, true,  false, true },
    /* From ERROR */    {true,  false, false, false}
};

BMS_TRANSITION_RESULT_e BMS_RequestStateChange(BMS_STATE_e targetState) {
    BMS_TRANSITION_RESULT_e result = BMS_TRANSITION_NOT_ALLOWED;

    FAS_ASSERT(BMS_IsValidState(targetState) == true);

    if (bms_transitionMatrix[bms_context.currentState][targetState] == true) {
        bms_context.previousState = bms_context.currentState;
        bms_context.currentState = targetState;
        bms_context.transitionCount++;
        result = BMS_TRANSITION_OK;
    }

    return result;
}
```

## MISRA Compliance Features

1. **Unsigned enum values:** All state values use `u` suffix
2. **Explicit casts:** `(uint8_t)state` for comparisons
3. **Validation functions:** Range checking before use
4. **Single return:** All functions use single return point
5. **FAS_ASSERT:** Parameter validation at function entry
6. **Default case:** Switch statements include default with FAS_TRAP

## foxBMS State Machine Pattern

```c
void BMS_ProcessStateMachine(void) {
    switch (bms_context.currentState) {
        case BMS_STATE_UNINITIALIZED:
            BMS_StateUninitialized();
            break;
        case BMS_STATE_INITIALIZATION:
            BMS_StateInitialization();
            break;
        case BMS_STATE_IDLE:
            BMS_StateIdle();
            break;
        case BMS_STATE_RUNNING:
            BMS_StateRunning();
            break;
        case BMS_STATE_ERROR:
            BMS_StateError();
            break;
        default:
            FAS_ASSERT(FAS_TRAP);
            break;
    }
}
```
