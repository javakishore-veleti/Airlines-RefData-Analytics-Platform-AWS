"""TDD: Health use case must traverse api facade → WF → task → dao with Ctx/Req/Resp."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from app.common.dtos.usecase import HealthCtx, HealthReq, HealthResp
from app.dao.health_dao import HealthDao
from app.facade.health.impl import HealthFacadeImpl
from app.wf.WFHealth.impl import WFHealthImpl
from app.wf.WFHealth.tasks.check_mysql_task import CheckMysqlTask


class TestHealthLayering(unittest.TestCase):
    def test_health_ok_when_dao_ping_succeeds(self) -> None:
        dao = MagicMock(spec=HealthDao)
        dao.ping.return_value = True
        task = CheckMysqlTask(dao=dao)
        wf = WFHealthImpl(check_mysql_task=task)
        facade = HealthFacadeImpl(wf=wf)

        ctx = HealthCtx(req=HealthReq(), resp=HealthResp())
        out = facade.check(ctx)

        self.assertEqual(out.resp.status, "ok")
        self.assertTrue(out.resp.mysql)
        dao.ping.assert_called_once()

    def test_health_degraded_when_dao_ping_fails(self) -> None:
        dao = MagicMock(spec=HealthDao)
        dao.ping.side_effect = RuntimeError("connection refused")
        task = CheckMysqlTask(dao=dao)
        wf = WFHealthImpl(check_mysql_task=task)
        facade = HealthFacadeImpl(wf=wf)

        ctx = HealthCtx(req=HealthReq(), resp=HealthResp())
        out = facade.check(ctx)

        self.assertEqual(out.resp.status, "degraded")
        self.assertFalse(out.resp.mysql)
        self.assertIn("connection refused", out.resp.detail or "")


if __name__ == "__main__":
    unittest.main()
