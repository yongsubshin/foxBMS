# Requirement ID System

Complete requirement ID naming convention for foxBMS.

## Base Format

```
[PROJECT]-[TYPE]-[MODULE]-[SEQ]
```

**Example:** `FBMS-SWE-BMS-001`

## Project Identifier

| Code | Project |
|------|---------|
| FBMS | foxBMS (Battery Management System) |

## Requirement Type Codes

### System Level (ISO 26262 Part 3)

| Code | Name | Description |
|------|------|-------------|
| SYS | System Requirement | Top-level system requirements |
| FSR | Functional Safety Requirement | Safety-related functional requirements |
| TSC | Technical Safety Concept | Technical safety measures |

### Software Level (ISO 26262 Part 6)

| Code | Name | Description |
|------|------|-------------|
| SWE | Software Requirement | Functional software requirements |
| ARC | Architecture Requirement | Software architecture requirements |
| DES | Design Requirement | Detailed design requirements |
| HSI | HW-SW Interface | Interface requirements |

### Hardware Level (ISO 26262 Part 5)

| Code | Name | Description |
|------|------|-------------|
| HWE | Hardware Requirement | Hardware component requirements |

### Verification (ISO 26262 Part 6)

| Code | Name | Description |
|------|------|-------------|
| TST | Test Requirement | Verification requirements |

## Module Codes

### Application Layer

| Code | Module | Description |
|------|--------|-------------|
| BMS | Battery Management | Main state machine, system control |
| SOC | State of Charge | Charge estimation algorithm |
| SOE | State of Energy | Energy estimation |
| SOH | State of Health | Health monitoring |
| SOF | State of Function | Function availability |
| BAL | Cell Balancing | Active/passive balancing |
| SOA | Safe Operating Area | Operating limits monitoring |

### Engine Layer

| Code | Module | Description |
|------|--------|-------------|
| DB | Database | Shared data management |
| DIAG | Diagnostics | Error detection and handling |
| SYS | System | System state control |
| SYSM | System Monitor | Task monitoring |

### Driver Layer

| Code | Module | Description |
|------|--------|-------------|
| AFE | Analog Front End | Cell monitoring IC driver |
| CAN | CAN Communication | CAN interface driver |
| CONT | Contactor | Contactor control |
| IMD | Insulation Monitoring | Insulation monitoring device |
| TS | Temperature Sensor | Temperature measurement |
| CURR | Current Sensor | Current measurement |
| SBC | System Basis Chip | SBC driver |

### Configuration

| Code | Module | Description |
|------|--------|-------------|
| CFG | Configuration | System configuration |
| CELL | Cell Configuration | Battery cell parameters |

## Sequence Number Rules

1. **Format:** 3 digits (001-999)
2. **Allocation:** Sequential within module
3. **Reserved ranges:**
   - 001-099: Core requirements
   - 100-199: Extended requirements
   - 200-299: Safety requirements
   - 900-999: Test/debug requirements

## Complete Examples

### System Requirements
```
FBMS-SYS-BMS-001  System shall manage battery state
FBMS-SYS-BMS-002  System shall monitor cell voltages
```

### Safety Requirements
```
FBMS-FSR-BMS-001  System shall enter safe state on critical error
FBMS-FSR-DIAG-001 System shall detect cell overvoltage within 100ms
FBMS-TSC-CONT-001 Contactors shall open on isolation fault
```

### Software Requirements
```
FBMS-SWE-SOC-001  SOC algorithm shall use Coulomb counting
FBMS-SWE-SOC-002  SOC shall be updated every 100ms
FBMS-SWE-AFE-001  AFE driver shall read all cell voltages
```

### Design Requirements
```
FBMS-DES-SOC-001  SOC calculation shall use fixed-point math
FBMS-DES-BMS-001  State machine shall have 5 states
```

### Interface Requirements
```
FBMS-HSI-CAN-001  CAN message 0x100 shall contain cell voltages
FBMS-HSI-AFE-001  SPI clock shall be max 1MHz
```

## Traceability in Code

Use `@req` Doxygen tag:

```c
/**
 * @brief   Calculate state of charge
 * @req     FBMS-SWE-SOC-001
 * @req     FBMS-SWE-SOC-002
 */
void SOC_Calculate(void);
```

## ID Registry

IDs are tracked in `.claude/parvis-data/config/id-registry.json`:

```json
{
  "project": "FBMS",
  "modules": {
    "BMS": {"next_swe": 15, "next_fsr": 5},
    "SOC": {"next_swe": 8, "next_des": 3}
  }
}
```
