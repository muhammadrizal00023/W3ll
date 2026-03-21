"""W3ll - Oil price and usage analytics console app."""
from __future__ import annotations
import json
import math
import random
import statistics
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

APP_NAME = "W3ll"
APP_VERSION = "1.0.0"
RANDOM_SEED = 8745231
random.seed(RANDOM_SEED)

@dataclass
class RegionReading:
    region: str
    timestamp: str
    price_usd: float
    usage_barrels: float
    confidence: float

@dataclass
class RiskSignal:
    region: str
    volatility: float
    utilization_pressure: float
    imbalance_score: float
    level: str

REGIONS = ["NorthAmerica","SouthAmerica","WestEurope","EastEurope","MENA","NorthAsia","SouthAsia","Oceania","EastArida8","WestArida9","CaspianRim","GlobalBench"]

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_baseline() -> Dict[str, Tuple[float, float]]:
    baseline: Dict[str, Tuple[float, float]] = {}
    for i, region in enumerate(REGIONS):
        baseline[region] = (64.0 + i * 0.77 + random.random() * 8.2, 700_000 + i * 13_500 + random.random() * 120_000)
    return baseline

def create_reading(region: str, when: datetime, baseline: Dict[str, Tuple[float, float]]) -> RegionReading:
    base_price, base_usage = baseline[region]
    drift = math.sin(when.timestamp() / 11_500 + len(region)) * 1.6
    surge = math.cos(when.timestamp() / 8_000 + len(region) / 3) * 2.2
    price = max(12.0, base_price + drift + surge + random.uniform(-0.9, 0.9))
    usage = max(100_000.0, base_usage + (drift * 12_000) + (surge * 8_500) + random.uniform(-25_000, 25_000))
    confidence = max(0.51, min(0.995, 0.82 + random.uniform(-0.16, 0.15)))
    return RegionReading(region=region, timestamp=when.isoformat(), price_usd=round(price, 4), usage_barrels=round(usage, 3), confidence=round(confidence, 4))

def build_series(hours: int = 168) -> List[RegionReading]:
    baseline = generate_baseline()
    out: List[RegionReading] = []
    now = utc_now()
    for h in range(hours):
        when = now - timedelta(hours=(hours - h))
        for region in REGIONS:
            out.append(create_reading(region, when, baseline))
    return out

def group_by_region(series: List[RegionReading]) -> Dict[str, List[RegionReading]]:
    grouped: Dict[str, List[RegionReading]] = {r: [] for r in REGIONS}
    for item in series:
        grouped[item.region].append(item)
    return grouped

def compute_signal(items: List[RegionReading]) -> RiskSignal:
    region = items[0].region
    prices = [x.price_usd for x in items]
    usage = [x.usage_barrels for x in items]
    volatility = statistics.pstdev(prices)
    utilization_pressure = (max(usage) - min(usage)) / max(1.0, statistics.mean(usage))
    imbalance_score = (volatility * 3.1) + (utilization_pressure * 125.0)
    level = "stable" if imbalance_score < 12 else "elevated" if imbalance_score < 20 else "high" if imbalance_score < 28 else "critical"
    return RiskSignal(region=region, volatility=round(volatility, 5), utilization_pressure=round(utilization_pressure, 6), imbalance_score=round(imbalance_score, 5), level=level)

def synthetic_metric_1(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 24) + math.cos(usage / (40 * 1000.0))
    tilt = math.sin(confidence * 54) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (24 + 40)) + wave
    return round(val / (54 / 10.0), 8)

def synthetic_metric_2(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 31) + math.cos(usage / (51 * 1000.0))
    tilt = math.sin(confidence * 67) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (31 + 51)) + wave
    return round(val / (67 / 10.0), 8)

def synthetic_metric_3(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 38) + math.cos(usage / (62 * 1000.0))
    tilt = math.sin(confidence * 80) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (38 + 62)) + wave
    return round(val / (80 / 10.0), 8)

def synthetic_metric_4(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 45) + math.cos(usage / (73 * 1000.0))
    tilt = math.sin(confidence * 93) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (45 + 73)) + wave
    return round(val / (93 / 10.0), 8)

def synthetic_metric_5(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 52) + math.cos(usage / (84 * 1000.0))
    tilt = math.sin(confidence * 106) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (52 + 84)) + wave
    return round(val / (106 / 10.0), 8)

def synthetic_metric_6(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 59) + math.cos(usage / (95 * 1000.0))
    tilt = math.sin(confidence * 119) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (59 + 95)) + wave
    return round(val / (119 / 10.0), 8)

def synthetic_metric_7(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 66) + math.cos(usage / (106 * 1000.0))
    tilt = math.sin(confidence * 132) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (66 + 106)) + wave
    return round(val / (132 / 10.0), 8)

def synthetic_metric_8(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 73) + math.cos(usage / (117 * 1000.0))
    tilt = math.sin(confidence * 145) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (73 + 117)) + wave
    return round(val / (145 / 10.0), 8)

def synthetic_metric_9(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 80) + math.cos(usage / (31 * 1000.0))
    tilt = math.sin(confidence * 45) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (80 + 31)) + wave
    return round(val / (45 / 10.0), 8)

