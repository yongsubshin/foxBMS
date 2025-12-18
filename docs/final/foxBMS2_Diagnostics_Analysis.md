# foxBMS 2 BMS Diagnostics System Analysis

**Analysis Date**: 2025-12-15
**Target Version**: foxBMS 2 v1.10.0
**Repository**: https://github.com/foxBMS/foxbms-2

---

## 1. Overview

foxBMS 2 is an open-source Battery Management System (BMS) developed by Fraunhofer, featuring a comprehensive diagnostics system. This diagnostic system monitors and handles various error states to ensure safe operation of the battery pack.

---

## 2. Diagnostics System Architecture

### 2.1 Core Module Structure

```
src/app/
├── engine/
│   ├── diag/                    # Core Diagnostic Engine
│   │   ├── diag.c/.h           # Main diagnostic handler
│   │   └── cbs/                # Diagnostic callback functions
│   │       ├── diag_cbs_voltage.c
│   │       ├── diag_cbs_temperature.c
│   │       ├── diag_cbs_current.c
│   │       ├── diag_cbs_insulation.c
│   │       ├── diag_cbs_plausibility.c
│   │       └── ... (other callbacks)
│   ├── sys_mon/                # System Monitoring
│   └── config/
│       ├── diag_cfg.c/.h       # Diagnostic configuration
│       └── sys_mon_cfg.c/.h    # System monitoring configuration
├── application/
│   ├── soa/                    # Safe Operating Area checks
│   ├── plausibility/           # Plausibility checks
│   └── redundancy/             # Redundancy checks
└── driver/
    └── imd/                    # Insulation Monitoring Device
```

### 2.2 Diagnostic Processing Flow

```
[Sensor Data] → [SOA Check] → [DIAG_Handler] → [Callback Function] → [Database Update]
                    ↓
            [Event Counter]
                    ↓
            [Threshold Exceeded]
                    ↓
            [CAN Error Transmission + Contactor Open]
```

---

## 3. Diagnostic Event Classification (DIAG_ID)

### 3.1 Voltage Diagnostics

| DIAG_ID | Description | Severity | Delay |
|---------|-------------|----------|-------|
| `DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MSL` | Cell overvoltage (Maximum Safety Limit) | Fatal Error | 200ms |
| `DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_RSL` | Cell overvoltage (Recommended Safety Limit) | Warning | - |
| `DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MOL` | Cell overvoltage (Maximum Operating Limit) | Info | - |
| `DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_MSL` | Cell undervoltage (Maximum Safety Limit) | Fatal Error | 200ms |
| `DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_RSL` | Cell undervoltage (Recommended Safety Limit) | Warning | - |
| `DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_MOL` | Cell undervoltage (Maximum Operating Limit) | Info | - |
| `DIAG_ID_DEEP_DISCHARGE_DETECTED` | Deep discharge detected | Fatal Error | 100ms |

### 3.2 Temperature Diagnostics

| DIAG_ID | Description | Severity | Delay |
|---------|-------------|----------|-------|
| `DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_MSL` | Overtemperature during charge (MSL) | Fatal Error | 1000ms |
| `DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_RSL` | Overtemperature during charge (RSL) | Warning | - |
| `DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_MOL` | Overtemperature during charge (MOL) | Info | - |
| `DIAG_ID_TEMP_OVERTEMPERATURE_DISCHARGE_MSL` | Overtemperature during discharge (MSL) | Fatal Error | 1000ms |
| `DIAG_ID_TEMP_UNDERTEMPERATURE_CHARGE_MSL` | Undertemperature during charge (MSL) | Fatal Error | 1000ms |
| `DIAG_ID_TEMP_UNDERTEMPERATURE_DISCHARGE_MSL` | Undertemperature during discharge (MSL) | Fatal Error | 1000ms |

### 3.3 Current Diagnostics

