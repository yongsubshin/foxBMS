.. foxBMS System Requirements

============================
System Requirements (SYS.1)
============================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

This document summarizes the system requirements for the foxBMS Battery Management System as defined in the System Requirements Specification (FBMS-WP-SYS1-001).

Safety Goals
============

The following safety goals are derived from Hazard Analysis and Risk Assessment (HARA):

.. list-table:: Safety Goals
   :header-rows: 1
   :widths: 10 45 10 10 15

   * - ID
     - Description
     - ASIL
     - FTTI
     - Safe State
   * - SG-001
     - Prevent battery thermal runaway under all operating conditions
     - ASIL-D
     - 100ms
     - Open contactors
   * - SG-002
     - Prevent cell overcharge above maximum voltage limits
     - ASIL-D
     - 1s
     - Open contactors
   * - SG-003
     - Prevent cell overdischarge below minimum voltage limits
     - ASIL-C
     - 10s
     - Open contactors
   * - SG-004
     - Prevent battery overcurrent conditions
     - ASIL-D
     - 50ms
     - Open contactors
   * - SG-005
     - Prevent unintended HV exposure to personnel
     - ASIL-D
     - 100ms
     - Open contactors

Technical Safety Requirements
==============================

Measurement Requirements
------------------------

.. list-table::
   :header-rows: 1
   :widths: 10 45 10 25

   * - ID
     - Description
     - ASIL
     - Acceptance Criteria
   * - TSR-001
     - Cell voltage measurement with +/-2mV accuracy
     - ASIL-D
     - Range: 0-5V, Rate: 100ms
   * - TSR-002
     - Temperature monitoring with +/-2C accuracy
     - ASIL-D
     - Range: -40 to +85C, Rate: 1s
   * - TSR-003
     - Current measurement with +/-1% accuracy
     - ASIL-D
     - Range: +/-500A, Rate: 10ms

Control Requirements
--------------------

.. list-table::
   :header-rows: 1
   :widths: 10 45 10 25

   * - ID
     - Description
     - ASIL
     - Acceptance Criteria
   * - TSR-004
     - Contactor control with feedback verification
     - ASIL-D
     - Response: <10ms
   * - TSR-005
     - Controlled precharge before main contactor closing
     - ASIL-C
     - Threshold: 95%, Timeout: 5s

Protection Requirements
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 10 45 10 25

   * - ID
     - Description
     - ASIL
     - Acceptance Criteria
   * - TSR-006
     - Continuous SOA monitoring and protective action
     - ASIL-D
     - Response: <100ms
   * - TSR-007
     - Fault detection, recording, and response
     - ASIL-D
     - Categories: Warning, Error, Fatal
   * - TSR-008
     - Safe state transition on fatal errors
     - ASIL-D
     - Transition: <100ms

System Supervision
------------------

.. list-table::
   :header-rows: 1
   :widths: 10 45 10 25

   * - ID
     - Description
     - ASIL
     - Acceptance Criteria
   * - TSR-009
     - Hardware watchdog for MCU supervision
     - ASIL-D
     - Window: 100ms
   * - TSR-010
     - Communication integrity for safety data
     - ASIL-C
     - CRC, Timeouts, E2E

Functional Requirements
========================

Measurement Functions
---------------------

- **SYS-FUNC-001**: Cell voltage acquisition from all battery cells
- **SYS-FUNC-002**: Temperature acquisition from all sensors
- **SYS-FUNC-003**: Pack current acquisition

State Estimation Functions
--------------------------

- **SYS-FUNC-010**: SOC estimation with +/-5% accuracy
- **SYS-FUNC-011**: SOH estimation with +/-10% accuracy
- **SYS-FUNC-012**: SOE/SOF estimation

Control Functions
-----------------

- **SYS-FUNC-020**: BMS state machine (7 states)
- **SYS-FUNC-021**: Contactor sequencing
- **SYS-FUNC-022**: Cell balancing control

Communication Functions
-----------------------

- **SYS-FUNC-030**: CAN communication (500 kbps)
- **SYS-FUNC-031**: Diagnostic interface (UDS over CAN)

Interface Requirements
======================

Hardware Interfaces
-------------------

.. list-table::
   :header-rows: 1
   :widths: 15 25 40

   * - ID
     - Interface
     - Specification
   * - IF-HW-001
     - MCU
     - TMS570LS12x, 160MHz, 1.25MB Flash
   * - IF-HW-002
     - AFE
     - SPI/isoSPI, 1-2 MHz
   * - IF-HW-003
     - SBC
     - NXP FS85xx, SPI
   * - IF-HW-004
     - CAN
     - 2 channels, 500 kbps

Non-Functional Requirements
===========================

Performance
-----------

- **NFR-PERF-001**: Safety-critical response within 100ms
- **NFR-PERF-002**: System operational within 500ms from power-on

Reliability
-----------

- **NFR-REL-001**: 99.99% availability during vehicle operation
- **NFR-REL-002**: Single fault tolerance for all safety functions

Safety
------

- **NFR-SAF-001**: ASIL-D compliance per ISO 26262
- **NFR-SAF-002**: Fail-safe design under any single fault

Traceability to SWE.1
=====================

System requirements trace to 648 software requirements:

.. list-table::
   :header-rows: 1
   :widths: 20 40 20

   * - System Req
     - SW Requirements
     - Test Cases
   * - TSR-001
     - FBMS-REQ-AFE-001..032
     - TC-SYS-001..010
   * - TSR-002
     - FBMS-REQ-TS-001..015
     - TC-SYS-011..020
   * - TSR-003
     - FBMS-REQ-MEAS-001..010
     - TC-SYS-021..025
   * - TSR-004
     - FBMS-REQ-CONT-001..020
     - TC-SYS-026..040
   * - TSR-005
     - FBMS-REQ-BMS-001..030
     - TC-SYS-041..055
   * - TSR-006
     - FBMS-REQ-SOA-001..015
     - TC-SYS-056..070
   * - TSR-007
     - FBMS-REQ-DIAG-001..025
     - TC-SYS-071..085
   * - TSR-008
     - FBMS-REQ-BMS-031..050
     - TC-SYS-086..095
   * - TSR-009
     - FBMS-REQ-SBC-001..023
     - TC-SYS-096..105
   * - TSR-010
     - FBMS-REQ-CAN-001..015
     - TC-SYS-106..115

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Source**: docs/parvis/system/SYS.1-system-requirements.md
