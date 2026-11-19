#!/usr/bin/env bash
# Tear down ARFD-managed services. Reused shared services are left running
# unless --including-shared is passed (D1).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=arfd-common.sh
source "${SCRIPT_DIR}/arfd-common.sh"

INCLUDING_SHARED=0
for arg in "$@"; do
  case "${arg}" in
    --including-shared) INCLUDING_SHARED=1 ;;
    -h|--help)
      cat <<'EOF'
Usage: ./all-down.sh [--including-shared]

Stops ARFD-started compose services (Kafka/Debezium, RabbitMQ, MinIO, and any
Airflow/Postgres/MySQL/Redis that ARFD started).

By default does NOT stop shared services that were reused (D1).
Pass --including-shared to also stop reused Airflow, PostgreSQL, MySQL, Redis
when they are still reachable (best-effort; external non-compose instances are
only stopped if they were ARFD compose containers recorded as managed-by-arfd,
or when --including-shared and they match ARFD compose project names).
EOF
      exit 0
      ;;
  esac
done

echo "ARFD: all-down (including-shared=${INCLUDING_SHARED})"

should_stop_shared() {
  local name="$1"
  local recorded
  recorded="$(state_get "${name}")"
  if [[ "${recorded}" == "managed-by-arfd" ]]; then
    return 0
  fi
  if [[ "${INCLUDING_SHARED}" -eq 1 && "${recorded}" == "reused" ]]; then
    return 0
  fi
  return 1
}

# Always stop ARFD platform compose stacks (Kafka, RabbitMQ, MinIO).
echo "  stopping Kafka/Debezium compose..."
compose_down "${SCRIPT_DIR}/Kafka" || true
echo "  stopping RabbitMQ compose..."
compose_down "${SCRIPT_DIR}/RabbitMQ" || true
echo "  stopping MinIO compose..."
compose_down "${SCRIPT_DIR}/MinIO" || true

# Shared services — conditional (D1)
mysql_state="$(state_get mysql)"
if [[ "${mysql_state}" == "managed-by-arfd" ]]; then
  echo "  stopping MySQL (managed-by-arfd)..."
  compose_down "${SCRIPT_DIR}/MySQL" || true
elif [[ "${INCLUDING_SHARED}" -eq 1 && "${mysql_state}" == "reused" ]]; then
  echo "  mysql: reused external instance — cannot stop via compose; stop it manually if needed"
else
  echo "  mysql: skipped (reused or unset; pass --including-shared for external note)"
fi

airflow_state="$(state_get airflow)"
postgres_state="$(state_get postgres)"
redis_state="$(state_get redis)"

if [[ "${airflow_state}" == "managed-by-arfd" ]] || { [[ "${INCLUDING_SHARED}" -eq 1 && "${airflow_state}" == "reused" ]]; }; then
  if [[ "${airflow_state}" == "managed-by-arfd" ]]; then
    echo "  stopping Airflow (managed-by-arfd)..."
    (cd "${SCRIPT_DIR}/Airflow" && docker compose -p "${ARFD_COMPOSE_PROJECT}" --profile arfd-airflow down --remove-orphans) || true
  else
    echo "  airflow: reused external — stop it manually if needed"
  fi
else
  echo "  airflow: skipped (reused)"
fi

if [[ "${postgres_state}" == "managed-by-arfd" ]]; then
  echo "  stopping PostgreSQL (managed-by-arfd)..."
  (cd "${SCRIPT_DIR}/Airflow" && docker compose -p "${ARFD_COMPOSE_PROJECT}" --profile arfd-postgres down --remove-orphans) || true
elif [[ "${INCLUDING_SHARED}" -eq 1 && "${postgres_state}" == "reused" ]]; then
  echo "  postgres: reused external — stop it manually if needed"
else
  echo "  postgres: skipped (reused or unset)"
fi

if [[ "${redis_state}" == "managed-by-arfd" ]]; then
  echo "  stopping Redis (managed-by-arfd)..."
  (cd "${SCRIPT_DIR}/Airflow" && docker compose -p "${ARFD_COMPOSE_PROJECT}" --profile arfd-redis down --remove-orphans) || true
elif [[ "${INCLUDING_SHARED}" -eq 1 && "${redis_state}" == "reused" ]]; then
  echo "  redis: reused external — stop it manually if needed"
else
  echo "  redis: skipped (reused or unset)"
fi

# Clear managed markers; keep reused markers unless including-shared wiped them.
if [[ "${INCLUDING_SHARED}" -eq 1 ]]; then
  rm -f "${ARFD_STATE_FILE}"
else
  state_clear_managed
fi

echo "ARFD: all-down complete."
