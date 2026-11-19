from __future__ import annotations
from app.common.dtos.usecase import UserCtx
from app.dao.user_dao import UserDao

class WFUserAdminImpl:
    def __init__(self, dao: UserDao) -> None:
        self._dao = dao

    def list(self, ctx: UserCtx) -> UserCtx:
        ctx.resp.users = self._dao.list_users()
        ctx.resp.ok = True
        return ctx

    def create(self, ctx: UserCtx) -> UserCtx:
        r = ctx.req
        uid = self._dao.create(r.username, r.password, r.display_name or r.username, r.role)
        ctx.resp.ok = True
        ctx.resp.user_id = uid
        ctx.resp.username = r.username
        ctx.resp.message = "created"
        return ctx

    def update(self, ctx: UserCtx) -> UserCtx:
        r = ctx.req
        assert r.user_id is not None
        ok = self._dao.update(r.user_id, r.display_name, r.role, r.password or None)
        ctx.resp.ok = ok
        ctx.resp.user_id = r.user_id
        ctx.resp.message = "updated" if ok else "not found"
        return ctx

    def delete(self, ctx: UserCtx) -> UserCtx:
        r = ctx.req
        assert r.user_id is not None
        ok = self._dao.delete(r.user_id)
        ctx.resp.ok = ok
        ctx.resp.message = "deleted" if ok else "not found"
        return ctx
