from __future__ import annotations
from typing import Any
from app.dao.health_dao import MysqlHealthDao
from app.dao.user_dao import MysqlUserDao
from app.dao.session_dao import MemorySessionDao
_BEANS: dict[str, Any] = {"health_dao": MysqlHealthDao(), "user_dao": MysqlUserDao(), "session_dao": MemorySessionDao()}
def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS: raise KeyError(bean_id)
    return _BEANS[bean_id]
