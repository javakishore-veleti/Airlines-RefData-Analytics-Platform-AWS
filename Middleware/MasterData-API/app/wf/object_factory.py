"""WF-layer bean lookup (D3)."""

from __future__ import annotations

from typing import Any

from app.dao import object_factory as dao_factory
from app.wf.WFHealth.impl import WFHealthImpl
from app.wf.WFHealth.tasks.check_mysql_task import CheckMysqlTask
from app.wf.WFGenerateCdcEvents.impl import WFGenerateCdcEventsImpl
from app.wf.WFGenerateCdcEvents.tasks.generate_mix_task import GenerateMixTask
from app.wf.WFMarketRuleWrite.impl import WFMarketRuleWriteImpl

_BEANS: dict[str, Any] = {}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        if bean_id == "wf_health":
            dao = dao_factory.get_bean("health_dao")
            _BEANS[bean_id] = WFHealthImpl(check_mysql_task=CheckMysqlTask(dao=dao))
        elif bean_id == "wf_generate_cdc":
            dao = dao_factory.get_bean("market_rule_dao")
            _BEANS[bean_id] = WFGenerateCdcEventsImpl(generate_mix_task=GenerateMixTask(dao=dao))
        elif bean_id == "wf_market_rule_write":
            dao = dao_factory.get_bean("market_rule_dao")
            _BEANS[bean_id] = WFMarketRuleWriteImpl(dao=dao)
        else:
            raise KeyError(f"unknown wf bean: {bean_id}")
    return _BEANS[bean_id]
