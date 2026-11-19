# Plan — M04-0003 (#31) MasterData-API skeleton

## Files

| Path | Role |
|---|---|
| `Middleware/MasterData-API/` | Renamed project root |
| `app/common/dtos/usecase.py` | HealthCtx/Req/Resp |
| `app/dao/`, `app/facade/`, `app/wf/WFHealth/` | Layered Health |
| `app/api/health.py`, `main.py` | HTTP + OpenAPI |
| `app-startup.sh` / `app-status.sh` / `app-shutdown.sh` | Lifecycle |
| `tests/test_health_layering.py` | TDD |

## Tasks

1. **Failing test** for HealthCtx through facade→WF→task→dao (fake dao).
2. **Implement** layers + object_factory stubs + config + main.
3. **Rename** API-Services → MasterData-API; update references.
4. **app-*.sh** + README.
5. **Keep** `/admin/cdc/generate` working.
6. Run tests; commit; merge via finishing-branch.
