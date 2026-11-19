"""DAO: read local lake JSON objects for market_rule."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from app.config import get_settings


class LakeDao(Protocol):
    def list_rules(self, limit: int = 50) -> list[dict[str, Any]]: ...
    def get_rule(self, rule_id: int) -> dict[str, Any] | None: ...


class JsonLakeDao:
    def __init__(self, lake_root: Path | None = None) -> None:
        if lake_root is not None:
            self._root = lake_root
        else:
            # Middleware/MasterData-API -> repo root
            repo = Path(__file__).resolve().parents[4]
            self._root = repo / "runtime_data" / "lake" / "market_db" / "market_rule"

    def list_rules(self, limit: int = 50) -> list[dict[str, Any]]:
        if not self._root.is_dir():
            return []
        items: list[dict[str, Any]] = []
        for path in sorted(self._root.glob("rule_id=*.json")):
            try:
                items.append(json.loads(path.read_text()))
            except Exception:  # noqa: BLE001
                continue
            if len(items) >= limit:
                break
        return items

    def get_rule(self, rule_id: int) -> dict[str, Any] | None:
        path = self._root / f"rule_id={rule_id}.json"
        if not path.is_file():
            return None
        return json.loads(path.read_text())
