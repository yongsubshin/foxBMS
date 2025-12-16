# foxBMS Software Architecture Design Document

**Document ID**: FBMS-WP-SWE2-001
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.2 (Software Architectural Design)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author          | Description                    |
|---------|------------|-----------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI-Orchestrator | Initial architecture document |

### Approval

| Role                  | Name | Date | Signature |
|-----------------------|------|------|-----------|
| Software Architect    |      |      |           |
| Safety Manager        |      |      |           |
| Quality Manager       |      |      |           |

---

## 1. Introduction

### 1.1 Purpose

This Software Architecture Design Document (SAD) defines the software architecture for the foxBMS Battery Management System (BMS). It establishes the structural decomposition of the software system into components and describes the interfaces between components.

### 1.2 Scope

This document covers:
- High-level software architecture overview
- Component decomposition and responsibilities
- Interface specifications between components
- Safety architecture and ASIL decomposition
- Dynamic behavior of key components

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|------------|
| AFE | Analog Front-End - IC for cell voltage and temperature measurement |
| ASIL | Automotive Safety Integrity Level (A, B, C, D) |
| BMS | Battery Management System |
| CAN | Controller Area Network |
| HAL | Hardware Abstraction Layer |
| RTOS | Real-Time Operating System |
| SBC | System Basis Chip |
| SOC | State of Charge |
| SOE | State of Energy |
| SOF | State of Function |
| SOH | State of Health |
| SOA | Safe Operating Area |
| SPI | Serial Peripheral Interface |

### 1.4 References

| Document ID | Title |
|-------------|-------|
| ISO 26262:2018 | Road vehicles - Functional safety |
| ASPICE v3.1 | Automotive SPICE Process Reference Model |
| FBMS-WP-SWE1-001 | Software Requirements Specification |

---

## 2. Architectural Overview

### 2.1 System Context

The foxBMS software operates on a TMS570LS12x microcontroller (ARM Cortex-R4F based) and manages battery pack monitoring, protection, and control functions. The system interfaces with:

- **External ECUs**: Via CAN bus for vehicle integration
- **Battery Cells**: Via AFE ICs for voltage/temperature measurement
- **Power Electronics**: Via contactors and power stages
- **Diagnostic Tools**: Via CAN/Ethernet for diagnostics

### 2.2 Design Principles

The architecture follows these key principles:

1. **Layered Architecture**: Clear separation between application, service, driver, and HAL layers
2. **Modular Design**: Independent modules with well-defined interfaces
3. **Safety by Design**: ASIL decomposition and freedom from interference
4. **Configurability**: Compile-time and run-time configuration options
5. **Testability**: Design for unit and integration testing

### 2.3 Layer Structure

```
+------------------------------------------------------------------+
|                    APPLICATION LAYER                              |
|  BMS Control | Algorithms | Balancing | SOA | Redundancy         |
+------------------------------------------------------------------+
|                    ENGINE LAYER                                   |
|  Database | Diagnostics | System Monitor | System Control         |
+------------------------------------------------------------------+
|                    DRIVER LAYER                                   |
|  AFE | SBC | Contactor | SPS | CAN | SPI | I2C | Temperature     |
+------------------------------------------------------------------+
|                    HAL LAYER                                      |
|  GPIO | ADC | Timer | DMA | Interrupt | MCU Peripherals          |
+------------------------------------------------------------------+
|                    RTOS LAYER                                     |
|  FreeRTOS / SafeRTOS | Task Management | Scheduling              |
+------------------------------------------------------------------+
|                    HARDWARE                                       |
|  TMS570LS12x MCU | AFE ICs | SBC | CAN Transceiver              |
+------------------------------------------------------------------+
```

---

## 3. Component Architecture

### 3.1 Application Layer Components

#### 3.1.1 BMS Control Component (COMP-APP-BMS)

**Source Location**: `src/app/application/bms/`

**Responsibility**:
- Central state machine controlling BMS operation
- Contactor sequencing and precharge control
- String management and power path control
- Error handling and safe state transitions

**Key Interfaces**:
- Receives state requests from CAN/SYS modules
- Commands CONTACTOR driver for contactor control
- Uses DATABASE for measurement data access
- Interfaces with DIAG for error reporting

