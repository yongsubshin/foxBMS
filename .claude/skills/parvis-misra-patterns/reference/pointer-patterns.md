# Pointer Validation Patterns

MISRA C:2012 Rules 11.x, 18.x - Pointer type conversions and validation for foxBMS.

## Pattern List

### PV-001: Null Pointer Check (Rule 11.9)
```c
/* CORRECT */
if (ptr != NULL) { /* safe to use */ }

/* WRONG */
if (ptr) { /* implicit conversion */ }
```
**Rationale:** Explicit comparison prevents implicit pointer-to-boolean conversion.

### PV-002: FAS_ASSERT Pointer Validation (Rule 11.9)
```c
/* CORRECT */
FAS_ASSERT(pParameter != NULL);

/* WRONG */
assert(pParameter);
```
**Rationale:** FAS_ASSERT provides consistent error handling across foxBMS.

### PV-003: Const Pointer Input Parameter (Rule 8.13)
```c
/* CORRECT */
void Function(const uint8_t* pData, uint32_t length);

/* WRONG */
void Function(uint8_t* pData, uint32_t length);
```
**Rationale:** Const correctness improves code safety and readability.

### PV-004: Pointer Arithmetic Bounds Check (Rule 18.1)
```c
/* CORRECT */
if ((index < arraySize) && (pArray != NULL)) {
    value = pArray[index];
}

/* WRONG */
value = pArray[index];
```
**Rationale:** Prevents buffer overflow vulnerabilities.

### PV-005: Void Pointer Cast (Rule 11.5)
```c
/* CORRECT - with documentation */
uint8_t* pData = (uint8_t*)pvMemory; /* Intentional: memory pool access */

/* WRONG - undocumented */
uint8_t* pData = pvMemory;
```
**Rationale:** Explicit cast documents intentional type conversion.

### PV-006: Function Pointer Validation (Rule 11.1)
```c
/* CORRECT */
if (pCallback != NULL) {
    pCallback(param);
}

/* WRONG */
pCallback(param);
```
**Rationale:** Prevents undefined behavior from null function pointers.

### PV-007: Pointer Return Value Check (Rule 11.9)
```c
/* CORRECT */
void* pMem = malloc(size);
if (pMem == NULL) {
    /* handle error */
}

/* WRONG */
void* pMem = malloc(size);
memset(pMem, 0, size);  /* potential NULL dereference */
```
**Rationale:** Prevents null pointer dereference on allocation failure.

### PV-008: Pointer to Integer Cast (Rule 11.4)
```c
/* CORRECT - use uintptr_t */
uintptr_t address = (uintptr_t)pRegister;

/* WRONG - size may not match */
uint32_t address = (uint32_t)pRegister;
```
**Rationale:** uintptr_t is guaranteed to hold pointer value.

### PV-009: Pointer Array Initialization (Rule 11.9)
```c
/* CORRECT */
static void* pointerArray[SIZE] = {NULL};

/* WRONG */
static void* pointerArray[SIZE];
```
**Rationale:** Uninitialized pointers have indeterminate values.

### PV-010: Double Pointer Validation
```c
/* CORRECT */
FAS_ASSERT(ppData != NULL);
FAS_ASSERT(*ppData != NULL);

/* WRONG - incomplete check */
FAS_ASSERT(ppData != NULL);
/* Missing *ppData check */
```
**Rationale:** Both levels of indirection must be validated.

## foxBMS Specific Patterns

### PV-011: Database Pointer Access
```c
/* CORRECT */
DATA_BLOCK_CELL_s* pCellData = DATA_GetTablePtr(DATA_BLOCK_ID_CELL_VOLTAGE);
FAS_ASSERT(pCellData != NULL);

/* Process data safely */
int16_t voltage = pCellData->cellVoltage_mV[0];
```

### PV-012: CAN Message Buffer Pointer
```c
/* CORRECT */
void CAN_ProcessMessage(const CAN_MESSAGE_s* pMessage) {
    FAS_ASSERT(pMessage != NULL);
    FAS_ASSERT(pMessage->pData != NULL);

    /* Safe to access message data */
}
```

### PV-013: State Machine Context Pointer
```c
/* CORRECT */
static BMS_STATE_s* pBmsState = NULL;

void BMS_Initialize(BMS_STATE_s* pState) {
    FAS_ASSERT(pState != NULL);
    pBmsState = pState;
}
```

## Summary Table

| ID | Rule | Pattern | Severity |
|----|------|---------|----------|
| PV-001 | 11.9 | Explicit NULL check | Required |
| PV-002 | 11.9 | FAS_ASSERT for params | Required |
| PV-003 | 8.13 | Const for input | Advisory |
| PV-004 | 18.1 | Bounds before access | Required |
| PV-005 | 11.5 | Document void casts | Advisory |
| PV-006 | 11.1 | Function ptr check | Required |
| PV-007 | 11.9 | Check return values | Required |
| PV-008 | 11.4 | Use uintptr_t | Advisory |
| PV-009 | 11.9 | Initialize to NULL | Required |
| PV-010 | 11.9 | Double ptr check | Required |