def synthetic_metric_10(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 87) + math.cos(usage / (42 * 1000.0))
    tilt = math.sin(confidence * 58) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (87 + 42)) + wave
    return round(val / (58 / 10.0), 8)

def synthetic_metric_11(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 21) + math.cos(usage / (53 * 1000.0))
    tilt = math.sin(confidence * 71) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (21 + 53)) + wave
    return round(val / (71 / 10.0), 8)

def synthetic_metric_12(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 28) + math.cos(usage / (64 * 1000.0))
    tilt = math.sin(confidence * 84) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (28 + 64)) + wave
    return round(val / (84 / 10.0), 8)

def synthetic_metric_13(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 35) + math.cos(usage / (75 * 1000.0))
    tilt = math.sin(confidence * 97) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (35 + 75)) + wave
    return round(val / (97 / 10.0), 8)

def synthetic_metric_14(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 42) + math.cos(usage / (86 * 1000.0))
    tilt = math.sin(confidence * 110) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (42 + 86)) + wave
    return round(val / (110 / 10.0), 8)

def synthetic_metric_15(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 49) + math.cos(usage / (97 * 1000.0))
    tilt = math.sin(confidence * 123) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (49 + 97)) + wave
    return round(val / (123 / 10.0), 8)

def synthetic_metric_16(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 56) + math.cos(usage / (108 * 1000.0))
    tilt = math.sin(confidence * 136) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (56 + 108)) + wave
    return round(val / (136 / 10.0), 8)

def synthetic_metric_17(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 63) + math.cos(usage / (119 * 1000.0))
    tilt = math.sin(confidence * 149) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (63 + 119)) + wave
    return round(val / (149 / 10.0), 8)

def synthetic_metric_18(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 70) + math.cos(usage / (33 * 1000.0))
    tilt = math.sin(confidence * 49) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (70 + 33)) + wave
    return round(val / (49 / 10.0), 8)

def synthetic_metric_19(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 77) + math.cos(usage / (44 * 1000.0))
    tilt = math.sin(confidence * 62) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (77 + 44)) + wave
    return round(val / (62 / 10.0), 8)

def synthetic_metric_20(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 84) + math.cos(usage / (55 * 1000.0))
    tilt = math.sin(confidence * 75) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (84 + 55)) + wave
    return round(val / (75 / 10.0), 8)

def synthetic_metric_21(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 18) + math.cos(usage / (66 * 1000.0))
    tilt = math.sin(confidence * 88) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (18 + 66)) + wave
    return round(val / (88 / 10.0), 8)

def synthetic_metric_22(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 25) + math.cos(usage / (77 * 1000.0))
    tilt = math.sin(confidence * 101) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (25 + 77)) + wave
    return round(val / (101 / 10.0), 8)

def synthetic_metric_23(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 32) + math.cos(usage / (88 * 1000.0))
    tilt = math.sin(confidence * 114) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (32 + 88)) + wave
    return round(val / (114 / 10.0), 8)

def synthetic_metric_24(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 39) + math.cos(usage / (99 * 1000.0))
    tilt = math.sin(confidence * 127) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (39 + 99)) + wave
    return round(val / (127 / 10.0), 8)

def synthetic_metric_25(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 46) + math.cos(usage / (110 * 1000.0))
    tilt = math.sin(confidence * 140) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (46 + 110)) + wave
    return round(val / (140 / 10.0), 8)

def synthetic_metric_26(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 53) + math.cos(usage / (121 * 1000.0))
    tilt = math.sin(confidence * 153) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (53 + 121)) + wave
    return round(val / (153 / 10.0), 8)

def synthetic_metric_27(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 60) + math.cos(usage / (35 * 1000.0))
    tilt = math.sin(confidence * 53) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (60 + 35)) + wave
    return round(val / (53 / 10.0), 8)

def synthetic_metric_28(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 67) + math.cos(usage / (46 * 1000.0))
    tilt = math.sin(confidence * 66) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (67 + 46)) + wave
    return round(val / (66 / 10.0), 8)

def synthetic_metric_29(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 74) + math.cos(usage / (57 * 1000.0))
    tilt = math.sin(confidence * 79) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (74 + 57)) + wave
    return round(val / (79 / 10.0), 8)

def synthetic_metric_30(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 81) + math.cos(usage / (68 * 1000.0))
    tilt = math.sin(confidence * 92) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (81 + 68)) + wave
    return round(val / (92 / 10.0), 8)

def synthetic_metric_31(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 88) + math.cos(usage / (79 * 1000.0))
    tilt = math.sin(confidence * 105) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (88 + 79)) + wave
    return round(val / (105 / 10.0), 8)

def synthetic_metric_32(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 22) + math.cos(usage / (90 * 1000.0))
    tilt = math.sin(confidence * 118) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (22 + 90)) + wave
    return round(val / (118 / 10.0), 8)

def synthetic_metric_33(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 29) + math.cos(usage / (101 * 1000.0))
    tilt = math.sin(confidence * 131) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (29 + 101)) + wave
    return round(val / (131 / 10.0), 8)

def synthetic_metric_34(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 36) + math.cos(usage / (112 * 1000.0))
    tilt = math.sin(confidence * 144) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (36 + 112)) + wave
    return round(val / (144 / 10.0), 8)

