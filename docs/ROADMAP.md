# Roadmap — Milestones → Epics → Features → Stories

Execution order is **strict**: finish each milestone via Superpowers (brainstorm → plan → TDD → review → finish) before starting the next.

Labels (GitHub): `type:epic` · `type:feature` · `type:story` · `area:*`

---

## Milestone M0 — Foundation & Superpowers

**Goal:** Repo methodology, docs, and skeleton paths exist; agents follow Superpowers.

### Epic E0.1 — Superpowers & agent contract
- **Feature F0.1.1 — Vendor Superpowers**
  - S0.1.1.1 Vendored skills + VERSION + README
  - S0.1.1.2 Cursor rule / AGENTS.md workflow contract
  - S0.1.1.3 Document `/add-plugin superpowers` for hooks
- **Feature F0.1.2 — Product docs**
  - S0.1.2.1 README: Introduction, Objective, Architecture (local-first + AWS later)
  - S0.1.2.2 ROADMAP (this file) synced to GitHub milestones/issues

### Epic E0.2 — Repository skeleton
- **Feature F0.2.1 — Directory placeholders**
  - S0.2.1.1 `CICD/Local/` scripts + Kafka compose path stubs
  - S0.2.1.2 `Middleware/MasterData-API`, `Middleware/DAGs`
  - S0.2.1.3 `Portals/Airlines-RD-Admin`, `Portals/Airlines-RD-Intelligence`

---

## Milestone M1 — Local platform bootstrap (`CICD/Local`)

**Goal:** One-command local stack lifecycle for core infra containers.

### Epic E1.1 — Docker lifecycle scripts
- **Feature F1.1.1 — Control scripts**
  - S1.1.1.1 `CICD/Local/docker-all-up.sh`
  - S1.1.1.2 `CICD/Local/all-down.sh`
  - S1.1.1.3 `CICD/Local/all-status.sh`

### Epic E1.2 — Compose services
- **Feature F1.2.1 — Data & messaging**
  - S1.2.1.1 MySQL (binlog-ready) container + seed SQL
  - S1.2.1.2 `CICD/Local/Kafka/docker-compose.yaml` (Kafka + Debezium Connect)
  - S1.2.1.3 RabbitMQ container (API / portal messaging)
- **Feature F1.2.2 — Orchestration & storage**
  - S1.2.2.1 Apache Airflow containers; mount `Middleware/DAGs` as DAG folder
  - S1.2.2.2 Local S3-compatible object storage (MinIO or equivalent)
  - S1.2.2.3 Healthchecks + `all-status.sh` probes for every service

---

## Milestone M2 — CDC → Iceberg lake (local)

**Goal:** MySQL changes land in Iceberg on local object storage via Debezium → Kafka → Airflow batches.

### Epic E2.1 — Debezium CDC
- **Feature F2.1.1 — Connector**
  - S2.1.1.1 Debezium MySQL connector for `market_db.market_rule`
  - S2.1.1.2 Topic naming + PK partitioning strategy documented

### Epic E2.2 — Airflow batch apply
- **Feature F2.2.1 — Kafka → Iceberg DAG**
  - S2.2.1.1 DAG under `Middleware/DAGs` consumes Kafka in batches
  - S2.2.1.2 Map Debezium `c`/`u`/`d` → Iceberg insert/update/delete
  - S2.2.1.3 Write Iceberg tables to local object storage; validate with query tool

---

## Milestone M3 — Middleware

**Goal:** API layer + DAG contracts for portals and pipeline control.

### Epic E3.1 — API Services
- **Feature F3.1.1 — `Middleware/MasterData-API`** (modular monolith; split later by deploy cadence)
  - S3.1.1.0 D3 architecture + root `package.json` `local:containers:*` / `local:middleware:*`
  - S3.1.1.1 Service skeleton (health through api→facade→WF→task→dao, config, OpenAPI, `app-*.sh`)
  - S3.1.1.2 Reference-data CRUD / publish APIs against MySQL (admin path; includes GenerateCdcEvents)
  - S3.1.1.3 Read APIs over Iceberg / query façade for Intelligence portal
  - S3.1.1.4 RabbitMQ integration for async jobs / notifications

### Epic E3.2 — DAG packaging
- **Feature F3.2.1 — Airflow-relative DAGs**
  - S3.2.1.1 Stable relative mount path documented for Airflow container
  - S3.2.1.2 Shared libraries for CDC parse + Iceberg writers

---

## Milestone M4 — Portal: Airlines-RD-Admin

**Goal:** Internal **Reference Data Admin** UI to manage source reference data.

### Epic E4.1 — Admin portal
- **Feature F4.1.1 — `Portals/Airlines-RD-Admin`**
  - S4.1.1.1 App shell + auth stub (local)
  - S4.1.1.2 Market rules list / create / update / deactivate
  - S4.1.1.3 CDC status view (pipeline health summary)
  - S4.1.1.4 Wire to `Middleware/MasterData-API`

---

## Milestone M5 — Portal: Airlines-RD-Intelligence

**Goal:** Internal customer portal for analysts, risk managers, data managers to view/query lake data.

### Epic E5.1 — Intelligence portal
- **Feature F5.1.1 — `Portals/Airlines-RD-Intelligence`**
  - S5.1.1.1 App shell + role-oriented nav (analyst / risk / data manager)
  - S5.1.1.2 Browse / filter reference data from Iceberg-backed APIs
  - S5.1.1.3 Ad-hoc query / saved views (scope TBD in brainstorm)
  - S5.1.1.4 Wire to `Middleware/MasterData-API`

---

## Milestone M6 — AWS cloud parity (deferred)

**Goal:** Map proven local pipeline to AWS (Aurora, DMS, Kinesis, Firehose, S3, Glue, Athena). **No AWS deploys before this milestone is explicitly started.**

### Epic E6.1 — AWS mapping
- **Feature F6.1.1 — CloudFormation / IaC**
  - S6.1.1.1 Parameterized stack from blog sample
  - S6.1.1.2 Local→AWS cutover runbook
  - S6.1.1.3 Monitoring & cleanup procedures

---

## Target repository layout

```text
CICD/Local/
  docker-all-up.sh
  all-down.sh
  all-status.sh
  Kafka/docker-compose.yaml
Middleware/
  MasterData-API/
  DAGs/                 # mounted into Airflow
Portals/
  Airlines-RD-Admin/
  Airlines-RD-Intelligence/
superpowers/            # vendored methodology
docs/ROADMAP.md
cloudformation/         # M6 only
```

## Superpowers execution queue

| Order | Milestone | Status |
|------:|-----------|--------|
| 1 | M0 Foundation & Superpowers | Next |
| 2 | M1 Local platform bootstrap | Blocked on M0 |
| 3 | M2 CDC → Iceberg | Blocked on M1 |
| 4 | M3 Middleware | Blocked on M2 |
| 5 | M4 Airlines-RD-Admin | Blocked on M3 |
| 6 | M5 Airlines-RD-Intelligence | Blocked on M3 (can parallelize with M4 after M3) |
| 7 | M6 AWS cloud parity | Blocked on M5 (+ explicit go-ahead) |
