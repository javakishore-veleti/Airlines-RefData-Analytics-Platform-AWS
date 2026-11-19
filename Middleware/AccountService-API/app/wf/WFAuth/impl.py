from __future__ import annotations
from app.common.dtos.usecase import AuthCtx
from app.dao.session_dao import SessionDao
from app.dao.user_dao import UserDao, verify_password

class WFAuthImpl:
    def __init__(self, user_dao: UserDao, session_dao: SessionDao) -> None:
        self._users = user_dao
        self._sessions = session_dao

    def signup(self, ctx: AuthCtx) -> AuthCtx:
        r = ctx.req
        self._users.create(r.username, r.password, r.display_name or r.username, "operator")
        token = self._sessions.create(r.username, "operator")
        ctx.resp.ok = True
        ctx.resp.token = token
        ctx.resp.username = r.username
        ctx.resp.role = "operator"
        ctx.resp.message = "signed up"
        return ctx

    def signin(self, ctx: AuthCtx) -> AuthCtx:
        row = self._users.get_by_username(ctx.req.username)
        if not row or not verify_password(ctx.req.password, row["password_salt"], row["password_hash"]):
            ctx.resp.ok = False
            ctx.resp.message = "invalid credentials"
            return ctx
        token = self._sessions.create(row["username"], row["role"])
        ctx.resp.ok = True
        ctx.resp.token = token
        ctx.resp.username = row["username"]
        ctx.resp.role = row["role"]
        ctx.resp.message = "signed in"
        return ctx

    def signout(self, ctx: AuthCtx) -> AuthCtx:
        ok = self._sessions.revoke(ctx.req.token)
        ctx.resp.ok = ok
        ctx.resp.message = "signed out" if ok else "unknown token"
        return ctx
