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

## D3 — MasterData-API modular monolith and layering

**Status:** Decided (2026-11-19) — story #56  
**Spec:** `docs/Superpowers/specs/2026-11-19-m04-0011-d3-masterdata-api-architecture.md`

**Summary:** `Middleware/MasterData-API/` is the FastAPI modular-monolith project root. The same layering applies later to `Middleware/AccountService-API/` (#58+).

**Call chain (mandatory):** `api → facade → WF → tasks → dao`. Business work does not skip layers.

| Concern | Rule |
|---|---|
| Project root | `Middleware/MasterData-API/` (FastAPI + OpenAPI) |
| Facades | `interface.py` + `impl.py`; callers use the interface |
| WF | Folder name starts with **`WF`** (e.g. `WFHealth`, `WFGenerateCdcEvents`); owns orchestration + `tasks/` |
| Tasks | Single-purpose units invoked by the WF |
| DAO | Persistence only (MySQL OLTP; lake readers when needed) |
| DTOs | `Ctx` / `Req` / `Resp` under `common/dtos/` — no raw ORM across facade/WF |
| object_factory | Per-layer bean lookup so tests can swap implementations |
| Packages | Domain-first under each layer (health, market_rule, cdc, lake_query, messaging) |
| Lifecycle | `app-startup.sh` / `app-status.sh` / `app-shutdown.sh` at the service root |
| Operator npm | Root `package.json` `local:containers:*` / `local:middleware:*` discover `Middleware/*/app-*.sh` (#55) |

**Reference use cases:** **Health** (#31 skeleton) and **GenerateCdcEvents** (#32 Admin write path).

**Implementing stories:** #31 skeleton, #55 npm scripts, #32 write APIs, #33 lake read façade, #34 async messaging.

## D4 — Debezium CDC for `market_db.market_rule`

**Status:** Decided (2026-11-19) — story #23

**Decision:** Register a Debezium MySQL connector on the local Connect cluster for `market_db.market_rule` only. Config: `CICD/Local/Kafka/connectors/market-rule-mysql.json`. Topic prefix `arfd`. Connect reaches MySQL via `host.docker.internal` + `ARFD_MYSQL_*`. Spec: `docs/Superpowers/specs/2026-11-19-m03-0003-cdc-market-rule-design.md`.

## D5 — Portal UI system (Angular, professional light theme)

**Status:** Decided (2026-11-19) — stories #62 / #40 / #46

**Context:** Admin and Intelligence portals must look like professional airline/enterprise SaaS — not academic gray slabs, not pure black, not generic purple AI themes. Research favors PrimeNG light presets + tinted neutrals + modern SVG icons over stock Bootstrap gray.

**Decision:**

| Layer | Choice |
|---|---|
| Framework | Angular (both `Portals/Airlines-RD-Admin` and `Portals/Airlines-RD-Intelligence`) |
| Primary components | **PrimeNG** with **Aura** or **Lara** light theme (tables, overlays, forms, menus) |
| Layout grid | Bootstrap 5 **Sass only** for grid/spacing; remap `$gray-*` / `$body-*` to ARFD tokens — do **not** ship default Bootstrap chrome |
| Icons | **Lucide** (`lucide-angular`); Phosphor Duotone optional for brand marks |
| Typography | **Plus Jakarta Sans** (geometric sans), body line-height ≥ 1.5 |
| Layout pattern | Top main menu bar + collapsible left nav + bright workspace; favicon + brand mark required |
| Auth UI | Signup / signin against **AccountService-API** (#57–#60) |
| Admin-only | **User Management** menu → AccountService user CRUD (#61) |

**Color tokens (no pure black / sterile gray):**

| Role | Token | Hex |
|---|---|---|
| Text / nav | Deep navy | `#0F172A` |
| Secondary text | Muted indigo | `#475569` |
| Canvas | Ice blue | `#F4F8FB` |
| Surfaces | White | `#FFFFFF` |
| Borders | Powder blue | `#DBEAFE` |
| Accent / CTA | Sky | `#0284C7` |
| Accent hover | Sky deep | `#0369A1` |

**60/30/10:** ~60% white + ice canvas, ~30% navy nav/headers, ~10% sky CTAs/active states.

**Forbidden defaults:** `#000000` body text, `#808080` / flat gray page chrome, dark-mode-first shells, purple-indigo gradient clichés.

**Applies to:** M05 #40/#61/#62, M06 #46; shared tokens live under each portal’s `styles/` (extract shared theme package later if duplication hurts).

## D6 — CDC topic naming and keys

**Status:** Decided (2026-11-19) — story #24

**Decision:** Topic `arfd.market_db.market_rule` with Debezium key=`rule_id` for per-rule ordering. Schema history topic `arfd.schemahistory.market_rule`. Spec: `docs/Superpowers/specs/2026-11-19-m03-0004-topic-naming.md`.

## D7 — CDC apply to local lake files

**Status:** Decided (2026-11-19) — stories #26–#28

**Decision:** Batch consumer under `Middleware/DAGs` (`arfd_cdc_market_rule_apply_dag.py`) runs `scripts/cdc_apply_market_rule.py`, mapping Debezium `c/r→insert`, `u→update`, `d→delete` via `lib/cdc_parse.py`, writing JSON objects under `runtime_data/lake/market_db/market_rule/rule_id=*.json` (MinIO-compatible prefix). Validate with `scripts/verify_lake_market_rule.py`.

**Next decision number:** D8

