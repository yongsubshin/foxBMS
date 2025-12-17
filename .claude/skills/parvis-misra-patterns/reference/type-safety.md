# Type Safety Patterns

MISRA C:2012 Rules 10.x, 7.x - Type handling for foxBMS.

## Integer Literal Patterns

### TS-001: Unsigned Integer Suffix (Rule 7.2)
```c
/* CORRECT */
#define BUFFER_SIZE     (256u)
#define MAX_VOLTAGE_mV  (4200u)
uint32_t counter = 0u;
uint16_t index = 100u;

/* WRONG */
#define BUFFER_SIZE     (256)
#define MAX_VOLTAGE_mV  (4200)
uint32_t counter = 0;
```
**Rationale:** Prevents unintended signed arithmetic.

### TS-002: Hexadecimal Suffix (Rule 7.2)
```c
/* CORRECT */
uint32_t mask = 0xFFFFu;
uint8_t flags = 0x80u;

/* WRONG */
uint32_t mask = 0xFFFF;
uint8_t flags = 0x80;
```

### TS-003: Long Suffix (Rule 7.2)
```c
/* CORRECT */
uint32_t bigValue = 100000uL;
int64_t timestamp = 1234567890LL;

/* WRONG */
uint32_t bigValue = 100000;
```

## Type Conversion Patterns

### TS-004: Explicit Type Cast (Rule 10.3)
```c
/* CORRECT */
uint8_t narrowValue = (uint8_t)wideValue;
int16_t signedVal = (int16_t)unsignedVal;

/* WRONG - implicit narrowing */
uint8_t narrowValue = wideValue;
```
**Rationale:** Makes narrowing conversions explicit and intentional.

### TS-005: Signed/Unsigned Conversion (Rule 10.4)
```c
/* CORRECT */
int16_t signedTemp = -10;
uint16_t unsignedVal = (signedTemp >= 0) ? (uint16_t)signedTemp : 0u;

/* WRONG - direct assignment */
uint16_t unsignedVal = signedTemp;  /* Negative becomes large positive */
```

### TS-006: Arithmetic Type Matching (Rule 10.4)
```c
/* CORRECT - same types */
uint32_t a = 100u;
uint32_t b = 200u;
uint32_t sum = a + b;

/* WRONG - mixed types */
uint32_t a = 100u;
int32_t b = -50;
uint32_t result = a + b;  /* Mixed signedness */
```

### TS-007: Shift Operation Types (Rule 12.2)
```c
/* CORRECT */
uint32_t result = 1u << bitPosition;
uint8_t mask = (uint8_t)(1u << 3u);

/* WRONG */
uint32_t result = 1 << bitPosition;  /* Signed shift */
```

## Boolean Patterns

### TS-008: Explicit Boolean Comparison (Rule 14.4)
```c
/* CORRECT */
if (isEnabled == true) {
    /* action */
}
if (count != 0u) {
    /* action */
}

/* WRONG */
if (isEnabled) {
    /* action */
}
if (count) {
    /* action */
}
```

### TS-009: Boolean Assignment (Rule 14.4)
```c
/* CORRECT */
bool isValid = (value < MAX_VALUE);
bool hasError = (errorCount != 0u);

/* WRONG */
bool isValid = value < MAX_VALUE;  /* OK but explicit is better */
```

### TS-010: Boolean Return (Rule 14.4)
```c
/* CORRECT */
bool IsInRange(uint32_t value) {
    bool result = false;
    if ((value >= MIN_VALUE) && (value <= MAX_VALUE)) {
        result = true;
    }
    return result;
}

/* Alternative - direct comparison OK */
bool IsInRange(uint32_t value) {
    return ((value >= MIN_VALUE) && (value <= MAX_VALUE));
}
```

## Enum Patterns

### TS-011: Enum Type Usage (Rule 10.3)
```c
/* CORRECT */
typedef enum {
    STATE_INIT = 0u,
    STATE_IDLE = 1u,
    STATE_RUN  = 2u
} STATE_e;

STATE_e currentState = STATE_INIT;

/* WRONG - integer assignment */
STATE_e currentState = 0;  /* Use enum constant */
```

### TS-012: Enum Value Specification (Rule 10.1)
```c
/* CORRECT - explicit values */
typedef enum {
    ERROR_NONE     = 0u,
    ERROR_TIMEOUT  = 1u,
    ERROR_OVERFLOW = 2u,
    ERROR_COUNT    = 3u  /* For array sizing */
} ERROR_e;

/* WRONG - implicit values */
typedef enum {
    ERROR_NONE,
    ERROR_TIMEOUT,
    ERROR_OVERFLOW
} ERROR_e;
```

## foxBMS Specific Types

### TS-013: Voltage Type (int16_t)
```c
/* foxBMS uses int16_t for voltage in mV */
int16_t cellVoltage_mV = 3700;  /* Signed for calculations */

/* Validation with explicit cast */
if ((cellVoltage_mV >= (int16_t)BMS_VOLTAGE_MIN_mV) &&
    (cellVoltage_mV <= (int16_t)BMS_VOLTAGE_MAX_mV)) {
    /* Valid voltage */
}
```

### TS-014: Temperature Type (int16_t)
```c
/* foxBMS uses int16_t for temperature in deci-degrees Celsius */
int16_t temperature_ddegC = 250;  /* 25.0 degrees */

/* Negative temperatures supported */
int16_t coldTemp_ddegC = -100;  /* -10.0 degrees */
```

### TS-015: Index Type (uint16_t)
```c
/* foxBMS uses uint16_t for indices */
for (uint16_t i = 0u; i < BS_NR_OF_CELL_BLOCKS_PER_STRING; i++) {
    /* Process cell */
}
```

## Summary Table

| ID | Rule | Pattern | Severity |
|----|------|---------|----------|
| TS-001 | 7.2 | Unsigned suffix `u` | Required |
| TS-002 | 7.2 | Hex suffix `u` | Required |
| TS-003 | 7.2 | Long suffix `L` | Required |
| TS-004 | 10.3 | Explicit cast | Required |
| TS-005 | 10.4 | Signed/unsigned care | Required |
| TS-006 | 10.4 | Type matching | Required |
| TS-007 | 12.2 | Unsigned shifts | Required |
| TS-008 | 14.4 | Explicit bool compare | Advisory |
| TS-009 | 14.4 | Bool assignment | Advisory |
| TS-010 | 14.4 | Bool return | Advisory |
| TS-011 | 10.3 | Enum constants | Required |
| TS-012 | 10.1 | Explicit enum values | Advisory |
