"""M02-compatible CDC generate endpoint (full WF layering lands in #32)."""

from __future__ import annotations

import random
from datetime import UTC, datetime

import pymysql
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings

router = APIRouter(tags=["admin-cdc"])

AIRPORTS = [
    "ORD", "SFO", "LAX", "JFK", "ATL", "DFW", "DEN", "SEA", "MIA", "BOS",
]


class GenerateCdcRequest(BaseModel):
    count: int = Field(..., ge=1, le=100_000, description="Number of CDC-triggering writes")


class GenerateCdcResponse(BaseModel):
    requested: int
    inserted: int
    updated: int
    deleted: int
    message: str


def _mysql_conn():
    s = get_settings()
    return pymysql.connect(
        host=s.mysql_host,
        port=s.mysql_port,
        user=s.mysql_user,
        password=s.mysql_password,
        database=s.mysql_database,
        charset="utf8mb4",
        autocommit=False,
    )


@router.post("/admin/cdc/generate", response_model=GenerateCdcResponse)
def generate_cdc(body: GenerateCdcRequest) -> GenerateCdcResponse:
    """Insert/update/delete market_rule rows to produce Debezium CDC events."""
    try:
        conn = _mysql_conn()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"MySQL unavailable: {exc}") from exc

    inserted = 0
    updated = 0
    deleted = 0
    now = datetime.now(UTC).replace(tzinfo=None)
    try:
        with conn.cursor() as cur:
            insert_budget = max(1, (body.count * 2) // 5)
            update_budget = (body.count * 2) // 5
            delete_budget = body.count - insert_budget - update_budget

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
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        conn.close()

    total = inserted + updated + deleted
    return GenerateCdcResponse(
        requested=body.count,
        inserted=inserted,
        updated=updated,
        deleted=deleted,
        message=f"Generated {total} MySQL writes for CDC (insert/update/delete)",
    )
