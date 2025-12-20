---
name: parvis:docs
description: "Generate final documentation from PARVIS intermediate outputs"
argument-hint: '[FORMAT] - Output format: all (default), sphinx, doxygen, html, or portal'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite, AskUserQuestion, Task, Skill
model: inherit
---

## Pre-execution Context

!git status --porcelain
!ls -la docs/parvis/ 2>/dev/null | head -10
!ls -la docs/final/ 2>/dev/null | head -10

## Essential Files

@docs/parvis/README.md
@docs/final/README.md
@.parvis/config.yaml

---

# PARVIS Documentation Generator

**Command Purpose**: Generate final documentation packages from PARVIS intermediate outputs.

**User Interaction Architecture**: AskUserQuestion must be used at COMMAND level only.

**Language Configuration**: Output language is determined by `.parvis/config.yaml` field `language.parvis_docs`. If not initialized, run `/parvis:init` first.

**Execution Model**: Commands orchestrate through `Task()` tool only.

---

## Command Overview

The `/parvis:docs` command transforms intermediate PARVIS documentation into final output formats:

**Documentation Flow:**
```
docs/parvis/ (intermediate outputs)
       |
       v  parvis-aidoc-generator
docs/final/
  +-- sphinx/      (process documentation)
  +-- doxygen/     (API reference)
  +-- html/        (interactive portal)
  +-- reports/     (generated reports)
```

---

## Output Formats

### 1. Sphinx Documentation (`sphinx`)

ASPICE-compliant process documentation:
- V-Model process docs (SYS.1-SYS.5, SWE.1-SWE.6)
- Requirements specification
- Architecture design
- Traceability matrices

**Build Command**: `sphinx-build -b html . _build/html`

### 2. Doxygen API Reference (`doxygen`)

Complete C API documentation:
- Function documentation from source
- Call graphs and dependencies
- Cross-referenced source browser

**Build Command**: `doxygen Doxyfile`

### 3. HTML Portal (`html`)

Modern interactive documentation:
- Dashboard with key metrics
- Interactive traceability matrix
- MISRA compliance dashboard
- Quality metrics visualization

### 4. Full Portal (`all` or `portal`)

All formats combined with unified entry point:
- Main index.html portal
- Links to all documentation sections
- Compliance badges and metrics

---

## Execution Phases

### Phase 1: Source Analysis

**Objective**: Analyze PARVIS intermediate outputs

**Actions**:
1. Scan docs/parvis/ structure
2. Parse all JSON and MD files
3. Build content inventory
4. Identify any gaps

**Agent Delegation**:
```
Use the parvis-aidoc-generator subagent to:
- Analyze docs/parvis/ content
- Build documentation inventory
- Identify gaps or missing sections
- Report analysis results
Output Language: Use language.parvis_docs from .parvis/config.yaml for generated documentation
Response Language: Use language.claude_output from .parvis/config.yaml for user responses
```

### Phase 2: Format Selection

**Objective**: Confirm output format with user

**Checkpoint**: User approval required

**Options**:
- all: Generate all formats (recommended)
- sphinx: Process documentation only
- doxygen: API reference only
- html: Interactive portal only

### Phase 3: Documentation Generation

**Objective**: Generate selected documentation formats

**For Sphinx**:
1. Convert PARVIS markdown to RST
2. Generate requirement tables
3. Create cross-references
4. Build HTML output

**For Doxygen**:
1. Configure Doxyfile
2. Parse source code
3. Generate API docs
4. Create search index

**For HTML Portal**:
1. Generate dashboard
2. Create traceability viewer
3. Build MISRA dashboard
4. Generate metrics charts

**Agent Delegation**:
```
Use the parvis-aidoc-generator subagent to:
- Generate [FORMAT] documentation
- Source: docs/parvis/
- Output: docs/final/
- Include traceability matrices
- Include compliance badges
Output Language: Use language.parvis_docs from .parvis/config.yaml for generated documentation
Response Language: Use language.claude_output from .parvis/config.yaml for user responses
```

### Phase 4: Build and Validate

**Objective**: Execute build tools and validate outputs

**Actions**:
1. Run build.sh for selected formats
2. Validate HTML links
3. Check completeness
4. Generate build report

**Build Script Location**: `docs/final/build.sh`

### Phase 5: Summary Report

**Objective**: Report generation results

**Report Contents**:
- Files generated count
- Build status (success/warnings/errors)
- Output locations
- View instructions

---

## Usage Examples

### Generate all documentation:
```
/parvis:docs
/parvis:docs all
```

### Generate Sphinx only:
```
/parvis:docs sphinx
```

### Generate Doxygen only:
```
/parvis:docs doxygen
```

### Generate HTML portal only:
```
/parvis:docs html
```

---

## Prerequisites

### Required:
- docs/parvis/ populated with PARVIS outputs
- Python 3 installed

### Optional (for full builds):
- Doxygen: `sudo apt install doxygen graphviz`
- Sphinx: `pip install sphinx sphinx-rtd-theme`
- PlantUML: `sudo apt install plantuml`

---

## Output Structure

```
docs/final/
+-- index.html              # Main portal entry
+-- README.md               # Documentation guide
+-- build.sh                # Build script
+-- Doxyfile                # Doxygen config
|
+-- sphinx/                 # Sphinx documentation
|   +-- conf.py
|   +-- index.rst
|   +-- v-model/
|   +-- requirements/
|   +-- architecture/
|   +-- design/
|   +-- verification/
|   +-- traceability/
|
+-- doxygen/                # Doxygen API docs
|   +-- html/
|       +-- index.html
|       +-- search/
|
+-- html/                   # Interactive portal
|   +-- assets/
|   +-- traceability/
|   +-- misra/
|   +-- metrics/
|   +-- v-model/
|
+-- reports/                # Generated reports
```

---

## Quality Metrics

Expected outputs:
- Software Requirements: 648+
- Safety Requirements: 147+ (ASIL classified)
- Traceability Coverage: 100%
- MISRA Compliance: ~99%
- Test Cases: 570+

---

## Error Handling

**Missing PARVIS Content**:
- Report missing sections
- Suggest running `/parvis:run` first
- Continue with available content

**Build Tool Missing**:
- Skip unavailable formats
- Generate placeholder pages
- Report installation instructions

**Validation Errors**:
- Log broken links
- Flag incomplete sections
- Generate error report

---

## Related Commands

- `/parvis:run` - Run PARVIS orchestrator pipeline first

---

Version: 1.0.0
Last Updated: 2025-12-17
