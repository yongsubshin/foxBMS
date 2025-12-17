---
name: parvis-code-templates
description: Jinja2 code generation templates for foxBMS BMS development. Use when generating MISRA-compliant C code for state machines, configurations, APIs, or safety assertions.
---

# PARVIS Code Generation Templates

Jinja2-based code generation templates for producing MISRA C:2012 compliant embedded C code for foxBMS Battery Management System.

## Quick Start

**Generate State Machine:**
```python
template = env.get_template('state-machine/enum-template.c.jinja')
output = template.render(prefix='BMS', states=[...])
```

## Available Templates

| Template | Purpose | MISRA Features |
|----------|---------|----------------|
| `enum-template.c.jinja` | State enumerations | Unsigned values, validation |
| `transition-template.c.jinja` | State transitions | Switch defaults, FAS_ASSERT |
| `define-template.c.jinja` | Configuration headers | `u` suffix, Doxygen |
| `api-template.c.jinja` | API interfaces | Const params, prototypes |
| `assertion-template.c.jinja` | Safety assertions | FAS_ASSERT, ASIL markers |

## Template Input Format

**Basic Schema:**
```json
{
  "filename": "bms_state.c",
  "prefix": "BMS",
  "requirement_id": "FBMS-SWE-BMS-001",
  "asil_level": "ASIL-B"
}
```

## Reference Files

For detailed template documentation:

- **[State Machine Templates](reference/state-machine.md)** - enum and transition templates
- **[Configuration Templates](reference/configuration.md)** - define and header templates
- **[API Templates](reference/api-interface.md)** - function prototypes and error handling
- **[Safety Templates](reference/safety.md)** - FAS_ASSERT and ASIL templates

## Generated Code Example

**Input:**
```json
{
  "prefix": "BMS",
  "states": [
    {"name": "INIT", "value": 0},
    {"name": "IDLE", "value": 1}
  ]
}
```

**Output:**
```c
typedef enum {
    BMS_STATE_INIT = 0u,
    BMS_STATE_IDLE = 1u
} BMS_STATE_e;

#define BMS_NUMBER_OF_STATES (2u)
```

## MISRA Compliance

All templates automatically include:
- Unsigned literals (`u` suffix)
- Explicit type casts
- FAS_ASSERT for pointer validation
- Switch default cases
- Doxygen documentation
- Requirement traceability tags

## Works Well With

- `parvis-misra-patterns` - MISRA compliance rules
- `parvis-id-conventions` - Requirement ID format
- `parvis-aicoder-safety` agent - Safety code generation

---
Version: 1.0.0 | Template Engine: Jinja2
