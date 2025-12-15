# SPEC-PARVIS-L2-001 Implementation Plan

## TAG BLOCK

```yaml
spec_id: SPEC-PARVIS-L2-001
plan_version: 1.0.0
created: 2025-12-16
updated: 2025-12-16
status: draft
```

---

## 1. Overview (개요)

### 1.1 목표

본 구현 계획은 PARVIS L2 Phase (Requirement Normalization and ID Assignment)의 단계별 구현 전략을 정의합니다.

### 1.2 범위

- parvis-aispec-reqid 에이전트 활성화 및 실행
- parvis-aispec-transformer 에이전트 활성화 및 실행
- 395개 추출 요구사항에 대한 ID 할당 및 정규화
- L2 품질 게이트 검증

### 1.3 선행 조건

| 조건 | 상태 | 비고 |
|-----|------|------|
| SPEC-PARVIS-IMPL-001 완료 | COMPLETED | Phase 1 완료 |
| 395개 요구사항 추출 | COMPLETED | extraction_summary.json 확인 |
| 에이전트 정의 완료 | COMPLETED | parvis-aispec-reqid, parvis-aispec-transformer |
| 데이터 디렉토리 구조 | COMPLETED | .moai/bms/ 구조 |

---

## 2. Implementation Milestones (구현 마일스톤)

### Milestone 1: 인프라 준비 (Primary Goal)

**목표:** L2 실행을 위한 디렉토리 구조 및 설정 파일 준비

**작업 항목:**

| 작업 ID | 작업 내용 | 의존성 |
|--------|---------|--------|
| M1-T01 | registry 디렉토리 생성 | 없음 |
| M1-T02 | normalized 디렉토리 생성 | 없음 |
| M1-T03 | quality 디렉토리 생성 | 없음 |
| M1-T04 | logs 디렉토리 생성 | 없음 |
| M1-T05 | module-map.json 초기화 | M1-T01 |
| M1-T06 | sequence-tracker.json 초기화 | M1-T01 |
| M1-T07 | reqid-config.json 생성 | M1-T01 |
| M1-T08 | transformer-config.json 생성 | M1-T02 |

**산출물:**
- `.moai/bms/requirements/registry/` 디렉토리
- `.moai/bms/requirements/normalized/` 디렉토리
- `.moai/bms/requirements/quality/` 디렉토리
- `.moai/bms/requirements/logs/` 디렉토리
- 초기 설정 파일들

---

### Milestone 2: parvis-aispec-reqid 실행 (Primary Goal)

**목표:** 395개 요구사항에 고유 ID 할당

**작업 항목:**

| 작업 ID | 작업 내용 | 의존성 |
|--------|---------|--------|
| M2-T01 | 추출 요구사항 로드 | M1 완료 |
| M2-T02 | 모듈별 요구사항 그룹화 | M2-T01 |
| M2-T03 | TYPE 코드 분류 | M2-T02 |
| M2-T04 | MODULE 코드 매핑 | M2-T02 |
| M2-T05 | 시퀀스 번호 할당 | M2-T03, M2-T04 |
| M2-T06 | ID 레지스트리 생성 | M2-T05 |
| M2-T07 | ID 충돌 검사 | M2-T06 |
| M2-T08 | ID 할당 결과 저장 | M2-T07 |
| M2-T09 | ID 할당 로그 생성 | M2-T08 |

**에이전트 실행 순서:**

Step 1: parvis-aispec-reqid 에이전트 호출
- 입력: `.moai/bms/requirements/extracted/*.json`
- 명령: "Assign IDs to all extracted requirements"
- 출력: ID 매핑이 포함된 요구사항

Step 2: ID 레지스트리 검증
- 입력: 생성된 id-registry.json
- 명령: "Validate IDs in all"
- 출력: 검증 보고서

**산출물:**
- `.moai/bms/requirements/registry/id-registry.json`
- `.moai/bms/requirements/logs/id-assignment-log.json`
- ID 할당 검증 보고서

**성공 기준:**
- 395개 요구사항 중 95% 이상 ID 할당 완료
- ID 충돌 0건
- 형식 위반 0건

---

### Milestone 3: parvis-aispec-transformer 실행 (Secondary Goal)

**목표:** ID가 할당된 요구사항의 정규화 및 품질 평가

**작업 항목:**

| 작업 ID | 작업 내용 | 의존성 |
|--------|---------|--------|
| M3-T01 | ID 할당된 요구사항 로드 | M2 완료 |
| M3-T02 | 내용 정규화 적용 | M3-T01 |
| M3-T03 | 용어 정규화 적용 | M3-T02 |
| M3-T04 | 속성 매핑 적용 | M3-T03 |
| M3-T05 | 중복 탐지 (Phase 1: Exact) | M3-T04 |
| M3-T06 | 중복 탐지 (Phase 2: Semantic) | M3-T05 |
| M3-T07 | 중복 병합 (Phase 3: Merge) | M3-T06 |
| M3-T08 | 유형 분류 적용 | M3-T07 |
| M3-T09 | 우선순위 분류 적용 | M3-T08 |
| M3-T10 | 품질 점수 계산 | M3-T09 |
| M3-T11 | 정규화 결과 저장 | M3-T10 |
| M3-T12 | 품질 보고서 생성 | M3-T11 |

