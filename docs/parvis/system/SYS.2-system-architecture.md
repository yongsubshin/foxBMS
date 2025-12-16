# foxBMS System Architecture Design Document

**Document ID**: FBMS-WP-SYS2-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Released
**Classification**: Technical
**ASPICE Process**: SYS.2 (System Architecture Design)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author          | Description                    |
|---------|------------|-----------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI | Initial system architecture |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| System Architect      |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This System Architecture Design Document defines the high-level architecture of the foxBMS Battery Management System. It describes the decomposition of the system into hardware and software elements, their interfaces, and the allocation of system requirements to these elements.

### 1.2 Scope

This document covers:
- System decomposition into HW and SW elements
- Hardware/Software allocation
- System block diagrams
- Interface definitions between system elements
- Safety architecture and ASIL allocation

### 1.3 References

| Document ID | Title |
|-------------|-------|
| FBMS-WP-SYS1-001 | System Requirements Specification |
| FBMS-WP-SWE2-001 | Software Architecture Design |
| ISO 26262:2018 Part 4 | Product development at system level |

---

## 2. System Architecture Overview

### 2.1 System Context Diagram

```
+------------------------------------------------------------------+
|                     EXTERNAL ENVIRONMENT                          |
+------------------------------------------------------------------+
        |              |              |              |
        v              v              v              v
+------------+  +------------+  +------------+  +------------+
|  Vehicle   |  |  Charger   |  |  Battery   |  |   User     |
|    ECU     |  |   System   |  |   Pack     |  |  Service   |
+------------+  +------------+  +------------+  +------------+
        |              |              |              |
        v              v              v              v
+------------------------------------------------------------------+
|                      foxBMS SYSTEM                                |
|  +------------------------------------------------------------+  |
|  |                    BMS CONTROLLER                           |  |
|  |  +--------+  +--------+  +--------+  +--------+            |  |
|  |  |  MCU   |  |  SBC   |  |  AFE   |  | Power  |            |  |
|  |  | (SW)   |  | (HW)   |  | (HW)   |  | Stage  |            |  |
|  |  +--------+  +--------+  +--------+  +--------+            |  |
|  +------------------------------------------------------------+  |
|                              |                                    |
|                              v                                    |
|  +------------------------------------------------------------+  |
|  |                    CONTACTORS                               |  |
|  |  [PLUS]    [MINUS]    [PRECHARGE]                          |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### 2.2 System Decomposition

The foxBMS system is decomposed into the following major elements:

| Element ID | Element Name | Type | Description |
|------------|--------------|------|-------------|
| SYS-HW-MCU | Microcontroller Unit | Hardware | TMS570LS12x ARM Cortex-R4F |
| SYS-HW-SBC | System Basis Chip | Hardware | NXP FS85xx power/safety IC |
| SYS-HW-AFE | Analog Front-End | Hardware | Cell measurement IC |
| SYS-HW-CONT | Contactors | Hardware | High-power switches |
| SYS-HW-SPS | Smart Power Switch | Hardware | Contactor drive stage |
| SYS-HW-CAN | CAN Transceiver | Hardware | CAN bus interface |
| SYS-HW-PWR | Power Supply | Hardware | Voltage regulators |
| SYS-SW-APP | Application Software | Software | BMS application logic |
| SYS-SW-DRV | Driver Software | Software | Hardware drivers |
| SYS-SW-RTOS | RTOS | Software | Real-time operating system |

---

## 3. Hardware Architecture

### 3.1 Hardware Block Diagram

```
                                    +-------------------+
                                    |   BATTERY PACK    |
                                    | +---+  +---+  +---+
                                    | |C1 |..|Cn |  |Tn |
                                    | +---+  +---+  +---+
                                    +--------+----------+
                                             |
                    +------------------------+------------------------+
                    |                        |                        |
                    v                        v                        v
            +---------------+        +---------------+        +---------------+
            |    AFE #1     |        |    AFE #2     |  ...   |    AFE #N     |
            | (ADES1830/    |        | (ADES1830/    |        | (ADES1830/    |
            |  LTC6813/     |        |  LTC6813/     |        |  LTC6813/     |
            |  MAX17853)    |        |  MAX17853)    |        |  MAX17853)    |
            +-------+-------+        +-------+-------+        +-------+-------+
                    |                        |                        |
                    +------------------------+------------------------+
                                             |
                                      isoSPI / SPI
                                             |