**Safety Relevance**: ASIL-D
- Controls contactors (high-power switching)
- Implements safe state transitions
- Handles safety-critical error conditions

**State Machine States**:
- BMS_STATEMACH_UNINITIALIZED
- BMS_STATEMACH_INITIALIZATION
- BMS_STATEMACH_INITIALIZED
- BMS_STATEMACH_IDLE
- BMS_STATEMACH_OPEN_CONTACTORS
- BMS_STATEMACH_STANDBY
- BMS_STATEMACH_PRECHARGE
- BMS_STATEMACH_NORMAL
- BMS_STATEMACH_DISCHARGE
- BMS_STATEMACH_CHARGE
- BMS_STATEMACH_ERROR

#### 3.1.2 Algorithm Component (COMP-APP-ALGO)

**Source Location**: `src/app/application/algorithm/`

**Responsibility**:
- State estimation algorithms (SOC, SOE, SOH, SOF)
- Calculation monitoring and timeout detection
- Algorithm execution scheduling

**Subcomponents**:
- `state_estimation/soc/` - State of Charge calculation
- `state_estimation/soe/` - State of Energy calculation
- `state_estimation/soh/` - State of Health calculation
- `state_estimation/sof/` - State of Function calculation
- `moving_average/` - Moving average filter algorithms

**Key Interfaces**:
- Reads measurement data from DATABASE
- Writes calculated states to DATABASE
- Notified by ALGO manager for execution

**Safety Relevance**: ASIL-C to ASIL-D
- SOC/SOE directly affect range prediction
- SOF affects current limiting decisions

#### 3.1.3 Balancing Component (COMP-APP-BAL)

**Source Location**: `src/app/application/bal/`

**Responsibility**:
- Cell balancing strategy implementation
- Voltage-based balancing control
- Balancing activation/deactivation logic

**Key Interfaces**:
- Receives cell voltage data from DATABASE
- Commands AFE for balancing transistor control
- Configured via BAL_CFG parameters

**Safety Relevance**: ASIL-B
- Prevents cell overcharge during balancing
- Limits balancing current

#### 3.1.4 SOA Component (COMP-APP-SOA)

**Source Location**: `src/app/application/soa/`

**Responsibility**:
- Safe Operating Area monitoring
- Voltage, temperature, current limit checking
- Diagnosis event triggering for limit violations

**Key Interfaces**:
- Reads min/max values from DATABASE
- Reports violations to DIAG module
- Configured via SOA_CFG parameters

**Safety Relevance**: ASIL-D
- Prevents overcharge/overdischarge
- Prevents thermal runaway

#### 3.1.5 Redundancy Component (COMP-APP-RED)

**Source Location**: `src/app/application/redundancy/`

**Responsibility**:
- Redundant measurement validation
- Plausibility checking of measurements
- Cross-validation of measurement sources

**Key Interfaces**:
- Reads measurements from multiple DATABASE entries
- Reports discrepancies to DIAG module

**Safety Relevance**: ASIL-D
- Detects measurement failures
- Enables degraded operation

#### 3.1.6 Plausibility Component (COMP-APP-PLAUS)

**Source Location**: `src/app/application/plausibility/`

**Responsibility**:
- Cell voltage plausibility checks
- Temperature plausibility checks
- Pack voltage plausibility checks

**Key Interfaces**:
- Receives measurement data
- Reports plausibility errors to DIAG

**Safety Relevance**: ASIL-C to ASIL-D

### 3.2 Engine Layer Components

#### 3.2.1 Database Component (COMP-ENG-DB)

**Source Location**: `src/app/engine/database/`

**Responsibility**:
- Central data storage for all BMS data
- Thread-safe data access via queues
- Data timestamping and validity tracking

**Key Interfaces**:
- DATA_READ_DATA() - Read data blocks
- DATA_WRITE_DATA() - Write data blocks
- Provides variadic macros for multi-block access

**Safety Relevance**: ASIL-B
- Data integrity mechanisms
- Access synchronization

**Data Blocks**:
- Cell voltages (per string, per cell)
- Cell temperatures
- Pack values (current, voltage)
- SOC/SOE/SOH/SOF values
- Contactor states
- Diagnostic flags

