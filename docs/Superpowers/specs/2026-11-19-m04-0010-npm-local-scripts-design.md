# M04-0010 — Root npm local containers and middleware scripts

**Story:** #55  
**Status:** Approved (autonomous)

## Decisions

1. Root `package.json` with npm scripts only (no Node runtime dependency beyond npm itself).
2. `local:containers:all:{start,stop,status}` wrap existing `CICD/Local/docker-all-up.sh`, `all-down.sh`, `all-status.sh`.
3. `local:middleware:all:{start,status,down}` call `scripts/local_middleware.sh` which scans `Middleware/*/app-*.sh` and invokes matching lifecycle scripts. Directories without `app-startup.sh` (e.g. `Middleware/DAGs`) are skipped.
4. Document in root README and `CICD/Local/README.md`.
