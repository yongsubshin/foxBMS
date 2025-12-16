# BMS Compliance Quick Reference Guide

One-page reference for critical compliance requirements across automotive safety standards.

**Last Updated:** December 16, 2025

---

## Critical Compliance Requirements Matrix

### ISO 26262 Functional Safety - Key Requirements

**For ASIL-D (Highest Safety Level):**

| Requirement | Standard | Status | Evidence Needed |
|-------------|----------|--------|-----------------|
| Functional Safety Concept | ISO 26262 Concept Phase | Mandatory | HARA document with safety goals |
| PMHF Calculation | ISO 26262 Part 5 | Mandatory | Failure rate analysis with proof |
| MC/DC Coverage | ISO 26262 Part 6 | Highly Recommended | 100% MC/DC for safety functions |
| Statement Coverage | ISO 26262 Part 6 | Recommended | 100% of safety-critical code |
| Branch Coverage | ISO 26262 Part 6 | Highly Recommended | 100% for ASIL-D functions |
| Traceability | ISO 26262 Part 3 | Mandatory | Bidirectional requirement-test links |
| Safety Case | ISO 26262 Part 3 | Mandatory | Residual risk documentation |

**BMS Critical Functions (All ASIL-D):**
- Overcharge protection (>4.2V cell)
- Overdischarge protection (<2.5V cell)
- Overtemperature protection (>60°C typical)
- Overcurrent protection (current limiting)

---

### ASPICE Level 2 - Mandatory Work Products

**Core Work Products (100% Required):**

| Category | Document | Phase | Traceability Link |
|----------|----------|-------|-------------------|
| Planning | Project Plan | Initiation | Scope definition |
| Planning | Resource Plan | Initiation | Team and competencies |
| Planning | Risk Management Plan | Initiation | Risk identification |
| Requirements | SRS (Software Requirements Spec) | Analysis | Requirement definition |
| Requirements | Traceability Matrix | All | Requirements → Design → Code → Test |
| Design | Software Design Document | Design | Design specification |
| Implementation | Source Code | Implementation | Code baseline |
| Implementation | Code Review Records | Implementation | Code quality evidence |
| Testing | Unit Test Plan & Results | Verification | Coverage metrics |
| Testing | System Test Plan & Results | Verification | Functional validation |
| Testing | Test Traceability Matrix | Verification | Test → Requirement links |
| Quality | QA Audit Records | All | Process compliance evidence |
| Configuration | Change Control Records | All | Change management proof |

**ASPICE 4.0 Change (December 2024):**
- Strategy documentation moved from Level 1 to Level 2
- Reduces VDA scope for faster development
- Easier Level 1 achievement
- Clearer Level 2 expectations

---

### MISRA C:2012 Compliance Thresholds

**Rule Category Compliance Targets (ASIL-D):**

| Rule Type | Count | ASIL-D Target | Deviation Allowed? |
|-----------|-------|---------------|-------------------|
| Mandatory | ~15 | 100% | No - zero exceptions |
| Required | ~90 | 100% | No for ASIL-D |
| Advisory | ~40 | 95%+ | Yes with documentation |

**Top Mandatory Rules for Safety-Critical Code:**
1. Rule 1.1: Text encoding (ASCII only)
2. Rule 10.1: Implicit conversion restrictions
3. Rule 13.5: Side effects in expressions
4. Rule 20.1: Pointer arithmetic restrictions
5. Rule 21.1: Standard library restrictions

**Verification Method:**
- Static analysis tool (SonarQube, LDRA, etc.)
- Code review for complex logic
- Deviation tracking with safety justification
- Metrics reporting for compliance evidence

---

### V-Model Verification - Traceability Structure

**Required Traceability Links:**

```
Requirements Specification
    ↓ (Forward Traceability)
Design Specification
    ↓ (Forward Traceability)
Source Code Implementation
    ↓ (Forward Traceability)
Unit/Integration Tests
    ↓ (Forward Traceability)
System Acceptance Tests
    ↓ (Verification Complete)
Safety Validation Evidence
```

