from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.common.dtos.usecase import UserCtx, UserReq, UserResp
from app.facade import object_factory as facade_factory

router = APIRouter(prefix="/users", tags=["users"])

class UserBody(BaseModel):
    username: str | None = None
    password: str | None = None
    display_name: str = ""
    role: str = "operator"

@router.get("")
def list_users() -> dict:
    out = facade_factory.get_bean("user_facade").list(UserCtx(req=UserReq(), resp=UserResp()))
    return {"users": out.resp.users}

@router.post("")
def create_user(body: UserBody) -> dict:
    if not body.username or not body.password:
        raise HTTPException(400, "username and password required")
    ctx = UserCtx(req=UserReq(username=body.username, password=body.password,
                              display_name=body.display_name or body.username, role=body.role),
                  resp=UserResp())
    try:
        out = facade_factory.get_bean("user_facade").create(ctx)
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"ok": out.resp.ok, "user_id": out.resp.user_id, "username": out.resp.username}

@router.put("/{user_id}")
def update_user(user_id: int, body: UserBody) -> dict:
    ctx = UserCtx(req=UserReq(user_id=user_id, display_name=body.display_name, role=body.role,
                              password=body.password or ""), resp=UserResp())
    out = facade_factory.get_bean("user_facade").update(ctx)
    if not out.resp.ok:
        raise HTTPException(404, "not found")
    return {"ok": True, "user_id": user_id}

@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict:
    out = facade_factory.get_bean("user_facade").delete(UserCtx(req=UserReq(user_id=user_id), resp=UserResp()))
    if not out.resp.ok:
        raise HTTPException(404, "not found")
    return {"ok": True}
