# Configuration Requirements Extraction Report

## Extraction Summary

| Metric | Value |
|--------|-------|
| Extraction Date | 2025-12-16 |
| Extractor | PARVIS-AISpec-Code |
| Total Requirements Extracted | 98 |
| High Confidence | 98 |
| Medium Confidence | 0 |
| Low Confidence | 0 |

## Source Directories

1. `/home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/application/config/`
2. `/home/kevin/work/forBMS/foxBMS/foxbms-2/src/app/driver/config/`

## Files Analyzed

### Application Configuration Files

| File | Requirements | Description |
|------|--------------|-------------|
| battery_cell_cfg.h | 13 | Cell voltage, temperature, and current limits (MSL/RSL/MOL) |
| battery_system_cfg.h | 25 | Pack configuration, timing, current sensor, open-wire check |
| bms_cfg.h | 19 | BMS state machine timing parameters |
| bal_cfg.h | 9 | Balancing configuration and thresholds |
| plausibility_cfg.h | 5 | Measurement plausibility tolerances |
| bms-slave_cfg.h | 4 | BMS-Slave hardware configuration |

### Driver Configuration Files

| File | Requirements | Description |
|------|--------------|-------------|
| spi_cfg.h | 4 | SPI interface configuration |
| can_cfg.h | 5 | CAN communication parameters |
| sps_cfg.h | 6 | Smart Power Switch configuration |
| interlock_cfg.h | 6 | Interlock circuit configuration |
| pex_cfg.h | 1 | Port expander configuration |
| dma_cfg.h | 1 | DMA channel configuration |
| tsi_plausibility_cfg.h | 2 | Temperature sensor plausibility limits |

## Requirements by Category

### Battery Cell Configuration (17 requirements)

Safety-critical cell limits defining the safe operating area:

- **Temperature Limits (8 requirements)**
  - Maximum/minimum temperature during discharge (MSL/RSL/MOL)
  - Maximum/minimum temperature during charge (MSL/RSL/MOL)

- **Voltage Limits (5 requirements)**
  - Maximum cell voltage (MSL/RSL/MOL): 2800/2750/2720 mV
  - Minimum cell voltage (MSL/RSL/MOL): 1500/1550/1580 mV
  - Deep-discharge voltage: 1500 mV
  - Nominal voltage: 2500 mV

- **Current Limits (2 requirements)**
  - Maximum discharge current: 180000 mA (MSL)
  - Maximum charge current: 180000 mA (MSL)

- **Cell Characteristics (2 requirements)**
  - Cell capacity: 3500 mAh
  - Cell energy: 10.0 Wh

### Battery System Configuration (26 requirements)

Pack-level configuration parameters:

- **Pack Topology (6 requirements)**
  - Number of strings: 1
  - Modules per string: 1
  - Cell blocks per module: 18
  - Parallel cells per block: 1
  - Temperature sensors per module: 8
  - Contactors: 2 per string + 1 precharge

- **Current Sensor (4 requirements)**
  - Presence flag: enabled
  - Response timeout: 200 ms
  - Coulomb counting timeout: 2000 ms
  - Energy counting timeout: 2000 ms

- **Safety Limits (6 requirements)**
  - Maximum break current: 3500 mA
  - Maximum fuse trigger duration: 3000 ms
  - Maximum string current: 2400 mA
  - Maximum pack current: 2400 mA x strings
  - Maximum voltage drop over fuse: 500 mV
  - Rest current threshold: 200 mA

- **Open-Wire Check (4 requirements)**
  - Standby mode check: disabled
  - Normal mode check: disabled
  - Charge mode check: disabled
  - Error mode period: 30000 ms

### BMS Timing Configuration (18 requirements)

State machine timing parameters:

- **Basic Timing (3 requirements)**
  - Task cycle: 10 ms
  - Short time: 1 trigger call
  - Medium time: 5 trigger calls
  - Long time: 10 trigger calls

- **Contactor Timing (8 requirements)**
  - Wait after closing string contactor: 200 ms
  - Wait after opening string contactor: 100 ms
  - Wait between closing strings: 100 ms
  - String close timeout: 5000 ms
  - String open timeout: 10000 ms
  - Precharge close timeout: 5000 ms
  - Precharge open timeout: 5000 ms

- **Precharge Parameters (5 requirements)**
  - Wait after closing precharge: 2000 ms
  - Wait after opening precharge: 500 ms
  - Voltage threshold: 1000 mV
  - Current threshold: 50 mA
  - Number of tries: 3

