# ARFD design decisions

Decisions are numbered `D##`. Record new ones here when brainstorming closes them.

## D1 — Reuse already-running shared services on the developer machine

**Status:** Decided (2026-11-19)

**Context:** Developers often already run platform services on the same machine for other projects (for example Apache Airflow, PostgreSQL, MySQL, Redis). Starting a second copy from ARFD’s `CICD/Local` lifecycle scripts causes port conflicts, wasted resources, and split-brain config.

**Decision:** `CICD/Local/docker-all-up.sh`, `all-down.sh`, and `all-status.sh` (and any compose wrappers they call) must treat these as **shared machine services** when already reachable:

| Service | Reuse rule |
|---|---|
| Apache Airflow | If an Airflow API/web endpoint (or documented compose project) is already healthy on this machine, **do not** start a new Airflow stack; mount/register `Middleware/DAGs` against the existing instance (or document the attach contract). |
| PostgreSQL | If Postgres is already accepting connections on the configured host/port (or discovered default), **reuse** it; create/migrate ARFD schemas/databases only. |
| MySQL | If MySQL is already accepting connections on the configured host/port, **reuse** it; create ARFD databases/users as needed without replacing the instance. |
| Redis | If Redis is already reachable on the configured host/port, **reuse** it; use an ARFD-specific key prefix/DB index. |

**Lifecycle behavior:**

1. **up:** Probe each shared service first. If healthy → record “reused” in status output and skip `docker compose up` for that service. If missing → start only that service from ARFD compose.
2. **status:** Report `reused` vs `managed-by-arfd` vs `down` per service.
3. **down:** By default, **stop only services ARFD started in this session/project**. Do **not** tear down reused external Airflow/Postgres/MySQL/Redis unless the operator passes an explicit flag (e.g. `--including-shared`).

**Config:** Connection targets and probe URLs come from env files (git-ignored secrets) with documented defaults; no machine-specific absolute paths committed to the repo.

**Applies to:** Milestone M02 stories for lifecycle scripts and platform compose (especially orchestration, operational database, and any Postgres/Redis dependencies introduced for Airflow or Middleware).

## D2 — Historical seed and Admin CDC simulation

**Status:** Decided (2026-11-19)

**Context:** The Architecture Blog walkthrough validates CDC with a small `market_rule` table. ARFD needs volume for realistic full-load and continuous CDC testing, plus an operator control to inject change events without hand-writing SQL.

**Decision:**

1. **Seed** — `scripts/seed_market_rules.py` loads **1,000,000** synthetic `market_rule` rows by default (`--count` / `--batch-size` / `--truncate` overrides). Schema matches `CICD/Local/MySQL/init/01-market_db.sql` and `sql/01-source-aurora-mysql.sql`. Connection via `ARFD_MYSQL_*` (see `CICD/Local/.env.example`).
2. **CDC generator API** — `Middleware/API-Services` exposes `GET /health` and `POST /admin/cdc/generate` with `{ "count": N }` to apply mixed INSERT/UPDATE/DELETE against `market_rule` so Debezium can observe change events.
3. **Admin UI** — `Portals/Airlines-RD-Admin/index.html` provides a **Generate CDC events** control that calls that API.

**Out of scope for D2:** Debezium connector registration and Iceberg apply (Milestone M03).

**Next decision number:** D3

