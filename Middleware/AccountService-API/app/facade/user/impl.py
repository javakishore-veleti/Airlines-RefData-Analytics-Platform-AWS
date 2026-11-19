from __future__ import annotations
from app.common.dtos.usecase import UserCtx
from app.wf.WFUserAdmin.interface import WFUserAdmin

class UserFacadeImpl:
    def __init__(self, wf: WFUserAdmin) -> None:
        self._wf = wf
    def list(self, ctx: UserCtx) -> UserCtx: return self._wf.list(ctx)
    def create(self, ctx: UserCtx) -> UserCtx: return self._wf.create(ctx)
    def update(self, ctx: UserCtx) -> UserCtx: return self._wf.update(ctx)
    def delete(self, ctx: UserCtx) -> UserCtx: return self._wf.delete(ctx)
