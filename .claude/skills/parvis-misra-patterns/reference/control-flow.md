# Control Flow Patterns

MISRA C:2012 Rules 15.x, 16.x - Control structures for foxBMS.

## Switch Statement Patterns

### CF-001: Switch Default Case (Rule 16.4)
```c
/* CORRECT */
switch (state) {
    case STATE_INIT:
        /* handle */
        break;
    case STATE_RUN:
        /* handle */
        break;
    default:
        FAS_ASSERT(FAS_TRAP);
        break;
}

/* WRONG - missing default */
switch (state) {
    case STATE_INIT:
        break;
    case STATE_RUN:
        break;
}
```

### CF-002: Switch Break Statement (Rule 16.3)
```c
/* CORRECT */
switch (value) {
    case 1:
        action1();
        break;
    case 2:
        action2();
        break;
    default:
        break;
}

/* WRONG - fall-through without comment */
switch (value) {
    case 1:
        action1();
    case 2:  /* Unintentional fall-through */
        action2();
        break;
}
```

### CF-003: Intentional Fall-Through (Rule 16.3)
```c
/* CORRECT - documented fall-through */
switch (errorType) {
    case ERROR_CRITICAL:
    case ERROR_SEVERE:
        /* FALL THROUGH - both handled same way */
        LogError();
        break;
    default:
        break;
}
```

### CF-004: Switch Expression Type (Rule 16.7)
```c
/* CORRECT - enum type */
switch (bmsState) {
    case BMS_STATE_INIT:
    case BMS_STATE_IDLE:
    case BMS_STATE_RUNNING:
    default:
        break;
}

/* WRONG - boolean in switch */
switch (isActive) {  /* Use if-else instead */
    case true: break;
    case false: break;
}
```

## Return Statement Patterns

### CF-005: Single Return Statement (Rule 15.5)
```c
/* CORRECT */
bool IsValid(uint32_t value) {
    bool result = false;

    if (value < MAX_VALUE) {
        result = true;
    }

    return result;
}

/* WRONG - multiple returns */
bool IsValid(uint32_t value) {
    if (value >= MAX_VALUE) {
        return false;
    }
    return true;
}
```

### CF-006: Return in Void Function (Rule 15.5)
```c
/* CORRECT */
void ProcessData(uint32_t data) {
    if (data == 0u) {
        /* Early exit for invalid data */
        return;
    }
    /* Process valid data */
}

/* Note: Single early return for error is acceptable */
```

## Loop Patterns

### CF-007: For Loop Counter (Rule 14.2)
```c
/* CORRECT */
for (uint16_t i = 0u; i < count; i++) {
    /* loop body - do not modify i */
}

/* WRONG - modifying loop counter */
for (uint16_t i = 0u; i < count; i++) {
    if (condition) {
        i++;  /* Violation */
    }
}
```

### CF-008: While Loop Condition (Rule 14.3)
```c
/* CORRECT */
while (continueProcessing == true) {
    /* process */
    if (exitCondition) {
        continueProcessing = false;
    }
}

/* WRONG - infinite loop without exit */
while (true) {
    /* process */
    if (exitCondition) {
        break;  /* Hidden exit */
    }
}
```

### CF-009: Loop Body Braces (Rule 15.6)
```c
/* CORRECT */
for (uint16_t i = 0u; i < count; i++) {
    ProcessItem(i);
}

/* WRONG */
for (uint16_t i = 0u; i < count; i++)
    ProcessItem(i);  /* Missing braces */
```

## Conditional Patterns

### CF-010: If-Else Braces (Rule 15.6)
```c
/* CORRECT */
if (condition) {
    action1();
} else {
    action2();
}

/* WRONG */
if (condition)
    action1();
else
    action2();
```

### CF-011: Nested If Depth (Rule 15.x)
```c
/* CORRECT - flat structure */
if (!precondition1) {
    return STD_NOT_OK;
}
if (!precondition2) {
    return STD_NOT_OK;
}
/* Main logic here */

/* WRONG - deep nesting */
if (cond1) {
    if (cond2) {
        if (cond3) {
            /* Too deep */
        }
    }
}
```

### CF-012: Else-If Chain Termination (Rule 15.7)
```c
/* CORRECT */
if (value == 1u) {
    /* handle 1 */
} else if (value == 2u) {
    /* handle 2 */
} else {
    /* handle all other cases */
}

/* WRONG - missing final else */
if (value == 1u) {
    /* handle 1 */
} else if (value == 2u) {
    /* handle 2 */
}
/* What about other values? */
```

## foxBMS State Machine Pattern

### CF-013: BMS State Machine Template
```c
void BMS_ProcessStateMachine(void) {
    switch (bms_state.currentState) {
        case BMS_STATE_UNINITIALIZED:
            BMS_HandleUninitialized();
            break;

        case BMS_STATE_INITIALIZATION:
            BMS_HandleInitialization();
            break;

        case BMS_STATE_IDLE:
            BMS_HandleIdle();
            break;

        case BMS_STATE_RUNNING:
            BMS_HandleRunning();
            break;

        case BMS_STATE_ERROR:
            BMS_HandleError();
            break;

        default:
            /* Invalid state - should never reach here */
            FAS_ASSERT(FAS_TRAP);
            break;
    }
}
```

## Summary Table

| ID | Rule | Pattern | Severity |
|----|------|---------|----------|
| CF-001 | 16.4 | Default case required | Required |
| CF-002 | 16.3 | Break after case | Required |
| CF-003 | 16.3 | Document fall-through | Required |
| CF-004 | 16.7 | Enum in switch | Advisory |
| CF-005 | 15.5 | Single return | Advisory |
| CF-006 | 15.5 | Early return for error | Advisory |
| CF-007 | 14.2 | Don't modify counter | Required |
| CF-008 | 14.3 | Avoid infinite loops | Required |
| CF-009 | 15.6 | Loop braces | Required |
| CF-010 | 15.6 | If-else braces | Required |
| CF-011 | - | Limit nesting depth | Advisory |
| CF-012 | 15.7 | Final else required | Required |