#### 3.2.2 Diagnostics Component (COMP-ENG-DIAG)

**Source Location**: `src/app/engine/diag/`

**Responsibility**:
- Error detection and recording
- Error counter management
- Severity classification (warning, error, fatal)
- Callback invocation for error handling

**Key Interfaces**:
- DIAG_Handler() - Main error handling entry point
- DIAG_CheckEvent() - Simplified event checking
- DIAG_IsAnyFatalErrorSet() - Fatal error query

**Safety Relevance**: ASIL-D
- Implements diagnostic monitoring per ISO 26262
- Triggers safe state transitions

**Error Severity Levels**:
- Warning: Logged but no action
- Error: Counter incremented, may trigger action
- Fatal: Immediate safe state transition required

#### 3.2.3 System Monitor Component (COMP-ENG-SYSMON)

**Source Location**: `src/app/engine/sys_mon/`

**Responsibility**:
- Task execution monitoring
- Watchdog triggering verification
- System health monitoring

**Key Interfaces**:
- Monitors task cycle times
- Reports to DIAG on timing violations

**Safety Relevance**: ASIL-D
- Detects software lock-ups

#### 3.2.4 System Control Component (COMP-ENG-SYS)

**Source Location**: `src/app/engine/sys/`

**Responsibility**:
- Overall system state management
- Initialization sequencing
- Power mode management

**Key Interfaces**:
- Coordinates initialization of all modules
- Manages system-wide state transitions

**Safety Relevance**: ASIL-C

### 3.3 Driver Layer Components

#### 3.3.1 AFE Driver Component (COMP-DRV-AFE)

**Source Location**: `src/app/driver/afe/`

**Subcomponents by Vendor**:
- `adi/` - Analog Devices ADES183x drivers
- `maxim/` - Maxim MAX1785x drivers
- `ltc/` - Linear Technology LTC6811/6813 drivers
- `nxp/` - NXP MC33775A drivers

**Responsibility**:
- AFE IC communication via SPI/isoSPI
- Cell voltage measurement acquisition
- Cell temperature measurement acquisition
- Open wire detection
- Balancing transistor control
- AFE self-test execution

**Key Interfaces**:
- SPI driver for communication
- DATABASE for measurement storage
- DIAG for error reporting

**Safety Relevance**: ASIL-D
- Critical for voltage/temperature monitoring
- Open wire detection is safety-critical
- CRC/PEC validation for communication integrity

**Safety Mechanisms**:
- CRC validation on all communication
- Command counter verification
- Register readback verification
- Redundant ADC measurements
- Open wire detection via pull-up/pull-down

#### 3.3.2 SBC Driver Component (COMP-DRV-SBC)

**Source Location**: `src/app/driver/sbc/`

**Responsibility**:
- System Basis Chip (NXP FS85xx) control
- Watchdog management
- Power supply supervision
- Safe state output control (FS0B)

**Key Interfaces**:
- SPI for SBC communication
- GPIO for status inputs
- DIAG for error reporting

**Safety Relevance**: ASIL-D
- Hardware watchdog for MCU monitoring
- Fail-safe output for contactor control
- Power supply monitoring

**Safety Mechanisms**:
- LBIST/ABIST verification
- OTP CRC verification
- DATA/DATA_NOT register verification
- RSTB/FS0B path checking
- Error counter monitoring

#### 3.3.3 Contactor Driver Component (COMP-DRV-CONT)

**Source Location**: `src/app/driver/contactor/`

**Responsibility**:
- Contactor state machine control
- Contactor feedback monitoring
- Current flow direction determination

**Key Interfaces**:
- SPS driver for contactor power control
- IO driver for feedback reading
- DIAG for feedback error reporting

**Safety Relevance**: ASIL-D
- Controls high-power switching
- Feedback validation required

#### 3.3.4 Temperature Sensor Driver Component (COMP-DRV-TS)

**Source Location**: `src/app/driver/ts/`

**Subcomponents by Manufacturer**:
- `epcos/` - EPCOS NTC sensors
- `vishay/` - Vishay NTC sensors
- `murata/` - Murata NTC sensors
- `tdk/` - TDK NTC sensors
- `semitec/` - Semitec NTC sensors

