# foxBMS Battery Management System

**Professional-Grade Open Source BMS with AI-Powered Documentation**

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![OSHWA Certified](https://img.shields.io/badge/OSHWA-DE000128-green.svg)](https://certification.oshwa.org/de000128.html)
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-ASIL--D-orange.svg)]()
[![ASPICE](https://img.shields.io/badge/ASPICE-Level%202-yellow.svg)]()

---

## Overview

foxBMS is a free, open, and flexible development environment for designing battery management systems. As the first modular open source BMS development platform, it provides a universal hardware and software solution for controlling modern and complex electrical energy storage systems of any size.

This repository contains the foxBMS project enhanced with **PARVIS** (PARVIS AI-based Requirements & Verification Integration System), an AI-powered documentation and verification system for automotive-grade compliance.

### Supported Energy Storage Technologies

- Lithium-Ion and Solid State Batteries
- Lithium-Sulfur Batteries
- Sodium-Ion Batteries
- Lithium-Ion Capacitors (LIC)
- Electric Double-Layer Capacitors (EDLC, supercapacitors)
- Redox-Flow Batteries (RFB)
- Fuel Cells (FC)
- Hybrid combinations of the above

---

## PARVIS AI Documentation System

PARVIS provides automated requirement extraction, traceability management, and verification support for automotive safety standards compliance.

### Key Achievements

| Metric | Result |
|--------|--------|
| Software Requirements | 648 (unified from 7 modules) |
| Safety Requirements | 147 (ASIL-D/C/B classified) |
| Test Cases | 570 (Unit, Integration, Qualification, Validation) |
| MC/DC Coverage | 100% (all safety-critical functions) |
| Traceability Coverage | 100% bidirectional |
| MISRA C:2012 Compliance | ~99% |
| ASPICE Level | Level 2 Compliant |

### PARVIS Components

- **Requirement Extraction Engine**: Automated extraction from C source code
- **V-Model Phase Tracking**: 8-phase workflow (L1-L4, R1-R4)
- **Quality Gate Enforcement**: Metric-based gate verification
- **Traceability Matrix**: Bidirectional requirement-to-test mapping
- **Safety Analysis**: ISO 26262 ASIL classification

### Documentation Structure

```
docs/parvis/
  00-FINAL-SUMMARY.md          # Project summary and status
  requirements/                 # Extracted and classified requirements
  architecture/                 # Software architecture design
  design/                       # Detailed module designs
  verification/                 # Test specifications and reports
  traceability/                 # Traceability matrices
  system/                       # System-level documents (SYS.1-SYS.5, VAL.1)
  safety/                       # Technical safety concept
  aspice/                       # ASPICE work products
```

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- foxBMS 2 toolchain (see foxbms-2/INSTALL.md)

### Extract Requirements from BMS Module

```bash
python3 .moai/bms/extraction_engine.py foxbms-2/src/app/application/bms BMS
```

### Generate Extraction Report

```bash
python3 .moai/bms/extraction_engine.py foxbms-2/src/app/application/bms BMS --report
```

### Check Phase Status

```bash
python3 .moai/bms/orchestrator_engine.py status BMS
```

### Generate Phase Status Report

```bash
python3 .moai/bms/orchestrator_engine.py report BMS
```

---

## foxBMS 2 Core

The core foxBMS 2 implementation is located in the `foxbms-2/` directory.

### Repository Structure

| Directory | Description |
|-----------|-------------|
| `foxbms-2/cli` | CLI tool to interact with the repository |
| `foxbms-2/conf` | High level configurations |
| `foxbms-2/docs` | Documentation source files |
| `foxbms-2/hardware` | Hardware schematic and layout information |
| `foxbms-2/src` | Source files for BMS embedded software |
| `foxbms-2/tests` | Tests for embedded sources and tools |
| `foxbms-2/tools` | Build tools and utilities |

### Official Documentation

- [Latest Documentation Build](https://iisb-foxbms.iisb.fraunhofer.de/foxbms/gen2/docs/html/latest/)
- [All Documentation Builds](https://iisb-foxbms.iisb.fraunhofer.de/foxbms/gen2/docs/html/)

### Installation

See [foxbms-2/INSTALL.md](./foxbms-2/INSTALL.md) for detailed installation instructions.

---

## Compliance and Standards

### ISO 26262 Compliance

| Part | Clause | Title | Status |
|------|--------|-------|--------|
| 4 | 6-9 | System Safety Requirements to Validation | COMPLETE |
| 6 | 6-11 | Software Safety Requirements to Qualification | DOCUMENTED |

### ASPICE Compliance

| Process | Description | Level |
|---------|-------------|-------|
| SYS.1-SYS.5 | System Processes | Level 2 |
| SWE.1-SWE.6 | Software Engineering | Level 2 |
| VAL.1 | Validation | Level 2 |

### MISRA C:2012 Compliance

- Overall Compliance: ~99%
- Mandatory Rules: 100%
- Documented Deviations: 41 (ISO 26262 compliant)

---

## V-Model Process

```
              SYSTEM LEVEL (SYS)
    SYS.1 ──────────────────────────► SYS.5
    Requirements                      Qualification
         │                                  │
         ▼                                  ▼
    SYS.2 ──────────────────────────► SYS.3/4
    Architecture                      Integration
         │                                  │
         │     SOFTWARE LEVEL (SWE)         │
         ▼                                  ▼
    SWE.1 ──────────────────────────► SWE.6
    SW Requirements                   SW Qualification
         │                                  │
         ▼                                  ▼
    SWE.2 ──────────────────────────► SWE.5
    SW Architecture                   SW Integration
         │                                  │
         ▼                                  ▼
    SWE.3 ──────────────────────────► SWE.4
    SW Design        foxBMS Code      Unit Test
```

---

## License

### Software

The software is covered by the **BSD 3-Clause License**.
See [foxbms-2/LICENSE.md](./foxbms-2/LICENSE.md) for details.

### Hardware and Documentation

The hardware and documentation are covered by the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**.

---

## Open Source Hardware Certification

foxBMS 2 has been certified as open source hardware by the Open Source Hardware Association under the OSHWA UID [DE000128](https://certification.oshwa.org/de000128.html).

---

## Acknowledgment

For funding acknowledgements and instructions on how to acknowledge foxBMS 2, please see [foxbms.org/acknowledgements](https://foxbms.org/acknowledgements/).

---

## Project Status

| Component | Status | Version |
|-----------|--------|---------|
| foxBMS 2 Core | Production | See foxbms-2 |
| PARVIS Documentation | Complete | 2.0.0 |
| V-Model Process | Complete | All phases documented |
| Quality Gate | PASSED | All metrics exceeded |

---

## Contributing

Contributions are welcome. Please refer to the foxBMS contribution guidelines and ensure compliance with the established coding standards and quality gates.

---

## Support

For issues or questions:
1. Review the documentation in `docs/parvis/`
2. Check the PARVIS implementation summary
3. Refer to the foxBMS official documentation

---

**Generated by**: PARVIS AI Documentation System
**Project**: foxBMS Battery Management System
**Compliance**: ISO 26262:2018, ASPICE 3.1, MISRA C:2012
