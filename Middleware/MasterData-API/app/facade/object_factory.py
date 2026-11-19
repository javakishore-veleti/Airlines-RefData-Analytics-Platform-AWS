"""Facade-layer bean lookup (D3)."""

from __future__ import annotations

from typing import Any

from app.facade.health.impl import HealthFacadeImpl
from app.facade.generate_cdc.impl import GenerateCdcFacadeImpl
from app.facade.market_rule.impl import MarketRuleFacadeImpl
from app.facade.lake_query.impl import LakeQueryFacadeImpl
from app.facade.messaging.impl import MessagingFacadeImpl
from app.wf import object_factory as wf_factory

_BEANS: dict[str, Any] = {}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        if bean_id == "health_facade":
            _BEANS[bean_id] = HealthFacadeImpl(wf=wf_factory.get_bean("wf_health"))
        elif bean_id == "generate_cdc_facade":
            _BEANS[bean_id] = GenerateCdcFacadeImpl(wf=wf_factory.get_bean("wf_generate_cdc"))
        elif bean_id == "messaging_facade":
            _BEANS[bean_id] = MessagingFacadeImpl(wf=wf_factory.get_bean("wf_messaging"))
        elif bean_id == "lake_query_facade":
            _BEANS[bean_id] = LakeQueryFacadeImpl(wf=wf_factory.get_bean("wf_lake_query"))
        elif bean_id == "market_rule_facade":
            _BEANS[bean_id] = MarketRuleFacadeImpl(wf=wf_factory.get_bean("wf_market_rule_write"))
        else:
            raise KeyError(f"unknown facade bean: {bean_id}")
    return _BEANS[bean_id]
