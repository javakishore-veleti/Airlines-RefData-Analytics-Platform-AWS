"""Lake read/query APIs for Intelligence."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.common.dtos.usecase import LakeQueryCtx, LakeQueryReq, LakeQueryResp
from app.facade import object_factory as facade_factory

router = APIRouter(prefix="/lake", tags=["lake"])


@router.get("/market-rules")
def list_market_rules(limit: int = Query(50, ge=1, le=1000)) -> dict:
    facade = facade_factory.get_bean("lake_query_facade")
    ctx = LakeQueryCtx(req=LakeQueryReq(limit=limit), resp=LakeQueryResp())
    out = facade.query(ctx)
    return {"count": out.resp.count, "items": out.resp.items}


@router.get("/market-rules/{rule_id}")
def get_market_rule(rule_id: int) -> dict:
    facade = facade_factory.get_bean("lake_query_facade")
    ctx = LakeQueryCtx(req=LakeQueryReq(rule_id=rule_id), resp=LakeQueryResp())
    out = facade.query(ctx)
    if not out.resp.items:
        raise HTTPException(status_code=404, detail="not found")
    return out.resp.items[0]
