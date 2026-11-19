"""Shared Ctx / Req / Resp DTOs for MasterData-API use cases (D3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HealthReq:
    """Empty request — Health needs no input beyond process config."""


@dataclass
class HealthResp:
    status: str = "unknown"
    mysql: bool = False
    detail: Optional[str] = None


@dataclass
class HealthCtx:
    req: HealthReq = field(default_factory=HealthReq)
    resp: HealthResp = field(default_factory=HealthResp)


@dataclass
class GenerateCdcEventsReq:
    count: int = 1


@dataclass
class GenerateCdcEventsResp:
    requested: int = 0
    inserted: int = 0
    updated: int = 0
    deleted: int = 0
    message: str = ""


@dataclass
class GenerateCdcEventsCtx:
    req: GenerateCdcEventsReq = field(default_factory=GenerateCdcEventsReq)
    resp: GenerateCdcEventsResp = field(default_factory=GenerateCdcEventsResp)


@dataclass
class MarketRuleWriteReq:
    name: str = ""
    weight: int = 1
    status: str = "ACTIVE"
    market_from: str = "ORD"
    market_to: str = "SFO"
    rule_id: int | None = None


@dataclass
class MarketRuleWriteResp:
    rule_id: int | None = None
    ok: bool = False
    message: str = ""


@dataclass
class MarketRuleWriteCtx:
    req: MarketRuleWriteReq = field(default_factory=MarketRuleWriteReq)
    resp: MarketRuleWriteResp = field(default_factory=MarketRuleWriteResp)
