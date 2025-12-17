# SBC Module Requirements Extraction Report

## Module Information

- **Module**: SBC (System Basis Chip)
- **Component**: NXP FS85xx MCU Supervisor Driver
- **Prefix**: SBC, FS85
- **Extraction Date**: 2025-12-16
- **foxBMS Version**: v1.10.0

## Source Files Analyzed

| File | Path | Purpose |
|------|------|---------|
| sbc.c | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/sbc.c | Main SBC state machine |
| sbc.h | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/sbc.h | SBC public interface |
| nxpfs85xx.c | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/nxpfs85xx.c | FS85xx device driver |
| nxpfs85xx.h | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/nxpfs85xx.h | FS85xx interface |
| sbc_fs8x.c | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/fs8x_driver/sbc_fs8x.c | NXP FS8x driver core |
| sbc_fs8x_communication.c | /home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/sbc/fs8x_driver/sbc_fs8x_communication.c | SPI/I2C communication |

## Extraction Summary

### Requirements by Type

| Type | Count | Description |
|------|-------|-------------|
| SWE | 18 | Software Engineering Requirements |
| FSR | 22 | Functional Safety Requirements |
| CFG | 10 | Configuration Requirements |
| HSI | 4 | Hardware-Software Interface Requirements |
| **Total** | **52** | |

### Requirements by Classification

| Classification | Count | Description |
|----------------|-------|-------------|
| safety | 22 | Safety-critical requirements |
| functional | 14 | Functional behavior requirements |
| constraint | 11 | Timing and configuration constraints |
| interface | 4 | Communication interface requirements |

### Requirements by Confidence Level

| Confidence | Count |
|------------|-------|
| high | 52 |
| medium | 0 |
| low | 0 |

### Extraction Methods Used

| Method | Count | Description |
|--------|-------|-------------|
| code_pattern | 25 | Patterns identified in source code |
| doxygen | 9 | Doxygen documentation comments |
| config | 9 | Configuration defines and constants |
| assertion | 4 | FAS_ASSERT safety assertions |
| state_machine | 3 | State machine definitions |

## Key Findings

### State Machine Architecture

The SBC module implements a hierarchical state machine with:

**Main States (SBC_STATEMACHINE_e)**:
- UNINITIALIZED: Initial state after power-on
- INITIALIZATION: Multi-phase FS85xx configuration
- RUNNING: Normal operation with watchdog servicing
- ERROR: Fault state after initialization failures

**Initialization Substates (SBC_STATEMACHINE_SUB_e)**:
- SBC_ENTRY: Entry point for each state
- SBC_INIT_RESET_FAULT_ERROR_COUNTER_PART1: Calculate required WD refreshes
- SBC_INIT_RESET_FAULT_ERROR_COUNTER_PART2: Verify fault counter cleared
- SBC_INITIALIZE_SAFETY_PATH_CHECK: RSTB and FS0B path verification

### Safety-Critical Features Identified

1. **Re-entrance Protection** (SBC-003, SBC-004)
   - OS critical sections protect triggerEntry counter
   - Prevents concurrent state machine execution

2. **Watchdog Management** (SBC-011 through SBC-013, SBC-043, SBC-044)
   - Configurable 100ms watchdog period (128ms window)
   - Good/bad refresh verification via GRL_FLAGS register
   - Fault error counter integration

3. **Safety Path Checks** (SBC-034 through SBC-038)
   - RSTB path verification for MCU reset capability
   - FS0B path verification for fail-safe output
   - FIN/RSTB short-circuit detection

4. **Built-In Self-Test Requirements** (SBC-017, SBC-029)
   - LBIST verification at startup
   - ABIST1 and ABIST2 verification
   - OTP CRC integrity check

5. **Fault Error Counter** (SBC-025, SBC-026, SBC-032)
   - Limit of 8 fault errors before reset
   - Cleared by consecutive good watchdog refreshes
   - Impacts both FS0B and RSTB on limit reach

### Communication Interface

1. **SPI Protocol** (SBC-047 through SBC-050)
   - 4-byte frame: CRC, Data LSB, Data MSB, Address/Command
   - CRC8 polynomial 0x1D with initial value 0xFF
   - Bidirectional CRC verification

