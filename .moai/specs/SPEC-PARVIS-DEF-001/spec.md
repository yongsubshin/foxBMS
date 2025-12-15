# SPEC-PARVIS-DEF-001: PARVIS 에이전트 시스템 정의

## TAG BLOCK

```yaml
spec_id: SPEC-PARVIS-DEF-001
title: PARVIS 잔여 12개 에이전트 정의
version: 1.0.0
created: 2025-12-15
updated: 2025-12-15
status: draft
priority: high
type: definition
domain: agent-system
compliance:
  - ISO 26262 Part 6
  - ASPICE 4.0
  - MISRA C:2012
```

---

## 1. Environment (환경)

### 1.1 프로젝트 컨텍스트

- **프로젝트명**: PARVIS (foxBMS V-Model AI Support)
- **목적**: foxBMS 배터리 관리 시스템의 V-Model 개발을 지원하는 AI 에이전트 시스템
- **대상 코드베이스**: foxbms-2 (C 언어 기반 BMS 소프트웨어)
- **준수 표준**: ISO 26262 ASIL-D, MISRA C:2012, Automotive SPICE Level 2+

### 1.2 기존 에이전트 (7개 완료)

| 에이전트명 | 역할 | 상태 |
|-----------|------|------|
| parvis-ai-orchestrator | V-Model 마스터 조정자 | 정의 완료 |
| parvis-aispec-code | 코드 역공학 요구사항 추출 | 정의 완료 |
| parvis-aispec-trace | 추적성 매트릭스 관리 | 정의 완료 |
| parvis-aicoder-misra | MISRA C:2012 검사 | 정의 완료 |
| parvis-aicoder-refactor | MISRA 위반 자동 수정 | 정의 완료 |
| parvis-aiverify-unittest | 단위 테스트 생성 | 정의 완료 |
| parvis-aidoc-aspice | ASPICE 산출물 생성 | 정의 완료 |

### 1.3 정의 대상 에이전트 (12개)

**SPEC 그룹 (3개):**
- parvis-aispec-reqid - 요구사항 ID 할당
- parvis-aispec-transformer - 요구사항 형식 변환
- parvis-aispec-safety - 안전 요구사항 분류

**CODER 그룹 (2개):**
- parvis-aicoder-doxygen - Doxygen 문서 생성
- parvis-aicoder-safety - 안전 중요 코드 패턴

**VERIFY 그룹 (4개):**
- parvis-aiverify-coverage - 테스트 커버리지 분석
- parvis-aiverify-integration - 통합 테스트 생성
- parvis-aiverify-safety - 안전 테스트 검증
- parvis-aiverify-report - 검증 보고서 생성

**DOC 그룹 (3개):**
- parvis-aidoc-safety - 안전 케이스 문서화
- parvis-aidoc-trace - 추적성 문서화
- parvis-aidoc-change - 변경 관리 문서화

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- A1: 모든 에이전트는 Claude Code 환경에서 실행됨
- A2: 에이전트 정의 파일은 `.claude/agents/parvis/` 디렉토리에 위치
- A3: 에이전트 간 통신은 파일 기반 데이터 교환으로 수행
- A4: foxBMS 코드베이스는 `foxbms-2/` 디렉토리에 존재
- A5: MISRA 검사는 Axivion Bauhaus Suite와 연동 가능

### 2.2 프로세스 가정

- A6: V-Model 개발 프로세스를 따름
- A7: ISO 26262 Part 6 요구사항을 준수
- A8: ASPICE Level 2+ 프로세스 성숙도를 목표로 함
- A9: 모든 에이전트는 단일 책임 원칙을 따름

### 2.3 의존성 가정

- A10: 기존 7개 에이전트 정의가 안정적임
- A11: ARCHITECTURE.md와 ROADMAP.md 문서가 최신 상태임
- A12: 표준 가이드 문서가 완성되어 있음

---

## 3. Requirements (요구사항)

### 3.1 SPEC 그룹 에이전트 요구사항

