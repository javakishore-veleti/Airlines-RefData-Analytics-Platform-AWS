"""HTTP Health endpoint — api → facade → WF → task → dao."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.common.dtos.usecase import HealthCtx, HealthReq, HealthResp
from app.facade import object_factory as facade_factory

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, Any]:
    facade = facade_factory.get_bean("health_facade")
    ctx = HealthCtx(req=HealthReq(), resp=HealthResp())
    out = facade.check(ctx)
    body: dict[str, Any] = {"status": out.resp.status, "mysql": out.resp.mysql}
    if out.resp.detail:
        body["detail"] = out.resp.detail
    return body
