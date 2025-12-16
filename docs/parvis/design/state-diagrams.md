# State Machine Diagrams

**Document ID**: FBMS-WP-SWE3-STD
**Version**: 1.0.0
**Date**: 2025-12-16
**Status**: Draft
**Classification**: Technical
**ASPICE Process**: SWE.3 (Software Detailed Design and Unit Construction)
**Target ASIL**: ASIL-D

---

## Document Control

### Revision History

| Version | Date       | Author                   | Description                    |
|---------|------------|--------------------------|--------------------------------|
| 1.0.0   | 2025-12-16 | PARVIS-AI-Orchestrator   | Initial state diagrams         |

---

## 1. BMS Main State Machine

### 1.1 State Diagram

```mermaid
stateDiagram-v2
    [*] --> UNINITIALIZED

    UNINITIALIZED --> INITIALIZATION : INIT_REQUEST

    INITIALIZATION --> INITIALIZED : Init Complete

    INITIALIZED --> IDLE : IMD Init Complete

    IDLE --> OPEN_CONTACTORS : STANDBY Request
    IDLE --> OPEN_CONTACTORS : Fatal Error

    OPEN_CONTACTORS --> STANDBY : All Contactors Open (Normal)
    OPEN_CONTACTORS --> ERROR : All Contactors Open (Error)

    STANDBY --> PRECHARGE : NORMAL Request
    STANDBY --> PRECHARGE : CHARGE Request
    STANDBY --> OPEN_CONTACTORS : Fatal Error

    PRECHARGE --> NORMAL : Precharge OK (Normal)
    PRECHARGE --> DISCHARGE : Precharge OK (Discharge)
    PRECHARGE --> CHARGE : Precharge OK (Charge)
    PRECHARGE --> STANDBY : Precharge Failed
    PRECHARGE --> OPEN_CONTACTORS : Fatal Error

    NORMAL --> STANDBY : STANDBY Request
    NORMAL --> OPEN_CONTACTORS : Fatal Error

    DISCHARGE --> STANDBY : STANDBY Request
    DISCHARGE --> OPEN_CONTACTORS : Fatal Error

    CHARGE --> STANDBY : STANDBY Request
    CHARGE --> OPEN_CONTACTORS : Fatal Error

    ERROR --> [*] : Power Cycle Required
```

### 1.2 State Description Table

| State          | Entry Condition              | Exit Condition               | Activities                    |
|----------------|------------------------------|------------------------------|-------------------------------|
| UNINITIALIZED  | Power-on                     | INIT_REQUEST                 | Wait for init request         |
| INITIALIZATION | INIT_REQUEST received        | Init complete                | Initialize modules            |
| INITIALIZED    | Init complete                | IMD init complete            | Wait for IMD                  |
| IDLE           | IMD ready                    | STANDBY request or error     | Monitor, report via CAN       |
| OPEN_CONTACTORS| Request or error             | All contactors open          | Open contactors sequence      |
| STANDBY        | Contactors open (normal)     | NORMAL/CHARGE request        | Ready for operation           |
| PRECHARGE      | NORMAL/CHARGE request        | Precharge complete/failed    | Execute precharge sequence    |
| NORMAL         | Precharge OK (normal)        | STANDBY request or error     | Normal operation              |
| DISCHARGE      | Precharge OK (discharge)     | STANDBY request or error     | Discharge operation           |
| CHARGE         | Precharge OK (charge)        | STANDBY request or error     | Charge operation              |
| ERROR          | Fatal error + contactors open| Power cycle                  | Safe state, log error         |

---

## 2. BMS Precharge Substate Machine

### 2.1 State Diagram

```mermaid
stateDiagram-v2
    [*] --> ENTRY

    ENTRY --> CHECK_ERROR_FLAGS_PRECHARGE : Timer Elapsed

    CHECK_ERROR_FLAGS_PRECHARGE --> PRECHARGE_CLOSE_MINUS : No Errors
    CHECK_ERROR_FLAGS_PRECHARGE --> [*] : Fatal Error (to OPEN_CONTACTORS)

    PRECHARGE_CLOSE_MINUS --> PRECHARGE_CLOSE_PRECHARGE : Minus Closed
    PRECHARGE_CLOSE_MINUS --> [*] : Timeout (to STANDBY)

    PRECHARGE_CLOSE_PRECHARGE --> PRECHARGE_CHECK_VOLTAGES : Precharge Closed
    PRECHARGE_CLOSE_PRECHARGE --> [*] : Timeout (to STANDBY)

    PRECHARGE_CHECK_VOLTAGES --> PRECHARGE_OPEN_PRECHARGE : Voltage OK
    PRECHARGE_CHECK_VOLTAGES --> [*] : Timeout (to STANDBY)
    PRECHARGE_CHECK_VOLTAGES --> [*] : Fatal Error (to OPEN_CONTACTORS)

    PRECHARGE_OPEN_PRECHARGE --> CLOSE_SECOND_CONTACTOR_PLUS : Precharge Open

    CLOSE_SECOND_CONTACTOR_PLUS --> CHECK_STRING_CLOSED : Plus Closed
    CLOSE_SECOND_CONTACTOR_PLUS --> [*] : Timeout (to STANDBY)

    CHECK_STRING_CLOSED --> [*] : Success (to NORMAL/CHARGE)
```

