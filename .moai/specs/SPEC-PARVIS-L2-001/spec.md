# SPEC-PARVIS-L2-001: PARVIS L2 Phase - Requirement Normalization and ID Assignment

## TAG BLOCK

```yaml
spec_id: SPEC-PARVIS-L2-001
title: PARVIS L2 Phase - Requirement Normalization and ID Assignment
version: 1.0.0
created: 2025-12-16
updated: 2025-12-16
completed: 2025-12-16
status: completed
priority: high
type: implementation
domain: agent-system
v_model_phase: L2
compliance:
  - ISO 26262-6 Part 6
  - ISO 26262-8 Part 8
  - ASPICE 4.0 SWE.1
depends_on:
  - SPEC-PARVIS-DEF-001
  - SPEC-PARVIS-IMPL-001
```

---

## 1. Environment (환경)

### 1.1 개요

본 SPEC은 PARVIS V-Model L2 단계 구현을 정의합니다. L2 단계는 L1 단계에서 추출된 395개 요구사항에 대해 정규화(Normalization) 및 고유 ID 할당을 수행합니다.

### 1.2 선행 조건

**Phase 1 (L1) 완료 현황:**

| 항목 | 수치 | 상태 |
|-----|------|------|
| 총 추출 요구사항 | 395개 | COMPLETED |
| High Confidence 비율 | 70.1% (277개) | PASSED |
| Medium Confidence | 29.9% (118개) | - |
| 분석 대상 모듈 | 12개 | COMPLETED |

**추출 유형별 분포:**

| 추출 유형 | 개수 | 비율 |
|----------|------|------|
| Doxygen | 155 | 39.2% |
| Assertion | 161 | 40.8% |
| State Machine | 19 | 4.8% |
| Config | 60 | 15.2% |

### 1.3 구현 대상 에이전트

| 에이전트 | 역할 | 정의 상태 |
|---------|------|----------|
| parvis-aispec-reqid | 요구사항 ID 할당 및 레지스트리 관리 | 정의 완료 |
| parvis-aispec-transformer | 요구사항 정규화 및 통합 | 정의 완료 |

### 1.4 데이터 위치

**입력 데이터:**
- `.moai/bms/requirements/extracted/*.json` - 추출된 요구사항 (395개)

**출력 데이터:**
- `.moai/bms/requirements/normalized/*.json` - 정규화된 요구사항
- `.moai/bms/requirements/registry/id-registry.json` - ID 레지스트리
- `.moai/bms/requirements/registry/module-map.json` - 모듈 매핑

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- A1: L1 단계에서 추출된 395개 요구사항 데이터가 유효하고 접근 가능함
- A2: 추출된 요구사항에 `suggested_type`, `suggested_module` 필드가 포함되어 있음
- A3: 각 요구사항에 `source_file`, `source_line` 정보가 포함되어 있음
- A4: JSON 파일 형식이 정의된 스키마를 따름

### 2.2 비즈니스 가정

- A5: 요구사항 ID 형식은 FBMS-[TYPE]-[MODULE]-[SEQ] 표준을 따름
- A6: 모듈 코드는 ARCHITECTURE.md에 정의된 코드 체계를 사용함
- A7: 중복 요구사항은 병합되며 원본 소스 정보가 보존됨
- A8: 품질 점수 50점 이상인 요구사항만 정규화 파이프라인 통과

### 2.3 의존성 가정

- A9: parvis-aispec-code 에이전트 실행이 완료됨
- A10: 추출 결과가 extraction_summary.json에 기록됨
- A11: 에이전트 정의 파일이 .claude/agents/parvis/ 디렉토리에 존재함

---

## 3. Requirements (요구사항)

### 3.1 parvis-aispec-reqid 구현 요구사항

#### REQ-L2-001: ID 생성 알고리즘 구현

**EARS 형식:**
THE parvis-aispec-reqid agent SHALL generate unique requirement IDs following the FBMS-[TYPE]-[MODULE]-[SEQ] format for each extracted requirement.

