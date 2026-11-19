# CICD/Local — ARFD runtime lifecycle

Scripts:

- `docker-all-up.sh` — start ARFD-managed services; **reuse** healthy Airflow, PostgreSQL, MySQL, Redis already on this machine (D1)
- `all-down.sh` — stop only ARFD-started services (use `--including-shared` to stop reused ones)
- `all-status.sh` — report `reused` / `managed-by-arfd` / `down`

Compose:

- `Kafka/docker-compose.yaml` — streaming + CDC connector stack
- Additional compose files added under M02 for MySQL, object storage, messaging as needed
