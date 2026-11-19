#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_ACCOUNT_PID_FILE:-$REPO_ROOT/runtime_data/tmp/accountservice-api.pid}"
HOST="${ARFD_ACCOUNT_API_HOST:-127.0.0.1}"
PORT="${ARFD_ACCOUNT_API_PORT:-8111}"
if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "process: running pid=$(cat "$PID_FILE")"
else echo "process: stopped"; fi
curl -sf "http://$HOST:$PORT/health" && echo && echo "health: ok" && exit 0
echo "health: unreachable"; exit 1
