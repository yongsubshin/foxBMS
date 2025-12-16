# AFE Driver Module Detailed Design Document

**Document ID**: FBMS-WP-SWE3-002
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D
**Component ID**: COMP-DRV-AFE

---

## Document Control

### Revision History

| Version | Date       | Author                   | Description                    |
|---------|------------|--------------------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI-Orchestrator   | Initial detailed design        |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Software Architect    |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This document provides the detailed design specification for the AFE (Analog Front-End) Driver Module (COMP-DRV-AFE) of the foxBMS Battery Management System. It specifies the communication protocols, measurement acquisition sequences, and safety mechanisms for various AFE ICs.

### 1.2 Scope

This document covers:
- AFE driver API specifications
- Communication protocol details (SPI/isoSPI)
- Measurement acquisition sequences
- CRC/PEC validation logic
- Error handling procedures
- Multi-vendor AFE support (ADI, Maxim, LTC, NXP)

### 1.3 References

| Document ID          | Title                                       |
|---------------------|---------------------------------------------|
| FBMS-WP-SWE1-001    | Software Requirements Specification         |
| FBMS-WP-SWE2-001    | Software Architecture Design                |
| ISO 26262-6:2018    | Product development at the software level   |

### 1.4 Source Files

| Directory/File                                | Description                         |
|----------------------------------------------|-------------------------------------|
| src/app/driver/afe/api/afe.h                 | AFE driver API header               |
| src/app/driver/afe/api/afe_dma.h             | AFE DMA interface header            |
| src/app/driver/afe/api/afe_plausibility.h    | AFE plausibility check header       |
| src/app/driver/afe/adi/                      | Analog Devices ADES183x drivers     |
| src/app/driver/afe/maxim/                    | Maxim MAX1785x drivers              |
| src/app/driver/afe/ltc/                      | Linear Technology LTC drivers       |
| src/app/driver/afe/nxp/                      | NXP MC3377x drivers                 |

---

## 2. Architecture Overview

### 2.1 Layered Design

```
+------------------------------------------+
|           AFE API Layer                   |
|  afe.h - Common interface for all AFEs   |
+------------------------------------------+
|        Vendor-Specific Layer              |
|  ADI | Maxim | LTC | NXP | TI | Debug    |
+------------------------------------------+
|        Communication Layer                |
|  SPI | isoSPI | DMA Transfer             |
+------------------------------------------+
|        Hardware Abstraction               |
|  HAL SPI | GPIO | Timer                   |
+------------------------------------------+
```

### 2.2 Supported AFE ICs

| Vendor           | IC Family      | Communication | Cell Channels |
|------------------|----------------|---------------|---------------|
| Analog Devices   | ADES1830       | isoSPI        | 16            |
| Maxim            | MAX17852       | UART/SPI      | 14            |
| Linear Technology| LTC6811        | isoSPI        | 12            |
| Linear Technology| LTC6813        | isoSPI        | 18            |
| Linear Technology| LTC6806        | SPI           | 5             |
| NXP              | MC33775A       | TPL           | 14            |
| Texas Instruments| BQ79xxx        | SPI/UART      | 16            |

---

## 3. API Specification

### 3.1 Request Enumeration

```c
typedef enum {
    AFE_START_REQUEST, /* Start measurement request */
    AFE_STOP_REQUEST,  /* Stop measurement request */
    AFE_NO_REQUEST,    /* No pending request */
    AFE_REQUEST_E_MAX,
} AFE_REQUEST_e;
```

### 3.2 I2C Transfer Types

```c
typedef enum {
    AFE_I2C_TRANSFER_TYPE_READ,          /* I2C read operation */
    AFE_I2C_TRANSFER_TYPE_WRITEREAD,     /* I2C write then read */
    AFE_I2C_TRANSFER_TYPE_READ_SUCCESS,  /* Read completed OK */
    AFE_I2C_TRANSFER_TYPE_READ_FAIL,     /* Read failed */
    AFE_I2C_TRANSFER_TYPE_WRITE,         /* I2C write operation */
    AFE_I2C_TRANSFER_TYPE_WRITE_SUCCESS, /* Write completed OK */
    AFE_I2C_TRANSFER_TYPE_WRITE_FAIL,    /* Write failed */
} AFE_I2C_TRANSFER_TYPE_e;
```

### 3.3 I2C Queue Structure