### 2.2 Precharge Timing Sequence

```mermaid
sequenceDiagram
    participant BMS
    participant CONT as Contactor
    participant MEAS as Measurement

    BMS->>CONT: Close MINUS contactor
    CONT-->>BMS: MINUS feedback OK

    Note over BMS: Wait 200ms

    BMS->>CONT: Close PRECHARGE contactor
    CONT-->>BMS: PRECHARGE feedback OK

    loop Check Voltage (max 2s)
        BMS->>MEAS: Get voltage difference
        MEAS-->>BMS: Voltage diff < 1000mV?
        alt Voltage OK
            Note over BMS: Precharge Complete
        else Voltage Not OK
            Note over BMS: Continue waiting
        end
    end

    BMS->>CONT: Close PLUS contactor
    CONT-->>BMS: PLUS feedback OK

    BMS->>CONT: Open PRECHARGE contactor
    CONT-->>BMS: PRECHARGE open OK

    Note over BMS: Transition to NORMAL/CHARGE
```

---

## 3. BMS Contactor Opening Substate Machine

### 3.1 State Diagram

```mermaid
stateDiagram-v2
    [*] --> ENTRY

    ENTRY --> HANDLE_30C_LOSS : 30C Supply Lost
    ENTRY --> OPEN_ALL_PRECHARGE : Normal Opening

    HANDLE_30C_LOSS --> OPEN_STRINGS_EXIT : All Contactors Opened

    OPEN_ALL_PRECHARGE --> OPEN_FIRST_STRING_CONTACTOR : Precharge Open

    OPEN_FIRST_STRING_CONTACTOR --> OPEN_SECOND_STRING_CONTACTOR : First Open
    OPEN_FIRST_STRING_CONTACTOR --> OPEN_FIRST_STRING_CONTACTOR : Current Too High

    OPEN_SECOND_STRING_CONTACTOR --> CHECK_SECOND_STRING : Wait Timer

    CHECK_SECOND_STRING --> OPEN_FIRST_STRING_CONTACTOR : More Strings
    CHECK_SECOND_STRING --> OPEN_STRINGS_EXIT : Last String
    CHECK_SECOND_STRING --> OPEN_FIRST_STRING_CONTACTOR : Timeout

    OPEN_STRINGS_EXIT --> [*] : Standby Request (to STANDBY)
    OPEN_STRINGS_EXIT --> [*] : Error (to ERROR)
```

### 3.2 String Opening Sequence

```mermaid
sequenceDiagram
    participant BMS
    participant CONT as Contactor
    participant CURRENT as Current Sensor

    BMS->>CONT: Open all PRECHARGE contactors
    CONT-->>BMS: All PRECHARGE open

    Note over BMS: Wait 50ms

    loop For each string (highest to lowest)
        BMS->>CURRENT: Get string current
        alt Current < Break Threshold
            BMS->>CONT: Open first contactor (preferred direction)
            CONT-->>BMS: First contactor open
            Note over BMS: Wait 100ms
            BMS->>CONT: Open second contactor
            CONT-->>BMS: Second contactor open
        else Current Too High
            Note over BMS: Wait for current to decrease
            alt Timeout exceeded
                BMS->>BMS: Set ALERT mode
                BMS->>CONT: Force open contactors
            end
        end
    end

    Note over BMS: All strings open
```

---

## 4. SBC State Machine

### 4.1 State Diagram

