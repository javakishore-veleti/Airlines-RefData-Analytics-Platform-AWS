"""Health facade interface."""

from __future__ import annotations

from typing import Protocol

from app.common.dtos.usecase import HealthCtx


class HealthFacade(Protocol):
    def check(self, ctx: HealthCtx) -> HealthCtx: ...
