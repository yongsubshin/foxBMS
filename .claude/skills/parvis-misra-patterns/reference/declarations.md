# Declaration Patterns

MISRA C:2012 Rules 8.x - Declarations for foxBMS.

## Storage Class Patterns

### DC-001: Static for File-Scope (Rule 8.7)
```c
/* CORRECT */
static uint32_t moduleCounter = 0u;
static bool isInitialized = false;

/* WRONG - external linkage by default */
uint32_t moduleCounter = 0u;
bool isInitialized = false;
```
**Rationale:** Limits visibility to translation unit, prevents name collisions.

### DC-002: Static Function Declaration (Rule 8.8)
```c
/* CORRECT */
static void ProcessInternal(void);
static bool ValidateData(const uint8_t* pData);

/* WRONG - should be static if not used externally */
void ProcessInternal(void);
```

### DC-003: Extern Declaration (Rule 8.4)
```c
/* In header file (.h) */
extern uint32_t GLOBAL_SystemTick;
extern void PUBLIC_Function(void);

/* In source file (.c) */
uint32_t GLOBAL_SystemTick = 0u;
void PUBLIC_Function(void) { /* ... */ }
```

## Initialization Patterns

### DC-004: Variable Initialization (Rule 9.1)
```c
/* CORRECT */
uint32_t counter = 0u;
bool flag = false;
int16_t* pData = NULL;

/* WRONG - uninitialized */
uint32_t counter;
bool flag;
int16_t* pData;
```
**Rationale:** Uninitialized variables have indeterminate values.

### DC-005: Array Initialization (Rule 9.2)
```c
/* CORRECT - full initialization */
uint8_t buffer[8] = {0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u};

/* CORRECT - partial with zero-fill */
uint8_t buffer[8] = {0u};  /* All elements zero */

/* WRONG - partial initialization */
uint8_t buffer[8] = {1u, 2u};  /* Elements 2-7 are zero but not obvious */
```

### DC-006: Structure Initialization (Rule 9.2)
```c
/* CORRECT - designated initializers */
BMS_STATE_s bmsState = {
    .currentState = BMS_STATE_UNINITIALIZED,
    .previousState = BMS_STATE_UNINITIALIZED,
    .errorFlags = 0u,
    .initialized = false
};

/* CORRECT - all zeros */
BMS_STATE_s bmsState = {0};
```

## Parameter Patterns

### DC-007: Const Input Parameter (Rule 8.13)
```c
/* CORRECT */
void ProcessData(const uint8_t* pData, uint32_t length);
void CompareValues(const DATA_BLOCK_s* pBlockA, const DATA_BLOCK_s* pBlockB);

/* WRONG - missing const */
void ProcessData(uint8_t* pData, uint32_t length);
```

### DC-008: Output Parameter Naming (Convention)
```c
/* CORRECT - clear output indication */
STD_RETURN_TYPE_e GetValue(uint32_t* pOutputValue);
STD_RETURN_TYPE_e ReadSensor(int16_t* pResult_mV);

/* foxBMS convention: p prefix for pointers */
void UpdateState(BMS_STATE_s* pState);
```

### DC-009: Void Parameter List (Rule 8.2)
```c
/* CORRECT */
void Initialize(void);
uint32_t GetCounter(void);

/* WRONG - empty parameter list (K&R style) */
void Initialize();
uint32_t GetCounter();
```

## Function Declaration Patterns

### DC-010: Function Prototype (Rule 8.2)
```c
/* CORRECT - full prototype */
static void ProcessCell(uint16_t cellIndex, int16_t voltage_mV);

/* WRONG - missing parameter names */
static void ProcessCell(uint16_t, int16_t);
```

### DC-011: Return Type Explicit (Rule 8.1)
```c
/* CORRECT */
static void ProcessData(void);
static uint32_t CalculateChecksum(const uint8_t* pData, uint32_t length);

/* WRONG - implicit int return (legacy C) */
static ProcessData(void);  /* Returns int implicitly */
```

### DC-012: Inline Function (Rule 8.10)
```c
/* CORRECT - static inline in header */
static inline bool IsValidIndex(uint16_t index) {
    return (index < MAX_INDEX);
}

/* In header file for inlining across translation units */
```

## foxBMS Naming Conventions

### DC-013: Module Prefix
```c
/* CORRECT - module prefix */
static void BMS_ProcessStateMachine(void);
static void AFE_ReadVoltages(void);
static void DIAG_HandleError(DIAG_ID_e diagId);

/* Type naming */
typedef struct BMS_STATE_s { /* ... */ } BMS_STATE_s;
typedef enum BMS_STATE_e { /* ... */ } BMS_STATE_e;
```

### DC-014: foxBMS File Structure
```c
/*========== Includes =======================================================*/
#include "bms.h"

/*========== Macros and Definitions =========================================*/
#define BMS_STATEMACHINE_SHORTTIME (1u)

/*========== Static Constant and Variable Definitions =======================*/
static BMS_STATE_s bms_state = {0};

/*========== Extern Constant and Variable Definitions =======================*/

/*========== Static Function Prototypes =====================================*/
static void BMS_ProcessStateMachine(void);

/*========== Static Function Implementations ================================*/
static void BMS_ProcessStateMachine(void) {
    /* Implementation */
}

/*========== Extern Function Implementations ================================*/
void BMS_Trigger(void) {
    /* Public function */
}
```

### DC-015: Header Guard
```c
/* CORRECT - foxBMS style */
#ifndef FOXBMS__BMS_H_
#define FOXBMS__BMS_H_

/* Header content */

#endif /* FOXBMS__BMS_H_ */

/* Format: FOXBMS__<MODULE>_H_ */
```

## Summary Table

| ID | Rule | Pattern | Severity |
|----|------|---------|----------|
| DC-001 | 8.7 | Static for file-scope | Required |
| DC-002 | 8.8 | Static functions | Required |
| DC-003 | 8.4 | Extern in headers | Required |
| DC-004 | 9.1 | Initialize variables | Required |
| DC-005 | 9.2 | Full array init | Required |
| DC-006 | 9.2 | Struct initializers | Advisory |
| DC-007 | 8.13 | Const input params | Advisory |
| DC-008 | - | Output param naming | Convention |
| DC-009 | 8.2 | Void parameter | Required |
| DC-010 | 8.2 | Full prototypes | Required |
| DC-011 | 8.1 | Explicit return type | Required |
| DC-012 | 8.10 | Static inline | Advisory |