#### REQ-DEF-001: parvis-aispec-reqid 에이전트 정의

**EARS 형식:**
WHEN 요구사항이 추출되면 THE parvis-aispec-reqid 에이전트 SHALL FBMS-[TYPE]-[MODULE]-[SEQ] 형식의 고유 ID를 할당한다.

**상세 요구사항:**
- REQ-DEF-001.1: ID 생성 알고리즘 구현
- REQ-DEF-001.2: ID 레지스트리 관리 기능
- REQ-DEF-001.3: 충돌 감지 및 해결 로직
- REQ-DEF-001.4: ID 유효성 검증 기능
- REQ-DEF-001.5: 모듈 분류 규칙 정의

**입출력:**
- 입력: 요구사항 내용, 모듈 분류
- 출력: 고유 요구사항 ID

#### REQ-DEF-002: parvis-aispec-transformer 에이전트 정의

**EARS 형식:**
WHEN 다양한 소스에서 요구사항이 수집되면 THE parvis-aispec-transformer 에이전트 SHALL 통합 형식으로 정규화한다.

**상세 요구사항:**
- REQ-DEF-002.1: 정규화 파이프라인 구현
- REQ-DEF-002.2: 중복 제거 로직
- REQ-DEF-002.3: 분류 로직 (기능/안전/인터페이스)
- REQ-DEF-002.4: 통합 출력 형식 정의
- REQ-DEF-002.5: 품질 지표 계산

**입출력:**
- 입력: parvis-aispec-code, parvis-aispec-excel, parvis-aispec-pdf의 원시 출력
- 출력: 정규화된 요구사항 JSON

#### REQ-DEF-003: parvis-aispec-safety 에이전트 정의

**EARS 형식:**
WHEN 안전 관련 요구사항이 식별되면 THE parvis-aispec-safety 에이전트 SHALL ISO 26262 HARA를 지원하고 ASIL 분류를 수행한다.

**상세 요구사항:**
- REQ-DEF-003.1: HARA 지원 기능 (위험 분석 및 위험 평가)
- REQ-DEF-003.2: ASIL 분류 (A/B/C/D) 할당 로직
- REQ-DEF-003.3: 안전 목표 도출 기능
- REQ-DEF-003.4: FSR (기능 안전 요구사항) 생성
- REQ-DEF-003.5: 안전 컨셉 문서화

**입출력:**
- 입력: 시스템 요구사항, 위험 정보
- 출력: ASIL 분류, 안전 목표, FSR

### 3.2 CODER 그룹 에이전트 요구사항

#### REQ-DEF-004: parvis-aicoder-doxygen 에이전트 정의

**EARS 형식:**
WHEN 소스 코드 문서화가 필요하면 THE parvis-aicoder-doxygen 에이전트 SHALL foxBMS Doxygen 스타일에 따라 주석을 생성 및 유지한다.

**상세 요구사항:**
- REQ-DEF-004.1: Doxygen 템플릿 생성기
- REQ-DEF-004.2: 요구사항 링크 삽입
- REQ-DEF-004.3: API 문서 생성
- REQ-DEF-004.4: 일관성 검사기
- REQ-DEF-004.5: 커버리지 분석

**입출력:**
- 입력: 소스 파일, 요구사항 링크
- 출력: Doxygen 주석이 추가된 소스 파일

#### REQ-DEF-005: parvis-aicoder-safety 에이전트 정의

**EARS 형식:**
WHEN 안전 중요 코드가 식별되면 THE parvis-aicoder-safety 에이전트 SHALL ASIL 마커와 방어적 프로그래밍 패턴을 추가한다.

**상세 요구사항:**
- REQ-DEF-005.1: 안전 어노테이션 템플릿
- REQ-DEF-005.2: ASIL 마커 삽입
- REQ-DEF-005.3: 방어적 프로그래밍 패턴 생성
- REQ-DEF-005.4: 어서션 생성 (FAS_ASSERT)
- REQ-DEF-005.5: 안전 검증 기능

