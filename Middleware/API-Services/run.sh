#!/usr/bin/env bash
# Start ARFD Middleware API-Services (health + Admin CDC generator).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT}/Middleware/API-Services"
export ARFD_MYSQL_HOST="${ARFD_MYSQL_HOST:-127.0.0.1}"
export ARFD_MYSQL_PORT="${ARFD_MYSQL_PORT:-3306}"
export ARFD_MYSQL_USER="${ARFD_MYSQL_USER:-arfd}"
export ARFD_MYSQL_PASSWORD="${ARFD_MYSQL_PASSWORD:-arfd}"
export ARFD_MYSQL_DATABASE="${ARFD_MYSQL_DATABASE:-market_db}"
HOST="${ARFD_API_HOST:-127.0.0.1}"
PORT="${ARFD_API_PORT:-8110}"
exec python3 -m uvicorn app.main:app --host "${HOST}" --port "${PORT}"
