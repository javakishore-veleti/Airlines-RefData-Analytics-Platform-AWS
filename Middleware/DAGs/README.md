# Middleware/DAGs

Airflow DAG home for ARFD batch apply jobs.

## Mount contract (M04-0008 / #36)

| Host path (repo-relative) | Container path | How |
|---|---|---|
| `Middleware/DAGs` | `/opt/airflow/dags` | `CICD/Local/docker-all-up.sh` / Airflow compose bind-mount |

Rules:
- Keep DAGs **relative** to the repo root (`Middleware/DAGs/...`) so Airflow and operators share one tree.
- Shared libraries live in `Middleware/DAGs/lib/` (CDC parse + lake writer) and must remain importable from DAG modules.
- Do **not** add `app-startup.sh` here — npm `local:middleware:*` intentionally skips this directory.
- When Airflow is **reused** (D1), point the existing instance DAG folder at this host path (same absolute path the compose mount would use).

## Contents

- `arfd_cdc_market_rule_apply_dag.py` — CDC → local lake apply
- `arfd_heartbeat_dag.py` — smoke
- `lib/cdc_parse.py`, `lib/lake_writer.py` — shared helpers (#37)
- `tests/` — unit tests for parse/mapping