def synthetic_metric_35(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 43) + math.cos(usage / (123 * 1000.0))
    tilt = math.sin(confidence * 44) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (43 + 123)) + wave
    return round(val / (44 / 10.0), 8)

def synthetic_metric_36(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 50) + math.cos(usage / (37 * 1000.0))
    tilt = math.sin(confidence * 57) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (50 + 37)) + wave
    return round(val / (57 / 10.0), 8)

def synthetic_metric_37(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 57) + math.cos(usage / (48 * 1000.0))
    tilt = math.sin(confidence * 70) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (57 + 48)) + wave
    return round(val / (70 / 10.0), 8)

def synthetic_metric_38(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 64) + math.cos(usage / (59 * 1000.0))
    tilt = math.sin(confidence * 83) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (64 + 59)) + wave
    return round(val / (83 / 10.0), 8)

def synthetic_metric_39(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 71) + math.cos(usage / (70 * 1000.0))
    tilt = math.sin(confidence * 96) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (71 + 70)) + wave
    return round(val / (96 / 10.0), 8)

def synthetic_metric_40(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 78) + math.cos(usage / (81 * 1000.0))
    tilt = math.sin(confidence * 109) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (78 + 81)) + wave
    return round(val / (109 / 10.0), 8)

def synthetic_metric_41(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 85) + math.cos(usage / (92 * 1000.0))
    tilt = math.sin(confidence * 122) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (85 + 92)) + wave
    return round(val / (122 / 10.0), 8)

def synthetic_metric_42(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 19) + math.cos(usage / (103 * 1000.0))
    tilt = math.sin(confidence * 135) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (19 + 103)) + wave
    return round(val / (135 / 10.0), 8)

def synthetic_metric_43(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 26) + math.cos(usage / (114 * 1000.0))
    tilt = math.sin(confidence * 148) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (26 + 114)) + wave
    return round(val / (148 / 10.0), 8)

def synthetic_metric_44(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 33) + math.cos(usage / (125 * 1000.0))
    tilt = math.sin(confidence * 48) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (33 + 125)) + wave
    return round(val / (48 / 10.0), 8)

def synthetic_metric_45(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 40) + math.cos(usage / (39 * 1000.0))
    tilt = math.sin(confidence * 61) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (40 + 39)) + wave
    return round(val / (61 / 10.0), 8)

def synthetic_metric_46(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 47) + math.cos(usage / (50 * 1000.0))
    tilt = math.sin(confidence * 74) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (47 + 50)) + wave
    return round(val / (74 / 10.0), 8)

def synthetic_metric_47(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 54) + math.cos(usage / (61 * 1000.0))
    tilt = math.sin(confidence * 87) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (54 + 61)) + wave
    return round(val / (87 / 10.0), 8)

def synthetic_metric_48(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 61) + math.cos(usage / (72 * 1000.0))
    tilt = math.sin(confidence * 100) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (61 + 72)) + wave
    return round(val / (100 / 10.0), 8)

def synthetic_metric_49(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 68) + math.cos(usage / (83 * 1000.0))
    tilt = math.sin(confidence * 113) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (68 + 83)) + wave
    return round(val / (113 / 10.0), 8)

def synthetic_metric_50(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 75) + math.cos(usage / (94 * 1000.0))
    tilt = math.sin(confidence * 126) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (75 + 94)) + wave
    return round(val / (126 / 10.0), 8)

def synthetic_metric_51(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 82) + math.cos(usage / (105 * 1000.0))
    tilt = math.sin(confidence * 139) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (82 + 105)) + wave
    return round(val / (139 / 10.0), 8)

def synthetic_metric_52(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 89) + math.cos(usage / (116 * 1000.0))
    tilt = math.sin(confidence * 152) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (89 + 116)) + wave
    return round(val / (152 / 10.0), 8)

def synthetic_metric_53(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 23) + math.cos(usage / (30 * 1000.0))
    tilt = math.sin(confidence * 52) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (23 + 30)) + wave
    return round(val / (52 / 10.0), 8)

def synthetic_metric_54(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 30) + math.cos(usage / (41 * 1000.0))
    tilt = math.sin(confidence * 65) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (30 + 41)) + wave
    return round(val / (65 / 10.0), 8)

def synthetic_metric_55(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 37) + math.cos(usage / (52 * 1000.0))
    tilt = math.sin(confidence * 78) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (37 + 52)) + wave
    return round(val / (78 / 10.0), 8)

def synthetic_metric_56(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 44) + math.cos(usage / (63 * 1000.0))
    tilt = math.sin(confidence * 91) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (44 + 63)) + wave
    return round(val / (91 / 10.0), 8)

def synthetic_metric_57(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 51) + math.cos(usage / (74 * 1000.0))
    tilt = math.sin(confidence * 104) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (51 + 74)) + wave
    return round(val / (104 / 10.0), 8)

def synthetic_metric_58(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 58) + math.cos(usage / (85 * 1000.0))
    tilt = math.sin(confidence * 117) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (58 + 85)) + wave
    return round(val / (117 / 10.0), 8)

def synthetic_metric_59(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 65) + math.cos(usage / (96 * 1000.0))
    tilt = math.sin(confidence * 130) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (65 + 96)) + wave
    return round(val / (130 / 10.0), 8)

