from __future__ import annotations
import unittest
from unittest.mock import MagicMock

from app.common.dtos.usecase import GenerateCdcEventsCtx, GenerateCdcEventsReq, GenerateCdcEventsResp
from app.dao.market_rule_dao import MarketRuleDao
from app.facade.generate_cdc.impl import GenerateCdcFacadeImpl
from app.wf.WFGenerateCdcEvents.impl import WFGenerateCdcEventsImpl
from app.wf.WFGenerateCdcEvents.tasks.generate_mix_task import GenerateMixTask


class TestGenerateCdcLayering(unittest.TestCase):
    def test_generate_fills_resp(self) -> None:
        dao = MagicMock(spec=MarketRuleDao)
        dao.generate_cdc_mix.return_value = (2, 1, 0)
        facade = GenerateCdcFacadeImpl(
            wf=WFGenerateCdcEventsImpl(generate_mix_task=GenerateMixTask(dao=dao))
        )
        ctx = GenerateCdcEventsCtx(req=GenerateCdcEventsReq(count=3), resp=GenerateCdcEventsResp())
        out = facade.generate(ctx)
        self.assertEqual(out.resp.inserted, 2)
        self.assertEqual(out.resp.updated, 1)
        self.assertEqual(out.resp.deleted, 0)
        dao.generate_cdc_mix.assert_called_once_with(3)


if __name__ == "__main__":
    unittest.main()
