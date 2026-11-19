"""ARFD Middleware API — health + CDC event generator for Admin."""
from __future__ import annotations

import os
import random
from datetime import datetime
from typing import Literal

import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="ARFD API Services", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AIRPORTS = ["ORD", "SFO", "LAX", "JFK", "LHR", "CDG", "NRT", "SYD", "DXB", "SIN"]


def db():
    return mysql.connector.connect(
        host=os.getenv("ARFD_MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("ARFD_MYSQL_PORT", "3306")),
        user=os.getenv("ARFD_MYSQL_USER", "arfd"),
        password=os.getenv("ARFD_MYSQL_PASSWORD", "arfd"),
        database=os.getenv("ARFD_MYSQL_DATABASE", "market_db"),
    )


class GenerateRequest(BaseModel):
    count: int = Field(ge=1, le=100_000, default=10)
    mix: Literal["mixed", "insert", "update", "delete"] = "mixed"


@app.get("/health")
def health():
    try:
        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        mysql_ok = True
    except Exception as exc:  # noqa: BLE001
        mysql_ok = False
        return {"status": "degraded", "mysql": False, "error": str(exc)}
    return {"status": "ok", "mysql": mysql_ok}


@app.post("/admin/cdc/generate")
def generate_cdc(req: GenerateRequest):
    """Apply N random INSERT/UPDATE/DELETE on market_rule to simulate CDC."""
    try:
        conn = db()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"mysql unavailable: {exc}") from exc

    cur = conn.cursor()
    stats = {"insert": 0, "update": 0, "delete": 0}
    now = datetime.utcnow()

    for _ in range(req.count):
        op = req.mix
        if op == "mixed":
            op = random.choice(["insert", "update", "delete"])

        if op == "insert":
            a, b = random.sample(AIRPORTS, 2)
            cur.execute(
                "INSERT INTO market_rule "
                "(name, weight, status, effective_from, market_from, market_to, created_at, updated_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    f"{a}-{b} CDC {random.randint(1, 1_000_000)}",
                    random.randint(1, 100),
                    "ACTIVE",
                    now,
                    a,
                    b,
                    now,
                    now,
                ),
            )
            stats["insert"] += 1
        elif op == "update":
            cur.execute("SELECT rule_id FROM market_rule ORDER BY RAND() LIMIT 1")
            row = cur.fetchone()
            if not row:
                continue
            cur.execute(
                "UPDATE market_rule SET weight=%s, updated_at=%s WHERE rule_id=%s",
                (random.randint(1, 100), now, row[0]),
            )
            stats["update"] += 1
        else:
            cur.execute("SELECT rule_id FROM market_rule ORDER BY RAND() LIMIT 1")
            row = cur.fetchone()
            if not row:
                continue
            cur.execute("DELETE FROM market_rule WHERE rule_id=%s", (row[0],))
            stats["delete"] += 1

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM market_rule")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"requested": req.count, "applied": stats, "market_rule_count": total}


@app.get("/admin/market-rules/count")
def market_rule_count():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM market_rule")
    n = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"count": n}
