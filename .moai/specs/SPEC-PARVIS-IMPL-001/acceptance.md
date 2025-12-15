# SPEC-PARVIS-IMPL-001 인수 기준

## TAG BLOCK

```yaml
acceptance_id: ACC-PARVIS-IMPL-001
spec_ref: SPEC-PARVIS-IMPL-001
version: 1.0.0
created: 2025-12-15
```

---

## 1. 인수 기준 개요

### 1.1 목적

PARVIS Phase 1 구현이 요구사항을 충족하는지 검증한다.

### 1.2 범위

- parvis-ai-orchestrator 구현 검증
- parvis-aispec-code 구현 검증
- 데이터 구조 검증
- 품질 메트릭 검증

---

## 2. 인수 테스트 시나리오

### 2.1 인프라 검증

#### AC-IMPL-001: 디렉토리 구조 생성

**Given:** PARVIS Phase 1 구현이 완료됨
**When:** .moai/bms/ 디렉토리를 검사함
**Then:**
- .moai/bms/config/ 디렉토리가 존재함
- .moai/bms/requirements/extracted/ 디렉토리가 존재함
- .moai/bms/requirements/normalized/ 디렉토리가 존재함
- .moai/bms/traceability/ 디렉토리가 존재함
- .moai/bms/quality/ 디렉토리가 존재함

#### AC-IMPL-002: 구성 파일 유효성

**Given:** 구성 파일들이 생성됨
**When:** 각 구성 파일을 JSON 파싱함
**Then:**
- agent-config.json이 유효한 JSON임
- module-mapping.json이 유효한 JSON임
- id-registry.json이 유효한 JSON임
- 각 파일이 정의된 스키마를 준수함

### 2.2 parvis-aispec-code 검증

#### AC-IMPL-003: Doxygen 파서 기능

**Given:** parvis-aispec-code 에이전트가 활성화됨
**When:** BMS 모듈 소스 파일을 분석함
**Then:**
- @file 태그에서 모듈명이 추출됨
- @brief 태그에서 기능 설명이 추출됨
- @param 태그에서 파라미터 정보가 추출됨
- @return 태그에서 반환값 정보가 추출됨
- @pre 태그에서 전제 조건이 추출됨
- @post 태그에서 사후 조건이 추출됨

#### AC-IMPL-004: 상태 머신 추출 기능

**Given:** BMS 모듈의 상태 머신 코드가 존재함
**When:** 상태 머신 추출기를 실행함
**Then:**
- BMS_STATEMACH_e 열거형이 인식됨
- 모든 상태 값이 추출됨 (UNINITIALIZED, INITIALIZATION, INITIALIZED, IDLE, RUNNING, ERROR)
- 상태 전환 조건이 추출됨
- 상태 변수 구조가 인식됨

#### AC-IMPL-005: FAS_ASSERT 분석 기능

**Given:** BMS 모듈에 FAS_ASSERT 문이 존재함
**When:** FAS_ASSERT 추출기를 실행함
**Then:**
- 모든 FAS_ASSERT 문이 인식됨
- 조건식이 파싱됨
- 분류가 수행됨 (포인터 유효성, 범위 검사, 상태 검증)
- 안전 제약이 도출됨

#### AC-IMPL-006: 구성 파라미터 추출 기능

**Given:** *_cfg.h 파일이 존재함
**When:** 구성 추출기를 실행함
**Then:**
- #define 상수가 추출됨
- 전압 한계 파라미터가 식별됨
- 온도 한계 파라미터가 식별됨
- 시간 상수가 식별됨

#### AC-IMPL-007: 추출 결과 JSON 생성

**Given:** BMS 모듈 추출이 완료됨
**When:** 출력 파일을 검사함
**Then:**
- BMS-extracted.json 파일이 존재함
- JSON이 정의된 스키마를 준수함
- requirements 배열에 추출된 요구사항이 포함됨
- 각 요구사항에 extraction_type, content, confidence가 포함됨
- statistics 섹션에 통계가 포함됨

#### AC-IMPL-008: 추출 보고서 생성

**Given:** BMS 모듈 추출이 완료됨
**When:** 보고서 파일을 검사함
**Then:**
- BMS-extraction-report.md 파일이 존재함
- 추출 요약이 포함됨
- 신뢰도별 분류가 포함됨
- 검토 필요 항목이 표시됨

### 2.3 품질 메트릭 검증

#### AC-IMPL-009: 추출 신뢰도 메트릭

**Given:** BMS 모듈 추출 결과가 생성됨
**When:** 신뢰도 통계를 분석함
**Then:**
- high confidence 요구사항 비율이 70% 이상임
- medium confidence 요구사항이 식별됨
- low confidence 요구사항에 검토 플래그가 있음

#### AC-IMPL-010: 추출 완전성 메트릭

