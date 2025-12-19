// OEM DTC Index - Auto-generated for HD (Hyundai) and KIA
const OEM_DTC_INDEX = {
    "Hyundai": {
        "IONIQ 5": {
            "NE EV": ["2022", "2023", "2024", "2025"],
            "NE EV N": ["2025"]
        },
        "IONIQ 6": {
            "CE EV": ["2023", "2024", "2025", "2026"],
            "CE EV N": ["2026"]
        },
        "IONIQ 9": {
            "ME EV": ["2025"]
        },
        "IONIQ": {
            "AE HEV": ["2016", "2017", "2018", "2019", "2020", "2021"],
            "AE PHEV": ["2017", "2018", "2019", "2020", "2021"],
            "AE EV": ["2017", "2018", "2019", "2020"]
        },
        "KONA": {
            "OS EV": ["2019", "2020", "2021"],
            "OS HEV": ["2020", "2021", "2022", "2023"],
            "SX2 EV": ["2024", "2025"],
            "SX2 HEV": ["2023", "2024", "2025"]
        },
        "Sonata": {
            "YF HEV": ["2011", "2012", "2013", "2014", "2015"],
            "LF HEV": ["2015", "2016", "2017", "2018", "2019"],
            "LF PHEV": ["2016", "2017", "2018", "2019"],
            "DN8 HEV": ["2020", "2021", "2022", "2023", "2024", "2025"]
        },
        "Grandeur": {
            "HG HEV": ["2014", "2015", "2016", "2017"],
            "IG HEV": ["2018", "2019", "2021", "2022", "2023"],
            "GN7 HEV": ["2023", "2024", "2025"]
        },
        "Avante": {
            "HD HEV": ["2011", "2012", "2013", "2014"],
            "CN7 HEV": ["2021", "2022", "2023", "2024", "2025"]
        },
        "Tucson": {
            "NX4 HEV": ["2021", "2022", "2023", "2024", "2025", "2026"]
        },
        "Santa Fe": {
            "TM HEV": ["2022", "2023"],
            "MX5 HEV": ["2024", "2025"]
        },
        "Palisade": {
            "LX3 HEV": ["2025"]
        },
        "Staria": {
            "US4 HEV": ["2025"]
        },
        "Porter 2": {
            "HR EV": ["2020", "2021", "2022", "2023", "2024", "2025"]
        },
        "GV60": {
            "JW1 EV": ["2022", "2023", "2024", "2025", "2026"]
        },
        "G70": {
            "JK1 EV": ["2023", "2024"]
        },
        "G80": {
            "RG3": ["2022", "2023", "2024", "2025"]
        },
        "CASPER": {
            "AX1 EV": ["2025", "2026"]
        },
        "BlueOn": {
            "EA EV": ["2011"]
        }
    },
    "KIA": {
        "EV3": {
            "SV1": ["2025", "2026"]
        },
        "EV4": {
            "CT1": ["2026"]
        },
        "EV5": {
            "OV1k": ["2026"]
        },
        "EV6": {
            "CV": ["2022", "2023", "2024", "2025", "2026"]
        },
        "EV9": {
            "MV": ["2024", "2025", "2026"]
        },
        "PV5": {
            "SW1K": ["2026"]
        },
        "Niro": {
            "DE HEV": ["2017", "2018", "2019", "2020", "2021", "2022"],
            "DE EV": ["2019", "2020", "2021", "2022"],
            "DE PHEV": ["2017", "2018", "2019", "2020", "2021", "2022"],
            "SG2 EV": ["2023", "2024", "2025", "2026"],
            "SG2 HEV": ["2022", "2023", "2024", "2025", "2026"]
        },
        "Niro Plus": {
            "DE EV PBV": ["2023", "2024"]
        },
        "K5": {
            "TF HEV": ["2012", "2013", "2014", "2015", "2016"],
            "VG HEV": ["2014", "2015", "2016"],
            "JF HEV": ["2016", "2017", "2018", "2019", "2020"],
            "JF PHEV": ["2017", "2018"],
            "DL3 HEV": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
        },
        "K7": {
            "YG HEV": ["2017", "2018", "2019", "2020", "2021"]
        },
        "K8": {
            "GL3 HEV": ["2022", "2023", "2024", "2025", "2026"]
        },
        "Sorento": {
            "MQ4 HEV": ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
        },
        "Sportage": {
            "NQ5 HEV": ["2022", "2023", "2024", "2025", "2026"]
        },
        "Carnival": {
            "KA4 HEV": ["2024", "2025", "2026"]
        },
        "Soul EV": {
            "PS EV": ["2015", "2016", "2017", "2018", "2019"],
            "SK3 EV": ["2020", "2021"]
        },
        "Ray EV": {
            "TAV EV": ["2012", "2013", "2014", "2015", "2016", "2017", "2024", "2025"]
        },
        "Bongo3 EV": {
            "PU EV": ["2020", "2021", "2022", "2023", "2024", "2025"]
        },
        "Forte": {
            "TD HEV": ["2010", "2011", "2012", "2013"]
        },
        "Pride": {
            "JB HEV": ["2005", "2006", "2007", "2008"]
        }
    }
};

