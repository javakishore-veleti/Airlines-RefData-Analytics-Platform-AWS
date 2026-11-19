#!/usr/bin/env bash
# Shared helpers for CICD/Local lifecycle scripts (D1 reuse).
# shellcheck disable=SC2034

ARFD_LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARFD_REPO_ROOT="$(cd "${ARFD_LOCAL_DIR}/../.." && pwd)"
ARFD_STATE_DIR="${ARFD_REPO_ROOT}/runtime_data/cicd-local"
ARFD_STATE_FILE="${ARFD_STATE_DIR}/started.env"
ARFD_COMPOSE_PROJECT="${ARFD_COMPOSE_PROJECT:-arfd}"

mkdir -p "${ARFD_STATE_DIR}"

# Load env: .env.example defaults, then optional .env overrides.
_load_env() {
  local f
  for f in "${ARFD_LOCAL_DIR}/.env.example" "${ARFD_LOCAL_DIR}/.env"; do
    if [[ -f "${f}" ]]; then
      set -a
      # shellcheck disable=SC1090
      source "${f}"
      set +a
    fi
  done
  : "${ARFD_MYSQL_HOST:=127.0.0.1}"
  : "${ARFD_MYSQL_PORT:=3306}"
  : "${ARFD_MYSQL_USER:=arfd}"
  : "${ARFD_MYSQL_PASSWORD:=arfd}"
  : "${ARFD_MYSQL_ROOT_PASSWORD:=arfdroot}"
  : "${ARFD_MYSQL_DATABASE:=market_db}"
  : "${ARFD_POSTGRES_HOST:=127.0.0.1}"
  : "${ARFD_POSTGRES_PORT:=5432}"
  : "${ARFD_POSTGRES_USER:=arfd}"
  : "${ARFD_POSTGRES_PASSWORD:=arfd}"
  : "${ARFD_POSTGRES_DB:=arfd}"
  : "${ARFD_REDIS_HOST:=127.0.0.1}"
  : "${ARFD_REDIS_PORT:=6379}"
  : "${ARFD_REDIS_DB:=1}"
  : "${ARFD_AIRFLOW_URL:=http://127.0.0.1:8080/health}"
  : "${ARFD_KAFKA_BOOTSTRAP:=127.0.0.1:9092}"
  : "${ARFD_DEBEZIUM_URL:=http://127.0.0.1:8083}"
  : "${ARFD_RABBITMQ_HOST:=127.0.0.1}"
  : "${ARFD_RABBITMQ_PORT:=5672}"
  : "${ARFD_RABBITMQ_MGMT_URL:=http://127.0.0.1:15672}"
  : "${ARFD_RABBITMQ_USER:=arfd}"
  : "${ARFD_RABBITMQ_PASSWORD:=arfd}"
  : "${ARFD_MINIO_URL:=http://127.0.0.1:9000}"
  : "${ARFD_MINIO_CONSOLE_URL:=http://127.0.0.1:9001}"
  : "${ARFD_MINIO_ROOT_USER:=arfdminio}"
  : "${ARFD_MINIO_ROOT_PASSWORD:=arfdminio}"
  : "${ARFD_MINIO_BUCKET:=arfd-lake}"
}
_load_env

_tcp_open() {
  local host="$1" port="$2"
  if command -v nc >/dev/null 2>&1; then
    nc -z -w 1 "${host}" "${port}" >/dev/null 2>&1
    return $?
  fi
  (echo >/dev/tcp/"${host}"/"${port}") >/dev/null 2>&1
}

probe_mysql() {
  _tcp_open "${ARFD_MYSQL_HOST}" "${ARFD_MYSQL_PORT}"
}

probe_postgres() {
  _tcp_open "${ARFD_POSTGRES_HOST}" "${ARFD_POSTGRES_PORT}"
}

probe_redis() {
  _tcp_open "${ARFD_REDIS_HOST}" "${ARFD_REDIS_PORT}"
}

probe_airflow() {
  if command -v curl >/dev/null 2>&1; then
    curl -sf --max-time 2 "${ARFD_AIRFLOW_URL}" >/dev/null 2>&1
    return $?
  fi
  _tcp_open "127.0.0.1" "8080"
}

probe_kafka() {
  local host port
  host="${ARFD_KAFKA_BOOTSTRAP%%:*}"
  port="${ARFD_KAFKA_BOOTSTRAP##*:}"
  _tcp_open "${host}" "${port}"
}

probe_debezium() {
  if command -v curl >/dev/null 2>&1; then
    curl -sf --max-time 2 "${ARFD_DEBEZIUM_URL}/" >/dev/null 2>&1
    return $?
  fi
  _tcp_open "127.0.0.1" "8083"
}

