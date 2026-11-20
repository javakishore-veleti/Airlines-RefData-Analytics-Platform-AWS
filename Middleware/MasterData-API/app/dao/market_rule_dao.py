"""DAO: market_rule OLTP writes for Admin / CDC generate."""

from __future__ import annotations

import random
from datetime import UTC, datetime
from typing import Protocol

import pymysql

from app.config import Settings, get_settings

AIRPORTS = [
    "ORD", "SFO", "LAX", "JFK", "ATL", "DFW", "DEN", "SEA", "MIA", "BOS",
]


class MarketRuleDao(Protocol):
    def list_rules(self, limit: int = 100) -> list[dict]: ...

    def list_rules(self, limit: int = 100) -> list[dict]:
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT rule_id, name, weight, status, market_from, market_to, updated_at
                    FROM market_rule
                    ORDER BY rule_id DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        finally:
            conn.close()

    def generate_cdc_mix(self, count: int) -> tuple[int, int, int]: ...
    def create(self, name: str, weight: int, status: str, market_from: str, market_to: str) -> int: ...
    def update(self, rule_id: int, name: str, weight: int, status: str, market_from: str, market_to: str) -> bool: ...
    def deactivate(self, rule_id: int) -> bool: ...


class MysqlMarketRuleDao:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def _conn(self):
        s = self._settings
        return pymysql.connect(
            host=s.mysql_host,
            port=s.mysql_port,
            user=s.mysql_user,
            password=s.mysql_password,
            database=s.mysql_database,
            charset="utf8mb4",
            autocommit=False,
        )

    def generate_cdc_mix(self, count: int) -> tuple[int, int, int]:
        conn = self._conn()
        inserted = updated = deleted = 0
        now = datetime.now(UTC).replace(tzinfo=None)
        try:
            with conn.cursor() as cur:
                insert_budget = max(1, (count * 2) // 5)
                update_budget = (count * 2) // 5
                delete_budget = count - insert_budget - update_budget
                if update_budget or delete_budget:
                    need = update_budget + delete_budget
                    cur.execute(
                        "SELECT rule_id FROM market_rule ORDER BY rule_id DESC LIMIT %s",
                        (need,),
                    )
                    ids = [row[0] for row in cur.fetchall()]
                    update_ids = ids[: min(update_budget, len(ids))]
                    delete_ids = ids[len(update_ids) : len(update_ids) + delete_budget]
                    for rule_id in update_ids:
                        cur.execute(
                            "UPDATE market_rule SET weight = %s, updated_at = %s WHERE rule_id = %s",
                            (random.randint(1, 500), now, rule_id),
                        )
                        updated += cur.rowcount
                    for rule_id in delete_ids:
                        cur.execute("DELETE FROM market_rule WHERE rule_id = %s", (rule_id,))
                        deleted += cur.rowcount
                    insert_budget += (update_budget - len(update_ids)) + (delete_budget - len(delete_ids))
                for i in range(insert_budget):
                    a = AIRPORTS[i % len(AIRPORTS)]
                    b = AIRPORTS[(i * 3) % len(AIRPORTS)]
                    if a == b:
                        b = AIRPORTS[(i + 1) % len(AIRPORTS)]
                    cur.execute(
                        """
                        INSERT INTO market_rule
                        (name, weight, status, effective_from, market_from, market_to, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            f"CDC Gen {a}-{b} {now.strftime('%Y%m%d%H%M%S')}-{i}",
                            random.randint(1, 200),
                            "ACTIVE",
                            now,
                            a,
                            b,
                            now,
                            now,
                        ),
                    )
                    inserted += 1
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        return inserted, updated, deleted

    def create(self, name: str, weight: int, status: str, market_from: str, market_to: str) -> int:
        conn = self._conn()
        now = datetime.now(UTC).replace(tzinfo=None)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO market_rule
                    (name, weight, status, effective_from, market_from, market_to, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (name, weight, status, now, market_from, market_to, now, now),
                )
                rule_id = cur.lastrowid
            conn.commit()
            return int(rule_id)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, rule_id: int, name: str, weight: int, status: str, market_from: str, market_to: str) -> bool:
        conn = self._conn()
        now = datetime.now(UTC).replace(tzinfo=None)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE market_rule
                    SET name=%s, weight=%s, status=%s, market_from=%s, market_to=%s, updated_at=%s
                    WHERE rule_id=%s
                    """,
                    (name, weight, status, market_from, market_to, now, rule_id),
                )
                ok = cur.rowcount > 0
            conn.commit()
            return ok
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deactivate(self, rule_id: int) -> bool:
        conn = self._conn()
        now = datetime.now(UTC).replace(tzinfo=None)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE market_rule SET status=%s, updated_at=%s WHERE rule_id=%s",
                    ("INACTIVE", now, rule_id),
                )
                ok = cur.rowcount > 0
            conn.commit()
            return ok
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