### Balancing Configuration (7 requirements)

Cell balancing control parameters:

- Default threshold: 200 mV
- Maximum threshold: 5000 mV
- Minimum threshold: 0 mV
- Hysteresis: 200 mV
- Lower voltage limit: 2000 mV
- Upper temperature limit: 70.0 degC
- Balancing time: 1 second per cycle

### Plausibility Configuration (5 requirements)

Measurement validation tolerances:

- String voltage tolerance: 3000 mV
- Cell voltage tolerance: 10 mV
- Cell temperature tolerance: 5.0 K
- Cell voltage spread tolerance: 300 mV
- Cell temperature spread tolerance: 10.0 K

### Driver Configuration (23 requirements)

Low-level driver parameters for SPI, CAN, SPS, Interlock, etc.

## Safety Classification Summary

| Classification | Count | Percentage |
|---------------|-------|------------|
| Safety | 24 | 24.5% |
| Functional | 62 | 63.3% |
| Constraint | 12 | 12.2% |

## Key Safety Requirements

The following requirements have direct safety implications (MSL violations trigger error state and contactor opening):

1. **CFG-APP-001 to CFG-APP-004**: Temperature limits during charge/discharge
2. **CFG-APP-005, CFG-APP-007**: Maximum/minimum cell voltage limits
3. **CFG-APP-008**: Deep-discharge voltage limit
4. **CFG-APP-009, CFG-APP-010**: Maximum discharge/charge current limits
5. **CFG-APP-024**: Maximum contactor break current
6. **CFG-APP-026, CFG-APP-027**: Maximum string/pack current limits
7. **CFG-APP-046, CFG-APP-047**: String close/open timeout
8. **CFG-APP-048, CFG-APP-049**: String voltage/current limits for closing
9. **CFG-APP-052**: Oscillation timeout protection
10. **CFG-APP-065, CFG-APP-066**: Balancing voltage/temperature limits

## Extraction Patterns Used

1. **Doxygen Define Extraction**: Extracted parameter values from `#define` macros with Doxygen comments containing `@brief`, `@details`, `@ptype`, `@unit`

2. **Static Assert Extraction**: Identified compile-time constraints from `#if` preprocessor checks and `FAS_STATIC_ASSERT` macros

3. **Range Documentation**: Captured valid ranges from `\par Range:` Doxygen annotations

4. **Unit Information**: Extracted units from macro suffixes (e.g., `_mV`, `_mA`, `_ms`, `_ddegC`)

## Recommendations

### High Priority Review Items

1. **Current Limits Verification**: The discharge/charge current limits (180A) should be verified against actual cell specifications
2. **Temperature Thresholds**: Verify temperature limits match cell datasheet specifications
3. **Timing Parameters**: Review state machine timing for specific application requirements

### Configuration Consistency Checks

1. Verify `BC_VOLTAGE_MIN_MSL_mV` equals `BC_VOLTAGE_DEEP_DISCHARGE_mV` (enforced by static assert)
2. Verify `BS_NR_OF_TEMP_SENSORS_PER_MODULE` does not exceed `SLV_NR_OF_GPIOS_PER_MODULE`
3. Verify `SPS_NR_OF_REQUIRED_CONTACTOR_CHANNELS` does not exceed `SPS_NR_OF_AVAILABLE_SPS_CHANNELS`

### Missing Documentation

The following files have incomplete documentation (marked with `@details TODO`):
- soa_cfg.h
- bms_cfg.h
- bal_cfg.h
- plausibility_cfg.h
- contactor_cfg.h
- can_cfg.h
- spi_cfg.h
- fram_cfg.h
- sps_cfg.h
- interlock_cfg.h
- pex_cfg.h
- dma_cfg.h
- tsi_plausibility_cfg.h

## Output Files

| File | Description |
|------|-------------|
| config-extracted.json | Machine-readable extracted requirements |
| config-extraction-report.md | This human-readable report |

## Next Steps

1. **Requirement ID Assignment**: Use parvis-aispec-reqid to assign formal requirement IDs
2. **Normalization**: Use parvis-aispec-transformer to convert to EARS format
3. **Traceability**: Use parvis-aispec-trace to link requirements to implementation code
4. **Review**: Human review of extracted requirements for accuracy and completeness

---

Generated by PARVIS-AISpec-Code
foxBMS Configuration Module Extraction
