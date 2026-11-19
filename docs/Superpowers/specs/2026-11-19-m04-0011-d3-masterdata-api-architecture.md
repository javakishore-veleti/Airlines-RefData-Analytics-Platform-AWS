# M04-0011 — D3 MasterData-API modular monolith and layering

**Story:** #56  
**Date:** 2026-11-19  
**Status:** Approved (autonomous — operator requested complete-all without further Q&A; locks prior D3 summary)

## Goal

Persist MasterData-API conventions as design decision **D3** so M04 stories (#31, #55, #32–#34) and AccountService (#58–#60) implement one contract.

## Approaches considered

| Option | Idea | Trade-off |
|---|---|---|
| A | Flat FastAPI routers + services | Fastest; hard to split deploy later |
| B | Domain microservices from day one | Over-split for Phase 1 |
| **C (chosen)** | Modular monolith under `Middleware/MasterData-API/` with strict layers | One process now; package boundaries ready to extract |

## Locked decisions

1. **Project root:** `Middleware/MasterData-API/` (FastAPI). Same layout later for `Middleware/AccountService-API/`.
2. **Call chain:** HTTP `api` → `facade` → `WF` (workflow) → `tasks` → `dao`. No skipping layers for business work. Health may be a thin api→facade→WF path.
3. **Facades:** Each facade package has `interface.py` + `impl.py`. Callers depend on the interface; `object_factory` returns the impl.
4. **WF naming:** Each use case lives in a folder whose name starts with **`WF`** (e.g. `WFHealth/`, `WFGenerateCdcEvents/`). Folder contains `interface.py`, `impl.py` (or equivalent), and `tasks/`.
5. **Tasks:** One focused unit of work per task module; WF orchestrates tasks in order.
6. **DAO:** Persistence only (MySQL for OLTP; lake readers behind their own DAO when needed). No business rules in DAO.
7. **DTOs:** `Ctx` / `Req` / `Resp` (and shared types) under `common/dtos/usecase.py` (and related modules). Do not pass raw ORM models across facade/WF boundaries.
8. **object_factory:** Per-layer `object_factory.py` resolves beans by name/type so tests can swap impls.
9. **Domain-first packages:** Prefer packages named by domain capability (health, market_rule, cdc, lake_query, messaging) under the layer roots — not a single god-module.
10. **Lifecycle scripts:** Each microservice root provides `app-startup.sh`, `app-status.sh`, `app-shutdown.sh`.
11. **Root npm discovery:** Repo-root `package.json` scripts `local:containers:*` and `local:middleware:*` discover and invoke `Middleware/*/app-*.sh` (story #55).
12. **Reference use cases for skeleton (#31) and writes (#32):**
    - **Health** — proves api→facade→WF→task→dao (dao may be a no-op or config ping).
    - **GenerateCdcEvents** — Admin-driven N random market_rule mutations (already exercised via portal; move behind MasterData-API WF).
13. **OpenAPI:** FastAPI auto OpenAPI at `/docs` / `/openapi.json`; tag routes by domain.
14. **Out of scope for D3 docs:** Implementing the skeleton (#31), npm scripts (#55), AccountService code (#58+).

## Suggested tree (informative for #31)

```text
Middleware/MasterData-API/
  app-startup.sh
  app-status.sh
  app-shutdown.sh
  requirements.txt / pyproject.toml
  app/
    main.py
    api/                 # routers
    facade/              # interface.py + impl.py per facade
    wf/                  # WFHealth/, WFGenerateCdcEvents/, …
    tasks/
    dao/
    common/dtos/
    object_factory.py    # and/or per-layer factories
```

Exact package names may tighten in the #31 plan; the layer names and WF prefix are mandatory.

## Acceptance mapping

| Acceptance | Delivery |
|---|---|
| D3 section in DESIGN.md | Expanded D3 with status Decided |
| Spec covers root, WF, facade/WF/task, Ctx/Req/Resp, object_factory, domain-first, app-*.sh + npm, Health + GenerateCdcEvents | This document + DESIGN.md |
| Spec under docs/Superpowers/specs/ | This file |
| Docs only | No Middleware/MasterData-API product tree in this story |

## Risks

- Over-documenting folder names that #31 will refine — keep DESIGN.md normative for layers/WF/DTO/factory; treat tree above as guidance.
- AccountService must clone the same layering (explicit in D3 / #58 brainstorm).
