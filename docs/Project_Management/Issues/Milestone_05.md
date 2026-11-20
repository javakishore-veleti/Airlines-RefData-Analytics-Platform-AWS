# Milestone M05 - Airlines-RD-Admin (UI)

**Scope:** Angular Admin portal with professional D5 UI (PrimeNG Aura/Lara light, Lucide, navy/ice/sky), AccountService auth, User Management, market rules, and wiring to MasterData-API + AccountService-API.

**Status:** closed — completed 2026-11-19. Epic #38; 1 feature; 6 stories. 6 done; 0 left to build.

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
| 1 | #38 | M05-0001 | Epic | Airlines-RD-Admin | Parent of the features below |
| 2 | #39 | M05-0002 | Feature | Admin portal application | Parent of the stories below |
| 3 | #62 | M05-0008 | Story | Record D5 portal UI system (PrimeNG Aura, palette, icons) | Lock UI before Angular shell |
| 4 | #40 | M05-0003 | Story | Angular Admin shell (PrimeNG Aura, nav, signup/signin) | Portal chrome + auth UI |
| 5 | #61 | M05-0007 | Story | User Management UI via AccountService-API | Admin user ops |
| 6 | #41 | M05-0004 | Story | Market rules management UI | Core admin job |
| 7 | #42 | M05-0005 | Story | Pipeline health summary view | Ops visibility |
| 8 | #43 | M05-0006 | Story | Wire Admin portal to MasterData-API and AccountService-API | End-to-end admin path |

## 2. The same issues grouped by epic and feature

