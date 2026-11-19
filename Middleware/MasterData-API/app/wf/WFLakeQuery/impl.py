from __future__ import annotations
from app.common.dtos.usecase import LakeQueryCtx
from app.dao.lake_dao import LakeDao

class WFLakeQueryImpl:
    def __init__(self, dao: LakeDao) -> None:
        self._dao = dao

    def execute(self, ctx: LakeQueryCtx) -> LakeQueryCtx:
        if ctx.req.rule_id is not None:
            row = self._dao.get_rule(ctx.req.rule_id)
            ctx.resp.items = [row] if row else []
        else:
            ctx.resp.items = self._dao.list_rules(limit=ctx.req.limit)
        ctx.resp.count = len(ctx.resp.items)
        return ctx
