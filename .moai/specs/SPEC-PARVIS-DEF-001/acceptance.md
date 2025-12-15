# SPEC-PARVIS-DEF-001 인수 기준

## TAG BLOCK

```yaml
acceptance_id: ACC-PARVIS-DEF-001
spec_ref: SPEC-PARVIS-DEF-001
version: 1.0.0
created: 2025-12-15
```

---

## 1. 인수 기준 개요

### 1.1 목적

12개 PARVIS 에이전트 정의가 품질 기준을 충족하는지 검증한다.

### 1.2 범위

- 에이전트 정의 파일 구조 검증
- 내용 완성도 검증
- 일관성 검증
- 통합성 검증

---

## 2. 인수 테스트 시나리오

### 2.1 SPEC 그룹 에이전트 검증

#### AC-DEF-001: parvis-aispec-reqid 정의 검증

**Given:** parvis-aispec-reqid.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- YAML 프론트매터에 name, description, tools, model, permissionMode, skills가 포함됨
- Agent Orchestration Metadata가 완성됨
- Primary Mission에 ID 할당 목적이 명시됨
- Core Capabilities에 ID 생성, 레지스트리 관리, 충돌 감지가 포함됨
- IN SCOPE에 ID 할당 업무가 명시됨
- OUT OF SCOPE에 요구사항 추출이 명시됨
- Workflow Commands에 "Assign ID" 명령이 정의됨
- Integration Points에 parvis-aispec-code, parvis-aispec-transformer가 명시됨

#### AC-DEF-002: parvis-aispec-transformer 정의 검증

**Given:** parvis-aispec-transformer.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 정규화 파이프라인이 Core Capabilities에 포함됨
- 중복 제거 로직이 정의됨
- 분류 로직 (기능/안전/인터페이스)이 명시됨
- 입력으로 원시 요구사항을 받음
- 출력으로 정규화된 JSON을 생성함

#### AC-DEF-003: parvis-aispec-safety 정의 검증

**Given:** parvis-aispec-safety.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- HARA 지원 기능이 정의됨
- ASIL 분류 (A/B/C/D) 로직이 포함됨
- 안전 목표 도출 기능이 명시됨
- ISO 26262 Part 3, 4 참조가 compliance에 포함됨

### 2.2 CODER 그룹 에이전트 검증

#### AC-DEF-004: parvis-aicoder-doxygen 정의 검증

**Given:** parvis-aicoder-doxygen.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- Doxygen 템플릿 생성 기능이 정의됨
- foxBMS Doxygen 스타일 참조가 포함됨
- 요구사항 링크 삽입 기능이 명시됨
- API 문서 생성 기능이 포함됨

#### AC-DEF-005: parvis-aicoder-safety 정의 검증

**Given:** parvis-aicoder-safety.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 안전 어노테이션 템플릿이 정의됨
- ASIL 마커 삽입 기능이 포함됨
- FAS_ASSERT 생성 기능이 명시됨
- 방어적 프로그래밍 패턴이 포함됨

### 2.3 VERIFY 그룹 에이전트 검증

#### AC-DEF-006: parvis-aiverify-coverage 정의 검증

**Given:** parvis-aiverify-coverage.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 문장 커버리지 분석 기능이 정의됨
- 분기 커버리지 분석 기능이 포함됨
- MC/DC 커버리지 (ASIL C/D용) 기능이 명시됨
- 커버리지 목표 (>80%)가 참조됨
- ISO 26262-6 Table 9 참조가 포함됨

#### AC-DEF-007: parvis-aiverify-integration 정의 검증

**Given:** parvis-aiverify-integration.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 통합 테스트 설계 기능이 정의됨
- 인터페이스 테스트 설계 기능이 포함됨
- 의존성 분석 기능이 명시됨
- ASPICE SWE.5, SWE.6 참조가 포함됨

#### AC-DEF-008: parvis-aiverify-safety 정의 검증

**Given:** parvis-aiverify-safety.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 안전 테스트 검증 기능이 정의됨
- MC/DC 검증 기능이 포함됨
- FMEA 검증 지원이 명시됨
- ISO 26262 Part 4, 6 참조가 포함됨

#### AC-DEF-009: parvis-aiverify-report 정의 검증

**Given:** parvis-aiverify-report.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 보고서 템플릿 기능이 정의됨
- 결과 집계 기능이 포함됨
- ASPICE 형식 출력이 명시됨
- 대시보드 생성 기능이 포함됨

### 2.4 DOC 그룹 에이전트 검증

