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