```c
typedef struct {
    uint8_t module;                    /* Target module number */
    AFE_I2C_TRANSFER_TYPE_e transferType; /* Transfer type */
    uint8_t deviceAddress;             /* I2C device address */
    uint8_t registerAddress;           /* Register address */
    uint8_t readData[13u];             /* Read data buffer */
    uint8_t readDataLength;            /* Read data length */
    uint8_t writeData[13u];            /* Write data buffer */
    uint8_t writeDataLength;           /* Write data length */
} AFE_I2C_QUEUE_s;
```

### 3.4 Constants

```c
/* Open wire measurement period */
#define AFE_ERROR_OPEN_WIRE_PERIOD_ms (30000u)

/* Invalid cell voltage value */
#define AFE_DEFAULT_CELL_VOLTAGE_INVALID_VALUE (INT16_MAX)
```

---

## 4. Function Specifications

### 4.1 AFE_TriggerIc()

**Purpose**: Main tick function to advance the AFE state machine.

**Prototype**:
```c
extern STD_RETURN_TYPE_e AFE_TriggerIc(void);
```

**Preconditions**:
- AFE module initialized
- SPI interface configured

**Postconditions**:
- AFE state machine advanced
- Measurements acquired (if triggered)

**Return Values**:
| Value      | Description                    |
|------------|--------------------------------|
| STD_OK     | Trigger executed successfully  |
| STD_NOT_OK | Error during execution         |

### 4.2 AFE_Initialize()

**Purpose**: Initialize the AFE driver module.

**Prototype**:
```c
extern STD_RETURN_TYPE_e AFE_Initialize(void);
```

**Postconditions**:
- AFE IC configuration registers set
- Communication verified
- Self-test passed (if supported)

### 4.3 AFE_IsFirstMeasurementCycleFinished()

**Purpose**: Check if the first complete measurement cycle has completed.

**Prototype**:
```c
extern bool AFE_IsFirstMeasurementCycleFinished(void);
```

**Return Values**:
| Value | Description                         |
|-------|-------------------------------------|
| true  | First measurement cycle completed   |
| false | Still waiting for first cycle       |

**Safety Purpose**: Ensures valid data before BMS makes decisions.

### 4.4 AFE_StartMeasurement()

**Purpose**: Request AFE to begin measurement acquisition.

**Prototype**:
```c
extern STD_RETURN_TYPE_e AFE_StartMeasurement(void);
```

### 4.5 AFE_RequestTemperatureRead()

**Purpose**: Request temperature measurement from external sensors on slave boards.

**Prototype**:
```c
extern STD_RETURN_TYPE_e AFE_RequestTemperatureRead(uint8_t string);
```

**Parameters**:
| Name   | Type    | Direction | Description      |
|--------|---------|-----------|------------------|
| string | uint8_t | In        | String to read   |

### 4.6 AFE_RequestOpenWireCheck()

**Purpose**: Initiate open wire detection sequence.

**Prototype**:
```c
extern STD_RETURN_TYPE_e AFE_RequestOpenWireCheck(uint8_t string);
```

**Parameters**:
| Name   | Type    | Direction | Description      |
|--------|---------|-----------|------------------|
| string | uint8_t | In        | String to check  |

**Safety Purpose**: Detects broken cell voltage sense wires (ASIL-D requirement).

---

## 5. Communication Protocol

### 5.1 isoSPI Communication (ADI, LTC)

#### 5.1.1 Frame Format

```
+--------+--------+--------+--------+--------+--------+
| CMD[0] | CMD[1] | DATA   | DATA   | PEC[0] | PEC[1] |
| (MSB)  | (LSB)  | [0]    | [n-1]  | (MSB)  | (LSB)  |
+--------+--------+--------+--------+--------+--------+
```

#### 5.1.2 PEC (Packet Error Code) Calculation

The PEC is a 15-bit CRC calculated over CMD and DATA bytes.

**Polynomial**: x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + 1

**PEC Calculation Function** (conceptual):
```c
uint16_t ADI_ADES183X_Pec15(uint8_t *pData, uint8_t length) {
    uint16_t pec = 16u; /* Initial seed */
    for (uint8_t i = 0u; i < length; i++) {
        uint8_t din = pData[i];
        for (uint8_t j = 0u; j < 8u; j++) {
            uint8_t in = (din >> (7u - j)) & 0x01u;
            /* CRC calculation logic */
        }
    }
    return (pec << 1u); /* Return with trailing bit */
}
```

