# Interface Control Document (ICD)

**Document ID**: FBMS-WP-SWE3-ICD
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author                   | Description                    |
|---------|------------|--------------------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI-Orchestrator   | Initial ICD document           |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Software Architect    |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This Interface Control Document (ICD) specifies the detailed interfaces between software components of the foxBMS Battery Management System. It defines data types, function prototypes, timing requirements, and error codes.

### 1.2 Scope

This document covers:
- Internal software interfaces (function calls, data structures)
- External interfaces (CAN, SPI, GPIO)
- Timing requirements and constraints
- Error codes and handling

---

## 2. Interface Catalog

### 2.1 Interface Summary

| Interface ID | Name                      | Type       | Components          | ASIL  |
|--------------|---------------------------|------------|---------------------|-------|
| IF-INT-001   | BMS to DATABASE           | Internal   | BMS <-> DB          | D     |
| IF-INT-002   | AFE to DATABASE           | Internal   | AFE -> DB           | D     |
| IF-INT-003   | ALGO to DATABASE          | Internal   | ALGO <-> DB         | C     |
| IF-INT-004   | SOA to DIAG               | Internal   | SOA -> DIAG         | D     |
| IF-INT-005   | BMS to CONTACTOR          | Internal   | BMS -> CONT         | D     |
| IF-INT-006   | SBC to SPI                | Internal   | SBC <-> SPI         | D     |
| IF-EXT-001   | CAN Bus                   | External   | CAN <-> Vehicle     | B     |
| IF-EXT-002   | AFE SPI/isoSPI            | External   | AFE <-> IC          | D     |

---

## 3. Internal Interface Specifications

### 3.1 IF-INT-001: BMS to DATABASE Interface

#### 3.1.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-INT-001                                 |
| Source        | COMP-APP-BMS                               |
| Destination   | COMP-ENG-DB                                |
| Direction     | Bidirectional                              |
| ASIL          | ASIL-D                                     |
| Cycle Time    | 10ms                                       |

#### 3.1.2 Data Types

**Read Data Blocks**:
```c
typedef struct {
    DATA_BLOCK_HEADER_s header;        /* Unique ID, timestamp */
    int32_t packCurrent_mA;            /* Pack current */
    int32_t stringCurrent_mA[BS_NR_OF_STRINGS]; /* String currents */
    int32_t stringVoltage_mV[BS_NR_OF_STRINGS]; /* String voltages */
    int32_t highVoltageBusVoltage_mV;  /* HV bus voltage */
    uint8_t invalidPackCurrent;        /* Pack current validity */
    uint8_t invalidStringCurrent[BS_NR_OF_STRINGS]; /* Current validity */
    uint8_t invalidStringVoltage[BS_NR_OF_STRINGS]; /* Voltage validity */
    uint8_t invalidHvBusVoltage;       /* HV bus validity */
} DATA_BLOCK_PACK_VALUES_s;

typedef struct {
    DATA_BLOCK_HEADER_s header;
    int16_t minimumCellVoltage_mV[BS_NR_OF_STRINGS];
    int16_t maximumCellVoltage_mV[BS_NR_OF_STRINGS];
    int16_t minimumTemperature_ddegC[BS_NR_OF_STRINGS];
    int16_t maximumTemperature_ddegC[BS_NR_OF_STRINGS];
} DATA_BLOCK_MIN_MAX_s;
```

**Write Data Blocks**:
```c
typedef struct {
    DATA_BLOCK_HEADER_s header;
    BMS_CAN_STATE_e bmsCanState;       /* Current BMS state for CAN */
} DATA_BLOCK_SYSTEM_STATE_s;
```

#### 3.1.3 Function Prototypes

```c
/* Read multiple data blocks */
extern STD_RETURN_TYPE_e DATA_READ_DATA(void *pDataBlock0, ...);

/* Write multiple data blocks */
extern STD_RETURN_TYPE_e DATA_WRITE_DATA(void *pDataBlock0, ...);
```

#### 3.1.4 Timing Requirements

| Parameter          | Value    | Description                    |
|--------------------|----------|--------------------------------|
| Max latency        | 1ms      | Max time for data access       |
| Update rate        | 10ms     | Data refresh rate              |
| Queue depth        | 5        | Max pending operations         |

