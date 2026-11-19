#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
PID_FILE="${ARFD_ACCOUNT_PID_FILE:-$REPO_ROOT/runtime_data/tmp/accountservice-api.pid}"
[[ -f "$PID_FILE" ]] || { echo "AccountService-API not running"; exit 0; }
PID="$(cat "$PID_FILE")"
kill "$PID" 2>/dev/null || true; sleep 0.3; kill -9 "$PID" 2>/dev/null || true
rm -f "$PID_FILE"; echo "AccountService-API stopped"
