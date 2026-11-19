from __future__ import annotations
from app.common.dtos.usecase import MessagingCtx
from app.wf.WFMessaging.interface import WFMessaging

class MessagingFacadeImpl:
    def __init__(self, wf: WFMessaging) -> None:
        self._wf = wf
    def publish(self, ctx: MessagingCtx) -> MessagingCtx:
        return self._wf.publish(ctx)
    def consume(self, ctx: MessagingCtx) -> MessagingCtx:
        return self._wf.consume(ctx)