| DIAG_ID | Description | Severity | Delay |
|---------|-------------|----------|-------|
| `DIAG_ID_OVERCURRENT_CHARGE_CELL_MSL` | Cell-level charge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_OVERCURRENT_DISCHARGE_CELL_MSL` | Cell-level discharge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_STRING_OVERCURRENT_CHARGE_MSL` | String-level charge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_STRING_OVERCURRENT_DISCHARGE_MSL` | String-level discharge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_PACK_OVERCURRENT_CHARGE_MSL` | Pack-level charge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_PACK_OVERCURRENT_DISCHARGE_MSL` | Pack-level discharge overcurrent | Fatal Error | 100ms |
| `DIAG_ID_CURRENT_ON_OPEN_STRING` | Current detected on open string | Fatal Error | 100ms |

### 3.4 Insulation Monitoring Diagnostics

| DIAG_ID | Description | Severity | Threshold |
|---------|-------------|----------|-----------|
| `DIAG_ID_INSULATION_MEASUREMENT_VALID` | Insulation measurement validity | Warning | - |
| `DIAG_ID_LOW_INSULATION_RESISTANCE_ERROR` | Critical insulation resistance | Warning | 500kOhm |
| `DIAG_ID_LOW_INSULATION_RESISTANCE_WARNING` | Warning-level insulation resistance | Warning | 750kOhm |
| `DIAG_ID_INSULATION_GROUND_ERROR` | Ground fault detected | Warning | - |

### 3.5 Communication Diagnostics

| DIAG_ID | Description | Severity |
|---------|-------------|----------|
| `DIAG_ID_AFE_SPI` | AFE SPI communication error | Fatal Error |
| `DIAG_ID_AFE_COMMUNICATION_INTEGRITY` | AFE communication integrity (PEC error) | Fatal Error |
| `DIAG_ID_AFE_MUX` | AFE multiplexer error | Fatal Error |
| `DIAG_ID_AFE_CONFIG` | AFE configuration error | Fatal Error |
| `DIAG_ID_CAN_TIMING` | CAN timing error | Fatal Error |
| `DIAG_ID_CAN_RX_QUEUE_FULL` | CAN RX queue full | Warning |
| `DIAG_ID_CAN_TX_QUEUE_FULL` | CAN TX queue full | Warning |

### 3.6 Sensor Diagnostics

| DIAG_ID | Description | Severity |
|---------|-------------|----------|
| `DIAG_ID_CURRENT_SENSOR_RESPONDING` | Current sensor response | Fatal Error |
| `DIAG_ID_CURRENT_SENSOR_CC_RESPONDING` | Coulomb counter response | Fatal Error |
| `DIAG_ID_CURRENT_SENSOR_EC_RESPONDING` | Energy counter response | Fatal Error |
| `DIAG_ID_CURRENT_MEASUREMENT_TIMEOUT` | Current measurement timeout | Fatal Error |
| `DIAG_ID_CURRENT_MEASUREMENT_ERROR` | Current measurement error | Fatal Error |

### 3.7 Plausibility Check Diagnostics

| DIAG_ID | Description | Severity |
|---------|-------------|----------|
| `DIAG_ID_PLAUSIBILITY_CELL_VOLTAGE` | Cell voltage plausibility | Warning |
| `DIAG_ID_PLAUSIBILITY_CELL_VOLTAGE_SPREAD` | Cell voltage spread plausibility | Warning |
| `DIAG_ID_PLAUSIBILITY_CELL_TEMP` | Cell temperature plausibility | Warning |
| `DIAG_ID_PLAUSIBILITY_CELL_TEMPERATURE_SPREAD` | Cell temperature spread plausibility | Warning |
| `DIAG_ID_PLAUSIBILITY_PACK_VOLTAGE` | Pack voltage plausibility | Fatal Error |

### 3.8 Contactor/Interlock Diagnostics

| DIAG_ID | Description | Severity |
|---------|-------------|----------|
| `DIAG_ID_INTERLOCK_FEEDBACK` | Interlock feedback error | Fatal Error |
| `DIAG_ID_STRING_MINUS_CONTACTOR_FEEDBACK` | String minus contactor feedback | Fatal Error |
| `DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK` | String plus contactor feedback | Fatal Error |
| `DIAG_ID_PRECHARGE_CONTACTOR_FEEDBACK` | Precharge contactor feedback | Fatal Error |

### 3.9 Other Diagnostics

| DIAG_ID | Description | Severity |
|---------|-------------|----------|
| `DIAG_ID_FLASHCHECKSUM` | Flash checksum error | Fatal Error |
| `DIAG_ID_SYSTEM_MONITORING` | System monitoring error | Fatal Error |
| `DIAG_ID_SBC_FIN_ERROR` | SBC FIN signal error | Warning |
| `DIAG_ID_SBC_RSTB_ERROR` | SBC RSTB pin activation | Fatal Error |
| `DIAG_ID_AFE_OPEN_WIRE` | Open wire detected | Warning |
| `DIAG_ID_ALERT_MODE` | Alert mode (fuse not triggered) | Fatal Error |
| `DIAG_ID_AEROSOL_ALERT` | Aerosol concentration warning | Warning |
| `DIAG_ID_FRAM_READ_CRC_ERROR` | FRAM CRC error | Info |

---

## 4. Safety Limits System

foxBMS 2 uses a 3-tier safety limit system:

### 4.1 Limit Levels

| Level | Abbreviation | Description | Response |
|-------|--------------|-------------|----------|
| **Maximum Safety Limit** | MSL | Maximum safety threshold | Immediate contactor opening |
| **Recommended Safety Limit** | RSL | Recommended safety threshold | Warning issued |
| **Maximum Operating Limit** | MOL | Maximum operating threshold | Information logging |

### 4.2 Database Flag Tables

- `DATA_BLOCK_MSL_FLAG_s`: MSL violation flags
- `DATA_BLOCK_RSL_FLAG_s`: RSL violation flags
- `DATA_BLOCK_MOL_FLAG_s`: MOL violation flags
- `DATA_BLOCK_ERROR_STATE_s`: General error state

---

## 5. Diagnostic Handler (DIAG_Handler)

### 5.1 Main Functions

```c
/**
 * @brief Process diagnostic event
 * @param diagId    Diagnostic ID
 * @param event     Event type (OK, NOT_OK, RESET)
 * @param impact    Impact level (SYSTEM, STRING)
 * @param data      Additional data (string number, etc.)
 */
