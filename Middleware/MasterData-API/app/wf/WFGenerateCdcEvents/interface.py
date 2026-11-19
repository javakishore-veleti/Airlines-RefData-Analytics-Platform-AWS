from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import GenerateCdcEventsCtx

class WFGenerateCdcEvents(Protocol):
    def execute(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx: ...
