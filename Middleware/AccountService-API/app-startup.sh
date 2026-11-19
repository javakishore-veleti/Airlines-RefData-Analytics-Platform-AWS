#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_ACCOUNT_PID_FILE:-$REPO_ROOT/runtime_data/tmp/accountservice-api.pid}"
LOG_FILE="${ARFD_ACCOUNT_LOG_FILE:-$REPO_ROOT/runtime_data/tmp/accountservice-api.log}"
HOST="${ARFD_ACCOUNT_API_HOST:-127.0.0.1}"
PORT="${ARFD_ACCOUNT_API_PORT:-8111}"
mkdir -p "$(dirname "$PID_FILE")"
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "AccountService-API already running pid=$(cat "$PID_FILE")"; exit 0
fi
cd "$ROOT"
[[ -f "$REPO_ROOT/CICD/Local/.env" ]] && set -a && source "$REPO_ROOT/CICD/Local/.env" && set +a
nohup python3 -m uvicorn app.main:app --host "$HOST" --port "$PORT" >>"$LOG_FILE" 2>&1 &
echo $! >"$PID_FILE"
echo "AccountService-API started pid=$(cat "$PID_FILE") http://$HOST:$PORT"
