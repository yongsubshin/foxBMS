# BMS Compliance Gap Analysis Template

Structured template for identifying and tracking compliance gaps against automotive safety standards.

**Project:** Fox BMS (Battery Management System)
**Assessment Date:** [To be filled]
**Assessed By:** [Team member name]
**Assessment Scope:** [e.g., "Software development processes, code quality, testing coverage"]

---

## Instructions for Use

1. For each standard (ISO 26262, ASPICE, MISRA, V-Model, MC/DC):
   - Review current state against requirement
   - Document evidence of compliance or non-compliance
   - Assess severity (Critical/High/Medium/Low)
   - Assign ownership for remediation

2. Critical gaps block certification; must be resolved before audit

3. Update this document as gaps are closed

4. Use evidence section for audit trail documentation

---

## Section A: ISO 26262 Functional Safety Gaps

### A1. Concept Phase Gaps

**Gap A1.1: HARA Documentation**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | HARA (Hazard Analysis and Risk Assessment) must document all hazards, risks, and ASIL assignments |
| Current State | [Document your current state] |
| Gap Description | [Describe what is missing] |
| Required State | Complete HARA document covering: overcharge, overdischarge, thermal, overcurrent, integration hazards |
| Evidence Location | [Where evidence will/can be found] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why the gap exists] |
| Remediation Plan | [Steps to close gap] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap A1.2: Safety Goals Definition**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Safety goals must be defined for each ASIL-D function |
| Current State | [Document your current state] |
| Gap Description | [Describe missing safety goals] |
| Required State | Safety goals for: overcharge protection, overdischarge protection, thermal protection, overcurrent protection |
| Evidence Location | [Document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Steps to define safety goals] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### A2. Development Phase Gaps

**Gap A2.1: Technical Safety Requirements**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Technical safety requirements must be derived from safety goals with verification methods defined |
| Current State | [Document your current state] |
| Gap Description | [What safety requirements are missing] |
| Required State | TSR document covering voltage thresholds, temperature limits, current limits, with verification methods |
| Evidence Location | [Documentation location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Create/update TSR documentation] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap A2.2: PMHF Calculation (ASIL-D)**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Probabilistic Metric for Hardware Failure must be calculated and proven for ASIL-D |
| Current State | [Document your current state] |
| Gap Description | [Describe PMHF analysis status] |
| Required State | PMHF calculation document showing ≤10^-9 failure rate with component analysis |
| Evidence Location | [Analysis document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Conduct PMHF analysis] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap A2.3: Design FMEA**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Failure Mode Effects Analysis must identify all failure modes and mitigation strategies |
| Current State | [Document your current state] |
| Gap Description | [What failure modes or mitigations are missing] |
| Required State | Complete FMEA covering hardware and software failure modes with mitigation strategies |
| Evidence Location | [FMEA document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Complete or update FMEA] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### A3. Implementation Phase Gaps

**Gap A3.1: MISRA C:2012 Compliance**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% mandatory rules, 100% required rules for ASIL-D safety-critical code |
| Current State | [Document your current state] |
| Gap Description | [What MISRA violations exist] |
| Required State | Zero violations of mandatory/required rules in safety-critical code; deviations justified |
| Evidence Location | [Static analysis tool output] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why violations exist] |
| Remediation Plan | [Code corrections and deviation management] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### A4. Testing Phase Gaps

**Gap A4.1: MC/DC Coverage**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% MC/DC coverage for ASIL-D safety-critical functions |
| Current State | [Document your current state] |
| Gap Description | [What MC/DC coverage gaps exist] |
| Required State | 100% MC/DC coverage with evidence from coverage tool for overcharge, overdischarge, thermal, current protection |
| Evidence Location | [Coverage tool report location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why coverage gap exists] |
| Remediation Plan | [Design additional test cases for coverage] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap A4.2: Statement Coverage**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% statement coverage for ASIL-D safety-critical code |
| Current State | [Document your current state] |
| Gap Description | [What statement coverage gaps exist] |
| Required State | 100% statement coverage with evidence from coverage tool |
| Evidence Location | [Coverage tool report location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Design additional test cases] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap A4.3: Branch Coverage**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% branch coverage for ASIL-D functions |
| Current State | [Document your current state] |
| Gap Description | [What branch coverage gaps exist] |
| Required State | 100% branch coverage with evidence from coverage tool |
| Evidence Location | [Coverage tool report location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Design additional test cases] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### A5. Validation Phase Gaps

**Gap A5.1: Safety Case**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Safety case document demonstrating residual risks are acceptable |
| Current State | [Document your current state] |
| Gap Description | [Describe missing safety case elements] |
| Required State | Complete safety case with hazard analysis, safety goals, evidence of achievement, residual risk assessment |
| Evidence Location | [Safety case document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop safety case] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

## Section B: ASPICE Level 2 Work Product Gaps

### B1. Planning and Management Gaps