DIAG_RETURNTYPE_e DIAG_Handler(
    DIAG_ID_e diagId,
    DIAG_EVENT_e event,
    DIAG_IMPACT_LEVEL_e impact,
    uint32_t data);
```

### 5.2 Event Types

```c
typedef enum {
    DIAG_EVENT_OK,      // Normal state
    DIAG_EVENT_NOT_OK,  // Error occurred
    DIAG_EVENT_RESET,   // Error reset
} DIAG_EVENT_e;
```

### 5.3 Severity Levels

```c
typedef enum {
    DIAG_FATAL_ERROR,  // Fatal error → Contactor open
    DIAG_WARNING,      // Warning
    DIAG_INFO,         // Information
} DIAG_SEVERITY_LEVEL_e;
```

### 5.4 Return Types

```c
typedef enum {
    DIAG_HANDLER_RETURN_OK,               // Normal or threshold not reached
    DIAG_HANDLER_RETURN_ERR_OCCURRED,     // Error occurred and active
    DIAG_HANDLER_RETURN_WARNING_OCCURRED, // Warning occurred
    DIAG_HANDLER_RETURN_WRONG_ID,         // Invalid diagnostic ID
    DIAG_HANDLER_RETURN_UNKNOWN,          // Unknown return type
    DIAG_HANDLER_INVALID_TYPE,            // Invalid diagnostic type
    DIAG_HANDLER_INVALID_DATA,            // Invalid data
    DIAG_HANDLER_INVALID_ERR_IMPACT,      // Invalid impact level
    DIAG_HANDLER_RETURN_NOT_READY,        // Diagnostic handler not ready
} DIAG_RETURNTYPE_e;
```

---

## 6. SOA (Safe Operating Area) Checks

### 6.1 Voltage Check (`SOA_CheckVoltages`)

```c
// Overvoltage check hierarchy
if (voltageMax_mV >= BC_VOLTAGE_MAX_MOL_mV) {
    DIAG_Handler(DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MOL, ...);
    if (voltageMax_mV >= BC_VOLTAGE_MAX_RSL_mV) {
        DIAG_Handler(DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_RSL, ...);
        if (voltageMax_mV >= BC_VOLTAGE_MAX_MSL_mV) {
            DIAG_Handler(DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MSL, ...);
        }
    }
}
```

### 6.2 Temperature Check (`SOA_CheckTemperatures`)

- Differentiated temperature limits based on charge/discharge state
- MSL/RSL/MOL level checks for both over and under temperature

### 6.3 Current Check (`SOA_CheckCurrent`)

- Cell-level, string-level, and pack-level current checks
- Differentiated limits based on charge/discharge direction
- Current detection on open strings

---

## 7. Plausibility Checks

### 7.1 Cell Voltage Plausibility Check

```c
STD_RETURN_TYPE_e PL_CheckCellVoltage(
    int16_t baseCellVoltage,
    int16_t redundancy0CellVoltage,
    int16_t *pCellVoltage);
