from __future__ import annotations
from app.common.dtos.usecase import AuthCtx
from app.wf.WFAuth.interface import WFAuth

class AuthFacadeImpl:
    def __init__(self, wf: WFAuth) -> None:
        self._wf = wf
    def signup(self, ctx: AuthCtx) -> AuthCtx: return self._wf.signup(ctx)
    def signin(self, ctx: AuthCtx) -> AuthCtx: return self._wf.signin(ctx)
    def signout(self, ctx: AuthCtx) -> AuthCtx: return self._wf.signout(ctx)
