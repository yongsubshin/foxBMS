---
name: parvis:run
description: "Execute PARVIS V-Model orchestrator pipeline"
argument-hint: 'MODULE - Target module (e.g., BMS, SOA, DIAG) or "all" for full extraction'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite, AskUserQuestion, Task, Skill
model: inherit
---

## Pre-execution Context

!git status --porcelain
!git branch --show-current

## Essential Files

@.claude/parvis-data/config/phase-status/BMS.json
@.claude/parvis-data/config/orchestrator-config.json
@.parvis/config.yaml

---

# PARVIS V-Model Orchestrator Pipeline

**Command Purpose**: Execute the full PARVIS V-Model development workflow from requirements extraction through phase progression.

**User Interaction Architecture**: AskUserQuestion must be used at COMMAND level only. Subagents via Task() are stateless and cannot interact with users.

**Language Configuration**: Output language is determined by `.parvis/config.yaml` field `language.parvis_run`. If not initialized, run `/parvis:init` first.

**Execution Model**: Commands orchestrate through `Task()` tool only.

---

## Command Overview

The `/parvis:run` command orchestrates the complete V-Model development workflow:

**Pipeline Flow:**
```
foxbms-2/src/ (source code)
       |
       v  parvis-aispec-code (extraction)
.claude/parvis-data/requirements/extracted/ (JSON)
       |
       v  parvis-aispec-transformer (normalization)
.claude/parvis-data/requirements/normalized/
       |
       v  parvis-aispec-reqid (ID assignment)
       |
       v  parvis-aispec-safety (ASIL classification)
       |
       v  parvis-ai-orchestrator (phase coordination)
docs/parvis/ (intermediate documentation)
```

---

## Execution Phases

### Phase 1: Status Check and Planning

**Objective**: Assess current phase status and determine execution plan

**Actions**:
1. Query current V-Model phase status for target module
2. Check quality gate status
3. Identify blocking issues
4. Present execution plan to user

**Checkpoint**: User approval required before proceeding

**Agent Delegation**:
```
Use the parvis-ai-orchestrator subagent to:
- Check current phase status for MODULE
- Verify quality gates
- Identify next required actions
- Generate execution plan
Output Language: Use language.parvis_run from .parvis/config.yaml for generated files
Response Language: Use language.claude_output from .parvis/config.yaml for user responses
```

### Phase 2: Phase Execution

**Objective**: Execute the appropriate V-Model phase activities

**Phase L1 (Requirements Extraction)**:
- Delegate to parvis-aispec-code for requirement extraction
- Run extraction_engine.py for target module
- Generate extraction reports

**Phase L2 (Normalization)**:
- Delegate to parvis-aispec-transformer for normalization
- Delegate to parvis-aispec-reqid for ID assignment
- Generate normalized requirement database

**Phase L3 (Safety Analysis)**:
- Delegate to parvis-aispec-safety for ASIL classification
- Generate safety analysis reports

**Phase L4 (Specification)**:
- Delegate to parvis-aispec-trace for traceability
- Generate specification documents to docs/parvis/

**Agent Selection by Phase**:
- L1: parvis-aispec-code
- L2: parvis-aispec-transformer, parvis-aispec-reqid
- L3: parvis-aispec-safety
- L4: parvis-aispec-trace, parvis-aidoc-aspice

### Phase 3: Quality Gate Verification

**Objective**: Verify phase completion meets quality criteria

**Actions**:
1. Run quality gate verification
2. Generate quality report
3. Determine phase transition eligibility

**Agent Delegation**:
```
Use the parvis-ai-orchestrator subagent to:
- Verify quality gates for current phase
- Generate quality report
- Recommend next steps
Output Language: Use language.parvis_run from .parvis/config.yaml for generated files
Response Language: Use language.claude_output from .parvis/config.yaml for user responses
```

### Phase 4: Output Generation

**Objective**: Generate documentation outputs to docs/parvis/

**Actions**:
1. Generate phase-appropriate documentation
2. Update traceability matrices
3. Create summary reports

**Output Structure**:
```
docs/parvis/
  requirements/     (requirement specifications)
  architecture/     (architecture design)
  design/          (detailed design)
  verification/    (verification reports)
  traceability/    (traceability matrices)
  system/          (system-level documents)
```

---

## Usage Examples

### Run for specific module:
```
/parvis:run BMS
```

### Run for all modules:
```
/parvis:run all
```

### Check status only:
```
/parvis:run BMS --status
```

---

## Quality Gates

### L1 Phase Gates:
- Extraction confidence >= 70%
- Source coverage >= 60%

### L2 Phase Gates:
- 100% requirements normalized
- 100% IDs assigned

### L3 Phase Gates:
- 100% safety analysis complete
- ASIL classification complete

### L4 Phase Gates:
- Specification documents generated
- Traceability >= 95%

---

## Error Handling

**Phase Blocked**:
- Report blocking issues
- Suggest remediation actions
- Offer manual override option

**Extraction Failure**:
- Log error details
- Retry with expanded patterns
- Report partial results

---

## Related Commands

- `/parvis:docs` - Generate final documentation from docs/parvis/

---

Version: 1.0.0
Last Updated: 2025-12-17