```

- Compares base measurement with redundant measurement
- Tolerance: `PL_CELL_VOLTAGE_TOLERANCE_mV`

### 7.2 Cell Temperature Plausibility Check

```c
STD_RETURN_TYPE_e PL_CheckCellTemperature(
    int16_t baseCellTemperature,
    int16_t redundancy0CellTemperature,
    int16_t *pCellTemperature);
```

- Tolerance: `PL_CELL_TEMPERATURE_TOLERANCE_dK`

### 7.3 Voltage/Temperature Spread Checks

- `PL_CheckVoltageSpread`: Cell voltage spread check
- `PL_CheckTemperatureSpread`: Cell temperature spread check
- Invalidates cells showing large deviation from average

---

## 8. Insulation Monitoring (IMD)

### 8.1 Supported Devices

- Bender IR155
- Bender ISO165C

### 8.2 Insulation Resistance Thresholds

```c
#define IMD_ERROR_THRESHOLD_INSULATION_RESISTANCE_kOhm   (500u)
#define IMD_WARNING_THRESHOLD_INSULATION_RESISTANCE_kOhm (750u)
```

### 8.3 State Machine

```
UNINITIALIZED → INITIALIZATION → IMD_ENABLE → RUNNING
                                      ↓
                                   ERROR
                                      ↓
                                  SHUTDOWN
```

---

## 9. System Monitoring

### 9.1 Features

- Periodic task execution time monitoring
- Timing violation detection and logging
- FRAM storage of violation records

### 9.2 Monitored Tasks

- Engine Task
- 1ms Cyclic Task
- 10ms Cyclic Task
- 100ms Cyclic Task
- 100ms Algorithm Task

### 9.3 Notification Interface

```c
void SYSM_Notify(
    SYSM_TASK_ID_e taskId,
    SYSM_NOTIFY_TYPE_e state,  // ENTER or EXIT
    uint32_t timestamp);
