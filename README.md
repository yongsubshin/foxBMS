# foxBMS + PARVIS AI 시스템

**AI 기반 문서화 및 검증을 통한 전문가급 BMS 개발**

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-ASIL--D-orange.svg)]()
[![ASPICE](https://img.shields.io/badge/ASPICE-Level%202-yellow.svg)]()
[![MISRA C](https://img.shields.io/badge/MISRA%20C-99%25-green.svg)]()

---

## 빠른 시작

### 사전 요구사항

- Claude Code CLI 설치
- Python 3.8 이상
- foxBMS 2 툴체인 (하드웨어 빌드 시 필요, 선택사항)

### 기본 사용법

```bash
# 프로젝트에서 Claude Code 시작
cd /path/to/foxBMS
claude

# PARVIS V-Model 파이프라인 전체 실행
/parvis:run BMS

# 문서 포털 생성
/parvis:docs all
```

---

## 시스템 아키텍처

### PARVIS V-Model 파이프라인

```
              PARVIS V-Model 파이프라인 (BMS)
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │   L1 ──► L2 ──► L3 ──► L4 ◄──► R1 ◄── R2 ◄── R3   │
    │   요구   아키   설계  구현    단위  통합  검증     │
    │                                                     │
    └─────────────────────────────────────────────────────┘

    명령어 ──► 에이전트 ──► 스킬 ──► 산출물
```

---

## 명령어

| 명령어 | 설명 | 사용법 |
|--------|------|--------|
| `/parvis:run` | V-Model 파이프라인 실행 | `/parvis:run BMS` 또는 `/parvis:run all` |
| `/parvis:docs` | 문서 생성 | `/parvis:docs all` 또는 `/parvis:docs sphinx` |

---

## 에이전트 (22개)

### PARVIS 에이전트 분류

| 단계 | 에이전트 | 목적 |
|------|----------|------|
| **명세** | `aispec-code`, `aispec-transformer`, `aispec-reqid`, `aispec-trace`, `aispec-safety` | 요구사항 추출 및 분석 |
| **코딩** | `aicoder-misra`, `aicoder-refactor`, `aicoder-doxygen`, `aicoder-safety` | 코드 품질 및 규정 준수 |
| **검증** | `aiverify-unittest`, `aiverify-coverage`, `aiverify-integration`, `aiverify-safety`, `aiverify-report`, `aiverify-misra-report` | 테스트 및 검증 |
| **문서** | `aidoc-aspice`, `aidoc-trace`, `aidoc-change`, `aidoc-safety`, `aidoc-generator` | 작업 산출물 생성 |
| **조율** | `ai-orchestrator` | 파이프라인 조율 |

---

## 스킬

| 스킬 | 목적 |
|------|------|
| `parvis-code-templates` | foxBMS용 Jinja2 코드 생성 |
| `parvis-misra-patterns` | MISRA C:2012 준수 패턴 |
| `parvis-id-conventions` | foxBMS 요구사항 ID 명명 규칙 |
| `parvis-i18n-templates` | 다국어 템플릿 (ko/en/ja) |

---

## V-Model 파이프라인 상세

### 왼쪽 (명세 → 구현)

```
L1: 요구사항 분석
    └─► aispec-code (소스에서 추출)
    └─► aispec-transformer (정규화)
    └─► aispec-reqid (ID 할당)
    └─► aispec-safety (ASIL 분류)

L2: 아키텍처 설계
    └─► aispec-trace (추적성 매트릭스)

L3: 상세 설계
    └─► aicoder-doxygen (문서화)

L4: 구현
    └─► aicoder-misra (MISRA 준수)
    └─► aicoder-refactor (자동 교정)
    └─► aicoder-safety (안전 어노테이션)
```

### 오른쪽 (검증 → 검증)

```
R1: 단위 검증
    └─► aiverify-unittest (테스트 생성)
    └─► aiverify-coverage (커버리지 분석)

R2: 통합 검증
    └─► aiverify-integration (인터페이스 테스트)

R3: 적격성 테스트
    └─► aiverify-safety (안전 검증)
    └─► aiverify-misra-report (개선 전/후 비교)

R4: 검증
    └─► aiverify-report (종합 보고서)
```

### 문서 생성

```
aidoc-aspice ─────► ASPICE 작업 산출물
aidoc-trace ──────► 추적성 보고서
aidoc-safety ─────► 안전 문서
aidoc-generator ──► HTML 포털, Sphinx, Doxygen
```

---

## 프로젝트 구조

```
foxBMS/
├── .claude/
│   ├── agents/parvis/      # PARVIS 에이전트 (22개)
│   ├── commands/parvis/    # /parvis:* 명령어
│   └── skills/parvis-*/    # PARVIS 스킬
├── .moai/bms/              # BMS 설정
│   ├── config/             # 오케스트레이터 설정
│   ├── extracted/          # 추출된 요구사항
│   └── normalized/         # 정규화된 데이터
├── docs/
│   ├── final/              # 생성된 HTML 포털
│   └── parvis/             # PARVIS 문서
├── foxbms-2/               # foxBMS 2 소스 (서브모듈)
└── guide/                  # 참조 가이드
```

---

## 주요 지표

| 지표 | 결과 |
|------|------|
| 소프트웨어 요구사항 | 648개 (7개 모듈 통합) |
| 안전 요구사항 | 147개 (ASIL 분류 완료) |
| 테스트 케이스 | 570개 |
| MISRA C:2012 준수율 | ~99% |
| 추적성 커버리지 | 100% 양방향 |

---

## 문서 포털

생성된 문서 접근:

```
docs/final/html/index.html
```

**포털 내용:**
- 모듈별 요구사항
- MISRA 준수 보고서 (개선 전/후)
- 추적성 매트릭스
- V-Model 상태 대시보드
- ASPICE 작업 산출물

---

## 라이선스

- **소프트웨어**: BSD 3-Clause License
- **하드웨어 및 문서**: CC-BY-4.0

---

## 링크

- [foxBMS 공식 사이트](https://foxbms.org)
- [foxBMS 2 문서](https://iisb-foxbms.iisb.fraunhofer.de/foxbms/gen2/docs/html/latest/)
- [GitHub 저장소](https://github.com/yongsubshin/foxBMS)

---

**PARVIS** - AI 기반 요구사항 및 검증 통합 시스템
