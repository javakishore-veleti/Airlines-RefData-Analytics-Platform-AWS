from __future__ import annotations
from app.common.dtos.usecase import HealthCtx
from app.dao.health_dao import HealthDao
class CheckMysqlTask:
    def __init__(self, dao: HealthDao) -> None:
        self._dao = dao
    def run(self, ctx: HealthCtx) -> HealthCtx:
        try:
            ok = self._dao.ping()
            ctx.resp.status = "ok" if ok else "degraded"
            ctx.resp.mysql = bool(ok)
        except Exception as exc:
            ctx.resp.status = "degraded"; ctx.resp.mysql = False; ctx.resp.detail = str(exc)
        return ctx
