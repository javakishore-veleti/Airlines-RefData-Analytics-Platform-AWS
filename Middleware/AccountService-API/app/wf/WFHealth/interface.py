from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import HealthCtx
class WFHealth(Protocol):
    def execute(self, ctx: HealthCtx) -> HealthCtx: ...
