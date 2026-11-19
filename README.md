# Airlines Reference Data Analytics Platform (ARFD)

**Project code:** `ARFD` — Airlines Reference Data

Near-real-time Change Data Capture (CDC) for airline **reference data (RD / RefData)**, landing in Apache Iceberg. Built **local-first**, then mapped to AWS.

> **Status:** Planning / board setup. **No AWS stacks.** Work runs **one milestone at a time** with Superpowers natives plus ARFD board wrappers (`/arfd-story-start`, …). See [`docs/ROADMAP.md`](docs/ROADMAP.md) and [`docs/Project_Management/`](docs/Project_Management/) (milestone docs coming alongside GitHub issues).

---

## Introduction

Airlines depend on **reference data** that changes often—market rules, route weights, status flags, and similar operational dimensions. That data usually lives in transactional MySQL. Analysts, risk managers, and data managers need those changes within minutes, not on overnight batch cycles.

**ARFD** is a reference-data analytics platform that:

1. Captures row-level changes from local MySQL with **Debezium** into **Apache Kafka**
2. Applies them in **batches** with **Apache Airflow** DAGs into **Apache Iceberg** on local S3-compatible object storage
3. Serves two portals through **Middleware/API-Services** (with **RabbitMQ** for async messaging):
   - **Airlines-RD-Admin** — create and manage source reference data
   - **Airlines-RD-Intelligence** — internal customers view and query lake-backed data
4. Later maps the same CDC → stream → batch-apply → Iceberg pattern to AWS (DMS, Kinesis, Firehose, S3), following the architecture described in the AWS Architecture Blog (see [References](#references))

Delivery uses **[Superpowers](https://github.com/obra/superpowers)** for design → plan → TDD → review, with project-specific **`/arfd-*`** skills as thin wrappers for GitHub board, milestone logging, and commit/push—not replacements for the native Superpowers skills.

---

## Objective

| Goal | What success looks like |
|---|---|
| Near-real-time RefData lake (local) | Inserts, updates, and deletes on MySQL appear in Iceberg tables on local object storage via Debezium → Kafka → Airflow |
| Correct CDC semantics | Operations applied with merge/upsert semantics on a unique key (e.g. `rule_id`) |
| One-command local platform | `CICD/Local/docker-all-up.sh`, `all-down.sh`, and `all-status.sh` manage MySQL, Kafka/Debezium, RabbitMQ, Airflow, and object storage |
| Middleware | `Middleware/API-Services` for portals; `Middleware/DAGs` mounted into Airflow by relative path |
| Admin portal | `Portals/Airlines-RD-Admin` manages reference data end to end |
| Intelligence portal | `Portals/Airlines-RD-Intelligence` lets analysts, risk managers, and data managers browse and query |
| Disciplined delivery (ARFD) | GitHub milestones M01–M07 with epics / features / stories; each story runs `/arfd-story-start` → Superpowers natives → `/arfd-story-complete` |
| AWS parity later | Milestone M07 only—no CloudFormation or paid AWS provisioning before then |

**Phase 1 in scope:** local MySQL (`market_db.market_rule`) → Debezium → Kafka → Airflow → Iceberg; Middleware; both portals.

**Phase 1 out of scope:** AWS DMS, Kinesis, Firehose, Lambda, Glue, Athena, and any live AWS stack creates.

---

## Architecture

### Phase 1 — Local (M01–M06)

```
Portals/Airlines-RD-Admin ──────┐
                                ├──► Middleware/API-Services ──► MySQL
Portals/Airlines-RD-Intelligence┘              │
                                               ├── RabbitMQ (async / notifications)
                                               └── read APIs ──► Iceberg / query façade

MySQL (binlog)
    → Debezium → Apache Kafka
                      → Airflow (Middleware/DAGs, batched)
                            → Iceberg on local object storage (e.g. MinIO)
```

### Phase 2 — AWS (M07, deferred)

```
Aurora MySQL → DMS → Kinesis → Firehose (+ Lambda) → Iceberg on S3 → Athena / Redshift / Glue
```

| Concern | Local (ARFD Phase 1) | AWS (later) |
|---|---|---|
| Source DB | MySQL | Aurora MySQL |
| CDC | Debezium | DMS |
| Stream | Kafka | Kinesis |
| Batch apply | Airflow DAGs | Firehose + Lambda |
| Object store | MinIO (or equivalent) | S3 |
| Table format | Iceberg | Iceberg |

---

## Repository layout (target)

```text
CICD/Local/
  docker-all-up.sh
  all-down.sh
  all-status.sh
  Kafka/docker-compose.yaml
Middleware/
  API-Services/
  DAGs/
Portals/
  Airlines-RD-Admin/
  Airlines-RD-Intelligence/
.cursor/skills/arfd-*     # board wrappers around Superpowers natives
.cursor/rules/            # hard gate: no product code without story + milestone
superpowers/              # vendored Superpowers skills
docs/Project_Management/  # milestone markdown (CCAA-style)
docs/ROADMAP.md
AGENTS.md
cloudformation/           # M07 only
```

---

## Milestones (execution order)

| # | Milestone | Focus |
|--:|-----------|--------|
| M01 | Foundation & Superpowers | ARFD methodology, docs, skeleton |
| M02 | Local platform bootstrap | Docker up/down/status + MySQL, Kafka, RabbitMQ, Airflow, MinIO |
| M03 | CDC → Iceberg | Debezium + Airflow DAGs → Iceberg |
| M04 | Middleware | API-Services + DAG packaging |
| M05 | Airlines-RD-Admin | RefData admin portal |
| M06 | Airlines-RD-Intelligence | Analyst / risk / data-manager portal |
| M07 | AWS cloud parity | Blog-aligned AWS stack (**deferred**) |

Full breakdown: [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## Superpowers and ARFD wrappers

Install Superpowers in Cursor:

```text
/add-plugin superpowers
```

**Native Superpowers** (design and build): `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, `/finishing-a-development-branch`

**ARFD wrappers** (board / git / milestone log only): `/arfd-story-start`, `/arfd-story-complete`, `/arfd-feature-complete`, `/arfd-epic-complete`, `/arfd-milestone-log`, `/arfd-commit-push`, `/arfd-progress-sync`

Skills live under [`.cursor/skills/`](.cursor/skills/). Vendored Superpowers copy: [`superpowers/`](superpowers/).

---

## References

- [How United Airlines streams database changes to Apache Iceberg with Amazon Data Firehose](https://aws.amazon.com/blogs/architecture/how-united-airlines-streams-database-changes-to-apache-iceberg-with-amazon-data-firehose/) — AWS Architecture Blog (source pattern for this platform)
- [obra/superpowers](https://github.com/obra/superpowers) — AI coding methodology used with ARFD wrappers
- [aws-samples/sample-near-real-time-sql-to-iceberg](https://github.com/aws-samples/sample-near-real-time-sql-to-iceberg) — accompanying CloudFormation sample for the blog pattern
- [Debezium MySQL connector](https://debezium.io/documentation/reference/stable/connectors/mysql.html)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache Airflow](https://airflow.apache.org/)
- [Apache Iceberg](https://iceberg.apache.org/)
