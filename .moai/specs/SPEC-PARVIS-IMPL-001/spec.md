# SPEC-PARVIS-IMPL-001: PARVIS Phase 1 구현

## TAG BLOCK

```yaml
spec_id: SPEC-PARVIS-IMPL-001
title: PARVIS Phase 1 구현 - Orchestrator 및 AISpec-Code
version: 1.0.0
created: 2025-12-15
updated: 2025-12-16
status: completed
priority: critical
type: implementation
domain: agent-system
compliance:
  - ISO 26262 Part 6
  - ASPICE 4.0 SWE.1
depends_on:
  - SPEC-PARVIS-DEF-001
```

---

## 1. Environment (환경)

### 1.1 구현 대상

**Phase 1 핵심 에이전트:**

| 에이전트 | 역할 | 구현 우선순위 |
|---------|------|-------------|
| parvis-ai-orchestrator | V-Model 마스터 조정자 | 최고 |
| parvis-aispec-code | 코드 역공학 요구사항 추출 | 최고 |

### 1.2 foxBMS 코드베이스 대상

**초기 분석 대상 모듈:**

| 모듈 | 위치 | 특징 |
|-----|------|------|
| BMS | src/app/application/bms/ | 주요 상태 머신, 핵심 제어 로직 |
| SOA | src/app/application/soa/ | 안전 운영 영역 모니터링 |
| DIAG | src/app/engine/diag/ | 진단 및 오류 처리 |
| DATABASE | src/app/engine/database/ | 공유 데이터 관리 |

### 1.3 개발 환경

- **에이전트 위치**: `.claude/agents/parvis/`
- **데이터 저장**: `.moai/bms/`
- **foxBMS 소스**: `foxbms-2/src/`
- **테스트**: `foxbms-2/tests/`

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- A1: foxBMS 코드베이스가 foxbms-2/ 디렉토리에 존재
- A2: Doxygen 형식의 주석이 코드에 포함되어 있음
- A3: 상태 머신 패턴이 일관되게 사용됨
- A4: FAS_ASSERT 매크로가 안전 검증에 사용됨

### 2.2 구현 가정

- A5: 에이전트 정의 파일이 완성되어 있음
- A6: .moai/bms/ 디렉토리 구조가 초기화됨
- A7: 에이전트 간 데이터 교환은 JSON 형식

---

## 3. Requirements (요구사항)

### 3.1 parvis-ai-orchestrator 구현 요구사항

#### REQ-IMPL-001: V-Model 단계 추적 구현

**EARS 형식:**
THE parvis-ai-orchestrator SHALL 각 모듈의 V-Model 개발 단계를 추적하고 상태를 기록한다.

**상세 요구사항:**
- REQ-IMPL-001.1: 단계 상태 데이터 구조 구현
- REQ-IMPL-001.2: 단계 상태 영속화 (JSON 파일)
- REQ-IMPL-001.3: 단계 상태 조회 기능
- REQ-IMPL-001.4: 단계 전환 로직

**구현 세부사항:**

단계 상태 구조:
```json
{
  "module_id": "BMS",
  "current_phase": "L1",
  "phase_status": {
    "L1": "in_progress",
    "L2": "not_started",
    "L3": "not_started",
    "L4": "not_started",
    "R1": "not_started",
    "R2": "not_started",
    "R3": "not_started",
    "R4": "not_started"
  },
  "quality_gates": {
    "REQ-QG-001": false,
    "REQ-QG-002": false
  },
  "last_updated": "2025-12-15T00:00:00Z"
}
```

저장 위치: `.moai/bms/config/phase-status/[module].json`

#### REQ-IMPL-002: 품질 게이트 엔진 구현

**EARS 형식:**
THE parvis-ai-orchestrator SHALL 각 단계의 품질 게이트 기준을 검증하고 단계 전환을 제어한다.

**상세 요구사항:**
- REQ-IMPL-002.1: 품질 게이트 기준 정의 로드
- REQ-IMPL-002.2: 기준 검증 로직
- REQ-IMPL-002.3: 전환 허용/차단 결정
- REQ-IMPL-002.4: 미충족 기준 보고

**구현 세부사항:**

품질 게이트 검증 흐름:
1. 현재 단계의 품질 게이트 기준 로드
2. 각 기준에 대해 검증 에이전트 호출
3. 결과 수집 및 평가
4. 모든 기준 충족 시 전환 허용

#### REQ-IMPL-003: 에이전트 위임 프로토콜 구현

**EARS 형식:**
THE parvis-ai-orchestrator SHALL 적절한 하위 에이전트에 작업을 위임하고 결과를 수집한다.

**상세 요구사항:**
- REQ-IMPL-003.1: 위임 컨텍스트 생성
- REQ-IMPL-003.2: 결과 수집 및 검증
- REQ-IMPL-003.3: 오류 처리 및 재시도
- REQ-IMPL-003.4: 작업 로깅

**위임 컨텍스트 구조:**
```json
{
  "task_id": "TASK-001",
  "target_agent": "parvis-aispec-code",
  "module": "BMS",
  "phase": "L1",
  "parameters": {},
  "timestamp": "2025-12-15T00:00:00Z"
}
```

