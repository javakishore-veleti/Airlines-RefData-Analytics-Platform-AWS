#!/usr/bin/env python3
"""Seed market_db.market_rule with synthetic historical rows (default 1_000_000)."""
from __future__ import annotations

import argparse
import os
import random
import string
from datetime import datetime, timedelta

try:
    import mysql.connector
except ImportError:
    raise SystemExit("Install mysql-connector-python: pip install mysql-connector-python")


AIRPORTS = [
    "ORD", "SFO", "LAX", "JFK", "LHR", "CDG", "NRT", "SYD", "DXB", "SIN",
    "FRA", "AMS", "HKG", "ICN", "MAD", "BCN", "MIA", "SEA", "DEN", "ATL",
]
STATUSES = ["ACTIVE", "DRAFT", "RETIRED"]


def connect():
    return mysql.connector.connect(
        host=os.getenv("ARFD_MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("ARFD_MYSQL_PORT", "3306")),
        user=os.getenv("ARFD_MYSQL_USER", "arfd"),
        password=os.getenv("ARFD_MYSQL_PASSWORD", "arfd"),
        database=os.getenv("ARFD_MYSQL_DATABASE", "market_db"),
    )


def ensure_table(cur) -> None:
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


def row(i: int):
    a, b = random.sample(AIRPORTS, 2)
    now = datetime.utcnow()
    eff = now - timedelta(days=random.randint(0, 3650))
    name = f"{a}-{b} Rule {i} {''.join(random.choices(string.ascii_uppercase, k=4))}"
    return (
        name[:120],
        random.randint(1, 100),
        random.choice(STATUSES),
        eff,
        a,
        b,
        now,
        now,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1_000_000)
    ap.add_argument("--batch-size", type=int, default=5000)
    ap.add_argument("--truncate", action="store_true")
    args = ap.parse_args()

    conn = connect()
    cur = conn.cursor()
    ensure_table(cur)
    if args.truncate:
        cur.execute("TRUNCATE TABLE market_rule")
        conn.commit()
        print("truncated market_rule")

    sql = (
        "INSERT INTO market_rule "
        "(name, weight, status, effective_from, market_from, market_to, created_at, updated_at) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    batch = []
    inserted = 0
    for i in range(1, args.count + 1):
        batch.append(row(i))
        if len(batch) >= args.batch_size:
            cur.executemany(sql, batch)
            conn.commit()
            inserted += len(batch)
            print(f"inserted {inserted}/{args.count}")
            batch.clear()
    if batch:
        cur.executemany(sql, batch)
        conn.commit()
        inserted += len(batch)
        print(f"inserted {inserted}/{args.count}")
    cur.execute("SELECT COUNT(*) FROM market_rule")
    print("total rows:", cur.fetchone()[0])
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