+-------------------------------------------------------------------------+
|                              MCU BOARD                                   |
|  +----------------+    +----------------+    +----------------+          |
|  |   TMS570LS12x  |    |   NXP FS85xx   |    |  CAN Trans-   |          |
|  |                |<-->|     (SBC)      |    |   ceiver      |          |
|  | - ARM Cortex-R4|    | - Watchdog     |    | - TJA1043     |          |
|  | - 160MHz       |    | - VCORE        |    +-------+-------+          |
|  | - 1.25MB Flash |    | - FS0B Output  |            |                  |
|  | - 192KB RAM    |    +-------+--------+      CAN1 / CAN2              |
|  +-------+--------+            |                     |                  |
|          |                     |                     v                  |
|          |              FAIL-SAFE               +---------+             |
|          |                OUTPUT                | Vehicle |             |
|          |                     |                |   ECU   |             |
|          v                     v                +---------+             |
|  +----------------+    +----------------+                               |
|  | Smart Power    |    |   Contactor    |                               |
|  |   Switch       |--->|   Control      |                               |
|  |  (SPS/NCV7718) |    +-------+--------+                               |
|  +----------------+            |                                        |
+-------------------------------------------------------------------------+
                                 |
                                 v
                    +------------------------+
                    |      CONTACTORS        |
                    | [+]   [-]   [PRE]      |
                    +------------------------+
                                 |
                                 v
                    +------------------------+
                    |     HV BUS OUTPUT      |
                    +------------------------+
