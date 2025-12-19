# EV BMS 진단 시스템 개발 종합 기술 가이드

전기차 배터리 관리 시스템(BMS)의 진단 체계는 **ISO 26262 기능안전**, **ISO 14229 UDS**, **ISO 15765 CAN 진단 프로토콜**을 기반으로 구축되며, AUTOSAR 아키텍처에서 DEM/DCM/FiM 모듈로 구현된다. 이 문서는 셀 전압/온도/전류 진단부터 절연저항 모니터링, DTC 관리, 회로 진단까지 BMS 진단의 전 영역을 실무 적용 관점에서 상세히 다룬다. **ASIL D** 등급의 안전 임계 기능(열 폭주 방지, 절연 고장 감지)부터 QM 등급의 SOC 추정까지 진단 커버리지 요구사항과 구현 방법을 포괄한다.

---

## 1. ISO 표준 기반 진단 체계

### ISO 26262 기능안전과 BMS ASIL 등급

BMS 기능은 위험 분석(HARA)을 통해 **심각도(Severity)**, **노출빈도(Exposure)**, **제어가능성(Controllability)**에 따라 ASIL 등급이 결정된다. 대부분의 BMS 핵심 기능은 **ASIL C~D** 등급을 요구하며, 이는 열 폭주나 감전 위험이 치명적 결과를 초래할 수 있기 때문이다.

| BMS 기능 | 일반 ASIL 등급 | 안전 목표 |
|---------|--------------|---------|
| 과전압/저전압 감지 | ASIL C-D | 과충전으로 인한 열 폭주 방지 |
| 과열 감지 | **ASIL D** | 열 폭주 및 화재 방지 |
| 절연 저항 모니터링 | **ASIL D** | 감전 위험 방지 |
| 과전류/단락 보호 | ASIL C-D | 열적 손상 및 화재 방지 |
| 컨택터 제어 | ASIL C-D | 안전한 전원 차단 보장 |
| SOC/SOH 추정 | QM~ASIL B | 정확한 주행거리 예측 |

**하드웨어 아키텍처 메트릭 요구사항:**

| 메트릭 | ASIL B | ASIL C | ASIL D |
|-------|--------|--------|--------|
| **SPFM** (단일점 고장 메트릭) | ≥90% | ≥97% | ≥99% |
| **LFM** (잠재 고장 메트릭) | ≥60% | ≥80% | ≥90% |
| **PMHF** (확률적 하드웨어 고장 메트릭) | <100 FIT | <100 FIT | <10 FIT |

**진단 커버리지(Diagnostic Coverage) 등급:**
- **Low DC (60%)**: 기본 모니터링
- **Medium DC (90%)**: 플로시빌리티 체크, 이중 센싱
- **High DC (99%)**: 듀얼 코어 락스텝, 종합 진단

**고장 허용 시간 간격(FTTI) 설계:**
```
FTTI = FDTI (고장 검출 시간) + FRTI (고장 반응 시간)

제약조건: 진단 테스트 주기 + 고장 반응 시간 ≤ FTTI

일반적인 BMS FTTI 값:
- 컨택터 개방: 50-100ms
- 과전류 보호: 10-50ms
- 과전압/저전압: 100-500ms
```

### ISO 14229 UDS 진단 서비스

BMS 진단에 적용되는 핵심 UDS 서비스는 다음과 같다:

| 서비스 ID | 서비스명 | BMS 적용 |
|----------|---------|---------|
| **0x10** | DiagnosticSessionControl | 세션 관리 (Default/Extended/Programming) |
| **0x14** | ClearDiagnosticInformation | DTC 삭제 |
| **0x19** | ReadDTCInformation | 저장된 고장코드 읽기 |
| **0x22** | ReadDataByIdentifier | 셀 전압, 온도, SOC 읽기 |
| **0x27** | SecurityAccess | 캘리브레이션/프로그래밍 잠금 해제 |
| **0x2E** | WriteDataByIdentifier | 캘리브레이션 데이터 쓰기 |
| **0x31** | RoutineControl | 셀 밸런싱, 자가진단 루틴 실행 |
| **0x3E** | TesterPresent | 세션 유지 |

**Service 0x19 주요 서브펑션:**

| 서브펑션 | 설명 |
|---------|------|
| 0x01 | DTC 개수 조회 (상태 마스크 기준) |
| 0x02 | DTC 목록 조회 (상태 마스크 기준) |
| 0x04 | Freeze Frame 데이터 조회 |
| 0x06 | Extended Data Record 조회 |
| 0x14 | Fault Detection Counter 조회 |

**BMS 전용 DID (Data Identifier) 예시:**

| DID | 설명 | 크기 |
|-----|------|-----|
| 0xFD01 | 배터리 팩 SOC | 1 byte (%) |
| 0xFD02 | 배터리 팩 SOH | 1 byte (%) |
| 0xFD10 | 셀 전압 배열 | N×2 bytes |
| 0xFD20 | 팩 전류 | 2 bytes (signed) |
| 0xFD30 | 온도 센서 배열 | N×1 bytes |

### ISO 15765 CAN 진단 통신

**ISO-TP 프레임 타입:**

