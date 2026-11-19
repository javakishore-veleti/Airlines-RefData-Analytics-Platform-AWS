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
