from __future__ import annotations
from app.common.dtos.usecase import LakeQueryCtx
from app.wf.WFLakeQuery.interface import WFLakeQuery

class LakeQueryFacadeImpl:
    def __init__(self, wf: WFLakeQuery) -> None:
        self._wf = wf
    def query(self, ctx: LakeQueryCtx) -> LakeQueryCtx:
        return self._wf.execute(ctx)
