from __future__ import annotations
from app.common.dtos.usecase import GenerateCdcEventsCtx
from app.wf.WFGenerateCdcEvents.interface import WFGenerateCdcEvents

class GenerateCdcFacadeImpl:
    def __init__(self, wf: WFGenerateCdcEvents) -> None:
        self._wf = wf

    def generate(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx:
        return self._wf.execute(ctx)