2. **Register Protection** (SBC-021, SBC-050)
   - DATA and DATA_NOT (inverted) register pairs
   - Corruption detection via REG_CORRUPT monitoring

### Configuration Parameters Extracted

| Parameter | Value | Source |
|-----------|-------|--------|
| Task cycle time | 10ms | SBC_STATEMACHINE_TASK_CYCLE_CONTEXT_MS |
| Watchdog period | 100ms | SBC_WINDOW_WATCHDOG_PERIOD_MS |
| WD window | 128ms | FS8X_FS_WD_WINDOW_128MS |
| WD duty cycle | 50% | FS8X_FS_WDW_DC_50 |
| WD recovery | 128ms | FS8X_FS_WDW_RECOVERY_128MS |
| Fault error limit | 8 | FS8X_FS_I_FLT_ERR_CNT_LIMIT_8 |
| RSTB pulse | 10ms | FS8X_FS_I_RSTB_DUR_10MS |
| WD seed default | 0x5AB2 | FS8x_WD_SEED_DEFAULT |
| SPI frame size | 4 bytes | FS8x_COMM_FRAME_SIZE |
| CRC polynomial | 0x1D | FS8x_COM_CRC_POLYNOM |
| Max init retries | 3 | retryCounter > 3u |

## Assertion Analysis

### FAS_ASSERT Usage

All public and internal functions validate pointer parameters:

```
FAS_ASSERT(pInstance != NULL_PTR)  // 9 occurrences in sbc.c
FAS_ASSERT(pInstance != NULL_PTR)  // 12 occurrences in nxpfs85xx.c
FAS_ASSERT(FAS_TRAP)               // 2 trap assertions for invalid states
```

### FS_ASSERT Usage (NXP Driver)

The NXP driver uses FS_ASSERT for internal validation:
- Parameter pointer checks
- Data structure validation
- Frame buffer validation

## Diagnostic Integration

The SBC module integrates with foxBMS diagnostics:

| Diagnostic ID | Purpose |
|--------------|---------|
| DIAG_ID_SBC_FIN_ERROR | FIN/RSTB short-circuit detection |
| DIAG_ID_SBC_RSTB_ERROR | RSTB path check status |

## NVRAM/FRAM Integration

Persistent storage for power-cycle recovery:

| FRAM Entry | Purpose |
|------------|---------|
| FRAM_BLOCK_ID_SBC_INIT_STATE | SBC initialization phase |
| fram_sbcInit.phase | Current init phase |
| fram_sbcInit.finState | FIN pin status |

## Review Items

### Items Requiring Human Verification

1. **TODO Items in Code**:
   - Line 224 (sbc.c): "Do what if triggering of watchdog fails?"
   - Line 1104-1110 (nxpfs85xx.c): Bad watchdog notification handling

2. **Incomplete Implementations**:
   - FS85_PerformPathCheckFs0b() contains only "TBD" comment
   - Ignition shutdown handling discards return value

3. **Safety Analysis Required**:
   - Verify FTTI compliance with 128ms watchdog window
   - Validate fault error counter limit for safety concept
   - Review FS0B release preconditions against safety requirements

### Traceability Recommendations

1. Link SBC requirements to system-level safety requirements
2. Map diagnostic IDs to FMEA failure modes
3. Trace configuration parameters to hardware specifications
4. Link BIST requirements to ISO 26262 diagnostic coverage

## Output Files

- Requirements JSON: `/home/kevin/work/forBMS/foxBMS/.moai/bms/requirements/extracted/sbc-extracted.json`
- This report: `/home/kevin/work/forBMS/foxBMS/.moai/bms/requirements/extracted/sbc-extraction-report.md`

## Next Steps

1. **Requirement ID Assignment**: Use parvis-aispec-reqid agent to assign formal IDs
2. **Normalization**: Use parvis-aispec-transformer for EARS format conversion
3. **Traceability**: Link to system requirements and test cases
4. **Safety Analysis**: Classify requirements per ISO 26262 ASIL levels
