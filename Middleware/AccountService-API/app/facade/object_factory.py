from __future__ import annotations
from typing import Any
from app.facade.health.impl import HealthFacadeImpl
from app.wf import object_factory as wf_factory
_BEANS: dict[str, Any] = {}
def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        if bean_id == "health_facade":
            _BEANS[bean_id] = HealthFacadeImpl(wf=wf_factory.get_bean("wf_health"))
        else: raise KeyError(bean_id)
    return _BEANS[bean_id]