```
Epic #38  M05-0001  Airlines-RD-Admin
|
+-- Feature #39  M05-0002  Admin portal application
\     +-- #62  Record D5 portal UI system (PrimeNG Aura, palette, icons)
\     +-- #40  Angular Admin shell (PrimeNG Aura, nav, signup/signin)
\     +-- #61  User Management UI via AccountService-API
\     +-- #41  Market rules management UI
\     +-- #42  Pipeline health summary view
\     +-- #43  Wire Admin portal to MasterData-API and AccountService-API
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; Superpowers natives own design/plan/TDD/implementation.

**No vibe coding.** Product/UI code only after `/arfd-story-start N` and only via the steps below in a story worktree. Depends on M04 AccountService stories (#58–#60) for live auth/user APIs (shell may mock until then if story acceptance allows).

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #62 | 1 | `/arfd-story-start 62` | Done | 2026-11-19 18:41 | 2026-11-19 18:41 |
| #62 | 2 | `/brainstorming Story #62: finalize D5 portal UI system (PrimeNG Aura/Lara, Lucide, navy/ice/sky, no black/gray academic chrome)` | Done | 2026-11-19 18:41 | 2026-11-19 19:40 |
| #62 | 3 | `/writing-plans Story #62` | Done | 2026-11-19 19:40 | 2026-11-19 19:40 |
| #62 | 4 | `/verification-before-completion Story #62` | Done | 2026-11-19 19:40 | 2026-11-19 19:40 |
| #62 | 5 | `/arfd-commit-push 62` | Done | 2026-11-19 19:40 | 2026-11-19 19:40 |
| #62 | 6 | `/arfd-story-complete 62` | Done | 2026-11-19 19:40 | 2026-11-19 19:40 |
| #40 | 1 | `/arfd-story-start 40` | Planned | - | - |
| #40 | 2 | `/brainstorming Story #40: Angular Admin shell with top bar, left nav, signup/signin, favicon per D5` | Planned | - | - |
| #40 | 3 | `/using-git-worktrees Story #40: branch m05-0003-admin-angular-shell` | Planned | - | - |
| #40 | 4 | `/writing-plans Story #40` | Planned | - | - |
| #40 | 5 | `/test-driven-development Story #40` | Planned | - | - |
| #40 | 6 | `/subagent-driven-development Story #40` | Planned | - | - |
| #40 | 7 | `/arfd-commit-push 40` after every task (repeat) | Planned | - | - |
| #40 | 8 | `/verification-before-completion Story #40` | Planned | - | - |
| #40 | 9 | `/requesting-code-review Story #40` | Planned | - | - |
| #40 | 10 | `/arfd-commit-push 40` | Planned | - | - |
| #40 | 11 | `/finishing-a-development-branch Story #40` | Planned | - | - |
| #40 | 12 | `/arfd-story-complete 40` | Planned | - | - |
| #61 | 1 | `/arfd-story-start 61` | Planned | - | - |
| #61 | 2 | `/brainstorming Story #61: User Management UI calling AccountService-API` | Planned | - | - |
| #61 | 3 | `/using-git-worktrees Story #61: branch m05-0007-user-management-ui` | Planned | - | - |
| #61 | 4 | `/writing-plans Story #61` | Planned | - | - |
| #61 | 5 | `/test-driven-development Story #61` | Planned | - | - |
| #61 | 6 | `/subagent-driven-development Story #61` | Planned | - | - |
| #61 | 7 | `/arfd-commit-push 61` after every task (repeat) | Planned | - | - |
| #61 | 8 | `/verification-before-completion Story #61` | Planned | - | - |
| #61 | 9 | `/requesting-code-review Story #61` | Planned | - | - |
| #61 | 10 | `/arfd-commit-push 61` | Planned | - | - |
| #61 | 11 | `/finishing-a-development-branch Story #61` | Planned | - | - |
| #61 | 12 | `/arfd-story-complete 61` | Planned | - | - |
| #41 | 1 | `/arfd-story-start 41` | Planned | - | - |
| #41 | 2 | `/brainstorming Story #41: market rules management UI for RD Admin` | Planned | - | - |
| #41 | 3 | `/using-git-worktrees Story #41: branch m05-0004-market-rules-ui` | Planned | - | - |
| #41 | 4 | `/writing-plans Story #41` | Planned | - | - |
| #41 | 5 | `/test-driven-development Story #41` | Planned | - | - |
| #41 | 6 | `/subagent-driven-development Story #41` | Planned | - | - |
| #41 | 7 | `/arfd-commit-push 41` after every task (repeat) | Planned | - | - |
| #41 | 8 | `/verification-before-completion Story #41` | Planned | - | - |
| #41 | 9 | `/requesting-code-review Story #41` | Planned | - | - |
| #41 | 10 | `/arfd-commit-push 41` | Planned | - | - |
| #41 | 11 | `/finishing-a-development-branch Story #41` | Planned | - | - |
| #41 | 12 | `/arfd-story-complete 41` | Planned | - | - |
| #42 | 1 | `/arfd-story-start 42` | Planned | - | - |
| #42 | 2 | `/brainstorming Story #42: pipeline health summary view` | Planned | - | - |
| #42 | 3 | `/using-git-worktrees Story #42: branch m05-0005-pipeline-health-view` | Planned | - | - |
| #42 | 4 | `/writing-plans Story #42` | Planned | - | - |
| #42 | 5 | `/test-driven-development Story #42` | Planned | - | - |
| #42 | 6 | `/subagent-driven-development Story #42` | Planned | - | - |
| #42 | 7 | `/arfd-commit-push 42` after every task (repeat) | Planned | - | - |
| #42 | 8 | `/verification-before-completion Story #42` | Planned | - | - |
| #42 | 9 | `/requesting-code-review Story #42` | Planned | - | - |
| #42 | 10 | `/arfd-commit-push 42` | Planned | - | - |
| #42 | 11 | `/finishing-a-development-branch Story #42` | Planned | - | - |
| #42 | 12 | `/arfd-story-complete 42` | Planned | - | - |
| #43 | 1 | `/arfd-story-start 43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 2 | `/brainstorming Story #43: wire Admin to MasterData-API and AccountService-API` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 3 | `/using-git-worktrees Story #43: branch m05-0006-admin-api-wire` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 4 | `/writing-plans Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 5 | `/test-driven-development Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 6 | `/subagent-driven-development Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 7 | `/arfd-commit-push 43` after every task (repeat) | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 8 | `/verification-before-completion Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 9 | `/requesting-code-review Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 10 | `/arfd-commit-push 43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 11 | `/finishing-a-development-branch Story #43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| #43 | 12 | `/arfd-story-complete 43` | Done | 2026-11-19 19:54 | 2026-11-19 19:54 |
| Feature #39 | 1 | `/arfd-feature-complete 39` | Planned | - | - |
| Epic #38 | 1 | `/arfd-epic-complete 38` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- **Prerequisite:** M03 complete (or explicit parallel); M04 AccountService (#58–#60) for real auth/user APIs.
- **Hard gate:** open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product/UI code.
- **No vibe coding:** Section 3 Superpowers natives only; `/arfd-*` for board/git/milestone logging.
- **D5 UI:** PrimeNG Aura/Lara light, Lucide, Plus Jakarta Sans, navy/ice/sky tokens — see `docs/Design/DESIGN.md` D5 and `docs/Superpowers/specs/2026-11-19-d5-portal-ui-system.md`.
- **Never:** pure black text, sterile gray chrome, academic Bootstrap-default admin look, purple AI gradients.
