# SPEC-PARVIS-IMPL-001 구현 계획

## TAG BLOCK

```yaml
plan_id: PLAN-PARVIS-IMPL-001
spec_ref: SPEC-PARVIS-IMPL-001
version: 1.0.0
created: 2025-12-15
priority: critical
```

---

## 1. 구현 개요

### 1.1 목표

PARVIS Phase 1의 핵심 에이전트 2개를 구현하여 foxBMS 코드에서 요구사항을 추출하고 V-Model 워크플로우를 관리하는 기반을 구축한다.

### 1.2 범위

- parvis-ai-orchestrator 구현 (V-Model 단계 추적, 품질 게이트)
- parvis-aispec-code 구현 (Doxygen 파싱, 상태 머신 추출, FAS_ASSERT 분석)
- 초기 데이터 구조 생성

---

## 2. 마일스톤

### 마일스톤 1: 인프라 초기화 (우선순위: 최고)

**목표:**
- .moai/bms/ 디렉토리 구조 생성
- 구성 파일 초기화
- 모듈 매핑 정의

**산출물:**
- .moai/bms/config/agent-config.json
- .moai/bms/config/module-mapping.json
- .moai/bms/config/id-registry.json
- 필요한 하위 디렉토리들

### 마일스톤 2: parvis-aispec-code 파서 구현 (우선순위: 최고)

**목표:**
- Doxygen 파서 구현
- 상태 머신 추출기 구현
- FAS_ASSERT 추출기 구현
- 구성 파라미터 추출기 구현

**산출물:**
- Doxygen 파싱 로직
- 상태 머신 패턴 인식
- 안전 어서션 분석
- 구성 추출

### 마일스톤 3: parvis-aispec-code 출력 생성 (우선순위: 최고)

**목표:**
- 추출 결과 JSON 생성
- 추출 보고서 생성
- 신뢰도 점수 계산

**산출물:**
- [module]-extracted.json
- [module]-extraction-report.md

### 마일스톤 4: BMS 모듈 파일럿 추출 (우선순위: 최고)

**목표:**
- BMS 모듈 요구사항 추출 실행
- 추출 결과 검증
- 추출 품질 평가

**산출물:**
- BMS-extracted.json
- BMS-extraction-report.md
- 품질 평가 결과

### 마일스톤 5: parvis-ai-orchestrator 단계 추적 구현 (우선순위: 높음)

**목표:**
- 단계 상태 데이터 구조 구현
- 단계 상태 영속화
- 상태 조회 기능

**산출물:**
- 단계 추적 로직
- phase-status/[module].json 파일

### 마일스톤 6: parvis-ai-orchestrator 품질 게이트 구현 (우선순위: 높음)

**목표:**
- 품질 게이트 기준 정의
- 기준 검증 로직
- 전환 제어 로직

**산출물:**
- 품질 게이트 엔진
- 검증 결과 보고서

---

## 3. 기술적 접근

### 3.1 Doxygen 파싱 전략

**파싱 대상 태그:**
```
@file, @brief, @details, @author, @date
@ingroup, @prefix
@param, @return, @pre, @post
```

**파싱 방법:**
1. 파일 읽기
2. Doxygen 블록 식별 (/** ... */)
3. 태그별 내용 추출
4. 구조화된 데이터로 변환

**예상 출력:**
```json
{
  "file": "bms.c",
  "brief": "Main state machine for BMS",
  "details": "Implements the primary control logic...",
  "functions": [
    {
      "name": "BMS_Trigger",
      "brief": "Trigger function for BMS state machine",
      "params": [...],
      "return": "BMS_STATE_e"
    }
  ]
}
```

### 3.2 상태 머신 추출 전략

**인식 패턴:**

1. 상태 열거형 패턴:
```
typedef enum { ... } *_STATE_e;
typedef enum { ... } *_STATEMACH_e;
```

2. 상태 변수 패턴:
```
static *_STATE_s *_state;
.state = ...,
.substate = ...,
```

3. 상태 전환 패턴:
```
switch (pState->state) {
    case *_STATEMACH_*:
        ...
        pState->state = *;
        break;
}
```

**추출 알고리즘:**
1. 열거형 정의 스캔
2. 상태 값 목록 생성
3. switch-case 문 분석
4. 전환 그래프 구성

### 3.3 FAS_ASSERT 분석 전략

**인식 패턴:**
```c
FAS_ASSERT(condition);
```

**분류 기준:**
- 포인터 유효성: `!= NULL_PTR`
- 범위 검사: `< MAX`, `> MIN`, `<= MAX`, `>= MIN`
- 상태 검증: `== STATE`, `!= STATE`
- 인덱스 검증: `< ARRAY_SIZE`

**출력:**
```json
{
  "assertion_type": "range_check",
  "variable": "cellIndex",
  "constraint": "< BS_NR_OF_CELL_BLOCKS",
  "source_line": 150,
  "safety_implication": "배열 인덱스 범위 초과 방지"
}
```

