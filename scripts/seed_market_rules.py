#!/usr/bin/env python3
"""Seed market_db.market_rule with synthetic reference-data rows (D2).

Default target: 1_000_000 rows. Uses batched multi-row INSERT for throughput.

Usage:
  python scripts/seed_market_rules.py
  python scripts/seed_market_rules.py --count 1000
  ARFD_MYSQL_HOST=127.0.0.1 python scripts/seed_market_rules.py --count 1000000
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from datetime import UTC, datetime, timedelta

try:
    import pymysql
except ImportError:  # pragma: no cover
    print("Install pymysql: pip install pymysql", file=sys.stderr)
    raise

AIRPORTS = [
    "ORD", "SFO", "LAX", "JFK", "ATL", "DFW", "DEN", "SEA", "MIA", "BOS",
    "EWR", "CLT", "PHX", "IAH", "MSP", "DTW", "PHL", "LGA", "BWI", "SLC",
    "SAN", "TPA", "MDW", "DAL", "HOU", "AUS", "RDU", "PDX", "STL", "HNL",
]
STATUSES = ["ACTIVE", "DRAFT", "INACTIVE"]


def connect():
    return pymysql.connect(
        host=os.environ.get("ARFD_MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("ARFD_MYSQL_PORT", "3306")),
        user=os.environ.get("ARFD_MYSQL_USER", "arfd"),
        password=os.environ.get("ARFD_MYSQL_PASSWORD", "arfd"),
        database=os.environ.get("ARFD_MYSQL_DATABASE", "market_db"),
        charset="utf8mb4",
        autocommit=False,
    )


def ensure_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS market_rule (
                rule_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                weight INT NOT NULL DEFAULT 0,
                status VARCHAR(10) NOT NULL DEFAULT 'DRAFT',
                effective_from DATETIME(6) NOT NULL,
                market_from VARCHAR(30) NOT NULL,
                market_to VARCHAR(30) NOT NULL,
                created_at DATETIME(6),
                updated_at DATETIME(6)
            )
            """
        )
    conn.commit()


def seed(count: int, batch_size: int, truncate: bool) -> None:
    conn = connect()
    try:
        ensure_table(conn)
        with conn.cursor() as cur:
            if truncate:
                cur.execute("TRUNCATE TABLE market_rule")
                conn.commit()
                print(f"Truncated market_rule; inserting {count:,} rows...")
            else:
                print(f"Appending {count:,} rows to market_rule...")

            sql = (
                "INSERT INTO market_rule "
                "(name, weight, status, effective_from, market_from, market_to, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            now = datetime.now(UTC).replace(tzinfo=None)
            t0 = time.time()
            inserted = 0
            while inserted < count:
                n = min(batch_size, count - inserted)
                rows = []
                for i in range(n):
                    idx = inserted + i + 1
                    a = AIRPORTS[idx % len(AIRPORTS)]
                    b = AIRPORTS[(idx * 7) % len(AIRPORTS)]
                    if a == b:
                        b = AIRPORTS[(idx + 1) % len(AIRPORTS)]
                    effective = now - timedelta(days=random.randint(0, 365))
                    rows.append(
                        (
                            f"{a}-{b} Rule {idx}",
                            random.randint(1, 200),
                            STATUSES[idx % len(STATUSES)],
                            effective,
                            a,
                            b,
                            now,
                            now,
                        )
                    )
                cur.executemany(sql, rows)
                conn.commit()
                inserted += n
                if inserted % (batch_size * 10) == 0 or inserted == count:
                    elapsed = time.time() - t0
                    rate = inserted / elapsed if elapsed else 0
                    print(f"  {inserted:,}/{count:,} ({rate:,.0f} rows/s)")
        print(f"Done: {count:,} rows in {time.time() - t0:.1f}s")
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Seed market_rule with synthetic rows (D2).")
    p.add_argument("--count", type=int, default=1_000_000, help="Number of rows (default 1000000)")
    p.add_argument("--batch-size", type=int, default=5000, help="Rows per INSERT batch")
    p.add_argument(
        "--truncate",
        action="store_true",
        help="TRUNCATE market_rule before insert (destructive)",
    )
    args = p.parse_args(argv)
    if args.count < 1:
        print("--count must be >= 1", file=sys.stderr)
        return 2
    seed(args.count, args.batch_size, args.truncate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
