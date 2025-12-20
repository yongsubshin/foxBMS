---
name: parvis:init
description: "Initialize PARVIS language settings for Claude output, run outputs, and documentation"
allowed-tools: Read, Write, Edit, AskUserQuestion
model: inherit
---

## Pre-execution Context

!ls -la .parvis/ 2>/dev/null
!cat .parvis/config.yaml 2>/dev/null | head -20

## Essential Files

@.parvis/config.yaml

---

# PARVIS Language Configuration Initializer

**Command Purpose**: Configure language settings for PARVIS workflow outputs.

**User Interaction Architecture**: All language preference questions must be asked at COMMAND level using AskUserQuestion. Questions must be in English.

---

## Language Settings Overview

PARVIS supports three independent language settings:

- **claude_output**: Claude response language for user-facing outputs
- **parvis_run**: Language for `/parvis:run` generated files (requirements, reports)
- **parvis_docs**: Language for `/parvis:docs` final documentation (Sphinx, HTML portal)

Supported Languages:
- en: English
- ko: Korean
- ja: Japanese
- zh: Chinese

---

## Execution Flow

### Phase 1: Directory Check

**Objective**: Ensure .parvis directory exists

**Actions**:
1. Check if `.parvis/` directory exists
2. If not exists: Create the directory
3. Proceed directly to language selection

### Phase 2: Language Selection

**Objective**: Gather user language preferences using AskUserQuestion

**IMPORTANT**: All questions must be asked in English because the user's language preference is not yet known.

**Question 1 - Claude Output Language**:
Use AskUserQuestion with the following:
- Question: "Select the language for Claude responses:"
- Header: "Claude Output"
- Options:
  - English: Claude will respond in English
  - Korean: Claude will respond in Korean
  - Japanese: Claude will respond in Japanese
  - Chinese: Claude will respond in Chinese

**Question 2 - PARVIS Run Output Language**:
Use AskUserQuestion with the following:
- Question: "Select the language for PARVIS Run generated files:"
- Header: "PARVIS Run"
- Options:
  - English (Recommended): Internal data in English for international standard compliance
  - Korean: Requirements, reports, and extractions in Korean
  - Japanese: Requirements, reports, and extractions in Japanese
  - Chinese: Requirements, reports, and extractions in Chinese

**Question 3 - PARVIS Docs Output Language**:
Use AskUserQuestion with the following:
- Question: "Select the language for PARVIS documentation:"
- Header: "PARVIS Docs"
- Options:
  - English: Final documentation in English
  - Korean: Final documentation in Korean
  - Japanese: Final documentation in Japanese
  - Chinese: Final documentation in Chinese

### Phase 3: Write Configuration

**Objective**: Save user selections to `.parvis/config.yaml`

**Actions**:
1. Map user selections to language codes:
   - English maps to en
   - Korean maps to ko
   - Japanese maps to ja
   - Chinese maps to zh

2. Create or update `.parvis/config.yaml` with selected values

3. Set `metadata.initialized` to true

4. Set `metadata.last_updated` to current timestamp

### Phase 4: Confirmation

**Objective**: Confirm configuration was saved successfully

**Report**:
Display the saved configuration to the user in their selected claude_output language:
- Show all three language settings
- Confirm the config file location
- Mention that settings can be changed by running `/parvis:init` again

---

## Configuration File Structure

The `.parvis/config.yaml` file structure:

```yaml
language:
  claude_output: [en|ko|ja|zh]
  parvis_run: [en|ko|ja|zh]
  parvis_docs: [en|ko|ja|zh]

metadata:
  version: "1.0.0"
  initialized: true
  last_updated: [ISO timestamp]
```

---

## Usage Examples

### Initialize or reconfigure:
```
/parvis:init
```

Running this command will always show language selection options and save the new settings.

---

## Integration Points

After configuration, the language settings are used by:

- **CLAUDE.md**: References `.parvis/config.yaml` for `claude_output`
- **/parvis:run**: Uses `parvis_run` for generated file language
- **/parvis:docs**: Uses `parvis_docs` for documentation language

---

## Error Handling

**Missing .parvis/ Directory**:
- Create the directory automatically
- Proceed with configuration

**Invalid Selection**:
- Re-prompt the question
- Use default (English) if unable to resolve

---

Version: 1.0.0
Last Updated: 2025-12-19