**입출력:**
- 입력: 소스 파일, 안전 요구사항
- 출력: 안전 어노테이션이 추가된 소스 파일

### 3.3 VERIFY 그룹 에이전트 요구사항

#### REQ-DEF-006: parvis-aiverify-coverage 에이전트 정의

**EARS 형식:**
WHEN 테스트가 실행되면 THE parvis-aiverify-coverage 에이전트 SHALL 커버리지 메트릭(문장, 분기, MC/DC)을 분석한다.

**상세 요구사항:**
- REQ-DEF-006.1: 커버리지 파서 구현
- REQ-DEF-006.2: 갭 분석 알고리즘
- REQ-DEF-006.3: 커버리지 보고서 생성
- REQ-DEF-006.4: MC/DC 추적 (안전용)
- REQ-DEF-006.5: 목표 달성 검증

**입출력:**
- 입력: 테스트 결과, 소스 코드
- 출력: 커버리지 보고서 (문장 >80%, 분기 >80%, MC/DC for ASIL C/D)

#### REQ-DEF-007: parvis-aiverify-integration 에이전트 정의

**EARS 형식:**
WHEN 모듈 통합이 필요하면 THE parvis-aiverify-integration 에이전트 SHALL 통합 테스트를 설계한다.

**상세 요구사항:**
- REQ-DEF-007.1: 통합 테스트 템플릿 생성
- REQ-DEF-007.2: 인터페이스 테스트 설계
- REQ-DEF-007.3: 통합 보고서 생성
- REQ-DEF-007.4: 의존성 분석
- REQ-DEF-007.5: 통합 순서 결정

**입출력:**
- 입력: 아키텍처 설계, 인터페이스 명세
- 출력: 통합 테스트 케이스

#### REQ-DEF-008: parvis-aiverify-safety 에이전트 정의

**EARS 형식:**
WHEN 안전 테스트가 필요하면 THE parvis-aiverify-safety 에이전트 SHALL 안전 테스트 완전성을 검증한다.

**상세 요구사항:**
- REQ-DEF-008.1: 안전 테스트 검증 기능
- REQ-DEF-008.2: MC/DC 검증
- REQ-DEF-008.3: 안전 증거 수집기
- REQ-DEF-008.4: FMEA 검증 지원
- REQ-DEF-008.5: 안전 보고서 생성

**입출력:**
- 입력: 안전 요구사항, 테스트 결과
- 출력: 안전 검증 보고서

#### REQ-DEF-009: parvis-aiverify-report 에이전트 정의

**EARS 형식:**
WHEN 검증이 완료되면 THE parvis-aiverify-report 에이전트 SHALL 포괄적인 테스트 보고서를 생성한다.

**상세 요구사항:**
- REQ-DEF-009.1: 보고서 템플릿 생성
- REQ-DEF-009.2: 결과 집계 기능
- REQ-DEF-009.3: ASPICE 형식 출력
- REQ-DEF-009.4: 대시보드 생성
- REQ-DEF-009.5: 추세 분석

**입출력:**
- 입력: 모든 테스트 결과, 커버리지 데이터
- 출력: ASPICE 준수 테스트 보고서

### 3.4 DOC 그룹 에이전트 요구사항

#### REQ-DEF-010: parvis-aidoc-safety 에이전트 정의

**EARS 형식:**
WHEN 안전 케이스 문서화가 필요하면 THE parvis-aidoc-safety 에이전트 SHALL 안전 케이스 및 안전 매뉴얼을 생성한다.

**상세 요구사항:**
- REQ-DEF-010.1: 안전 케이스 템플릿
- REQ-DEF-010.2: 안전 증거 수집 기능
- REQ-DEF-010.3: 안전 보고서 생성
- REQ-DEF-010.4: 안전 매뉴얼 생성
- REQ-DEF-010.5: ISO 26262-2 준수