```mermaid
stateDiagram-v2
    [*] --> UNINITIALIZED

    UNINITIALIZED --> INITIALIZATION : INIT_REQUEST

    state INITIALIZATION {
        [*] --> ENTRY
        ENTRY --> RESET_FEC_PART1 : Init FS Phase OK
        ENTRY --> ENTRY : Init Failed (retry max 3)
        RESET_FEC_PART1 --> RESET_FEC_PART2 : Got WD Count
        RESET_FEC_PART2 --> SAFETY_PATH_CHECK : FEC = 0
        RESET_FEC_PART2 --> RESET_FEC_PART2 : FEC != 0 (retry)
        SAFETY_PATH_CHECK --> [*] : Paths OK
    }

    INITIALIZATION --> RUNNING : Init Success
    INITIALIZATION --> ERROR : Init Failed (max retries)

    RUNNING --> RUNNING : WD Trigger OK
    RUNNING --> ERROR : WD Timeout

    ERROR --> [*] : Power Cycle Required
```

### 4.2 SBC Initialization Sequence

```mermaid
sequenceDiagram
    participant SBC as SBC Module
    participant FS85 as FS85xx IC
    participant GPIO

    SBC->>FS85: Read OTP CRC
    FS85-->>SBC: CRC OK

    SBC->>FS85: Verify LBIST/ABIST
    FS85-->>SBC: Self-test passed

    SBC->>FS85: Configure Watchdog
    FS85-->>SBC: Config ACK

    SBC->>FS85: Configure FSSM
    FS85-->>SBC: Config ACK

    SBC->>FS85: Close INIT_FS
    FS85-->>SBC: INIT_FS closed

    Note over SBC: Start periodic WD triggers

    loop Required WD refreshes
        SBC->>FS85: Trigger Watchdog
        FS85-->>SBC: Good refresh
    end

    SBC->>FS85: Check FEC = 0
    FS85-->>SBC: FEC = 0

    SBC->>GPIO: Test RSTB path
    GPIO-->>SBC: RSTB OK

    SBC->>GPIO: Test FS0B path
    GPIO-->>SBC: FS0B OK

    SBC->>FS85: Release FS0B
    FS85-->>SBC: FS0B released

    Note over SBC: Transition to RUNNING
```

---

## 5. Contactor State Transitions

### 5.1 Single Contactor State

```mermaid
stateDiagram-v2
    [*] --> OFF

    OFF --> CLOSING : Close Request
    CLOSING --> ON : Feedback = Closed
    CLOSING --> OFF : Timeout

    ON --> OPENING : Open Request
    OPENING --> OFF : Feedback = Open
    OPENING --> ON : Timeout

    ON --> FEEDBACK_ERROR : Feedback Mismatch
    OFF --> FEEDBACK_ERROR : Feedback Mismatch

    FEEDBACK_ERROR --> OFF : Error Handled
```

### 5.2 String Contactor Sequence

```mermaid
sequenceDiagram
    participant BMS
    participant MINUS as MINUS Contactor
    participant PRECH as PRECHARGE Contactor
    participant PLUS as PLUS Contactor

    Note over BMS,PLUS: Closing Sequence
    BMS->>MINUS: Close
    MINUS-->>BMS: Closed
    BMS->>PRECH: Close
    PRECH-->>BMS: Closed
    Note over BMS: Wait for precharge
    BMS->>PLUS: Close
    PLUS-->>BMS: Closed
    BMS->>PRECH: Open
    PRECH-->>BMS: Open

    Note over BMS,PLUS: Opening Sequence
    BMS->>PRECH: Open (if closed)
    PRECH-->>BMS: Open
    BMS->>PLUS: Open (or MINUS based on current)
    PLUS-->>BMS: Open
    BMS->>MINUS: Open
    MINUS-->>BMS: Open
```

---

## 6. AFE Measurement State Machine

### 6.1 State Diagram

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> START_ADC : Trigger

    START_ADC --> WAIT_CONVERSION : ADCV Command Sent

    WAIT_CONVERSION --> READ_VOLTAGES : Conversion Complete
    WAIT_CONVERSION --> ERROR : Timeout

    READ_VOLTAGES --> VALIDATE_PEC : Data Received

    VALIDATE_PEC --> STORE_DATA : PEC Valid
    VALIDATE_PEC --> RETRY : PEC Invalid

    RETRY --> START_ADC : Retry Count < Max
    RETRY --> ERROR : Max Retries

    STORE_DATA --> START_TEMPERATURE : Voltage Done

    START_TEMPERATURE --> WAIT_TEMP_CONV : ADAX Command Sent

    WAIT_TEMP_CONV --> READ_TEMPERATURE : Conversion Complete

    READ_TEMPERATURE --> VALIDATE_TEMP_PEC : Data Received

    VALIDATE_TEMP_PEC --> STORE_TEMP : PEC Valid
    VALIDATE_TEMP_PEC --> ERROR : PEC Invalid

    STORE_TEMP --> IDLE : Cycle Complete

    ERROR --> IDLE : Error Handled
