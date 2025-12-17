.. foxBMS Design Traceability

==========================
Design Traceability Matrix
==========================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

This document establishes traceability between software architecture design elements and their implementation in source code.

Design Element Summary
======================

Component Statistics
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 15 15 20

   * - Component ID
     - Name
     - Type
     - ASIL
     - Source Files
   * - COMP-ALG-MGR
     - Algorithm Manager
     - SW Unit
     - QM
     - 2
   * - COMP-ALG-CFG
     - Algorithm Config
     - Config Unit
     - QM
     - 2
   * - COMP-ALG-SAF
     - Algorithm Safety
     - Safety Unit
     - ASIL-B
     - 2
   * - COMP-DRV-AFE
     - AFE Driver
     - SW Unit
     - ASIL-D
     - 15+
   * - COMP-APP-BMS
     - BMS Application
     - SW Unit
     - ASIL-D
     - 3
   * - COMP-DRV-SBC
     - SBC Driver
     - SW Unit
     - ASIL-D
     - 4
   * - COMP-DRV-CONT
     - Contactor Driver
     - SW Unit
     - ASIL-D
     - 4
   * - CFG-COMP-SAFETY
     - Safety Config
     - Config Unit
     - ASIL-D
     - 3
   * - CFG-COMP-CELL
     - Cell Config
     - Config Unit
     - QM
     - 1
   * - CFG-COMP-SYSTEM
     - System Config
     - Config Unit
     - QM
     - 1

Architecture to Code Mapping
=============================

Algorithm Manager Component
---------------------------

**Component ID**: COMP-ALG-MGR

**Source Files**:
   - foxbms-2/src/app/application/algorithm/algorithm.c
   - foxbms-2/src/app/application/algorithm/algorithm.h

**Functions**:
   - ALGO_MainFunction()
   - ALGO_UnlockInitialization()
   - ALGO_Initialize()

**Traced Requirements**: 6

AFE Driver Component
--------------------

**Component ID**: COMP-DRV-AFE

**Source Files**:
   - foxbms-2/src/app/driver/afe/api/afe.h
   - foxbms-2/src/app/driver/afe/adi/ades183x.c
   - foxbms-2/src/app/driver/afe/maxim/*.c
   - foxbms-2/src/app/driver/afe/ltc/*.c
   - foxbms-2/src/app/driver/afe/nxp/*.c

**Functions**:
   - AFE_TriggerIc()
   - AFE_Initialize()
   - AFE driver-specific implementations

**Traced Requirements**: 46

BMS Application Component
-------------------------

**Component ID**: COMP-APP-BMS

**Source Files**:
   - foxbms-2/src/app/application/bms/bms.c
   - foxbms-2/src/app/application/bms/bms.h
   - foxbms-2/src/app/application/config/bms_cfg.h

**Functions**:
   - BMS_Trigger()
   - BMS_SetStateRequest()
   - BMS_CheckPrecharge()
   - BMS_IsBatterySystemStateOkay()

**Traced Requirements**: 111

SBC Driver Component
--------------------

**Component ID**: COMP-DRV-SBC

**Source Files**:
   - foxbms-2/src/app/driver/sbc/sbc.c
   - foxbms-2/src/app/driver/sbc/sbc.h
   - foxbms-2/src/app/driver/sbc/nxpfs85xx.c
   - foxbms-2/src/app/driver/sbc/nxpfs85xx.h

**Functions**:
   - SBC_Trigger()
   - SBC_Initialize()
   - FS85_InitializeDriver()

**Traced Requirements**: 52

Contactor Driver Component
--------------------------

**Component ID**: COMP-DRV-CONT

**Source Files**:
   - foxbms-2/src/app/driver/contactor/contactor.c
   - foxbms-2/src/app/driver/contactor/contactor.h
   - foxbms-2/src/app/driver/config/contactor_cfg.h
   - foxbms-2/src/app/driver/config/contactor_cfg.c

**Functions**:
   - CONT_Initialize()
   - CONT_CloseContactor()
   - CONT_OpenContactor()

**Traced Requirements**: 15

Safety Configuration Component
------------------------------

**Component ID**: CFG-COMP-SAFETY

**Source Files**:
   - foxbms-2/src/app/application/config/battery_cell_cfg.h
   - foxbms-2/src/app/application/config/battery_system_cfg.h
   - foxbms-2/src/app/application/config/soa_cfg.h

**Configuration Items**:
   - Voltage limits (MSL/RSL/MOL)
   - Temperature limits (MSL/RSL/MOL)
   - Current limits (MSL/RSL/MOL)
   - Timing constraints

**Traced Requirements**: 23

Interface Traceability
======================

Internal Interfaces
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Interface ID
     - From
     - To
     - Protocol
   * - IF-INT-001
     - BMS
     - AFE Driver
     - Function call
   * - IF-INT-002
     - BMS
     - CONT Driver
     - Function call
   * - IF-INT-003
     - BMS
     - SOA Module
     - Function call
   * - IF-INT-004
     - ALGO
     - DATA Module
     - Database access
   * - IF-INT-005
     - AFE Driver
     - SPI Driver
     - HAL call
   * - IF-INT-006
     - SBC Driver
     - SPI Driver
     - HAL call
   * - IF-INT-007
     - ALL
     - DIAG Module
     - Fault reporting
   * - IF-INT-008
     - ALL
     - DATA Module
     - Data storage

External Interfaces
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 40 20

   * - Interface ID
     - From
     - To
     - Protocol
   * - IF-EXT-001
     - CAN Driver
     - Vehicle ECU
     - CAN 2.0B
   * - IF-EXT-002
     - AFE Driver
     - AFE ICs
     - SPI/isoSPI
   * - IF-EXT-003
     - SBC Driver
     - SBC IC
     - SPI
   * - IF-EXT-004
     - CONT Driver
     - Contactors
     - GPIO/PWM
   * - IF-EXT-005
     - TS Driver
     - NTC Sensors
     - ADC
   * - IF-EXT-006
     - Power
     - Battery 12V
     - Power

ASPICE SWE.2 Evidence
=====================

This design traceability provides evidence for ASPICE SWE.2:

- BP1: Software architecture elements identified
- BP2: Interfaces between elements specified
- BP3: Dynamic behavior described
- BP4: Resource consumption evaluated
- BP5: Traceability to requirements established
- BP6: Consistency ensured
- BP7: Architecture verified

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Compliance**: ASPICE 3.1 SWE.2
