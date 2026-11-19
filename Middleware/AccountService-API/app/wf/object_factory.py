from __future__ import annotations
from typing import Any
from app.dao import object_factory as dao_factory
from app.wf.WFHealth.impl import WFHealthImpl
from app.wf.WFHealth.tasks.check_mysql_task import CheckMysqlTask
_BEANS: dict[str, Any] = {}
def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        if bean_id == "wf_health":
            _BEANS[bean_id] = WFHealthImpl(check_mysql_task=CheckMysqlTask(dao=dao_factory.get_bean("health_dao")))
        else: raise KeyError(bean_id)
    return _BEANS[bean_id]
