#!/usr/bin/env python3
"""Consume Debezium CDC from Kafka and apply to the local lake (M03 #26–#28).

Usage:
  ARFD_KAFKA_BOOTSTRAP=127.0.0.1:9092 \\
  ARFD_LAKE_ROOT=runtime_data/lake \\
  python scripts/cdc_apply_market_rule.py --max-messages 100 --timeout-sec 20
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Middleware" / "DAGs"))

from lib.cdc_parse import map_debezium_op  # noqa: E402
from lib.lake_writer import MarketRuleLakeWriter  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--bootstrap", default=os.environ.get("ARFD_KAFKA_BOOTSTRAP", "127.0.0.1:9092"))
    p.add_argument("--topic", default="arfd.market_db.market_rule")
    p.add_argument("--group", default="arfd-cdc-lake-apply")
    p.add_argument("--lake-root", default=os.environ.get("ARFD_LAKE_ROOT", str(ROOT / "runtime_data" / "lake")))
    p.add_argument("--max-messages", type=int, default=100)
    p.add_argument("--timeout-sec", type=float, default=20.0)
    args = p.parse_args(argv)

    try:
        from kafka import KafkaConsumer
    except ImportError:
        print("Install kafka-python: pip install kafka-python", file=sys.stderr)
        return 2

    writer = MarketRuleLakeWriter(Path(args.lake_root))
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap.split(","),
        group_id=args.group,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=int(args.timeout_sec * 1000),
        value_deserializer=lambda b: json.loads(b.decode("utf-8")) if b else None,
    )

    applied = 0
    t0 = time.time()
    try:
        for msg in consumer:
            if msg.value is None:
                continue
            op = map_debezium_op(msg.value)
            if op is None:
                continue
            action = writer.apply(op)
            applied += 1
            print(f"{action} rule_id={op.rule_id} op={op.op}")
            if applied >= args.max_messages:
                break
    finally:
        consumer.close()

    print(f"Done: applied={applied} lake_root={args.lake_root} elapsed={time.time()-t0:.1f}s")
    print(f"Lake rule_ids={writer.list_rule_ids()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
