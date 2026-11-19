# Milestone M04 - Middleware

**Scope:** API services for portals and stable DAG packaging for the orchestration runtime.

**Status:** open. Epic #29; 2 features; 6 stories. 0 done; 6 left to build.

How to read this file:
- `#N` is the GitHub issue number. The `M0N-00NN` key is the sequence tag at the start of the issue title.
- Section 1 is build order. Section 2 groups epic → feature → story.
- Section 3 is the Superpowers + `/arfd-*` command queue. Run one story at a time.

## Contents

- [1. Table of contents (build order)](#1-table-of-contents-build-order)
- [2. The same issues grouped by epic and feature](#2-the-same-issues-grouped-by-epic-and-feature)
- [3. Superpowers workflow](#3-superpowers-workflow)
- [4. Project skills](#4-project-skills-arfd----airlines-reference-data)
- [5. Notes](#5-notes)

## 1. Table of contents (build order)

| # | Issue | Key | Type | Title | Why here |
|---|---|---|---|---|---|
| 1 | #29 | M04-0001 | Epic | Middleware | Parent of the features below |
| 2 | #30 | M04-0002 | Feature | API Services | Parent of the stories below |
| 3 | #31 | M04-0003 | Story | API service skeleton (health, config, OpenAPI) | API foundation |
| 4 | #32 | M04-0004 | Story | Reference-data write APIs for Admin | Admin needs writes |
| 5 | #33 | M04-0005 | Story | Lake read / query façade for Intelligence | Intelligence needs reads |
| 6 | #34 | M04-0006 | Story | Async messaging integration | Decouple portal/API work |
| 7 | #35 | M04-0007 | Feature | DAG packaging | Parent of the stories below |
| 8 | #36 | M04-0008 | Story | Document Middleware/DAGs mount contract | Stable path |
| 9 | #37 | M04-0009 | Story | Shared CDC parse and lake writer libraries | Reuse across jobs |

## 2. The same issues grouped by epic and feature

```
Epic #29  M04-0001  Middleware
|
+-- Feature #30  M04-0002  API Services
|     +-- #31  API service skeleton (health, config, OpenAPI)
|     +-- #32  Reference-data write APIs for Admin
|     +-- #33  Lake read / query façade for Intelligence
|     +-- #34  Async messaging integration
+-- Feature #35  M04-0007  DAG packaging
\     +-- #36  Document Middleware/DAGs mount contract
\     +-- #37  Shared CDC parse and lake writer libraries
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #31 | 1 | `/arfd-story-start 31` | In progress | - | - |
| #31 | 2 | `/brainstorming Story #31: scaffold Middleware/API-Services with health, config, OpenAPI` | Planned | - | - |
| #31 | 3 | `/using-git-worktrees Story #31: branch m04-0003-api-skeleton` | Planned | - | - |
| #31 | 4 | `/writing-plans Story #31` | Planned | - | - |
| #31 | 5 | `/test-driven-development Story #31` | Planned | - | - |
| #31 | 6 | `/subagent-driven-development Story #31` | Planned | - | - |
| #31 | 7 | `/arfd-commit-push 31` after every task (repeat) | Planned | - | - |
| #31 | 8 | `/verification-before-completion Story #31` | Planned | - | - |
| #31 | 9 | `/requesting-code-review Story #31` | Planned | - | - |
| #31 | 10 | `/arfd-commit-push 31` | Planned | - | - |
| #31 | 11 | `/finishing-a-development-branch Story #31` | Planned | - | - |
| #31 | 12 | `/arfd-story-complete 31` | Planned | - | - |
| #32 | 1 | `/arfd-story-start 32` | Planned | - | - |
| #32 | 2 | `/brainstorming Story #32: design RefData write APIs for Airlines-RD-Admin` | Planned | - | - |
| #32 | 3 | `/using-git-worktrees Story #32: branch m04-0004-refdata-write-apis` | Planned | - | - |
| #32 | 4 | `/writing-plans Story #32` | Planned | - | - |
| #32 | 5 | `/test-driven-development Story #32` | Planned | - | - |
| #32 | 6 | `/subagent-driven-development Story #32` | Planned | - | - |
| #32 | 7 | `/arfd-commit-push 32` after every task (repeat) | Planned | - | - |
| #32 | 8 | `/verification-before-completion Story #32` | Planned | - | - |
| #32 | 9 | `/requesting-code-review Story #32` | Planned | - | - |
| #32 | 10 | `/arfd-commit-push 32` | Planned | - | - |
| #32 | 11 | `/finishing-a-development-branch Story #32` | Planned | - | - |
| #32 | 12 | `/arfd-story-complete 32` | Planned | - | - |
| #33 | 1 | `/arfd-story-start 33` | Planned | - | - |
| #33 | 2 | `/brainstorming Story #33: design lake read/query façade APIs for Airlines-RD-Intelligence` | Planned | - | - |
| #33 | 3 | `/using-git-worktrees Story #33: branch m04-0005-lake-read-apis` | Planned | - | - |
| #33 | 4 | `/writing-plans Story #33` | Planned | - | - |
| #33 | 5 | `/test-driven-development Story #33` | Planned | - | - |
| #33 | 6 | `/subagent-driven-development Story #33` | Planned | - | - |
| #33 | 7 | `/arfd-commit-push 33` after every task (repeat) | Planned | - | - |
| #33 | 8 | `/verification-before-completion Story #33` | Planned | - | - |
| #33 | 9 | `/requesting-code-review Story #33` | Planned | - | - |
| #33 | 10 | `/arfd-commit-push 33` | Planned | - | - |
| #33 | 11 | `/finishing-a-development-branch Story #33` | Planned | - | - |
| #33 | 12 | `/arfd-story-complete 33` | Planned | - | - |
| #34 | 1 | `/arfd-story-start 34` | Planned | - | - |
| #34 | 2 | `/brainstorming Story #34: integrate async messaging for ARFD middleware` | Planned | - | - |
| #34 | 3 | `/using-git-worktrees Story #34: branch m04-0006-async-messaging` | Planned | - | - |
| #34 | 4 | `/writing-plans Story #34` | Planned | - | - |
| #34 | 5 | `/test-driven-development Story #34` | Planned | - | - |
| #34 | 6 | `/subagent-driven-development Story #34` | Planned | - | - |
| #34 | 7 | `/arfd-commit-push 34` after every task (repeat) | Planned | - | - |
| #34 | 8 | `/verification-before-completion Story #34` | Planned | - | - |
| #34 | 9 | `/requesting-code-review Story #34` | Planned | - | - |
| #34 | 10 | `/arfd-commit-push 34` | Planned | - | - |
| #34 | 11 | `/finishing-a-development-branch Story #34` | Planned | - | - |
| #34 | 12 | `/arfd-story-complete 34` | Planned | - | - |
| #36 | 1 | `/arfd-story-start 36` | Planned | - | - |
| #36 | 2 | `/brainstorming Story #36: document Middleware/DAGs relative mount contract` | Planned | - | - |
| #36 | 3 | `/verification-before-completion Story #36` | Planned | - | - |
| #36 | 4 | `/arfd-commit-push 36` | Planned | - | - |
| #36 | 5 | `/arfd-story-complete 36` | Planned | - | - |
| #37 | 1 | `/arfd-story-start 37` | Planned | - | - |
| #37 | 2 | `/brainstorming Story #37: extract shared CDC parse and lake writer libraries for ARFD DAGs` | Planned | - | - |
| #37 | 3 | `/using-git-worktrees Story #37: branch m04-0009-shared-cdc-lake-libs` | Planned | - | - |
| #37 | 4 | `/writing-plans Story #37` | Planned | - | - |
| #37 | 5 | `/test-driven-development Story #37` | Planned | - | - |
| #37 | 6 | `/subagent-driven-development Story #37` | Planned | - | - |
| #37 | 7 | `/arfd-commit-push 37` after every task (repeat) | Planned | - | - |
| #37 | 8 | `/verification-before-completion Story #37` | Planned | - | - |
| #37 | 9 | `/requesting-code-review Story #37` | Planned | - | - |
| #37 | 10 | `/arfd-commit-push 37` | Planned | - | - |
| #37 | 11 | `/finishing-a-development-branch Story #37` | Planned | - | - |
| #37 | 12 | `/arfd-story-complete 37` | Planned | - | - |
| Feature #30 | 1 | `/arfd-feature-complete 30` | Planned | - | - |
| Feature #35 | 1 | `/arfd-feature-complete 35` | Planned | - | - |
| Epic #29 | 1 | `/arfd-epic-complete 29` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
