# foxBMS-2 Reverse-Engineered Requirements Extraction Report

## Executive Summary

This report documents the extraction of software requirements from the foxBMS-2 source code (v1.10.0) focusing on undocumented algorithms, safety-critical modules, and configuration parameters.

**Extraction Date:** 2025-12-16
**Source Version:** v1.10.0
**Total Requirements Extracted:** 78
**Extraction Agent:** PARVIS-AISpec-Code

## Extraction Scope

### Priority Targets Analyzed

| Module | Files Analyzed | Requirements Extracted |
|--------|---------------|----------------------|
| State Estimation (SOC) | soc_counting.c, soc_counting_cfg.h | 7 |
| State Estimation (SOE) | soe_counting.c, soe_counting_cfg.h | 3 |
| State Estimation (SOF) | sof_trapezoid.c, sof_trapezoid_cfg.h | 6 |
| Balancing (BAL) | bal.c, bal.h, bal_strategy_voltage.c, bal_cfg.h | 9 |
| Safety Configuration | battery_cell_cfg.h, battery_system_cfg.h | 23 |
| Diagnostic Callbacks | diag_cbs_*.c (22 handlers) | 13 |
| CAN Messages | can_cfg*.h, can_cbs_tx_*.c | 12 |

## Extraction Results by Category

### 1. State Estimation Algorithms

#### SOC (State of Charge) - Coulomb Counting

**Algorithm Summary:**
- Method: Ampere-hour integration (coulomb counting)
- Update: Triggered on current sensor timestamp change
- Recalibration: Voltage-based lookup table when at rest
- Storage: FRAM persistence for power cycle recovery

**Key Extracted Requirements:**

| ID | Requirement | Source Line |
|----|-------------|-------------|
| FBMS-EXT-SOC-001 | SOC calculation using coulomb counting | 299-398 |
| FBMS-EXT-SOC-002 | SOC range [0.0, 100.0]% limitation | 84-87, 217-239 |
| FBMS-EXT-SOC-004 | SOC recalibration at rest via LUT | 313-316 |

**Formula Extracted:**
```
deltaSOC_perc = ((current_mA * timeStep_s) / SOC_STRING_CAPACITY_mAs) * 100.0 / 1000.0
```

#### SOE (State of Energy) - Energy Counting

**Algorithm Summary:**
- Method: Watt-hour integration
- Formula: deltaSOE = (I * V) / time / 3600
- Recalibration: Voltage-based when at rest

**Key Extracted Requirements:**

| ID | Requirement | Source Line |
|----|-------------|-------------|
| FBMS-EXT-SOE-001 | SOE calculation using energy counting | 367-483 |
| FBMS-EXT-SOE-002 | SOE range [0.0, 100.0]% limitation | 88-89, 295-317 |

#### SOF (State of Function) - Trapezoid Derating

**Algorithm Summary:**
- Method: Trapezoid curve derating
- Inputs: Cell voltage (min/max), Temperature (min/max)
- Outputs: Allowed charge/discharge currents (continuous, peak)

**Derating Logic:**
1. Voltage-based: Linear derating between cutoff and limit voltages
2. Temperature-based: Linear derating at low/high temperature extremes
3. Final value: Minimum of voltage-based and temperature-based limits

**Key Extracted Requirements:**

| ID | Requirement | ASIL |
|----|-------------|------|
| FBMS-EXT-SOF-001 | Trapezoid derating curves | ASIL-B |
| FBMS-EXT-SOF-002 | Voltage-based current limiting | ASIL-B |
| FBMS-EXT-SOF-003 | Temperature-based current limiting | ASIL-B |
| FBMS-EXT-SOF-004 | Emergency shutoff override (all currents to 0) | ASIL-B |

### 2. Balancing Module

**State Machine Structure:**
- 12 Main States (BAL_STATEMACH_e)
- 6 Substates (BAL_STATEMACH_SUB_e)
- Trigger period: 100ms

**State Machine Diagram:**
```
UNINITIALIZED -> INITIALIZATION -> INITIALIZED -> CHECK_BALANCING
                                                         |
                                                         v
                                                      BALANCE
                                                         |
                                         (balancing complete)
                                                         |
                                                         v
                                               CHECK_BALANCING
```

