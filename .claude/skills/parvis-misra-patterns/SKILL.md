---
name: parvis-misra-patterns
description: MISRA C:2012 compliant code patterns for foxBMS BMS development. Use when writing safety-critical embedded C code, validating MISRA compliance, or generating code with FAS_ASSERT safety checks.
---

# PARVIS MISRA C:2012 Patterns

MISRA C:2012 compliant code patterns for foxBMS Battery Management System with FAS_ASSERT integration.

## Quick Start

**Essential Pattern - FAS_ASSERT Pointer Check:**
```c
FAS_ASSERT(pParameter != NULL);  /* Rule 11.9 */
```

**Essential Pattern - Unsigned Literal:**
```c
#define BUFFER_SIZE (256u)  /* Rule 7.2 */
```

**Essential Pattern - Switch Default:**
```c
default:
    FAS_ASSERT(FAS_TRAP);  /* Rule 16.4 */
    break;
```

## Top 10 Essential Patterns

| ID | Rule | Pattern | Anti-Pattern |
|----|------|---------|--------------|
| PV-001 | 11.9 | `if (ptr != NULL)` | `if (ptr)` |
| PV-002 | 11.9 | `FAS_ASSERT(p != NULL)` | `assert(p)` |
| LT-001 | 7.2 | `100u` | `100` |
| CF-001 | 16.4 | `default: FAS_ASSERT(FAS_TRAP)` | missing default |
| CF-002 | 15.5 | single return | multiple returns |
| TS-001 | 10.3 | `(uint8_t)val` | implicit cast |
| DC-001 | 8.7 | `static` for file-scope | extern by default |
| FN-001 | 8.13 | `const uint8_t*` | `uint8_t*` |
| EX-001 | 14.4 | `if (flag == true)` | `if (flag)` |
| AR-001 | 18.1 | bounds check first | direct access |

## Reference Files

For detailed patterns by category:

- **[Pointer Patterns](reference/pointer-patterns.md)** - 20 patterns for pointer validation (Rules 11.x, 18.x)
- **[Control Flow](reference/control-flow.md)** - 20 patterns for control structures (Rules 15.x, 16.x)
- **[Type Safety](reference/type-safety.md)** - 15 patterns for type handling (Rules 10.x, 7.x)
- **[Declarations](reference/declarations.md)** - 15 patterns for declarations (Rules 8.x)
- **[Safety Assertions](reference/safety-assertions.md)** - FAS_ASSERT patterns for foxBMS

## Usage Examples

**Function with full MISRA compliance:**
```c
STD_RETURN_TYPE_e BMS_GetCellVoltage(
    uint16_t stringIndex,
    uint16_t cellIndex,
    int16_t* pVoltage_mV
) {
    STD_RETURN_TYPE_e result = STD_NOT_OK;

    /* PV-002: Pointer validation */
    FAS_ASSERT(pVoltage_mV != NULL);

    /* AR-001: Bounds check */
    if ((stringIndex < BS_NR_OF_STRINGS) &&
        (cellIndex < BS_NR_OF_CELL_BLOCKS_PER_STRING)) {

        *pVoltage_mV = data_cellVoltage[stringIndex].cellVoltage_mV[cellIndex];
        result = STD_OK;
    }

    /* CF-002: Single return */
    return result;
}
```

## Works Well With

- `parvis-code-templates` - Code generation with MISRA compliance
- `parvis-id-conventions` - Requirement ID formatting
- `parvis-aicoder-misra` agent - Automated MISRA checking

---
Version: 1.0.0 | Compliance: MISRA C:2012, ISO 26262-6
