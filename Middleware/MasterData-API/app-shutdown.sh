#!/usr/bin/env bash
# Stop MasterData-API background process.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_MASTERDATA_PID_FILE:-$REPO_ROOT/runtime_data/tmp/masterdata-api.pid}"

if [[ ! -f "$PID_FILE" ]]; then
  echo "MasterData-API not running (no pid file)"
  exit 0
fi
PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID" || true
  sleep 0.5
  kill -9 "$PID" 2>/dev/null || true
  echo "MasterData-API stopped pid=$PID"
else
  echo "MasterData-API pid file stale"
fi
rm -f "$PID_FILE"
