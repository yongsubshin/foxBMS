/**
 * Diagnostic Comparison Data Structure
 * foxBMS vs HD/KIA OEM BMS Diagnostics
 *
 * Complete mapping of all 85 foxBMS DIAG_IDs with OEM DTC equivalents
 * Data extracted from:
 * - foxbms-2/src/app/engine/config/diag_cfg.h (85 DIAG_IDs)
 * - KIA EV6(CV) 2024 BMS DTC List
 * - Hyundai IONIQ 5 NE EV Battery 2024 DTC
 * - Hyundai IONIQ 6 CE EV Battery 2024 DTC
 *
 * Last Updated: 2025-12-19
 * Version: 2.0.0 (Complete 85 DIAG_IDs)
 */

const DIAGNOSTIC_COMPARISON = {
    // Metadata
    meta: {
        foxbmsVersion: "v1.10.0",
        lastUpdated: "2025-12-19",
        totalCategories: 10,
        totalFoxbmsFeatures: 85,
        oemBrands: ["Hyundai", "KIA"]
    },

    // Diagnostic Categories
    categories: [
        {
            id: "voltage",
            name: {
                en: "Voltage Diagnostics",
                ko: "전압 진단",
                ja: "電圧診断"
            },
            icon: "fa-bolt",
            foxbms: [
                {
                    id: "DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MSL",
                    name: "Cell Overvoltage (MSL)",
                    nameKo: "셀 과전압 (MSL)",
                    nameJa: "セル過電圧 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0DE700"]
                },
                {
                    id: "DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_RSL",
                    name: "Cell Overvoltage (RSL)",
                    nameKo: "셀 과전압 (RSL)",
                    nameJa: "セル過電圧 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CELL_VOLTAGE_OVERVOLTAGE_MOL",
                    name: "Cell Overvoltage (MOL)",
                    nameKo: "셀 과전압 (MOL)",
                    nameJa: "セル過電圧 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_MSL",
                    name: "Cell Undervoltage (MSL)",
                    nameKo: "셀 저전압 (MSL)",
                    nameJa: "セル低電圧 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0DE600"]
                },
                {
                    id: "DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_RSL",
                    name: "Cell Undervoltage (RSL)",
                    nameKo: "셀 저전압 (RSL)",
                    nameJa: "セル低電圧 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CELL_VOLTAGE_UNDERVOLTAGE_MOL",
                    name: "Cell Undervoltage (MOL)",
                    nameKo: "셀 저전압 (MOL)",
                    nameJa: "セル低電圧 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_DEEP_DISCHARGE_DETECTED",
                    name: "Deep Discharge Detected",
                    nameKo: "과방전 감지",
                    nameJa: "過放電検出",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PLAUSIBILITY_PACK_VOLTAGE",
                    name: "Pack Voltage Plausibility",
                    nameKo: "팩 전압 정합성",
                    nameJa: "パック電圧妥当性",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PLAUSIBILITY_CELL_VOLTAGE",
                    name: "Cell Voltage Plausibility (Redundancy)",
                    nameKo: "셀 전압 정합성 (이중화)",
                    nameJa: "セル電圧妥当性 (冗長性)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PLAUSIBILITY_CELL_VOLTAGE_SPREAD",
                    name: "Cell Voltage Spread Plausibility",
                    nameKo: "셀 전압 편차 정합성",
                    nameJa: "セル電圧偏差妥当性",
                    severity: "warning",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B9600", "P1AA700"]
                },
                {
                    id: "DIAG_ID_AFE_CELL_VOLTAGE_MEAS_ERROR",
                    name: "AFE Cell Voltage Measurement Error",
                    nameKo: "AFE 셀 전압 측정 에러",
                    nameJa: "AFEセル電圧測定エラー",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0B3B00", "P0B4000", "P0B4500", "P0B4A00", "P0B4F00", "P0B5400", "P0B5900", "P0B5E00", "P0B6300", "P0B6800", "P0B6D00", "P0B7200", "P0B7700", "P0B7C00", "P0B8100", "P0B8600"]
                }
            ],
            oemOnly: [
                {
                    id: "voltage_sensing_unit",
                    name: "Voltage Sensing Unit Error",
                    nameKo: "전압센싱부 이상",
                    nameJa: "電圧センシング部異常",
                    oemCodes: ["P0B3B00", "P0B3B01", "P0B3F00", "P0B4000", "P0B4001", "P0B4400", "P0B4500", "P0B4501", "P0B4900", "P0B4A00", "P0B4A01", "P0B4F00", "P0B4F01", "P0B5400", "P0B5401", "P0B5900", "P0B5901", "P0B5E00", "P0B5E01", "P0B6300", "P0B6301", "P0B6800", "P0B6801", "P0B6D00", "P0B6D01", "P0B7200", "P0B7201", "P0B7700", "P0B7701", "P0B7C00", "P0B7C01", "P0B8100", "P0B8101", "P0B8600", "P0B8601"],
                    description: "Individual cell voltage sensing circuit diagnostics (1-16)",
                    descriptionKo: "개별 셀 전압센싱 회로 진단 (1-16번)",
                    descriptionJa: "個別セル電圧センシング回路診断 (1-16番)"
                },
                {
                    id: "module_voltage_sensing",
                    name: "Module Voltage Sensing Unit Error",
                    nameKo: "모듈 전압센싱부 이상",
                    nameJa: "モジュール電圧センシング部異常",
                    oemCodes: ["P0B3600"],
                    description: "Battery module voltage sensing unit diagnostics",
                    descriptionKo: "배터리 모듈 전압센싱부 진단",
                    descriptionJa: "バッテリーモジュール電圧センシング部診断"
                },
                {
                    id: "cell_voltage_deviation",
                    name: "Cell Voltage Deviation",
                    nameKo: "셀 전압 편차",
                    nameJa: "セル電圧偏差",
                    oemCodes: ["P1B9600", "P1AA700", "P189600", "P1B8600"],
                    description: "Detection of abnormal voltage difference between cells",
                    descriptionKo: "셀 간 비정상적인 전압 차이 감지",
                    descriptionJa: "セル間異常電圧差検出"
                },
                {
                    id: "voltage_rationality",
                    name: "Cell Voltage Rationality Diagnosis",
                    nameKo: "셀전압 측정 Rationality 진단",
                    nameJa: "セル電圧測定妥当性診断",
                    oemCodes: ["P1B9800"],
                    description: "Cell voltage measurement rationality check",
                    descriptionKo: "셀 전압 측정 합리성 체크",
                    descriptionJa: "セル電圧測定合理性チェック"
                }
            ]
        },
        {
            id: "temperature",
            name: {
                en: "Temperature Diagnostics",
                ko: "온도 진단",
                ja: "温度診断"
            },
            icon: "fa-thermometer-half",
            foxbms: [
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_MSL",
                    name: "Overtemperature Charge (MSL)",
                    nameKo: "충전 중 과온 (MSL)",
                    nameJa: "充電中過温 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0A7E00", "P1AAB00"]
                },
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_RSL",
                    name: "Overtemperature Charge (RSL)",
                    nameKo: "충전 중 과온 (RSL)",
                    nameJa: "充電中過温 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_CHARGE_MOL",
                    name: "Overtemperature Charge (MOL)",
                    nameKo: "충전 중 과온 (MOL)",
                    nameJa: "充電中過温 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_DISCHARGE_MSL",
                    name: "Overtemperature Discharge (MSL)",
                    nameKo: "방전 중 과온 (MSL)",
                    nameJa: "放電中過温 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0A7E00", "P1AAB00"]
                },
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_DISCHARGE_RSL",
                    name: "Overtemperature Discharge (RSL)",
                    nameKo: "방전 중 과온 (RSL)",
                    nameJa: "放電中過温 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_OVERTEMPERATURE_DISCHARGE_MOL",
                    name: "Overtemperature Discharge (MOL)",
                    nameKo: "방전 중 과온 (MOL)",
                    nameJa: "放電中過温 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_CHARGE_MSL",
                    name: "Undertemperature Charge (MSL)",
                    nameKo: "충전 중 저온 (MSL)",
                    nameJa: "充電中低温 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_CHARGE_RSL",
                    name: "Undertemperature Charge (RSL)",
                    nameKo: "충전 중 저온 (RSL)",
                    nameJa: "充電中低温 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_CHARGE_MOL",
                    name: "Undertemperature Charge (MOL)",
                    nameKo: "충전 중 저온 (MOL)",
                    nameJa: "充電中低温 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_DISCHARGE_MSL",
                    name: "Undertemperature Discharge (MSL)",
                    nameKo: "방전 중 저온 (MSL)",
                    nameJa: "放電中低温 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_DISCHARGE_RSL",
                    name: "Undertemperature Discharge (RSL)",
                    nameKo: "방전 중 저온 (RSL)",
                    nameJa: "放電中低温 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_TEMP_UNDERTEMPERATURE_DISCHARGE_MOL",
                    name: "Undertemperature Discharge (MOL)",
                    nameKo: "방전 중 저온 (MOL)",
                    nameJa: "放電中低温 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PLAUSIBILITY_CELL_TEMP",
                    name: "Cell Temperature Plausibility (Redundancy)",
                    nameKo: "셀 온도 정합성 (이중화)",
                    nameJa: "セル温度妥当性 (冗長性)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PLAUSIBILITY_CELL_TEMPERATURE_SPREAD",
                    name: "Cell Temperature Spread Plausibility",
                    nameKo: "셀 온도 편차 정합성",
                    nameJa: "セル温度偏差妥当性",
                    severity: "warning",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B9700", "P1AAE00"]
                },
                {
                    id: "DIAG_ID_AFE_CELL_TEMPERATURE_MEAS_ERROR",
                    name: "AFE Cell Temperature Measurement Error",
                    nameKo: "AFE 셀 온도 측정 에러",
                    nameJa: "AFEセル温度測定エラー",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0A9B11", "P0A9B12", "P0AC511", "P0AC512", "P0ACA11", "P0ACA12", "P0AE811", "P0AE812", "P0BC211", "P0BC212", "P0C3311", "P0C3312", "P0C7C11", "P0C7C12", "P0C8111", "P0C8112"]
                }
            ],
            oemOnly: [
                {
                    id: "temperature_sensors_1_16",
                    name: "Temperature Sensor Errors (1-16)",
                    nameKo: "온도센서 이상 (1-16번)",
                    nameJa: "温度センサー異常 (1-16番)",
                    oemCodes: ["P0A8511", "P0A8512", "P0A8D12", "P0A9B11", "P0A9B12", "P0A9E11", "P0A9E12", "P0AB611", "P0AB612", "P0AC511", "P0AC512", "P0ACA11", "P0ACA12", "P0AE811", "P0AE812", "P0BC211", "P0BC212", "P0C3311", "P0C3312", "P0C7C11", "P0C7C12", "P0C8111", "P0C8112", "P0C8811", "P0C8812", "P0C8D11", "P0C8D12", "P0C9211", "P0C9212", "P0C9711", "P0C9712", "P0CA811", "P0CA812", "P0CAD11", "P0CAD12", "P0CB211", "P0CB212", "P0CB711", "P0CB712"],
                    description: "Individual temperature sensor circuit diagnostics (1-16)",
                    descriptionKo: "개별 온도센서 회로 진단 (1-16번)",
                    descriptionJa: "個別温度センサー回路診断 (1-16番)"
                },
                {
                    id: "temperature_sensors_17_31",
                    name: "Temperature Sensor Errors (17-31)",
                    nameKo: "온도센서 이상 (17-31번)",
                    nameJa: "温度センサー異常 (17-31番)",
                    oemCodes: ["P1CBB11", "P1CBB12", "P1CBC12", "P1CBD11", "P1CBD12", "P1CBE11", "P1CBE12", "P1CBF11", "P1CBF12", "P1CC012", "P1CC111", "P1CC112", "P1CC212", "P1CC311", "P1CC312", "P1CC412", "P1CC511", "P1CC612", "P1CC711", "P1CC812", "P1CC911", "P1CCA12", "P2FE811", "P2FE812", "P2FE911", "P2FE912", "P2FEA11", "P2FEA12", "P2FEB11", "P2FEB12", "P2FEC11", "P2FEC12", "P2FED11", "P2FED12", "P2FEE11", "P2FEE12"],
                    description: "Extended temperature sensor circuit diagnostics (17-31)",
                    descriptionKo: "확장 온도센서 회로 진단 (17-31번)",
                    descriptionJa: "拡張温度センサー回路診断 (17-31番)"
                },
                {
                    id: "temperature_deviation",
                    name: "Temperature Deviation",
                    nameKo: "온도 편차",
                    nameJa: "温度偏差",
                    oemCodes: ["P1B9700", "P1AAE00", "P189700", "P1B8200", "P1B8300", "P1B8400", "P1B8500", "P1B8700", "P1B8800", "P1B8900", "P1B8A00"],
                    description: "Detection of abnormal temperature difference between sensors",
                    descriptionKo: "센서 간 비정상적인 온도 차이 감지",
                    descriptionJa: "センサー間異常温度差検出"
                },
                {
                    id: "heater_temp_sensor",
                    name: "Heater Temperature Sensor",
                    nameKo: "히터 온도센서",
                    nameJa: "ヒーター温度センサー",
                    oemCodes: ["P1B8000", "P1B8100", "P1B8011", "P1B8012"],
                    description: "Battery heater temperature sensor diagnostics",
                    descriptionKo: "배터리 히터 온도센서 진단",
                    descriptionJa: "バッテリーヒーター温度センサー診断"
                },
                {
                    id: "bottom_temp_sensor",
                    name: "Bottom Temperature Sensor",
                    nameKo: "하부 온도센서",
                    nameJa: "下部温度センサー",
                    oemCodes: ["P1BE511", "P1BE512", "P1BE612", "P1BE711", "P1BE712", "P1BE812", "P1BE911", "P1BEA12", "P1BEB11", "P1BEC12", "P1BEE11", "P1BEF12", "P1F5311", "P1F5412"],
                    description: "Battery pack bottom temperature monitoring (1-6)",
                    descriptionKo: "배터리팩 하부 온도 모니터링 (1-6번)",
                    descriptionJa: "バッテリーパック下部温度監視 (1-6番)"
                },
                {
                    id: "fast_charger_inlet_temp",
                    name: "Fast Charger Inlet Temperature Sensor",
                    nameKo: "급속충전기 인렛 온도센서",
                    nameJa: "急速充電器インレット温度センサー",
                    oemCodes: ["P0D9911", "P0D9912"],
                    description: "Fast charger inlet temperature sensor diagnostics",
                    descriptionKo: "급속충전기 인렛 온도센서 진단",
                    descriptionJa: "急速充電器インレット温度センサー診断"
                },
                {
                    id: "12v_battery_temp",
                    name: "12V Lithium Battery Temperature",
                    nameKo: "12V 리튬배터리 온도센서",
                    nameJa: "12Vリチウムバッテリー温度センサー",
                    oemCodes: ["P1BB300", "P1BB400", "P1BB500"],
                    description: "12V auxiliary lithium battery temperature monitoring",
                    descriptionKo: "12V 보조 리튬배터리 온도 모니터링",
                    descriptionJa: "12V補助リチウムバッテリー温度監視"
                },
                {
                    id: "battery_overheat_deterioration",
                    name: "Battery Overheat and Deterioration",
                    nameKo: "배터리 과열 및 열화",
                    nameJa: "バッテリー過熱および劣化",
                    oemCodes: ["P0A7E4B", "P0A7F00"],
                    description: "High voltage battery overheat and deterioration detection",
                    descriptionKo: "고전압 배터리 과열 및 열화 감지",
                    descriptionJa: "高電圧バッテリー過熱および劣化検出"
                }
            ]
        },
        {
            id: "current",
            name: {
                en: "Current Diagnostics",
                ko: "전류 진단",
                ja: "電流診断"
            },
            icon: "fa-exchange-alt",
            foxbms: [
                {
                    id: "DIAG_ID_OVERCURRENT_CHARGE_CELL_MSL",
                    name: "Cell-level Charge Overcurrent (MSL)",
                    nameKo: "셀 레벨 충전 과전류 (MSL)",
                    nameJa: "セルレベル充電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_OVERCURRENT_CHARGE_CELL_RSL",
                    name: "Cell-level Charge Overcurrent (RSL)",
                    nameKo: "셀 레벨 충전 과전류 (RSL)",
                    nameJa: "セルレベル充電過電流 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_OVERCURRENT_CHARGE_CELL_MOL",
                    name: "Cell-level Charge Overcurrent (MOL)",
                    nameKo: "셀 레벨 충전 과전류 (MOL)",
                    nameJa: "セルレベル充電過電流 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_OVERCURRENT_DISCHARGE_CELL_MSL",
                    name: "Cell-level Discharge Overcurrent (MSL)",
                    nameKo: "셀 레벨 방전 과전류 (MSL)",
                    nameJa: "セルレベル放電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_OVERCURRENT_DISCHARGE_CELL_RSL",
                    name: "Cell-level Discharge Overcurrent (RSL)",
                    nameKo: "셀 레벨 방전 과전류 (RSL)",
                    nameJa: "セルレベル放電過電流 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_OVERCURRENT_DISCHARGE_CELL_MOL",
                    name: "Cell-level Discharge Overcurrent (MOL)",
                    nameKo: "셀 레벨 방전 과전류 (MOL)",
                    nameJa: "セルレベル放電過電流 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_CHARGE_MSL",
                    name: "String-level Charge Overcurrent (MSL)",
                    nameKo: "스트링 레벨 충전 과전류 (MSL)",
                    nameJa: "ストリングレベル充電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_CHARGE_RSL",
                    name: "String-level Charge Overcurrent (RSL)",
                    nameKo: "스트링 레벨 충전 과전류 (RSL)",
                    nameJa: "ストリングレベル充電過電流 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_CHARGE_MOL",
                    name: "String-level Charge Overcurrent (MOL)",
                    nameKo: "스트링 레벨 충전 과전류 (MOL)",
                    nameJa: "ストリングレベル充電過電流 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_DISCHARGE_MSL",
                    name: "String-level Discharge Overcurrent (MSL)",
                    nameKo: "스트링 레벨 방전 과전류 (MSL)",
                    nameJa: "ストリングレベル放電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_DISCHARGE_RSL",
                    name: "String-level Discharge Overcurrent (RSL)",
                    nameKo: "스트링 레벨 방전 과전류 (RSL)",
                    nameJa: "ストリングレベル放電過電流 (RSL)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_STRING_OVERCURRENT_DISCHARGE_MOL",
                    name: "String-level Discharge Overcurrent (MOL)",
                    nameKo: "스트링 레벨 방전 과전류 (MOL)",
                    nameJa: "ストリングレベル放電過電流 (MOL)",
                    severity: "info",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PACK_OVERCURRENT_CHARGE_MSL",
                    name: "Pack-level Charge Overcurrent (MSL)",
                    nameKo: "팩 레벨 충전 과전류 (MSL)",
                    nameJa: "パックレベル充電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_PACK_OVERCURRENT_DISCHARGE_MSL",
                    name: "Pack-level Discharge Overcurrent (MSL)",
                    nameKo: "팩 레벨 방전 과전류 (MSL)",
                    nameJa: "パックレベル放電過電流 (MSL)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_ON_OPEN_STRING",
                    name: "Current on Open String",
                    nameKo: "오픈 스트링 전류 감지",
                    nameJa: "オープンストリング電流検出",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_SENSOR_RESPONDING",
                    name: "Current Sensor Responding",
                    nameKo: "전류센서 응답",
                    nameJa: "電流センサー応答",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0ABF01", "P0ABF11", "P0ABF12"]
                },
                {
                    id: "DIAG_ID_CURRENT_SENSOR_CC_RESPONDING",
                    name: "Current Sensor Coulomb Counter Responding",
                    nameKo: "전류센서 쿨롱 카운터 응답",
                    nameJa: "電流センサークーロンカウンター応答",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_SENSOR_EC_RESPONDING",
                    name: "Current Sensor Energy Counter Responding",
                    nameKo: "전류센서 에너지 카운터 응답",
                    nameJa: "電流センサーエネルギーカウンター応答",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                }
            ],
            oemOnly: [
                {
                    id: "current_sensor",
                    name: "Current Sensor Performance",
                    nameKo: "전류센서 성능이상",
                    nameJa: "電流センサー性能異常",
                    oemCodes: ["P0ABF01", "P0ABF11", "P0ABF12", "P0AF011", "P0AF012", "P0AF111", "P0AF112"],
                    description: "High voltage battery current sensor diagnostics",
                    descriptionKo: "고전압 배터리 전류센서 진단",
                    descriptionJa: "高電圧バッテリー電流センサー診断"
                },
                {
                    id: "12v_battery_current",
                    name: "12V Lithium Battery Current Sensor",
                    nameKo: "12V 리튬배터리 전류센서",
                    nameJa: "12Vリチウムバッテリー電流センサー",
                    oemCodes: ["P1BB600", "P1BB700", "P1BB800"],
                    description: "12V auxiliary lithium battery current sensor diagnostics",
                    descriptionKo: "12V 보조 리튬배터리 전류센서 진단",
                    descriptionJa: "12V補助リチウムバッテリー電流センサー診断"
                },
                {
                    id: "catl_current_sensor",
                    name: "CATL Current Sensor Module",
                    nameKo: "CATL 전류센서 모듈",
                    nameJa: "CATL電流センサーモジュール",
                    oemCodes: ["P146000"],
                    description: "CATL high voltage current sensor module fault",
                    descriptionKo: "CATL 고전압 전류센서 모듈 고장",
                    descriptionJa: "CATL高電圧電流センサーモジュール故障"
                },
                {
                    id: "catl_overcurrent",
                    name: "CATL Battery Overcurrent",
                    nameKo: "CATL 배터리 과전류",
                    nameJa: "CATLバッテリー過電流",
                    oemCodes: ["P146900", "P146A00"],
                    description: "CATL high voltage battery overcurrent detection",
                    descriptionKo: "CATL 고전압 배터리 과전류 감지",
                    descriptionJa: "CATL高電圧バッテリー過電流検出"
                }
            ]
        },
        {
            id: "communication",
            name: {
                en: "Communication Diagnostics",
                ko: "통신 진단",
                ja: "通信診断"
            },
            icon: "fa-network-wired",
            foxbms: [
                {
                    id: "DIAG_ID_AFE_SPI",
                    name: "AFE SPI Communication Error",
                    nameKo: "AFE SPI 통신 에러",
                    nameJa: "AFE SPI通信エラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_AFE_COMMUNICATION_INTEGRITY",
                    name: "AFE Communication Integrity (PEC)",
                    nameKo: "AFE 통신 무결성 (PEC)",
                    nameJa: "AFE通信整合性 (PEC)",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_AFE_MUX",
                    name: "AFE Multiplexer Error",
                    nameKo: "AFE 멀티플렉서 에러",
                    nameJa: "AFEマルチプレクサーエラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_AFE_CONFIG",
                    name: "AFE Configuration Error",
                    nameKo: "AFE 설정 에러",
                    nameJa: "AFE設定エラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CAN_TIMING",
                    name: "CAN Timing Error",
                    nameKo: "CAN 타이밍 에러",
                    nameJa: "CANタイミングエラー",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["U000100"]
                },
                {
                    id: "DIAG_ID_CAN_RX_QUEUE_FULL",
                    name: "CAN RX Queue Full",
                    nameKo: "CAN 수신 큐 풀",
                    nameJa: "CAN受信キュー満杯",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CAN_TX_QUEUE_FULL",
                    name: "CAN TX Queue Full",
                    nameKo: "CAN 송신 큐 풀",
                    nameJa: "CAN送信キュー満杯",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
            ],
            oemOnly: [
                {
                    id: "can_pcan",
                    name: "P-CAN Communication",
                    nameKo: "P-CAN 통신",
                    nameJa: "P-CAN通信",
                    oemCodes: ["U000100", "U010000", "U011000", "U019800", "U019B00", "U029300"],
                    description: "P-CAN bus communication diagnostics (MCU, HCU/VCU, OBC)",
                    descriptionKo: "P-CAN 버스 통신 진단 (MCU, HCU/VCU, OBC)",
                    descriptionJa: "P-CANバス通信診断 (MCU, HCU/VCU, OBC)"
                },
                {
                    id: "can_hcan",
                    name: "H-CAN Communication",
                    nameKo: "H-CAN 통신",
                    nameJa: "H-CAN通信",
                    oemCodes: ["U100100", "U100400", "U100500", "U141182", "U159400"],
                    description: "H-CAN bus communication diagnostics (HCU, MCU)",
                    descriptionKo: "H-CAN 버스 통신 진단 (HCU, MCU)",
                    descriptionJa: "H-CANバス通信診断 (HCU, MCU)"
                },
                {
                    id: "can_gcan",
                    name: "G-CAN Communication",
                    nameKo: "G-CAN 통신",
                    nameJa: "G-CAN通信",
                    oemCodes: ["U059400", "U141582"],
                    description: "G-CAN bus communication diagnostics (HCU/VCU, VCMS)",
                    descriptionKo: "G-CAN 버스 통신 진단 (HCU/VCU, VCMS)",
                    descriptionJa: "G-CANバス通信診断 (HCU/VCU, VCMS)"
                },
                {
                    id: "can_fcu_mcu",
                    name: "FCU-MCU Data Reliability",
                    nameKo: "FCU-MCU 데이터 신뢰성",
                    nameJa: "FCU-MCUデータ信頼性",
                    oemCodes: ["U041182"],
                    description: "Front control unit to MCU data integrity",
                    descriptionKo: "전방 제어 유닛-MCU 데이터 무결성",
                    descriptionJa: "フロント制御ユニット-MCUデータ整合性"
                },
                {
                    id: "can_ewp",
                    name: "EWP Communication",
                    nameKo: "냉각수 펌프 통신",
                    nameJa: "冷却水ポンプ通信",
                    oemCodes: ["U111800", "U111900"],
                    description: "Electric water pump communication diagnostics",
                    descriptionKo: "전동 워터펌프 통신 진단",
                    descriptionJa: "電動ウォーターポンプ通信診断"
                },
                {
                    id: "can_vcms",
                    name: "VCMS Communication",
                    nameKo: "VCMS 통신",
                    nameJa: "VCMS通信",
                    oemCodes: ["U130E87", "U077C82", "U077C8C"],
                    description: "Vehicle charging management system communication",
                    descriptionKo: "차량 충전 관리 시스템 통신",
                    descriptionJa: "車両充電管理システム通信"
                },
                {
                    id: "can_coolant_valve",
                    name: "Coolant Valve Communication",
                    nameKo: "냉각수 밸브 통신",
                    nameJa: "冷却水バルブ通信",
                    oemCodes: ["U112800", "U113800", "U113900"],
                    description: "Battery coolant valve communication error",
                    descriptionKo: "배터리 냉각수 밸브 통신 에러",
                    descriptionJa: "バッテリー冷却水バルブ通信エラー"
                },
                {
                    id: "can_vehicle_modules",
                    name: "Vehicle Module Communication",
                    nameKo: "차량 모듈 통신",
                    nameJa: "車両モジュール通信",
                    oemCodes: ["U003788", "U081082", "U08108C", "U106582", "U10658C"],
                    description: "Drive motor and powertrain control module communication",
                    descriptionKo: "구동 모터 및 파워트레인 제어 모듈 통신",
                    descriptionJa: "駆動モーターおよびパワートレイン制御モジュール通信"
                },
                {
                    id: "can_ccm_obc",
                    name: "CCM/OBC Communication",
                    nameKo: "CCM/OBC 통신",
                    nameJa: "CCM/OBC通信",
                    oemCodes: ["U130D00"],
                    description: "Charging control and onboard charger communication",
                    descriptionKo: "충전 제어 및 온보드 차저 통신",
                    descriptionJa: "充電制御およびオンボードチャージャー通信"
                },
                {
                    id: "catl_bms_communication",
                    name: "CATL BMS Communication",
                    nameKo: "CATL BMS 통신",
                    nameJa: "CATL BMS通信",
                    oemCodes: ["P146B00"],
                    description: "CATL battery management system communication timeout",
                    descriptionKo: "CATL 배터리 관리 시스템 통신 타임아웃",
                    descriptionJa: "CATLバッテリー管理システム通信タイムアウト"
                }
            ]
        },
        {
            id: "insulation",
            name: {
                en: "Insulation Monitoring (IMD)",
                ko: "절연 모니터링 (IMD)",
                ja: "絶縁モニタリング (IMD)"
            },
            icon: "fa-shield-virus",
            foxbms: [
                {
                    id: "DIAG_ID_INSULATION_MEASUREMENT_VALID",
                    name: "Insulation Measurement Validity",
                    nameKo: "절연 측정 유효성",
                    nameJa: "絶縁測定有効性",
                    severity: "warning",
                    hasOemEquivalent: true,
                    oemCodes: ["P0AA700", "P0AA701"]
                },
                {
                    id: "DIAG_ID_LOW_INSULATION_RESISTANCE_ERROR",
                    name: "Critical Insulation Resistance (<500kOhm)",
                    nameKo: "절연저항 위험 (<500kOhm)",
                    nameJa: "絶縁抵抗危険 (<500kOhm)",
                    severity: "warning",
                    hasOemEquivalent: true,
                    oemCodes: ["P0AA600", "P1AA800"]
                },
                {
                    id: "DIAG_ID_LOW_INSULATION_RESISTANCE_WARNING",
                    name: "Low Insulation Resistance (<750kOhm)",
                    nameKo: "절연저항 경고 (<750kOhm)",
                    nameJa: "絶縁抵抗警告 (<750kOhm)",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_INSULATION_GROUND_ERROR",
                    name: "Ground Fault Detected",
                    nameKo: "접지 고장 감지",
                    nameJa: "接地故障検出",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                }
            ],
            oemOnly: []
        },
        {
            id: "circuit",
            name: {
                en: "Circuit Diagnostics (AFE)",
                ko: "회로 진단 (AFE)",
                ja: "回路診断 (AFE)"
            },
            icon: "fa-microchip",
            foxbms: [
                {
                    id: "DIAG_ID_AFE_OPEN_WIRE",
                    name: "Open Wire Detection",
                    nameKo: "오픈 와이어 감지",
                    nameJa: "オープンワイヤー検出",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: [],
                    supportedAfe: ["LTC6804-1", "LTC6806", "LTC6811-1", "LTC6813-1", "ADES1830", "MC33775A"]
                }
            ],
            oemOnly: []
        },
        {
            id: "thermal",
            name: {
                en: "Thermal Management",
                ko: "열관리 시스템",
                ja: "熱管理システム"
            },
            icon: "fa-fan",
            foxbms: [],
            oemOnly: [
                {
                    id: "cooling_fan",
                    name: "Cooling Fan System",
                    nameKo: "냉각 팬 시스템",
                    nameJa: "冷却ファンシステム",
                    oemCodes: ["P0A8113", "P0A811F", "P0A8190", "P0A8200", "P0A8201", "P0A819E", "P0A819F", "P0A81F0", "P0A829F"],
                    description: "High voltage battery cooling fan diagnostics",
                    descriptionKo: "고전압 배터리 냉각 팬 진단",
                    descriptionJa: "高電圧バッテリー冷却ファン診断"
                },
                {
                    id: "coolant_temp_sensor",
                    name: "Coolant Temperature Sensor",
                    nameKo: "냉각수 온도센서",
                    nameJa: "冷却水温度センサー",
                    oemCodes: ["P0C4211", "P0C4212", "P00B111", "P00B112"],
                    description: "Battery and radiator coolant temperature monitoring",
                    descriptionKo: "배터리 및 라디에이터 냉각수 온도 모니터링",
                    descriptionJa: "バッテリーおよびラジエーター冷却水温度監視"
                },
                {
                    id: "coolant_pump",
                    name: "Coolant Pump (EWP)",
                    nameKo: "냉각수 펌프 (EWP)",
                    nameJa: "冷却水ポンプ (EWP)",
                    oemCodes: ["P0C4792", "P0CE992", "P0A8190"],
                    description: "Electric water pump performance diagnostics",
                    descriptionKo: "전동 워터펌프 성능 진단",
                    descriptionJa: "電動ウォーターポンプ性能診断"
                },
                {
                    id: "coolant_valve",
                    name: "Coolant Valve",
                    nameKo: "냉각수 밸브",
                    nameJa: "冷却水バルブ",
                    oemCodes: ["P0CDF7F", "P0D1A7F"],
                    description: "Battery cooling valve control diagnostics",
                    descriptionKo: "배터리 냉각 밸브 제어 진단",
                    descriptionJa: "バッテリー冷却バルブ制御診断"
                },
                {
                    id: "coolant_level_sensor",
                    name: "Coolant Level Sensor",
                    nameKo: "냉각수 수위센서",
                    nameJa: "冷却水レベルセンサー",
                    oemCodes: ["P1BD212", "P1BD311", "P1BD400", "P1BD812", "P1BD911"],
                    description: "Battery coolant level sensor diagnostics",
                    descriptionKo: "배터리 냉각수 수위센서 진단",
                    descriptionJa: "バッテリー冷却水レベルセンサー診断"
                },
                {
                    id: "cooling_power_supply",
                    name: "Cooling System Power Supply",
                    nameKo: "냉각 시스템 전원 공급",
                    nameJa: "冷却システム電源供給",
                    oemCodes: ["P0BBF01", "P0B6F01"],
                    description: "Cooling components power supply circuit diagnostics",
                    descriptionKo: "냉각 부품 전원 공급 회로 진단",
                    descriptionJa: "冷却部品電源供給回路診断"
                },
                {
                    id: "heating_system",
                    name: "Battery Heating System",
                    nameKo: "배터리 히팅 시스템",
                    nameJa: "バッテリーヒーティングシステム",
                    oemCodes: ["P1BA500", "P1BA512", "P1BA700", "P1BA800"],
                    description: "Battery heater and heater relay diagnostics",
                    descriptionKo: "배터리 히터 및 히터 릴레이 진단",
                    descriptionJa: "バッテリーヒーターおよびヒーターリレー診断"
                },
                {
                    id: "pra_busbar",
                    name: "PRA Busbar Temperature",
                    nameKo: "PRA 버스바 온도",
                    nameJa: "PRAバスバー温度",
                    oemCodes: ["P1BC000", "P1BC600", "P1BC611", "P1BC612", "P1BC700", "P1BC800", "P1BD000", "P1BD100", "P1BD600", "P1BD700"],
                    description: "Power relay assembly busbar thermal monitoring",
                    descriptionKo: "파워 릴레이 어셈블리 버스바 열 모니터링",
                    descriptionJa: "パワーリレーアセンブリバスバー熱監視"
                }
            ]
        },
        {
            id: "abnormal",
            name: {
                en: "Battery Abnormal Behavior Detection",
                ko: "배터리 비정상 거동 감지",
                ja: "バッテリー異常動作検出"
            },
            icon: "fa-exclamation-triangle",
            foxbms: [],
            oemOnly: [
                {
                    id: "abnormal_general",
                    name: "General Abnormal Behavior",
                    nameKo: "일반 비정상 거동",
                    nameJa: "一般異常動作",
                    oemCodes: ["P1AA000", "P1AA600"],
                    description: "General battery abnormal behavior detection",
                    descriptionKo: "일반 배터리 비정상 거동 감지",
                    descriptionJa: "一般バッテリー異常動作検出"
                },
                {
                    id: "cell_voltage_variation",
                    name: "Cell Voltage Variation",
                    nameKo: "셀 전압 변화",
                    nameJa: "セル電圧変化",
                    oemCodes: ["P1AA900"],
                    description: "Abnormal cell voltage change detection",
                    descriptionKo: "비정상적인 셀 전압 변화 감지",
                    descriptionJa: "異常なセル電圧変化検出"
                },
                {
                    id: "cv_section",
                    name: "CV Section Current Variation",
                    nameKo: "CV구간 전류 변화",
                    nameJa: "CV区間電流変化",
                    oemCodes: ["P1AAA00"],
                    description: "Constant voltage section charging current anomaly",
                    descriptionKo: "정전압 구간 충전 전류 이상",
                    descriptionJa: "定電圧区間充電電流異常"
                },
                {
                    id: "ocv_deviation",
                    name: "OCV Deviation",
                    nameKo: "OCV 편차",
                    nameJa: "OCV偏差",
                    oemCodes: ["P1AD000"],
                    description: "Open circuit voltage deviation detection",
                    descriptionKo: "개방 회로 전압 편차 감지",
                    descriptionJa: "開回路電圧偏差検出"
                },
                {
                    id: "ccv_deviation",
                    name: "CCV Deviation",
                    nameKo: "CCV 편차",
                    nameJa: "CCV偏差",
                    oemCodes: ["P1AD100"],
                    description: "Closed circuit voltage deviation detection",
                    descriptionKo: "폐회로 전압 편차 감지",
                    descriptionJa: "閉回路電圧偏差検出"
                },
                {
                    id: "rs_deviation",
                    name: "Internal Resistance Deviation",
                    nameKo: "내부 저항 편차",
                    nameJa: "内部抵抗偏差",
                    oemCodes: ["P1AD200"],
                    description: "Cell internal resistance deviation detection",
                    descriptionKo: "셀 내부 저항 편차 감지",
                    descriptionJa: "セル内部抵抗偏差検出"
                },
                {
                    id: "misd",
                    name: "Micro Internal Short Detection (MISD)",
                    nameKo: "미세 단락 진단 (MISD)",
                    nameJa: "微細短絡診断 (MISD)",
                    oemCodes: ["P1AD300"],
                    description: "Detection of micro-short circuits within cells",
                    descriptionKo: "셀 내부 미세 단락 감지",
                    descriptionJa: "セル内部微細短絡検出"
                },
                {
                    id: "sp_misd",
                    name: "Short-Period MISD",
                    nameKo: "단기 미세 단락 진단",
                    nameJa: "短期微細短絡診断",
                    oemCodes: ["P1AD500"],
                    description: "Short-period micro internal short detection",
                    descriptionKo: "단기 미세 내부 단락 감지",
                    descriptionJa: "短期微細内部短絡検出"
                },
                {
                    id: "misd2",
                    name: "MISD Level 2",
                    nameKo: "미세 단락 진단 레벨2",
                    nameJa: "微細短絡診断レベル2",
                    oemCodes: ["P1AD600"],
                    description: "Advanced micro internal short detection",
                    descriptionKo: "고급 미세 내부 단락 감지",
                    descriptionJa: "高度微細内部短絡検出"
                },
                {
                    id: "thermal_runaway",
                    name: "Thermal Runaway Detection",
                    nameKo: "열폭주 감지",
                    nameJa: "熱暴走検出",
                    oemCodes: ["P1AD42E", "P1BED00", "P1BED2E"],
                    description: "Battery thermal runaway event detection",
                    descriptionKo: "배터리 열폭주 이벤트 감지",
                    descriptionJa: "バッテリー熱暴走イベント検出"
                },
                {
                    id: "insulation_failure",
                    name: "Insulation Failure Detection",
                    nameKo: "절연고장 감지",
                    nameJa: "絶縁故障検出",
                    oemCodes: ["P1AA800"],
                    description: "Battery insulation failure behavior detection",
                    descriptionKo: "배터리 절연고장 비정상 거동 감지",
                    descriptionJa: "バッテリー絶縁故障異常動作検出"
                },
                {
                    id: "rdv",
                    name: "RDV Detection",
                    nameKo: "RDV 감지",
                    nameJa: "RDV検出",
                    oemCodes: ["P1AB000"],
                    description: "Residual discharge voltage anomaly detection",
                    descriptionKo: "잔류 방전 전압 이상 감지",
                    descriptionJa: "残留放電電圧異常検出"
                },
                {
                    id: "avcd",
                    name: "AVCD Detection",
                    nameKo: "AVCD 감지",
                    nameJa: "AVCD検出",
                    oemCodes: ["P1AAF00"],
                    description: "Abnormal voltage change detection",
                    descriptionKo: "비정상 전압 변화 감지",
                    descriptionJa: "異常電圧変化検出"
                },
                {
                    id: "abnormal_overtemperature",
                    name: "Abnormal Overtemperature",
                    nameKo: "비정상 과온",
                    nameJa: "異常過温",
                    oemCodes: ["P1AAB00"],
                    description: "Abnormal battery overtemperature detection",
                    descriptionKo: "비정상 배터리 과온 감지",
                    descriptionJa: "異常バッテリー過温検出"
                },
                {
                    id: "abnormal_overvoltage",
                    name: "Abnormal Overvoltage",
                    nameKo: "비정상 과전압",
                    nameJa: "異常過電圧",
                    oemCodes: ["P1AAC00"],
                    description: "Abnormal battery overvoltage detection",
                    descriptionKo: "비정상 배터리 과전압 감지",
                    descriptionJa: "異常バッテリー過電圧検出"
                },
                {
                    id: "abnormal_undervoltage",
                    name: "Abnormal Undervoltage",
                    nameKo: "비정상 저전압",
                    nameJa: "異常低電圧",
                    oemCodes: ["P1AAD00"],
                    description: "Abnormal battery undervoltage detection",
                    descriptionKo: "비정상 배터리 저전압 감지",
                    descriptionJa: "異常バッテリー低電圧検出"
                }
            ]
        },
        {
            id: "system",
            name: {
                en: "System & Safety",
                ko: "시스템 및 안전",
                ja: "システム＆安全"
            },
            icon: "fa-cogs",
            foxbms: [
                {
                    id: "DIAG_ID_INTERLOCK_FEEDBACK",
                    name: "Interlock Circuit Feedback",
                    nameKo: "인터락 회로 피드백",
                    nameJa: "インターロック回路フィードバック",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P0A0A12"]
                },
                {
                    id: "DIAG_ID_STRING_MINUS_CONTACTOR_FEEDBACK",
                    name: "String Minus Contactor Feedback",
                    nameKo: "스트링 마이너스 컨택터 피드백",
                    nameJa: "ストリングマイナスコンタクターフィードバック",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B7600"]
                },
                {
                    id: "DIAG_ID_STRING_PLUS_CONTACTOR_FEEDBACK",
                    name: "String Plus Contactor Feedback",
                    nameKo: "스트링 플러스 컨택터 피드백",
                    nameJa: "ストリングプラスコンタクターフィードバック",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B7600"]
                },
                {
                    id: "DIAG_ID_PRECHARGE_CONTACTOR_FEEDBACK",
                    name: "Precharge Contactor Feedback",
                    nameKo: "프리차지 컨택터 피드백",
                    nameJa: "プリチャージコンタクターフィードバック",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B7700"]
                },
                {
                    id: "DIAG_ID_PRECHARGE_ABORT_REASON_VOLTAGE",
                    name: "Precharge Abort: Voltage Difference",
                    nameKo: "프리차지 중단: 전압 차이",
                    nameJa: "プリチャージ中止：電圧差",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B7700"]
                },
                {
                    id: "DIAG_ID_PRECHARGE_ABORT_REASON_CURRENT",
                    name: "Precharge Abort: High Current",
                    nameKo: "프리차지 중단: 고전류",
                    nameJa: "プリチャージ中止：高電流",
                    severity: "fatal",
                    hasOemEquivalent: true,
                    oemCodes: ["P1B7700"]
                },
                {
                    id: "DIAG_ID_SBC_FIN_ERROR",
                    name: "SBC FIN Signal Error",
                    nameKo: "SBC FIN 신호 에러",
                    nameJa: "SBC FIN信号エラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_SBC_RSTB_ERROR",
                    name: "SBC RSTB Pin Activation",
                    nameKo: "SBC RSTB 핀 활성화",
                    nameJa: "SBC RSTBピン起動",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_ALERT_MODE",
                    name: "Alert Mode: Contactor Opening Critical Error",
                    nameKo: "경고 모드: 컨택터 개방 치명적 에러",
                    nameJa: "警告モード：コンタクター開放致命的エラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_AEROSOL_ALERT",
                    name: "High Aerosol Concentration Detected",
                    nameKo: "고농도 에어로졸 감지",
                    nameJa: "高濃度エアロゾル検出",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                }
            ],
            oemOnly: [
                {
                    id: "interlock_circuit",
                    name: "Interlock Circuit",
                    nameKo: "인터락 회로",
                    nameJa: "インターロック回路",
                    oemCodes: ["P0A7A00", "P0A7A12"],
                    description: "High voltage system interlock circuit diagnostics",
                    descriptionKo: "고전압 시스템 인터락 회로 진단",
                    descriptionJa: "高電圧システムインターロック回路診断"
                },
                {
                    id: "airbag_signal",
                    name: "Airbag Deployment Signal",
                    nameKo: "에어백 전개 신호",
                    nameJa: "エアバッグ展開信号",
                    oemCodes: ["P1A6F00", "P1A6F11", "P1A6F12", "P1A7100", "P1AF000"],
                    description: "Integration with vehicle airbag deployment system",
                    descriptionKo: "차량 에어백 전개 시스템 연동",
                    descriptionJa: "車両エアバッグ展開システム連動"
                },
                {
                    id: "relay_control",
                    name: "Relay Control Circuit",
                    nameKo: "릴레이 제어 회로",
                    nameJa: "リレー制御回路",
                    oemCodes: ["P0AD911", "P0ADD11", "P0AE411", "P187600", "P187700", "P1B6800", "P1BDD00"],
                    description: "High voltage relay control circuit diagnostics",
                    descriptionKo: "고전압 릴레이 제어 회로 진단",
                    descriptionJa: "高電圧リレー制御回路診断"
                },
                {
                    id: "overcharge_protection",
                    name: "Overcharge Protection Circuit",
                    nameKo: "과충전 차단 회로",
                    nameJa: "過充電遮断回路",
                    oemCodes: ["P0C3000", "P1B9A00", "P1BBA00", "P1BBC00", "P1BBD00"],
                    description: "BMS overcharge cutoff circuit and SOC excess detection",
                    descriptionKo: "BMS 과충전 차단 회로 및 SOC 과다 감지",
                    descriptionJa: "BMS過充電遮断回路およびSOC過多検出"
                },
                {
                    id: "12v_battery_system",
                    name: "12V Lithium Battery System",
                    nameKo: "12V 리튬배터리 시스템",
                    nameJa: "12Vリチウムバッテリーシステム",
                    oemCodes: ["P1BB000", "P1BB200", "P1BB900", "P1BBA00", "P1BBB00", "P1BBE00", "P1BBF00"],
                    description: "12V auxiliary lithium battery system diagnostics",
                    descriptionKo: "12V 보조 리튬배터리 시스템 진단",
                    descriptionJa: "12V補助リチウムバッテリーシステム診断"
                },
                {
                    id: "fast_charging_system",
                    name: "Fast Charging System",
                    nameKo: "급속충전 시스템",
                    nameJa: "急速充電システム",
                    oemCodes: ["P1BA400", "P1BAB00", "P1BAC00", "P1BAD00"],
                    description: "DC fast charging relay and system diagnostics",
                    descriptionKo: "DC 급속충전 릴레이 및 시스템 진단",
                    descriptionJa: "DC急速充電リレーおよびシステム診断"
                },
                {
                    id: "inverter_voltage",
                    name: "Inverter-Battery Voltage Deviation",
                    nameKo: "인버터-배터리 전압 편차",
                    nameJa: "インバーター・バッテリー電圧偏差",
                    oemCodes: ["P1B2500", "P1B5000"],
                    description: "Voltage difference between inverter and battery pack",
                    descriptionKo: "인버터와 배터리팩 간 전압 차이",
                    descriptionJa: "インバーターとバッテリーパック間電圧差"
                },
                {
                    id: "battery_pack_composite",
                    name: "Battery Pack Composite Diagnosis",
                    nameKo: "배터리팩 복합진단",
                    nameJa: "バッテリーパック複合診断",
                    oemCodes: ["P1AA500"],
                    description: "Comprehensive battery pack health assessment",
                    descriptionKo: "종합적인 배터리팩 상태 평가",
                    descriptionJa: "総合的なバッテリーパック状態評価"
                },
                {
                    id: "12v_path",
                    name: "12V Voltage Path",
                    nameKo: "12V 전압 경로",
                    nameJa: "12V電圧経路",
                    oemCodes: ["P1BE000"],
                    description: "12V voltage path error diagnostics",
                    descriptionKo: "12V 전압 경로 이상 진단",
                    descriptionJa: "12V電圧経路異常診断"
                },
                {
                    id: "coolant_overfill",
                    name: "Coolant Overfill Detection",
                    nameKo: "냉각수 과충전 감지",
                    nameJa: "冷却水過充填検出",
                    oemCodes: ["P1BD500"],
                    description: "Battery cooling system overfill detection",
                    descriptionKo: "배터리 냉각 시스템 과충전 감지",
                    descriptionJa: "バッテリー冷却システム過充填検出"
                },
                {
                    id: "catl_bms_system",
                    name: "CATL BMS System",
                    nameKo: "CATL BMS 시스템",
                    nameJa: "CATLBMSシステム",
                    oemCodes: ["P146100", "P146200", "P146300", "P146400", "P146500", "P146600", "P146700", "P146800", "P146C00", "P146D00", "P146E00", "P146F00", "P147000", "P147100"],
                    description: "CATL battery management system diagnostics",
                    descriptionKo: "CATL 배터리 관리 시스템 진단",
                    descriptionJa: "CATLバッテリー管理システム診断"
                }
            ]
        },
        {
            id: "redundancy",
            name: {
                en: "Redundancy & Timeout",
                ko: "이중화 및 타임아웃",
                ja: "冗長性＆タイムアウト"
            },
            icon: "fa-clock",
            foxbms: [
                {
                    id: "DIAG_ID_BASE_CELL_VOLTAGE_MEASUREMENT_TIMEOUT",
                    name: "Base Cell Voltage Measurement Timeout",
                    nameKo: "베이스 셀 전압 측정 타임아웃",
                    nameJa: "ベースセル電圧測定タイムアウト",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_BASE_CELL_TEMPERATURE_MEASUREMENT_TIMEOUT",
                    name: "Base Cell Temperature Measurement Timeout",
                    nameKo: "베이스 셀 온도 측정 타임아웃",
                    nameJa: "ベースセル温度測定タイムアウト",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_MEASUREMENT_TIMEOUT",
                    name: "Current Measurement Timeout",
                    nameKo: "전류 측정 타임아웃",
                    nameJa: "電流測定タイムアウト",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_MEASUREMENT_ERROR",
                    name: "Current Measurement Invalid",
                    nameKo: "전류 측정 무효",
                    nameJa: "電流測定無効",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_CURRENT_SENSOR_POWER_MEASUREMENT_TIMEOUT",
                    name: "Current Sensor Power Measurement Timeout",
                    nameKo: "전류센서 전력 측정 타임아웃",
                    nameJa: "電流センサー電力測定タイムアウト",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_POWER_MEASUREMENT_ERROR",
                    name: "Power Measurement Invalid",
                    nameKo: "전력 측정 무효",
                    nameJa: "電力測定無効",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                }
            ],
            oemOnly: []
        },
        {
            id: "memory",
            name: {
                en: "Memory & Flash",
                ko: "메모리 및 플래시",
                ja: "メモリ＆フラッシュ"
            },
            icon: "fa-memory",
            foxbms: [
                {
                    id: "DIAG_ID_FLASHCHECKSUM",
                    name: "Flash Checksum Validation Error",
                    nameKo: "플래시 체크섬 검증 에러",
                    nameJa: "フラッシュチェックサム検証エラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_FRAM_READ_CRC_ERROR",
                    name: "FRAM Read CRC Error",
                    nameKo: "FRAM 읽기 CRC 에러",
                    nameJa: "FRAM読み取りCRCエラー",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_RTC_CLOCK_INTEGRITY_ERROR",
                    name: "RTC Clock Integrity Error",
                    nameKo: "RTC 클럭 무결성 에러",
                    nameJa: "RTCクロック整合性エラー",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_RTC_BATTERY_LOW_ERROR",
                    name: "RTC Battery Low",
                    nameKo: "RTC 배터리 부족",
                    nameJa: "RTCバッテリー低下",
                    severity: "warning",
                    hasOemEquivalent: false,
                    oemCodes: []
                },
                {
                    id: "DIAG_ID_SYSTEM_MONITORING",
                    name: "System Monitoring: Task Timing Deviation",
                    nameKo: "시스템 모니터링: 태스크 타이밍 편차",
                    nameJa: "システム監視：タスクタイミング偏差",
                    severity: "fatal",
                    hasOemEquivalent: false,
                    oemCodes: []
                }
            ],
            oemOnly: []
        }
    ],

    // Vehicle Coverage Summary
    vehicleCoverage: {
        hyundai: {
            models: [
                { name: "IONIQ 5", code: "NE", type: "EV", years: [2022, 2023, 2024, 2025] },
                { name: "IONIQ 5 N", code: "NE-N", type: "EV", years: [2025] },
                { name: "IONIQ 6", code: "CE", type: "EV", years: [2023, 2024, 2025, 2026] },
                { name: "IONIQ 6 N", code: "CE-N", type: "EV", years: [2026] },
                { name: "IONIQ 9", code: "ME", type: "EV", years: [2025] },
                { name: "KONA Electric", code: "OS/SX2", type: "EV", years: [2019, 2020, 2021, 2024, 2025] },
                { name: "Genesis GV60", code: "JW1", type: "EV", years: [2022, 2023, 2024, 2025, 2026] },
                { name: "Genesis G80 Electrified", code: "RG3", type: "EV", years: [2022, 2023, 2024, 2025] }
            ]
        },
        kia: {
            models: [
                { name: "EV3", code: "SV1", type: "EV", years: [2025, 2026] },
                { name: "EV6", code: "CV", type: "EV", years: [2022, 2023, 2024, 2025, 2026] },
                { name: "EV9", code: "MV", type: "EV", years: [2024, 2025, 2026] },
                { name: "Niro EV", code: "DE/SG2", type: "EV", years: [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] }
            ]
        }
    },

    // Summary Statistics (dynamically calculated by HTML)
    summary: {
        foxbmsFeatures: {
            total: 77,
            byCategory: {
                voltage: 11,
                temperature: 15,
                current: 18,
                communication: 7,
                insulation: 4,
                circuit: 1,
                thermal: 0,
                abnormal: 0,
                system: 10,
                redundancy: 6,
                memory: 5
            }
        },
        oemFeatures: {
            total: 308,
            totalItems: 61,
            byCategory: {
                voltage: 4,
                temperature: 8,
                current: 4,
                communication: 10,
                insulation: 0,
                circuit: 0,
                thermal: 8,
                abnormal: 16,
                system: 11,
                redundancy: 0,
                memory: 0
            },
            byCategoryCodeCount: {
                voltage: 39,
                temperature: 104,
                current: 16,
                communication: 28,
                insulation: 0,
                circuit: 0,
                thermal: 32,
                abnormal: 18,
                system: 57,
                redundancy: 0,
                memory: 0
            }
        },
        comparison: {
            bothHave: 18,
            foxbmsOnly: 59,
            oemOnly: 308
        }
    }
};

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DIAGNOSTIC_COMPARISON;
}