| 타입 | PCI | 설명 |
|-----|-----|------|
| Single Frame (SF) | 0x0 | 페이로드 ≤7 bytes |
| First Frame (FF) | 0x1 | 멀티프레임 시작, 길이 포함 |
| Consecutive Frame (CF) | 0x2 | 연속 데이터 |
| Flow Control (FC) | 0x3 | 수신측 흐름 제어 |

**타이밍 파라미터:**

| 파라미터 | 설명 | 기본값 |
|---------|------|-------|
| N_As/N_Ar | CAN 프레임 전송 시간 | 1000ms |
| N_Bs | FF 후 FC 대기 시간 | 1000ms |
| N_Cr | CF 수신 대기 시간 | 1000ms |
| P2Server | 응답 시간 (기본 세션) | 50ms |
| P2*Server | 응답 시간 (확장) | 5000ms |

---

## 2. BMS 주요 진단 항목 상세

### 셀 전압 진단

**과전압(OV) 검출 임계값:**

| 셀 타입 | 경고 임계값 | 고장 임계값 |
|--------|-----------|-----------|
| NMC/NCA | 4.15V | 4.25V ±0.025V |
| LFP | 3.60V | 3.65V ±0.05V |

**저전압(UV) 검출 임계값:**

| 셀 타입 | 경고 임계값 | 방전 차단 |
|--------|-----------|----------|
| NMC/NCA | 2.8-3.0V | 2.5V |
| LFP | 2.5-2.8V | 2.0V |

**디바운싱 파라미터:**
- 보호 지연: 0.5~2초 (일반 1초)
- 카운터 기반: 연속 3-5회 임계값 초과
- 필터: 100-500ms 윈도우 이동 평균
- 히스테리시스: 검출 전압보다 50-150mV 높은 복귀 전압

**셀 전압 편차 진단:**
- 최대 델타 전압 (운행 중): 50-200mV
- 밸런싱 시작 임계값: 10-50mV 차이
- 경고 임계값: ΔV > 100mV
- 고장 임계값: ΔV > 300-500mV

**플로시빌리티 체크 구현:**
- Primary AFE IC 측정 + Secondary ADC 참조
- 인접 셀 간 교차 검증 (합산 = 팩 전압 ±0.5%)
- 셀 전압 측정 정확도: ±2-5mV

### 셀 온도 진단

**과열 검출 임계값:**

| 조건 | 경고 | 고장/차단 |
|-----|------|---------|
| 충전 중 | 40-45°C | 55-60°C |
| 방전 중 | 50-55°C | 60-65°C |
| 열 폭주 위험 | 60°C | >80°C (치명) |

**저온 검출 임계값:**

| 조건 | 경고 | 충전 금지 |
|-----|------|---------|
| 충전 | 0°C | -10°C ~ -20°C |
| 방전 | -10°C | -30°C ~ -40°C |

**NTC 센서 고장 검출:**

| 고장 유형 | 검출 방법 | 임계값 |
|---------|---------|-------|
| 단선 (Open) | 전압 = Vref (풀업) | R > 1MΩ (T < -60°C 등가) |
| 단락 (Short) | 전압 = 0V | R < 100Ω (T > 150°C 등가) |
| 범위 초과 | 온도 비정상 | < -40°C 또는 > 125°C |
| 고착 | 시간 경과 무변화 | 부하 변화에도 60초 이상 정적 |

**열 폭주 조기 경보:**
- 온도 상승률: >1-2°C/초 지속
- 온도 60°C 접근 + 가속
- 전압 강하 + 온도 상승 조합 (가스 발생 지표)
- 응답 시간: 검출 <1초, 즉시 컨택터 개방

### 절연 저항 진단

**UN ECE R100/ISO 6469 기준 임계값:**

| 조건 | 최소 요구사항 | 일반 배터리 목표 |
|-----|-------------|----------------|
| HV 시스템 (컨택터 닫힘) | >500Ω/V | >2,000kΩ |
| 배터리 팩 단독 | - | >1,500kΩ ~ >3,000kΩ |

**400V 시스템 예시:**
- 최소: 400V × 500Ω/V = **200kΩ**
- 일반 목표: **>1,500kΩ**
- 경고 임계값: 510kΩ
- 고장 임계값: 90kΩ

