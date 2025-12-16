# Algorithm Module Requirements Extraction Report

**Extraction Date:** 2025-12-16
**Source Directory:** `foxbms-2/src/app/application/algorithm/`
**Total Files Analyzed:** 24
**Total Requirements Extracted:** 84

---

## Executive Summary

This report documents the requirements extracted from the foxBMS Algorithm module family, which includes the algorithm manager, moving average calculations, and state estimation algorithms (SOC, SOE, SOH, SOF).

### Quality Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Requirements | 84 | - | - |
| High Confidence | 84 (100%) | 70%+ | PASS |
| Medium Confidence | 0 (0%) | - | - |
| Low Confidence | 0 (0%) | - | - |

---

## Extraction Statistics

### By Requirement Type

| Type | Count | Percentage | Description |
|------|-------|------------|-------------|
| SWE | 47 | 56.0% | Software Engineering Requirements |
| FSR | 16 | 19.0% | Functional Safety Requirements |
| CFG | 21 | 25.0% | Configuration Requirements |
| HSI | 0 | 0.0% | Hardware-Software Interface |

### By Classification

| Classification | Count | Percentage |
|---------------|-------|------------|
| Functional | 40 | 47.6% |
| Constraint | 17 | 20.2% |
| Safety | 16 | 19.0% |
| Interface | 11 | 13.1% |

### By Module

| Module | Count | Description |
|--------|-------|-------------|
| algorithm/sof | 33 | State of Function (current derating) |
| algorithm/soc | 14 | State of Charge calculation |
| algorithm/soe | 12 | State of Energy calculation |
| algorithm/manager | 10 | Algorithm execution management |
| algorithm/moving_average | 5 | Moving average calculations |
| algorithm/state_estimation | 4 | State estimation wrapper |
| algorithm/soh | 4 | State of Health calculation |
| algorithm/config | 2 | Algorithm configuration |

### By Extraction Pattern

| Pattern | Count | Description |
|---------|-------|-------------|
| Interface | 35 | Function signatures and data flow |
| Config | 22 | #define and configuration values |
| Assertion | 14 | FAS_ASSERT safety checks |
| Doxygen | 12 | Documentation comments |
| State Machine | 1 | Enum state definitions |

---

## Files Analyzed

### Main Algorithm Manager
- `algorithm.h` - Algorithm module header
- `algorithm.c` - Algorithm execution handler
- `config/algorithm_cfg.h` - Algorithm configuration header
- `config/algorithm_cfg.c` - Algorithm configuration implementation

### Moving Average
- `moving_average/moving_average.h` - Moving average header
- `moving_average/moving_average.c` - Moving average implementation

### State Estimation Wrapper
- `state_estimation/state_estimation.h` - State estimation API
- `state_estimation/state_estimation.c` - State estimation wrapper

### SOC (State of Charge)
- `state_estimation/soc/counting/soc_counting.c` - Coulomb counting implementation
- `state_estimation/soc/counting/soc_counting_cfg.h` - SOC configuration
- `state_estimation/soc/debug/soc_debug.c` - Debug variant
- `state_estimation/soc/none/soc_none.c` - No-op variant

### SOE (State of Energy)
- `state_estimation/soe/counting/soe_counting.c` - Energy counting implementation
- `state_estimation/soe/counting/soe_counting_cfg.h` - SOE configuration
- `state_estimation/soe/debug/soe_debug.c` - Debug variant
- `state_estimation/soe/debug/soe_debug_cfg.h` - Debug configuration
- `state_estimation/soe/none/soe_none.c` - No-op variant
- `state_estimation/soe/none/soe_none_cfg.h` - No-op configuration

### SOH (State of Health)
- `state_estimation/soh/debug/soh_debug.c` - Debug variant
- `state_estimation/soh/none/soh_none.c` - No-op variant

### SOF (State of Function)
- `state_estimation/sof/trapezoid/sof_trapezoid.h` - SOF header
- `state_estimation/sof/trapezoid/sof_trapezoid.c` - Trapezoid derating implementation
- `state_estimation/sof/trapezoid/sof_trapezoid_cfg.h` - SOF configuration header
- `state_estimation/sof/trapezoid/sof_trapezoid_cfg.c` - SOF configuration values

---

## Key Findings

### Algorithm Manager Architecture

1. **State Machine Design**: The algorithm module implements a well-defined state machine with states: UNINITIALIZED, READY, RUNNING, BLOCKED, FAILED_INIT, and REINIT_REQUESTED.

2. **Cycle Time Enforcement**: Algorithms must have cycle times that are multiples of the 100ms base tick (ALGO_TICK_ms).

3. **Runtime Monitoring**: The module monitors algorithm execution time and blocks algorithms that exceed their maximum calculation duration.

### State Estimation Algorithms

1. **Modular Design**: Each state estimation type (SOC, SOE, SOH, SOF) supports multiple implementation variants:
   - Counting (full implementation)
   - Debug (simplified for testing)
   - None (no-op stub)