**Responsibility**:
- NTC resistance to temperature conversion
- Lookup table or polynomial calculation
- Error handling for out-of-range values

**Key Interfaces**:
- Receives ADC/GPIO voltage readings
- Returns temperature in decidegrees Celsius

**Safety Relevance**: ASIL-C to ASIL-D
- Temperature monitoring for thermal protection

#### 3.3.5 SPS Driver Component (COMP-DRV-SPS)

**Source Location**: `src/app/driver/sps/`

**Responsibility**:
- Smart Power Switch control
- Contactor power stage control
- Channel state management

**Key Interfaces**:
- SPI for SPS IC communication
- Commanded by CONTACTOR driver

**Safety Relevance**: ASIL-C

#### 3.3.6 CAN Driver Component (COMP-DRV-CAN)

**Source Location**: `src/app/driver/can/`

**Responsibility**:
- CAN message transmission and reception
- Message filtering and routing
- TX/RX buffer management

**Key Interfaces**:
- HAL CAN peripheral interface
- APPLICATION layer for message handling

**Safety Relevance**: ASIL-B
- Communication integrity via CAN CRC

#### 3.3.7 SPI Driver Component (COMP-DRV-SPI)

**Source Location**: `src/app/driver/spi/`

**Responsibility**:
- SPI bus management
- DMA-based data transfer
- Chip select control

**Key Interfaces**:
- HAL SPI peripheral interface
- AFE, SBC, SPS drivers

**Safety Relevance**: ASIL-B
- Data integrity mechanisms

#### 3.3.8 ADC Driver Component (COMP-DRV-ADC)

**Source Location**: `src/app/driver/adc/`

**Responsibility**:
- Internal ADC management
- Auxiliary voltage measurements
- Pack current measurement input

**Key Interfaces**:
- HAL ADC peripheral interface
- DATABASE for result storage

**Safety Relevance**: ASIL-B

### 3.4 HAL Layer Components

#### 3.4.1 MCU Abstraction (COMP-HAL-MCU)

**Source Location**: `src/app/hal/`

**Responsibility**:
- TMS570 peripheral abstraction
- Register access encapsulation
- Interrupt management

**Safety Relevance**: ASIL-B

### 3.5 Task Layer Components

#### 3.5.1 Task Management (COMP-TASK)

**Source Location**: `src/app/task/`

**Responsibility**:
- RTOS task definitions
- Task timing configuration
- Task startup sequencing

**Key Tasks**:
- 1ms Task: High-priority timing critical
- 10ms Task: BMS state machine, SBC trigger
- 100ms Task: Algorithm execution, SOA checking
- Idle Task: Background processing

**Safety Relevance**: ASIL-C
- Task scheduling determines system responsiveness

---

## 4. Interface Specifications

### 4.1 Internal Interfaces

#### 4.1.1 BMS to DATABASE Interface

**Interface ID**: IF-INT-001

**Direction**: Bidirectional

**Data Exchanged**:
- Read: Pack values, cell voltages, temperatures, SOC/SOE
- Write: BMS state, contactor commands

**Mechanism**: DATA_READ_DATA() / DATA_WRITE_DATA() macros

**Timing**: 10ms cycle

**Safety Classification**: ASIL-D

#### 4.1.2 AFE to DATABASE Interface

**Interface ID**: IF-INT-002

**Direction**: Write (AFE to DATABASE)

**Data Exchanged**:
- Cell voltages per string
- Cell temperatures per string
- Open wire status
- AFE status flags

**Mechanism**: DATA_WRITE_DATA() macro

**Timing**: 100ms cycle (configurable)

**Safety Classification**: ASIL-D

#### 4.1.3 ALGO to DATABASE Interface

**Interface ID**: IF-INT-003

**Direction**: Bidirectional

**Data Exchanged**:
- Read: Voltages, temperatures, currents
- Write: SOC, SOE, SOH, SOF values

**Mechanism**: DATA_READ_DATA() / DATA_WRITE_DATA() macros

**Timing**: 100ms cycle

**Safety Classification**: ASIL-C