```

### 3.2 Hardware Element Specifications

#### 3.2.1 MCU (SYS-HW-MCU)

| Attribute | Specification |
|-----------|--------------|
| Device | TMS570LS12x |
| Architecture | ARM Cortex-R4F (dual-core lockstep) |
| Clock | 160 MHz |
| Flash | 1.25 MB (ECC protected) |
| RAM | 192 KB (ECC protected) |
| Safety | ASIL-D capable, IEC 61508 SIL3 |
| Peripherals | CAN, SPI, ADC, GPIO, Timer |

**Safety Features**:
- Dual-core lockstep with comparison
- ECC on Flash and RAM
- Memory protection unit (MPU)
- Built-in self-test (BIST)
- Clock monitoring
- Voltage monitoring

#### 3.2.2 SBC (SYS-HW-SBC)

| Attribute | Specification |
|-----------|--------------|
| Device | NXP FS8530 / FS8536 |
| Supply | 10V to 32V input |
| Outputs | 5V, 3.3V regulated |
| Watchdog | Window watchdog (ASIL-D) |
| Fail-Safe | FS0B output for contactor control |

**Safety Features**:
- LBIST/ABIST for self-diagnosis
- Fail-safe output (FS0B)
- Voltage monitoring
- CRC-protected OTP
- Independent watchdog

#### 3.2.3 AFE (SYS-HW-AFE)

| Attribute | Specification |
|-----------|--------------|
| Supported ICs | ADI ADES183x, LTC6811/6813, MAX17853, NXP MC33775A |
| Cells per IC | 12-18 depending on variant |
| Voltage Range | 0V to 5V per cell |
| Accuracy | +/-2mV |
| Communication | SPI / isoSPI |

**Safety Features**:
- CRC on all communication
- Redundant ADC measurements
- Open wire detection
- Overvoltage/undervoltage comparators
- Internal self-test

#### 3.2.4 Contactors (SYS-HW-CONT)

| Attribute | Specification |
|-----------|--------------|
| Types | Main Plus, Main Minus, Precharge |
| Voltage Rating | 450V DC minimum |
| Current Rating | 300A continuous (configurable) |
| Coil Voltage | 12V nominal |
| Feedback | Auxiliary contacts |

#### 3.2.5 Smart Power Switch (SYS-HW-SPS)

| Attribute | Specification |
|-----------|--------------|
| Device | NCV7718 / TLE75008 |
| Channels | 8 high-side switches |
| Current | 1A per channel |
| Diagnostics | Open load, overcurrent, overtemperature |

---

## 4. Software Architecture

### 4.1 Software Layer Structure

```
+------------------------------------------------------------------+
|                    APPLICATION LAYER (ASIL-D)                     |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|  |   BMS    | |   SOA    | |  ALGO    | |   BAL    | |   RED    | |
|  | Control  | | Monitor  | |(SOC/SOH) | |Balancing | |Redundancy| |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
+------------------------------------------------------------------+
|                    ENGINE LAYER (ASIL-C)                          |
|  +----------+ +----------+ +----------+ +----------+              |
|  | Database | |   Diag   | |  SysMon  | |   SYS    |              |
|  |  (DATA)  | |          | |          | |          |              |
|  +----------+ +----------+ +----------+ +----------+              |
+------------------------------------------------------------------+
|                    DRIVER LAYER (ASIL-B/C)                        |
|  +------+ +------+ +------+ +------+ +------+ +------+ +------+  |
|  | AFE  | | SBC  | | CONT | |  TS  | | SPS  | | CAN  | | SPI  |  |
|  +------+ +------+ +------+ +------+ +------+ +------+ +------+  |
+------------------------------------------------------------------+
|                    HAL LAYER (QM/ASIL-B)                          |
|  +----------+ +----------+ +----------+ +----------+              |
|  |   GPIO   | |   ADC    | |  Timer   | |   DMA    |              |
|  +----------+ +----------+ +----------+ +----------+              |
+------------------------------------------------------------------+
|                    RTOS LAYER (ASIL-B)                            |
|  +----------------------------------------------------------+    |
|  |              FreeRTOS / SafeRTOS                          |    |
|  +----------------------------------------------------------+    |
+------------------------------------------------------------------+
```

### 4.2 Software Element Allocation

| SW Element | HW Element | ASIL | Functions |
|------------|-----------|------|-----------|
| BMS Control | MCU | ASIL-D | State machine, contactor sequencing |
| SOA Monitor | MCU | ASIL-D | Limit monitoring, protection |
| Algorithm | MCU | ASIL-C | SOC, SOH, SOE, SOF estimation |
| Balancing | MCU | ASIL-B | Cell balancing control |
| Redundancy | MCU | ASIL-D | Measurement cross-validation |
| Database | MCU | ASIL-B | Central data storage |
| Diagnostics | MCU | ASIL-D | Fault detection and handling |
| AFE Driver | MCU+AFE | ASIL-D | Cell measurement acquisition |
| SBC Driver | MCU+SBC | ASIL-D | Watchdog, power management |
| Contactor Driver | MCU+SPS+CONT | ASIL-D | Contactor control |

---

## 5. HW/SW Allocation Matrix

### 5.1 System Requirements to Element Allocation

| System Req | HW Allocation | SW Allocation | ASIL |
|------------|---------------|---------------|------|
| TSR-001 (Cell Voltage) | AFE | AFE Driver, Database | ASIL-D |
| TSR-002 (Temperature) | AFE, NTC | TS Driver, Database | ASIL-D |
| TSR-003 (Current) | Hall Sensor, ADC | MEAS Driver, Database | ASIL-D |
| TSR-004 (Contactor Control) | SPS, Contactors | CONT Driver, BMS | ASIL-D |
| TSR-005 (Precharge) | SPS, Contactors | BMS Control | ASIL-C |
| TSR-006 (SOA Monitoring) | MCU | SOA Module | ASIL-D |
| TSR-007 (Fault Detection) | MCU | DIAG Module | ASIL-D |
| TSR-008 (Safe State) | SBC, SPS | BMS Control, SBC Driver | ASIL-D |
| TSR-009 (Watchdog) | SBC | SBC Driver | ASIL-D |
| TSR-010 (Communication) | CAN Transceiver | CAN Driver | ASIL-C |

### 5.2 Safety Element Allocation

```
+------------------------------------------------------------------+
|                    SAFETY ARCHITECTURE                            |
+------------------------------------------------------------------+
|                                                                    |
|  PRIMARY PROTECTION PATH (ASIL-D)                                 |
|  +----------+    +----------+    +----------+    +----------+     |
|  |   AFE    |--->|    SW    |--->|   SPS    |--->| CONTACTOR|     |
|  |Measurement|   |BMS+SOA+  |   |  Driver  |   |  Control  |     |
|  +----------+    |   DIAG   |    +----------+    +----------+     |
|                  +----------+                                      |
|                                                                    |
|  SECONDARY PROTECTION PATH (ASIL-D)                               |
|  +----------+    +----------+    +----------+                     |
|  |   SBC    |--->|  FS0B    |--->| CONTACTOR|                     |
|  | Watchdog |    |  Output  |    |  Driver  |                     |
|  +----------+    +----------+    +----------+                     |
|                                                                    |
|  TERTIARY PROTECTION (QM - External)                              |
|  +----------+                                                      |
|  |   FUSE   |  <- Physical protection, independent of BMS         |
|  +----------+                                                      |
|                                                                    |
+------------------------------------------------------------------+
```

---

## 6. Interface Definitions

### 6.1 System Internal Interfaces

#### IF-SYS-001: MCU to AFE Interface

| Attribute | Value |
|-----------|-------|
| Physical | SPI / isoSPI (isolated) |
| Data Rate | 1-2 Mbps |
| Protocol | AFE-specific command/response |
| Safety | CRC on all frames |

#### IF-SYS-002: MCU to SBC Interface

| Attribute | Value |
|-----------|-------|
| Physical | SPI |
| Data Rate | 4 MHz |
| Protocol | FS85xx register access |
| Safety | Watchdog answer, CRC |

#### IF-SYS-003: MCU to SPS Interface

| Attribute | Value |
|-----------|-------|
| Physical | SPI |
| Data Rate | 2 MHz |
| Protocol | Register read/write |
| Safety | Diagnostic readback |

#### IF-SYS-004: SPS to Contactor Interface

| Attribute | Value |
|-----------|-------|
| Physical | Power output (12V, 1A) |
| Control | PWM capable |
| Feedback | Voltage sense, current sense |

#### IF-SYS-005: Contactor Feedback Interface

| Attribute | Value |
|-----------|-------|
| Physical | GPIO input |
| Signal | Auxiliary contact state |
| Sampling | 10ms |

### 6.2 System External Interfaces

#### IF-EXT-001: CAN Bus Interface

| Attribute | Value |
|-----------|-------|
| Physical | CAN 2.0B (ISO 11898) |
| Speed | 500 kbps |
| Connector | OEM-specific |
| Messages | TX: Status, Measurements; RX: Commands |

#### IF-EXT-002: Power Supply Interface

| Attribute | Value |
|-----------|-------|
| Voltage | 10V to 32V DC |
| Current | 500mA typical, 2A peak |
| Protection | Reverse polarity, overvoltage |

#### IF-EXT-003: HV Bus Interface

| Attribute | Value |
|-----------|-------|
| Voltage | Up to 450V DC |
| Current | Up to 500A |
| Connection | Via contactors only |

---

## 7. Safety Architecture

### 7.1 ASIL Decomposition

The system achieves ASIL-D by combining independent protection paths:

| Path | ASIL | Description |
|------|------|-------------|
| Primary | ASIL-D | SW-based monitoring and control |
| Secondary | ASIL-D | SBC watchdog with FS0B |
| Combined | ASIL-D | Redundant paths ensure ASIL-D |

### 7.2 Freedom from Interference

#### 7.2.1 Hardware FFI

- Isolated power domains for safety-critical circuits
- Separate voltage regulators for MCU and SBC
- Physical separation of HV and LV circuits
- EMC protection on all interfaces

#### 7.2.2 Software FFI

- Memory protection via MPU
- Task isolation via RTOS
- ASIL partitioning at software layer boundaries
- Time-triggered architecture

### 7.3 Diagnostic Coverage

| Fault Category | Detection Mechanism | Coverage |
|----------------|---------------------|----------|
| MCU Failure | Dual-core lockstep, ECC, BIST | 99% |
| SBC Failure | LBIST/ABIST, CRC | 95% |
| AFE Failure | CRC, redundant ADC, self-test | 99% |
| Contactor Failure | Feedback monitoring | 90% |
| Communication Failure | CRC, timeout, counter | 99% |

---

## 8. Dynamic Behavior

### 8.1 System Startup Sequence

```
[Power Applied]
     |
     v
