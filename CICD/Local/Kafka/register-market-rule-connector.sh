#!/usr/bin/env bash
# Register or update the Debezium MySQL connector for market_db.market_rule (story #23 / D4).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONNECT_URL="${ARFD_DEBEZIUM_URL:-http://127.0.0.1:8083}"
CFG_TEMPLATE="${SCRIPT_DIR}/connectors/market-rule-mysql.json"
NAME="arfd-market-rule-mysql"

# Load env defaults
for f in "${LOCAL_DIR}/.env.example" "${LOCAL_DIR}/.env"; do
  if [[ -f "${f}" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${f}"
    set +a
  fi
done

: "${ARFD_MYSQL_HOST:=host.docker.internal}"
: "${ARFD_MYSQL_PORT:=3306}"
: "${ARFD_MYSQL_USER:=arfd}"
: "${ARFD_MYSQL_PASSWORD:=arfd}"

# From Connect container, host MySQL is reached via host.docker.internal
DB_HOST="host.docker.internal"
DB_PORT="${ARFD_MYSQL_PORT}"

if [[ ! -f "${CFG_TEMPLATE}" ]]; then
  echo "missing connector config: ${CFG_TEMPLATE}" >&2
  exit 1
fi

if ! curl -sf --max-time 3 "${CONNECT_URL}/" >/dev/null; then
  echo "Connect not reachable at ${CONNECT_URL}. Start Kafka stack first (CICD/Local/docker-all-up.sh)." >&2
  exit 1
fi

BODY=$(python3 - <<PY
import json
from pathlib import Path
data = json.loads(Path("${CFG_TEMPLATE}").read_text())
cfg = data["config"]
cfg["database.hostname"] = "${DB_HOST}"
cfg["database.port"] = str(${DB_PORT})
cfg["database.user"] = "${ARFD_MYSQL_USER}"
cfg["database.password"] = "${ARFD_MYSQL_PASSWORD}"
print(json.dumps(data))
PY
)

if curl -sf "${CONNECT_URL}/connectors/${NAME}" >/dev/null 2>&1; then
  echo "Updating connector ${NAME}..."
  CONFIG_ONLY=$(python3 -c 'import json,sys; print(json.dumps(json.loads(sys.argv[1])["config"]))' "${BODY}")
  curl -sf -X PUT -H "Content-Type: application/json" \
    --data "${CONFIG_ONLY}" \
    "${CONNECT_URL}/connectors/${NAME}/config" >/dev/null
else
  echo "Creating connector ${NAME}..."
  curl -sf -X POST -H "Content-Type: application/json" \
    --data "${BODY}" \
    "${CONNECT_URL}/connectors" >/dev/null
fi

echo "Status:"
curl -sf "${CONNECT_URL}/connectors/${NAME}/status" | python3 -m json.tool
echo "Done. Topic prefix: arfd → expect arfd.market_db.market_rule"
