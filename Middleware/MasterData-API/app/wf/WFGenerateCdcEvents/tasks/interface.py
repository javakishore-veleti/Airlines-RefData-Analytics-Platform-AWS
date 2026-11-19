from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import GenerateCdcEventsCtx

class GenerateCdcTask(Protocol):
    def run(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx: ...