**상세 요구사항:**

- REQ-L2-001.1: TYPE 코드 매핑 구현
  - SWE: Software Engineering Requirement
  - FSR: Functional Safety Requirement
  - HSI: Hardware-Software Interface Requirement
  - TST: Test Requirement
  - CFG: Configuration Requirement

- REQ-L2-001.2: MODULE 코드 매핑 구현
  - Application Layer: SOA, BAL, ALG(ALGO), PLS(PLAUS), RED(REDUND)
  - Engine Layer: DBS(DB), DIA(DIAG), SYS, MON(SYSMON)
  - Driver Layer: CON(CONT), CAN, IMD

- REQ-L2-001.3: SEQ 시퀀스 관리
  - 3자리 숫자 (001-999)
  - TYPE+MODULE 조합별 독립 시퀀스
  - 자동 증가 및 갭 추적

**매핑 테이블:**

| 추출 모듈 코드 | ID 모듈 코드 | 전체 이름 |
|--------------|-------------|----------|
| SOA | SOA | Safe Operating Area |
| BAL | BAL | Cell Balancing |
| ALGO | ALG | Algorithm Manager |
| PLAUS | PLS | Plausibility Checks |
| REDUND | RED | Redundancy |
| DB | DBS | Database |
| DIAG | DIA | Diagnostics |
| SYS | SYS | System Control |
| SYSMON | MON | System Monitor |
| CONT | CON | Contactor |
| CAN | CAN | CAN Communication |
| IMD | IMD | Insulation Monitoring |

#### REQ-L2-002: ID 레지스트리 관리 구현

**EARS 형식:**
THE parvis-aispec-reqid agent SHALL maintain a master ID registry that tracks all assigned, reserved, and deprecated IDs with full audit trail.

**상세 요구사항:**

- REQ-L2-002.1: 레지스트리 JSON 스키마 구현
  ```
  Registry Entry:
  - id: string (FBMS-XXX-XXX-NNN)
  - status: enum (assigned, reserved, deprecated, deleted)
  - created_date: ISO 8601 timestamp
  - modified_date: ISO 8601 timestamp
  - assigned_to: requirement file reference
  - source_file: original source location
  - parent_id: optional parent ID for hierarchical requirements
  - children: array of child IDs
  ```

- REQ-L2-002.2: 레지스트리 영속화
  - 저장 위치: `.moai/bms/requirements/registry/id-registry.json`
  - 백업 위치: `.moai/bms/requirements/registry/id-registry.backup.json`
  - 수정 시 자동 백업

- REQ-L2-002.3: 시퀀스 추적 구조
  - MODULE+TYPE별 next_sequence 관리
  - allocated_sequences 배열 유지
  - reserved_sequences 배열 유지

#### REQ-L2-003: 충돌 감지 및 방지 구현

**EARS 형식:**
THE parvis-aispec-reqid agent SHALL detect and prevent ID collisions by checking the registry before any ID assignment.

**상세 요구사항:**

- REQ-L2-003.1: 할당 전 중복 검사
- REQ-L2-003.2: 시퀀스 갭 탐지 및 보고
- REQ-L2-003.3: 형식 위반 거부
- REQ-L2-003.4: 충돌 시 해결 방안 제시 (기존 ID 사용 또는 하위 ID 생성)

#### REQ-L2-004: ID 유효성 검증 구현

**EARS 형식:**
THE parvis-aispec-reqid agent SHALL validate all existing IDs against format rules and registry consistency.

**상세 요구사항:**

- REQ-L2-004.1: 형식 규칙 검증 (FBMS-[TYPE]-[MODULE]-[SEQ])
- REQ-L2-004.2: 레지스트리 존재 확인
- REQ-L2-004.3: ID-요구사항 매핑 일관성 확인
- REQ-L2-004.4: 검증 보고서 생성

### 3.2 parvis-aispec-transformer 구현 요구사항

