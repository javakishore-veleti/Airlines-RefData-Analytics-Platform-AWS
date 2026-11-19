"""Signup / signin / signout for Admin + Intelligence portals."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.common.dtos.usecase import AuthCtx, AuthReq, AuthResp
from app.facade import object_factory as facade_factory

router = APIRouter(prefix="/auth", tags=["auth"])


class Creds(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    display_name: str = ""


class TokenBody(BaseModel):
    token: str


@router.post("/signup")
def signup(body: Creds) -> dict:
    ctx = AuthCtx(
        req=AuthReq(username=body.username, password=body.password, display_name=body.display_name),
        resp=AuthResp(),
    )
    try:
        out = facade_factory.get_bean("auth_facade").signup(ctx)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": out.resp.ok, "token": out.resp.token, "username": out.resp.username, "role": out.resp.role}


@router.post("/signin")
def signin(body: Creds) -> dict:
    out = facade_factory.get_bean("auth_facade").signin(
        AuthCtx(req=AuthReq(username=body.username, password=body.password), resp=AuthResp())
    )
    if not out.resp.ok:
        raise HTTPException(status_code=401, detail=out.resp.message)
    return {"ok": True, "token": out.resp.token, "username": out.resp.username, "role": out.resp.role}


@router.post("/signout")
def signout(body: TokenBody) -> dict:
    out = facade_factory.get_bean("auth_facade").signout(
        AuthCtx(req=AuthReq(token=body.token), resp=AuthResp())
    )
    return {"ok": out.resp.ok, "message": out.resp.message}
