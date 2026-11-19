from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class HealthReq:
    pass

@dataclass
class HealthResp:
    status: str = "unknown"
    mysql: bool = False
    detail: Optional[str] = None

@dataclass
class HealthCtx:
    req: HealthReq = field(default_factory=HealthReq)
    resp: HealthResp = field(default_factory=HealthResp)