**Given:** BMS 모듈 추출 결과가 생성됨
**When:** 완전성을 분석함
**Then:**
- 모든 상태 전환이 추출됨
- 모든 FAS_ASSERT가 분석됨
- 주요 구성 파라미터가 추출됨

### 2.4 parvis-ai-orchestrator 검증

#### AC-IMPL-011: 단계 상태 추적 기능

**Given:** parvis-ai-orchestrator 에이전트가 활성화됨
**When:** "Initialize V-Model for BMS" 명령을 실행함
**Then:**
- .moai/bms/config/phase-status/BMS.json 파일이 생성됨
- current_phase가 "L1"로 설정됨
- phase_status에 모든 단계가 포함됨
- quality_gates에 기준이 포함됨

#### AC-IMPL-012: 단계 상태 조회 기능

**Given:** BMS 모듈의 단계 상태가 초기화됨
**When:** "Check phase status for BMS" 명령을 실행함
**Then:**
- 현재 단계가 반환됨
- 완료된 품질 게이트 기준이 표시됨
- 미완료된 품질 게이트 기준이 표시됨

#### AC-IMPL-013: 품질 게이트 검증 기능

**Given:** 요구사항 단계 (L1)가 진행 중임
**When:** "Advance BMS to next phase" 명령을 실행함
**Then:**
- 품질 게이트 기준이 검증됨
- 미충족 기준이 있으면 전환이 차단됨
- 차단 사유가 보고됨

### 2.5 통합 검증

#### AC-IMPL-014: 에이전트 간 데이터 교환

**Given:** parvis-aispec-code 추출이 완료됨
**When:** parvis-ai-orchestrator가 결과를 참조함
**Then:**
- 추출 결과 JSON을 읽을 수 있음
- 통계를 품질 게이트 검증에 사용할 수 있음

#### AC-IMPL-015: 전체 워크플로우 실행

**Given:** 모든 Phase 1 구현이 완료됨
**When:** BMS 모듈에 대해 전체 워크플로우를 실행함
**Then:**
1. V-Model 초기화 성공
2. 요구사항 추출 성공
3. 추출 결과 저장 성공
4. 단계 상태 업데이트 성공
5. 품질 게이트 검증 성공

---

## 3. 검증 체크리스트

### 3.1 인프라 체크리스트

- [ ] .moai/bms/ 디렉토리 구조 완성
- [ ] agent-config.json 유효
- [ ] module-mapping.json 유효
- [ ] id-registry.json 유효

### 3.2 parvis-aispec-code 체크리스트

- [ ] Doxygen 파서 동작
- [ ] 상태 머신 추출기 동작
- [ ] FAS_ASSERT 분석기 동작
- [ ] 구성 추출기 동작
- [ ] JSON 출력 생성
- [ ] 보고서 생성

### 3.3 품질 메트릭 체크리스트

- [ ] high confidence 비율 >= 70%
- [ ] 상태 전환 100% 추출
- [ ] FAS_ASSERT 100% 분석

### 3.4 parvis-ai-orchestrator 체크리스트

- [ ] 단계 상태 초기화 기능
- [ ] 단계 상태 조회 기능
- [ ] 품질 게이트 검증 기능
- [ ] 단계 전환 제어 기능

### 3.5 통합 체크리스트

- [ ] 에이전트 간 데이터 교환
- [ ] 전체 워크플로우 실행

---

## 4. Definition of Done

SPEC-PARVIS-IMPL-001은 다음 조건이 모두 충족될 때 완료된다:

1. **인프라 완료**: 모든 디렉토리 및 구성 파일 생성됨
2. **추출기 구현 완료**: Doxygen, 상태 머신, FAS_ASSERT, 구성 파서 동작
3. **출력 생성 완료**: JSON 및 보고서 파일 생성됨
4. **품질 기준 충족**: high confidence >= 70%, 완전성 100%
5. **오케스트레이터 구현 완료**: 단계 추적 및 품질 게이트 동작
6. **통합 테스트 통과**: 전체 워크플로우 성공적 실행

---

## 5. 검증 명령어

### 5.1 인프라 검증

```bash
# 디렉토리 구조 확인
ls -la .moai/bms/

# JSON 유효성 확인
cat .moai/bms/config/module-mapping.json | python -m json.tool
```

### 5.2 추출 검증

```bash
# 추출 결과 확인
cat .moai/bms/requirements/extracted/BMS-extracted.json | python -m json.tool

# 통계 확인
grep -A 5 "statistics" .moai/bms/requirements/extracted/BMS-extracted.json
```

### 5.3 단계 상태 검증

```bash
# 단계 상태 확인
cat .moai/bms/config/phase-status/BMS.json | python -m json.tool
```

---

## 6. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-15 | 초기 버전 |
