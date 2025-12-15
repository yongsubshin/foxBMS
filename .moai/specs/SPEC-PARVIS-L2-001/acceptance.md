# SPEC-PARVIS-L2-001 Acceptance Criteria

## TAG BLOCK

```yaml
spec_id: SPEC-PARVIS-L2-001
acceptance_version: 1.0.0
created: 2025-12-16
updated: 2025-12-16
status: draft
```

---

## 1. Overview (개요)

본 문서는 SPEC-PARVIS-L2-001 (PARVIS L2 Phase - Requirement Normalization and ID Assignment)의 수락 기준을 정의합니다.

---

## 2. Acceptance Criteria by Requirement (요구사항별 수락 기준)

### 2.1 REQ-L2-001: ID 생성 알고리즘

#### AC-001: ID 형식 준수

**Given:** 추출된 요구사항이 suggested_type과 suggested_module 정보를 포함할 때
**When:** parvis-aispec-reqid 에이전트가 ID를 생성하면
**Then:**
- 생성된 ID는 FBMS-[TYPE]-[MODULE]-[SEQ] 형식을 따라야 한다
- TYPE은 SWE, FSR, HSI, TST, CFG 중 하나여야 한다
- MODULE은 정의된 모듈 코드 목록에 포함되어야 한다
- SEQ는 001-999 범위의 3자리 숫자여야 한다

**검증 방법:**
```
1. 생성된 ID 형식을 정규표현식으로 검증
   Pattern: ^FBMS-(SWE|FSR|HSI|TST|CFG)-(SOA|BAL|ALG|PLS|RED|DBS|DIA|SYS|MON|CON|CAN|IMD)-\d{3}$
2. 형식 위반 ID 개수 = 0 확인
```

#### AC-002: TYPE 코드 매핑

**Given:** 추출된 요구사항의 extraction_type이 주어질 때
**When:** TYPE 코드를 결정하면
**Then:**
- extraction_type:doxygen -> SWE
- extraction_type:assertion -> FSR
- extraction_type:state_machine -> SWE
- extraction_type:config -> CFG

**검증 방법:**
```
1. 각 extraction_type별 할당된 TYPE 코드 확인
2. 매핑 일관성 100% 확인
```

#### AC-003: MODULE 코드 매핑

**Given:** 추출된 요구사항의 suggested_module이 주어질 때
**When:** MODULE 코드를 결정하면
**Then:**
| suggested_module | MODULE 코드 |
|-----------------|------------|
| SOA | SOA |
| BAL | BAL |
| ALGO | ALG |
| PLAUS | PLS |
| REDUND | RED |
| DB | DBS |
| DIAG | DIA |
| SYS | SYS |
| SYSMON | MON |
| CONT | CON |
| CAN | CAN |
| IMD | IMD |

**검증 방법:**
```
1. module-map.json의 매핑 테이블 확인
2. 12개 모듈 모두 올바르게 매핑됨 확인
```

#### AC-004: 시퀀스 관리

**Given:** 동일 TYPE+MODULE 조합의 요구사항이 여러 개 있을 때
**When:** 시퀀스 번호를 할당하면
**Then:**
- 시퀀스는 001부터 시작하여 순차 증가
- 각 TYPE+MODULE 조합은 독립적인 시퀀스를 가짐
- sequence-tracker.json에 next_sequence가 올바르게 기록됨

**검증 방법:**
```
1. sequence-tracker.json의 각 TYPE+MODULE별 시퀀스 확인
2. 할당된 시퀀스에 중복 없음 확인
3. 시퀀스 갭 보고서 생성
```

---

### 2.2 REQ-L2-002: ID 레지스트리 관리

#### AC-005: 레지스트리 생성

**Given:** ID 할당이 완료되었을 때
**When:** id-registry.json을 확인하면
**Then:**
- 각 ID에 대한 엔트리가 존재해야 함
- 엔트리에 id, status, created_date, assigned_to, source_file 필드 포함
- status는 "assigned"로 설정

**검증 방법:**
```
1. id-registry.json 스키마 검증
2. 필수 필드 존재 확인
3. 할당된 ID 수 = 레지스트리 엔트리 수
```

#### AC-006: 레지스트리 백업

**Given:** ID 레지스트리가 수정될 때
**When:** 수정이 완료되면
**Then:**
- id-registry.backup.json에 이전 버전 저장
- 백업 파일과 현재 파일의 차이가 기록됨

**검증 방법:**
```
1. id-registry.backup.json 존재 확인
2. 백업 파일 타임스탬프가 현재 파일보다 이전임 확인
```

---

