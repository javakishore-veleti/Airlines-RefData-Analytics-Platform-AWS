"""Common task interface for WFHealth tasks."""

from __future__ import annotations

from typing import Protocol

from app.common.dtos.usecase import HealthCtx


class HealthTask(Protocol):
    def run(self, ctx: HealthCtx) -> HealthCtx: ...