---

### 3.2 IF-INT-002: AFE to DATABASE Interface

#### 3.2.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-INT-002                                 |
| Source        | COMP-DRV-AFE                               |
| Destination   | COMP-ENG-DB                                |
| Direction     | Write (AFE -> DB)                          |
| ASIL          | ASIL-D                                     |
| Cycle Time    | 100ms (configurable)                       |

#### 3.2.2 Data Types

```c
typedef struct {
    DATA_BLOCK_HEADER_s header;
    int16_t cellVoltage_mV[BS_NR_OF_STRINGS][BS_NR_OF_CELLS_PER_STRING];
    uint16_t nrValidCellVoltages[BS_NR_OF_STRINGS];
    uint8_t invalidCellVoltage[BS_NR_OF_STRINGS][BS_NR_OF_CELLS_PER_STRING];
} DATA_BLOCK_CELL_VOLTAGE_s;

typedef struct {
    DATA_BLOCK_HEADER_s header;
    int16_t cellTemperature_ddegC[BS_NR_OF_STRINGS][BS_NR_OF_TEMP_SENSORS_PER_STRING];
    uint16_t nrValidTemperatures[BS_NR_OF_STRINGS];
    uint8_t invalidCellTemperature[BS_NR_OF_STRINGS][BS_NR_OF_TEMP_SENSORS_PER_STRING];
} DATA_BLOCK_CELL_TEMPERATURE_s;

typedef struct {
    DATA_BLOCK_HEADER_s header;
    uint8_t openWire[BS_NR_OF_STRINGS][(BS_NR_OF_CELL_BLOCKS_PER_MODULE + 1) * BS_NR_OF_MODULES_PER_STRING];
} DATA_BLOCK_OPEN_WIRE_s;
```

#### 3.2.3 Timing Requirements

| Parameter          | Value    | Description                    |
|--------------------|----------|--------------------------------|
| Update rate        | 100ms    | Measurement update rate        |
| Data freshness     | 200ms    | Max age of valid data          |
| First cycle        | 500ms    | Max time for first measurement |

---

### 3.3 IF-INT-004: SOA to DIAG Interface

#### 3.3.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-INT-004                                 |
| Source        | COMP-APP-SOA                               |
| Destination   | COMP-ENG-DIAG                              |
| Direction     | Unidirectional (SOA -> DIAG)               |
| ASIL          | ASIL-D                                     |
| Trigger       | Event-driven                               |

#### 3.3.2 Function Prototype

```c
extern STD_RETURN_TYPE_e DIAG_Handler(
    DIAG_ID_e diagId,           /* Diagnostic ID */
    DIAG_EVENT_e event,         /* OK or NOT_OK */
    DIAG_IMPACT_LEVEL_e impact, /* System, String, Cell, Module */
    uint8_t data                /* Additional data (string/cell number) */
);
```

#### 3.3.3 Diagnostic IDs

| Diagnostic ID                      | Severity | Description                    |
|------------------------------------|----------|--------------------------------|
| DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE   | Fatal    | Cell OV detected               |
| DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE  | Fatal    | Cell UV detected               |
| DIAG_ID_CELL_TEMPERATURE_OVERTEMPERATURE | Fatal | Cell OT detected          |
| DIAG_ID_CELL_TEMPERATURE_UNDERTEMPERATURE | Fatal | Cell UT detected         |
| DIAG_ID_OVERCURRENT_CHARGE         | Fatal    | Charge overcurrent             |
| DIAG_ID_OVERCURRENT_DISCHARGE      | Fatal    | Discharge overcurrent          |
| DIAG_ID_AFE_OPEN_WIRE              | Warning  | Open wire detected             |

#### 3.3.4 Event Types

```c
typedef enum {
    DIAG_EVENT_OK,      /* Condition cleared */
    DIAG_EVENT_NOT_OK,  /* Condition detected */
} DIAG_EVENT_e;
```

---

### 3.4 IF-INT-005: BMS to CONTACTOR Interface

#### 3.4.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-INT-005                                 |
| Source        | COMP-APP-BMS                               |
| Destination   | COMP-DRV-CONT                              |
| Direction     | Unidirectional (BMS -> CONT)               |
| ASIL          | ASIL-D                                     |
| Cycle Time    | 10ms                                       |