+------------+
| SBC Init   | <- Voltage ramp, watchdog init
+------------+
     |
     v
+------------+
| MCU Boot   | <- Flash check, RAM init, BIST
+------------+
     |
     v
+------------+
| RTOS Start | <- Task creation, scheduling
+------------+
     |
     v
+------------+
| Driver Init| <- SPI, CAN, GPIO initialization
+------------+
     |
     v
+------------+
| AFE Init   | <- Communication check, configuration
+------------+
     |
     v
+------------+
| BMS Init   | <- State machine to IDLE
+------------+
     |
     v
[System Ready]
```

### 8.2 Normal Operation Mode

- AFE measurements acquired every 100ms
- SOA limits checked continuously
- SOC/SOH updated every 100ms
- CAN messages transmitted per schedule
- Watchdog triggered every 100ms

### 8.3 Safe State Transition

```
[Fatal Error Detected]
     |
     v
+-------------------+
| DIAG: Fatal Flag  |
+-------------------+
     |
     v
+-------------------+
| BMS -> ERROR      |
+-------------------+
     |
     v
+-------------------+     +-------------------+
| Open PLUS Contactor|     | SBC: FS0B Assert |
| (SW Path)          | OR  | (HW Path)         |
+-------------------+     +-------------------+
     |                           |
     +-------------+-------------+
                   |
                   v
          +-------------------+
          | All Contactors    |
          | OPEN              |
          +-------------------+
                   |
                   v
          [SAFE STATE ACHIEVED]
