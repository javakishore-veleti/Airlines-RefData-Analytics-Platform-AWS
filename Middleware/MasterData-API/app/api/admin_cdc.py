"""GenerateCdcEvents HTTP — api → facade → WF → task → dao."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.common.dtos.usecase import GenerateCdcEventsCtx, GenerateCdcEventsReq, GenerateCdcEventsResp
from app.facade import object_factory as facade_factory

router = APIRouter(tags=["admin-cdc"])


class GenerateCdcRequest(BaseModel):
    count: int = Field(..., ge=1, le=100_000)


class GenerateCdcResponse(BaseModel):
    requested: int
    inserted: int
    updated: int
    deleted: int
    message: str


@router.post("/admin/cdc/generate", response_model=GenerateCdcResponse)
def generate_cdc(body: GenerateCdcRequest) -> GenerateCdcResponse:
    facade = facade_factory.get_bean("generate_cdc_facade")
    ctx = GenerateCdcEventsCtx(
        req=GenerateCdcEventsReq(count=body.count),
        resp=GenerateCdcEventsResp(),
    )
    try:
        out = facade.generate(ctx)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return GenerateCdcResponse(
        requested=out.resp.requested,
        inserted=out.resp.inserted,
        updated=out.resp.updated,
        deleted=out.resp.deleted,
        message=out.resp.message,
    )