2. **Common Patterns**:
   - All implementations validate pointer parameters via FAS_ASSERT
   - All implementations validate string number bounds
   - All implementations support per-string calculations

3. **Persistence**: SOC and SOE values are persisted to FRAM for recovery after power cycles.

4. **Recalibration**: SOC and SOE recalibrate via voltage lookup tables when the battery system is at rest.

### SOF Current Derating

1. **Trapezoid Profile**: The SOF module uses trapezoidal derating curves based on:
   - Cell voltage limits (upper and lower)
   - Temperature limits (high and low, for both charge and discharge)

2. **Safety Integration**: Current limits are set to zero when:
   - BMS is transitioning to ERROR state
   - Cell voltage exceeds safety thresholds
   - Temperature exceeds safety thresholds

3. **String Aggregation**: Pack current limits are calculated as the sum of minimum string currents across all closed strings.

---

## Safety Requirements Summary

The following safety-critical requirements were extracted:

| ID | Description | Source |
|----|-------------|--------|
| ALGO-MGR-006 | Block algorithms exceeding max calculation duration | algorithm.c:158-165 |
| ALGO-MGR-008 | Validate algorithm index bounds | algorithm_cfg.c:83,94 |
| ALGO-SE-003 | Validate stringNumber parameter | state_estimation.c |
| ALGO-SOC-002 | Validate pSocValues pointer | soc_counting.c:254 |
| ALGO-SOC-003 | Validate stringNumber bounds | soc_counting.c:255 |
| ALGO-SOC-004 | Validate pSocValues before processing | soc_counting.c:301 |
| ALGO-SOE-002 | Validate pSoeValues pointer | soe_counting.c:322 |
| ALGO-SOE-003 | Validate stringNumber bounds | soe_counting.c:323 |
| ALGO-SOE-004 | Validate pSoeValues before processing | soe_counting.c:368 |
| ALGO-SOH-002 | Validate pSohValues pointer | soh_none.c:72 |
| ALGO-SOH-003 | Validate stringNumber bounds | soh_none.c:73 |
| ALGO-SOH-004 | Validate pSohValues before processing | soh_none.c:77 |
| ALGO-SOF-004 | Validate voltage limit pointers | sof_trapezoid.c:197-199 |
| ALGO-SOF-005 | Validate temperature limit pointers | sof_trapezoid.c:242-244 |
| ALGO-SOF-014 | Zero current during ERROR transition | sof_trapezoid.c:426-431 |

---

## Configuration Parameters Extracted

### Algorithm Manager Configuration
- ALGO_TICK_ms = 100ms (base scheduling tick)

### Moving Average Configuration
- MOVING_AVERAGE_DURATION_CURRENT_CONFIG_ms = 3000ms
- MOVING_AVERAGE_DURATION_POWER_CONFIG_ms = 3000ms
- ISA_CURRENT_CYCLE_TIME_ms = 200ms
- ISA_POWER_CYCLE_TIME_ms = 200ms

### SOC Configuration
- SOC_STRING_CAPACITY_mAh (derived from battery cell)
- SOC_MAXIMUM_SOC_perc = 100.0%
- SOC_MINIMUM_SOC_perc = 0.0%

### SOE Configuration
- SOE_CELL_ENERGY_Wh = 20000Wh (debug)
- SOE_STRING_ENERGY_Wh (derived from battery cell)
- MAXIMUM_SOE_PERC = 100.0%
- MINIMUM_SOE_PERC = 0.0%

### SOF Configuration
- SOF_STRING_CURRENT_CONTINUOUS_CHARGE_mA (derived)
- SOF_STRING_CURRENT_CONTINUOUS_DISCHARGE_mA (derived)
- SOF_STRING_CURRENT_LIMP_HOME_mA = 20000mA
- Temperature thresholds (derived from battery cell limits)
- Voltage thresholds (derived from battery cell limits)

---

## Recommendations for Review

1. **Complete TODOs**: Several files contain TODO placeholders in their @details sections that should be filled in with proper descriptions.

2. **SOH Implementation**: The current SOH implementations are stubs (debug/none variants). A full SOH calculation algorithm should be implemented based on cell degradation models.

3. **Configuration Validation**: Consider adding compile-time or runtime validation for configuration parameter relationships (e.g., cutoff vs limit values).

4. **Test Coverage**: The externalized test function interfaces (TEST_*) indicate unit test support. Ensure all extracted requirements have corresponding test cases.

---

## Output Files

| File | Description |
|------|-------------|
| `algorithm-extracted.json` | Complete JSON extraction with all 84 requirements |
| `algorithm-extraction-report.md` | This summary report |

---

## Next Steps

1. **Requirement Normalization**: Process extracted requirements through the requirement transformer to normalize format and language.

2. **ID Assignment**: Assign formal requirement IDs using the PARVIS-AISpec-ReqID agent.

3. **Traceability Linking**: Establish traceability between extracted requirements and source code using the PARVIS-AISpec-Trace agent.

4. **Gap Analysis**: Compare extracted requirements against any existing specification documents.

---

*Report generated by PARVIS-AISpec-Code agent*
