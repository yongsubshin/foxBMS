# SPEC-PARVIS-DEF-001 구현 계획

## TAG BLOCK

```yaml
plan_id: PLAN-PARVIS-DEF-001
spec_ref: SPEC-PARVIS-DEF-001
version: 1.0.0
created: 2025-12-15
priority: high
```

---

## 1. 구현 개요

### 1.1 목표

12개의 PARVIS 에이전트 정의 파일을 생성하여 V-Model 개발 지원 에이전트 시스템을 완성한다.

### 1.2 범위

- SPEC 그룹 3개 에이전트 정의
- CODER 그룹 2개 에이전트 정의
- VERIFY 그룹 4개 에이전트 정의
- DOC 그룹 3개 에이전트 정의

---

## 2. 마일스톤

### 마일스톤 1: SPEC 그룹 에이전트 정의 (우선순위: 최고)

**목표:**
- parvis-aispec-reqid 정의
- parvis-aispec-transformer 정의
- parvis-aispec-safety 정의

**근거:**
- 요구사항 관리가 V-Model의 기초
- 다른 모든 에이전트의 입력 제공
- Phase 2 핵심 구성요소

**산출물:**
- parvis-aispec-reqid.md
- parvis-aispec-transformer.md
- parvis-aispec-safety.md

### 마일스톤 2: CODER 그룹 에이전트 정의 (우선순위: 높음)

**목표:**
- parvis-aicoder-doxygen 정의
- parvis-aicoder-safety 정의

**근거:**
- 코드 품질 보장 필수
- MISRA 에이전트와 연계 필요
- 안전 어노테이션 표준화

**산출물:**
- parvis-aicoder-doxygen.md
- parvis-aicoder-safety.md

### 마일스톤 3: VERIFY 그룹 에이전트 정의 (우선순위: 높음)

**목표:**
- parvis-aiverify-coverage 정의
- parvis-aiverify-integration 정의
- parvis-aiverify-safety 정의
- parvis-aiverify-report 정의

**근거:**
- V-Model 우측 검증 단계 완성
- ISO 26262 검증 요구사항 충족
- 테스트 커버리지 목표 달성

**산출물:**
- parvis-aiverify-coverage.md
- parvis-aiverify-integration.md
- parvis-aiverify-safety.md
- parvis-aiverify-report.md

### 마일스톤 4: DOC 그룹 에이전트 정의 (우선순위: 중간)

**목표:**
- parvis-aidoc-safety 정의
- parvis-aidoc-trace 정의
- parvis-aidoc-change 정의

**근거:**
- ASPICE 산출물 완성
- 안전 케이스 문서화
- 변경 관리 지원

**산출물:**
- parvis-aidoc-safety.md
- parvis-aidoc-trace.md
- parvis-aidoc-change.md

---

## 3. 기술적 접근

### 3.1 에이전트 정의 템플릿

기존 완료된 에이전트 정의 파일의 구조를 따른다:

```markdown
---
name: parvis-[group]-[function]
description: [설명]
tools: [도구 목록]
model: inherit
permissionMode: default
skills: [스킬 목록]
---

# Agent Orchestration Metadata (v1.0)
# [메타데이터]

---

# [에이전트명] - [역할]

## Primary Mission
## Core Capabilities
## Scope Boundaries
## [도메인별 섹션]
## Workflow Commands
## Integration Points
## Error Handling
## Works Well With
```

### 3.2 도구 할당 원칙

| 에이전트 유형 | 권장 도구 |
|-------------|----------|
| SPEC 에이전트 | Read, Write, Edit, Grep, Glob |
| CODER 에이전트 | Read, Write, Edit, Grep, Glob, Bash |
| VERIFY 에이전트 | Read, Write, Edit, Grep, Glob, Bash |
| DOC 에이전트 | Read, Write, Edit, Grep, Glob |

### 3.3 스킬 할당 원칙

- 기본 스킬: moai-foundation-claude
- 언어 관련: moai-lang-unified
- 프로젝트 관련: moai-workflow-project

---

## 4. 의존성 분석

### 4.1 에이전트 간 의존성

