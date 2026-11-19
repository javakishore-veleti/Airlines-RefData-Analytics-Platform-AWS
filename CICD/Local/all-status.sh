#!/usr/bin/env bash
# Report health / reuse labels for ARFD local services (D1).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=arfd-common.sh
source "${SCRIPT_DIR}/arfd-common.sh"

EXIT=0

print_row() {
  local name="$1" label="$2"
  printf "%-12s %s\n" "${name}" "${label}"
  if [[ "${label}" == "down" ]]; then
    EXIT=1
  fi
}

echo "ARFD local status (reused | managed-by-arfd | down)"
echo "------------------------------------------------"

# D1 shared services
print_row "airflow" "$(label_shared airflow probe_airflow)"
print_row "postgres" "$(label_shared postgres probe_postgres)"
print_row "mysql" "$(label_shared mysql probe_mysql)"
print_row "redis" "$(label_shared redis probe_redis)"

# Platform services
print_row "kafka" "$(label_platform kafka probe_kafka)"
print_row "debezium" "$(label_platform debezium probe_debezium)"
print_row "rabbitmq" "$(label_platform rabbitmq probe_rabbitmq)"
print_row "minio" "$(label_platform minio probe_minio)"

exit "${EXIT}"