#### 4.1.4 SOA to DIAG Interface

**Interface ID**: IF-INT-004

**Direction**: SOA to DIAG

**Data Exchanged**:
- Voltage limit violations
- Temperature limit violations
- Current limit violations

**Mechanism**: DIAG_Handler() function calls

**Timing**: Event-driven

**Safety Classification**: ASIL-D

#### 4.1.5 BMS to CONTACTOR Interface

**Interface ID**: IF-INT-005

**Direction**: BMS to CONTACTOR

**Data Exchanged**:
- Contactor open/close commands
- String selection

**Mechanism**: Direct function calls

**Timing**: 10ms cycle

**Safety Classification**: ASIL-D

#### 4.1.6 SBC to SPI Interface

**Interface ID**: IF-INT-006

**Direction**: Bidirectional

**Data Exchanged**:
- SBC register read/write
- Watchdog trigger commands
- Status queries

**Mechanism**: SPI frame transactions

**Timing**: 100ms watchdog cycle

**Safety Classification**: ASIL-D

### 4.2 External Interfaces

#### 4.2.1 CAN Bus Interface

**Interface ID**: IF-EXT-001

**Protocol**: CAN 2.0B

**Baud Rate**: 500 kbps (configurable)

**Message Types**:
- TX: BMS state, cell voltages, temperatures, SOC, errors
- RX: Control commands, configuration updates

**Safety Classification**: ASIL-B (QM for non-safety messages)

#### 4.2.2 AFE SPI/isoSPI Interface

**Interface ID**: IF-EXT-002

**Protocol**: SPI Mode 0/3 or isoSPI

**Data Format**: Vendor-specific command/response frames

**Safety Mechanisms**:
- CRC/PEC on all frames
- Command counter validation
- Readback verification

**Safety Classification**: ASIL-D

---

## 5. Safety Architecture

### 5.1 Safety Concept Overview

The foxBMS safety architecture implements multiple layers of protection:

1. **Primary Protection**: SOA monitoring with immediate response
2. **Secondary Protection**: Redundant measurement validation
3. **Tertiary Protection**: Hardware watchdog (SBC) for MCU failure
4. **Quaternary Protection**: External fuse for ultimate protection

### 5.2 ASIL Decomposition

| Component | Allocated ASIL | Decomposition Rationale |
|-----------|----------------|------------------------|
| BMS Control | ASIL-D | Controls contactors, no decomposition |
| AFE Driver | ASIL-D | Primary measurement source |
| SBC Driver | ASIL-D | Hardware watchdog, fail-safe outputs |
| SOA | ASIL-D | Limit monitoring, no decomposition |
| Algorithms | ASIL-C | SOC/SOE can use redundant estimation |
| Database | ASIL-B | Data integrity, not safety function |
| CAN Driver | ASIL-B | Communication, not safety-critical |
| Balancing | ASIL-B | Limited by hardware current |

### 5.3 Freedom from Interference

#### 5.3.1 Spatial Partitioning

- ASIL-D functions use dedicated memory sections
- Critical data structures have CRC protection
- Stack overflow detection via hardware MPU

#### 5.3.2 Temporal Partitioning

- Time-triggered architecture with fixed task periods
- Watchdog monitoring of task execution
- Maximum execution time limits per task

### 5.4 Safe States

| Safe State | Trigger Condition | Action |
|------------|-------------------|--------|
| SS-1: Open Contactors | Fatal error detected | Open all contactors immediately |
| SS-2: Current Limiting | SOA violation | Reduce current limits to zero |
| SS-3: Balancing Stop | Temperature limit | Disable all balancing |
| SS-4: MCU Reset | Watchdog timeout | SBC initiates MCU reset |

### 5.5 Safety Mechanisms

#### 5.5.1 Software Safety Mechanisms

| Mechanism | Description | Coverage |
|-----------|-------------|----------|
| FAS_ASSERT | Runtime assertion checking | Logic errors |
| FAS_TRAP | Invalid state detection | State machine errors |
| CRC Protection | Data integrity checking | Memory corruption |
| Timeout Monitoring | Watchdog and timing checks | Timing failures |
| Range Checking | Parameter validation | Invalid inputs |
| Pointer Validation | Null pointer checks | Memory access errors |