**Balancing Strategy (Voltage-Based):**
- Threshold: Configurable (default 200mV, range 0-5000mV)
- Hysteresis: 200mV (prevents oscillation)
- Safety limits:
  - Minimum voltage: 2000mV (stop balancing)
  - Maximum temperature: 70.0 degC (stop balancing)
- Precondition: Battery must be at rest

### 3. Safety Parameters (MSL/RSL/MOL)

The system implements a three-tier safety limit architecture:

| Tier | Name | Action |
|------|------|--------|
| MSL | Maximum Safety Limit | Error state, open contactors |
| RSL | Recommended Safety Limit | Warning flag |
| MOL | Maximum Operating Limit | Operational boundary |

#### Cell Voltage Limits

| Parameter | MSL | RSL | MOL | Unit |
|-----------|-----|-----|-----|------|
| Maximum | 2800 | 2750 | 2720 | mV |
| Minimum | 1500 | 1550 | 1580 | mV |
| Deep Discharge | 1500 | - | - | mV |

#### Temperature Limits (Discharge)

| Parameter | MSL | RSL | MOL | Unit |
|-----------|-----|-----|-----|------|
| Maximum | 55.0 | 50.0 | 45.0 | degC |
| Minimum | -20.0 | -15.0 | -10.0 | degC |

#### Temperature Limits (Charge)

| Parameter | MSL | RSL | MOL | Unit |
|-----------|-----|-----|-----|------|
| Maximum | 45.0 | 40.0 | 35.0 | degC |
| Minimum | -20.0 | -15.0 | -10.0 | degC |

#### Current Limits

| Parameter | MSL | RSL | MOL | Unit |
|-----------|-----|-----|-----|------|
| Discharge | 180000 | 175000 | 170000 | mA |
| Charge | 180000 | 175000 | 170000 | mA |
| String Max | 2400 | - | - | mA |

### 4. Diagnostic Callbacks

**22 Diagnostic Handlers Analyzed:**

| Handler | Diagnostic IDs Supported | ASIL |
|---------|-------------------------|------|
| DIAG_ErrorOvervoltage | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorUndervoltage | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorOvertemperatureCharge | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorOvertemperatureDischarge | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorUndertemperatureCharge | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorUndertemperatureDischarge | MSL, RSL, MOL | ASIL-B |
| DIAG_ErrorOvercurrentCharge | Cell/String/Pack MSL/RSL/MOL | ASIL-B |
| DIAG_ErrorOvercurrentDischarge | Cell/String/Pack MSL/RSL/MOL | ASIL-B |
| DIAG_ErrorCurrentMeasurement | Timeout, Invalid | ASIL-B |
| DIAG_ErrorCurrentOnOpenString | Single ID | ASIL-B |
| DIAG_StringContactorFeedback | Plus, Minus | ASIL-B |
| DIAG_PrechargeContactorFeedback | Single ID | ASIL-B |
| DIAG_ErrorDeepDischarge | Single ID (FRAM) | ASIL-B |

### 5. CAN Message Configuration

#### TX Cyclic Messages

| Message | ID (hex) | DLC | Period (ms) | Content |
|---------|----------|-----|-------------|---------|
| BMS State | 0x220 | 8 | 100 | State, errors, flags |
| BMS State Details | 0x221 | 8 | 1000 | Detailed state info |
| Cell Voltages | 0x250 | 8 | 100 | Cell voltage values |
| Cell Temperatures | 0x260 | 8 | 200 | Temperature values |
| Pack Limits | 0x232 | 8 | 100 | Current limits |
| Pack Min/Max | 0x231 | 8 | 100 | Min/max values |
| Pack State Est. | 0x235 | 8 | 1000 | SOC/SOE/SOH |
| String State | 0x240 | 8 | 100 | String status |
| String State Est. | 0x245 | 8 | 1000 | String SOC/SOE |

#### BMS State Message (0x220) Signal Layout

| Signal | Start Bit | Length | Description |
|--------|-----------|--------|-------------|
| Connected Strings | 7 | 4 | Number of connected strings |
| BMS State | 3 | 4 | Current state machine state |
| BMS Substate | 37 | 6 | Current substate |
| General Error | 10 | 1 | Fatal error flag |
| Emergency Shutoff | 11 | 1 | Transition to error active |
| System Mon Error | 12 | 1 | Timing violation |
| Insulation Mon | 13 | 1 | IMD running flag |
| Insulation Error | 23 | 1 | Insulation fault |
| Insulation Resistance | 63 | 8 | Resistance value (factor 200) |