### 5.2 SPI Communication (NXP, Maxim)

#### 5.2.1 Frame Format (NXP MC33775A)

```
+----------+----------+----------+----------+
| HEADER   | ADDRESS  | DATA     | CRC      |
| (8-bit)  | (16-bit) | (16-bit) | (16-bit) |
+----------+----------+----------+----------+
```

#### 5.2.2 CRC-8 Calculation (Maxim)

**Polynomial**: x^8 + x^5 + x^4 + 1 (0x31)

```c
uint8_t MXM_Crc8(uint8_t *pData, uint8_t length) {
    uint8_t crc = 0u;
    for (uint8_t i = 0u; i < length; i++) {
        crc ^= pData[i];
        for (uint8_t j = 0u; j < 8u; j++) {
            if (crc & 0x80u) {
                crc = (crc << 1u) ^ 0x31u;
            } else {
                crc <<= 1u;
            }
        }
    }
    return crc;
}
```

---

## 6. Measurement Acquisition Sequence

### 6.1 Cell Voltage Measurement

#### 6.1.1 Sequence Steps (ADI ADES183x)

1. **Send ADCV Command**: Start cell voltage ADC conversion
2. **Wait for Conversion**: Typical 2.3ms (all cells)
3. **Poll PLADC Status**: Check conversion complete (optional)
4. **Read Register Group A**: Cells 1-3
5. **Read Register Group B**: Cells 4-6
6. **Read Register Group C**: Cells 7-9
7. **Read Register Group D**: Cells 10-12
8. **Read Register Group E**: Cells 13-16 (if applicable)
9. **Verify PEC**: Check all register group PECs
10. **Store to Database**: Write validated data

#### 6.1.2 ADC Conversion Modes

| Mode | Description           | Conversion Time |
|------|-----------------------|-----------------|
| 7kHz | Normal mode           | 2.3ms          |
| 3kHz | Low power             | 4.4ms          |
| 2kHz | Filtered              | 6.6ms          |
| 1kHz | Very low power        | 12.6ms         |

### 6.2 Temperature Measurement

#### 6.2.1 Sequence Steps

1. **Configure GPIO**: Set GPIO pins for temperature sensor
2. **Start GPIO ADC**: Send ADAX command
3. **Wait for Conversion**: Typical 2.3ms
4. **Read AUX Register A**: GPIO 1-3 voltages
5. **Read AUX Register B**: GPIO 4-5 voltages
6. **Convert to Temperature**: Apply NTC lookup table
7. **Store to Database**: Write validated temperatures

### 6.3 Open Wire Detection

#### 6.3.1 Pull-Up Method

1. **Apply Pull-Up Current**: Enable internal pull-up
2. **Start Conversion**: ADOW command with PUP=1
3. **Read Voltages**: Store V_PU
4. **Apply Pull-Down Current**: Enable internal pull-down
5. **Start Conversion**: ADOW command with PUP=0
6. **Read Voltages**: Store V_PD
7. **Calculate Difference**: V_diff = V_PU - V_PD
8. **Detect Open Wire**: If V_diff > threshold, wire is open

#### 6.3.2 Detection Thresholds

| Condition           | Threshold   | Unit |
|---------------------|-------------|------|
| Open wire detected  | > 400       | mV   |
| Normal connection   | < 100       | mV   |

---

## 7. Error Handling

### 7.1 Communication Errors

| Error Type          | Detection Method           | Response                    |
|---------------------|----------------------------|-----------------------------|
| PEC/CRC Mismatch    | Compare calculated vs RX   | Retry, report DIAG          |
| Command Counter     | Track sequence numbers     | Re-sync, report DIAG        |
| Timeout             | SPI timeout detection      | Reset SPI, retry            |
| No Response         | MISO stays low/high        | Check isoSPI connection     |

### 7.2 Measurement Errors

| Error Type          | Detection Method           | Response                    |
|---------------------|----------------------------|-----------------------------|
| Open Wire           | Pull-up/pull-down test     | Mark cell invalid, DIAG     |
| Overvoltage         | Compare vs limits          | Report SOA violation        |
| Undervoltage        | Compare vs limits          | Report SOA violation        |
| Invalid Value       | Out of range check         | Use default invalid value   |

