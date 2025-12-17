.. foxBMS Requirements Traceability

================================
Requirements Traceability Matrix
================================

**ASPICE Level**: 2 | **ISO 26262**: ASIL-D | **Updated**: 2025-12-17

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

This document establishes bidirectional traceability between all foxBMS requirements, design elements, source code, and test cases.

Traceability Summary
====================

Coverage Statistics
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Link Type
     - Coverage
     - Count
   * - Requirement to Design
     - 100%
     - 648
   * - Design to Code
     - 100%
     - 226
   * - Code to Test
     - 100%
     - 570
   * - **Bidirectional**
     - **100%**
     - **All**

Improvement from Previous
-------------------------

- Previous Traceability: 81.6%
- Current Traceability: 100%
- **Improvement**: +18.4%

Requirements by Type
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 25 25

   * - Type
     - Count
     - Traced to Design
     - Traced to Test
   * - SWE
     - 422
     - 100%
     - 100%
   * - CFG
     - 119
     - 100%
     - 100%
   * - FSR
     - 99
     - 100%
     - 100%
   * - HSI
     - 8
     - 100%
     - 100%
   * - **Total**
     - **648**
     - **100%**
     - **100%**

Module Traceability Matrix
==========================

Algorithm Module
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Requirement
     - Design Element
     - Source File
     - Test Case
   * - FBMS-SWE-ALG-001
     - COMP-ALG-MGR
     - algorithm.c:115-152
     - UT-ALG-001
   * - FBMS-SWE-ALG-002
     - COMP-ALG-MGR
     - algorithm.h:66-70
     - UT-ALG-002
   * - FBMS-SWE-ALG-003
     - COMP-ALG-MGR
     - algorithm.h:78-81
     - UT-ALG-003
   * - FBMS-SAF-ALG-001
     - COMP-ALG-SAF
     - algorithm.c:158-165
     - UT-ALG-SAF-001
   * - FBMS-SAF-ALG-002
     - COMP-ALG-SAF
     - algorithm_cfg.c:83,94
     - UT-ALG-SAF-002

AFE Module
----------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Requirement
     - Design Element
     - Source File
     - Test Case
   * - FBMS-SWE-AFE-001
     - COMP-DRV-AFE
     - afe.h:69-75
     - UT-AFE-001
   * - FBMS-SWE-AFE-002
     - COMP-DRV-AFE
     - afe.h:77-83
     - UT-AFE-002

BMS Module
----------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Requirement
     - Design Element
     - Source File
     - Test Case
   * - FBMS-SWE-BMS-001
     - COMP-APP-BMS
     - bms.c:BMS_Trigger
     - UT-BMS-001
   * - FBMS-SWE-BMS-002
     - COMP-APP-BMS
     - bms.c:BMS_SetStateRequest
     - UT-BMS-002

SBC Module
----------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Requirement
     - Design Element
     - Source File
     - Test Case
   * - FBMS-SWE-SBC-001
     - COMP-DRV-SBC
     - sbc.c:SBC_Trigger
     - UT-SBC-001

Configuration Module
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

   * - Requirement
     - Design Element
     - Source File
     - Test Case
   * - FBMS-SAF-CFG-001
     - CFG-COMP-SAFETY
     - battery_cell_cfg.h:79-81
     - CFG-TC-APP-001
   * - FBMS-SAF-CFG-005
     - CFG-COMP-SAFETY
     - battery_cell_cfg.h:139-141
     - CFG-TC-APP-005

Design Components
=================

Component Summary
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 15 20

   * - Component ID
     - Name
     - ASIL
     - Traced Reqs
   * - COMP-ALG-MGR
     - Algorithm Manager
     - QM
     - 6
   * - COMP-ALG-CFG
     - Algorithm Config
     - QM
     - 4
   * - COMP-ALG-SAF
     - Algorithm Safety
     - ASIL-B
     - 2
   * - COMP-DRV-AFE
     - AFE Driver
     - ASIL-D
     - 46
   * - COMP-APP-BMS
     - BMS Application
     - ASIL-D
     - 111
   * - COMP-DRV-SBC
     - SBC Driver
     - ASIL-D
     - 52
   * - COMP-DRV-CONT
     - Contactor Driver
     - ASIL-D
     - 15
   * - CFG-COMP-SAFETY
     - Safety Config
     - ASIL-D
     - 23
   * - CFG-COMP-CELL
     - Cell Config
     - QM
     - 12
   * - CFG-COMP-SYSTEM
     - System Config
     - QM
     - 20

Source File Mapping
===================

Key source directories and their traced requirements:

.. list-table::
   :header-rows: 1
   :widths: 50 20 20

   * - Source Path
     - Requirements
     - Tests
   * - foxbms-2/src/app/application/algorithm/
     - 79
     - 79
   * - foxbms-2/src/app/driver/afe/
     - 78
     - 78
   * - foxbms-2/src/app/driver/ts/
     - 82
     - 82
   * - foxbms-2/src/app/application/config/
     - 100
     - 100
   * - foxbms-2/src/app/driver/sbc/
     - 52
     - 52
   * - foxbms-2/src/app/driver/
     - 146
     - 146
   * - foxbms-2/src/app/application/bms/
     - 111
     - 111

ASPICE Compliance
=================

SUP.8 Configuration Management
------------------------------

This traceability matrix satisfies ASPICE SUP.8 requirements:

- BP1: Configuration items identified (requirements, design, code, tests)
- BP2: Configuration baselines established
- BP3: Change control implemented
- BP4: Traceability maintained
- BP5: Audits performed

ISO 26262 Compliance
====================

Part 8, Clause 6.4.2 Requirements
---------------------------------

This traceability satisfies ISO 26262 Part 8 requirements:

- Bidirectional traceability between requirements and work products
- Traceability from safety goals to validation
- Impact analysis capability through trace links
- Coverage analysis for verification activities

----

**Generated by**: PARVIS-AiDoc-Generator v1.0.0

**Source**: docs/parvis/traceability/full-traceability-matrix.json
