# Safety Assertion Templates

Templates for generating ASIL-compliant safety code for foxBMS.

## assertion-template.c.jinja

**Purpose:** Generate safety assertion functions with ASIL markers.

### Input Schema

```json
{
  "filename": "bms_safety.c",
  "prefix": "BMS",
  "module_name": "BMS Safety Checks",
  "asil_level": "ASIL-B",
  "requirement_id": "FBMS-FSR-BMS-001",
  "range_checks": [
    {
      "name": "CellVoltage",
      "type": "int32_t",
      "min": "2000",
      "max": "4500",
      "asil_level": "ASIL-B"
    },
    {
      "name": "Temperature",
      "type": "int16_t",
      "min": "-400",
      "max": "800",
      "asil_level": "ASIL-B"
    }
  ],
  "enum_checks": [
    {
      "name": "State",
      "type": "BMS_STATE_e",
      "valid_values": ["BMS_STATE_INIT", "BMS_STATE_IDLE", "BMS_STATE_RUN"]
    }
  ]
}
```

### Generated Output

```c
/**
 * @file    bms_safety.c
 * @brief   Safety assertion functions for BMS Safety Checks
 * @asil    ASIL-B
 * @req     FBMS-FSR-BMS-001
 */

/* ASIL Level Markers */
#define BMS_ASIL_QM  (0u)
#define BMS_ASIL_A   (1u)
#define BMS_ASIL_B   (2u)
#define BMS_ASIL_C   (3u)
#define BMS_ASIL_D   (4u)

/* MISRA C:2012 Compliant Assertion Macros */
#define BMS_ASSERT(condition) \
    do { \
        if ((condition) == false) { \
            FAS_ASSERT(FAS_TRAP); \
        } \
    } while (false)

/* Range Validation Functions */
bool BMS_ValidateCellvoltageRange(int32_t value) {
    bool isValid = false;
    if ((value >= (int32_t)2000) && (value <= (int32_t)4500)) {
        isValid = true;
    }
    return isValid;
}

void BMS_AssertCellvoltageRange(int32_t value) {
    FAS_ASSERT(BMS_ValidateCellvoltageRange(value) == true);
}

bool BMS_ValidateTemperatureRange(int16_t value) {
    bool isValid = false;
    if ((value >= (int16_t)-400) && (value <= (int16_t)800)) {
        isValid = true;
    }
    return isValid;
}

void BMS_AssertTemperatureRange(int16_t value) {
    FAS_ASSERT(BMS_ValidateTemperatureRange(value) == true);
}

/* Enum Validation Functions */
bool BMS_ValidateStateEnum(BMS_STATE_e value) {
    bool isValid = false;
    switch (value) {
        case BMS_STATE_INIT:
        case BMS_STATE_IDLE:
        case BMS_STATE_RUN:
            isValid = true;
            break;
        default:
            isValid = false;
            break;
    }
    return isValid;
}
```

### Template Variables

| Variable | Type | Description |
|----------|------|-------------|
| `prefix` | string | Module prefix |
| `asil_level` | string | Default ASIL level |
| `range_checks` | array | Range validation definitions |
| `range_checks[].name` | string | Check name |
| `range_checks[].type` | string | C data type |
| `range_checks[].min` | string | Minimum value |
| `range_checks[].max` | string | Maximum value |
| `enum_checks` | array | Enum validation definitions |

## ASIL Level Guidelines

| ASIL | Validation Type | Example |
|------|----------------|---------|
| QM | Basic null checks | `FAS_ASSERT(p != NULL)` |
| ASIL-A | Range validation | Min/max bounds |
| ASIL-B | Plausibility checks | Multi-signal validation |
| ASIL-C | Redundancy checks | Dual-channel comparison |
| ASIL-D | Full decomposition | Independent monitoring |

## Safety Check Patterns

### Pointer Validation (All ASIL)
```c
bool BMS_ValidatePointerNotNull(const void* ptr) {
    bool isValid = false;
    if (ptr != NULL) {
        isValid = true;
    }
    return isValid;
}
```

### Array Bounds (All ASIL)
```c
bool BMS_ValidateArrayBounds(uint32_t index, uint32_t arraySize) {
    bool isValid = false;
    if (index < arraySize) {
        isValid = true;
    }
    return isValid;
}
```

### Diagnostic Integration
```c
bool BMS_SafetyCheck_CellVoltage(int32_t voltage_mV) {
    bool isSafe = true;

    if (BMS_ValidateCellvoltageRange(voltage_mV) == false) {
        isSafe = false;
        DIAG_Handler(DIAG_ID_CELL_VOLTAGE_OOR,
                    DIAG_EVENT_NOT_OK, DIAG_SYSTEM, 0u);
    }

    return isSafe;
}
```
