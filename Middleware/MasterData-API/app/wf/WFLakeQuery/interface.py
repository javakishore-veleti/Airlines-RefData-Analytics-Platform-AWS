from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import LakeQueryCtx
class WFLakeQuery(Protocol):
    def execute(self, ctx: LakeQueryCtx) -> LakeQueryCtx: ...