#### 5.5.2 Hardware Safety Mechanisms

| Mechanism | Description | Coverage |
|-----------|-------------|----------|
| ECC Memory | Error correcting code | Memory bit flips |
| Hardware Watchdog | SBC watchdog | MCU lock-up |
| Voltage Supervisor | SBC voltage monitoring | Power failures |
| MPU | Memory protection unit | Memory corruption |
| CPU Self-Test | LBIST/ABIST | CPU failures |

---

## 6. Dynamic Behavior

### 6.1 Startup Sequence

1. MCU reset and SBC initialization
2. RTOS kernel start
3. Task creation and scheduling start
4. Database initialization
5. Driver initialization (HAL, SPI, CAN)
6. AFE initialization and communication check
7. Measurement acquisition start
8. BMS state machine to INITIALIZED
9. System ready for operation

### 6.2 Normal Operation Cycle

**10ms Cycle**:
- BMS state machine trigger
- SBC watchdog trigger
- Contactor state update

**100ms Cycle**:
- AFE measurement acquisition
- Algorithm execution (SOC, SOE, SOH)
- SOA limit checking
- CAN message transmission

### 6.3 Error Handling Sequence

1. Error detected by monitoring function
2. DIAG_Handler() called with error ID
3. Error counter incremented
4. If threshold exceeded: Fatal error flag set
5. BMS transitions to ERROR state
6. Contactors opened in safe sequence
7. Error logged and reported via CAN

### 6.4 Precharge Sequence

1. BMS receives standby request
2. Transition to PRECHARGE state
3. Close minus contactor
4. Close precharge contactor
5. Monitor voltage rise (timeout check)
6. Verify voltage within tolerance
7. Close plus contactor
8. Open precharge contactor
9. Transition to NORMAL state

---

## 7. Configuration Management

### 7.1 Compile-Time Configuration

Configuration files in `src/app/*/config/`:
- `battery_system_cfg.h` - Battery topology
- `battery_cell_cfg.h` - Cell parameters
- `bms_cfg.h` - BMS operation parameters
- `soa_cfg.h` - SOA limits
- `bal_cfg.h` - Balancing parameters

### 7.2 Run-Time Configuration

- CAN-based parameter updates
- FRAM-stored calibration data
- Non-volatile error logging

---

## 8. Traceability

### 8.1 Requirements to Architecture Traceability

See: `/docs/parvis/architecture/allocation-matrix.json`

### 8.2 Architecture to Design Traceability

Detailed design documents provide mapping from architecture components to implementation modules.

---

## 9. Appendices

### 9.1 Component Catalog

| Component ID | Name | Layer | ASIL |
|--------------|------|-------|------|
| COMP-APP-BMS | BMS Control | Application | D |
| COMP-APP-ALGO | Algorithm | Application | C |
| COMP-APP-BAL | Balancing | Application | B |
| COMP-APP-SOA | SOA Monitor | Application | D |
| COMP-APP-RED | Redundancy | Application | D |
| COMP-APP-PLAUS | Plausibility | Application | C |
| COMP-ENG-DB | Database | Engine | B |
| COMP-ENG-DIAG | Diagnostics | Engine | D |
| COMP-ENG-SYSMON | System Monitor | Engine | D |
| COMP-ENG-SYS | System Control | Engine | C |
| COMP-DRV-AFE | AFE Driver | Driver | D |
| COMP-DRV-SBC | SBC Driver | Driver | D |
| COMP-DRV-CONT | Contactor | Driver | D |
| COMP-DRV-TS | Temperature | Driver | C |
| COMP-DRV-SPS | Smart Power Switch | Driver | C |
| COMP-DRV-CAN | CAN | Driver | B |
| COMP-DRV-SPI | SPI | Driver | B |
| COMP-DRV-ADC | ADC | Driver | B |
| COMP-HAL-MCU | MCU HAL | HAL | B |
| COMP-TASK | Task Management | OS | C |

### 9.2 Glossary

See Section 1.3 for definitions and acronyms.

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L2 Phase (Software Architecture Design)*
*ASPICE SWE.2 Compliance*
