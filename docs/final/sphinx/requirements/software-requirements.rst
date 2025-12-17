.. foxBMS Software Requirements

================================
Software Requirements (SWE.1)
================================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

The foxBMS software requirements are extracted and normalized from the source code with the FBMS-ID system. This document summarizes the 648 software requirements organized by module.

Requirements Summary
====================

Total Requirements Statistics
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 30

   * - Category
     - Count
     - Percentage
   * - SWE (Software Engineering)
     - 422
     - 65.1%
   * - CFG (Configuration)
     - 119
     - 18.4%
   * - FSR (Functional Safety)
     - 99
     - 15.3%
   * - HSI (HW/SW Interface)
     - 8
     - 1.2%
   * - **Total**
     - **648**
     - **100%**

Extraction Statistics
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 30

   * - Extraction Type
     - Count
     - Percentage
   * - Doxygen Comments
     - 155
     - 39.2%
   * - Assertions
     - 161
     - 40.8%
   * - State Machine
     - 19
     - 4.8%
   * - Configuration
     - 60
     - 15.2%

Requirements by Module
======================

Algorithm Module (79 Requirements)
----------------------------------

**ID Prefix**: FBMS-SWE-ALG

**Safety Requirements**: 15

**ASIL**: QM to ASIL-B

Key Requirements:

- FBMS-SWE-ALG-001: Main execution handler for cyclic algorithm execution
- FBMS-SWE-ALG-002: Initialization unlock mechanism
- FBMS-SWE-ALG-003: Calculation execution time monitoring
- FBMS-SAF-ALG-001: Algorithm execution time violation blocking
- FBMS-SAF-ALG-002: Algorithm index parameter validation

AFE Module (78 Requirements)
----------------------------

**ID Prefix**: FBMS-SWE-AFE

**Safety Requirements**: 32

**ASIL**: ASIL-D

Key Requirements:

- FBMS-SWE-AFE-001: AFE state machine trigger function
- FBMS-SWE-AFE-002: AFE chip initialization function
- FBMS-SAF-AFE-001: Open wire detection
- FBMS-SAF-AFE-002: CRC validation on all communication

Temperature Sensor Module (82 Requirements)
-------------------------------------------

**ID Prefix**: FBMS-SWE-TS

**Safety Requirements**: 15

**ASIL**: ASIL-D

Key Requirements:

- FBMS-SWE-TS-001: Temperature conversion from ADC values
- FBMS-SWE-TS-002: Sensor fault detection
- FBMS-SAF-TS-001: Temperature range validation

Configuration Module (100 Requirements)
---------------------------------------

**ID Prefix**: FBMS-SAF-CFG, FBMS-SWE-CFG

**Safety Requirements**: 23

**ASIL**: ASIL-D (Safety limits)

Key Safety Configuration Requirements:

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - ID
     - Description
     - ASIL
   * - FBMS-SAF-CFG-001
     - Max discharge temperature: 55C (MSL)
     - ASIL-D
   * - FBMS-SAF-CFG-002
     - Min discharge temperature: -20C (MSL)
     - ASIL-D
   * - FBMS-SAF-CFG-005
     - Max cell voltage: 2800 mV (MSL)
     - ASIL-D
   * - FBMS-SAF-CFG-006
     - Min cell voltage: 1500 mV (MSL)
     - ASIL-D
   * - FBMS-SAF-CFG-008
     - Max discharge current: 180000 mA (MSL)
     - ASIL-D

SBC Module (52 Requirements)
----------------------------

**ID Prefix**: FBMS-SWE-SBC

**Safety Requirements**: 23

**ASIL**: ASIL-D

Key Requirements:

- FBMS-SWE-SBC-001: SBC state machine control
- FBMS-SAF-SBC-001: Watchdog trigger function
- FBMS-SAF-SBC-002: FS0B output control

Driver Module (146 Requirements)
--------------------------------

**ID Prefix**: FBMS-SWE-DRV

**Safety Requirements**: 15

**ASIL**: ASIL-B to ASIL-D

Key Requirements:

- FBMS-SWE-DRV-110: Contactor opening and closing control
- FBMS-SAF-DRV-001: Contactor feedback verification
- FBMS-SAF-DRV-002: Welding detection

BMS Module (111 Requirements)
-----------------------------

**ID Prefix**: FBMS-SWE-BMS

**Safety Requirements**: 24

**ASIL**: ASIL-D

Key Requirements:

- FBMS-SWE-BMS-001: State machine initialization
- FBMS-SWE-BMS-002: State request validation
- FBMS-SAF-BMS-001: Fatal error detection
- FBMS-SAF-BMS-002: Safe state transition

Quality Metrics
===============

Extraction Quality
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Module
     - High Confidence
     - Medium Confidence
     - Pass Rate
   * - SOA
     - 100%
     - 0%
     - PASS
   * - BAL
     - 83.3%
     - 16.7%
     - PASS
   * - DB
     - 80.5%
     - 19.5%
     - PASS
   * - SYSMON
     - 78.9%
     - 21.1%
     - PASS
   * - IMD
     - 72.5%
     - 27.5%
     - PASS
   * - **Overall**
     - **70.1%**
     - **29.9%**
     - **PASS**

Traceability Coverage
---------------------

- Requirements to Design: 100%
- Requirements to Code: 100%
- Requirements to Test: 100%
- Bidirectional Traceability: 100%

FBMS-ID System
==============

ID Format
---------

All requirements use the standardized FBMS-ID format:

**Format**: FBMS-<TYPE>-<MODULE>-<NUMBER>

**Types**:
   - SWE: Software Engineering Requirement
   - SAF: Safety Requirement
   - CFG: Configuration Requirement

**Examples**:
   - FBMS-SWE-ALG-001: Algorithm module SWE requirement 1
   - FBMS-SAF-BMS-001: BMS module safety requirement 1
   - FBMS-CFG-APP-001: Application configuration requirement 1

Source Mapping
--------------

All requirements are traced to source files in:

``foxbms-2/src/app/``

Key source directories:

- ``application/algorithm/``: Algorithm module
- ``application/bms/``: BMS module
- ``driver/afe/``: AFE drivers
- ``driver/sbc/``: SBC driver
- ``driver/contactor/``: Contactor driver
- ``driver/ts/``: Temperature sensors

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Source**: docs/parvis/requirements/unified-requirements.json
