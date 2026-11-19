"""WFHealth implementation — orchestrates CheckMysqlTask."""

from __future__ import annotations

from app.common.dtos.usecase import HealthCtx
from app.wf.WFHealth.tasks.check_mysql_task import CheckMysqlTask


class WFHealthImpl:
    def __init__(self, check_mysql_task: CheckMysqlTask) -> None:
        self._check_mysql_task = check_mysql_task

    def execute(self, ctx: HealthCtx) -> HealthCtx:
        return self._check_mysql_task.run(ctx)