**Backward Traceability (Audit Trail):**
```
Safety Validation Evidence
    ↑ (Backward Traceability)
Acceptance Test Results
    ↑ (Backward Traceability)
Unit Test Coverage
    ↑ (Backward Traceability)
Code Implementation
    ↑ (Backward Traceability)
Design Specification
    ↑ (Backward Traceability)
Requirements Definition
```

**Compliance Metrics:**
- 100% of requirements traced to design
- 100% of design traced to code
- 100% of code traced to tests
- 100% of tests traced to requirements
- No orphan requirements or tests

---

### MC/DC Testing - ASIL-D Requirements

**MC/DC Definition:**
Each condition in a decision must independently affect the outcome.

**Test Case Formula:**
- For N conditions in a decision: minimum N+1 test cases
- Example: 3 conditions (A, B, C) = 4 test cases minimum

**ASIL-D MC/DC Requirements:**
- Mandatory for all safety-critical functions
- 100% MC/DC coverage required
- 100% of tests must pass
- Traceability to requirements required

**BMS Functions Requiring 100% MC/DC:**

| Function | Example Conditions | Min Tests | Coverage Evidence |
|----------|-------------------|-----------|------------------|
| Overcharge Protection | voltage > MAX && charger_on | 3 | Coverage tool report |
| Overdischarge Protection | voltage < MIN \|\| load_critical | 3 | Coverage tool report |
| Thermal Protection | temp > LIMIT \|\| temp_rate > MAX | 3 | Coverage tool report |
| Current Limiting | charge_I > MAX \|\| discharge_I > MAX | 3 | Coverage tool report |

---

## Compliance Audit Checklist (High-Level)

### Phase 1: Documentation Assessment
- [ ] HARA and safety goals documented
- [ ] Technical safety requirements specified
- [ ] Design FMEA completed
- [ ] Software Design Document exists
- [ ] Test Plan covers all requirements

### Phase 2: Traceability Verification
- [ ] Requirements → Design traceability complete
- [ ] Design → Code traceability complete
- [ ] Code → Test traceability complete
- [ ] Test → Requirement traceability complete
- [ ] No orphan requirements or tests

### Phase 3: Code Compliance
- [ ] MISRA C:2012 100% mandatory rule compliance
- [ ] MISRA C:2012 100% required rule compliance (ASIL-D)
- [ ] Static analysis run and reviewed
- [ ] Code review records available
- [ ] Static analysis in CI/CD pipeline

### Phase 4: Testing Coverage
- [ ] MC/DC: 100% for safety-critical functions
- [ ] Statement Coverage: 100% for safety-critical code
- [ ] Branch Coverage: 100% for ASIL-C/D functions
- [ ] Integration tests executed
- [ ] System tests validate safety goals

### Phase 5: Process Compliance
- [ ] Project Plan with scope/schedule/resources
- [ ] Change Control procedures defined
- [ ] Configuration Management in place
- [ ] Quality Assurance audits documented
- [ ] Risk Management Plan active

---

## Common Compliance Gaps (From 2025 Research)

**Frequently Identified Gaps:**

1. **Incomplete Traceability**
   - Orphan requirements without test cases
   - Test cases without requirement links
   - Design changes not reflected in code
   - Impact: Assessment failure

2. **MISRA Deviations Without Justification**
   - Required rules violated without formal deviation
   - No safety analysis for exceptions
   - Missing deviation approval
   - Impact: ASIL-D assessment failure

3. **Inadequate MC/DC Coverage**
   - Only branch coverage, missing MC/DC
   - Partial MC/DC (e.g., 80% instead of 100%)
   - Manual testing without tool verification
   - Impact: ASIL-D assessment failure

4. **Missing Documentation**
   - No formal test plans
   - Design documentation incomplete
   - Missing code review records
   - Risk management not documented
   - Impact: ASPICE Level 2 failure