### 7.3 Diagnostic Integration

```c
/* Example diagnostic reporting */
if (pecError == true) {
    DIAG_Handler(DIAG_ID_AFE_SPI, DIAG_EVENT_NOT_OK, DIAG_STRING, stringNumber);
}

if (openWireDetected == true) {
    DIAG_Handler(DIAG_ID_AFE_OPEN_WIRE, DIAG_EVENT_NOT_OK, DIAG_STRING, stringNumber);
}
```

---

## 8. Safety Mechanisms

### 8.1 Redundant ADC Measurements

Many AFE ICs support redundant ADC:
- ADI ADES183x: S-ADC (second ADC) for redundancy
- NXP MC33775A: Dual measurement paths
- Maxim: Internal reference verification

### 8.2 Register Readback Verification

After writing configuration registers, read back and verify:

```c
/* Write configuration */
AFE_WriteConfig(regAddress, regValue);

/* Read back */
readValue = AFE_ReadConfig(regAddress);

/* Verify */
if (readValue != regValue) {
    /* Configuration mismatch - report error */
    DIAG_Handler(DIAG_ID_AFE_CONFIG, DIAG_EVENT_NOT_OK, DIAG_STRING, string);
}
```

### 8.3 Watchdog Monitoring

AFE ICs with internal watchdog:
- Must be triggered periodically
- Failure detection via status register
- Auto-reset on watchdog timeout

### 8.4 Self-Test Execution

| Self-Test Type      | Purpose                    | Trigger          |
|---------------------|----------------------------|------------------|
| ADC Self-Test       | Verify ADC accuracy        | On init, periodic|
| Multiplexer Test    | Verify channel selection   | On init          |
| Open Wire Test      | Detect broken connections  | Periodic         |
| Reference Test      | Verify voltage reference   | On init, periodic|

---

## 9. Vendor-Specific Implementation

### 9.1 Analog Devices (ADES183x)

#### 9.1.1 Source Files

| File                              | Description                     |
|-----------------------------------|--------------------------------|
| adi_ades183x.c                    | Main state machine             |
| adi_ades183x_commands.c           | Command definitions            |
| adi_ades183x_voltages.c           | Voltage measurement            |
| adi_ades183x_temperatures.c       | Temperature measurement        |
| adi_ades183x_diagnostic_w.c       | Diagnostic functions           |
| adi_ades183x_pec.c                | PEC calculation                |
| adi_ades183x_initialization.c     | Init sequence                  |

#### 9.1.2 Key Features

- isoSPI daisy-chain communication
- 16-bit ADC resolution
- Built-in cell balancing
- Redundant ADC (S-ADC)

### 9.2 Maxim (MAX1785x)

#### 9.2.1 Source Files

| File                              | Description                     |
|-----------------------------------|--------------------------------|
| mxm_1785x.c                       | Main state machine             |
| mxm_17841b.c                      | UART bridge driver             |
| mxm_battery_management.c          | Battery management logic       |
| mxm_registry.c                    | Device registry                |
| mxm_crc8.c                        | CRC-8 calculation              |

#### 9.2.2 Key Features

- UART-based daisy chain
- 14-cell capability
- I2C interface for external sensors

### 9.3 Linear Technology (LTC6811/6813)

#### 9.3.1 Source Files

| File                              | Description                     |
|-----------------------------------|--------------------------------|
| ltc_6813-1.c                      | LTC6813 driver                 |
| ltc_6806.c                        | LTC6806 driver                 |
| ltc_pec.c                         | PEC calculation                |
| ltc_afe_dma.c                     | DMA transfer                   |

#### 9.3.2 Key Features

- isoSPI communication (LTC6813)
- SPI communication (LTC6806)
- 12/18 cell capability

### 9.4 NXP (MC33775A)

#### 9.4.1 Source Files

| File                              | Description                     |
|-----------------------------------|--------------------------------|
| nxp_mc3377x.c                     | Main state machine             |
| nxp_mc3377x-ll.c                  | Low-level communication        |
| nxp_mc3377x_helpers.c             | Helper functions               |
| nxp_mc3377x_database.c            | Database interface             |

#### 9.4.2 Key Features

- Transformer Physical Layer (TPL)
- 14-cell capability
- High-speed daisy chain

---

## 10. DMA Transfer

### 10.1 DMA Configuration