#### REQ-L2-005: 정규화 파이프라인 구현

**EARS 형식:**
THE parvis-aispec-transformer agent SHALL normalize requirements from 4 extraction types (doxygen, assertion, state_machine, config) into a unified JSON format.

**상세 요구사항:**

- REQ-L2-005.1: 입력 형식 파싱 및 검증
  - parvis-aispec-code 출력 형식 처리
  - 필수 필드 존재 확인

- REQ-L2-005.2: 내용 표준화
  - 공백 정규화 (앞뒤 제거, 내부 단일 공백)
  - 문장 부호 표준화 (마침표로 종료)
  - 기술 용어 보존

- REQ-L2-005.3: 용어 정규화
  - "must" 유지 (필수 요구사항)
  - "shall" 유지 (필수 요구사항)
  - "should" -> "shall" + priority:medium 태그
  - "may" -> "can" + classification:optional 태그

- REQ-L2-005.4: 속성 매핑
  - extraction_type:doxygen -> source_category:documentation
  - extraction_type:assertion -> classification:safety
  - extraction_type:state_machine -> tags:["state-machine", "behavior"]
  - extraction_type:config -> type:CFG

#### REQ-L2-006: 중복 제거 엔진 구현

**EARS 형식:**
THE parvis-aispec-transformer agent SHALL detect and merge semantically similar requirements while maintaining source provenance.

**상세 요구사항:**

- REQ-L2-006.1: Phase 1 - 정확 일치 탐지
  - 내용 정규화 (소문자, 구두점 제거)
  - 해시값 생성 및 그룹화
  - 정확 중복 마킹

- REQ-L2-006.2: Phase 2 - 의미적 유사도
  - 핵심 용어 추출
  - Jaccard 유사도 계산
  - 유사도 0.7 초과 쌍 플래그

- REQ-L2-006.3: Phase 3 - 병합 전략
  - 품질 점수 최고인 요구사항을 주 요구사항으로
  - 모든 중복의 소스 정보 집계
  - 중복 제거 기록 생성

#### REQ-L2-007: 분류 로직 구현

**EARS 형식:**
THE parvis-aispec-transformer agent SHALL classify requirements by type (functional, safety, interface, constraint) and priority (critical, high, medium, low).

**상세 요구사항:**

- REQ-L2-007.1: 유형 분류
  - Functional: 시스템 동작 설명, 기능 명세
  - Safety: 안전 관련 용어 포함 (safe state, fault, error, diagnostic, FAS_ASSERT)
  - Interface: 컴포넌트 간 통신, 데이터 교환 형식, API
  - Constraint: 제한사항 ("shall not", "must not"), 임계값

- REQ-L2-007.2: 우선순위 분류
  - Critical: 안전 관련, 시스템 수준, 다수 파생 요구사항의 기반
  - High: 핵심 기능, 다중 컴포넌트 참조, 외부 인터페이스
  - Medium: 표준 기능, 모듈별 동작, 구성 파라미터
  - Low: 개선/최적화, 선택 기능, 문서화 요구사항

#### REQ-L2-008: 품질 메트릭 계산 구현

**EARS 형식:**
THE parvis-aispec-transformer agent SHALL calculate quality scores (0-100) for each requirement based on completeness, clarity, testability, and atomicity.

**상세 요구사항:**

- REQ-L2-008.1: 완전성 점수 (25점)
  - 필수 필드 채움 여부
  - 누락 필드당 -5점

- REQ-L2-008.2: 명확성 점수 (25점)
  - 모호한 용어 탐지 (always, never, all, none, some, any)
  - 주관적 수식어 탐지 (very, extremely, highly)
  - 모호한 논리 탐지 (and/or)
  - 인스턴스당 -3점

- REQ-L2-008.3: 테스트 가능성 점수 (25점)
  - 수치 임계값 존재
  - 시간 제약 명시
  - 명확한 통과/실패 기준
  - 관찰 가능한 결과 정의