probe_rabbitmq() {
  _tcp_open "${ARFD_RABBITMQ_HOST}" "${ARFD_RABBITMQ_PORT}"
}

probe_minio() {
  if command -v curl >/dev/null 2>&1; then
    curl -sf --max-time 2 "${ARFD_MINIO_URL}/minio/health/live" >/dev/null 2>&1
    return $?
  fi
  _tcp_open "127.0.0.1" "9000"
}

# State file helpers: KEY=reused|managed-by-arfd
state_set() {
  local key="$1" value="$2"
  mkdir -p "${ARFD_STATE_DIR}"
  touch "${ARFD_STATE_FILE}"
  if grep -q "^${key}=" "${ARFD_STATE_FILE}" 2>/dev/null; then
    # portable in-place update
    local tmp
    tmp="$(mktemp)"
    awk -v k="${key}" -v v="${value}" -F= 'BEGIN{OFS="="} $1==k{$2=v} {print}' "${ARFD_STATE_FILE}" >"${tmp}"
    mv "${tmp}" "${ARFD_STATE_FILE}"
  else
    echo "${key}=${value}" >>"${ARFD_STATE_FILE}"
  fi
}

state_get() {
  local key="$1"
  [[ -f "${ARFD_STATE_FILE}" ]] || { echo ""; return 0; }
  awk -F= -v k="${key}" '$1==k{print $2; exit}' "${ARFD_STATE_FILE}"
}

state_clear_managed() {
  [[ -f "${ARFD_STATE_FILE}" ]] || return 0
  local tmp
  tmp="$(mktemp)"
  awk -F= '$2!="managed-by-arfd"{print}' "${ARFD_STATE_FILE}" >"${tmp}"
  mv "${tmp}" "${ARFD_STATE_FILE}"
}

compose_up() {
  local dir="$1"
  shift
  (cd "${dir}" && docker compose -p "${ARFD_COMPOSE_PROJECT}" up -d "$@")
}

compose_down() {
  local dir="$1"
  (cd "${dir}" && docker compose -p "${ARFD_COMPOSE_PROJECT}" down --remove-orphans)
}

label_shared() {
  # Prints reused | managed-by-arfd | down for a shared D1 service.
  local name="$1"
  local probe_fn="$2"
  local recorded
  recorded="$(state_get "${name}")"
  if ${probe_fn}; then
    if [[ "${recorded}" == "managed-by-arfd" ]]; then
      echo "managed-by-arfd"
    elif [[ "${recorded}" == "reused" ]]; then
      echo "reused"
    else
      # Healthy but no ARFD record → treat as external reuse.
      echo "reused"
    fi
  else
    echo "down"
  fi
}

label_platform() {
  local name="$1"
  local probe_fn="$2"
  if ${probe_fn}; then
    echo "managed-by-arfd"
  else
    echo "down"
  fi
}

ensure_mysql_schema() {
  # Create market_db / market_rule when MySQL is reachable (reused or managed).
  if ! command -v docker >/dev/null 2>&1; then
    return 0
  fi
  local init_sql="${ARFD_LOCAL_DIR}/MySQL/init/01-market_db.sql"
  if [[ ! -f "${init_sql}" ]]; then
    return 0
  fi
  # Prefer mysql client in a throwaway container against host port.
  docker run --rm --network host \
    -e MYSQL_PWD="${ARFD_MYSQL_PASSWORD}" \
    -v "${init_sql}:/init.sql:ro" \
    mysql:8.0 \
    mysql -h"${ARFD_MYSQL_HOST}" -P"${ARFD_MYSQL_PORT}" -u"${ARFD_MYSQL_USER}" \
    --protocol=TCP < /dev/null 2>/dev/null || true
  docker run --rm --network host \
    -e MYSQL_PWD="${ARFD_MYSQL_ROOT_PASSWORD}" \
    -v "${init_sql}:/init.sql:ro" \
    mysql:8.0 \
    mysql -h"${ARFD_MYSQL_HOST}" -P"${ARFD_MYSQL_PORT}" -uroot \
    --protocol=TCP -e "source /init.sql" 2>/dev/null \
    || docker run --rm --network host \
      -e MYSQL_PWD="${ARFD_MYSQL_PASSWORD}" \
      -v "${init_sql}:/init.sql:ro" \
      mysql:8.0 \
      mysql -h"${ARFD_MYSQL_HOST}" -P"${ARFD_MYSQL_PORT}" -u"${ARFD_MYSQL_USER}" \
      --protocol=TCP -e "source /init.sql" 2>/dev/null \
    || echo "WARN: could not apply MySQL init SQL (ensure market_db exists)." >&2
}
