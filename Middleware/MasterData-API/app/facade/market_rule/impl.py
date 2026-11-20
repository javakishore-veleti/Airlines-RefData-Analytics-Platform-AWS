from __future__ import annotations
from app.common.dtos.usecase import MarketRuleWriteCtx
from app.wf.WFMarketRuleWrite.interface import WFMarketRuleWrite

class MarketRuleFacadeImpl:
    def __init__(self, wf: WFMarketRuleWrite) -> None:
        self._wf = wf

    def list(self, limit: int = 100):
        return self._wf.list(limit)

    def create(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        return self._wf.create(ctx)

    def update(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        return self._wf.update(ctx)

    def deactivate(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        return self._wf.deactivate(ctx)
