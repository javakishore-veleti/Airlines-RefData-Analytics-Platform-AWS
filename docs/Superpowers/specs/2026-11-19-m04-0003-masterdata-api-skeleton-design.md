# M04-0003 — MasterData-API skeleton

**Story:** #31  
**Date:** 2026-11-19  
**Status:** Approved (autonomous complete-all)  
**Depends on:** D3 (#56)

## Goal

Rename `Middleware/API-Services` → `Middleware/MasterData-API` and deliver Health through `api → facade → WF → task → dao` with Ctx/Req/Resp, config, OpenAPI, and `app-*.sh`.

## Decisions

1. **Rename** in-repo; update Admin portal / docs / env references that point at `API-Services`.
2. **Health** is the reference layered use case (`WFHealth`). MySQL ping lives in dao; degraded status when unreachable.
3. **GenerateCdcEvents** HTTP route remains for M02 compatibility in this story but is **not** fully re-layered yet (#32 owns that). Implementation may live under `api/` calling a shared mysql helper so Admin CDC keep working.
4. **Config:** env-based (`ARFD_MYSQL_*`, `ARFD_API_HOST`, `ARFD_API_PORT`) via `app/config.py`.
5. **Lifecycle:** `app-startup.sh` starts uvicorn in background (pid under `runtime_data/tmp/masterdata-api.pid`), `app-status.sh` curls `/health`, `app-shutdown.sh` kills pid.
6. **Tests:** unittest (or pytest if already present) for Health layering with a fake dao — no live MySQL required for unit path; optional live smoke documented.

## Out of scope

Full GenerateCdcEvents WF (#32), lake reads (#33), RabbitMQ (#34), npm scripts (#55).
