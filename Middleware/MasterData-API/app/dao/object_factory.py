"""DAO-layer bean lookup (D3)."""

from __future__ import annotations

from typing import Any

from app.dao.health_dao import MysqlHealthDao
from app.dao.market_rule_dao import MysqlMarketRuleDao

_BEANS: dict[str, Any] = {
    "health_dao": MysqlHealthDao(),
    "market_rule_dao": MysqlMarketRuleDao(),
}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        raise KeyError(f"unknown dao bean: {bean_id}")
    return _BEANS[bean_id]
