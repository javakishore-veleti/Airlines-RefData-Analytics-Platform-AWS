#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
HOST="${ARFD_API_HOST:-127.0.0.1}"
PORT="${ARFD_API_PORT:-8110}"
exec python3 -m uvicorn app.main:app --host "$HOST" --port "$PORT"
