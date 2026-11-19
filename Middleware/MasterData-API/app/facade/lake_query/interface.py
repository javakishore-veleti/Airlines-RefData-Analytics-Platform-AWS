from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import LakeQueryCtx
class LakeQueryFacade(Protocol):
    def query(self, ctx: LakeQueryCtx) -> LakeQueryCtx: ...