5. **Weak Change Control**
   - Code changes without configuration management
   - Test results not reproducible
   - Traceability not updated after changes
   - Impact: Audit traceability failure

---

## Recommended Assessment Timeline

**Week 1-2: Documentation Audit**
- Gather all compliance-related documents
- Assess completeness against checklists
- Identify critical gaps in documentation

**Week 3-4: Traceability Analysis**
- Build or verify traceability matrix
- Identify orphan requirements/tests
- Plan remediation for gaps

**Week 5-6: Code Assessment**
- Run static analysis (MISRA C:2012)
- Review MISRA deviations
- Plan code corrections

**Week 7-8: Testing Verification**
- Measure code coverage (MC/DC, statement, branch)
- Identify coverage gaps
- Plan additional test cases

**Week 9-10: Process Review**
- Audit project management processes
- Verify change control implementation
- Review configuration management
- Document QA activities

**Week 11-12: Gap Remediation**
- Execute identified improvements
- Update documentation
- Verify compliance with standards
- Prepare audit evidence package

---

## Tool Recommendations (2025)

**Requirements Management:**
- JAMA Connect (cloud-based, strong traceability)
- Polarion by Siemens (integrated with development)
- IBM DOORS (industry standard, complex projects)
- Ketryx (compliance-focused, audit-ready)

**Static Analysis (MISRA C:2012):**
- SonarQube (open source, free option)
- LDRA TBrun (safety-critical focus)
- Clang+Scan-build (free, good for C)
- Parasoft C/C++Test (commercial, comprehensive)

**Code Coverage (MC/DC):**
- Clang Coverage (with -fcoverage-mcdc flag, free)
- LDRA (integrated with static analysis)
- QA Systems MC/DC (specialized tool)
- Rapita Systems (embedded systems focus)

**Test Management:**
- TestRail (test case management)
- Zephyr (Jira integrated)
- xRay (Atlassian ecosystem)
- Qmetry (cross-platform)

**Version Control & CI/CD:**
- Git + GitHub/GitLab (standard practice)
- Jenkins (CI/CD pipeline)
- GitHub Actions (integrated with GitHub)
- GitLab CI (integrated with GitLab)

---

## Standards References

**ISO 26262:2018 - Functional Safety of Electrical/Electronic Systems**
- Part 1: Concepts and definitions
- Part 2: Management of functional safety
- Part 3: Product development at the concept phase
- Part 4: Product development at the system level
- Part 5: Product development at the hardware level
- Part 6: Product development at the software level
- Part 7: Communication and management of safety goals
- Part 8: Supporting processes
- Part 9: Automotive Safety Integrity Level (ASIL)
- Part 10: Guideline on ISO 26262

**Automotive SPICE 4.0 (December 2024)**
- Released by VDA QMC
- Replaced ASPICE 3.1
- Enhanced Agile and DevOps support
- Clearer work product expectations

**MISRA C:2012**
- 143 rules and 16 directives
- Mandatory, Required, and Advisory categories
- Covers C90 and C99 standards
- Focus on safety-critical embedded systems

**V-Model (IEC/IEEE 42010:2011)**
- System decomposition → integration
- Left side: design and development
- Right side: verification and validation
- Emphasizes traceability

**ISO 61508 (Generic Functional Safety)**
- Foundation for domain-specific standards
- SIL 1-4 levels (similar to ASIL A-D)
- Referenced by ISO 26262 for methodology

---

## Research Sources (December 2025)

All compliance information in this guide is based on current web research from:
- Official ISO 26262 standards documentation
- VDA QMC ASPICE 4.0 Pocket Guide
- Industry compliance frameworks (LDRA, QA Systems, Ketryx)
- Academic research on automotive safety
- Recent case studies (FPT Industrial ASIL C certification, 2025)

For the most current guidance, consult:
1. Official standard documents (ISO, VDA)
2. Tool vendor documentation
3. Industry compliance consultants
4. Peer organization assessment results

---

**End of Quick Reference Guide**