### 2.3 REQ-L2-003: 충돌 감지 및 방지

#### AC-007: 중복 ID 방지

**Given:** 새로운 ID를 할당하려고 할 때
**When:** 해당 ID가 이미 레지스트리에 존재하면
**Then:**
- ID 할당이 거부됨
- 충돌 오류가 기록됨
- 대체 ID 또는 하위 ID가 제안됨

**검증 방법:**
```
1. id-assignment-log.json에서 충돌 이벤트 검색
2. 최종 레지스트리에 중복 ID = 0 확인
```

#### AC-008: 형식 위반 거부

**Given:** 형식을 위반하는 ID가 생성되려고 할 때
**When:** 형식 검증을 수행하면
**Then:**
- 형식 위반 ID는 거부됨
- 위반 상세 내용이 로그에 기록됨
- 올바른 형식 가이드가 제공됨

**검증 방법:**
```
1. 레지스트리의 모든 ID가 형식 패턴과 일치 확인
2. 형식 위반 거부 로그 존재 확인 (있는 경우)
```

---

### 2.4 REQ-L2-004: ID 유효성 검증

#### AC-009: 검증 보고서 생성

**Given:** ID 할당이 완료되었을 때
**When:** "Validate IDs in all" 명령을 실행하면
**Then:**
- validation-report.json이 생성됨
- 총 ID 수, 유효 ID 수, 무효 ID 수가 포함됨
- 무효 ID에 대한 상세 사유가 기록됨

**검증 방법:**
```
1. validation-report.json 존재 확인
2. 유효 ID 비율 >= 95% 확인
3. 무효 ID 목록 및 사유 확인
```

---

### 2.5 REQ-L2-005: 정규화 파이프라인

#### AC-010: 내용 표준화

**Given:** 원본 요구사항 내용이 주어질 때
**When:** 내용 정규화를 적용하면
**Then:**
- 앞뒤 공백이 제거됨
- 내부 공백이 단일 공백으로 정규화됨
- 문장이 마침표로 종료됨
- 기술 용어가 보존됨

**검증 방법:**
```
1. 정규화 전후 샘플 비교
2. 공백 패턴 검증
3. 기술 용어 보존 확인
```

#### AC-011: 용어 정규화

**Given:** "should" 또는 "may"가 포함된 요구사항이 있을 때
**When:** 용어 정규화를 적용하면
**Then:**
- "should" -> "shall" 변환, priority:medium 태그 추가
- "may" -> "can" 변환, classification:optional 태그 추가
- "must", "shall"은 변경 없이 유지

**검증 방법:**
```
1. 정규화 후 "should" 포함 요구사항 = 0
2. priority:medium 태그가 적절히 추가됨 확인
```

#### AC-012: 속성 매핑

**Given:** extraction_type이 지정된 요구사항이 있을 때
**When:** 속성 매핑을 적용하면
**Then:**
- doxygen -> source_category:documentation
- assertion -> classification:safety
- state_machine -> tags:["state-machine", "behavior"]
- config -> type:CFG

**검증 방법:**
```
1. 각 extraction_type별 속성 매핑 검증
2. 매핑 일관성 100% 확인
```

---

### 2.6 REQ-L2-006: 중복 제거 엔진

#### AC-013: 정확 일치 탐지

**Given:** 동일한 내용의 요구사항이 여러 개 있을 때
**When:** 중복 탐지 Phase 1을 실행하면
**Then:**
- 동일 해시값을 가진 요구사항이 그룹화됨
- 중복 그룹이 deduplication-log.json에 기록됨

**검증 방법:**
```
1. 샘플 중복 요구사항으로 테스트
2. 해시 기반 그룹화 확인
```

#### AC-014: 의미적 유사도 탐지

**Given:** 유사한 내용의 요구사항이 있을 때
**When:** 중복 탐지 Phase 2를 실행하면
**Then:**
- Jaccard 유사도 > 0.7인 쌍이 플래그됨
- 잠재적 중복 목록이 생성됨

**검증 방법:**
```
1. 알려진 유사 요구사항 쌍으로 테스트
2. 유사도 계산 정확도 확인
```

#### AC-015: 중복 병합

**Given:** 중복으로 식별된 요구사항 그룹이 있을 때
**When:** 병합을 수행하면
**Then:**
- 품질 점수가 가장 높은 요구사항이 주 요구사항으로 선택됨
- 모든 소스 정보가 집계됨
- 병합 기록이 생성됨
- 최종 중복 = 0

**검증 방법:**
```
1. 병합 후 중복 요구사항 수 = 0
2. sources 배열에 모든 원본 소스 포함 확인
```

---

