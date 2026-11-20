from __future__ import annotations
from app.common.dtos.usecase import MarketRuleWriteCtx
from app.dao.market_rule_dao import MarketRuleDao

class WFMarketRuleWriteImpl:
    def __init__(self, dao: MarketRuleDao) -> None:
        self._dao = dao

    def list(self, limit: int = 100):
        return self._dao.list_rules(limit=limit)

    def create(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        r = ctx.req
        rule_id = self._dao.create(r.name, r.weight, r.status, r.market_from, r.market_to)
        ctx.resp.rule_id = rule_id
        ctx.resp.ok = True
        ctx.resp.message = "created"
        return ctx

    def update(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        r = ctx.req
        assert r.rule_id is not None
        ok = self._dao.update(r.rule_id, r.name, r.weight, r.status, r.market_from, r.market_to)
        ctx.resp.rule_id = r.rule_id
        ctx.resp.ok = ok
        ctx.resp.message = "updated" if ok else "not found"
        return ctx

    def deactivate(self, ctx: MarketRuleWriteCtx) -> MarketRuleWriteCtx:
        r = ctx.req
        assert r.rule_id is not None
        ok = self._dao.deactivate(r.rule_id)
        ctx.resp.rule_id = r.rule_id
        ctx.resp.ok = ok
        ctx.resp.message = "deactivated" if ok else "not found"
        return ctx