### 3.2 parvis-aispec-code 구현 요구사항

#### REQ-IMPL-004: Doxygen 파서 구현

**EARS 형식:**
THE parvis-aispec-code SHALL foxBMS Doxygen 주석을 파싱하여 요구사항 정보를 추출한다.

**상세 요구사항:**
- REQ-IMPL-004.1: 파일 헤더 파싱 (@file, @brief, @details)
- REQ-IMPL-004.2: 함수 문서 파싱 (@brief, @param, @return, @pre, @post)
- REQ-IMPL-004.3: 그룹 정보 파싱 (@ingroup, @prefix)
- REQ-IMPL-004.4: 추출 결과 구조화

**Doxygen 태그 매핑:**

| Doxygen 태그 | 추출 정보 | 요구사항 필드 |
|-------------|----------|-------------|
| @file | 모듈명 | module |
| @brief | 기능 설명 | description |
| @details | 상세 설명 | details |
| @param | 입력 제약 | input_constraints |
| @return | 출력 명세 | output_spec |
| @pre | 전제 조건 | preconditions |
| @post | 사후 조건 | postconditions |

#### REQ-IMPL-005: 상태 머신 추출기 구현

**EARS 형식:**
THE parvis-aispec-code SHALL foxBMS 상태 머신 패턴을 인식하고 상태 전환 요구사항을 추출한다.

**상세 요구사항:**
- REQ-IMPL-005.1: 상태 열거형 인식 (typedef enum *_STATE_e)
- REQ-IMPL-005.2: 상태 변수 인식 (static *_state)
- REQ-IMPL-005.3: 상태 전환 로직 분석 (switch-case)
- REQ-IMPL-005.4: 전환 조건 추출

**foxBMS 상태 머신 패턴:**

상태 열거형:
```c
typedef enum {
    BMS_STATEMACH_UNINITIALIZED,
    BMS_STATEMACH_INITIALIZATION,
    BMS_STATEMACH_INITIALIZED,
    BMS_STATEMACH_IDLE,
    BMS_STATEMACH_RUNNING,
    BMS_STATEMACH_ERROR
} BMS_STATEMACH_e;
```

상태 변수:
```c
static BMS_STATE_s bms_state = {
    .state = BMS_STATEMACH_UNINITIALIZED,
    .substate = BMS_ENTRY,
    .lastState = BMS_STATEMACH_UNINITIALIZED,
    .timer = 0u,
};
```

#### REQ-IMPL-006: FAS_ASSERT 추출기 구현

**EARS 형식:**
THE parvis-aispec-code SHALL FAS_ASSERT 매크로를 분석하여 안전 제약 요구사항을 추출한다.

**상세 요구사항:**
- REQ-IMPL-006.1: FAS_ASSERT 문 인식
- REQ-IMPL-006.2: 조건식 파싱
- REQ-IMPL-006.3: 안전 제약 도출
- REQ-IMPL-006.4: 분류 (파라미터 검증, 범위 검사, 상태 검증)

**FAS_ASSERT 패턴:**
```c
FAS_ASSERT(pBmsState != NULL_PTR);  /* 포인터 유효성 */
FAS_ASSERT(cellIndex < BS_NR_OF_CELL_BLOCKS);  /* 범위 검사 */
FAS_ASSERT(state == BMS_STATEMACH_INITIALIZED);  /* 상태 검증 */
```

#### REQ-IMPL-007: 구성 파라미터 추출기 구현

**EARS 형식:**
THE parvis-aispec-code SHALL *_cfg.c/h 파일에서 구성 파라미터를 추출하여 구성 요구사항을 도출한다.

**상세 요구사항:**
- REQ-IMPL-007.1: #define 상수 추출
- REQ-IMPL-007.2: 구성 구조체 추출
- REQ-IMPL-007.3: 임계값 및 한계 식별
- REQ-IMPL-007.4: 구성 의존성 분석

**구성 패턴 예:**
```c
/* battery_cell_cfg.h */
#define BC_CELL_MAX_VOLTAGE_mV (4200u)
#define BC_CELL_MIN_VOLTAGE_mV (2500u)
#define BC_TEMPERATURE_MAX_DISCHARGE_deci_degC (550)
```

#### REQ-IMPL-008: 요구사항 출력 생성기 구현

**EARS 형식:**
THE parvis-aispec-code SHALL 추출된 정보를 구조화된 요구사항 JSON으로 출력한다.

**상세 요구사항:**
- REQ-IMPL-008.1: 추출 결과 통합
- REQ-IMPL-008.2: JSON 스키마 준수
- REQ-IMPL-008.3: 신뢰도 점수 계산
- REQ-IMPL-008.4: 추적성 힌트 포함

