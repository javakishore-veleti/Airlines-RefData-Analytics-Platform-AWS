#!/usr/bin/env bash
# Discover Middleware/*/app-*.sh and run lifecycle action.
# Usage: local_middleware.sh start|status|down
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ACTION="${1:-}"
case "$ACTION" in
  start) SCRIPT_NAME=app-startup.sh ;;
  status) SCRIPT_NAME=app-status.sh ;;
  down|stop) SCRIPT_NAME=app-shutdown.sh ;;
  *)
    echo "usage: $0 start|status|down" >&2
    exit 2
    ;;
esac

shopt -s nullglob
found=0
for dir in "$ROOT"/Middleware/*/; do
  name="$(basename "$dir")"
  startup="$dir/app-startup.sh"
  target="$dir/$SCRIPT_NAME"
  if [[ ! -f "$startup" ]]; then
    echo "skip $name (no app-startup.sh)"
    continue
  fi
  if [[ ! -x "$target" && ! -f "$target" ]]; then
    echo "missing $SCRIPT_NAME in $name" >&2
    exit 1
  fi
  echo "==> $name: $SCRIPT_NAME"
  bash "$target"
  found=$((found + 1))
done

if [[ "$found" -eq 0 ]]; then
  echo "no Middleware services with app-startup.sh found" >&2
  exit 1
fi
echo "middleware $ACTION complete ($found service(s))"