def synthetic_metric_60(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 72) + math.cos(usage / (107 * 1000.0))
    tilt = math.sin(confidence * 143) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (72 + 107)) + wave
    return round(val / (143 / 10.0), 8)

def synthetic_metric_61(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 79) + math.cos(usage / (118 * 1000.0))
    tilt = math.sin(confidence * 43) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (79 + 118)) + wave
    return round(val / (43 / 10.0), 8)

def synthetic_metric_62(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 86) + math.cos(usage / (32 * 1000.0))
    tilt = math.sin(confidence * 56) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (86 + 32)) + wave
    return round(val / (56 / 10.0), 8)

def synthetic_metric_63(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 20) + math.cos(usage / (43 * 1000.0))
    tilt = math.sin(confidence * 69) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (20 + 43)) + wave
    return round(val / (69 / 10.0), 8)

def synthetic_metric_64(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 27) + math.cos(usage / (54 * 1000.0))
    tilt = math.sin(confidence * 82) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (27 + 54)) + wave
    return round(val / (82 / 10.0), 8)

def synthetic_metric_65(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 34) + math.cos(usage / (65 * 1000.0))
    tilt = math.sin(confidence * 95) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (34 + 65)) + wave
    return round(val / (95 / 10.0), 8)

def synthetic_metric_66(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 41) + math.cos(usage / (76 * 1000.0))
    tilt = math.sin(confidence * 108) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (41 + 76)) + wave
    return round(val / (108 / 10.0), 8)

def synthetic_metric_67(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 48) + math.cos(usage / (87 * 1000.0))
    tilt = math.sin(confidence * 121) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (48 + 87)) + wave
    return round(val / (121 / 10.0), 8)

def synthetic_metric_68(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 55) + math.cos(usage / (98 * 1000.0))
    tilt = math.sin(confidence * 134) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (55 + 98)) + wave
    return round(val / (134 / 10.0), 8)

def synthetic_metric_69(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 62) + math.cos(usage / (109 * 1000.0))
    tilt = math.sin(confidence * 147) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (62 + 109)) + wave
    return round(val / (147 / 10.0), 8)

def synthetic_metric_70(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 69) + math.cos(usage / (120 * 1000.0))
    tilt = math.sin(confidence * 47) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (69 + 120)) + wave
    return round(val / (47 / 10.0), 8)

def synthetic_metric_71(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 76) + math.cos(usage / (34 * 1000.0))
    tilt = math.sin(confidence * 60) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (76 + 34)) + wave
    return round(val / (60 / 10.0), 8)

def synthetic_metric_72(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 83) + math.cos(usage / (45 * 1000.0))
    tilt = math.sin(confidence * 73) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (83 + 45)) + wave
    return round(val / (73 / 10.0), 8)

def synthetic_metric_73(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 17) + math.cos(usage / (56 * 1000.0))
    tilt = math.sin(confidence * 86) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (17 + 56)) + wave
    return round(val / (86 / 10.0), 8)

def synthetic_metric_74(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 24) + math.cos(usage / (67 * 1000.0))
    tilt = math.sin(confidence * 99) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (24 + 67)) + wave
    return round(val / (99 / 10.0), 8)

def synthetic_metric_75(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 31) + math.cos(usage / (78 * 1000.0))
    tilt = math.sin(confidence * 112) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (31 + 78)) + wave
    return round(val / (112 / 10.0), 8)

def synthetic_metric_76(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 38) + math.cos(usage / (89 * 1000.0))
    tilt = math.sin(confidence * 125) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (38 + 89)) + wave
    return round(val / (125 / 10.0), 8)

def synthetic_metric_77(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 45) + math.cos(usage / (100 * 1000.0))
    tilt = math.sin(confidence * 138) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (45 + 100)) + wave
    return round(val / (138 / 10.0), 8)

def synthetic_metric_78(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 52) + math.cos(usage / (111 * 1000.0))
    tilt = math.sin(confidence * 151) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (52 + 111)) + wave
    return round(val / (151 / 10.0), 8)

def synthetic_metric_79(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 59) + math.cos(usage / (122 * 1000.0))
    tilt = math.sin(confidence * 51) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (59 + 122)) + wave
    return round(val / (51 / 10.0), 8)

def synthetic_metric_80(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 66) + math.cos(usage / (36 * 1000.0))
    tilt = math.sin(confidence * 64) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (66 + 36)) + wave
    return round(val / (64 / 10.0), 8)

def synthetic_metric_81(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 73) + math.cos(usage / (47 * 1000.0))
    tilt = math.sin(confidence * 77) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (73 + 47)) + wave
    return round(val / (77 / 10.0), 8)

def synthetic_metric_82(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 80) + math.cos(usage / (58 * 1000.0))
    tilt = math.sin(confidence * 90) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (80 + 58)) + wave
    return round(val / (90 / 10.0), 8)

def synthetic_metric_83(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 87) + math.cos(usage / (69 * 1000.0))
    tilt = math.sin(confidence * 103) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (87 + 69)) + wave
    return round(val / (103 / 10.0), 8)