```

### 6.2 AFE Communication Sequence

```mermaid
sequenceDiagram
    participant AFE as AFE Driver
    participant SPI
    participant IC as AFE IC
    participant DB as Database

    AFE->>SPI: Send ADCV Command + PEC
    SPI->>IC: isoSPI Transfer
    IC-->>SPI: ACK

    Note over AFE: Wait 2.3ms (conversion)

    AFE->>SPI: Send RDCVA Command + PEC
    SPI->>IC: isoSPI Transfer
    IC-->>SPI: Cell 1-3 Data + PEC

    AFE->>AFE: Verify PEC
    alt PEC OK
        AFE->>DB: Store Cell 1-3 Voltages
    else PEC Error
        AFE->>AFE: Increment error counter
    end

    AFE->>SPI: Send RDCVB Command + PEC
    SPI->>IC: isoSPI Transfer
    IC-->>SPI: Cell 4-6 Data + PEC

    Note over AFE: Continue for all register groups

    AFE->>DB: Store all validated voltages
```

---

## 7. System Power-Up Sequence

### 7.1 Initialization Flow

```mermaid
flowchart TD
    A[Power On] --> B[MCU Reset]
    B --> C[SBC Init]
    C --> D{SBC OK?}
    D -->|No| E[SBC Error]
    D -->|Yes| F[RTOS Start]
    F --> G[Database Init]
    G --> H[Driver Init]
    H --> I[AFE Init]
    I --> J{AFE OK?}
    J -->|No| K[AFE Error]
    J -->|Yes| L[BMS Init Request]
    L --> M[BMS State Machine Start]
    M --> N[Wait for IMD]
    N --> O{IMD Ready?}
    O -->|No| N
    O -->|Yes| P[System Ready]
    P --> Q[IDLE State]
```

---

## 8. Error Handling Flow

### 8.1 Fatal Error Response

```mermaid
flowchart TD
    A[Error Detected] --> B{Error Severity?}
    B -->|Warning| C[Log & Continue]
    B -->|Error| D[Increment Counter]
    B -->|Fatal| E[Start Delay Timer]

    D --> F{Counter > Threshold?}
    F -->|No| C
    F -->|Yes| E

    E --> G{Delay Elapsed?}
    G -->|No| G
    G -->|Yes| H[Transition to OPEN_CONTACTORS]

    H --> I[Open All Contactors]
    I --> J[Transition to ERROR State]
    J --> K[Report Error via CAN]
    K --> L[Wait for Power Cycle]
```

### 8.2 Error Priority Handling

```mermaid
sequenceDiagram
    participant DIAG as Diagnostics
    participant BMS
    participant CONT as Contactor
    participant CAN

    Note over DIAG: Error 1 detected (delay 100ms)
    DIAG->>BMS: Fatal error flag set
    BMS->>BMS: Start delay timer (100ms)

    Note over DIAG: Error 2 detected (delay 50ms)
    DIAG->>BMS: Second fatal error
    BMS->>BMS: Update delay to 50ms (shorter)

    Note over BMS: 50ms elapsed

    BMS->>CONT: Open all contactors
    CONT-->>BMS: Contactors open

    BMS->>CAN: Report ERROR state
    BMS->>BMS: Enter ERROR state
```

---

## 9. Watchdog Timing

### 9.1 SBC Watchdog Timing

```mermaid
gantt
    title SBC Watchdog Timing
    dateFormat X
    axisFormat %L

    section Window
    Closed Window   :done, 0, 0
    Open Window     :active, 0, 100

    section Triggers
    WD Trigger 1    :crit, milestone, 10, 0
    WD Trigger 2    :crit, milestone, 110, 0
    WD Trigger 3    :crit, milestone, 210, 0

    section Period
    Period 1        :0, 100
    Period 2        :100, 200
    Period 3        :200, 300
```

### 9.2 Task Timing Diagram

```mermaid
gantt
    title foxBMS Task Timing
    dateFormat X
    axisFormat %L

    section 1ms Task
    Task Execution :0, 1
    Task Execution :1, 2
    Task Execution :2, 3

    section 10ms Task
    BMS Trigger :0, 2
    SBC Trigger :2, 3
    CONT Check  :3, 4

    section 100ms Task
    AFE Measure :0, 5
    Algorithm   :5, 8
    SOA Check   :8, 10
```

---

**End of Document**

---

*Generated by PARVIS-AI-Orchestrator for L3 Phase (Software Detailed Design)*
*ASPICE SWE.3 Compliance*
