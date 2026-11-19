from __future__ import annotations
from app.common.dtos.usecase import GenerateCdcEventsCtx
from app.dao.market_rule_dao import MarketRuleDao

class GenerateMixTask:
    def __init__(self, dao: MarketRuleDao) -> None:
        self._dao = dao

    def run(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx:
        inserted, updated, deleted = self._dao.generate_cdc_mix(ctx.req.count)
        ctx.resp.requested = ctx.req.count
        ctx.resp.inserted = inserted
        ctx.resp.updated = updated
        ctx.resp.deleted = deleted
        total = inserted + updated + deleted
        ctx.resp.message = f"Generated {total} MySQL writes for CDC (insert/update/delete)"
        return ctx
