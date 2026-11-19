from __future__ import annotations
from app.common.dtos.usecase import GenerateCdcEventsCtx
from app.wf.WFGenerateCdcEvents.tasks.generate_mix_task import GenerateMixTask

class WFGenerateCdcEventsImpl:
    def __init__(self, generate_mix_task: GenerateMixTask) -> None:
        self._task = generate_mix_task

    def execute(self, ctx: GenerateCdcEventsCtx) -> GenerateCdcEventsCtx:
        return self._task.run(ctx)