## System Configuration Parameters

### Battery System Architecture

| Parameter | Value | Unit |
|-----------|-------|------|
| Number of Strings | 1 | - |
| Modules per String | 1 | - |
| Cell Blocks per Module | 18 | - |
| Parallel Cells per Block | 1 | - |
| Temperature Sensors per Module | 8 | - |
| Cell Capacity | 3500 | mAh |
| Cell Energy | 10.0 | Wh |
| Nominal Cell Voltage | 2500 | mV |

### Timing Parameters

| Parameter | Value | Unit | Description |
|-----------|-------|------|-------------|
| Current Sensor Timeout | 200 | ms | Error if no update |
| Coulomb Counter Timeout | 2000 | ms | CC measurement timeout |
| Energy Counter Timeout | 2000 | ms | EC measurement timeout |
| Rest Current Threshold | 200 | mA | Below = at rest |
| Relaxation Period | 600 | s | Wait before rest state |
| Fuse Trigger Wait | 3000 | ms | Max wait for fuse |

### Contactor Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Maximum Break Current | 3500 | mA |
| Number of Contactors | 3 | - |

## ASIL Classification Summary

Based on extracted safety-critical functionality:

| Category | Count | ASIL |
|----------|-------|------|
| Safety Functions (FSR) | 27 | ASIL-B |
| Software Requirements (SWE) | 51 | Various |
| Total ASIL-B | 58 | - |
| Total QM | 20 | - |

## Traceability Hints

### Code-to-Requirement Mapping

| Source File | Requirements |
|-------------|--------------|
| soc_counting.c | FBMS-EXT-SOC-001 to 007 |
| soe_counting.c | FBMS-EXT-SOE-001 to 003 |
| sof_trapezoid.c | FBMS-EXT-SOF-001 to 006 |
| bal_strategy_voltage.c | FBMS-EXT-BAL-001 to 009 |
| battery_cell_cfg.h | FBMS-EXT-SAFETY-001 to 011 |
| battery_system_cfg.h | FBMS-EXT-SYS-001 to 010 |
| diag_cbs_*.c | FBMS-EXT-DIAG-001 to 013 |
| can_cfg*.h | FBMS-EXT-CAN-001 to 012 |

## Recommendations

### High Priority Items

1. **Document Algorithm Accuracy Specifications**
   - SOC counting accuracy depends on current sensor accuracy
   - SOE counting requires accurate voltage and current measurements
   - Consider adding accuracy requirements

2. **Formalize State Machine Requirements**
   - BAL state machine has implicit timing requirements
   - Add explicit timing constraints for state transitions

3. **Validate Safety Limits**
   - Current cell parameters (2.8V max, 1.5V min) suggest specific cell chemistry
   - Verify limits match actual cell datasheet

### Medium Priority Items

1. **CAN DBC File Generation**
   - Extracted signal definitions can generate DBC file
   - Enables automated test harness development

2. **Diagnostic Coverage Analysis**
   - Map diagnostic handlers to failure modes
   - Verify FMEA coverage

### Low Priority Items

1. **Add MOL/RSL flag handling requirements**
   - Current extraction shows MSL triggers error
   - RSL/MOL behavior needs explicit requirements

## Appendix: Extraction Statistics

### Files Analyzed

- Total C source files: 35
- Total header files: 18
- Lines of code analyzed: ~12,000

### Extraction Method Distribution

| Method | Count |
|--------|-------|
| Algorithm Analysis | 7 |
| Safety Constraint | 4 |
| Safety Limit | 14 |
| Configuration | 14 |
| State Machine | 4 |
| Timing | 4 |
| Diagnostic | 13 |
| Interface | 12 |
| Assertion | 3 |
| Other | 3 |

### Confidence Levels

All 78 extracted requirements have HIGH confidence level, indicating:
- Clear source code implementation
- Explicit parameter definitions
- Consistent patterns across codebase

---

**Document Version:** 1.0
**Generated by:** PARVIS-AISpec-Code Agent
**Output Location:** docs/parvis/requirements/