```

---

## 10. Diagnostic Configuration

### 10.1 Configuration Structure

```c
typedef struct {
    DIAG_ID_e id;                          // Diagnostic ID
    uint16_t threshold;                     // Event threshold
    DIAG_SEVERITY_LEVEL_e severity;         // Severity level
    uint32_t delay_ms;                      // Delay time
    DIAG_EVALUATE_e enable_evaluate;        // Evaluation enable
    DIAG_CALLBACK_FUNCTION_f *fpCallback;   // Callback function
} DIAG_ID_CFG_s;
```

### 10.2 Event Sensitivity Settings

```c
#define DIAG_SEN_EVENT_1    (0u)    // Log on 1st event
#define DIAG_SEN_EVENT_5    (4u)    // Log on 5th event
#define DIAG_SEN_EVENT_10   (9u)    // Log on 10th event
#define DIAG_SEN_EVENT_50   (49u)   // Log on 50th event
#define DIAG_SEN_EVENT_100  (99u)   // Log on 100th event
#define DIAG_SEN_EVENT_500  (499u)  // Log on 500th event
```

### 10.3 Delay Settings

```c
#define DIAG_DELAY_DISCARD  (UINT32_MAX)  // No delay (non-fatal)
#define DIAG_NO_DELAY       (0u)          // Immediate response
#define DIAG_DELAY_100ms    (100u)
#define DIAG_DELAY_200ms    (200u)
#define DIAG_DELAY_1000ms   (1000u)
```

---

## 11. Error Transmission (CAN)

### 11.1 Fatal Error Transmission

- Errors with `DIAG_FATAL_ERROR` severity are transmitted via CAN
- Active errors retransmitted every 100ms
- Clear message sent when error is resolved

### 11.2 Related Functions

```c
// Transmit fatal error ID
CANTX_SendFatalErrorId(DIAG_ID_e errorId);
```

---

## 12. Diagnostic Callback Functions

| Callback Function | Purpose |
|-------------------|---------|
| `DIAG_ErrorOvervoltage` | Overvoltage event |
| `DIAG_ErrorUndervoltage` | Undervoltage event |
| `DIAG_ErrorOvertemperatureCharge` | Charge overtemperature event |
| `DIAG_ErrorOvertemperatureDischarge` | Discharge overtemperature event |
| `DIAG_ErrorUndertemperatureCharge` | Charge undertemperature event |
| `DIAG_ErrorUndertemperatureDischarge` | Discharge undertemperature event |
| `DIAG_ErrorOvercurrentCharge` | Charge overcurrent event |
| `DIAG_ErrorOvercurrentDischarge` | Discharge overcurrent event |
| `DIAG_ErrorCurrentOnOpenString` | Open string current |
| `DIAG_ErrorCurrentMeasurement` | Current measurement error |
| `DIAG_ErrorHighVoltageMeasurement` | High voltage measurement error |
| `DIAG_ErrorSystemMonitoring` | System monitoring error |
| `DIAG_ErrorInterlock` | Interlock error |
| `DIAG_ErrorCanTiming` | CAN timing error |
| `DIAG_ErrorAfeDriver` | AFE driver error |
| `DIAG_ErrorAfe` | AFE-related error |
| `DIAG_ErrorCurrentSensor` | Current sensor error |
| `DIAG_ErrorPlausibility` | Plausibility check error |
| `DIAG_PlausibilityCheck` | Plausibility check |
| `DIAG_StringContactorFeedback` | String contactor feedback |
| `DIAG_PrechargeContactorFeedback` | Precharge contactor feedback |
| `DIAG_ErrorDeepDischarge` | Deep discharge event |
| `DIAG_ErrorPowerMeasurement` | Power measurement error |
| `DIAG_Insulation` | Insulation monitoring |
| `DIAG_Sbc` | SBC-related event |
| `DIAG_I2c` | I2C error |
| `DIAG_Rtc` | RTC error |
| `DIAG_FramError` | FRAM error |
| `DIAG_AlertFlag` | Alert flag |
| `DIAG_AerosolAlert` | Aerosol alert |
| `DIAG_PrechargeProcess` | Precharge process |
| `DIAG_SupplyVoltageClamp30c` | Clamp30C supply |

---

## 13. File Location Summary

| File | Location | Description |
|------|----------|-------------|
| `diag.c/.h` | `src/app/engine/diag/` | Core diagnostic engine |
| `diag_cfg.c/.h` | `src/app/engine/config/` | Diagnostic configuration |
| `diag_cbs_*.c` | `src/app/engine/diag/cbs/` | Diagnostic callback functions |
| `soa.c/.h` | `src/app/application/soa/` | SOA checks |
| `plausibility.c/.h` | `src/app/application/plausibility/` | Plausibility checks |
| `redundancy.c/.h` | `src/app/application/redundancy/` | Redundancy checks |
| `imd.c/.h` | `src/app/driver/imd/` | Insulation monitoring |
| `sys_mon.c/.h` | `src/app/engine/sys_mon/` | System monitoring |

---

## 14. Circuit Diagnostics

foxBMS 2 implements hardware circuit diagnostic functions at the AFE (Analog Front-End) driver level.

### 14.1 AFE Driver Diagnostics

#### Diagnostic ID List

| DIAG_ID | Description | Severity | Callback |
|---------|-------------|----------|----------|
| `DIAG_ID_AFE_SPI` | SPI communication error | Fatal Error | `DIAG_ErrorAfeDriver` |
| `DIAG_ID_AFE_COMMUNICATION_INTEGRITY` | CRC/PEC communication integrity error | Fatal Error | `DIAG_ErrorAfeDriver` |
| `DIAG_ID_AFE_MUX` | Multiplexer error | Fatal Error | `DIAG_ErrorAfeDriver` |
| `DIAG_ID_AFE_CONFIG` | AFE configuration error | Fatal Error | `DIAG_ErrorAfeDriver` |
| `DIAG_ID_AFE_OPEN_WIRE` | Open wire detection | Warning | `DIAG_ErrorAfeDriver` |
| `DIAG_ID_AFE_CELL_VOLTAGE_MEAS_ERROR` | Cell voltage measurement error | - | `DIAG_ErrorAfe` |
| `DIAG_ID_AFE_CELL_TEMPERATURE_MEAS_ERROR` | Cell temperature measurement error | - | `DIAG_ErrorAfe` |

#### Database Error Flags

```c
// AFE-related flags in DATA_BLOCK_ERROR_STATE_s structure
afeCommunicationSpiError[stringNumber]           // SPI communication error
afeCommunicationCrcError[stringNumber]           // CRC/PEC error
afeSlaveMultiplexerError[stringNumber]           // Multiplexer error
afeConfigurationError[stringNumber]              // Configuration error
openWireDetectedError[stringNumber]              // Open wire detected
afeCellVoltageInvalidError[stringNumber]         // Cell voltage measurement invalid
afeCellTemperatureInvalidError[stringNumber]     // Cell temperature measurement invalid
baseCellVoltageMeasurementTimeoutError           // Base voltage measurement timeout
redundancy0CellVoltageMeasurementTimeoutError    // Redundant voltage measurement timeout
baseCellTemperatureMeasurementTimeoutError       // Base temperature measurement timeout
redundancy0CellTemperatureMeasurementTimeoutError // Redundant temperature measurement timeout
```

### 14.2 Open Wire Detection

Detects wire breaks (open wire) in cell voltage measurement lines.

#### LTC Series Implementation (LTC6806, LTC6813-1)

**File Locations**:
- `src/app/driver/afe/ltc/6806/ltc_6806.c`
- `src/app/driver/afe/ltc/6813-1/ltc_6813-1.c`

**Data Structures**:

```c
// Open wire detection data
typedef struct {
    int32_t openWirePup[BS_NR_OF_STRINGS][BS_NR_OF_CELL_BLOCKS_PER_STRING];   // Pull-up voltage
    int32_t openWirePdown[BS_NR_OF_STRINGS][BS_NR_OF_CELL_BLOCKS_PER_STRING]; // Pull-down voltage
    int32_t openWireDelta[BS_NR_OF_STRINGS][BS_NR_OF_CELL_BLOCKS_PER_STRING]; // Voltage difference
} LTC_OPENWIRE_DETECTION_s;