// File path resolver
function getFilePath(brand, model, variant, year) {
    if (brand === "Hyundai") {
        return getHyundaiFilePath(model, variant, year);
    } else if (brand === "KIA") {
        return getKiaFilePath(model, variant, year);
    }
    return null;
}

function getHyundaiFilePath(model, variant, year) {
    const basePath = "../../HD/";
    const modelMap = {
        "IONIQ 5": { "NE EV": `ioniq5_ne_ev_battery_${year}_dtc.md`, "NE EV N": `ioniq5_n_ne_ev_n_${year}_dtc.md` },
        "IONIQ 6": { "CE EV": `ioniq6_ce_ev_battery_${year}_dtc.md`, "CE EV N": `ioniq6_n_ce_ev_n_bms_${year}_dtc.md` },
        "IONIQ 9": { "ME EV": `IONIQ9_ME_EV_${year}_BMS_DTC.md` },
        "IONIQ": {
            "AE HEV": `IONIQ_AE_HEV_${year}_BMS_DTC.md`,
            "AE PHEV": `IONIQ_AE_PHEV_${year}_BMS_DTC.md`,
            "AE EV": `IONIQ_Electric_AE_EV_${year}_BMS_DTC.md`
        },
        "KONA": {
            "OS EV": `KONA_OS_EV_${year}_BMS_DTC.md`,
            "OS HEV": `KONA_OS_HEV_${year}_BMS_DTC.md`,
            "SX2 EV": `KONA_SX2_EV_${year}_BMS_DTC.md`,
            "SX2 HEV": `kona_hybrid_sx2_hev_${year}_battery_dtc.md`
        },
        "Sonata": {
            "YF HEV": `sonata_yf_hev_${year}_dtc.md`,
            "LF HEV": `sonata_lf_hev_${year}_dtc.md`,
            "LF PHEV": `sonata_lf_phev_${year}_dtc.md`,
            "DN8 HEV": `sonata_dn8_hev_${year}_dtc.md`
        },
        "Grandeur": {
            "HG HEV": `Grandeur_HG_HEV_${year}_BMS_DTC.md`,
            "IG HEV": `Grandeur_IG_HEV_${year}_BMS_DTC.md`,
            "GN7 HEV": `Grandeur_GN7_HEV_${year}_BMS_DTC.md`
        },
        "Avante": {
            "HD HEV": `avante_hd_hev_${year}_dtc.md`,
            "CN7 HEV": `avante_cn7_hev_${year}_dtc.md`
        },
        "Tucson": { "NX4 HEV": `tucson_hybrid_nx4_hev_${year}_battery_dtc.md` },
        "Santa Fe": {
            "TM HEV": `santafe_tm_hev_${year}_dtc.md`,
            "MX5 HEV": `Santafe_MX5_HEV_${year}_BMS_DTC.md`
        },
        "Palisade": { "LX3 HEV": `palisade_hybrid_lx3_hev_${year}_battery_dtc.md` },
        "Staria": { "US4 HEV": `Staria_US4_HEV_${year}_BMS_DTC.md` },
        "Porter 2": { "HR EV": `porter2_electric_hr_ev_${year}_battery_dtc.md` },
        "GV60": { "JW1 EV": `gv_60_jw_1_ev_${year}_bms.md` },
        "G70": { "JK1 EV": `g_70_jk_1_ev_${year}_bms_dtc_list.md` },
        "G80": { "RG3": `g_80_rg_3_${year}_bms_dtc_list.md` },
        "CASPER": { "AX1 EV": `CASPER_AX1_EV_${year}_BMS_DTC.md` },
        "BlueOn": { "EA EV": `BlueOn_EAEV_${year}_BMS_DTC.md` }
    };

    if (modelMap[model] && modelMap[model][variant]) {
        return basePath + modelMap[model][variant];
    }
    return null;
}