### 2.7 REQ-L2-007: 분류 로직

#### AC-016: 유형 분류

**Given:** 정규화된 요구사항이 있을 때
**When:** 유형 분류를 적용하면
**Then:**
- 각 요구사항에 functional, safety, interface, constraint 중 하나가 할당됨
- safety 분류는 안전 관련 키워드 포함 시 적용
- interface 분류는 통신/API 관련 시 적용

**검증 방법:**
```
1. 분류 결과 분포 확인
2. 샘플 요구사항 분류 정확도 검증
```

#### AC-017: 우선순위 분류

**Given:** 정규화된 요구사항이 있을 때
**When:** 우선순위 분류를 적용하면
**Then:**
- 각 요구사항에 critical, high, medium, low 중 하나가 할당됨
- safety 분류 요구사항은 critical 또는 high
- 구성 파라미터는 medium 이하

**검증 방법:**
```
1. 우선순위 분포 확인
2. safety 요구사항의 critical/high 비율 확인
```

---

### 2.8 REQ-L2-008: 품질 메트릭 계산

#### AC-018: 품질 점수 계산

**Given:** 정규화된 요구사항이 있을 때
**When:** 품질 점수를 계산하면
**Then:**
- 점수 범위: 0-100
- 완전성 (25점), 명확성 (25점), 테스트 가능성 (25점), 원자성 (25점)
- 각 감점 사유가 quality_issues 배열에 기록됨

**검증 방법:**
```
1. 점수 계산 로직 검증
2. 감점 사유와 점수 차감 일치 확인
```

#### AC-019: 품질 임계값 적용

**Given:** 품질 점수가 30점 미만인 요구사항이 있을 때
**When:** 정규화 파이프라인을 통과시키면
**Then:**
- 해당 요구사항은 플래그됨
- 품질 개선 제안이 생성됨
- 처리가 차단되고 보고됨

**검증 방법:**
```
1. 30점 미만 요구사항 플래그 확인
2. 품질 개선 제안 존재 확인
```

---

### 2.9 REQ-L2-009: 에이전트 실행 순서

#### AC-020: 실행 순서 보장

**Given:** L2 Phase를 실행할 때
**When:** 에이전트 실행 순서를 확인하면
**Then:**
- parvis-aispec-reqid가 먼저 완료됨
- ID 할당 완료 후 parvis-aispec-transformer 실행
- 실행 순서가 로그에 기록됨

**검증 방법:**
```
1. transformation-audit.json 타임스탬프 확인
2. ID 할당 로그 타임스탬프 < 정규화 로그 타임스탬프
```

---

### 2.10 REQ-L2-010: L2 품질 게이트

#### AC-021: QG-L2-001 (High Confidence 비율)

**Given:** 정규화가 완료되었을 때
**When:** High Confidence 비율을 계산하면
**Then:** High Confidence 비율 >= 75%

**검증 방법:**
```
High Confidence Count / Total Count >= 0.75
```

#### AC-022: QG-L2-002 (모듈 커버리지)

**Given:** 정규화가 완료되었을 때
**When:** 모듈 커버리지를 계산하면
**Then:** 12개 모듈 중 9개 이상에 요구사항 존재 (75%)

**검증 방법:**
```
Modules with Requirements / Total Modules >= 0.75
```

#### AC-023: QG-L2-003 (ID 할당률)

**Given:** ID 할당이 완료되었을 때
**When:** ID 할당률을 계산하면
**Then:** ID 할당률 >= 95%

**검증 방법:**
```
Assigned IDs / Total Requirements >= 0.95
```

#### AC-024: QG-L2-004 (중복 제거)

**Given:** 중복 제거가 완료되었을 때
**When:** 잔여 중복을 확인하면
**Then:** 잔여 중복 = 0

**검증 방법:**
```
Remaining Duplicates = 0
```

#### AC-025: QG-L2-005 (품질 점수 평균)

**Given:** 품질 점수 계산이 완료되었을 때
**When:** 평균 품질 점수를 계산하면
**Then:** 평균 품질 점수 >= 50

**검증 방법:**
```
Sum(quality_scores) / Count(requirements) >= 50
```

---

## 3. Quality Gate Summary (품질 게이트 요약)

### 3.1 L2 품질 게이트 체크리스트

| 게이트 ID | 기준 | 목표값 | 수락 기준 ID |
|----------|------|--------|-------------|
| QG-L2-001 | High Confidence 비율 | >= 75% | AC-021 |
| QG-L2-002 | 모듈 커버리지 | >= 75% (9/12) | AC-022 |
| QG-L2-003 | ID 할당률 | >= 95% | AC-023 |
| QG-L2-004 | 중복 제거 완료 | = 0 | AC-024 |
| QG-L2-005 | 품질 점수 평균 | >= 50 | AC-025 |

