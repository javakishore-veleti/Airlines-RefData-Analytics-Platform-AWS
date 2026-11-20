"""Admin market_rule write APIs."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.common.dtos.usecase import MarketRuleWriteCtx, MarketRuleWriteReq, MarketRuleWriteResp
from app.facade import object_factory as facade_factory

router = APIRouter(prefix="/admin/market-rules", tags=["market-rules"])


class MarketRuleBody(BaseModel):
    name: str
    weight: int = Field(1, ge=0)
    status: str = "ACTIVE"
    market_from: str = "ORD"
    market_to: str = "SFO"


@router.get("")
def list_rules(limit: int = 100) -> dict:
    facade = facade_factory.get_bean("market_rule_facade")
    items = facade.list(limit=limit)
    # serialize datetimes
    out = []
    for row in items:
        item = dict(row)
        for k, v in list(item.items()):
            if hasattr(v, "isoformat"):
                item[k] = v.isoformat()
        out.append(item)
    return {"count": len(out), "items": out}


@router.post("")
def create_rule(body: MarketRuleBody) -> dict:
    facade = facade_factory.get_bean("market_rule_facade")
    ctx = MarketRuleWriteCtx(
        req=MarketRuleWriteReq(
            name=body.name,
            weight=body.weight,
            status=body.status,
            market_from=body.market_from,
            market_to=body.market_to,
        ),
        resp=MarketRuleWriteResp(),
    )
    try:
        out = facade.create(ctx)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"rule_id": out.resp.rule_id, "ok": out.resp.ok, "message": out.resp.message}


@router.put("/{rule_id}")
def update_rule(rule_id: int, body: MarketRuleBody) -> dict:
    facade = facade_factory.get_bean("market_rule_facade")
    ctx = MarketRuleWriteCtx(
        req=MarketRuleWriteReq(
            rule_id=rule_id,
            name=body.name,
            weight=body.weight,
            status=body.status,
            market_from=body.market_from,
            market_to=body.market_to,
        ),
        resp=MarketRuleWriteResp(),
    )
    out = facade.update(ctx)
    if not out.resp.ok:
        raise HTTPException(status_code=404, detail="not found")
    return {"rule_id": out.resp.rule_id, "ok": out.resp.ok, "message": out.resp.message}


@router.post("/{rule_id}/deactivate")
def deactivate_rule(rule_id: int) -> dict:
    facade = facade_factory.get_bean("market_rule_facade")
    ctx = MarketRuleWriteCtx(req=MarketRuleWriteReq(rule_id=rule_id), resp=MarketRuleWriteResp())
    out = facade.deactivate(ctx)
    if not out.resp.ok:
        raise HTTPException(status_code=404, detail="not found")
    return {"rule_id": out.resp.rule_id, "ok": out.resp.ok, "message": out.resp.message}
