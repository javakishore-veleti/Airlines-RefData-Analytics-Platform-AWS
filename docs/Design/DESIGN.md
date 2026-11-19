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

**Next decision number:** D2
