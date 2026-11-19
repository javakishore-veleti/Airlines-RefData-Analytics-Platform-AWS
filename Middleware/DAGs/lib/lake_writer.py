"""Local lake writer for market_rule CDC apply (stories #26/#28).

Writes JSON rows under a filesystem lake root that mirrors the MinIO prefix
`market_db/market_rule/`. Suitable for local validation; Iceberg/Spark can
ingest the same layout later.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .cdc_parse import LakeOp


class MarketRuleLakeWriter:
    def __init__(self, lake_root: Path):
        self.root = Path(lake_root) / "market_db" / "market_rule"
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, rule_id: int) -> Path:
        return self.root / f"rule_id={rule_id}.json"

    def apply(self, op: LakeOp) -> str:
        path = self.path_for(op.rule_id)
        if op.op == "delete":
            if path.exists():
                path.unlink()
            return "deleted"
        assert op.row is not None
        path.write_text(json.dumps(op.row, default=str, indent=2) + "\n")
        return "upserted"

    def list_rule_ids(self) -> list[int]:
        ids: list[int] = []
        for p in self.root.glob("rule_id=*.json"):
            try:
                ids.append(int(p.stem.split("=", 1)[1]))
            except ValueError:
                continue
        return sorted(ids)

    def read(self, rule_id: int) -> dict[str, Any] | None:
        path = self.path_for(rule_id)
        if not path.exists():
            return None
        return json.loads(path.read_text())
