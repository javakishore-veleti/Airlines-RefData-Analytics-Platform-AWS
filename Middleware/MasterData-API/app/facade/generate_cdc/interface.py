from __future__ import annotations
from typing import Protocol
from app.common.dtos.usecase import GenerateCdcEventsCtx

class GenerateCdcFacade(Protocol):
    def generate(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx: ...