// Open wire result storage
typedef struct {
    uint8_t openWire[BS_NR_OF_STRINGS][BS_NR_OF_MODULES_PER_STRING * (BS_NR_OF_CELL_BLOCKS_PER_MODULE + 1)];
    uint16_t nrOpenWires[BS_NR_OF_STRINGS];  // Number of detected open wires
    uint8_t state;
} DATA_BLOCK_OPEN_WIRE_s;
```

**Detection Algorithm**:

```
1. Apply pull-up current → Measure cell voltage (openWirePup)
2. Apply pull-down current → Measure cell voltage (openWirePdown)
3. Calculate voltage difference: openWireDelta = openWirePup - openWirePdown
4. Compare against threshold to determine open wire:
   - First cell: Pup value is 0 or max → Open wire
   - Last cell: Pdown value is 0 or max → Open wire
   - Middle cells: Delta value is negative (< -400mV) → Open wire
```

### 14.3 ADI ADES183x Diagnostics

**File Locations**:
- `src/app/driver/afe/adi/common/ades183x/adi_ades183x_diagnostic.h`
- `src/app/driver/afe/adi/common/ades183x/adi_ades183x_diagnostic_w.c`

**Diagnostic Functions**:

```c
// Execute AFE built-in diagnostic functions
void ADI_Diagnostic(ADI_STATE_s *adiState);