- REQ-L2-008.4: 원자성 점수 (25점)
  - 복합 요구사항 탐지 (다중 "shall" 문)
  - 접속사 과다 (and, additionally, also)
  - 추가 요구사항 탐지당 -10점

### 3.3 통합 요구사항

#### REQ-L2-009: 에이전트 실행 순서 보장

**EARS 형식:**
THE PARVIS orchestrator SHALL ensure parvis-aispec-reqid executes before parvis-aispec-transformer to guarantee ID availability for normalization.

**상세 요구사항:**

- REQ-L2-009.1: 실행 순서: parvis-aispec-reqid -> parvis-aispec-transformer
- REQ-L2-009.2: ID 할당 완료 후 정규화 시작
- REQ-L2-009.3: 실패 시 롤백 메커니즘

#### REQ-L2-010: L2 품질 게이트 구현

**EARS 형식:**
THE L2 phase SHALL pass quality gates before proceeding to L3 phase.

**품질 게이트 기준:**

| 품질 게이트 | 기준 | 목표 |
|-----------|------|------|
| QG-L2-001 | High Confidence 비율 | 75% 이상 |
| QG-L2-002 | 모듈 커버리지 | 12개 모듈 75% 이상 |
| QG-L2-003 | ID 할당률 | 95% 이상 |
| QG-L2-004 | 중복 제거 완료 | 중복 0개 |
| QG-L2-005 | 품질 점수 평균 | 50점 이상 |

---

## 4. Specifications (명세)

### 4.1 출력 디렉토리 구조

```
.moai/bms/requirements/
    +-- registry/
    |       +-- id-registry.json          (마스터 ID 레지스트리)
    |       +-- id-registry.backup.json   (백업)
    |       +-- module-map.json           (모듈 매핑)
    |       +-- sequence-tracker.json     (시퀀스 추적)
    |
    +-- normalized/
    |       +-- SOA-normalized.json
    |       +-- BAL-normalized.json
    |       +-- ALG-normalized.json
    |       +-- PLS-normalized.json
    |       +-- RED-normalized.json
    |       +-- DBS-normalized.json
    |       +-- DIA-normalized.json
    |       +-- SYS-normalized.json
    |       +-- MON-normalized.json
    |       +-- CON-normalized.json
    |       +-- CAN-normalized.json
    |       +-- IMD-normalized.json
    |       +-- master-normalized.json    (통합 정규화 파일)
    |
    +-- quality/
    |       +-- l2-quality-report.md      (L2 품질 보고서)
    |       +-- deduplication-log.json    (중복 제거 로그)
    |       +-- validation-report.json    (검증 보고서)
    |
    +-- logs/
            +-- transformation-audit.json  (변환 감사 로그)
            +-- id-assignment-log.json     (ID 할당 로그)
```

### 4.2 정규화된 요구사항 스키마

```json
{
  "id": "FBMS-SWE-BMS-001",
  "content": "정규화된 요구사항 내용",
  "original_content": "원본 요구사항 내용",
  "type": "SWE",
  "classification": "functional",
  "priority": "high",
  "status": "draft",
  "sources": [
    {
      "file": "bms.c",
      "line": 42,
      "extraction_type": "doxygen"
    }
  ],
  "quality_score": 85,
  "quality_issues": [],
  "tags": ["state-machine", "behavior"],
  "created_date": "2025-12-16T00:00:00Z",
  "modified_date": "2025-12-16T00:00:00Z",
  "transformation_version": "1.0.0"
}
```

### 4.3 워크플로우 명령어

**parvis-aispec-reqid 명령어:**

| 명령어 | 기능 |
|-------|------|
| Assign IDs to requirements in [module] | 모듈 요구사항에 ID 할당 |
| Assign IDs to all extracted requirements | 전체 추출 요구사항에 ID 할당 |
| Validate IDs in [scope] | ID 유효성 검증 |
| Generate ID registry report | 레지스트리 보고서 생성 |

