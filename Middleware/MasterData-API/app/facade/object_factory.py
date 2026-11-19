"""Facade-layer bean lookup (D3)."""

from __future__ import annotations

from typing import Any

from app.facade.health.impl import HealthFacadeImpl
from app.wf import object_factory as wf_factory

_BEANS: dict[str, Any] = {}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        if bean_id == "health_facade":
            wf = wf_factory.get_bean("wf_health")
            _BEANS[bean_id] = HealthFacadeImpl(wf=wf)
        else:
            raise KeyError(f"unknown facade bean: {bean_id}")
    return _BEANS[bean_id]