**에이전트 실행 순서:**

Step 1: parvis-aispec-transformer 에이전트 호출
- 입력: ID 할당된 요구사항
- 명령: "Normalize all extracted requirements"
- 출력: 정규화된 요구사항 JSON

Step 2: 품질 분석 실행
- 입력: 정규화된 요구사항
- 명령: "Analyze requirement quality for all"
- 출력: 품질 보고서

**산출물:**
- `.moai/bms/requirements/normalized/[module]-normalized.json` (12개 파일)
- `.moai/bms/requirements/normalized/master-normalized.json`
- `.moai/bms/requirements/quality/l2-quality-report.md`
- `.moai/bms/requirements/quality/deduplication-log.json`
- `.moai/bms/requirements/logs/transformation-audit.json`

**성공 기준:**
- 중복 제거 후 잔여 중복 0건
- 평균 품질 점수 50점 이상
- 품질 점수 30점 미만 요구사항 플래그 및 보고

---

### Milestone 4: L2 품질 게이트 검증 (Final Goal)

**목표:** L2 완료 기준 검증 및 L3 진행 승인

**작업 항목:**

| 작업 ID | 작업 내용 | 의존성 |
|--------|---------|--------|
| M4-T01 | QG-L2-001 검증 (High Confidence 비율) | M3 완료 |
| M4-T02 | QG-L2-002 검증 (모듈 커버리지) | M3 완료 |
| M4-T03 | QG-L2-003 검증 (ID 할당률) | M2 완료 |
| M4-T04 | QG-L2-004 검증 (중복 제거) | M3 완료 |
| M4-T05 | QG-L2-005 검증 (품질 점수 평균) | M3 완료 |
| M4-T06 | 품질 게이트 종합 보고서 | M4-T01~T05 |
| M4-T07 | L2 완료 상태 업데이트 | M4-T06 |

**품질 게이트 기준:**

| 게이트 ID | 기준 | 목표값 | 검증 방법 |
|----------|------|--------|----------|
| QG-L2-001 | High Confidence 비율 | 75% 이상 | 정규화 후 confidence 필드 집계 |
| QG-L2-002 | 모듈 커버리지 | 12개 모듈 75% 이상 | 모듈별 요구사항 존재 확인 |
| QG-L2-003 | ID 할당률 | 95% 이상 | id-registry.json 분석 |
| QG-L2-004 | 중복 제거 완료 | 중복 0개 | deduplication-log.json 확인 |
| QG-L2-005 | 품질 점수 평균 | 50점 이상 | quality_score 필드 평균 |

**산출물:**
- `.moai/bms/quality/gates/l2-gate-report.json`
- `.moai/bms/config/phase-status/` 업데이트

---

## 3. Technical Approach (기술적 접근)

### 3.1 ID 생성 알고리즘

**Step 1: 요구사항 로드 및 분류**
```
For each extracted requirement:
  1. Load requirement from extracted/*.json
  2. Extract suggested_type and suggested_module
  3. Map to standard TYPE and MODULE codes
```

**Step 2: 시퀀스 할당**
```
For each TYPE+MODULE combination:
  1. Look up current sequence in sequence-tracker.json
  2. Allocate next available sequence
  3. Format: FBMS-{TYPE}-{MODULE}-{SEQ:03d}
  4. Update sequence-tracker.json
```

**Step 3: 레지스트리 업데이트**
```
For each assigned ID:
  1. Create registry entry
  2. Check for collisions
  3. Update id-registry.json atomically
  4. Log assignment
```

### 3.2 정규화 파이프라인

**Pipeline Stages:**

```
Stage 1: Input Validation
  - Verify JSON schema compliance
  - Check required fields
  - Log invalid entries

Stage 2: Content Normalization
  - Trim whitespace
  - Normalize internal spacing
  - Standardize punctuation
  - Preserve technical terms

Stage 3: Term Normalization
  - Apply term replacement rules
  - Add appropriate tags

Stage 4: Attribute Mapping
  - Map extraction_type to classification
  - Add domain tags

Stage 5: Deduplication
  - Phase 1: Exact match
  - Phase 2: Semantic similarity
  - Phase 3: Merge

Stage 6: Classification
  - Type classification
  - Priority assignment

Stage 7: Quality Scoring
  - Calculate component scores
  - Aggregate total score
  - Identify issues

Stage 8: Output Generation
  - Generate normalized JSON
  - Create quality report
  - Update audit log
```

### 3.3 중복 탐지 알고리즘

**Exact Match Detection:**
```
1. For each requirement:
   a. Normalize content (lowercase, remove punctuation)
   b. Generate SHA-256 hash
   c. Store in hash map

2. Group requirements by hash
3. Mark groups with size > 1 as duplicates
```

**Semantic Similarity:**
```
1. For each requirement:
   a. Extract key terms (nouns, verbs, technical terms)
   b. Create term set

2. For each pair of requirements:
   a. Calculate Jaccard similarity:
      J(A,B) = |A intersect B| / |A union B|
   b. If J > 0.7, flag as potential duplicate

3. Review flagged pairs for merge decision
```

