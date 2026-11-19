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

Expect `binlog_format=ROW`, `binlog_row_image=FULL`, `binlog_checksum=NONE` (set in `MySQL/docker-compose.yaml`). User `arfd` is granted `REPLICATION SLAVE` / `REPLICATION CLIENT` for Debezium.

### Register Debezium connector for `market_rule` (M03 / D4)

Connect reaches MySQL via `host.docker.internal` (see `Kafka/docker-compose.yaml` `extra_hosts`). Set `ARFD_MYSQL_PORT` in `.env` if MySQL is not on 3306.

```bash
# After docker-all-up (MySQL + Kafka/Connect healthy)
cd CICD/Local/Kafka
./register-market-rule-connector.sh
# Expect connector state RUNNING
curl -s http://127.0.0.1:8083/connectors/arfd-market-rule-mysql/status | python3 -m json.tool

# Smoke: write rows then consume (topic arfd.market_db.market_rule)
# e.g. POST /admin/cdc/generate or SQL against market_db.market_rule
```

Config checked in: `Kafka/connectors/market-rule-mysql.json`.

### Reused Airflow — DAG attach

When Airflow is reused, point its DAG folder (or git-sync) at this repo’s `Middleware/DAGs` directory. Do not start a second Airflow on port 8080.

## Seed + CDC generator (D2)

```bash
# 1,000,000 synthetic market_rule rows
pip install pymysql
python scripts/seed_market_rules.py --count 1000000

# Middleware API (health + CDC generate) — default port 8110
cd Middleware/MasterData-API
pip install -r requirements.txt
./run.sh
# or: uvicorn app.main:app --host 127.0.0.1 --port 8110

# Admin UI (API base defaults to http://127.0.0.1:8110)
open Portals/Airlines-RD-Admin/index.html
# or: python -m http.server 5500 --directory Portals/Airlines-RD-Admin
```

`POST /admin/cdc/generate` body: `{"count": 10}` — mixed INSERT/UPDATE/DELETE on `market_rule` so Debezium can emit change events.
