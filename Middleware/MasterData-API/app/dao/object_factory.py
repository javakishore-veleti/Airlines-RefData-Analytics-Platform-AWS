"""DAO-layer bean lookup (D3)."""

from __future__ import annotations

from typing import Any

from app.dao.health_dao import MysqlHealthDao
from app.dao.market_rule_dao import MysqlMarketRuleDao
from app.dao.lake_dao import JsonLakeDao
from app.dao.messaging_dao import RabbitMessagingDao

_BEANS: dict[str, Any] = {
    "health_dao": MysqlHealthDao(),
    "market_rule_dao": MysqlMarketRuleDao(),
    "lake_dao": JsonLakeDao(),
    "messaging_dao": RabbitMessagingDao(),
}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        raise KeyError(f"unknown dao bean: {bean_id}")
    return _BEANS[bean_id]
