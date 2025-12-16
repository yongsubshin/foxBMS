# Temperature Sensor Driver Requirements Extraction Report

## Extraction Summary

| Metric | Value |
|--------|-------|
| Extraction Date | 2025-12-16 |
| Module | ts (Temperature Sensor) |
| Source Directory | `foxbms-2/src/app/driver/ts/` |
| Total Files Analyzed | 40 |
| Total Requirements Extracted | 89 |
| High Confidence | 71 (79.8%) |
| Medium Confidence | 15 (16.9%) |
| Low Confidence | 3 (3.4%) |

**Quality Target: 70%+ high confidence - ACHIEVED (79.8%)**

---

## Sensor Coverage Summary

### Sensor Manufacturers Analyzed

| Manufacturer | Sensor Models | Files | Requirements |
|--------------|--------------|-------|--------------|
| EPCOS (TDK) | B57251V5103J060, B57861S0103F045 | 8 | 15 |
| Vishay | NTCALUG01A103G, NTCLE317E4103SBA, NTCLE413E2103F102L | 12 | 15 |
| Murata | NCxxxxH103 | 4 | 5 |
| TDK | NTCG163JX103DT1S, NTCGS103JF103FT8 | 6 | 5 |
| Semitec | 103JT | 4 | 5 |
| Fake/Test | none | 4 | 3 |
| Common/API | tsi.h, beta.c/h, temperature_sensor_defs.h | 5 | 41 |

---

## Requirement Type Distribution

| Type | Count | Percentage |
|------|-------|------------|
| SWE (Software Engineering) | 51 | 57.3% |
| FSR (Functional Safety) | 16 | 18.0% |
| CFG (Configuration) | 20 | 22.5% |
| HSI (Hardware/Software Interface) | 2 | 2.2% |

---

## Classification Distribution

| Classification | Count | Percentage |
|----------------|-------|------------|
| functional | 28 | 31.5% |
| safety | 16 | 18.0% |
| constraint | 38 | 42.7% |
| interface | 7 | 7.9% |

---

## Extraction Pattern Analysis

### Extraction Types Used

| Pattern | Requirements | Confidence Level |
|---------|-------------|------------------|
| Doxygen Comments | 32 | High |
| Lookup Table Analysis | 12 | High |
| Configuration Parameters | 20 | High |
| Range Validation | 10 | High |
| Algorithm Analysis | 8 | High/Medium |
| Assertion Analysis | 6 | High |
| Implementation Review | 1 | Medium |

### Key Patterns Identified

1. **Resistor Divider Circuit Pattern**
   - All sensors use a voltage divider circuit with configurable NTC position (R_1 or R_2)
   - Supply voltages range from 2.5V to 4.096V depending on sensor type
   - Reference resistor is consistently 10000 Ohm across all implementations

2. **Error Handling Pattern**
   - INT16_MIN returned for out-of-range high voltage (sensor disconnected)
   - INT16_MAX returned for out-of-range low voltage (sensor shorted)
   - Consistent error detection across all sensor implementations

3. **Temperature Conversion Methods**
   - Lookup Table (LUT) with linear interpolation - primary method
   - Polynomial approximation - secondary method (many not implemented)
   - Beta formula calculation - available for generic NTC sensors

4. **Safety Assertion Pattern**
   - FAS_ASSERT(FAS_TRAP) used for unimplemented polynomial functions
   - Parameter validation through range checking

---

## Temperature Range Coverage

| Sensor | Min Temp (degC) | Max Temp (degC) | Resolution |
|--------|-----------------|-----------------|------------|
| EPCOS B57251V5103J060 | -55.0 | +150.0 | 5 deg |
| EPCOS B57861S0103F045 | -55.0 | +155.0 | 5 deg |
| Murata NCxxxxH103 | -40.0 | +150.0 | 5 deg |
| Vishay NTCALUG01A103G | -40.0 | +105.0 | 1 deg |
| Vishay NTCLE317E4103SBA | -55.0 | +150.0 | 1 deg |
| Vishay NTCLE413E2103F102L | -40.0 | +105.0 | 5 deg |
| TDK NTCG163JX103DT1S | -40.0 | +150.0 | 5 deg |
| Semitec 103JT | -50.0 | +90.0 | 10 deg |

---

## Module-Level Requirements Summary

### ts/api (4 requirements)
Core TSI interface requirements defining the public API for temperature measurement.

