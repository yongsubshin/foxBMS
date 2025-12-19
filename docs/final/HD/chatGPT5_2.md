# 전기차 BMS 진단(Diagnostic, 回路Diag) 설계 정리

## 1. 목적

본 문서는 **전기차용 BMS(Battery Management System)** 개발을 위해 필요한  
**진단(Diagnostic, 일본 현업 표현: 回路Diag)** 항목을 체계적으로 정리한 것이다.

- 차량 탑재형 BMS (BCU–CMU–VCU 구조) 기준
- 회로 기반 진단 → SW 진단 로직 → Fail-safe까지 연결
- AUTOSAR / ISO 26262 / UN R100 / ASPICE 대응 가능 수준

---

## 2. BMS 시스템 구성 및 진단 대상 범위

### 2.1 시스템 구성

- **BCU (Battery Control Unit)**  
  - 배터리 팩 전체 제어
  - 진단 로직의 중심

- **CMU (Cell Monitoring Unit)**  
  - 셀 전압/온도 측정
  - BCU와 내부 통신

- **VCU (Vehicle Control Unit)**  
  - 차량 구동/충전 제어
  - BMS와 CAN 통신

### 2.2 진단 범위 요약

- 셀 전압 / 전류 / 온도
- 전원 / 고전압 / 접촉기
- 내부 통신 (BCU–CMU)
- 외부 통신 (CAN)
- BMS 내부 전원 및 로직

---

## 3. 회로 기반 진단 항목 (回路Diag)

### 3.1 셀 전압 진단 (Cell Voltage Diagnostic)

| Failure Mode | 진단 내용 |
|--------------|----------|
| Cell Open | 셀 센싱선 단선 |
| Cell Short | 센싱선 단락 |
| Over Voltage | 셀 과전압 |
| Under Voltage | 셀 저전압 |
| Cell Imbalance | 셀 간 전압 편차 과다 |
| ADC Stuck | ADC 값 고착 |

---

### 3.2 전류 센서 진단 (Current Sensor Diagnostic)

| Failure Mode | 진단 내용 |
|--------------|----------|
| Sensor Open | 센서 단선 |
| Sensor Short | 센서 단락 |
| Over Current | 과전류 |
| Offset Drift | 오프셋 드리프트 |
| Range Error | 측정 범위 초과 |
| Plausibility Error | SOC/전류 불일치 |

---

### 3.3 온도 센서 진단 (Temperature Diagnostic)

| Failure Mode | 진단 내용 |
|--------------|----------|
| Sensor Open | 온도 센서 단선 |
| Sensor Short | 온도 센서 단락 |
| Over Temperature | 과온 |
| Under Temperature | 저온 |
| Plausibility Error | 인접 센서 비교 이상 |

---

### 3.4 전원 / 고전압 진단 (Power & HV Diagnostic)

| Failure Mode | 진단 내용 |
|--------------|----------|
| VBAT Over | 배터리 전원 과전압 |
| VBAT Under | 배터리 전원 저전압 |
| Isolation Fault | 절연 저항 저하 |
| HVIL Open | 고전압 인터록 개방 |
| Precharge Fail | 프리차지 실패 |
| Main Contactor Weld | 접촉기 용착 |
| Main Contactor Open Fail | 접촉기 미동작 |
| Fuse Blow | 메인 퓨즈 단선 |
| BMS Power Fail | BMS 내부 전원 이상 |

---

### 3.5 통신 진단 (Communication Diagnostic)

| Failure Mode | 진단 내용 |
|--------------|----------|
| CMU Timeout | BCU–CMU 통신 두절 |
| CMU CRC Error | 내부 통신 데이터 오류 |
| CAN Timeout | VCU 통신 타임아웃 |
| CAN Bus-Off | CAN 물리 계층 오류 |
| Alive Counter Fail | 메시지 정지 |

---

## 4. SW 진단 구현 (AUTOSAR / ASPICE 관점)

### 4.1 Diagnostic Traceability Matrix

| HW Failure Mode | SW Req ID | DEM Event | DTC | Fail-safe |
|-----------------|-----------|-----------|-----|-----------|
| Cell Over Voltage | SW-REQ-DIAG-01 | DEM_CELL_OV | P1A001 | Charge inhibit |
| Cell Under Voltage | SW-REQ-DIAG-02 | DEM_CELL_UV | P1A002 | Discharge limit |
| Current Sensor Fail | SW-REQ-DIAG-03 | DEM_CUR_FAIL | P1A010 | Torque limit |
| Temp Sensor Open | SW-REQ-DIAG-04 | DEM_TEMP_OC | P1A020 | Power derating |
| CAN Timeout | SW-REQ-DIAG-05 | DEM_CAN_TO | U0100 | Limp mode |

---

## 5. 표준 및 규격 대응

### 5.1 ISO 26262 (기능 안전)

- 과전압 / 과전류 / 절연 결함 / 접촉기 용착  
  → **ASIL C ~ ASIL D Safety Mechanism**
- HW 고장 → SW 진단 → Fail-safe 연결 필수

### 5.2 AUTOSAR

- DEM: 진단 이벤트 관리
- DCM: UDS 진단 서비스
- COM/NM: 통신 진단

### 5.3 ASPICE

- SWE.1: Diagnostic 요구사항 정의
- SWE.2: Diagnostic 설계
- SWE.4: Diagnostic 구현
- SWE.5: Diagnostic 시험

---

## 6. 일본 OEM 기준 권장 표현

### 슬라이드 / 제안서 문구

> **回路構成を考慮した  
> BMSソフトウェア故障診断設計  
> （セル電圧・電流・温度・電源・通信）**

또는

> **BMS 回路レベル診断（SW）**

---

## 7. 요약

- **回路Diag = 회로 기반 SW 진단 설계**
- BMS 진단은 안전의 핵심이며 설계 초기부터 구조화 필요
- AUTOSAR + ISO 26262 + ASPICE를 동시에 만족하도록 구성 가능
- 본 문서는 **실제 BMS 개발 기준선(Baseline)** 으로 활용 가능

