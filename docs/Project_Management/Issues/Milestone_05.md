# Milestone M05 - Airlines-RD-Admin

**Scope:** Reference Data Admin portal for operators who manage source reference data.

**Status:** open. Epic #38; 1 features; 4 stories. 0 done; 4 left to build.

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
| 3 | #40 | M05-0003 | Story | App shell and auth stub | Portal foundation |
| 4 | #41 | M05-0004 | Story | Market rules management UI | Core admin job |
| 5 | #42 | M05-0005 | Story | Pipeline health summary view | Ops visibility |
| 6 | #43 | M05-0006 | Story | Wire Admin portal to Middleware/API-Services | End-to-end admin path |

## 2. The same issues grouped by epic and feature

```
Epic #38  M05-0001  Airlines-RD-Admin
|
+-- Feature #39  M05-0002  Admin portal application
\     +-- #40  App shell and auth stub
\     +-- #41  Market rules management UI
\     +-- #42  Pipeline health summary view
\     +-- #43  Wire Admin portal to Middleware/API-Services
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #40 | 1 | `/arfd-story-start 40` | In progress | - | - |
| #40 | 2 | `/brainstorming Story #40: scaffold Airlines-RD-Admin app shell and auth stub` | Planned | - | - |
| #40 | 3 | `/using-git-worktrees Story #40: branch m05-0003-admin-app-shell` | Planned | - | - |
| #40 | 4 | `/writing-plans Story #40` | Planned | - | - |
| #40 | 5 | `/test-driven-development Story #40` | Planned | - | - |
| #40 | 6 | `/subagent-driven-development Story #40` | Planned | - | - |
| #40 | 7 | `/arfd-commit-push 40` after every task (repeat) | Planned | - | - |
| #40 | 8 | `/verification-before-completion Story #40` | Planned | - | - |
| #40 | 9 | `/requesting-code-review Story #40` | Planned | - | - |
| #40 | 10 | `/arfd-commit-push 40` | Planned | - | - |
| #40 | 11 | `/finishing-a-development-branch Story #40` | Planned | - | - |
| #40 | 12 | `/arfd-story-complete 40` | Planned | - | - |
| #41 | 1 | `/arfd-story-start 41` | Planned | - | - |
| #41 | 2 | `/brainstorming Story #41: build market rules management UI for RD Admin` | Planned | - | - |
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
| #42 | 2 | `/brainstorming Story #42: add pipeline health summary view to RD Admin` | Planned | - | - |
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
| #43 | 1 | `/arfd-story-start 43` | Planned | - | - |
| #43 | 2 | `/brainstorming Story #43: wire Airlines-RD-Admin to Middleware/API-Services` | Planned | - | - |
| #43 | 3 | `/using-git-worktrees Story #43: branch m05-0006-admin-api-wire` | Planned | - | - |
| #43 | 4 | `/writing-plans Story #43` | Planned | - | - |
| #43 | 5 | `/test-driven-development Story #43` | Planned | - | - |
| #43 | 6 | `/subagent-driven-development Story #43` | Planned | - | - |
| #43 | 7 | `/arfd-commit-push 43` after every task (repeat) | Planned | - | - |
| #43 | 8 | `/verification-before-completion Story #43` | Planned | - | - |
| #43 | 9 | `/requesting-code-review Story #43` | Planned | - | - |
| #43 | 10 | `/arfd-commit-push 43` | Planned | - | - |
| #43 | 11 | `/finishing-a-development-branch Story #43` | Planned | - | - |
| #43 | 12 | `/arfd-story-complete 43` | Planned | - | - |
| Feature #39 | 1 | `/arfd-feature-complete 39` | Planned | - | - |
| Epic #38 | 1 | `/arfd-epic-complete 38` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