**측정 방법:**
1. **DC 주입법**: HV 버스와 샤시 간 알려진 전압 주입, 결과 전류 측정
2. **저항 네트워크법** (ECE R100 Annex 4):
   - V1 (HV-에서 샤시) 측정
   - V2 (HV+에서 샤시) 측정
   - 알려진 R0 삽입 후 V1' 또는 V2' 측정
   - 계산: Ri = R0 × (Vb/V1' - Vb/V1)

### SOC/SOH 진단

**SOC 추정 방법 비교:**

| 방법 | 정확도 | 제한사항 |
|-----|-------|---------|
| 쿨롱 카운팅 | ±2-5% | 시간 경과 드리프트, 전류 센서 의존 |
| OCV 룩업 | ±1-3% | 휴지 기간 필요 (>3시간) |
| 칼만 필터 (EKF/UKF) | ±1-2% | 계산 복잡도, 모델 정확도 의존 |
| 신경망/AI | <2% | 학습 데이터 의존 |

**불일치 검출:**
- 쿨롱 카운팅 vs OCV 방법 비교 (휴지 후)
- 허용 불일치: <5% SOC
- 고장 임계값: >10% SOC 불일치

**SOH 열화 모니터링 지표:**

| 지표 | 계산 | 경고 임계값 |
|-----|------|-----------|
| 용량 감소 | 현재 용량 / 초기 용량 | <80% |
| 내부 저항 증가 | 현재 R / 초기 R | >150-200% |
| 에너지 처리량 | 총 충방전 Wh | 제조사 지정 |
| 사이클 수 | 완전 등가 사이클 | >1000-2000 cycles |

### 전류 센서 진단

**센서 기술 비교:**

| 기술 | 정확도 | 범위 | 절연 |
|-----|-------|-----|-----|
| 션트 저항 | ±0.1-0.5% | 25-100µΩ (EV) | 외부 절연 필요 |
| 홀 센서 | ±0.5-2% | ~±2500A | 내장 절연 |
| 플럭스게이트 | ±0.1-0.5% | 고전류 | 내장 절연 |

**오프셋 드리프트 검출:**
- 휴지 시 전류 모니터링 (0A 이어야 함)
- 허용 오프셋 드리프트: ±0.5-1A
- 차량 키오프 시 오프셋 주기적 캘리브레이션

**과전류 검출 임계값:**

| 조건 | 경고 | 보호 (OCD) | 응답 시간 |
|-----|------|----------|---------|
| 충전 과전류 | >1.5C | >2C | 1-5초 |
| 방전 과전류 | >2C | >3-5C | 500ms-2초 |
| 단락 | N/A | >10C | 50-500µs |

### 통신 진단

**CAN 버스 고장 검출:**

| 고장 유형 | 검출 방법 | 임계값 |
|---------|---------|-------|
| Bus-Off | CAN 컨트롤러 에러 카운터 | TEC 또는 REC > 255 |
| 메시지 타임아웃 | 예상 메시지 누락 | 100-500ms |
| CRC/체크섬 오류 | 내장 CAN 오류 검출 | 오류 증가 |
| 메시지 카운터 오류 | 롤링 카운터 불일치 | 갭 > 1 |

**타임아웃 임계값:**
- 중요 메시지 (전압, 전류): 50-100ms
- 비중요 메시지 (SOC, SOH): 500ms-1초
- 하트비트/킵얼라이브: 100-200ms

---

## 3. 회로 진단 (Circuit Diagnostics)

### 셀 모니터링 IC (AFE) 진단

**주요 AFE IC 제조사 및 진단 기능:**

| 제조사 | 제품군 | 핵심 진단 기능 |
|-------|-------|---------------|
| **ADI** | LTC6813, ADBMS6830B | Open-wire 검출 (±100μA 전류원), 이중 내부 참조, MUX 셀프테스트 |
| **TI** | BQ769x0, BQ78350 | 14비트 ADC, 쿨롱 카운터, 내부 온도/외부 써미스터 모니터링 |
| **NXP** | MC33771C, FS26 | ASIL D SBC, 멀티플 레귤레이터, 아날로그 MUX 진단 |
| **Renesas** | ISL78600 | 배터리 OV/UV 검출, 오픈 라인 검출, 참조 전압 검증, **ASIL D 지원** |

**AFE 셀프진단 기능:**

| 진단 유형 | 검출 방법 | 임계값 | ISO 26262 분류 |
|---------|---------|-------|----------------|
| Open Wire 검출 | 전류원 주입 (±100μA) | CELLΔ < -400mV | SM (안전 메커니즘) |
| ADC 정확도 | 이중 참조 비교 | ±10mV 요구 | ASIL B-D |
| 참조 전압 | 보조 내부 참조 교차 체크 | ±0.1% 드리프트 | SM - 하드웨어 |
| MUX 테스트 | 알려진 참조로 셀프테스트 | Pass/Fail | SM - 하드웨어 |
| 워치독 | 통신 타임아웃 모니터링 | 2-30ms 타임아웃 | SM - HW/SW 결합 |

**Open Wire 검출 알고리즘 (ADI LTC6813 예시):**
```
1. ADOW 명령 실행 (PUP=1, +100μA) 2회
2. ADOW 명령 실행 (PUP=0, -100μA) 2회
3. 계산: CELLΔ[n] = CELLPU[n] - CELLPD[n]
4. 검출 기준:
   - CELLΔ[n+1] < -400mV → C(n) 단선
   - CELLPU[1] = 0V → C0 단선
   - CELLPD[18] = 0V → C18 단선
```

### 컨택터/릴레이 진단

**용착(Welding) 검출 방법 (TI TPSI2140-Q1 활용):**

절연 솔리드 스테이트 스위치와 전압 분배기를 사용하여 검출:
- 800V 배터리, 3.3V MCU 가정
- RDIV1 = 1MΩ, RDIV2 = 2kΩ
- 전압 분배기 공식: VA = V_PACK × (RDIV2 / (RDIV1 + RDIV2))

**검출 진리표:**

| 테스트 | SW1 | SW2 | 정상 예상 전압 | 용착 감지 시 |
|-------|-----|-----|--------------|-------------|
| SW1 용착 체크 | Open | - | VA = 0V | VA = 1.6V |
| SW1 개방 체크 | Closed | - | VA = 1.6V | VA = 0V |
| SW2 용착 체크 | Closed | Open | VA = 1.6V | VA = 0V |

**접촉 저항 모니터링:**
- 정상 접촉 저항: <100μΩ
- 열화 경고: 100-500μΩ
- 고장 임계값: >1mΩ

### 프리차지 회로 진단

**프리차지 시퀀스:**
1. 배터리 음극 컨택터 닫힘
2. 팩 분리 컨택터 닫힘 (해당시)
3. 프리차지 릴레이 닫힘
4. 배터리 양극 컨택터 닫힘
5. 프리차지 릴레이 열림

**진단 방법:**

| 고장 유형 | 검출 방법 | 임계값/기준 |
|---------|---------|-----------|
| 프리차지 저항 단선 | 프리차지 중 부하 버스 전압 모니터링 | 전압 상승 < 예상 기울기 |
| 프리차지 타임아웃 | 타이머 기반 모니터링 | 일반 2-5초 max |
| 커패시터 전압 상승 | dV/dt 모니터링 | V_bus가 타임아웃 내 V_pack의 90% 도달 |

**800V 시스템 설계값:**
- 프리차지 저항: 50-200Ω
- 프리차지 시정수: τ = R × C (목표 ~0.5-2초)
- DC 링크 커패시턴스: 100-500μF
- 성공 기준: 메인 컨택터 닫기 전 V_bus > 90% × V_pack

### 퓨즈 및 파이로퓨즈 진단

**파이로퓨즈 (Pyro-Fuse) 제조사:**
- Autoliv: PSS (최대 1000V)
- Eaton Bussmann: PDD5 시리즈 (20kA/900VDC)
- Daicel: 고속 차단 장치

**특성:**
- 응답 시간: <2ms (버스바 분리 <0.1ms)
- 트리거: BMS 신호, 에어백 제어 유닛, 충돌 센서
- 단일 사용, 비가역 동작

**진단 기능:**

| 체크 | 방법 | Tesla 구현 |
|-----|------|-----------|
| 회로 무결성 | 점화기 회로 루프 저항 체크 | BMS가 파이로 회로 연속성 모니터링 |
| 저항 테스트 | HV 접합부 Hioki 미터 측정 | 0.050-0.150mΩ 허용 범위 |

### HVIL (High Voltage Interlock Loop) 모니터링

**검출 방법:**

1. **정전류 방식 (Tesla):**
   - BMS가 정전류 (~20mA) 생성
   - 알려진 저항에 대한 전압 강하 측정
   - 정상: 0.02A × 240Ω = 4.8V
   - 편차 시 BMS_f008_HW_HVIL 고장 트리거

2. **PWM 신호 방식:**
   - 더 복잡하나 노이즈 내성 향상
   - 배터리 단락 및 접지 단락 고장 검출 가능

**고장 상태 검출:**

| 상태 | HVIL-Send | HVIL-Return | 진단 |
|-----|-----------|-------------|------|
| 정상 | 중간 범위 | 중간 범위 | 루프 정상 |
| 개방 연결 | High | Low | 커넥터 분리됨 |
| 배터리 단락 | High | High | 배선 고장 |
| 접지 단락 | Low | Low | 배선 고장 |

---

## 4. DTC 체계 및 Fault Memory 관리

### 표준 DTC 코드 구조

**5문자 영숫자 형식: XNNNN**

| 접두사 | 시스템 | 이진 인코딩 (Bit 7-6) |
|-------|-------|---------------------|
| **P** | 파워트레인 | 00 |
| **C** | 샤시 | 01 |
| **B** | 바디 | 10 |
| **U** | 네트워크/통신 | 11 |

**P코드 범위 (파워트레인 - BMS 관련):**

| 범위 | 설명 |
|-----|------|
| P0xxx | ISO/SAE 표준화 |
| P1xxx | 제조사 특정 |
| P2xxx | ISO/SAE 예약 |
| P0Axx | **하이브리드/EV 배터리 팩 전용** |

### 3-Byte DTC 구조 (ISO 14229-1 UDS)

```
| High Byte | Middle Byte | Low Byte (FTB) |
|-----------|-------------|----------------|
| 8 bits    | 8 bits      | 8 bits         |

High Byte 구조:
  Bit 7-6: DTC 타입 (00=P, 01=C, 10=B, 11=U)
  Bit 5-4: 첫 번째 자릿수 (0-3)
  Bit 3-0: 두 번째 자릿수 (0-F hex)

예: DTC P0650 → 0x06 0x50 <FTB>
```

**Failure Type Byte (FTB) 정의:**

| FTB High Nibble | 고장 카테고리 |
|-----------------|-------------|
| 0x0x | 일반/서브타입 없음 |
| 0x1x | 회로/신호 범위/성능 |
| 0x2x | 회로 Low 입력 |
| 0x3x | 회로 High 입력 |
| 0x4x | 회로 간헐적 |
| 0x7x | 하드웨어 문제 |
| 0xDx | 과온도 |
| 0xEx | 저온도 |

### BMS 전용 DTC 예시

**Orion BMS 표준 DTC:**

| DTC | Hex 코드 | 고장 설명 |
|-----|---------|---------|
| P0AFA | 0x0A 0xFA | 셀 전압 Low 고장 |
| P0A80 | 0x0A 0x80 | Weak Cell 고장 |
| P0A04 | 0x0A 0x04 | Open Wiring 고장 |
| P0AC0 | 0x0A 0xC0 | 전류 센서 고장 |
| P0AA6 | 0x0A 0xA6 | 고전압 절연 고장 |
| P0A9C | 0x0A 0x9C | 써미스터 고장 |
| U0100 | 0xC1 0x00 | CAN 버스 통신 고장 |

**현대/기아 EV BMS DTC (제조사 특정):**

| DTC | 설명 |
|-----|------|
| P1AA6 | 배터리 셀 전압 편차 |
| P1AA7 | 불량 절연 검출 |
| P1AA8 | 충전 후 비정상 셀 전압 |
| P1AAA | 과전압 조건 |
| P1AAB | 온도 편차 |

### Fault Memory 관리

**DTC 라이프사이클 상태:**

```
┌──────────┐    고장 검출     ┌──────────┐
│  No DTC  │ ───────────────→│ Pending  │
│  (Pass)  │                 │   DTC    │
└──────────┘                 └────┬─────┘
     ↑                            │
     │ Aging 완료                  │ N 드라이빙 사이클
     │ (40 운행 사이클)              │ 고장 지속
     │                            ↓
┌────┴─────┐    Healing 완료  ┌──────────┐
│  Aged    │ ←───────────────│Confirmed │
│   Out    │   (N 사이클 통과)   │   DTC    │
└──────────┘                 └────┬─────┘
                                  │
                                  │ 배출 관련
                                  ↓
                             ┌──────────┐
                             │Permanent │
                             │   DTC    │
                             └──────────┘
```

**상태별 정의:**

| 상태 | 트리거 | 목적 |
|-----|-------|-----|
| **Pending DTC** | 초기 고장 검출 (testFailed = 1) | 확정 전 임시 저장 |
| **Confirmed DTC** | N 연속 드라이빙 사이클 고장 지속 (보통 2) | 영구 고장 저장, MIL 점등 |
| **Permanent DTC** | 배출 관련 DTC만 해당 | ClearDiagnosticInformation으로 삭제 불가 |

**Aging 메커니즘:**
- 카운터 시작: DTC 확정 시 0
- 각 운행 사이클마다 테스트 완료 및 통과 시 증가
- 고장 재발생 시 0으로 리셋
- 임계값 (일반 40 사이클) 도달 시 DTC "aged out"

### DTC 상태 바이트 (8-bit)

```
Bit 7 │ Bit 6 │ Bit 5 │ Bit 4 │ Bit 3 │ Bit 2 │ Bit 1 │ Bit 0
──────┼───────┼───────┼───────┼───────┼───────┼───────┼──────
 WIR  │ TNCTO │ TFSLC │ TNCSL │  CDTC │ PDTC  │ TFTOC │  TF
```

| Bit | 약어 | 설명 |
|-----|-----|------|
| 0 | TF | testFailed - 현재 테스트 결과 실패 |
| 1 | TFTOC | testFailedThisOperationCycle - 현재 운행 사이클 중 실패 |
| 2 | PDTC | pendingDTC - 확정 대기 중 |
| 3 | CDTC | confirmedDTC - 장기 메모리 저장됨 |
| 4 | TNCSLC | testNotCompletedSinceLastClear - 마지막 클리어 이후 테스트 미완료 |
| 5 | TFSLC | testFailedSinceLastClear - 마지막 클리어 이후 실패 |
| 6 | TNCTOC | testNotCompletedThisOperationCycle - 현재 사이클 테스트 미완료 |
| 7 | WIR | warningIndicatorRequested - MIL/경고등 ON 요청 |

**상태 바이트 예시:**

| 값 | 의미 |
|---|------|
| 0x00 | 고장 없음, 모든 테스트 완료 |
| 0x04 | Pending DTC (확정 대기) |
| 0x08 | Confirmed DTC (저장됨) |
| 0x89 | Confirmed + WIR + testFailed (활성 확정 고장, MIL ON) |

---

## 5. AUTOSAR 기반 진단 소프트웨어 아키텍처

### 진단 스택 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│    (BMS SWCs: SoC 추정, 셀 밸런싱, 고장 관리)                   │
├─────────────────────────────────────────────────────────────┤
│                         RTE                                  │
├─────────────────────────────────────────────────────────────┤
│                   SERVICES LAYER                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   DEM    │ │   DCM    │ │   FiM    │ │   NvM    │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│              COMMUNICATION SERVICES                          │
│         (PduR, CanTp, ComM, Com, DoIP)                      │
└─────────────────────────────────────────────────────────────┘
```

### DEM (Diagnostic Event Manager)

**핵심 기능:**
- 이벤트 설정 및 관리
- 이벤트-DTC 매핑
- 이벤트 상태 처리
- 고장 메모리 관리

**주요 API:**

```c
// 이벤트 상태 보고
Std_ReturnType Dem_SetEventStatus(
    Dem_EventIdType EventId,
    Dem_EventStatusType EventStatus  // PASSED, FAILED, PREPASSED, PREFAILED
);

// 이벤트 상태 조회
Std_ReturnType Dem_GetEventStatus(
    Dem_EventIdType EventId,
    Dem_UdsStatusByteType* EventStatusByte
);

// Fault Detection Counter 조회
Std_ReturnType Dem_GetFaultDetectionCounter(
    Dem_EventIdType EventId,
    sint8* FaultDetectionCounter  // -128 ~ +127
);
```

**이벤트 조합 유형:**
- **DEM_EVCOMB_DISABLED**: 1 Event → 1 DTC
- **DEM_EVCOMB_ONSTORAGE**: 다수 이벤트가 단일 메모리 항목 공유
- **DEM_EVCOMB_ONRETRIEVAL**: 별도 항목, 테스터용 조합

### DCM (Diagnostic Communication Manager)

**서브모듈:**
- **DSL**: 세션/보안 관리, 타이밍
- **DSD**: 요청 검증, 라우팅
- **DSP**: 서비스 실행, 응답 조립

**세션 관리:**

| 세션 | Hex 값 | 접근 수준 |
|-----|-------|---------|
| Default | 0x01 | 읽기 전용 DTC |
| Programming | 0x02 | 플래시 프로그래밍 |
| Extended | 0x03 | 전체 진단 접근 |
| BMS Calibration | 0x40 (사용자 정의) | BMS 파라미터 조정 |

### FiM (Function Inhibition Manager)

**기능 억제 메커니즘:**

```
DEM → 이벤트 상태 → FiM → Permission 조회 → SW-C/BSW
```

**억제 마스크:**
- **LAST_FAILED**: 마지막 테스트 실패 시 억제
- **NOT_TESTED**: 아직 테스트되지 않은 경우 억제
- **TESTED_AND_FAILED**: 테스트됨 AND 실패 시 억제

**BMS 기능 억제 예시:**

| FID | 관련 이벤트 | 동작 |
|-----|-----------|------|
| FID_Charging | CellOverVoltage, CellOverTemp, IsolationFault | AC/DC 충전 컨택터 억제 |
| FID_Discharging | CellUnderVoltage, CellUnderTemp, OverCurrent | 메인 컨택터 개방, VCU 신호 |
| FID_CellBalancing | CellOverTemp, BalancingCircuitFault | 패시브/액티브 밸런싱 비활성화 |

### 디바운싱 전략

**카운터 기반 디바운싱:**

```xml
<DemDebounceCounterBasedClass>
  <DemDebounceCounterDecrementStepSize>1</DemDebounceCounterDecrementStepSize>
  <DemDebounceCounterIncrementStepSize>1</DemDebounceCounterIncrementStepSize>
  <DemDebounceCounterFailedThreshold>3</DemDebounceCounterFailedThreshold>
  <DemDebounceCounterPassedThreshold>-3</DemDebounceCounterPassedThreshold>
  <DemDebounceCounterJumpDown>true</DemDebounceCounterJumpDown>
  <DemDebounceCounterJumpDownValue>0</DemDebounceCounterJumpDownValue>
</DemDebounceCounterBasedClass>
```

**상태 머신:**
```
                 PREFAILED (Counter++)
     ┌────────────────────────────────────────┐
     │                                        ↓
[PASSED] ←──────── [QUALIFICATION] ──────→ [FAILED]
Counter=-3        Counter: -3 to +3        Counter=+3
     ↑                                        │
     └────────────────────────────────────────┘
                 PREPASSED (Counter--)
```

**시간 기반 디바운싱:**
- DemDebounceTimeFailedThreshold: 100ms (예)
- DemDebounceTimePassedThreshold: 200ms (예)

**BMS 디바운싱 파라미터 가이드라인:**

| 고장 유형 | 전략 | 실패 임계값 | 통과 임계값 | 근거 |
|---------|------|-----------|-----------|-----|
| 셀 과전압 | Counter | 3 cycles | -3 cycles | 빠른 검출, 노이즈 회피 |
| 셀 저전압 | Counter | 5 cycles | -3 cycles | 긴 확정, 빠른 복구 |
| 과온도 | Time | 500ms | 1000ms | 열질량으로 느린 변화 |
| 통신 손실 | Counter | 10 cycles | -3 cycles | 네트워크 노이즈 허용 |
| 절연 고장 | Time | 200ms | 500ms | 안전 임계, 빠른 검출 |

### NvM 통합

**DEM-NvM 블록 구조:**
```
NvM Block: Dem_NvData_PrimaryMemory
├── EventMemoryEntry_0
│   ├── DTC Number (3 bytes)
│   ├── Status Byte (1 byte)
│   ├── Occurrence Counter (2 bytes)
│   ├── Aging Counter (1 byte)
│   └── Freeze Frame Data (N bytes)
├── EventMemoryEntry_1
└── EventMemoryEntry_N
```

**저장 전략:**
- **Immediate Storage**: TestFailed/ConfirmedDTC 비트 설정 시 즉시 - 안전 임계 BMS 고장용
- **Shutdown Storage**: ECU 종료 시 저장 - 비임계 정보성 DTC용

---

## 6. 개발 프로세스 및 도구

### 진단 개발 워크플로우

```
[요구사항] → [시스템 설계] → [SW 구현] → [통합] → [검증]
     ↓           ↓              ↓          ↓         ↓
  DRS/ODX    AUTOSAR 설정    DCM/DEM 코딩   HIL/SIL   CANoe 테스트
CANdelaStudio DaVinci Cfg   MICROSAR BSW   dSPACE    진단 검증
```

### HIL (Hardware-in-the-Loop) 테스트

**주요 플랫폼:**
- **NI/DMC BMS Power-HIL**: 셀 에뮬레이션, 고장 주입, NI VeriStand
- **Chroma 8630**: Simulink 모델 임포트, NEDC/WLTP 드라이브 사이클, ISO 26262 고장 주입
- **Typhoon HIL**: IPG CarMaker 공동 시뮬레이션
- **dSPACE VHIL**: BMS SIL/HIL 검증용 가상 테스트 환경

**HIL 테스트 기능:**
- 셀 전압 시뮬레이션 (채널당 최대 5A source/sink)
- 온도 센서 에뮬레이션
- 고장 주입 유닛 (역극성, 단선, 단락)
- 절연 측정
- CAN/LIN 통신 통합

### EOL (End-of-Line) 진단 테스트

**표준 EOL 테스트 항목:**

| 테스트 카테고리 | 검증 항목 |
|--------------|---------|
| BMS 통신 | UDS 프로토콜 메시지, 펌웨어 버전 확인, CAN/LIN 응답 |
| 전압 | 팩 전압 매칭, 셀 전압 밸런스, HV 내전압 테스트 |
| 전류 | 충방전 펄스 테스트, 내부 저항 측정 |
| 온도 | 센서 공차 검증, 열 분포 |
| 안전 | 절연 저항, HV 인터록, 컨택터 동작 |

**EOL 테스트 플로우 (ISO 14229/15765):**
1. BMS 웨이크업 및 초기 통신
2. 소프트웨어 버전 검증 및 DTC 클리어
3. 전압/전류/온도 캘리브레이션 검증
4. 충방전 기능 테스트
5. 보호 기능 검증
6. 데이터 쓰기 및 MES 생산 로깅

### DRS (Diagnostic Requirements Specification) 작성 가이드

**문서 구조:**

```
1. 서론
   1.1 목적 및 범위
   1.2 문서 규약
   1.3 참조 (ISO 26262, ISO 14229, ISO 15765)

2. 시스템 개요
   2.1 BMS 아키텍처
   2.2 진단 인터페이스
   2.3 통신 프로토콜

3. 진단 요구사항
   3.1 DTC 요구사항 (고장 유형별)
   3.2 DID 요구사항
   3.3 루틴 제어 요구사항
   3.4 보안 접근 요구사항

4. 기능 안전 요구사항
   4.1 ASIL 분류
   4.2 안전 목표 추적성
   4.3 진단 커버리지 요구사항

5. 검증 기준
   5.1 테스트 방법
   5.2 합격/불합격 기준
```

**요구사항 ID 넘버링 스킴:**

형식: `[시스템]_[유형]_[카테고리]_[순번]`

예시:
- `BMS_DTC_OV_001` - BMS 과전압 DTC #1
- `BMS_DID_SOC_002` - BMS SOC DID #2
- `BMS_RTN_BAL_003` - BMS 셀 밸런싱 루틴 #3

### 개발 도구 권장

| 카테고리 | 권장 도구 |
|---------|---------|
| 진단 사양 | Vector CANdelaStudio, Star Diagnosis Author |
| AUTOSAR 설정 | Vector DaVinci, EB tresos, ETAS ISOLAR |
| HIL 테스트 | Chroma 8630, NI/DMC Power-HIL, dSPACE SCALEXIO |
| 진단 테스트 | Vector CANoe, Intrepid Vehicle Spy, ETAS INCA |
| ODX/PDX 편집 | Softing DTS, Vector CANdelaStudio |
| SIL 시뮬레이션 | MATLAB/Simulink, dSPACE VEOS |

---

## 7. OEM/Tier1 구현 사례 및 Best Practice

### 주요 구현 사례

**Tesla BMS 진단:**
- 마스터-슬레이브 토폴로지로 배터리 모듈 전반에 처리 분산
- 전압 차이 10mV 공차 내 유지, 열 제어 ±3°C
- 독점 도구 (Toolbox 2/3)를 통한 UDS 진단 접근
- 게이트웨이 잠금 해제 필요

**LG Energy Solution (2024년 12월):**
- Qualcomm Snapdragon Digital Chassis와 SoC 기반 BMS 진단 솔루션 출시
- 기존 BMS 대비 80배 향상된 컴퓨팅 파워
- 90%+ 검출률, ~1% 진단 오류율
- 서버 연결 없이 실시간 차량 내 분석
- 현대/기아 포함 글로벌 9개 OEM에 이미 배치

**CATL:**
- 3단계 BMS 아키텍처: CSC → SBMU → MBMU
- CAN 통신을 통한 분산 BMS 방식
- 무선 BMS 기능으로 배선 단순화
- 차량-클라우드 협업을 통한 종합 진단

### 일반적인 함정 및 교훈

| 함정 | 영향 | 완화 |
|-----|------|-----|
| 과도하게 타이트한 알람 임계값 | 높은 오탐률, 불필요한 종료 | 필터링 및 히스테리시스 사용; 필드 데이터로 검증 |
| 잘못된 센서 캘리브레이션 | SOC/SOH 추정 오류, 보호 실패 | 센서 로트별 캘리브레이션; 런타임 캘리브레이션 체크 구현 |
| 누락된 디바운스 로직 | 스퓨리어스 고장 트리거 | 고장 유형별 적절한 디바운스 시간 적용 |
| 센싱의 단일점 고장 | 완전한 진단 맹점 | 이중 센싱 또는 플로시빌리티 체크 구현 |

**오탐/미탐 감소 전략:**
- **센서 퓨전**: 고장 선언 전 다수 센서 교차 검증
- **칼만 필터링**: 전압/전류 측정에서 노이즈 필터
- **플로시빌리티 체크**: 계산값 vs 측정값 비교
- **고장 확정 카운터**: DTC 설정 전 다수 발생 요구

---

## 8. 미래 동향

### DoIP (Diagnostics over IP)

**ISO 13400 구현:**
- 100 Mbps 대역폭 (CAN 500 kbps 대비)
- 신뢰성 있는 진단 메시지 전송을 위한 TCP/IP
- 검색 및 차량 식별을 위한 UDP

**BMS 이점:**
- 대용량 BMS 소프트웨어의 빠른 펌웨어 업데이트
- 텔레매틱스 게이트웨이를 통한 원격 진단 기능
- 멀티셀 데이터 검색을 위한 높은 처리량

### 클라우드 연결 진단

**플랫폼 기능:**
- **Sibros Deep Updater**: ISO 26262 ASIL-D 안전 인증 OTA 업데이트
- **Excelfore eSync/eDatX**: 실제 데이터 집계, 폐루프 개선
- **AutoPi Cloud**: 플릿 전반 OTA 및 진단 관리

**핵심 기능:**
- 실시간 플릿 건강 모니터링
- 예측 유지보수 알림
- 델타 업데이트 (변경된 바이트만 전송)
- 자동 롤백 기능의 단계별 롤아웃

### AI/ML 기반 예측 진단

**SOH 예측 방법:**

| 방법 | 적용 | 정확도 |
|-----|------|-------|
| 가우시안 프로세스 회귀 | 불확실성 정량화 | 적절한 학습으로 높음 |
| LSTM 신경망 | 시간적 열화 패턴 | 시퀀스 데이터에 우수 |
| Random Forest | 특성 기반 SOH 추정 | R² > 0.99 달성 가능 |
| XGBoost | 생산 준비 배포 | RMSE ~1.575% |

**ML을 위한 건강 지표:**
- 용량 감소 추적
- 내부 저항 증가
- 드라이브 사이클 중 전력 자기상관
- 전압 이완 거동
- 온도 분포 패턴

**구현 고려사항:**
- Raspberry Pi 4B에서 28-49ms 추론 시간 (엣지 배포 가능)
- 물리 정보 특성이 일반화 향상
- 안전 적용을 위한 불확실성 정량화 필수
- 다양한 운전 조건에서의 학습 데이터 필요

---

## 부록: BMS 진단 구성 종합 표

### 이벤트 구성 테이블

| 이벤트명 | DTC | FID 링크 | 디바운스 | 저장 |
|---------|-----|----------|---------|-----|
| Cell_OverVoltage | P0A80_12 | FID_Charging | Counter(3/-3) | Immediate |
| Cell_UnderVoltage | P0A80_14 | FID_Discharging | Counter(5/-3) | Immediate |
| Cell_OverTemp | P0A1F_11 | FID_Charging, FID_Discharge | Time(500ms) | Immediate |
| Cell_UnderTemp | P0A1F_12 | FID_Charging | Time(1s) | Shutdown |
| Pack_OverCurrent | P0A7D_00 | FID_Discharging | Counter(2/-2) | Immediate |
| Isolation_Fault | P0AA6_00 | FID_All | Time(200ms) | Immediate |
| CAN_Timeout | U0100_00 | FID_Estimation | Counter(10/-3) | Shutdown |

### DTC 우선순위 및 심각도 매핑

| 우선순위 | DTC 예시 | 이유 | ASIL |
|---------|---------|-----|------|
| 1 (최고) | P0AA6 - 절연 고장 | 안전 위험 | D |
| 2 | P0A08 - 컨택터 고장 | 안전 작동 불가 | D |
| 3 | P0AFA - 셀 저전압 | 배터리 손상 위험 | C |
| 4 | P0A80 - Weak Cell | 성능 저하 | B |
| 5 (최저) | P0A81 - 팬 모니터 | 유지보수 필요 | QM |

---

## 핵심 표준 참조

| 표준 | 설명 |
|-----|------|
| **ISO 26262:2018** | 도로 차량 — 기능 안전 |
| **ISO 14229-1:2020** | UDS Part 1: 애플리케이션 레이어 |
| **ISO 15765** | CAN 통한 진단 통신 |
| **ISO 13400** | DoIP 프로토콜 |
| **ISO 22901** | ODX 데이터 교환 형식 |
| **ISO/SAE 21434:2021** | 도로 차량 — 사이버보안 엔지니어링 |
| **AUTOSAR 4.x** | Diagnostic Extract Template (DEXT) 사양 |

이 기술 문서는 EV BMS 진단 시스템 개발을 위한 종합적인 참조 자료로, ISO 표준 준수부터 실무 구현 가이드까지 개발 전 과정을 지원한다. 셀 레벨 진단, 회로 진단, AUTOSAR 아키텍처, DTC 관리의 모든 측면을 포괄하며, OEM/Tier1의 실제 구현 사례와 미래 기술 동향까지 포함하여 차세대 BMS 개발에 활용할 수 있다.