#### 3.4.2 Function Prototypes

```c
/* Open a specific contactor */
extern STD_RETURN_TYPE_e CONT_OpenContactor(
    uint8_t stringNumber,
    CONT_TYPE_e contactor
);

/* Close a specific contactor */
extern STD_RETURN_TYPE_e CONT_CloseContactor(
    uint8_t stringNumber,
    CONT_TYPE_e contactor
);

/* Close precharge contactor */
extern STD_RETURN_TYPE_e CONT_ClosePrecharge(uint8_t stringNumber);

/* Open precharge contactor */
extern STD_RETURN_TYPE_e CONT_OpenPrecharge(uint8_t stringNumber);

/* Get contactor feedback state */
extern CONT_ELECTRICAL_STATE_TYPE_e CONT_GetContactorState(
    uint8_t stringNumber,
    CONT_TYPE_e contactorType
);

/* Open all contactors (emergency) */
extern void CONT_OpenAllContactors(void);
```

#### 3.4.3 Parameter Constraints

| Parameter    | Valid Range              | Unit | Description              |
|--------------|--------------------------|------|--------------------------|
| stringNumber | 0 to BS_NR_OF_STRINGS-1  | -    | String index             |
| contactor    | CONT_PLUS, CONT_MINUS, CONT_PRECHARGE | - | Type      |

#### 3.4.4 Return Values

```c
typedef enum {
    STD_OK,      /* Operation successful */
    STD_NOT_OK,  /* Operation failed */
} STD_RETURN_TYPE_e;
```

---

### 3.5 IF-INT-006: SBC to SPI Interface

#### 3.5.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-INT-006                                 |
| Source        | COMP-DRV-SBC                               |
| Destination   | COMP-DRV-SPI                               |
| Direction     | Bidirectional                              |
| ASIL          | ASIL-D                                     |
| Cycle Time    | 100ms (watchdog)                           |

#### 3.5.2 Data Format

**SPI Frame Structure**:
```
+--------+--------+--------+--------+
| ADDR   | DATA   | DATA   | CRC    |
| (8-bit)| (8-bit)| (8-bit)| (8-bit)|
+--------+--------+--------+--------+
```

#### 3.5.3 Timing Requirements

| Parameter          | Value    | Description                    |
|--------------------|----------|--------------------------------|
| Clock frequency    | 4MHz     | SPI clock speed                |
| Frame time         | 8us      | Time per frame                 |
| CS setup time      | 100ns    | Chip select to clock           |
| CS hold time       | 100ns    | Clock to chip select release   |

---

## 4. External Interface Specifications

### 4.1 IF-EXT-001: CAN Bus Interface

#### 4.1.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-EXT-001                                 |
| Protocol      | CAN 2.0B                                   |
| Baud Rate     | 500 kbps (configurable)                    |
| Direction     | Bidirectional                              |
| ASIL          | ASIL-B                                     |

#### 4.1.2 TX Message Catalog

| Message Name         | ID (hex) | DLC | Cycle | Description              |
|---------------------|----------|-----|-------|--------------------------|
| BMS_State           | 0x100    | 8   | 100ms | BMS state information    |
| BMS_StateDetails    | 0x101    | 8   | 100ms | Detailed state info      |
| Cell_Voltages       | 0x200-x  | 8   | 100ms | Cell voltage data        |
| Cell_Temperatures   | 0x300-x  | 8   | 100ms | Cell temperature data    |
| Pack_Values_P0      | 0x400    | 8   | 100ms | Pack voltage/current     |
| Pack_Values_P1      | 0x401    | 8   | 100ms | Pack power info          |
| State_Estimation    | 0x500    | 8   | 100ms | SOC/SOE/SOH values       |
| Pack_Limits         | 0x600    | 8   | 100ms | Current/power limits     |
| MinMax_Values       | 0x700    | 8   | 100ms | Min/max cell values      |

#### 4.1.3 RX Message Catalog

| Message Name         | ID (hex) | DLC | Description                    |
|---------------------|----------|-----|--------------------------------|
| BMS_StateRequest    | 0x080    | 8   | State request from vehicle     |
| Current_Sensor      | 0x521-x  | 8   | Current sensor readings        |
| Debug               | 0x7FF    | 8   | Debug commands                 |
| IMD_Info            | 0x37-x   | 8   | Insulation monitor data        |