**parvis-aispec-transformer 명령어:**

| 명령어 | 기능 |
|-------|------|
| Normalize requirements for [module] | 모듈 요구사항 정규화 |
| Normalize all extracted requirements | 전체 요구사항 정규화 |
| Analyze requirement quality for [scope] | 품질 분석 |
| Merge sources from [source1] and [source2] | 소스 병합 |

---

## 5. Constraints (제약사항)

### 5.1 기술적 제약

- C1: ID 형식은 FBMS-[TYPE]-[MODULE]-[SEQ] 엄수
- C2: 시퀀스 번호는 999를 초과할 수 없음 (초과 시 계층 확장)
- C3: 할당된 ID는 재사용 불가 (deprecated 상태로만 변경)
- C4: 정규화된 JSON은 정의된 스키마 준수

### 5.2 성능 제약

- C5: 전체 395개 요구사항 ID 할당 시간 5분 이내
- C6: 전체 정규화 처리 시간 10분 이내
- C7: 중복 탐지 유사도 계산 시간 최적화

### 5.3 품질 제약

- C8: 품질 점수 30점 미만 요구사항은 처리 차단
- C9: 중복 제거 후 잔여 중복 0개
- C10: 모든 요구사항에 고유 ID 할당

---

## 6. Traceability (추적성)

### 6.1 SPEC 의존성

| 본 SPEC 요구사항 | 의존 SPEC |
|----------------|----------|
| REQ-L2-001~004 | SPEC-PARVIS-DEF-001 (parvis-aispec-reqid 정의) |
| REQ-L2-005~008 | SPEC-PARVIS-DEF-001 (parvis-aispec-transformer 정의) |
| REQ-L2-009~010 | SPEC-PARVIS-IMPL-001 (Phase 1 구현) |

### 6.2 ARCHITECTURE.md 연결

| 요구사항 | ARCHITECTURE.md 섹션 |
|---------|---------------------|
| REQ-L2-001~004 | ID Naming Convention System |
| REQ-L2-005~008 | Agent Definitions Summary - Phase 1 |
| REQ-L2-009~010 | Quality Gates |

### 6.3 ROADMAP.md 연결

| 요구사항 | ROADMAP.md 단계 |
|---------|-----------------|
| REQ-L2-001~004 | Phase 2.2: parvis-aispec-reqid |
| REQ-L2-005~008 | Phase 2.4: parvis-aispec-transformer |
| REQ-L2-009~010 | Phase 2 Completion Criteria |

### 6.4 에이전트 정의 연결

| 요구사항 | 에이전트 정의 파일 |
|---------|------------------|
| REQ-L2-001~004 | .claude/agents/parvis/parvis-aispec-reqid.md |
| REQ-L2-005~008 | .claude/agents/parvis/parvis-aispec-transformer.md |

---

## 7. Risk Analysis (위험 분석)

### 7.1 기술적 위험

| 위험 | 영향 | 확률 | 완화 방안 |
|-----|------|------|----------|
| 모듈 코드 매핑 불일치 | 잘못된 ID 할당 | 중간 | 매핑 테이블 검증 자동화 |
| 중복 탐지 정확도 부족 | 잔여 중복 발생 | 낮음 | 유사도 임계값 조정 |
| 품질 점수 편향 | 과도한 요구사항 거부 | 중간 | 임계값 점진적 조정 |

### 7.2 프로세스 위험

| 위험 | 영향 | 확률 | 완화 방안 |
|-----|------|------|----------|
| L1 데이터 불완전 | L2 처리 실패 | 낮음 | 입력 검증 강화 |
| 실행 순서 오류 | ID 미할당 상태 정규화 | 중간 | 의존성 검증 자동화 |

---

## 8. Version History

| 버전 | 날짜 | 작성자 | 변경 내용 |
|-----|------|-------|----------|
| 1.0.0 | 2025-12-16 | PARVIS | 초기 버전 |