**Gap B1.1: Project Plan**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Comprehensive project plan with scope, schedule, resources, budget |
| Current State | [Document your current state] |
| Gap Description | [What elements are missing from project plan] |
| Required State | Project plan covering project objectives, scope definition, schedule with milestones, resource allocation, budget, constraints |
| Evidence Location | [Document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Create/update project plan] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B1.2: Risk Management Plan**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Risk management plan with risk identification, assessment, and mitigation strategies |
| Current State | [Document your current state] |
| Gap Description | [What risk management activities are missing] |
| Required State | Risk register with identified risks, probability/impact assessment, mitigation plans, ownership |
| Evidence Location | [Risk document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop risk management process] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B1.3: Change Control Process**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Defined change control procedures with impact assessment and approval |
| Current State | [Document your current state] |
| Gap Description | [What change control procedures are missing] |
| Required State | Documented change control process with change request template, impact analysis, approval workflow, traceability update |
| Evidence Location | [Process documentation location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Define change control procedures] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### B2. Requirements and Design Gaps

**Gap B2.1: Software Requirements Specification**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Complete software requirements specification with functional and non-functional requirements |
| Current State | [Document your current state] |
| Gap Description | [What requirements or requirement details are missing] |
| Required State | SRS document with clear, verifiable, traceable requirements; safety requirements identified; review and approval evidence |
| Evidence Location | [SRS document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop/complete SRS] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B2.2: Requirements Traceability Matrix**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Bidirectional traceability from requirements to design and test cases |
| Current State | [Document your current state] |
| Gap Description | [What traceability links are missing] |
| Required State | RTM showing 100% requirements traced to design, 100% design traced to code, 100% code traced to tests |
| Evidence Location | [Traceability matrix location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Build/update traceability matrix] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B2.3: Software Design Document**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Design documentation with architecture and detailed design specifications |
| Current State | [Document your current state] |
| Gap Description | [What design documentation is missing] |
| Required State | SDD with system architecture, module design, interface specifications, data structure design, with traceability to requirements |
| Evidence Location | [Design document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop/complete design documentation] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### B3. Implementation and Testing Gaps

**Gap B3.1: Code Review Process**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Documented code review process with evidence of reviews completed before integration |
| Current State | [Document your current state] |
| Gap Description | [What code review process or evidence is missing] |
| Required State | Code review procedure, code review checklist, review records for all critical code sections |
| Evidence Location | [Code review records location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Define code review process and conduct reviews] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B3.2: Unit Test Plan and Coverage**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Unit test plan with test cases covering safety-critical code and coverage metrics |
| Current State | [Document your current state] |
| Gap Description | [What unit tests or coverage metrics are missing] |
| Required State | Unit test plan, test cases for all modules, coverage metrics (statement, branch, MC/DC), test execution results |
| Evidence Location | [Test documentation and results location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop unit tests and measure coverage] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B3.3: Integration and System Test Plans**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Integration and system test plans with test cases and results |
| Current State | [Document your current state] |
| Gap Description | [What integration or system tests are missing] |
| Required State | Integration test plan covering module interfaces, system test plan covering functional and safety requirements, test execution results, traceability to requirements |
| Evidence Location | [Test documentation location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop and execute test plans] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

### B4. Quality Assurance Gaps

**Gap B4.1: Quality Assurance Plan**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | QA plan with defined standards, review procedures, audit schedules |
| Current State | [Document your current state] |
| Gap Description | [What QA planning is missing] |
| Required State | QA plan with quality standards, review and audit procedures, schedule, responsibilities |
| Evidence Location | [QA plan document location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Develop QA plan] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap B4.2: Process Audits and Reviews**

| Attribute | Finding |
|-----------|---------|
| ASPICE Requirement | Evidence of audits and reviews showing process compliance |
| Current State | [Document your current state] |
| Gap Description | [What audit or review evidence is missing] |
| Required State | Audit schedule, audit checklists, audit reports, non-conformance tracking and closure |
| Evidence Location | [Audit records location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Conduct audits and document results] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

## Section C: MISRA C:2012 Gaps

### C1. Static Analysis Implementation

**Gap C1.1: Static Analysis Tool Integration**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | Static analysis tool configured for MISRA C:2012 checking |
| Current State | [Document your current state] |
| Gap Description | [What tool integration is missing] |
| Required State | Static analysis tool configured, integrated into build process, reporting MISRA violations |
| Evidence Location | [Tool output/reports location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Implement static analysis tool] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap C1.2: Mandatory Rule Compliance**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% compliance with MISRA mandatory rules |
| Current State | [Document your current state] |
| Gap Description | [What mandatory rule violations exist] |
| Required State | Zero mandatory rule violations, with evidence from static analysis tool |
| Evidence Location | [Static analysis reports location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why violations exist] |
| Remediation Plan | [Correct code violations] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap C1.3: Required Rule Compliance and Deviations**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% required rule compliance or documented deviations for ASIL-D |
| Current State | [Document your current state] |
| Gap Description | [What required rule violations or deviations exist] |
| Required State | Zero required rule violations or all deviations formally documented with safety justification and approval |
| Evidence Location | [Deviation registry location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Correct violations or process deviations] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap C1.4: Advisory Rule Compliance**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 95%+ compliance with advisory rules for ASIL-D |
| Current State | [Document your current state] |
| Gap Description | [What advisory rule violations exist] |
| Required State | 95%+ advisory rule compliance with exceptions documented |
| Evidence Location | [Static analysis reports location] |
| Severity | [Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Address advisory violations] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