#### 4.1.4 BMS_StateRequest Message Format

| Byte | Bit | Signal             | Values                          |
|------|-----|--------------------|---------------------------------|
| 0    | 0-7 | RequestedState     | 0=None, 1=Normal, 2=Charge, 3=Standby |
| 1    | 0-7 | RequestID          | Request identifier              |

#### 4.1.5 BMS_State Message Format

| Byte | Bit | Signal             | Values                          |
|------|-----|--------------------|---------------------------------|
| 0    | 0-7 | CurrentState       | BMS_CAN_STATE_e enum value      |
| 1    | 0-7 | ContactorState     | Bitmask of closed contactors    |
| 2    | 0-7 | ErrorFlags         | Bitmask of active errors        |

---

### 4.2 IF-EXT-002: AFE SPI/isoSPI Interface

#### 4.2.1 Interface Description

| Attribute     | Value                                      |
|---------------|-------------------------------------------|
| Interface ID  | IF-EXT-002                                 |
| Protocol      | SPI Mode 0/3, isoSPI                       |
| Direction     | Bidirectional                              |
| ASIL          | ASIL-D                                     |

#### 4.2.2 isoSPI Timing (ADI, LTC)

| Parameter          | Value    | Description                    |
|--------------------|----------|--------------------------------|
| Clock frequency    | 1MHz     | isoSPI data rate               |
| Bit period         | 1us      | Time per bit                   |
| Start of frame     | 4us      | Idle before transmission       |
| End of frame       | 6.5us    | Idle after transmission        |

#### 4.2.3 Frame Format

**Command Frame**:
```
+--------+--------+--------+--------+--------+--------+
| CMD[0] | CMD[1] | DATA   | DATA   | PEC[0] | PEC[1] |
| (MSB)  | (LSB)  | [0]    | [n-1]  | (MSB)  | (LSB)  |
+--------+--------+--------+--------+--------+--------+
```

#### 4.2.4 PEC (Packet Error Code)

- 15-bit CRC
- Polynomial: x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + 1
- Initial value: 0x0010
- Final XOR: None

---

## 5. Data Type Definitions

### 5.1 Common Data Types

```c
/* Standard return type */
typedef enum {
    STD_OK,
    STD_NOT_OK,
} STD_RETURN_TYPE_e;

/* Data block header */
typedef struct {
    DATA_BLOCK_ID_e uniqueId;      /* Block identifier */
    uint32_t timestamp_ms;         /* Update timestamp */
    uint32_t previousTimestamp_ms; /* Previous timestamp */
} DATA_BLOCK_HEADER_s;
```

### 5.2 BMS Data Types

```c
/* BMS states */
typedef enum {
    BMS_STATEMACH_UNINITIALIZED,
    BMS_STATEMACH_INITIALIZATION,
    BMS_STATEMACH_INITIALIZED,
    BMS_STATEMACH_IDLE,
    BMS_STATEMACH_OPEN_CONTACTORS,
    BMS_STATEMACH_STANDBY,
    BMS_STATEMACH_PRECHARGE,
    BMS_STATEMACH_NORMAL,
    BMS_STATEMACH_DISCHARGE,
    BMS_STATEMACH_CHARGE,
    BMS_STATEMACH_ERROR,
} BMS_STATEMACH_e;

/* BMS state requests */
typedef enum {
    BMS_STATE_INIT_REQUEST,
    BMS_STATE_ERROR_REQUEST,
    BMS_STATE_NO_REQUEST,
} BMS_STATE_REQUEST_e;
```

### 5.3 Contactor Data Types

```c
/* Contactor types */
typedef enum {
    CONT_PLUS,
    CONT_MINUS,
    CONT_PRECHARGE,
    CONT_UNDEFINED,
} CONT_TYPE_e;

/* Contactor electrical states */
typedef enum {
    CONT_SWITCH_OFF,
    CONT_SWITCH_ON,
    CONT_SWITCH_UNDEFINED,
} CONT_ELECTRICAL_STATE_TYPE_e;
```

---