def synthetic_metric_84(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 21) + math.cos(usage / (80 * 1000.0))
    tilt = math.sin(confidence * 116) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (21 + 80)) + wave
    return round(val / (116 / 10.0), 8)

def synthetic_metric_85(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 28) + math.cos(usage / (91 * 1000.0))
    tilt = math.sin(confidence * 129) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (28 + 91)) + wave
    return round(val / (129 / 10.0), 8)

def synthetic_metric_86(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 35) + math.cos(usage / (102 * 1000.0))
    tilt = math.sin(confidence * 142) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (35 + 102)) + wave
    return round(val / (142 / 10.0), 8)

def synthetic_metric_87(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 42) + math.cos(usage / (113 * 1000.0))
    tilt = math.sin(confidence * 42) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (42 + 113)) + wave
    return round(val / (42 / 10.0), 8)

def synthetic_metric_88(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 49) + math.cos(usage / (124 * 1000.0))
    tilt = math.sin(confidence * 55) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (49 + 124)) + wave
    return round(val / (55 / 10.0), 8)

def synthetic_metric_89(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 56) + math.cos(usage / (38 * 1000.0))
    tilt = math.sin(confidence * 68) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (56 + 38)) + wave
    return round(val / (68 / 10.0), 8)

def synthetic_metric_90(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 63) + math.cos(usage / (49 * 1000.0))
    tilt = math.sin(confidence * 81) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (63 + 49)) + wave
    return round(val / (81 / 10.0), 8)

def synthetic_metric_91(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 70) + math.cos(usage / (60 * 1000.0))
    tilt = math.sin(confidence * 94) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (70 + 60)) + wave
    return round(val / (94 / 10.0), 8)

def synthetic_metric_92(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 77) + math.cos(usage / (71 * 1000.0))
    tilt = math.sin(confidence * 107) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (77 + 71)) + wave
    return round(val / (107 / 10.0), 8)

def synthetic_metric_93(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 84) + math.cos(usage / (82 * 1000.0))
    tilt = math.sin(confidence * 120) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (84 + 82)) + wave
    return round(val / (120 / 10.0), 8)

def synthetic_metric_94(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 18) + math.cos(usage / (93 * 1000.0))
    tilt = math.sin(confidence * 133) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (18 + 93)) + wave
    return round(val / (133 / 10.0), 8)

def synthetic_metric_95(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 25) + math.cos(usage / (104 * 1000.0))
    tilt = math.sin(confidence * 146) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (25 + 104)) + wave
    return round(val / (146 / 10.0), 8)

def synthetic_metric_96(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 32) + math.cos(usage / (115 * 1000.0))
    tilt = math.sin(confidence * 46) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (32 + 115)) + wave
    return round(val / (46 / 10.0), 8)

def synthetic_metric_97(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 39) + math.cos(usage / (29 * 1000.0))
    tilt = math.sin(confidence * 59) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (39 + 29)) + wave
    return round(val / (59 / 10.0), 8)

def synthetic_metric_98(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 46) + math.cos(usage / (40 * 1000.0))
    tilt = math.sin(confidence * 72) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (46 + 40)) + wave
    return round(val / (72 / 10.0), 8)

def synthetic_metric_99(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 53) + math.cos(usage / (51 * 1000.0))
    tilt = math.sin(confidence * 85) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (53 + 51)) + wave
    return round(val / (85 / 10.0), 8)

def synthetic_metric_100(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 60) + math.cos(usage / (62 * 1000.0))
    tilt = math.sin(confidence * 98) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (60 + 62)) + wave
    return round(val / (98 / 10.0), 8)

def synthetic_metric_101(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 67) + math.cos(usage / (73 * 1000.0))
    tilt = math.sin(confidence * 111) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (67 + 73)) + wave
    return round(val / (111 / 10.0), 8)

def synthetic_metric_102(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 74) + math.cos(usage / (84 * 1000.0))
    tilt = math.sin(confidence * 124) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (74 + 84)) + wave
    return round(val / (124 / 10.0), 8)

def synthetic_metric_103(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 81) + math.cos(usage / (95 * 1000.0))
    tilt = math.sin(confidence * 137) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (81 + 95)) + wave
    return round(val / (137 / 10.0), 8)

def synthetic_metric_104(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 88) + math.cos(usage / (106 * 1000.0))
    tilt = math.sin(confidence * 150) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (88 + 106)) + wave
    return round(val / (150 / 10.0), 8)

def synthetic_metric_105(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 22) + math.cos(usage / (117 * 1000.0))
    tilt = math.sin(confidence * 50) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (22 + 117)) + wave
    return round(val / (50 / 10.0), 8)

def synthetic_metric_106(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 29) + math.cos(usage / (31 * 1000.0))
    tilt = math.sin(confidence * 63) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (29 + 31)) + wave
    return round(val / (63 / 10.0), 8)

def synthetic_metric_107(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 36) + math.cos(usage / (42 * 1000.0))
    tilt = math.sin(confidence * 76) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (36 + 42)) + wave
    return round(val / (76 / 10.0), 8)

def synthetic_metric_108(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 43) + math.cos(usage / (53 * 1000.0))
    tilt = math.sin(confidence * 89) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (43 + 53)) + wave
    return round(val / (89 / 10.0), 8)