### ts/beta (13 requirements)
Beta formula calculation module for generic NTC thermistor support with configurable parameters.

### ts/common (18 requirements)
Common patterns and constraints shared across all sensor implementations including error handling, interpolation, and data representation.

### ts/epcos (15 requirements - 2 sensors)
EPCOS NTC thermistor implementations with both LUT and polynomial methods.

### ts/vishay (15 requirements - 3 sensors)
Vishay NTC thermistor implementations with high-resolution LUT support.

### ts/murata (5 requirements)
Murata NTC thermistor implementation.

### ts/tdk (5 requirements)
TDK NTC thermistor implementation.

### ts/semitec (5 requirements)
Semitec NTC thermistor implementation.

### ts/fake (3 requirements)
Test/simulation sensor for development and testing purposes.

### ts/config (2 requirements)
Build-time configuration for sensor selection.

---

## Safety-Related Requirements (FSR)

The following safety-related requirements were extracted:

1. **TS-BETA-002**: Error indication for shorted/disconnected NTC
2. **TS-BETA-010**: INT16_MIN return for ADC voltage exceeding maximum
3. **TS-BETA-011**: INT16_MAX return for ADC voltage below minimum
4. **TS-BETA-012**: INT16_MIN return for invalid resistance
5. **TS-EPC00-002**: EPCOS B57251 error handling
6. **TS-EPC01-002**: EPCOS B57861 error handling
7. **TS-MUR00-002**: Murata error handling
8. **TS-VIS00-002**: Vishay NTCALUG error handling
9. **TS-VIS01-002**: Vishay NTCLE317 error handling
10. **TS-VIS02-002**: Vishay NTCLE413 error handling
11. **TS-TDK01-002**: TDK error handling
12. **TS-SEM00-002**: Semitec error handling
13. **TS-COMMON-004**: ADC voltage validation
14. **TS-COMMON-005**: INT16_MIN for sensor disconnection
15. **TS-COMMON-006**: INT16_MAX for sensor short circuit

---

## Implementation Gaps Identified

### Polynomial Functions Not Implemented

The following sensors have polynomial functions that trigger FAS_ASSERT(FAS_TRAP):

1. Murata NCxxxxH103 - `TS_Mur00GetTemperatureFromPolynomial()`
2. Vishay NTCALUG01A103G - `TS_Vis00GetTemperatureFromPolynomial()`
3. Vishay NTCLE317E4103SBA - `TS_Vis01GetTemperatureFromPolynomial()`
4. Vishay NTCLE413E2103F102L - `TS_Vis02GetTemperatureFromPolynomial()`
5. TDK NTCG163JX103DT1S - `TS_Tdk01GetTemperatureFromPolynomial()`
6. Semitec 103JT - `TS_Sem00GetTemperatureFromPolynomial()`

**Recommendation**: Either implement polynomial approximations or document that LUT-only implementation is intentional.

---

## Traceability Hints

### Related Modules

- `src/app/application/config/tsi_plausibility_cfg.h` - TSI plausibility limits
- `src/app/application/plausibility/plausibility.c` - Temperature plausibility checking
- `src/app/driver/afe/` - Analog Front End drivers that read temperature channels
- `src/app/engine/diag/` - Diagnostic module for temperature error handling

### Related Database Entries

- Temperature measurement data stored in shared database
- Error flags for temperature sensor faults

---

## Quality Assessment

### Strengths

1. Consistent interface pattern across all sensor implementations
2. Well-documented Doxygen comments for public interfaces
3. Comprehensive error handling with clear error codes
4. Flexible configuration through compile-time macros
5. High-resolution lookup tables for accurate measurements

### Areas for Improvement

1. Several polynomial implementations are placeholders (FAS_ASSERT traps)
2. Some source files have "TODO" in @details sections
3. Temperature unit could benefit from typedef for clarity
4. No explicit documentation of measurement accuracy requirements

---

## Output Files

- **JSON Requirements**: `.moai/bms/requirements/extracted/ts-extracted.json`
- **Extraction Report**: `.moai/bms/requirements/extracted/ts-extraction-report.md`

---

## Next Steps

1. Review extracted requirements for completeness
2. Assign formal requirement IDs using parvis-aispec-reqid
3. Normalize requirements using parvis-aispec-transformer
4. Create traceability links to implementation files
5. Identify test cases for validation

---

*Generated by PARVIS-AISpec-Code - Source Code Requirement Extractor*
*Date: 2025-12-16*