function getKiaFilePath(model, variant, year) {
    const basePath = "../../KIA/";
    const folderMap = {
        "EV3": { "SV1": `EV3(SV1)/EV3_SV1_${year}_BMS_DTC.md` },
        "EV4": { "CT1": `EV4(CT1)/EV4_CT1_${year}_BMS_DTC_List.md` },
        "EV5": { "OV1k": `EV5(OV1k)/EV5_OV1k_${year}_BMS_DTC_List.md` },
        "EV6": { "CV": `EV6(CV)/EV6_CV_${year}_BMS_DTC_List.md` },
        "EV9": { "MV": `EV9(MV)/EV9_MV_${year}_BMS_DTC_List.md` },
        "PV5": { "SW1K": `PV5(SW1K)/PV5_SW1K_${year}_BMS_DTC_List.md` },
        "Niro": {
            "DE HEV": `NIro(DE_HEV)/Niro_DE_HEV_${year}_BMS_DTC_List.md`,
            "DE EV": `Niro(DE_EV)/Niro_DE_EV_${year}_BMS_DTC_List.md`,
            "DE PHEV": `Niro(DE_PHEV)/Niro_DE_PHEV_${year}_BMS_DTC_List.md`,
            "SG2 EV": `Niro(SG2_EV)/Niro_SG2_EV_${year}_BMS_DTC_List.md`,
            "SG2 HEV": `Niro(SG2_HEV)/Niro_SG2_HEV_${year}_BMS_DTC_List.md`
        },
        "Niro Plus": { "DE EV PBV": `Niro_Plus(DE_EV_PBV)/Niro_Plus_DE_EV_PBV_${year}_BMS_DTC_List.md` },
        "K5": {
            "TF HEV": `K5_HEV(TF_HEV)/K5_HEV_TF_${year}_BMS_DTC_List.md`,
            "VG HEV": `K5_HEV(VG_HEV)/K5_HEV_VG_${year}_BMS_DTC_List.md`,
            "JF HEV": `K5_HEV(JF_HEV)/K5_HEV_JF_${year}_BMS_DTC_List.md`,
            "JF PHEV": `K5_PHEV(JF_PHEV)/K5_PHEV_JF_${year}_BMS_DTC_List.md`,
            "DL3 HEV": `K5_HEV(DL3_HEV)/K5_HEV_DL3_${year}_BMS_DTC_List.md`
        },
        "K7": { "YG HEV": `K5_HEV(YG_HEV)/K7_HEV_YG_${year}_BMS_DTC_List.md` },
        "K8": { "GL3 HEV": `K5_HEV(GL3_HEV)/K8_HEV_${year}_BMS_DTC_List.md` },
        "Sorento": { "MQ4 HEV": `쏘렌토_HEV(MQ4_HEV)/Sorento_HEV_MQ4_HEV_${year}_BMS_DTC_List.md` },
        "Sportage": { "NQ5 HEV": `스포티지_HEV(NQ5_HEV)/Sportage_HEV_NQ5_HEV_${year}_BMS_DTC_List.md` },
        "Carnival": { "KA4 HEV": `카니발_HEV(KA4_HEV)/Carnival_HEV_KA4_HEV_${year}_BMS_DTC_List.md` },
        "Soul EV": {
            "PS EV": `쏘울_EV(PS_EV)/Soul_EV_PS_EV_${year}_BMS_DTC_List.md`,
            "SK3 EV": `쏘울EV(SK3_EV)/SoulEV_SK3_EV_${year}_BMS_DTC_List.md`
        },
        "Ray EV": { "TAV EV": `레이_EV(TAV_EV)/Ray_EV_TAV_EV_${year}_BMS_DTC_List.md` },
        "Bongo3 EV": { "PU EV": `봉고3_EV(PU_EV)/Bongo3_EV_PU_EV_${year}_BMS_DTC_List.md` },
        "Forte": { "TD HEV": `포르테_HEV(TD_HEV)/Forte_HEV_TD_HEV_${year}_BMS_DTC_List.md` },
        "Pride": { "JB HEV": `프라이드_HEV(JB_HEV)/Pride_HEV_JB_HEV_${year}_BMS_DTC_List.md` }
    };

    if (folderMap[model] && folderMap[model][variant]) {
        return basePath + folderMap[model][variant];
    }
    return null;
}
