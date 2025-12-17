.. foxBMS Safety Requirements

===============================
Safety Requirements (ISO 26262)
===============================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

This document summarizes the 147 safety requirements identified in the foxBMS BMS software, classified according to ISO 26262 ASIL levels.

Safety Requirements by ASIL
============================

ASIL Distribution
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - ASIL Level
     - Count
     - Percentage
     - Verification Method
   * - ASIL-D
     - 52
     - 35.4%
     - MC/DC + Independent Review
   * - ASIL-C
     - 50
     - 34.0%
     - MC/DC
   * - ASIL-B
     - 30
     - 20.4%
     - Branch Coverage
   * - ASIL-A
     - 15
     - 10.2%
     - Statement Coverage
   * - **Total**
     - **147**
     - **100%**
     - -

ASIL-D Requirements (52)
========================

BMS Safety Requirements
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - ID
     - Description
     - Module
   * - FBMS-SAF-BMS-001
     - Fatal error detection and handling
     - BMS
   * - FBMS-SAF-BMS-002
     - Safe state transition within FTTI
     - BMS
   * - FBMS-SAF-BMS-003
     - Contactor feedback verification
     - BMS
   * - FBMS-SAF-BMS-004
     - Precharge failure detection
     - BMS
   * - FBMS-SAF-BMS-005
     - String isolation on error
     - BMS

AFE Safety Requirements
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - ID
     - Description
     - Module
   * - FBMS-SAF-AFE-001
     - Open wire detection
     - AFE
   * - FBMS-SAF-AFE-002
     - CRC validation on communication
     - AFE
   * - FBMS-SAF-AFE-003
     - Overvoltage detection
     - AFE
   * - FBMS-SAF-AFE-004
     - Undervoltage detection
     - AFE
   * - FBMS-SAF-AFE-005
     - Redundant measurement validation
     - AFE

SBC Safety Requirements
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - ID
     - Description
     - Module
   * - FBMS-SAF-SBC-001
     - Watchdog trigger function
     - SBC
   * - FBMS-SAF-SBC-002
     - FS0B output control
     - SBC
   * - FBMS-SAF-SBC-003
     - LBIST/ABIST self-test
     - SBC
   * - FBMS-SAF-SBC-004
     - Power supply monitoring
     - SBC

Configuration Safety Requirements
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - ID
     - Description
     - Module
   * - FBMS-SAF-CFG-001
     - Max discharge temperature limit
     - Config
   * - FBMS-SAF-CFG-002
     - Min discharge temperature limit
     - Config
   * - FBMS-SAF-CFG-005
     - Max cell voltage limit
     - Config
   * - FBMS-SAF-CFG-006
     - Min cell voltage limit
     - Config
   * - FBMS-SAF-CFG-008
     - Max discharge current limit
     - Config

ASIL-C Requirements (50)
========================

Key ASIL-C safety requirements include:

- SOC/SOH estimation accuracy
- Temperature averaging validation
- Communication timeout detection
- Precharge sequence control
- Balancing limits enforcement

ASIL-B Requirements (30)
========================

Key ASIL-B safety requirements include:

- Algorithm execution time monitoring
- Data integrity checks
- Diagnostic logging
- Cell balancing control

ASIL-A Requirements (15)
========================

Key ASIL-A safety requirements include:

- Performance monitoring
- Status reporting
- Non-critical fault logging

Safety Mechanisms
=================

Total Safety Mechanisms: 42

AFE Mechanisms (8)
------------------

- SM-AFE-001: Open wire detection
- SM-AFE-002: CRC on all frames
- SM-AFE-003: Redundant ADC measurement
- SM-AFE-004: Overvoltage comparator
- SM-AFE-005: Undervoltage comparator
- SM-AFE-006: Self-test sequence
- SM-AFE-007: Watchdog reset
- SM-AFE-008: Temperature monitoring

SBC Mechanisms (6)
------------------

- SM-SBC-001: Window watchdog
- SM-SBC-002: FS0B fail-safe output
- SM-SBC-003: LBIST/ABIST
- SM-SBC-004: Voltage monitoring
- SM-SBC-005: CRC-protected OTP
- SM-SBC-006: Error pin monitoring

BMS Mechanisms (8)
------------------

- SM-BMS-001: State machine validation
- SM-BMS-002: Contactor feedback check
- SM-BMS-003: Precharge monitoring
- SM-BMS-004: String isolation
- SM-BMS-005: Fatal error handling
- SM-BMS-006: Safe state enforcement
- SM-BMS-007: Request validation
- SM-BMS-008: Timing verification

DIAG Mechanisms (4)
-------------------

- SM-DIAG-001: Fault categorization
- SM-DIAG-002: Fault logging
- SM-DIAG-003: Fault counter management
- SM-DIAG-004: Fault recovery handling

SOA Mechanisms (6)
------------------

- SM-SOA-001: Voltage limit monitoring
- SM-SOA-002: Temperature limit monitoring
- SM-SOA-003: Current limit monitoring
- SM-SOA-004: Multi-level thresholds (MOL/RSL/MSL)
- SM-SOA-005: Limit violation response
- SM-SOA-006: Cross-validation

Contactor Mechanisms (5)
------------------------

- SM-CONT-001: Feedback monitoring
- SM-CONT-002: Welding detection
- SM-CONT-003: Sequencing control
- SM-CONT-004: Timing verification
- SM-CONT-005: Emergency opening

SysMon Mechanisms (5)
---------------------

- SM-SYSMON-001: Task monitoring
- SM-SYSMON-002: Timing violation detection
- SM-SYSMON-003: Stack usage monitoring
- SM-SYSMON-004: Notification handling
- SM-SYSMON-005: System reset trigger

Verification Status
===================

MC/DC Coverage
--------------

**BMS Module**: 100% MC/DC coverage achieved

**Test Vectors**: 52 test vectors implemented

**Functions Covered**:
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

Independent Review
------------------

**Status**: Pending

All ASIL-D requirements require independent verification per ISO 26262 Part 6.

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Compliance**: ISO 26262:2018 Part 6