```
[선행 에이전트] -> [후행 에이전트]

parvis-aispec-code -> parvis-aispec-reqid
parvis-aispec-code -> parvis-aispec-transformer
parvis-aispec-reqid -> parvis-aispec-transformer
parvis-aispec-transformer -> parvis-aispec-trace
parvis-aispec-transformer -> parvis-aispec-safety

parvis-aicoder-misra -> parvis-aicoder-refactor (완료)
parvis-aispec-safety -> parvis-aicoder-safety

parvis-aiverify-unittest -> parvis-aiverify-coverage
parvis-aispec-safety -> parvis-aiverify-safety
parvis-aiverify-* -> parvis-aiverify-report

parvis-aiverify-safety -> parvis-aidoc-safety
parvis-aispec-trace -> parvis-aidoc-trace
parvis-aispec-trace -> parvis-aidoc-change
```

### 4.2 구현 순서 권장

1. parvis-aispec-reqid (의존성 없음)
2. parvis-aispec-transformer (reqid 이후)
3. parvis-aispec-safety (transformer 이후)
4. parvis-aicoder-doxygen (의존성 없음)
5. parvis-aicoder-safety (safety 요구사항 이후)
6. parvis-aiverify-coverage (unittest 이후)
7. parvis-aiverify-integration (의존성 없음)
8. parvis-aiverify-safety (safety 요구사항 이후)
9. parvis-aiverify-report (모든 verify 이후)
10. parvis-aidoc-safety (verify-safety 이후)
11. parvis-aidoc-trace (trace 이후)
12. parvis-aidoc-change (trace 이후)

---

## 5. 위험 분석 및 대응

### 5.1 기술적 위험

| 위험 | 확률 | 영향 | 대응 전략 |
|-----|-----|-----|----------|
| 에이전트 간 인터페이스 불일치 | 중간 | 높음 | 기존 에이전트 패턴 준수 |
| 표준 요구사항 누락 | 낮음 | 높음 | 표준 가이드 문서 참조 |
| 도구 권한 부족 | 낮음 | 중간 | 최소 권한 원칙 적용 |

### 5.2 프로세스 위험

| 위험 | 확률 | 영향 | 대응 전략 |
|-----|-----|-----|----------|
| 정의 일관성 부족 | 중간 | 중간 | 템플릿 엄격 준수 |
| 의존성 순서 오류 | 낮음 | 중간 | 의존성 그래프 검증 |

---

## 6. 품질 게이트

### 6.1 에이전트 정의 품질 기준

각 에이전트 정의는 다음을 충족해야 한다:

- [ ] YAML 프론트매터 완성
- [ ] Agent Orchestration Metadata 포함
- [ ] Primary Mission 명확히 정의
- [ ] Core Capabilities 3개 이상
- [ ] IN SCOPE / OUT OF SCOPE 명시
- [ ] Workflow Commands 정의
- [ ] Integration Points 명시
- [ ] Error Handling 전략
- [ ] Works Well With 정의

### 6.2 통합 품질 기준

- [ ] 모든 에이전트가 의존성 그래프에 포함
- [ ] 순환 의존성 없음
- [ ] 명명 규칙 준수
- [ ] 파일 위치 규칙 준수

---

## 7. 산출물 목록

### 7.1 에이전트 정의 파일

| 파일명 | 위치 | 우선순위 |
|-------|------|---------|
| parvis-aispec-reqid.md | .claude/agents/parvis/ | 최고 |
| parvis-aispec-transformer.md | .claude/agents/parvis/ | 최고 |
| parvis-aispec-safety.md | .claude/agents/parvis/ | 최고 |
| parvis-aicoder-doxygen.md | .claude/agents/parvis/ | 높음 |
| parvis-aicoder-safety.md | .claude/agents/parvis/ | 높음 |
| parvis-aiverify-coverage.md | .claude/agents/parvis/ | 높음 |
| parvis-aiverify-integration.md | .claude/agents/parvis/ | 높음 |
| parvis-aiverify-safety.md | .claude/agents/parvis/ | 높음 |
| parvis-aiverify-report.md | .claude/agents/parvis/ | 높음 |
| parvis-aidoc-safety.md | .claude/agents/parvis/ | 중간 |
| parvis-aidoc-trace.md | .claude/agents/parvis/ | 중간 |
| parvis-aidoc-change.md | .claude/agents/parvis/ | 중간 |

### 7.2 관련 문서 업데이트

| 파일명 | 업데이트 내용 |
|-------|-------------|
| ARCHITECTURE.md | 에이전트 상태 업데이트 |
| ROADMAP.md | 완료 상태 표시 |

---

## 8. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-15 | 초기 버전 |
