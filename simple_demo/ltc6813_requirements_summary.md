# LTC 6813-1 AFE Driver - Extracted Software Requirements Summary

**Source File**: `foxbms-2/src/app/driver/afe/ltc/6813-1/ltc_6813-1.c`
**Extraction Date**: 2025-12-19
**Tool**: PARVIS-AISpec-Code (Requirement Extraction Agent)

---

## Executive Summary

This document summarizes software requirements reverse-engineered from the LTC 6813-1 Analog Front-End (AFE) driver source code. The extraction focused on three key areas:

1. **Safety Assertions (FAS_ASSERT)**: Runtime safety checks preventing null pointer access and invalid state conditions
2. **Cell Voltage Monitoring**: Measurement, validation, and plausibility checking of cell voltages
3. **MISRA C:2012 Compliance Patterns**: Coding standards demonstrating automotive-grade software development

---

## Statistics Overview

| Category | Count |
|----------|-------|
| Total Requirements Extracted | 33 |
| Safety Assertions | 22 |
| Cell Voltage Monitoring | 13 |
| MISRA Compliance Patterns | 11 |

---

## 1. Safety Assertions (FAS_ASSERT Patterns)

### 1.1 Pointer Validation Requirements

The driver implements comprehensive null pointer validation at function entry points. Every function that receives pointer parameters validates them before use.

**Key Requirements**:

| ID | Function | Assertion | Purpose |
|----|----------|-----------|---------|
| SW-REQ-LTC-001 | LTC_SaveVoltages | `ltc_state != NULL_PTR` | Prevent null dereference when saving voltages |
| SW-REQ-LTC-002 | LTC_SaveVoltages | `stringNumber < BS_NR_OF_STRINGS` | Prevent array out-of-bounds |
| SW-REQ-LTC-011 | LTC_Init | Multiple pointer checks | Validate SPI and buffer pointers |
| SW-REQ-LTC-018 | LTC_ReadRegister | 4 pointer validations | Ensure valid command and SPI resources |

**Pattern**: All functions follow defensive programming by asserting pointer validity before any dereference operation.

### 1.2 Invalid State Detection Requirements

| ID | Function | Condition | Action |
|----|----------|-----------|--------|
| SW-REQ-LTC-021 | LTC_Trigger | default case in switch | FAS_TRAP on invalid state |
| SW-REQ-LTC-022 | LTC_SaveMuxMeasurement | Invalid mux ID | FAS_TRAP on unknown multiplexer |

**Pattern**: State machines use `FAS_ASSERT(FAS_TRAP)` in default switch cases to catch invalid states during runtime.

---

## 2. Cell Voltage Monitoring Requirements

### 2.1 Measurement Chain

The voltage measurement process follows this sequence:

```
Start Measurement (ADCV command)
       |
       v
Read Register Groups (RDCVA-F)
       |
       v
Convert Raw ADC to mV
       |
       v
Validate PEC (CRC-15)
       |
       v
Check Open Wire Status
       |
       v
Plausibility Check (0-5000mV)
       |
       v
Calculate String Voltage
       |
       v
Update Database
```

### 2.2 Key Functional Requirements

| ID | Requirement | Source Line |
|----|-------------|-------------|
| SW-REQ-LTC-030 | Read 6 voltage register groups via SPI | 3042-3142 |
| SW-REQ-LTC-031 | Convert ADC values: voltage_mV = raw * 100e-6 * 1000 | 3103 |
| SW-REQ-LTC-032 | Store only PEC-valid measurements | 3106-3123 |
| SW-REQ-LTC-034 | Plausibility check: 0-5000mV range | 624-635 |
| SW-REQ-LTC-035 | Validate open-wire status before accepting voltage | 610-620 |
| SW-REQ-LTC-036 | Calculate string voltage from valid cells | 628-630 |

### 2.3 Plausibility Configuration

```c
static const AFE_PLAUSIBILITY_VALUES_s ltc_plausibleCellVoltages681x = {
    .maximumPlausibleVoltage_mV = 5000,
    .minimumPlausibleVoltage_mV = 0,
};
```

**Rationale**: Physical limits for lithium-ion cell voltage (0V fully discharged, 5V covers all chemistry types with margin).

### 2.4 Data Integrity (PEC Verification)

The driver implements CRC-15 Packet Error Code checking:

1. Calculate PEC over received 6 data bytes
2. Compare against received 2-byte PEC
3. Update per-device PEC_valid flag in error table
4. Only store measurements with valid PEC

---

## 3. MISRA C:2012 Compliance Patterns

### 3.1 Documented Deviations

| ID | Rule | Location | Justification |
|----|------|----------|---------------|
| SW-REQ-LTC-050 | Rule 1.2 | Lines 112-117 | PEC buffers in shared RAM for DMA performance |