### 3.4 구성 파라미터 추출 전략

**인식 패턴:**
```c
#define PARAM_NAME (value)
#define PARAM_NAME_unit (value)
```

**분류:**
- 전압 한계: `*_VOLTAGE_*`
- 전류 한계: `*_CURRENT_*`
- 온도 한계: `*_TEMPERATURE_*`
- 시간 상수: `*_TIME_*`, `*_TIMEOUT_*`

---

## 4. 의존성

### 4.1 선행 작업

| 의존성 | 설명 | 상태 |
|-------|------|------|
| 에이전트 정의 파일 | parvis-ai-orchestrator.md, parvis-aispec-code.md | 완료 |
| foxBMS 코드베이스 | foxbms-2/ 디렉토리 | 존재 확인 필요 |
| .moai/ 디렉토리 | 기본 구조 | 생성 필요 |

### 4.2 외부 의존성

| 의존성 | 용도 |
|-------|------|
| Grep 도구 | 패턴 검색 |
| Glob 도구 | 파일 검색 |
| Read/Write/Edit 도구 | 파일 조작 |

---

## 5. 위험 분석 및 대응

### 5.1 기술적 위험

| 위험 | 확률 | 영향 | 대응 전략 |
|-----|-----|-----|----------|
| Doxygen 형식 비일관성 | 중간 | 중간 | 유연한 파서, 폴백 로직 |
| 상태 머신 패턴 변형 | 중간 | 높음 | 패턴 라이브러리 확장 |
| 대용량 파일 처리 | 낮음 | 중간 | 청크 단위 처리 |
| foxBMS 경로 변경 | 낮음 | 높음 | 구성 가능한 경로 |

### 5.2 품질 위험

| 위험 | 확률 | 영향 | 대응 전략 |
|-----|-----|-----|----------|
| 낮은 추출 정확도 | 중간 | 높음 | 신뢰도 점수, 수동 검토 |
| 누락된 요구사항 | 중간 | 높음 | 커버리지 분석 |
| 잘못된 분류 | 중간 | 중간 | 검토 워크플로우 |

---

## 6. 품질 게이트

### 6.1 마일스톤별 완료 기준

**마일스톤 1 완료 기준:**
- [ ] .moai/bms/ 디렉토리 구조 생성됨
- [ ] agent-config.json 유효한 JSON
- [ ] module-mapping.json 모든 초기 모듈 포함

**마일스톤 2 완료 기준:**
- [ ] Doxygen 태그 80% 이상 인식
- [ ] 상태 열거형 100% 인식
- [ ] FAS_ASSERT 100% 인식
- [ ] 구성 상수 90% 이상 추출

**마일스톤 3 완료 기준:**
- [ ] JSON 스키마 준수
- [ ] 보고서 생성됨
- [ ] 신뢰도 점수 포함

**마일스톤 4 완료 기준:**
- [ ] BMS 모듈 추출 완료
- [ ] high confidence 비율 70% 이상
- [ ] 모든 상태 전환 추출됨
- [ ] 추출 보고서 검토됨

**마일스톤 5 완료 기준:**
- [ ] 단계 상태 파일 생성됨
- [ ] 상태 조회 기능 동작
- [ ] 상태 업데이트 기능 동작

**마일스톤 6 완료 기준:**
- [ ] 품질 게이트 기준 정의됨
- [ ] 기준 검증 로직 동작
- [ ] 전환 차단 기능 동작

---

## 7. 산출물 목록

### 7.1 구성 파일

| 파일 | 위치 |
|-----|------|
| agent-config.json | .moai/bms/config/ |
| module-mapping.json | .moai/bms/config/ |
| id-registry.json | .moai/bms/config/ |

### 7.2 추출 결과

| 파일 | 위치 |
|-----|------|
| BMS-extracted.json | .moai/bms/requirements/extracted/ |
| BMS-extraction-report.md | .moai/bms/requirements/extracted/ |

### 7.3 단계 상태

| 파일 | 위치 |
|-----|------|
| BMS.json | .moai/bms/config/phase-status/ |

---

## 8. 실행 계획

### 8.1 1단계: 환경 준비

**작업:**
1. foxbms-2/ 디렉토리 존재 확인
2. .moai/bms/ 구조 생성
3. 초기 구성 파일 생성

### 8.2 2단계: 파서 구현

**작업:**
1. Doxygen 파서 개발
2. 상태 머신 추출기 개발
3. FAS_ASSERT 분석기 개발
4. 구성 추출기 개발

### 8.3 3단계: 통합 및 테스트

**작업:**
1. BMS 모듈 파일럿 추출
2. 결과 검증
3. 품질 평가
4. 피드백 반영

### 8.4 4단계: 오케스트레이터 구현

**작업:**
1. 단계 추적 구현
2. 품질 게이트 구현
3. 통합 테스트

---

## 9. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-15 | 초기 버전 |