**입출력:**
- 입력: 안전 분석, 검증 결과
- 출력: 안전 케이스, 안전 매뉴얼, 안전 보고서

#### REQ-DEF-011: parvis-aidoc-trace 에이전트 정의

**EARS 형식:**
WHEN 추적성 보고가 필요하면 THE parvis-aidoc-trace 에이전트 SHALL 추적성 보고서 및 갭 분석을 생성한다.

**상세 요구사항:**
- REQ-DEF-011.1: 추적성 보고서 템플릿
- REQ-DEF-011.2: 커버리지 매트릭스 생성
- REQ-DEF-011.3: 갭 분석 보고서
- REQ-DEF-011.4: 양방향 추적성 시각화
- REQ-DEF-011.5: ISO 26262-8 준수

**입출력:**
- 입력: 추적성 매트릭스
- 출력: 추적성 보고서, 갭 분석

#### REQ-DEF-012: parvis-aidoc-change 에이전트 정의

**EARS 형식:**
WHEN 변경이 제안되면 THE parvis-aidoc-change 에이전트 SHALL 변경 영향 분석을 수행한다.

**상세 요구사항:**
- REQ-DEF-012.1: 영향 분석 알고리즘
- REQ-DEF-012.2: 변경 알림 기능
- REQ-DEF-012.3: 승인 워크플로우
- REQ-DEF-012.4: 변경 이력 관리
- REQ-DEF-012.5: ISO 26262-8 준수

**입출력:**
- 입력: 제안된 변경, 추적성 매트릭스
- 출력: 영향 분석 보고서, 승인 요청

---

## 4. Specifications (명세)

### 4.1 에이전트 정의 파일 형식

모든 에이전트 정의 파일은 다음 구조를 따른다:

```yaml
---
name: parvis-[group]-[function]
description: [1-2줄 설명]
tools: [사용 가능 도구 목록]
model: inherit
permissionMode: default
skills: [필요 스킬 목록]
---

# Agent Orchestration Metadata (v1.0)
# [메타데이터 섹션]

---

# 에이전트명 - 역할 설명

## Primary Mission
## Core Capabilities
## Scope Boundaries
## Workflow Commands
## Integration Points
## Error Handling
## Works Well With
```

### 4.2 에이전트 간 의존성

```
parvis-ai-orchestrator
    |
    +-- SPEC 그룹
    |       +-- parvis-aispec-code (완료)
    |       +-- parvis-aispec-reqid (신규) <- parvis-aispec-code
    |       +-- parvis-aispec-transformer (신규) <- parvis-aispec-code, reqid
    |       +-- parvis-aispec-trace (완료) <- parvis-aispec-transformer
    |       +-- parvis-aispec-safety (신규) <- parvis-aispec-transformer
    |
    +-- CODER 그룹
    |       +-- parvis-aicoder-misra (완료)
    |       +-- parvis-aicoder-refactor (완료) <- parvis-aicoder-misra
    |       +-- parvis-aicoder-doxygen (신규)
    |       +-- parvis-aicoder-safety (신규) <- parvis-aispec-safety
    |
    +-- VERIFY 그룹
    |       +-- parvis-aiverify-unittest (완료)
    |       +-- parvis-aiverify-coverage (신규) <- parvis-aiverify-unittest
    |       +-- parvis-aiverify-integration (신규)
    |       +-- parvis-aiverify-safety (신규) <- parvis-aispec-safety
    |       +-- parvis-aiverify-report (신규) <- 모든 verify 에이전트
    |
    +-- DOC 그룹
            +-- parvis-aidoc-aspice (완료)
            +-- parvis-aidoc-safety (신규) <- parvis-aiverify-safety
            +-- parvis-aidoc-trace (신규) <- parvis-aispec-trace
            +-- parvis-aidoc-change (신규) <- parvis-aispec-trace
```

### 4.3 파일 위치

