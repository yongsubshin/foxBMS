---
name: parvis-id-conventions
description: foxBMS requirement and artifact ID naming conventions following ISO 26262 and ASPICE standards. Use when creating requirement IDs, test case IDs, design IDs, or work product references.
---

# PARVIS ID Naming Conventions

Standardized ID naming system for foxBMS BMS development following ISO 26262 and ASPICE.

## Quick Reference

**Requirement ID:** `FBMS-SWE-BMS-001`
**Test Case ID:** `FBMS-TC-UT-BMS-001`
**Design ID:** `FBMS-DES-SOC-001`
**Work Product:** `FBMS-WP-SWE1-001`

## ID Format

```
[PROJECT]-[TYPE]-[MODULE]-[SEQ]
    │        │       │       │
    │        │       │       └── 3-digit sequence (001-999)
    │        │       └────────── Module code (BMS, SOC, AFE...)
    │        └────────────────── Type code (SWE, TST, DES...)
    └─────────────────────────── Project (FBMS for foxBMS)
```

## Type Codes

| Code | Full Name | ISO 26262 |
|------|-----------|-----------|
| SYS | System Requirement | Part 3 |
| SWE | Software Requirement | Part 6 |
| HWE | Hardware Requirement | Part 5 |
| TSC | Technical Safety Concept | Part 4 |
| FSR | Functional Safety Requirement | Part 3 |
| HSI | Hardware-Software Interface | Part 6 |
| ARC | Architecture Requirement | Part 6 |
| DES | Design Requirement | Part 6 |
| TST | Test Requirement | Part 6 |

## Module Codes

| Code | Module | Layer |
|------|--------|-------|
| BMS | Battery Management System | Application |
| SOC | State of Charge | Application |
| SOE | State of Energy | Application |
| SOH | State of Health | Application |
| BAL | Cell Balancing | Application |
| AFE | Analog Front End | Driver |
| CAN | CAN Communication | Driver |
| DIAG | Diagnostics | Engine |
| CONT | Contactor Control | Driver |
| IMD | Insulation Monitoring | Driver |

## Reference Files

- **[Requirement IDs](reference/requirement-ids.md)** - Full requirement ID system
- **[Test Case IDs](reference/test-case-ids.md)** - Unit, integration, system tests
- **[ASPICE Work Products](reference/aspice-ids.md)** - ASPICE work product IDs

## Examples

```
FBMS-SWE-DIAG-001  → Software requirement for diagnostics
FBMS-FSR-BMS-015   → Functional safety requirement
FBMS-TC-UT-SOC-003 → Unit test for State of Charge
FBMS-WP-SWE1-001   → ASPICE SWE.1 work product
```

## Works Well With

- `parvis-misra-patterns` - Code with requirement traceability
- `parvis-code-templates` - Generated code with `@req` tags
- `parvis-aidoc-trace` agent - Traceability matrix generation

---
Version: 1.0.0 | Compliance: ISO 26262-8, ASPICE PAM 3.1
