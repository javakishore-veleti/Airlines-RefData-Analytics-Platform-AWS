from __future__ import annotations
import unittest
from unittest.mock import MagicMock
from app.common.dtos.usecase import HealthCtx, HealthReq, HealthResp
from app.dao.health_dao import HealthDao
from app.facade.health.impl import HealthFacadeImpl
from app.wf.WFHealth.impl import WFHealthImpl
from app.wf.WFHealth.tasks.check_mysql_task import CheckMysqlTask

class TestHealth(unittest.TestCase):
    def test_ok(self):
        dao = MagicMock(spec=HealthDao); dao.ping.return_value = True
        out = HealthFacadeImpl(wf=WFHealthImpl(check_mysql_task=CheckMysqlTask(dao=dao))).check(
            HealthCtx(req=HealthReq(), resp=HealthResp())
        )
        self.assertEqual(out.resp.status, "ok")

if __name__ == "__main__":
    unittest.main()
