#!/usr/bin/env bash
# D1 probes — detect healthy shared services on this machine.
# shellcheck disable=SC2034

arfd_load_env() {
  local root dir envf
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  envf="${dir}/.env"
  if [[ -f "${envf}" ]]; then
    # shellcheck disable=SC1090
    set -a; source "${envf}"; set +a
  elif [[ -f "${dir}/.env.example" ]]; then
    set -a; source "${dir}/.env.example"; set +a
  fi
  ARFD_COMPOSE_PROJECT="${ARFD_COMPOSE_PROJECT:-arfd}"
  ARFD_STATE_DIR="${ARFD_STATE_DIR:-${dir}/.arfd-state}"
  mkdir -p "${ARFD_STATE_DIR}"
}

arfd_tcp_open() {
  local host="$1" port="$2"
  (echo >/dev/tcp/"${host}"/"${port}") >/dev/null 2>&1
}

arfd_http_ok() {
  local url="$1"
  curl -fsS --max-time 2 "${url}" >/dev/null 2>&1
}

arfd_mysql_ok() {
  arfd_tcp_open "${ARFD_MYSQL_HOST:-127.0.0.1}" "${ARFD_MYSQL_PORT:-3306}"
}

arfd_postgres_ok() {
  arfd_tcp_open "${ARFD_POSTGRES_HOST:-127.0.0.1}" "${ARFD_POSTGRES_PORT:-5432}"
}

arfd_redis_ok() {
  arfd_tcp_open "${ARFD_REDIS_HOST:-127.0.0.1}" "${ARFD_REDIS_PORT:-6379}"
}

arfd_airflow_ok() {
  arfd_http_ok "${ARFD_AIRFLOW_URL:-http://127.0.0.1:8080/health}" \
    || arfd_http_ok "http://127.0.0.1:8080/" \
    || arfd_tcp_open 127.0.0.1 8080
}

arfd_rabbitmq_ok() {
  arfd_tcp_open "${ARFD_RABBITMQ_HOST:-127.0.0.1}" "${ARFD_RABBITMQ_PORT:-5672}"
}

arfd_minio_ok() {
  arfd_http_ok "${ARFD_MINIO_URL:-http://127.0.0.1:9000}/minio/health/live" \
    || arfd_tcp_open 127.0.0.1 9000
}

arfd_kafka_ok() {
  arfd_tcp_open 127.0.0.1 9092
}

arfd_mark_started() {
  local name="$1"
  touch "${ARFD_STATE_DIR}/${name}.started"
}

arfd_mark_reused() {
  local name="$1"
  echo reused > "${ARFD_STATE_DIR}/${name}.mode"
}

arfd_mark_managed() {
  local name="$1"
  echo managed-by-arfd > "${ARFD_STATE_DIR}/${name}.mode"
  arfd_mark_started "${name}"
}

arfd_clear_started() {
  local name="$1"
  rm -f "${ARFD_STATE_DIR}/${name}.started" "${ARFD_STATE_DIR}/${name}.mode"
}

arfd_mode_of() {
  local name="$1" f
  f="${ARFD_STATE_DIR}/${name}.mode"
  if [[ -f "${f}" ]]; then
    cat "${f}"
  else
    echo down
  fi
}

arfd_was_started_by_us() {
  [[ -f "${ARFD_STATE_DIR}/$1.started" ]]
}
