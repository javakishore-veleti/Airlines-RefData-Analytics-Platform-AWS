from __future__ import annotations
from typing import Any
_BEANS: dict[str, Any] = {}
def get_bean(bean_id: str) -> Any:
    if bean_id not in _BEANS: raise KeyError(bean_id)
    return _BEANS[bean_id]
