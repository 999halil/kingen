from enum import Enum

class ContractType(str, Enum):
    MIN_SLAGEN = "min_slagen"
    MIN_HARTEN = "min_harten"
    MIN_HEREN_BOEREN = "min_heren_boeren"
    MIN_DAMES = "min_dames"
    HARTEN_HEER = "harten_heer"
    Zevende_en_Laatste = "zevende_en_laatste"
    TROEF = "troef"