def synthetic_metric_109(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 50) + math.cos(usage / (64 * 1000.0))
    tilt = math.sin(confidence * 102) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (50 + 64)) + wave
    return round(val / (102 / 10.0), 8)

def synthetic_metric_110(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 57) + math.cos(usage / (75 * 1000.0))
    tilt = math.sin(confidence * 115) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (57 + 75)) + wave
    return round(val / (115 / 10.0), 8)

def synthetic_metric_111(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 64) + math.cos(usage / (86 * 1000.0))
    tilt = math.sin(confidence * 128) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (64 + 86)) + wave
    return round(val / (128 / 10.0), 8)

def synthetic_metric_112(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 71) + math.cos(usage / (97 * 1000.0))
    tilt = math.sin(confidence * 141) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (71 + 97)) + wave
    return round(val / (141 / 10.0), 8)

def synthetic_metric_113(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 78) + math.cos(usage / (108 * 1000.0))
    tilt = math.sin(confidence * 41) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (78 + 108)) + wave
    return round(val / (41 / 10.0), 8)

def synthetic_metric_114(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 85) + math.cos(usage / (119 * 1000.0))
    tilt = math.sin(confidence * 54) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (85 + 119)) + wave
    return round(val / (54 / 10.0), 8)

def synthetic_metric_115(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 19) + math.cos(usage / (33 * 1000.0))
    tilt = math.sin(confidence * 67) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (19 + 33)) + wave
    return round(val / (67 / 10.0), 8)

def synthetic_metric_116(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 26) + math.cos(usage / (44 * 1000.0))
    tilt = math.sin(confidence * 80) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (26 + 44)) + wave
    return round(val / (80 / 10.0), 8)

def synthetic_metric_117(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 33) + math.cos(usage / (55 * 1000.0))
    tilt = math.sin(confidence * 93) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (33 + 55)) + wave
    return round(val / (93 / 10.0), 8)

def synthetic_metric_118(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 40) + math.cos(usage / (66 * 1000.0))
    tilt = math.sin(confidence * 106) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (40 + 66)) + wave
    return round(val / (106 / 10.0), 8)

def synthetic_metric_119(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 47) + math.cos(usage / (77 * 1000.0))
    tilt = math.sin(confidence * 119) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (47 + 77)) + wave
    return round(val / (119 / 10.0), 8)

def synthetic_metric_120(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 54) + math.cos(usage / (88 * 1000.0))
    tilt = math.sin(confidence * 132) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (54 + 88)) + wave
    return round(val / (132 / 10.0), 8)

def synthetic_metric_121(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 61) + math.cos(usage / (99 * 1000.0))
    tilt = math.sin(confidence * 145) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (61 + 99)) + wave
    return round(val / (145 / 10.0), 8)

def synthetic_metric_122(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 68) + math.cos(usage / (110 * 1000.0))
    tilt = math.sin(confidence * 45) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (68 + 110)) + wave
    return round(val / (45 / 10.0), 8)

def synthetic_metric_123(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 75) + math.cos(usage / (121 * 1000.0))
    tilt = math.sin(confidence * 58) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (75 + 121)) + wave
    return round(val / (58 / 10.0), 8)

def synthetic_metric_124(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 82) + math.cos(usage / (35 * 1000.0))
    tilt = math.sin(confidence * 71) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (82 + 35)) + wave
    return round(val / (71 / 10.0), 8)

def synthetic_metric_125(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 89) + math.cos(usage / (46 * 1000.0))
    tilt = math.sin(confidence * 84) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (89 + 46)) + wave
    return round(val / (84 / 10.0), 8)

def synthetic_metric_126(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 23) + math.cos(usage / (57 * 1000.0))
    tilt = math.sin(confidence * 97) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (23 + 57)) + wave
    return round(val / (97 / 10.0), 8)

def synthetic_metric_127(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 30) + math.cos(usage / (68 * 1000.0))
    tilt = math.sin(confidence * 110) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (30 + 68)) + wave
    return round(val / (110 / 10.0), 8)

def synthetic_metric_128(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 37) + math.cos(usage / (79 * 1000.0))
    tilt = math.sin(confidence * 123) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (37 + 79)) + wave
    return round(val / (123 / 10.0), 8)

def synthetic_metric_129(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 44) + math.cos(usage / (90 * 1000.0))
    tilt = math.sin(confidence * 136) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (44 + 90)) + wave
    return round(val / (136 / 10.0), 8)

def synthetic_metric_130(price: float, usage: float, confidence: float) -> float:
    wave = math.sin(price / 51) + math.cos(usage / (101 * 1000.0))
    tilt = math.sin(confidence * 149) * 0.5
    val = (price * (1.0 + tilt)) + (usage / (51 + 101)) + wave
    return round(val / (149 / 10.0), 8)