// Evaluate cell voltage measurement diagnostics
bool ADI_EvaluateDiagnosticCellVoltages(ADI_STATE_s *adiState, uint16_t moduleNumber);

// Evaluate GPIO voltage measurement diagnostics
bool ADI_EvaluateDiagnosticGpioVoltages(ADI_STATE_s *adiState, uint16_t moduleNumber);

// Evaluate string/module voltage measurement diagnostics
bool ADI_EvaluateDiagnosticStringAndModuleVoltages(ADI_STATE_s *adiState, uint16_t moduleNumber);
```

### 14.4 Communication Integrity Check (PEC/CRC)

Each AFE chipset verifies communication data integrity.

| Manufacturer | Chipset | Verification Method | File Location |
|--------------|---------|---------------------|---------------|
| **LTC (ADI)** | LTC6804/6806/6811/6813 | PEC (Packet Error Code) | `src/app/driver/afe/ltc/common/ltc_pec.c` |
| **ADI** | ADES1830 | PEC-15 | `src/app/driver/afe/adi/common/ades183x/pec/adi_ades183x_pec.c` |
| **Maxim** | MAX17852 | CRC8 | `src/app/driver/afe/maxim/common/mxm_crc8.c` |
| **NXP** | MC33775A | CRC | `src/app/driver/afe/nxp/common/mc3377x/nxp_mc3377x.c` |

#### PEC/CRC Verification Flow

```
[SPI Transmit] → [Data + PEC/CRC Transmission] → [AFE Receive and Verify]
                                                        ↓
[SPI Receive] ← [Data + PEC/CRC Response] ← [AFE Response]
      ↓
[PEC/CRC Calculate and Compare]
      ↓
