from __future__ import annotations
import unittest
from app.common.dtos.usecase import MessagingCtx, MessagingReq, MessagingResp
from app.dao.messaging_dao import InMemoryMessagingDao
from app.facade.messaging.impl import MessagingFacadeImpl
from app.wf.WFMessaging.impl import WFMessagingImpl

class TestMessaging(unittest.TestCase):
    def test_publish_consume(self) -> None:
        dao = InMemoryMessagingDao()
        facade = MessagingFacadeImpl(wf=WFMessagingImpl(dao=dao))
        facade.publish(MessagingCtx(req=MessagingReq(payload="hello"), resp=MessagingResp()))
        out = facade.consume(MessagingCtx(req=MessagingReq(max_messages=5), resp=MessagingResp()))
        self.assertEqual(out.resp.messages, ["hello"])

if __name__ == "__main__":
    unittest.main()
