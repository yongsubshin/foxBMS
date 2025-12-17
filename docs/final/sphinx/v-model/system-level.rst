.. foxBMS System Level Process Documentation

================================
System Level (SYS.1 - SYS.5)
================================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

This section documents the system-level V-Model processes for the foxBMS Battery Management System.

.. contents:: Contents
   :local:
   :depth: 2

SYS.1 - System Requirements Analysis
=====================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SYS1-001

**Status**: Released

**Purpose**: Define system-level requirements for the foxBMS BMS including functional, safety, and interface requirements.

Key Metrics
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Metric
     - Value
   * - Total System Requirements
     - 10 TSR + 5 Safety Goals
   * - ASIL Classification
     - ASIL-D (Primary)
   * - SW Requirements Derived
     - 648
   * - Traceability Coverage
     - 100%

Safety Goals
------------

The following safety goals are derived from HARA:

.. list-table::
   :header-rows: 1
   :widths: 10 40 10 20

   * - ID
     - Description
     - ASIL
     - FTTI
   * - SG-001
     - Prevent battery thermal runaway
     - ASIL-D
     - 100ms
   * - SG-002
     - Prevent cell overcharge
     - ASIL-D
     - 1s
   * - SG-003
     - Prevent cell overdischarge
     - ASIL-C
     - 10s
   * - SG-004
     - Prevent battery overcurrent
     - ASIL-D
     - 50ms
   * - SG-005
     - Prevent HV exposure hazard
     - ASIL-D
     - 100ms

Technical Safety Requirements
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 10 50 10 15

   * - ID
     - Description
     - ASIL
     - Parent
   * - TSR-001
     - Cell voltage measurement with +/-2mV accuracy
     - ASIL-D
     - SG-001, SG-002
   * - TSR-002
     - Temperature monitoring with +/-2C accuracy
     - ASIL-D
     - SG-001
   * - TSR-003
     - Current measurement with +/-1% accuracy
     - ASIL-D
     - SG-004
   * - TSR-004
     - Contactor control with feedback verification
     - ASIL-D
     - SG-001, SG-005
   * - TSR-005
     - Controlled precharge before main closing
     - ASIL-C
     - SG-004
   * - TSR-006
     - Continuous SOA monitoring and protection
     - ASIL-D
     - SG-001..004
   * - TSR-007
     - Fault detection, recording, and response
     - ASIL-D
     - All SGs
   * - TSR-008
     - Safe state transition on fatal errors
     - ASIL-D
     - SG-001, SG-004
   * - TSR-009
     - Hardware watchdog supervision
     - ASIL-D
     - SG-001, SG-004
   * - TSR-010
     - Communication integrity for safety data
     - ASIL-C
     - SG-001, SG-004

SYS.2 - System Architecture Design
===================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SYS2-001

**Status**: Released

**Purpose**: Define system decomposition into hardware and software elements with HW/SW allocation.

System Elements
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 25 15 45

   * - Element ID
     - Name
     - Type
     - Description
   * - SYS-HW-MCU
     - Microcontroller
     - Hardware
     - TMS570LS12x ARM Cortex-R4F
   * - SYS-HW-SBC
     - System Basis Chip
     - Hardware
     - NXP FS85xx power/safety IC
   * - SYS-HW-AFE
     - Analog Front-End
     - Hardware
     - Cell measurement IC
   * - SYS-HW-CONT
     - Contactors
     - Hardware
     - High-power switches
   * - SYS-SW-APP
     - Application SW
     - Software
     - BMS application logic
   * - SYS-SW-DRV
     - Driver SW
     - Software
     - Hardware drivers
   * - SYS-SW-RTOS
     - RTOS
     - Software
     - Real-time OS

Software Architecture Layers
----------------------------

The software is organized into 4 layers:

1. **Application Layer (ASIL-D)**: BMS Control, SOA, Algorithm, Balancing, Redundancy
2. **Engine Layer (ASIL-C)**: Database, Diagnostics, System Monitor, SYS
3. **Driver Layer (ASIL-B/C)**: AFE, SBC, Contactor, TS, SPS, CAN, SPI
4. **HAL Layer (QM/ASIL-B)**: GPIO, ADC, Timer, DMA

Safety Architecture
-------------------

The system achieves ASIL-D through redundant protection paths:

**Primary Path (ASIL-D)**: Software-based monitoring -> SPS Driver -> Contactor Control

**Secondary Path (ASIL-D)**: SBC Watchdog -> FS0B Output -> Contactor Control

**Tertiary Path (QM)**: Physical fuse protection (external)

SYS.3 - System Integration Test Specification
==============================================

**Document ID**: FBMS-WP-SYS3-001

**Status**: Complete

**Test Cases Planned**: 69

Test Coverage
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Category
     - Test Cases
     - Status
   * - Interface Integration
     - 24
     - Documented
   * - Functional Chain Tests
     - 20
     - Documented
   * - Safety Mechanism Tests
     - 15
     - Documented
   * - Communication Tests
     - 10
     - Documented
   * - **Total**
     - **69**
     - **Documented**

SYS.4 - System Integration
===========================

**Document ID**: FBMS-WP-SYS4-001

**Status**: Complete

**Purpose**: Define integration plan for combining system elements.

Integration Strategy
--------------------

The integration follows a bottom-up approach:

1. Hardware component integration (AFE, SBC, MCU)
2. Driver software integration with hardware
3. Engine layer integration with drivers
4. Application layer integration
5. Full system integration

SYS.5 - System Qualification Testing
=====================================

**Document ID**: FBMS-WP-SYS5-001

**Status**: Complete

**Test Cases Planned**: 95

Qualification Categories
------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Category
     - Test Cases
     - Status
   * - Functional Qualification
     - 30
     - Documented
   * - Safety Function Tests
     - 25
     - Documented
   * - Performance Tests
     - 15
     - Documented
   * - Environmental Tests
     - 15
     - Documented
   * - EMC Tests
     - 10
     - Documented
   * - **Total**
     - **95**
     - **Documented**

Traceability Summary
=====================

All system-level work products maintain bidirectional traceability:

- SYS.1 Requirements -> SYS.2 Architecture Elements (100%)
- SYS.2 Elements -> SWE.1 Software Requirements (100%)
- SYS.1 Requirements -> SYS.5 Qualification Tests (100%)
- SYS.2 Architecture -> SYS.3 Integration Tests (100%)

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Compliance**: ISO 26262:2018, ASPICE 3.1