```

---

## 9. Traceability

### 9.1 SYS.1 to SYS.2 Traceability

| SYS.1 Requirement | SYS.2 Element | Rationale |
|-------------------|---------------|-----------|
| TSR-001 | SYS-HW-AFE, AFE Driver | Cell voltage measurement |
| TSR-002 | SYS-HW-AFE, TS Driver | Temperature measurement |
| TSR-003 | SYS-HW-MCU ADC, MEAS Driver | Current measurement |
| TSR-004 | SYS-HW-CONT, SYS-HW-SPS, CONT Driver | Contactor control |
| TSR-005 | SYS-SW-APP (BMS) | Precharge logic |
| TSR-006 | SYS-SW-APP (SOA) | SOA monitoring |
| TSR-007 | SYS-SW-APP (DIAG) | Fault handling |
| TSR-008 | SYS-SW-APP (BMS), SYS-HW-SBC | Safe state |
| TSR-009 | SYS-HW-SBC, SBC Driver | Watchdog |
| TSR-010 | SYS-HW-CAN, CAN Driver | Communication |

---

## 10. Appendices

### 10.1 Component List

| Component | Part Number | Manufacturer | ASIL Capability |
|-----------|------------|--------------|-----------------|
| MCU | TMS570LS1227 | Texas Instruments | ASIL-D |
| SBC | FS8530 | NXP | ASIL-D |
| AFE | ADES1830 | Analog Devices | ASIL-D |
| CAN | TJA1043 | NXP | ASIL-B |
| SPS | NCV7718 | onsemi | ASIL-B |

### 10.2 Block Diagram Legend

| Symbol | Meaning |
|--------|---------|
| ---> | Data/signal flow |
| [+] [-] [PRE] | Contactors (Plus, Minus, Precharge) |
| C1..Cn | Battery cells |
| Tn | Temperature sensors |

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-12-16 | Initial release |

---

**Generated by**: PARVIS-AI System Architecture Design
**Project**: foxBMS Battery Management System
**Compliance**: ISO 26262:2018, ASPICE 3.1 SYS.2