---

## 4. Risk Mitigation (위험 완화)

### 4.1 기술적 위험 완화

| 위험 | 완화 전략 |
|-----|----------|
| 모듈 코드 매핑 불일치 | 사전 매핑 테이블 검증, 알 수 없는 코드 플래그 |
| ID 충돌 | 할당 전 충돌 검사 필수화, 트랜잭션 처리 |
| 중복 탐지 오류 | 유사도 임계값 조정 가능, 수동 검토 옵션 |
| 품질 점수 편향 | 임계값 구성 가능, 점진적 조정 |

### 4.2 프로세스 위험 완화

| 위험 | 완화 전략 |
|-----|----------|
| 실행 순서 오류 | Orchestrator 의존성 검증 |
| 데이터 손실 | 처리 전 백업, 롤백 메커니즘 |
| 품질 게이트 실패 | 세부 실패 원인 보고, 재처리 옵션 |

---

## 5. Agent Execution Order (에이전트 실행 순서)

### 5.1 전체 실행 흐름

```
Phase L2 Execution Flow:

[Start L2]
    |
    v
[Milestone 1: Infrastructure Setup]
    |
    v
[parvis-aispec-reqid]
    |
    +-- Input: extracted/*.json (395 requirements)
    +-- Process: ID assignment
    +-- Output: ID-mapped requirements
    |
    v
[ID Validation Check]
    |
    +-- Pass: Continue to Milestone 3
    +-- Fail: Report errors, halt
    |
    v
[parvis-aispec-transformer]
    |
    +-- Input: ID-mapped requirements
    +-- Process: Normalization pipeline
    +-- Output: Normalized requirements
    |
    v
[Quality Gate Validation]
    |
    +-- QG-L2-001: High Confidence >= 75%
    +-- QG-L2-002: Module Coverage >= 75%
    +-- QG-L2-003: ID Assignment >= 95%
    +-- QG-L2-004: Duplicates = 0
    +-- QG-L2-005: Avg Quality >= 50
    |
    v
[All Gates Pass?]
    |
    +-- Yes: [L2 Complete] -> Ready for L3
    +-- No: [Report Failures] -> Remediation Required
```

### 5.2 에이전트별 호출 명령

**parvis-aispec-reqid 호출:**
```
Agent: parvis-aispec-reqid
Command: "Assign IDs to all extracted requirements"
Input:
  - Path: .moai/bms/requirements/extracted/*.json
  - Count: 395 requirements
Expected Output:
  - id-registry.json with 375+ entries (95% threshold)
  - id-assignment-log.json
  - Zero collisions
```

**parvis-aispec-transformer 호출:**
```
Agent: parvis-aispec-transformer
Command: "Normalize all extracted requirements"
Input:
  - Path: ID-assigned requirements
  - Count: 395 requirements
Expected Output:
  - 12 module-specific normalized JSON files
  - master-normalized.json
  - deduplication-log.json
  - transformation-audit.json
  - l2-quality-report.md
```

---

## 6. Deliverables Summary (산출물 요약)

### 6.1 파일 산출물

| 파일 | 위치 | 설명 |
|-----|------|------|
| id-registry.json | registry/ | 마스터 ID 레지스트리 |
| module-map.json | registry/ | 모듈 코드 매핑 |
| sequence-tracker.json | registry/ | 시퀀스 추적 |
| [module]-normalized.json | normalized/ | 모듈별 정규화 파일 (12개) |
| master-normalized.json | normalized/ | 통합 정규화 파일 |
| l2-quality-report.md | quality/ | L2 품질 보고서 |
| deduplication-log.json | quality/ | 중복 제거 로그 |
| validation-report.json | quality/ | 검증 보고서 |
| transformation-audit.json | logs/ | 변환 감사 로그 |
| id-assignment-log.json | logs/ | ID 할당 로그 |
| l2-gate-report.json | quality/gates/ | 품질 게이트 결과 |

### 6.2 상태 업데이트

| 파일 | 업데이트 내용 |
|-----|-------------|
| phase-status/BMS.json | L2: completed |
| config.json | l2_completed: true |
| extraction_summary.json | l2_metrics 추가 |

---

## 7. Success Criteria (성공 기준)

### 7.1 Milestone별 성공 기준

| Milestone | 성공 기준 |
|-----------|----------|
| M1 | 모든 디렉토리 및 설정 파일 생성 완료 |
| M2 | 95% 이상 요구사항 ID 할당, 충돌 0건 |
| M3 | 정규화 완료, 중복 0건, 평균 품질 50점 이상 |
| M4 | 모든 품질 게이트 통과 |

### 7.2 전체 L2 성공 기준

- 395개 요구사항 중 375개 이상 ID 할당 완료 (95%)
- 정규화 후 중복 요구사항 0개
- High Confidence 비율 75% 이상 유지
- 12개 모듈 중 9개 이상 커버리지 (75%)
- 평균 품질 점수 50점 이상
- 모든 품질 게이트 통과

---

## 8. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-16 | 초기 버전 |
