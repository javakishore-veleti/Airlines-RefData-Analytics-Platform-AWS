# CICD/Local — ARFD runtime lifecycle

Local-first platform bootstrap for Milestone **M02**. No AWS resources are created here.

## Scripts

| Script | Role |
|---|---|
| `docker-all-up.sh` | Probe shared services first (D1); start only what is missing |
| `all-down.sh` | Stop ARFD-started compose services; leave reused shared services alone |
| `all-status.sh` | Print `reused` / `managed-by-arfd` / `down` per service (non-zero if any required service is `down`) |
| `arfd-common.sh` | Shared probes, env loading, compose helpers |

### D1 — Shared service reuse

Before starting a second copy, scripts probe:

| Service | Default probe |
|---|---|
| MySQL | `ARFD_MYSQL_HOST:ARFD_MYSQL_PORT` (3306) |
| PostgreSQL | `ARFD_POSTGRES_HOST:ARFD_POSTGRES_PORT` (5432) |
| Redis | `ARFD_REDIS_HOST:ARFD_REDIS_PORT` (6379) |
| Airflow | `ARFD_AIRFLOW_URL` (`http://127.0.0.1:8080/health`) |

- **up:** healthy → record `reused` and skip compose for that service; missing → start from ARFD compose and record `managed-by-arfd`.
- **down:** stops only ARFD-managed services by default. Pass `--including-shared` for operator notes / force-stop of ARFD-managed shared containers.
- **status:** labels each shared service `reused` \| `managed-by-arfd` \| `down`.

Runtime markers live under `runtime_data/cicd-local/` (git-ignored).

### Usage

```bash
cd CICD/Local
cp .env.example .env   # optional overrides
./docker-all-up.sh
./all-status.sh
./all-down.sh
./all-down.sh --including-shared
```

## Compose stacks

| Path | Services | Notes |
|---|---|---|
| `MySQL/` | MySQL 8 (ROW binlog, GTID) | Skipped when MySQL already healthy (D1). Init: `MySQL/init/01-market_db.sql` |
| `Kafka/` | Zookeeper, Kafka, Debezium Connect | CDC path; started if Kafka/Connect not already up |
| `RabbitMQ/` | RabbitMQ + management UI (`:15672`) | Local creds: `arfd` / `arfd`, vhost `arfd` |
| `MinIO/` | MinIO + bucket init | Bucket `arfd-lake`; lake prefix `market_db/market_rule/` |
| `Airflow/` | Postgres, Redis, webserver, scheduler | Profiles `arfd-postgres` / `arfd-redis` / `arfd-airflow`. DAGs mount: `Middleware/DAGs` → `/opt/airflow/dags` |

### CDC prerequisites (MySQL)

Expect `binlog_format=ROW`, `binlog_row_image=FULL`, `binlog_checksum=NONE` (set in `MySQL/docker-compose.yaml`). User `arfd` is granted `REPLICATION SLAVE` / `REPLICATION CLIENT` for Debezium (wired in M03).

### Reused Airflow — DAG attach

When Airflow is reused, point its DAG folder (or git-sync) at this repo’s `Middleware/DAGs` directory. Do not start a second Airflow on port 8080.

## Seed + CDC generator (D2)

```bash
# 1,000,000 synthetic market_rule rows
pip install pymysql
python scripts/seed_market_rules.py --count 1000000

# Middleware API (health + CDC generate)
cd Middleware/API-Services
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8100

# Admin UI
open Portals/Airlines-RD-Admin/index.html
# or: python -m http.server 5500 --directory Portals/Airlines-RD-Admin
```

`POST /admin/cdc/generate` body: `{"count": 10}` — inserts/updates rows so Debezium can emit change events.