#### AC-DEF-010: parvis-aidoc-safety 정의 검증

**Given:** parvis-aidoc-safety.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 안전 케이스 템플릿이 정의됨
- 안전 증거 수집 기능이 포함됨
- 안전 매뉴얼 생성 기능이 명시됨
- ISO 26262-2 참조가 포함됨

#### AC-DEF-011: parvis-aidoc-trace 정의 검증

**Given:** parvis-aidoc-trace.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 추적성 보고서 템플릿이 정의됨
- 커버리지 매트릭스 생성 기능이 포함됨
- 갭 분석 보고서 기능이 명시됨
- ISO 26262-8 참조가 포함됨

#### AC-DEF-012: parvis-aidoc-change 정의 검증

**Given:** parvis-aidoc-change.md 파일이 생성됨
**When:** 에이전트 정의 내용을 검토함
**Then:**
- 영향 분석 알고리즘이 정의됨
- 변경 알림 기능이 포함됨
- 승인 워크플로우가 명시됨
- ISO 26262-8 참조가 포함됨

---

## 3. 통합 검증 기준

### 3.1 일관성 검증

#### AC-INT-001: 명명 규칙 일관성

**Given:** 모든 12개 에이전트 정의 파일이 생성됨
**When:** 파일명과 에이전트명을 검토함
**Then:**
- 모든 파일명이 parvis-[group]-[function].md 형식을 따름
- YAML name 필드가 파일명과 일치함

#### AC-INT-002: 구조 일관성

**Given:** 모든 12개 에이전트 정의 파일이 생성됨
**When:** 파일 구조를 검토함
**Then:**
- 모든 파일이 동일한 섹션 구조를 가짐
- 모든 파일에 Primary Mission, Core Capabilities, Scope Boundaries가 포함됨

### 3.2 의존성 검증

#### AC-INT-003: 의존성 그래프 완성성

**Given:** 모든 에이전트 정의가 완료됨
**When:** Integration Points를 분석함
**Then:**
- 모든 에이전트가 의존성 그래프에 포함됨
- 순환 의존성이 없음
- 각 에이전트의 upstream/downstream이 명시됨

#### AC-INT-004: 도구 권한 일관성

**Given:** 모든 에이전트 정의가 완료됨
**When:** tools 필드를 분석함
**Then:**
- 읽기 전용 에이전트는 Read, Grep, Glob만 포함
- 쓰기 에이전트는 Write, Edit 포함
- Bash 사용은 필요한 경우에만 포함

---

## 4. 품질 게이트 체크리스트

### 4.1 개별 에이전트 체크리스트

각 에이전트 정의에 대해:

- [ ] YAML 프론트매터 완성
- [ ] Agent Orchestration Metadata 완성
- [ ] Primary Mission 정의 (2-3문장)
- [ ] Core Capabilities 정의 (3개 이상)
- [ ] IN SCOPE 항목 (5개 이상)
- [ ] OUT OF SCOPE 항목 (3개 이상)
- [ ] Workflow Commands 정의 (2개 이상)
- [ ] Integration Points 정의
- [ ] Error Handling 정의
- [ ] Works Well With 정의

### 4.2 전체 시스템 체크리스트

- [ ] 12개 에이전트 파일 모두 생성됨
- [ ] 명명 규칙 100% 준수
- [ ] 구조 일관성 100%
- [ ] 의존성 그래프 완성
- [ ] 순환 의존성 없음
- [ ] ARCHITECTURE.md 업데이트
- [ ] ROADMAP.md 업데이트

---

## 5. 검증 방법

### 5.1 자동 검증

- 파일 존재 여부 확인 (Glob)
- YAML 프론트매터 파싱 검증
- 필수 섹션 존재 여부 확인 (Grep)

### 5.2 수동 검증

- 내용 품질 검토
- 기술적 정확성 검토
- 표준 준수 여부 검토

---

## 6. Definition of Done

SPEC-PARVIS-DEF-001은 다음 조건이 모두 충족될 때 완료된다:

1. **파일 생성 완료**: 12개 에이전트 정의 파일이 모두 .claude/agents/parvis/ 디렉토리에 존재
2. **품질 기준 충족**: 모든 개별 에이전트 체크리스트 항목이 통과
3. **일관성 검증 통과**: 명명 규칙, 구조 일관성 검증 통과
4. **통합 검증 통과**: 의존성 그래프 완성, 순환 의존성 없음
5. **문서 업데이트**: ARCHITECTURE.md, ROADMAP.md 업데이트 완료

---

## 7. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-15 | 초기 버전 |
