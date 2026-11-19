# Middleware/DAGs

Airflow DAG home for ARFD batch apply jobs.

When `CICD/Local/docker-all-up.sh` starts Airflow, this directory is mounted at `/opt/airflow/dags`.

When Airflow is **reused** (D1), point the existing instance’s DAG folder at this path.

CDC → Iceberg apply DAGs land in Milestone M03.
