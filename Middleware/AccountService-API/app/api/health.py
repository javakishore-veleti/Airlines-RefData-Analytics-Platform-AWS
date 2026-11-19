from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from app.common.dtos.usecase import HealthCtx, HealthReq, HealthResp
from app.facade import object_factory as facade_factory
router = APIRouter(tags=["health"])
@router.get("/health")
def health() -> dict[str, Any]:
    out = facade_factory.get_bean("health_facade").check(HealthCtx(req=HealthReq(), resp=HealthResp()))
    body: dict[str, Any] = {"status": out.resp.status, "mysql": out.resp.mysql}
    if out.resp.detail: body["detail"] = out.resp.detail
    return body
