# Safety Assertion Patterns

FAS_ASSERT patterns for foxBMS safety-critical code (ISO 26262).

## FAS_ASSERT Fundamentals

### SA-001: Basic FAS_ASSERT Usage
```c
/* FAS_ASSERT triggers system error handler on failure */
FAS_ASSERT(condition);

/* Examples */
FAS_ASSERT(pData != NULL);              /* Pointer validation */
FAS_ASSERT(index < ARRAY_SIZE);         /* Bounds check */
FAS_ASSERT(value != INVALID_VALUE);     /* Value validation */
```

### SA-002: FAS_TRAP for Unreachable Code
```c
/* Use FAS_TRAP in switch default for enum switches */
switch (state) {
    case STATE_A:
        break;
    case STATE_B:
        break;
    default:
        FAS_ASSERT(FAS_TRAP);  /* Should never reach here */
        break;
}
```

## Parameter Validation

### SA-003: Pointer Parameter Validation
```c
void ProcessBuffer(uint8_t* pBuffer, uint32_t length) {
    /* Validate all pointer parameters at function entry */
    FAS_ASSERT(pBuffer != NULL);

    /* Then use safely */
    for (uint32_t i = 0u; i < length; i++) {
        pBuffer[i] = 0u;
    }
}
```

### SA-004: Double Pointer Validation
```c
void GetReference(DATA_BLOCK_s** ppBlock) {
    /* Validate both levels */
    FAS_ASSERT(ppBlock != NULL);
    FAS_ASSERT(*ppBlock != NULL);

    /* Safe to use */
}
```

### SA-005: Range Parameter Validation
```c
void SetCellIndex(uint16_t stringIndex, uint16_t cellIndex) {
    /* Validate indices are within bounds */
    FAS_ASSERT(stringIndex < BS_NR_OF_STRINGS);
    FAS_ASSERT(cellIndex < BS_NR_OF_CELL_BLOCKS_PER_STRING);

    /* Safe to use as array indices */
}
```

## Array Access Safety

### SA-006: Array Index Validation
```c
int16_t GetCellVoltage(uint16_t index) {
    /* Always validate before array access */
    FAS_ASSERT(index < BS_NR_OF_CELL_BLOCKS_PER_STRING);

    return cellVoltages[index];
}
```

### SA-007: Multi-Dimensional Array
```c
int16_t GetVoltage(uint16_t stringIdx, uint16_t cellIdx) {
    /* Validate all dimensions */
    FAS_ASSERT(stringIdx < BS_NR_OF_STRINGS);
    FAS_ASSERT(cellIdx < BS_NR_OF_CELL_BLOCKS_PER_STRING);

    return data[stringIdx].voltage[cellIdx];
}
```

## State Validation

### SA-008: State Machine Validation
```c
void BMS_SetState(BMS_STATE_e newState) {
    /* Validate state is within enum range */
    FAS_ASSERT((uint8_t)newState < BMS_STATE_COUNT);

    /* Validate state transition is allowed */
    FAS_ASSERT(BMS_IsTransitionAllowed(bms_state.current, newState) == true);

    bms_state.current = newState;
}
```

### SA-009: Initialization Check
```c
void BMS_Process(void) {
    /* Ensure module is initialized before processing */
    FAS_ASSERT(bms_state.initialized == true);

    /* Safe to proceed */
}
```

## Return Value Validation

### SA-010: Function Return Validation
```c
void ProcessData(void) {
    STD_RETURN_TYPE_e result = DATA_Read();

    /* Validate critical function succeeded */
    FAS_ASSERT(result == STD_OK);

    /* Continue with valid data */
}
```

### SA-011: OS Function Validation
```c
void TaskFunction(void) {
    OS_RETURN_e osResult = OS_ReceiveFromQueue(queue, &message, timeout);

    /* For critical operations, assert success */
    FAS_ASSERT(osResult == OS_SUCCESS);
}
```

## ASIL-Level Assertions

