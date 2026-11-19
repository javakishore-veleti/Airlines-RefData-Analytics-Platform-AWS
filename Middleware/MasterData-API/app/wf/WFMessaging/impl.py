from __future__ import annotations
from app.common.dtos.usecase import MessagingCtx
from app.dao.messaging_dao import MessagingDao

class WFMessagingImpl:
    def __init__(self, dao: MessagingDao) -> None:
        self._dao = dao

    def publish(self, ctx: MessagingCtx) -> MessagingCtx:
        self._dao.publish(ctx.req.payload)
        ctx.resp.ok = True
        ctx.resp.detail = "published"
        return ctx

    def consume(self, ctx: MessagingCtx) -> MessagingCtx:
        msgs = self._dao.consume(ctx.req.max_messages)
        ctx.resp.ok = True
        ctx.resp.messages = msgs
        ctx.resp.detail = f"consumed {len(msgs)}"
        return ctx
