#!/usr/bin/env python3
"""Validate local lake files for market_rule (story #28)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Middleware" / "DAGs"))

from lib.lake_writer import MarketRuleLakeWriter  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lake-root", default=os.environ.get("ARFD_LAKE_ROOT", str(ROOT / "runtime_data" / "lake")))
    p.add_argument("--min-rows", type=int, default=1)
    args = p.parse_args(argv)

    writer = MarketRuleLakeWriter(Path(args.lake_root))
    ids = writer.list_rule_ids()
    if len(ids) < args.min_rows:
        print(f"FAIL: expected >= {args.min_rows} lake rows, found {len(ids)}", file=sys.stderr)
        return 1
    for rid in ids:
        row = writer.read(rid)
        if not row or int(row.get("rule_id", -1)) != rid:
            print(f"FAIL: bad row for rule_id={rid}: {row}", file=sys.stderr)
            return 1
    print(json.dumps({"ok": True, "count": len(ids), "rule_ids": ids}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