- 에이전트 정의: `/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis/`
- 데이터 저장: `.moai/bms/`
- 요구사항: `.moai/bms/requirements/`
- 추적성: `.moai/bms/traceability/`
- 테스트: `.moai/bms/tests/`
- 문서: `.moai/bms/documentation/`

### 4.4 품질 기준

**에이전트 정의 품질 기준:**
- 명확한 Primary Mission 정의
- 범위 경계 (IN SCOPE / OUT OF SCOPE) 명시
- 워크플로우 명령어 정의
- 통합 포인트 명시
- 에러 처리 전략
- 협업 에이전트 명시

---

## 5. Constraints (제약사항)

### 5.1 기술적 제약

- C1: 에이전트 정의 파일은 Markdown 형식
- C2: 에이전트명은 parvis-[group]-[function] 형식
- C3: 도구 접근은 최소 권한 원칙 적용
- C4: 파일 기반 데이터 교환 (JSON 형식)

### 5.2 프로세스 제약

- C5: ISO 26262 Part 6 요구사항 준수
- C6: ASPICE SWE 프로세스 산출물 준수
- C7: MISRA C:2012 규칙 참조
- C8: foxBMS 코딩 스타일 준수

### 5.3 구현 제약

- C9: 기존 에이전트와의 일관성 유지
- C10: 단일 책임 원칙 준수
- C11: 명확한 입출력 정의

---

## 6. Traceability (추적성)

### 6.1 상위 문서 연결

| 요구사항 ID | ARCHITECTURE.md 참조 | ROADMAP.md 참조 |
|------------|---------------------|-----------------|
| REQ-DEF-001 | Agent Hierarchy | Phase 2: Step 2.2 |
| REQ-DEF-002 | Agent Hierarchy | Phase 2: Step 2.4 |
| REQ-DEF-003 | Phase 5: Step 5.1 | Phase 5: Step 5.1 |
| REQ-DEF-004 | Phase 3: Step 3.3 | Phase 3: Step 3.3 |
| REQ-DEF-005 | Phase 5: Step 5.2 | Phase 5: Step 5.2 |
| REQ-DEF-006 | Phase 4: Step 4.2 | Phase 4: Step 4.2 |
| REQ-DEF-007 | Phase 4: Step 4.3 | Phase 4: Step 4.3 |
| REQ-DEF-008 | Phase 5: Step 5.3 | Phase 5: Step 5.3 |
| REQ-DEF-009 | Phase 4: Step 4.5 | Phase 4: Step 4.5 |
| REQ-DEF-010 | Phase 5: Step 5.2 | Phase 5: Step 5.2 |
| REQ-DEF-011 | Phase 5: Step 5.3 | Phase 5: Step 5.3 |
| REQ-DEF-012 | Phase 5: Step 5.4 | Phase 5: Step 5.4 |

### 6.2 표준 문서 연결

| 요구사항 ID | ISO 26262 | ASPICE | MISRA |
|------------|-----------|--------|-------|
| REQ-DEF-001 | Part 8 | SWE.1 | - |
| REQ-DEF-002 | Part 6 | SWE.1 | - |
| REQ-DEF-003 | Part 3, 4 | SWE.1 | - |
| REQ-DEF-004 | Part 6 | SWE.3 | - |
| REQ-DEF-005 | Part 6 | SWE.3 | C:2012 |
| REQ-DEF-006 | Part 6 Table 9 | SWE.4 | - |
| REQ-DEF-007 | Part 6 | SWE.5, SWE.6 | - |
| REQ-DEF-008 | Part 4, 6 | SWE.4 | - |
| REQ-DEF-009 | Part 6 | SWE.4, 5, 6 | - |
| REQ-DEF-010 | Part 2 | - | - |
| REQ-DEF-011 | Part 8 | SUP.8 | - |
| REQ-DEF-012 | Part 8 | SUP.8 | - |

---

## 7. Version History

| 버전 | 날짜 | 작성자 | 변경 내용 |
|-----|------|-------|----------|
| 1.0.0 | 2025-12-15 | PARVIS | 초기 버전 |