## 6. Error Code Definitions

### 6.1 Diagnostic Error Codes

| Code                                    | Value | Description                    |
|-----------------------------------------|-------|--------------------------------|
| DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE        | 0x01  | Cell overvoltage               |
| DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE       | 0x02  | Cell undervoltage              |
| DIAG_ID_CELL_TEMPERATURE_OVERTEMPERATURE| 0x03  | Cell overtemperature           |
| DIAG_ID_CELL_TEMPERATURE_UNDERTEMPERATURE| 0x04 | Cell undertemperature          |
| DIAG_ID_OVERCURRENT_CHARGE              | 0x05  | Charge overcurrent             |
| DIAG_ID_OVERCURRENT_DISCHARGE           | 0x06  | Discharge overcurrent          |
| DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK  | 0x10  | Plus contactor feedback error  |
| DIAG_ID_STRING_MINUS_CONTACTOR_FEEDBACK | 0x11  | Minus contactor feedback error |
| DIAG_ID_PRECHARGE_CONTACTOR_FEEDBACK    | 0x12  | Precharge feedback error       |
| DIAG_ID_AFE_SPI                         | 0x20  | AFE communication error        |
| DIAG_ID_AFE_OPEN_WIRE                   | 0x21  | Open wire detected             |
| DIAG_ID_PRECHARGE_ABORT_REASON_VOLTAGE  | 0x30  | Precharge voltage failure      |
| DIAG_ID_PRECHARGE_ABORT_REASON_CURRENT  | 0x31  | Precharge current failure      |
| DIAG_ID_ALERT_MODE                      | 0x40  | System in alert mode           |
| DIAG_ID_SUPPLY_VOLTAGE_CLAMP_30C_LOST   | 0x50  | 30C supply voltage lost        |

### 6.2 Return Code Summary

| Module     | Function                | Return Codes                    |
|------------|-------------------------|--------------------------------|
| BMS        | BMS_SetStateRequest     | BMS_OK, BMS_REQUEST_PENDING, BMS_ILLEGAL_REQUEST |
| SBC        | SBC_SetStateRequest     | SBC_OK, SBC_REQUEST_PENDING, SBC_ILLEGAL_REQUEST |
| AFE        | AFE_Initialize          | STD_OK, STD_NOT_OK             |
| CONTACTOR  | CONT_OpenContactor      | STD_OK, STD_NOT_OK             |
| DATABASE   | DATA_READ_DATA          | STD_OK, STD_NOT_OK             |

---

## 7. Timing Diagrams

### 7.1 BMS State Machine Timing

```
Time (ms):  0      10      20      30      40      50
            |       |       |       |       |       |
BMS_Trigger:+---+   +---+   +---+   +---+   +---+
                |       |       |       |       |
SOA_Check:      +---+   +---+   +---+   +---+   +---+
                    |       |       |       |
CONT_Check:         +--+    +--+    +--+    +--+
```

### 7.2 Precharge Sequence Timing

```
Time (s):   0    0.1   0.2   0.3   0.4   0.5   1.0   2.0
            |     |     |     |     |     |     |     |
MINUS:      |_____+=====================================+
            |     |
PRECHARGE:  |_____|_____+========+
            |                    |
VOLTAGE:    |     /------/------/
            |    /      /      /
PLUS:       |_____|_____|_____|______+==================+
            |                       |
PRECHARGE:                          +____________________|
```

---

## 8. Traceability

### 8.1 Requirements Traceability

| Interface ID | Requirement ID        | Description                    |
|--------------|----------------------|--------------------------------|
| IF-INT-001   | FBMS-FUNC-INT-001    | BMS to Database interface      |
| IF-INT-002   | FBMS-FUNC-INT-002    | AFE to Database interface      |
| IF-INT-004   | FBMS-SAFETY-INT-001  | SOA to DIAG interface          |
| IF-INT-005   | FBMS-SAFETY-INT-002  | BMS to Contactor interface     |
| IF-INT-006   | FBMS-SAFETY-INT-003  | SBC to SPI interface           |
| IF-EXT-001   | FBMS-FUNC-EXT-001    | CAN bus interface              |
| IF-EXT-002   | FBMS-SAFETY-EXT-001  | AFE communication interface    |

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