## Section D: V-Model Traceability Gaps

### D1. Bidirectional Traceability

**Gap D1.1: Requirement-to-Design Traceability**

| Attribute | Finding |
|-----------|---------|
| V-Model Requirement | 100% of requirements must trace to design components |
| Current State | [Document your current state] |
| Gap Description | [What requirements lack design traceability] |
| Required State | Complete RTM with all requirements traced to design with no orphan requirements |
| Evidence Location | [Traceability matrix location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Complete traceability mapping] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap D1.2: Design-to-Code Traceability**

| Attribute | Finding |
|-----------|---------|
| V-Model Requirement | 100% of design must trace to implementation code |
| Current State | [Document your current state] |
| Gap Description | [What design components lack code traceability] |
| Required State | Complete traceability matrix with all design elements traced to code modules |
| Evidence Location | [Traceability matrix location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Complete design-to-code mapping] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap D1.3: Code-to-Test Traceability**

| Attribute | Finding |
|-----------|---------|
| V-Model Requirement | 100% of safety-critical code must have test cases |
| Current State | [Document your current state] |
| Gap Description | [What code lacks test case traceability] |
| Required State | All safety-critical code modules linked to unit test cases; orphan test cases identified |
| Evidence Location | [Test traceability matrix location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Complete code-to-test mapping] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap D1.4: Requirement-to-Test Traceability**

| Attribute | Finding |
|-----------|---------|
| V-Model Requirement | 100% of requirements must have corresponding test cases |
| Current State | [Document your current state] |
| Gap Description | [What requirements lack test case traceability] |
| Required State | All functional and safety requirements traced to system test cases; no orphan tests |
| Evidence Location | [Test traceability matrix location] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Complete requirement-to-test mapping] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

## Section E: MC/DC Testing Gaps

### E1. MC/DC Coverage Deficiencies

**Gap E1.1: MC/DC Test Case Design**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | MC/DC test cases for all ASIL-D safety-critical functions |
| Current State | [Document your current state] |
| Gap Description | [What MC/DC test cases are missing] |
| Required State | MC/DC test cases for overcharge, overdischarge, thermal, and current protection functions with condition matrices |
| Evidence Location | [Test specification documents] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Design MC/DC test cases] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

**Gap E1.2: MC/DC Coverage Measurement**

| Attribute | Finding |
|-----------|---------|
| Standard Requirement | 100% MC/DC coverage measurement for ASIL-D functions |
| Current State | [Document your current state] |
| Gap Description | [What MC/DC coverage is missing] |
| Required State | 100% MC/DC coverage verified by automated tool for all safety-critical decision points |
| Evidence Location | [Coverage tool reports] |
| Severity | [Critical/High/Medium/Low] |
| Root Cause | [Why gap exists] |
| Remediation Plan | [Implement coverage measurement and additional tests] |
| Target Date | [Completion estimate] |
| Owner | [Responsible person] |
| Status | [Open/In Progress/Closed] |

---

## Summary and Prioritization

### Critical Gaps (Blocking Audit)

| Gap ID | Area | Description | Owner | Target Date |
|--------|------|-------------|-------|-------------|
| [List critical gaps that prevent certification] |
| | | | |

### High Priority Gaps (Before Audit)

| Gap ID | Area | Description | Owner | Target Date |
|--------|------|-------------|-------|-------------|
| [List high priority gaps needing resolution] |
| | | | |

### Medium Priority Gaps (After Audit)

| Gap ID | Area | Description | Owner | Target Date |
|--------|------|-------------|-------|-------------|
| [List medium priority gaps] |
| | | | |

### Low Priority Gaps (Future Improvement)

| Gap ID | Area | Description | Owner | Target Date |
|--------|------|-------------|-------|-------------|
| [List low priority gaps] |
| | | | |

---

## Closure Tracking

**Gap Closure Sign-Off:**

| Gap ID | Resolution | Verified By | Date | Evidence |
|--------|-----------|------------|------|----------|
| [Track gap closures] |
| | | |

---

## Assessment Timeline

**Planned Assessment Phases:**

1. Documentation audit (Date: ____)
2. Traceability analysis (Date: ____)
3. Code assessment (Date: ____)
4. Testing verification (Date: ____)
5. Process review (Date: ____)
6. Gap remediation (Date: ____)
7. Audit readiness review (Date: ____)

---

**End of Compliance Gap Analysis Template**

Use this template to systematically identify, track, and close compliance gaps before external audit.