### 3.2 L2 완료 기준

L2 Phase는 다음 조건이 모두 충족될 때 완료됩니다:

- [ ] 모든 품질 게이트 (QG-L2-001 ~ QG-L2-005) 통과
- [ ] id-registry.json 생성 및 검증 완료
- [ ] 12개 모듈별 normalized JSON 파일 생성
- [ ] master-normalized.json 생성
- [ ] l2-quality-report.md 생성
- [ ] deduplication-log.json 생성
- [ ] transformation-audit.json 생성
- [ ] 모든 수락 기준 (AC-001 ~ AC-025) 충족

---

## 4. Test Scenarios (테스트 시나리오)

### 4.1 ID 생성 테스트

**TS-001: 정상 ID 생성**
```
Given: SOA 모듈의 doxygen 추출 요구사항
When: ID 생성 실행
Then: FBMS-SWE-SOA-001 형식 ID 생성
```

**TS-002: 다중 요구사항 ID 생성**
```
Given: BAL 모듈의 10개 요구사항
When: 일괄 ID 생성 실행
Then: FBMS-SWE-BAL-001 ~ FBMS-SWE-BAL-010 생성
```

**TS-003: 충돌 시나리오**
```
Given: 이미 존재하는 FBMS-SWE-BMS-001
When: 동일 ID 생성 시도
Then: 충돌 오류 발생, FBMS-SWE-BMS-001.1 제안
```

### 4.2 정규화 테스트

**TS-004: 내용 정규화**
```
Given: "  The system should   provide  authentication  "
When: 내용 정규화 적용
Then: "The system shall provide authentication."
       + priority:medium 태그
```

**TS-005: 중복 탐지**
```
Given:
  - "System shall validate input parameters"
  - "System shall validate input parameters"
When: 중복 탐지 실행
Then: 2개 요구사항이 1개로 병합, sources에 2개 원본 기록
```

**TS-006: 품질 점수 계산**
```
Given: 완전한 필드, 명확한 내용, 측정 가능한 기준의 요구사항
When: 품질 점수 계산
Then: 점수 >= 80
```

### 4.3 품질 게이트 테스트

**TS-007: 품질 게이트 통과**
```
Given: L2 처리 완료된 요구사항 세트
When: 품질 게이트 검증 실행
Then: 5개 게이트 모두 PASS
```

**TS-008: 품질 게이트 실패**
```
Given: High Confidence 비율 70%인 요구사항 세트
When: QG-L2-001 검증
Then: FAIL, 상세 보고서 생성
```

---

## 5. Definition of Done (완료 정의)

### 5.1 L2 Phase Definition of Done

L2 Phase는 다음이 모두 완료되었을 때 "Done"으로 간주됩니다:

**산출물 체크리스트:**
- [ ] `.moai/bms/requirements/registry/id-registry.json` 생성
- [ ] `.moai/bms/requirements/registry/module-map.json` 생성
- [ ] `.moai/bms/requirements/registry/sequence-tracker.json` 생성
- [ ] `.moai/bms/requirements/normalized/*.json` (12개 모듈 파일) 생성
- [ ] `.moai/bms/requirements/normalized/master-normalized.json` 생성
- [ ] `.moai/bms/requirements/quality/l2-quality-report.md` 생성
- [ ] `.moai/bms/requirements/quality/deduplication-log.json` 생성
- [ ] `.moai/bms/requirements/quality/validation-report.json` 생성
- [ ] `.moai/bms/requirements/logs/transformation-audit.json` 생성
- [ ] `.moai/bms/requirements/logs/id-assignment-log.json` 생성
- [ ] `.moai/bms/quality/gates/l2-gate-report.json` 생성

**품질 체크리스트:**
- [ ] ID 할당률 >= 95%
- [ ] 중복 요구사항 = 0
- [ ] High Confidence 비율 >= 75%
- [ ] 모듈 커버리지 >= 75%
- [ ] 평균 품질 점수 >= 50

**검증 체크리스트:**
- [ ] 모든 수락 기준 (AC-001 ~ AC-025) 검증 완료
- [ ] 모든 품질 게이트 (QG-L2-001 ~ QG-L2-005) 통과
- [ ] l2-gate-report.json에 모든 게이트 PASS 기록

---

## 6. Version History

| 버전 | 날짜 | 변경 내용 |
|-----|------|----------|
| 1.0.0 | 2025-12-16 | 초기 버전 |
