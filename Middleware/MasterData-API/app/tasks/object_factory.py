"""Task-layer bean lookup stub (D3) — WFHealth wires tasks directly today."""

from __future__ import annotations

from typing import Any

_BEANS: dict[str, Any] = {}


def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS:
        raise KeyError(f"unknown task bean: {bean_id}")
    return _BEANS[bean_id]


def register(bean_id: str, bean: Any) -> None:
    _BEANS[bean_id] = bean
