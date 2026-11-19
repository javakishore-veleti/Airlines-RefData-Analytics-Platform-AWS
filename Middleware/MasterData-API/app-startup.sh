#!/usr/bin/env bash
# Start MasterData-API (uvicorn) in background.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_MASTERDATA_PID_FILE:-$REPO_ROOT/runtime_data/tmp/masterdata-api.pid}"
LOG_FILE="${ARFD_MASTERDATA_LOG_FILE:-$REPO_ROOT/runtime_data/tmp/masterdata-api.log}"
HOST="${ARFD_API_HOST:-127.0.0.1}"
PORT="${ARFD_API_PORT:-8110}"

mkdir -p "$(dirname "$PID_FILE")"
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "MasterData-API already running pid=$(cat "$PID_FILE")"
  exit 0
fi

cd "$ROOT"
# shellcheck disable=SC1091
[[ -f "$REPO_ROOT/CICD/Local/.env" ]] && set -a && source "$REPO_ROOT/CICD/Local/.env" && set +a

nohup python3 -m uvicorn app.main:app --host "$HOST" --port "$PORT" >>"$LOG_FILE" 2>&1 &
echo $! >"$PID_FILE"
echo "MasterData-API started pid=$(cat "$PID_FILE") http://$HOST:$PORT"
