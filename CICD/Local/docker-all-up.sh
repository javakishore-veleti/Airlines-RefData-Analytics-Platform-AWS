#!/usr/bin/env bash
# Bring up ARFD local platform services with D1 shared-service reuse.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=arfd-common.sh
source "${SCRIPT_DIR}/arfd-common.sh"

echo "ARFD: docker-all-up (D1 reuse for Airflow / PostgreSQL / MySQL / Redis)"

# --- Shared: MySQL ---
if probe_mysql; then
  echo "  mysql: reused (${ARFD_MYSQL_HOST}:${ARFD_MYSQL_PORT})"
  state_set mysql reused
else
  echo "  mysql: starting (managed-by-arfd)"
  compose_up "${SCRIPT_DIR}/MySQL"
  state_set mysql managed-by-arfd
  # Wait for port
  for _ in $(seq 1 60); do
    probe_mysql && break
    sleep 1
  done
fi

# Ensure schema/user exist (reused or managed)
init_sql="${SCRIPT_DIR}/MySQL/init/01-market_db.sql"
if probe_mysql && command -v docker >/dev/null 2>&1; then
  docker run --rm --network host \
    -v "${init_sql}:/init.sql:ro" \
    -e MYSQL_PWD="${ARFD_MYSQL_ROOT_PASSWORD}" \
    mysql:8.0 \
    mysql -h"${ARFD_MYSQL_HOST}" -P"${ARFD_MYSQL_PORT}" -uroot --protocol=TCP \
    -e "source /init.sql" >/dev/null 2>&1 \
    || docker run --rm --network host \
      -v "${init_sql}:/init.sql:ro" \
      -e MYSQL_PWD="${ARFD_MYSQL_PASSWORD}" \
      mysql:8.0 \
      mysql -h"${ARFD_MYSQL_HOST}" -P"${ARFD_MYSQL_PORT}" -u"${ARFD_MYSQL_USER}" \
      --protocol=TCP "${ARFD_MYSQL_DATABASE}" \
      -e "source /init.sql" >/dev/null 2>&1 \
    || echo "  mysql: WARN schema apply skipped (credentials / init timing)"
fi

# --- Shared: PostgreSQL (Airflow metadata) ---
if probe_postgres; then
  echo "  postgres: reused (${ARFD_POSTGRES_HOST}:${ARFD_POSTGRES_PORT})"
  state_set postgres reused
  export ARFD_AIRFLOW_POSTGRES_HOST="${ARFD_POSTGRES_HOST}"
  export ARFD_AIRFLOW_POSTGRES_PORT="${ARFD_POSTGRES_PORT}"
else
  echo "  postgres: starting (managed-by-arfd)"
  compose_up "${SCRIPT_DIR}/Airflow" --profile arfd-postgres postgres
  state_set postgres managed-by-arfd
  export ARFD_AIRFLOW_POSTGRES_HOST=postgres
  export ARFD_AIRFLOW_POSTGRES_PORT=5432
  for _ in $(seq 1 60); do
    probe_postgres && break
    sleep 1
  done
fi

# --- Shared: Redis ---
if probe_redis; then
  echo "  redis: reused (${ARFD_REDIS_HOST}:${ARFD_REDIS_PORT})"
  state_set redis reused
else
  echo "  redis: starting (managed-by-arfd)"
  compose_up "${SCRIPT_DIR}/Airflow" --profile arfd-redis redis
  state_set redis managed-by-arfd
  for _ in $(seq 1 30); do
    probe_redis && break
    sleep 1
  done
fi

# --- Shared: Airflow ---
if probe_airflow; then
  echo "  airflow: reused (${ARFD_AIRFLOW_URL})"
  echo "           attach Middleware/DAGs to the existing instance (see README)"
  state_set airflow reused
else
  echo "  airflow: starting (managed-by-arfd); DAGs mount Middleware/DAGs"
  # When Postgres is reused on host, Airflow containers need host.docker.internal
  if [[ "$(state_get postgres)" == "reused" ]]; then
    export ARFD_AIRFLOW_POSTGRES_HOST=host.docker.internal
    export ARFD_AIRFLOW_POSTGRES_PORT="${ARFD_POSTGRES_PORT}"
  else
    export ARFD_AIRFLOW_POSTGRES_HOST=postgres
    export ARFD_AIRFLOW_POSTGRES_PORT=5432
  fi
  compose_up "${SCRIPT_DIR}/Airflow" --profile arfd-airflow airflow-init
  compose_up "${SCRIPT_DIR}/Airflow" --profile arfd-airflow airflow-webserver airflow-scheduler
  state_set airflow managed-by-arfd
fi

# --- Platform: Kafka + Debezium (start if not already up) ---
if probe_kafka && probe_debezium; then
  echo "  kafka+debezium: already up — skip compose"
  state_set kafka managed-by-arfd
  state_set debezium managed-by-arfd
else
  echo "  kafka+debezium: starting"
  compose_up "${SCRIPT_DIR}/Kafka"
  state_set kafka managed-by-arfd
  state_set debezium managed-by-arfd
fi

# --- Platform: RabbitMQ ---
if probe_rabbitmq; then
  echo "  rabbitmq: already up — skip compose"
  state_set rabbitmq managed-by-arfd
else
  echo "  rabbitmq: starting"
  compose_up "${SCRIPT_DIR}/RabbitMQ"
  state_set rabbitmq managed-by-arfd
fi

# --- Platform: MinIO ---
if probe_minio; then
  echo "  minio: already up — skip compose"
  state_set minio managed-by-arfd
else
  echo "  minio: starting"
  compose_up "${SCRIPT_DIR}/MinIO"
  state_set minio managed-by-arfd
fi

echo "ARFD: docker-all-up complete. Run ./all-status.sh for labels."
