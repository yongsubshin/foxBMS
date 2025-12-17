# Test Case ID System

Test case ID naming convention for foxBMS verification.

## Base Format

```
[PROJECT]-TC-[LEVEL]-[MODULE]-[SEQ]
```

**Example:** `FBMS-TC-UT-SOC-001`

## Test Level Codes

| Code | Level | ASPICE Process | Description |
|------|-------|----------------|-------------|
| UT | Unit Test | SWE.4 | Single function/module testing |
| IT | Integration Test | SWE.5 | Module integration testing |
| ST | System Test | SWE.6 | Full system testing |
| AT | Acceptance Test | - | Customer acceptance |

## Examples by Level

### Unit Tests (UT)
```
FBMS-TC-UT-SOC-001    Test SOC_Calculate with valid input
FBMS-TC-UT-SOC-002    Test SOC_Calculate with zero current
FBMS-TC-UT-SOC-003    Test SOC_Calculate boundary conditions
FBMS-TC-UT-BMS-001    Test BMS_GetState returns current state
FBMS-TC-UT-AFE-001    Test AFE_ReadVoltages null pointer handling
```

### Integration Tests (IT)
```
FBMS-TC-IT-SOC-001    Test SOC update with real AFE data
FBMS-TC-IT-BMS-001    Test BMS state machine transitions
FBMS-TC-IT-CAN-001    Test CAN message transmission chain
FBMS-TC-IT-DIAG-001   Test diagnostic to contactor integration
```

### System Tests (ST)
```
FBMS-TC-ST-BMS-001    Test complete startup sequence
FBMS-TC-ST-BMS-002    Test emergency shutdown procedure
FBMS-TC-ST-SOA-001    Test safe operating area enforcement
```

## Traceability to Requirements

Each test case traces to one or more requirements:

```
Test Case: FBMS-TC-UT-SOC-001
Verifies:  FBMS-SWE-SOC-001, FBMS-SWE-SOC-002
Method:    Branch coverage
Coverage:  MC/DC for ASIL-B
```

## Test Case Documentation Format

```c
/**
 * @test    FBMS-TC-UT-SOC-001
 * @brief   Test SOC calculation with valid inputs
 * @verifies FBMS-SWE-SOC-001
 * @pre     SOC module initialized
 * @steps   1. Set current to 10A
 *          2. Set time delta to 1s
 *          3. Call SOC_Calculate()
 * @expect  SOC decreases by expected amount
 */
void TEST_SOC_Calculate_ValidInput(void) {
    /* Test implementation */
}
```

## Coverage Requirements by ASIL

| ASIL | Statement | Branch | MC/DC |
|------|-----------|--------|-------|
| QM | Recommended | - | - |
| ASIL-A | Highly Recommended | Recommended | - |
| ASIL-B | Required (100%) | Required (100%) | Highly Recommended |
| ASIL-C | Required (100%) | Required (100%) | Required |
| ASIL-D | Required (100%) | Required (100%) | Required |

## Test Result ID

Test results use the test case ID with timestamp:

```
FBMS-TC-UT-SOC-001_2025-12-17_PASS
FBMS-TC-IT-BMS-001_2025-12-17_FAIL
```

## foxBMS Unity Test Framework

```c
void setUp(void) {
    /* Setup code */
}

void tearDown(void) {
    /* Cleanup code */
}

/* @test FBMS-TC-UT-SOC-001 */
void test_SOC_Calculate_ValidInput(void) {
    /* Arrange */
    SOC_Initialize();

    /* Act */
    int32_t result = SOC_Calculate(100, 1000);

    /* Assert */
    TEST_ASSERT_EQUAL_INT32(expected, result);
}
```