AFE communication uses DMA for efficient data transfer:

```c
/* DMA buffer structure */
typedef struct {
    uint8_t txBuffer[AFE_TX_BUFFER_SIZE];
    uint8_t rxBuffer[AFE_RX_BUFFER_SIZE];
    volatile bool transferComplete;
} AFE_DMA_BUFFER_s;
```

### 10.2 Transfer Sequence

1. **Prepare TX Buffer**: Load command and data
2. **Start DMA Transfer**: Initiate SPI DMA
3. **Wait for Completion**: Poll or use interrupt
4. **Process RX Buffer**: Extract received data
5. **Verify Integrity**: Check PEC/CRC

---

## 11. Plausibility Checking

### 11.1 Cell Voltage Plausibility

```c
STD_RETURN_TYPE_e AFE_PlausibilityCheckCellVoltage(
    int16_t cellVoltage_mV,
    AFE_PLAUSIBILITY_VALUES_s *pPlausibilityValues
) {
    STD_RETURN_TYPE_e retval = STD_NOT_OK;

    if ((cellVoltage_mV >= pPlausibilityValues->minimumVoltage_mV) &&
        (cellVoltage_mV <= pPlausibilityValues->maximumVoltage_mV)) {
        retval = STD_OK;
    }

    return retval;
}
```

### 11.2 Plausibility Thresholds

| Parameter          | Minimum | Maximum | Unit |
|--------------------|---------|---------|------|
| Cell Voltage       | 0       | 5000    | mV   |
| Cell Temperature   | -40     | 125     | degC |
| Pack Current       | -500000 | 500000  | mA   |

---

## 12. Traceability

### 12.1 Requirements Traceability

| Design Element          | Requirement ID        | Description                   |
|------------------------|-----------------------|-------------------------------|
| AFE_TriggerIc          | FBMS-FUNC-DRV-001    | AFE state machine trigger     |
| PEC Calculation        | FBMS-SAFETY-DRV-001  | Communication integrity       |
| Open Wire Detection    | FBMS-SAFETY-DRV-002  | Connection verification       |
| Redundant ADC          | FBMS-SAFETY-DRV-003  | Measurement redundancy        |
| Plausibility Check     | FBMS-SAFETY-DRV-004  | Value range validation        |

### 12.2 Architecture Traceability

| Design Element    | Architecture Component | Interface ID  |
|-------------------|----------------------|---------------|
| AFE module        | COMP-DRV-AFE         | -             |
| SPI interface     | COMP-DRV-SPI         | IF-EXT-002    |
| Database          | COMP-ENG-DB          | IF-INT-002    |
| DIAG              | COMP-ENG-DIAG        | -             |

---

## 13. Appendix

### 13.1 Register Map Reference (ADI ADES183x)

| Register Group | Address | Description              | Size   |
|----------------|---------|--------------------------|--------|
| RDCVA          | 0x0004  | Cell Voltages 1-3        | 6 bytes|
| RDCVB          | 0x0006  | Cell Voltages 4-6        | 6 bytes|
| RDCVC          | 0x0008  | Cell Voltages 7-9        | 6 bytes|
| RDCVD          | 0x000A  | Cell Voltages 10-12      | 6 bytes|
| RDCVE          | 0x0009  | Cell Voltages 13-16      | 6 bytes|
| RDAUXA         | 0x000C  | Auxiliary Group A        | 6 bytes|
| RDAUXB         | 0x000E  | Auxiliary Group B        | 6 bytes|
| RDCFGA         | 0x0002  | Configuration Group A    | 6 bytes|
| RDCFGB         | 0x0026  | Configuration Group B    | 6 bytes|
| RDSTATA        | 0x0010  | Status Group A           | 6 bytes|
| RDSTATB        | 0x0012  | Status Group B           | 6 bytes|

### 13.2 Command Reference (ADI ADES183x)

| Command | Code    | Description                  |
|---------|---------|------------------------------|
| ADCV    | 0x0360  | Start Cell Voltage ADC       |
| ADAX    | 0x0460  | Start GPIO ADC               |
| ADOW    | 0x0228  | Start Open Wire ADC          |
| WRCFGA  | 0x0001  | Write Configuration A        |
| WRCFGB  | 0x0024  | Write Configuration B        |
| CLRFLAG | 0x0714  | Clear Status Flags           |

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