**Code Pattern**:
```c
/* AXIVION Disable Style MisraC2012-1.2: Performance reasons */
#pragma SET_DATA_SECTION(".sharedRAM")
uint16_t ltc_RxPecBuffer[...] = {0};
uint16_t ltc_TxPecBuffer[...] = {0};
#pragma SET_DATA_SECTION()
/* AXIVION Enable Style MisraC2012-1.2: only Pec buffer needed */
```

### 3.2 Coding Standard Patterns

| ID | Pattern | Example | MISRA Rule |
|----|---------|---------|------------|
| SW-REQ-LTC-051 | Unsigned suffix | `0u`, `0xFFu` | Rule 7.2 |
| SW-REQ-LTC-052 | Explicit casts | `(uint8_t)(value)` | Rule 10.3 |
| SW-REQ-LTC-053 | Boolean comparisons | `== true`, `== false` | Rule 14.4 |
| SW-REQ-LTC-054 | Void return cast | `(void)function()` | Rule 17.7 |
| SW-REQ-LTC-055 | NULL_PTR macro | `!= NULL_PTR` | Rule 11.9 |
| SW-REQ-LTC-058 | Static functions | `static void func()` | Rule 8.8 |
| SW-REQ-LTC-060 | Named constants | `#define LTC_ICOM_START` | Rule 2.5 |

---

## 4. State Machine Architecture

### 4.1 State Definition

The driver uses a hierarchical state machine with main states and substates:

**Initial State**: `LTC_STATEMACH_UNINITIALIZED`

**Key States**:
- UNINITIALIZED
- INITIALIZED
- STARTMEAS (Start Measurement)
- READVOLTAGE
- READGPIO
- BALANCECONTROL
- OPENWIRE

### 4.2 State Transition Pattern

```c
static void LTC_StateTransition(
    LTC_STATE_s *ltc_state,
    LTC_STATEMACH_e state,
    uint8_t substate,
    uint16_t timer_ms);
```

**Pattern**: All state transitions go through centralized transition functions that update state, substate, and timer atomically.

---

## 5. Interface Requirements

### 5.1 SPI Communication

| Parameter | Value |
|-----------|-------|
| Protocol | Daisy-chain SPI |
| Command Size | 4 bytes (2 cmd + 2 PEC) |
| Data Size | 8 bytes per device (6 data + 2 PEC) |
| Devices | LTC_N_LTC (configurable) |

### 5.2 Database Interface

The driver writes to these database blocks:
- `DATA_BLOCK_ID_CELL_VOLTAGE_BASE`
- `DATA_BLOCK_ID_CELL_TEMPERATURE_BASE`
- `DATA_BLOCK_ID_BALANCING_FEEDBACK_BASE`
- `DATA_BLOCK_ID_BALANCING_CONTROL`
- `DATA_BLOCK_ID_ALL_GPIO_VOLTAGES_BASE`
- `DATA_BLOCK_ID_OPEN_WIRE_BASE`

### 5.3 Diagnostic Integration

| Diagnostic ID | Purpose |
|---------------|---------|
| DIAG_ID_AFE_SPI | SPI communication errors |
| DIAG_ID_AFE_COMMUNICATION_INTEGRITY | PEC errors |
| DIAG_ID_AFE_MUX | Multiplexer errors |
| DIAG_ID_AFE_CELL_VOLTAGE_MEAS_ERROR | Voltage measurement validity |
| DIAG_ID_AFE_CELL_TEMPERATURE_MEAS_ERROR | Temperature measurement validity |

---

## 6. Traceability Matrix

| Requirement ID | Code Location | Test Method |
|----------------|---------------|-------------|
| SW-REQ-LTC-001 to -022 | FAS_ASSERT statements | Unit test with null pointers |
| SW-REQ-LTC-030 to -042 | Voltage processing functions | Unit test with SPI mock |
| SW-REQ-LTC-050 to -060 | Throughout source file | Static analysis (AXIVION) |

---

## 7. Output Files

| File | Description |
|------|-------------|
| `simple_demo/ltc6813_requirements.json` | Structured JSON with all extracted requirements |
| `simple_demo/ltc6813_requirements_summary.md` | This summary document |

---

## 8. Recommendations for Requirements Documentation

1. **Formalize Safety Requirements**: The FAS_ASSERT patterns should be documented in a formal safety requirements specification with ASIL ratings.

2. **Add Test References**: Each requirement should link to corresponding unit test cases.

3. **Version Control**: Requirements should include version numbers matching the source code version (currently v1.10.0).

4. **Bidirectional Traceability**: Create links from requirements to design documents and from design to code.

---

**Document Version**: 1.0
**Generated by**: PARVIS-AISpec-Code
**foxBMS Version**: v1.10.0
