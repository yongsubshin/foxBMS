.. foxBMS Software Level Process Documentation

==================================
Software Level (SWE.1 - SWE.6)
==================================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

This section documents the software-level V-Model processes for the foxBMS Battery Management System.

.. contents:: Contents
   :local:
   :depth: 2

SWE.1 - Software Requirements Analysis
========================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE1-001

**Status**: Complete

**Purpose**: Define software requirements derived from system requirements.

Requirements Summary
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20

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

Requirements by Module
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 15 15

   * - Module
     - Total
     - Safety
     - Coverage
   * - Drivers
     - 146
     - 15
     - 100%
   * - BMS
     - 111
     - 24
     - 100%
   * - Config
     - 100
     - 23
     - 100%
   * - TS (Temperature)
     - 82
     - 15
     - 100%
   * - Algorithm
     - 79
     - 15
     - 100%
   * - AFE
     - 78
     - 32
     - 100%
   * - SBC
     - 52
     - 23
     - 100%
   * - **Total**
     - **648**
     - **147**
     - **100%**

Safety Requirements by ASIL
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 30

   * - ASIL Level
     - Count
     - Percentage
   * - ASIL-D
     - 52
     - 35.4%
   * - ASIL-C
     - 50
     - 34.0%
   * - ASIL-B
     - 30
     - 20.4%
   * - ASIL-A
     - 15
     - 10.2%
   * - **Total**
     - **147**
     - **100%**

SWE.2 - Software Architecture Design
======================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE2-001

**Status**: Complete

**Purpose**: Define software architecture with component interfaces.

Architecture Summary
--------------------

**Number of Layers**: 4

**Number of Modules**: 7 major modules

**Interfaces Defined**: 8 internal, 6 external

Layer Architecture
------------------

**Application Layer (ASIL-D)**:
   - BMS Control Module
   - SOA (Safe Operating Area) Module
   - Algorithm Module (SOC/SOH/SOE/SOF)
   - Balancing Module
   - Redundancy Module

**Engine Layer (ASIL-C)**:
   - Database (DATA) Module
   - Diagnostics (DIAG) Module
   - System Monitor (SYSMON) Module
   - System (SYS) Module

**Driver Layer (ASIL-B/C)**:
   - AFE Driver
   - SBC Driver
   - Contactor (CONT) Driver
   - Temperature Sensor (TS) Driver
   - CAN Driver
   - SPI Driver

**HAL Layer (QM/ASIL-B)**:
   - GPIO, ADC, Timer, DMA

SWE.3 - Software Detailed Design
==================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE3-001

**Status**: Complete

**Purpose**: Define detailed design for software units.

Design Coverage
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20

   * - Module
     - Functions Documented
     - Status
   * - BMS Control
     - 45
     - Complete
   * - AFE Driver
     - 52
     - Complete
   * - SBC Driver
     - 38
     - Complete
   * - Contactor Driver
     - 26
     - Complete
   * - Other Modules
     - 65
     - Complete
   * - **Total**
     - **226**
     - **Complete**

Detailed Design Documents
-------------------------

- BMS: State machine design, contactor sequencing
- AFE: Measurement acquisition, communication protocols
- SBC: Watchdog management, power control
- Contactor: Driver control, feedback monitoring

SWE.4 - Software Unit Verification
====================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE4-001

**Status**: Complete

**Purpose**: Verify software units meet their requirements.

Unit Test Summary
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Module
     - Unit Tests
     - MC/DC
     - Status
   * - BMS Module
     - 45
     - 100%
     - Complete
   * - AFE Driver
     - 15
     - N/A
     - Complete
   * - SBC Driver
     - 12
     - N/A
     - Complete
   * - Other Modules
     - 25
     - N/A
     - Complete
   * - **Total**
     - **97**
     - **100% (BMS)**
     - **Complete**

MC/DC Analysis (BMS Module)
---------------------------

**Functions Analyzed**: 12 safety-critical functions

**Total Test Vectors**: 52

**MC/DC Coverage**: 100%

Key Functions with MC/DC:
   - BMS_CheckPrecharge
   - BMS_IsBatterySystemStateOkay
   - BMS_GetFirstContactorToBeOpened
   - BMS_CheckStateRequest
   - BMS_Trigger
   - BMS_GetHighestString
   - BMS_GetClosestString
   - BMS_UpdateBatterySystemState
   - BMS_IsContactorFeedbackValid
   - BMS_IsAnyFatalErrorFlagSet
   - BMS_GetCurrentFlowDirection
   - BMS_CheckCanRequests

SWE.5 - Software Integration Test
==================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE5-001

**Status**: Documented

**Purpose**: Verify software components integrate correctly.

Integration Test Summary
------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Category
     - Test Cases
     - Status
   * - Internal Interface Tests
     - 45
     - Documented
   * - External Interface Tests
     - 17
     - Documented
   * - Fault Injection Tests
     - 10
     - Documented
   * - Data Flow Tests
     - 15
     - Documented
   * - **Total**
     - **87**
     - **Documented**

SWE.6 - Software Qualification Test
====================================

Document Overview
-----------------

**Document ID**: FBMS-WP-SWE6-001

**Status**: Documented

**Purpose**: Verify software meets all specified requirements.

Qualification Test Summary
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 20

   * - Category
     - Test Cases
     - Status
   * - Functional Chain Tests
     - 24
     - Documented
   * - Safety Mechanism Tests
     - 42
     - Documented
   * - Interface Tests
     - 18
     - Documented
   * - Performance Tests
     - 12
     - Documented
   * - Resource Usage Tests
     - 8
     - Documented
   * - Communication Tests
     - 16
     - Documented
   * - Error Handling Tests
     - 24
     - Documented
   * - State Machine Tests
     - 12
     - Documented
   * - **Total**
     - **156**
     - **Documented**

MISRA C:2012 Compliance
========================

Overall Compliance Status
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 30

   * - Category
     - Violations
     - Status
   * - Mandatory Rules
     - 0
     - PASS
   * - Required Rules
     - 35
     - PASS (Deviations)
   * - Advisory Rules
     - 6
     - INFO
   * - **Total Deviations**
     - **41**
     - **Documented**

**Overall Compliance**: ~99%

**Files Analyzed**: 228

**Rule 17.7 Fixes**: 345+ violations resolved

Critical Bugs Resolved
-----------------------

1. **CF-001**: diag.c:364 logic operation bug - RESOLVED
2. **CF-002**: diag.c:216 dead code - Confirmed FALSE POSITIVE

Traceability Summary
=====================

All software-level work products maintain 100% bidirectional traceability:

- SWE.1 Requirements -> SWE.2 Architecture (100%)
- SWE.2 Architecture -> SWE.3 Detailed Design (100%)
- SWE.3 Design -> Implementation (100%)
- Implementation -> SWE.4 Unit Tests (100%)
- SWE.2 Architecture -> SWE.5 Integration Tests (100%)
- SWE.1 Requirements -> SWE.6 Qualification Tests (100%)

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Compliance**: ISO 26262:2018, ASPICE 3.1
