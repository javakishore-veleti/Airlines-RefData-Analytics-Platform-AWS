# CICD/Local — ARFD runtime lifecycle

## Quick start

```bash
cp CICD/Local/.env.example CICD/Local/.env
./CICD/Local/docker-all-up.sh
./CICD/Local/all-status.sh
```

## D1 — Shared service reuse

Before starting anything, scripts probe this machine:

| Service | Behavior |
|---|---|
| MySQL | Reuse if port healthy; otherwise start `MySQL/docker-compose.yaml` |
| PostgreSQL | **Reuse only** (never start a second Postgres) |
| Redis | **Reuse only** |
| Airflow | **Reuse only** — point existing Airflow `DAGS_FOLDER` at `Middleware/DAGs` |
| Kafka / Debezium / RabbitMQ / MinIO | Reuse if already up; otherwise start ARFD compose |

`./all-down.sh` stops **only** services ARFD started. Pass `--including-shared` to acknowledge shared services (Airflow/Postgres/Redis still must be stopped from their own tooling).

Status labels: `reused` | `managed-by-arfd` | `down`.

## Seed 1M market rules

```bash
pip install mysql-connector-python
python scripts/seed_market_rules.py --count 1000000
```

## API + Admin CDC simulator

```bash
cd Middleware/API-Services
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8100
```

Open `Portals/Airlines-RD-Admin/index.html` and use **Generate CDC events**.

## Attach existing Airflow

Set the existing Airflow deployment’s DAGs folder (or an extra volume) to the absolute path of `Middleware/DAGs` in this repo. The `arfd_heartbeat` DAG should appear after a refresh.