**출력 JSON 스키마:**
```json
{
  "extraction_id": "EXT-BMS-001",
  "source_file": "src/app/application/bms/bms.c",
  "extracted_at": "2025-12-15T00:00:00Z",
  "requirements": [
    {
      "req_id": null,
      "suggested_type": "SWE",
      "suggested_module": "BMS",
      "extraction_type": "doxygen|state_machine|assertion|config",
      "content": "요구사항 내용",
      "source_line": 100,
      "confidence": "high|medium|low",
      "traceability_hints": ["function_name", "state_name"],
      "rationale": "추출 근거"
    }
  ],
  "statistics": {
    "total_extracted": 25,
    "high_confidence": 18,
    "medium_confidence": 5,
    "low_confidence": 2
  }
}
```

---

## 4. Specifications (명세)

### 4.1 데이터 디렉토리 구조

```
.moai/bms/
    +-- config/
    |       +-- agent-config.json
    |       +-- id-registry.json
    |       +-- module-mapping.json
    |       +-- phase-status/
    |               +-- BMS.json
    |               +-- SOA.json
    |               +-- DIAG.json
    |
    +-- requirements/
    |       +-- extracted/
    |       |       +-- BMS-extracted.json
    |       |       +-- BMS-extraction-report.md
    |       +-- normalized/
    |       +-- safety/
    |
    +-- traceability/
    |       +-- matrix.json
    |       +-- indexes/
    |
    +-- quality/
            +-- gates/
            +-- reports/
```

### 4.2 모듈 매핑

```json
{
  "modules": {
    "BMS": {
      "code": "BMS",
      "name": "Battery Management System",
      "path": "src/app/application/bms/",
      "type": "application",
      "safety_critical": true
    },
    "SOA": {
      "code": "SOA",
      "name": "Safe Operating Area",
      "path": "src/app/application/soa/",
      "type": "application",
      "safety_critical": true
    },
    "DIAG": {
      "code": "DIAG",
      "name": "Diagnostics",
      "path": "src/app/engine/diag/",
      "type": "engine",
      "safety_critical": true
    },
    "DB": {
      "code": "DB",
      "name": "Database",
      "path": "src/app/engine/database/",
      "type": "engine",
      "safety_critical": false
    }
  }
}
```

### 4.3 워크플로우 명령어

**parvis-ai-orchestrator 명령어:**

| 명령어 | 기능 |
|-------|------|
| Initialize V-Model for [module] | 모듈 V-Model 워크플로우 초기화 |
| Check phase status for [module] | 현재 단계 상태 확인 |
| Advance [module] to next phase | 다음 단계로 전환 시도 |
| Generate V-Model status report | 전체 상태 보고서 생성 |

**parvis-aispec-code 명령어:**

| 명령어 | 기능 |
|-------|------|
| Extract requirements from [module] | 모듈에서 요구사항 추출 |
| Extract all requirements | 전체 코드베이스에서 추출 |
| Extract requirements from changed files | 변경된 파일에서 추출 |

---

## 5. Constraints (제약사항)

### 5.1 기술적 제약

- C1: foxBMS Doxygen 스타일 준수 필수
- C2: 상태 머신 패턴은 foxBMS 표준을 따름
- C3: JSON 출력은 정의된 스키마 준수
- C4: 파일 접근은 정의된 경로 내에서만 수행

### 5.2 성능 제약

- C5: 단일 모듈 추출 시간 3분 이내
- C6: 전체 코드베이스 추출 시간 30분 이내
- C7: 메모리 사용량 최적화

### 5.3 품질 제약

- C8: 추출된 요구사항의 high confidence 비율 70% 이상
- C9: 모든 상태 전환이 추출되어야 함
- C10: 모든 FAS_ASSERT가 분석되어야 함

---

## 6. Traceability (추적성)

### 6.1 SPEC-PARVIS-DEF-001 연결

| 구현 요구사항 | 정의 요구사항 |
|-------------|-------------|
| REQ-IMPL-001 | parvis-ai-orchestrator 정의 |
| REQ-IMPL-002 | parvis-ai-orchestrator 정의 |
| REQ-IMPL-003 | parvis-ai-orchestrator 정의 |
| REQ-IMPL-004 | REQ-DEF-001 (parvis-aispec-code) |
| REQ-IMPL-005 | REQ-DEF-001 (parvis-aispec-code) |
| REQ-IMPL-006 | REQ-DEF-001 (parvis-aispec-code) |
| REQ-IMPL-007 | REQ-DEF-001 (parvis-aispec-code) |
| REQ-IMPL-008 | REQ-DEF-001 (parvis-aispec-code) |

### 6.2 ARCHITECTURE.md 연결

| 구현 요구사항 | ARCHITECTURE.md 섹션 |
|-------------|---------------------|
| REQ-IMPL-001~003 | PARVIS-AI-Orchestrator Design |
| REQ-IMPL-004~008 | Phase 1: PARVIS-AISpec Agents |

### 6.3 ROADMAP.md 연결

| 구현 요구사항 | ROADMAP.md 단계 |
|-------------|-----------------|
| REQ-IMPL-001~003 | Phase 1.1: PARVIS-AI-Orchestrator Core |
| REQ-IMPL-004~008 | Phase 2.1: parvis-aispec-code |

---

## 7. Version History

| 버전 | 날짜 | 작성자 | 변경 내용 |
|-----|------|-------|----------|
| 1.0.0 | 2025-12-15 | PARVIS | 초기 버전 |
