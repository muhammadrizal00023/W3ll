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
