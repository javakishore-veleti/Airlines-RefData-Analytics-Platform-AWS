# Airlines Reference Data Analytics Platform (ARFD)

**Project code:** `ARFD` — Airlines Reference Data

Near-real-time Change Data Capture (CDC) for airline **reference data (RD / RefData)**—kept current for operational and analytics users through dedicated portals.

---

## Introduction

Airlines depend on **reference data** that changes often—market rules, route weights, status flags, and similar operational dimensions. That data typically lives in transactional databases. Analysts, risk managers, and data managers need those changes within minutes, not on overnight batch cycles.

**ARFD** is a reference-data analytics platform that:

1. Captures row-level changes from the operational database—through a CDC and streaming path, or through **AWS native services** in the cloud—and lands them in an open analytics lake table format
2. Applies inserts, updates, and deletes so the lake reflects the current state of reference data
3. Exposes the data through middleware APIs to two portals:
   - **Airlines-RD-Admin** — create and manage source reference data
   - **Airlines-RD-Intelligence** — analysts, risk managers, and data managers view and query lake-backed data
4. Follows the same CDC → stream → apply → lake pattern described in the AWS Architecture Blog (see [References](#references)), whether running on the application stack or on AWS managed services

Delivery follows **[Superpowers](https://github.com/obra/superpowers)** (design → plan → TDD → review), with project-specific **`/arfd-*`** skills for GitHub board, milestone logging, and commit/push. Those wrappers do not replace the native Superpowers skills.

---

## Objective

| Goal | What success looks like |
|---|---|
| Near-real-time RefData lake | Source inserts, updates, and deletes appear in the analytics lake within minutes |
| Correct CDC semantics | Current-state rows stay accurate after inserts, updates, and deletes (keyed identity) |
| Repeatable runtime lifecycle | Lifecycle scripts start, stop, and report the platform services used for development and CI |
| Middleware | APIs for portals; batch jobs mounted for the orchestration runtime |
| Admin portal | `Portals/Airlines-RD-Admin` manages reference data end to end |
| Intelligence portal | `Portals/Airlines-RD-Intelligence` lets analysts, risk managers, and data managers browse and query |
| Milestone-driven delivery | GitHub milestones M01–M07 with epics / features / stories; each story runs `/arfd-story-start` → Superpowers natives → `/arfd-story-complete` |
| AWS deployment path | Milestone M07 delivers the cloud managed-service deployment of the same pattern |

**Scope (M01–M06):** CDC from the operational database into the analytics lake; middleware; both portals.

**Scope (M07):** Same pattern on AWS native / managed services.

---

## Architecture

### Application stack (M01–M06)

```
Portals/Airlines-RD-Admin ──────┐
                                ├──► Middleware/MasterData-API ──► MySQL
Portals/Airlines-RD-Intelligence┘              │
                                               ├── RabbitMQ (async / notifications)
                                               └── read APIs ──► Iceberg / query façade

MySQL (binlog)
    → Debezium → Apache Kafka
                      → Airflow (Middleware/DAGs, batched)
                            → Iceberg on S3-compatible object storage
```

### AWS managed services (M07)

```
Aurora MySQL → DMS → Kinesis → Firehose (+ Lambda) → Iceberg on S3 → Athena / Redshift / Glue
```

| Concern | Application stack | AWS managed services |
|---|---|---|
| Source DB | MySQL | Aurora MySQL |
| CDC | Debezium | DMS |
| Stream | Kafka | Kinesis |
| Batch apply | Airflow DAGs | Firehose + Lambda |
| Object store | S3-compatible storage | Amazon S3 |
| Table format | Iceberg | Iceberg |

---


## Local operator npm scripts

```bash
npm run local:containers:all:start
npm run local:containers:all:status
npm run local:containers:all:stop

npm run local:middleware:all:start
npm run local:middleware:all:status
npm run local:middleware:all:down
```

`local:middleware:*` scans `Middleware/*/app-startup.sh` (skips `Middleware/DAGs`).

## Repository layout

```text
CICD/Local/
  docker-all-up.sh
  all-down.sh
  all-status.sh
  Kafka/docker-compose.yaml
Middleware/
  MasterData-API/
  DAGs/
Portals/
  Airlines-RD-Admin/
  Airlines-RD-Intelligence/
.cursor/skills/arfd-*
.cursor/rules/
superpowers/
docs/Project_Management/
docs/ROADMAP.md
AGENTS.md
cloudformation/
```

---

## Milestones (execution order)

| # | Milestone | Focus |
|--:|-----------|--------|
| M01 | Foundation & Superpowers | ARFD methodology, docs, skeleton |
| M02 | Runtime bootstrap | Lifecycle scripts + MySQL, Kafka, RabbitMQ, Airflow, object storage |
| M03 | CDC → Iceberg | Debezium + Airflow DAGs → Iceberg |
| M04 | Middleware | MasterData-API + DAG packaging |
| M05 | Airlines-RD-Admin | RefData admin portal |
| M06 | Airlines-RD-Intelligence | Analyst / risk / data-manager portal |
| M07 | AWS deployment | Managed-service stack aligned with the Architecture Blog |

Full breakdown: [`docs/ROADMAP.md`](docs/ROADMAP.md) · milestone boards: [`docs/Project_Management/Issues/`](docs/Project_Management/Issues/)

---

## Superpowers and ARFD wrappers

Superpowers is enabled in [`.cursor/settings.json`](.cursor/settings.json). If needed in Agent chat:

```text
/add-plugin superpowers
```

**Native Superpowers:** `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, `/finishing-a-development-branch`

**ARFD wrappers** (board / git / milestone log only): `/arfd-story-start`, `/arfd-story-complete`, `/arfd-feature-complete`, `/arfd-epic-complete`, `/arfd-milestone-log`, `/arfd-commit-push`, `/arfd-progress-sync`

Skills: [`.cursor/skills/`](.cursor/skills/). Vendored copy: [`superpowers/`](superpowers/).

---

## References

- [How United Airlines streams database changes to Apache Iceberg with Amazon Data Firehose](https://aws.amazon.com/blogs/architecture/how-united-airlines-streams-database-changes-to-apache-iceberg-with-amazon-data-firehose/) — AWS Architecture Blog (source pattern for this platform)
- [obra/superpowers](https://github.com/obra/superpowers) — delivery methodology used with ARFD wrappers
- [aws-samples/sample-near-real-time-sql-to-iceberg](https://github.com/aws-samples/sample-near-real-time-sql-to-iceberg) — accompanying CloudFormation sample for the blog pattern
- [Debezium MySQL connector](https://debezium.io/documentation/reference/stable/connectors/mysql.html)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Airflow](https://airflow.apache.org/)
- [Apache Iceberg](https://iceberg.apache.org/)
