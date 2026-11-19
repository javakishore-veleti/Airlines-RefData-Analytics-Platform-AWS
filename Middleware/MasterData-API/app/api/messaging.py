"""Async messaging publish/consume HTTP surface."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.common.dtos.usecase import MessagingCtx, MessagingReq, MessagingResp
from app.facade import object_factory as facade_factory

router = APIRouter(prefix="/messaging", tags=["messaging"])


class PublishBody(BaseModel):
    payload: str = Field(..., min_length=1)


@router.post("/publish")
def publish(body: PublishBody) -> dict:
    facade = facade_factory.get_bean("messaging_facade")
    ctx = MessagingCtx(req=MessagingReq(payload=body.payload), resp=MessagingResp())
    try:
        out = facade.publish(ctx)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"ok": out.resp.ok, "detail": out.resp.detail}


@router.get("/consume")
def consume(max_messages: int = 10) -> dict:
    facade = facade_factory.get_bean("messaging_facade")
    ctx = MessagingCtx(req=MessagingReq(max_messages=max_messages), resp=MessagingResp())
    try:
        out = facade.consume(ctx)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"ok": out.resp.ok, "messages": out.resp.messages, "detail": out.resp.detail}
