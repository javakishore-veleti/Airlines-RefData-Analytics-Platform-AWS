#!/usr/bin/env bash
# Report MasterData-API process + /health.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_MASTERDATA_PID_FILE:-$REPO_ROOT/runtime_data/tmp/masterdata-api.pid}"
HOST="${ARFD_API_HOST:-127.0.0.1}"
PORT="${ARFD_API_PORT:-8110}"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "process: running pid=$(cat "$PID_FILE")"
else
  echo "process: stopped"
fi

if curl -sf "http://$HOST:$PORT/health"; then
  echo
  echo "health: ok"
  exit 0
fi
echo "health: unreachable"
exit 1