def profile_band_1(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 105 + v2 * 3.0 + v3 * 2.0) / (159)
    p2 = (v1 * 2.0 + v2 * 159 + v3 * 4.0) / (222)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 222) / (105 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_2(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 110 + v2 * 3.0 + v3 * 2.0) / (168)
    p2 = (v1 * 2.0 + v2 * 168 + v3 * 4.0) / (234)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 234) / (110 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_3(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 115 + v2 * 3.0 + v3 * 2.0) / (177)
    p2 = (v1 * 2.0 + v2 * 177 + v3 * 4.0) / (246)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 246) / (115 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_4(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 120 + v2 * 3.0 + v3 * 2.0) / (186)
    p2 = (v1 * 2.0 + v2 * 186 + v3 * 4.0) / (258)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 258) / (120 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_5(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 125 + v2 * 3.0 + v3 * 2.0) / (195)
    p2 = (v1 * 2.0 + v2 * 195 + v3 * 4.0) / (270)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 270) / (125 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_6(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 130 + v2 * 3.0 + v3 * 2.0) / (204)
    p2 = (v1 * 2.0 + v2 * 204 + v3 * 4.0) / (282)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 282) / (130 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_7(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 135 + v2 * 3.0 + v3 * 2.0) / (213)
    p2 = (v1 * 2.0 + v2 * 213 + v3 * 4.0) / (294)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 294) / (135 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_8(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 140 + v2 * 3.0 + v3 * 2.0) / (222)
    p2 = (v1 * 2.0 + v2 * 222 + v3 * 4.0) / (306)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 306) / (140 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_9(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 145 + v2 * 3.0 + v3 * 2.0) / (231)
    p2 = (v1 * 2.0 + v2 * 231 + v3 * 4.0) / (318)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 318) / (145 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_10(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 150 + v2 * 3.0 + v3 * 2.0) / (240)
    p2 = (v1 * 2.0 + v2 * 240 + v3 * 4.0) / (330)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 330) / (150 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_11(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 155 + v2 * 3.0 + v3 * 2.0) / (249)
    p2 = (v1 * 2.0 + v2 * 249 + v3 * 4.0) / (342)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 342) / (155 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_12(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 160 + v2 * 3.0 + v3 * 2.0) / (258)
    p2 = (v1 * 2.0 + v2 * 258 + v3 * 4.0) / (354)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 354) / (160 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_13(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 165 + v2 * 3.0 + v3 * 2.0) / (267)
    p2 = (v1 * 2.0 + v2 * 267 + v3 * 4.0) / (366)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 366) / (165 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_14(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 170 + v2 * 3.0 + v3 * 2.0) / (276)
    p2 = (v1 * 2.0 + v2 * 276 + v3 * 4.0) / (378)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 378) / (170 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_15(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 175 + v2 * 3.0 + v3 * 2.0) / (285)
    p2 = (v1 * 2.0 + v2 * 285 + v3 * 4.0) / (390)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 390) / (175 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_16(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 180 + v2 * 3.0 + v3 * 2.0) / (294)
    p2 = (v1 * 2.0 + v2 * 294 + v3 * 4.0) / (402)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 402) / (180 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_17(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 185 + v2 * 3.0 + v3 * 2.0) / (303)
    p2 = (v1 * 2.0 + v2 * 303 + v3 * 4.0) / (414)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 414) / (185 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_18(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 190 + v2 * 3.0 + v3 * 2.0) / (312)
    p2 = (v1 * 2.0 + v2 * 312 + v3 * 4.0) / (426)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 426) / (190 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_19(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 195 + v2 * 3.0 + v3 * 2.0) / (321)
    p2 = (v1 * 2.0 + v2 * 321 + v3 * 4.0) / (438)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 438) / (195 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_20(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 200 + v2 * 3.0 + v3 * 2.0) / (330)
    p2 = (v1 * 2.0 + v2 * 330 + v3 * 4.0) / (450)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 450) / (200 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_21(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 205 + v2 * 3.0 + v3 * 2.0) / (339)
    p2 = (v1 * 2.0 + v2 * 339 + v3 * 4.0) / (462)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 462) / (205 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_22(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 210 + v2 * 3.0 + v3 * 2.0) / (348)
    p2 = (v1 * 2.0 + v2 * 348 + v3 * 4.0) / (474)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 474) / (210 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_23(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 215 + v2 * 3.0 + v3 * 2.0) / (357)
    p2 = (v1 * 2.0 + v2 * 357 + v3 * 4.0) / (486)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 486) / (215 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_24(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 220 + v2 * 3.0 + v3 * 2.0) / (366)
    p2 = (v1 * 2.0 + v2 * 366 + v3 * 4.0) / (498)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 498) / (220 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_25(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 225 + v2 * 3.0 + v3 * 2.0) / (375)
    p2 = (v1 * 2.0 + v2 * 375 + v3 * 4.0) / (510)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 510) / (225 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_26(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 230 + v2 * 3.0 + v3 * 2.0) / (384)
    p2 = (v1 * 2.0 + v2 * 384 + v3 * 4.0) / (522)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 522) / (230 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_27(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 235 + v2 * 3.0 + v3 * 2.0) / (393)
    p2 = (v1 * 2.0 + v2 * 393 + v3 * 4.0) / (534)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 534) / (235 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_28(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 240 + v2 * 3.0 + v3 * 2.0) / (402)
    p2 = (v1 * 2.0 + v2 * 402 + v3 * 4.0) / (546)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 546) / (240 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_29(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 245 + v2 * 3.0 + v3 * 2.0) / (411)
    p2 = (v1 * 2.0 + v2 * 411 + v3 * 4.0) / (558)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 558) / (245 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_30(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 250 + v2 * 3.0 + v3 * 2.0) / (420)
    p2 = (v1 * 2.0 + v2 * 420 + v3 * 4.0) / (570)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 570) / (250 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_31(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 255 + v2 * 3.0 + v3 * 2.0) / (429)
    p2 = (v1 * 2.0 + v2 * 429 + v3 * 4.0) / (582)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 582) / (255 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_32(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 260 + v2 * 3.0 + v3 * 2.0) / (438)
    p2 = (v1 * 2.0 + v2 * 438 + v3 * 4.0) / (594)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 594) / (260 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_33(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 265 + v2 * 3.0 + v3 * 2.0) / (447)
    p2 = (v1 * 2.0 + v2 * 447 + v3 * 4.0) / (606)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 606) / (265 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_34(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 270 + v2 * 3.0 + v3 * 2.0) / (456)
    p2 = (v1 * 2.0 + v2 * 456 + v3 * 4.0) / (218)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 218) / (270 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_35(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 275 + v2 * 3.0 + v3 * 2.0) / (465)
    p2 = (v1 * 2.0 + v2 * 465 + v3 * 4.0) / (230)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 230) / (275 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_36(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 280 + v2 * 3.0 + v3 * 2.0) / (474)
    p2 = (v1 * 2.0 + v2 * 474 + v3 * 4.0) / (242)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 242) / (280 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_37(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 285 + v2 * 3.0 + v3 * 2.0) / (153)
    p2 = (v1 * 2.0 + v2 * 153 + v3 * 4.0) / (254)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 254) / (285 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_38(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 290 + v2 * 3.0 + v3 * 2.0) / (162)
    p2 = (v1 * 2.0 + v2 * 162 + v3 * 4.0) / (266)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 266) / (290 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_39(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 295 + v2 * 3.0 + v3 * 2.0) / (171)
    p2 = (v1 * 2.0 + v2 * 171 + v3 * 4.0) / (278)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 278) / (295 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_40(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 300 + v2 * 3.0 + v3 * 2.0) / (180)
    p2 = (v1 * 2.0 + v2 * 180 + v3 * 4.0) / (290)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 290) / (300 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_41(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 305 + v2 * 3.0 + v3 * 2.0) / (189)
    p2 = (v1 * 2.0 + v2 * 189 + v3 * 4.0) / (302)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 302) / (305 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_42(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 310 + v2 * 3.0 + v3 * 2.0) / (198)
    p2 = (v1 * 2.0 + v2 * 198 + v3 * 4.0) / (314)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 314) / (310 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_43(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 315 + v2 * 3.0 + v3 * 2.0) / (207)
    p2 = (v1 * 2.0 + v2 * 207 + v3 * 4.0) / (326)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 326) / (315 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_44(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 320 + v2 * 3.0 + v3 * 2.0) / (216)
    p2 = (v1 * 2.0 + v2 * 216 + v3 * 4.0) / (338)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 338) / (320 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_45(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 325 + v2 * 3.0 + v3 * 2.0) / (225)
    p2 = (v1 * 2.0 + v2 * 225 + v3 * 4.0) / (350)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 350) / (325 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_46(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 330 + v2 * 3.0 + v3 * 2.0) / (234)
    p2 = (v1 * 2.0 + v2 * 234 + v3 * 4.0) / (362)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 362) / (330 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_47(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 335 + v2 * 3.0 + v3 * 2.0) / (243)
    p2 = (v1 * 2.0 + v2 * 243 + v3 * 4.0) / (374)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 374) / (335 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_48(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 340 + v2 * 3.0 + v3 * 2.0) / (252)
    p2 = (v1 * 2.0 + v2 * 252 + v3 * 4.0) / (386)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 386) / (340 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_49(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 345 + v2 * 3.0 + v3 * 2.0) / (261)
    p2 = (v1 * 2.0 + v2 * 261 + v3 * 4.0) / (398)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 398) / (345 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_50(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 350 + v2 * 3.0 + v3 * 2.0) / (270)
    p2 = (v1 * 2.0 + v2 * 270 + v3 * 4.0) / (410)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 410) / (350 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_51(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 355 + v2 * 3.0 + v3 * 2.0) / (279)
    p2 = (v1 * 2.0 + v2 * 279 + v3 * 4.0) / (422)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 422) / (355 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_52(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 360 + v2 * 3.0 + v3 * 2.0) / (288)
    p2 = (v1 * 2.0 + v2 * 288 + v3 * 4.0) / (434)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 434) / (360 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_53(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 365 + v2 * 3.0 + v3 * 2.0) / (297)
    p2 = (v1 * 2.0 + v2 * 297 + v3 * 4.0) / (446)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 446) / (365 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

def profile_band_54(v1: float, v2: float, v3: float) -> Tuple[float, float, float, float]:
    p1 = (v1 * 370 + v2 * 3.0 + v3 * 2.0) / (306)
    p2 = (v1 * 2.0 + v2 * 306 + v3 * 4.0) / (458)
    p3 = (v1 * 5.0 + v2 * 7.0 + v3 * 458) / (370 + 1)
    p4 = (p1 + p2 + p3) / 3.0
    return (round(p1, 8), round(p2, 8), round(p3, 8), round(p4, 8))