[On Mismatch] → DIAG_Handler(DIAG_ID_AFE_COMMUNICATION_INTEGRITY, DIAG_EVENT_NOT_OK, ...)
```

### 14.5 AFE Chipset Circuit Diagnostic Support

| Manufacturer | Chipset | Open Wire | PEC/CRC | Built-in Diag | Multiplexer |
|--------------|---------|:---------:|:-------:|:-------------:|:-----------:|
| **LTC (ADI)** | LTC6804-1 | Yes | Yes | - | Yes |
| **LTC (ADI)** | LTC6806 | Yes | Yes | - | Yes |
| **LTC (ADI)** | LTC6811-1 | Yes | Yes | - | Yes |
| **LTC (ADI)** | LTC6813-1 | Yes | Yes | - | Yes |
| **ADI** | ADES1830 | Yes | Yes | Yes | Yes |
| **NXP** | MC33775A | Yes | Yes | - | Yes |
| **Maxim** | MAX17852 | - | Yes | - | - |
| **TI** | BQ79xxx | - | Yes | - | - |

### 14.6 Circuit Diagnostic File Locations

| File | Location | Description |
|------|----------|-------------|
| `diag_cbs_afe.c` | `src/app/engine/diag/cbs/` | AFE diagnostic callback functions |
| `ltc_pec.c` | `src/app/driver/afe/ltc/common/` | LTC PEC calculation |
| `ltc_6806.c` | `src/app/driver/afe/ltc/6806/` | LTC6806 driver (includes open wire) |
| `ltc_6813-1.c` | `src/app/driver/afe/ltc/6813-1/` | LTC6813-1 driver (includes open wire) |
| `adi_ades183x_diagnostic.h` | `src/app/driver/afe/adi/common/ades183x/` | ADI diagnostic header |
| `adi_ades183x_diagnostic_w.c` | `src/app/driver/afe/adi/common/ades183x/` | ADI diagnostic implementation |
| `adi_ades183x_pec.c` | `src/app/driver/afe/adi/common/ades183x/pec/` | ADI PEC calculation |
| `mxm_crc8.c` | `src/app/driver/afe/maxim/common/` | Maxim CRC8 calculation |
| `nxp_mc3377x.c` | `src/app/driver/afe/nxp/common/mc3377x/` | NXP driver |
| `afe_plausibility.c` | `src/app/driver/afe/api/` | AFE plausibility checks |

### 14.7 Circuit Diagnostic Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AFE Driver Level                              │
├─────────────────────────────────────────────────────────────────┤
│  [SPI Communication]                                             │
│      ↓                                                           │
│  [PEC/CRC Verify] ─────────────────→ [Fail] → DIAG_ID_AFE_SPI   │
│      ↓ Success                              or                   │
│  [Data Verify] ────────────────────→ [Fail] → DIAG_ID_AFE_COMMUNICATION_INTEGRITY │
│      ↓ Success                                                   │
│  [Open Wire Detection] ────────────→ [Detected] → DIAG_ID_AFE_OPEN_WIRE │
│      ↓                                                           │
│  [Built-in Diagnostic (ADI)] ──────→ [Fail] → Corresponding DIAG_ID │
│      ↓                                                           │
│  [Return Normal Data]                                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Diagnostic Engine Level                       │
├─────────────────────────────────────────────────────────────────┤
│  DIAG_Handler() → Callback Function → Database Flag Setting      │
│                                     ↓                            │
│                            [On Fatal Error]                      │
│                                     ↓                            │
│                         CAN Error Transmission + Contactor Open  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 15. Conclusion

The foxBMS 2 diagnostic system features the following characteristics:

1. **Hierarchical Safety Limits**: Flexible response with MSL/RSL/MOL 3-tier system
2. **Comprehensive Monitoring**: Covers all areas including voltage, temperature, current, insulation, and communication
3. **Configurability**: User-definable thresholds, sensitivity, and delay times
4. **Extensibility**: Callback-based architecture for easy addition of new diagnostic items
5. **Redundancy**: Measurement reliability through plausibility checks
6. **Communication Integration**: Error state transmission via CAN support
7. **Circuit Diagnostics**: AFE-level open wire, PEC/CRC, and built-in diagnostic support

This diagnostic system is designed to meet safety requirements for automotive and industrial battery systems (ISO 26262, etc.).

---

## 16. Official Documentation References

Official documentation files included in the repository (RST format):

| File Path | Description |
|-----------|-------------|
| `docs/software/modules/engine/diag/diag.rst` | Diagnostic module overview and configuration |
| `docs/software/modules/engine/diag/diag_how-to.rst` | Diagnostic module usage guide |
| `docs/software/modules/engine/sys_mon/sys_mon.rst` | System monitoring module details |
| `docs/software/modules/driver/imd/imd.rst` | IMD state machine and interface |
| `docs/software/modules/driver/imd/bender/bender_ir155.rst` | Bender IR155 driver |
| `docs/software/modules/driver/imd/bender/bender_iso165c.rst` | Bender ISO165C driver |
| `docs/system/system-error-table.csv` | Diagnostic error table (CSV) |
| `docs/system/system-voltage-and-current-monitoring.rst` | Voltage/current monitoring system structure |

### Building Documentation

foxBMS 2 documentation is built using Sphinx:

```bash
# Build documentation
cd foxbms-2
./fox.sh doc
```

Built documentation can be found in the `build/docs/` directory.
