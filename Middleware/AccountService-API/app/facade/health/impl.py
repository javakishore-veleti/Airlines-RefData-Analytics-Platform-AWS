from __future__ import annotations
from app.common.dtos.usecase import HealthCtx
from app.wf.WFHealth.interface import WFHealth
class HealthFacadeImpl:
    def __init__(self, wf: WFHealth) -> None:
        self._wf = wf
    def check(self, ctx: HealthCtx) -> HealthCtx:
        return self._wf.execute(ctx)