### SA-012: ASIL-B Critical Path
```c
/**
 * @brief   ASIL-B critical voltage validation
 * @param   voltage_mV Measured cell voltage
 * @asil    ASIL-B
 */
void DIAG_ValidateVoltage_ASILB(int16_t voltage_mV) {
    /* Primary check - must pass */
    FAS_ASSERT(voltage_mV >= BMS_VOLTAGE_MIN_mV);
    FAS_ASSERT(voltage_mV <= BMS_VOLTAGE_MAX_mV);

    /* Plausibility check - ASIL requirement */
    FAS_ASSERT(voltage_mV > BMS_VOLTAGE_IMPLAUSIBLE_LOW_mV);
}
```

### SA-013: Safety-Critical Calculation
```c
/**
 * @brief   ASIL-B SOC calculation validation
 * @asil    ASIL-B
 */
void SOC_Calculate(void) {
    /* Pre-condition: inputs must be valid */
    FAS_ASSERT(soc_inputData.valid == true);

    /* Calculation */
    int32_t result = /* ... */;

    /* Post-condition: result must be in range */
    FAS_ASSERT((result >= 0) && (result <= 10000));  /* 0-100.00% */
}
```

## Combined Validation Patterns

### SA-014: Complete Function Entry Validation
```c
STD_RETURN_TYPE_e BMS_WriteData(
    const DATA_BLOCK_s* pData,
    uint16_t stringIndex,
    uint16_t cellIndex
) {
    STD_RETURN_TYPE_e result = STD_NOT_OK;

    /* 1. Pointer validation */
    FAS_ASSERT(pData != NULL);

    /* 2. Index validation */
    FAS_ASSERT(stringIndex < BS_NR_OF_STRINGS);
    FAS_ASSERT(cellIndex < BS_NR_OF_CELL_BLOCKS_PER_STRING);

    /* 3. State validation (if required) */
    FAS_ASSERT(bms_state.initialized == true);

    /* Safe to proceed */
    /* ... */

    return result;
}
```

### SA-015: Interrupt-Safe Assertion
```c
void ISR_CriticalHandler(void) {
    /* In ISR context, keep assertions minimal */
    FAS_ASSERT(pIsrData != NULL);

    /* Quick validation and exit */
}
```

## foxBMS Diagnostic Integration

### SA-016: Diagnostic with FAS_ASSERT
```c
void CheckSafetyCondition(void) {
    if (criticalError == true) {
        /* Log diagnostic event first */
        DIAG_Handler(DIAG_ID_CRITICAL_ERROR, DIAG_EVENT_NOT_OK, DIAG_SYSTEM, 0u);

        /* Then assert for stack trace */
        FAS_ASSERT(FAS_TRAP);
    }
}
```

## Summary Table

| ID | Pattern | Use Case | ASIL |
|----|---------|----------|------|
| SA-001 | Basic FAS_ASSERT | General validation | QM-D |
| SA-002 | FAS_TRAP | Unreachable code | QM-D |
| SA-003 | Pointer validation | Function entry | QM-D |
| SA-004 | Double pointer | Complex pointers | QM-D |
| SA-005 | Range validation | Parameter bounds | QM-D |
| SA-006 | Array index | Before access | QM-D |
| SA-007 | Multi-dim array | Matrix access | QM-D |
| SA-008 | State machine | State changes | B-D |
| SA-009 | Initialization | Before use | B-D |
| SA-010 | Return value | Critical calls | B-D |
| SA-011 | OS functions | RTOS calls | B-D |
| SA-012 | ASIL-B critical | Safety paths | B |
| SA-013 | Calculation | Safety calcs | B |
| SA-014 | Complete entry | Full validation | B-D |
| SA-015 | ISR-safe | Interrupt context | B-D |
| SA-016 | With diagnostic | Error handling | B-D |

## Best Practices

1. **Place assertions at function entry** - Fail fast principle
2. **Validate all pointer parameters** - Prevent NULL dereference
3. **Check array bounds before access** - Prevent buffer overflow
4. **Use FAS_TRAP for unreachable code** - Document impossible states
5. **Combine with DIAG_Handler** - Log before assert for diagnostics
6. **Keep ISR assertions minimal** - Timing constraints
7. **Document ASIL level** - For safety traceability
