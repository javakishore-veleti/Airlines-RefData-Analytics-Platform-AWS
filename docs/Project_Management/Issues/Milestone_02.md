# Milestone M02 - Runtime bootstrap

**Scope:** Lifecycle scripts and containerized platform services (database, streaming, messaging, orchestration, object storage) for development and CI environments.

**Status: complete.** Runtime bootstrap delivered (D1 reuse, compose, 1M seed tooling, CDC generator).

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

| # | Issue | Key | Done | Title | Why here |
|---|---|---|---|---|---|
| 1 | #10 | M02-0001 | Epic | Runtime bootstrap | Parent of the features below |
| 2 | #11 | M02-0002 | Feature | Lifecycle control scripts | Parent of the stories below |
| 3 | #12 | M02-0003 | Story | docker-all-up.sh | Bring the stack up |
| 4 | #13 | M02-0004 | Story | all-down.sh | Tear the stack down |
| 5 | #14 | M02-0005 | Story | all-status.sh | Operator visibility |
| 6 | #15 | M02-0006 | Feature | Platform compose services | Parent of the stories below |
| 7 | #16 | M02-0007 | Story | Operational database with CDC-ready configuration | Source of reference data |
| 8 | #17 | M02-0008 | Story | Streaming and CDC connector compose | CDC path |
| 9 | #18 | M02-0009 | Story | Messaging broker for APIs and portals | Async messaging |
| 10 | #19 | M02-0010 | Story | Orchestration runtime with Middleware/DAGs mount | Batch apply home |
| 11 | #20 | M02-0011 | Story | S3-compatible object storage for the lake | Lake storage |

## 2. The same issues grouped by epic and feature

```
Epic #10  M02-0001  Runtime bootstrap
|
+-- Feature #11  M02-0002  Lifecycle control scripts
|     +-- #12  docker-all-up.sh
|     +-- #13  all-down.sh
|     +-- #14  all-status.sh
+-- Feature #15  M02-0006  Platform compose services
\     +-- #16  Operational database with CDC-ready configuration
\     +-- #17  Streaming and CDC connector compose
\     +-- #18  Messaging broker for APIs and portals
\     +-- #19  Orchestration runtime with Middleware/DAGs mount
\     +-- #20  S3-compatible object storage for the lake
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #12 | 1 | `/arfd-story-start 12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 2 | `/brainstorming Story #12: design docker-all-up.sh to start the ARFD platform services in order` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 3 | `/using-git-worktrees Story #12: branch m02-0003-docker-all-up` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 4 | `/writing-plans Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 5 | `/test-driven-development Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 6 | `/subagent-driven-development Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 7 | `/arfd-commit-push 12` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 8 | `/verification-before-completion Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 9 | `/requesting-code-review Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 10 | `/arfd-commit-push 12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 11 | `/finishing-a-development-branch Story #12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #12 | 12 | `/arfd-story-complete 12` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 1 | `/arfd-story-start 13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 2 | `/brainstorming Story #13: design all-down.sh teardown behavior for ARFD services` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 3 | `/using-git-worktrees Story #13: branch m02-0004-all-down` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 4 | `/writing-plans Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 5 | `/test-driven-development Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 6 | `/subagent-driven-development Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 7 | `/arfd-commit-push 13` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 8 | `/verification-before-completion Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 9 | `/requesting-code-review Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 10 | `/arfd-commit-push 13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 11 | `/finishing-a-development-branch Story #13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #13 | 12 | `/arfd-story-complete 13` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 1 | `/arfd-story-start 14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 2 | `/brainstorming Story #14: design all-status.sh health probes for ARFD services` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 3 | `/using-git-worktrees Story #14: branch m02-0005-all-status` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 4 | `/writing-plans Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 5 | `/test-driven-development Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 6 | `/subagent-driven-development Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 7 | `/arfd-commit-push 14` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 8 | `/verification-before-completion Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 9 | `/requesting-code-review Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 10 | `/arfd-commit-push 14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 11 | `/finishing-a-development-branch Story #14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #14 | 12 | `/arfd-story-complete 14` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 1 | `/arfd-story-start 16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 2 | `/brainstorming Story #16: define operational database service and CDC prerequisites for ARFD` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 3 | `/using-git-worktrees Story #16: branch m02-0007-operational-database` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 4 | `/writing-plans Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 5 | `/test-driven-development Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 6 | `/subagent-driven-development Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 7 | `/arfd-commit-push 16` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 8 | `/verification-before-completion Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 9 | `/requesting-code-review Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 10 | `/arfd-commit-push 16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 11 | `/finishing-a-development-branch Story #16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #16 | 12 | `/arfd-story-complete 16` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 1 | `/arfd-story-start 17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 2 | `/brainstorming Story #17: define streaming and CDC connector compose for ARFD` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 3 | `/using-git-worktrees Story #17: branch m02-0008-streaming-cdc-compose` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 4 | `/writing-plans Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 5 | `/test-driven-development Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 6 | `/subagent-driven-development Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 7 | `/arfd-commit-push 17` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 8 | `/verification-before-completion Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 9 | `/requesting-code-review Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 10 | `/arfd-commit-push 17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 11 | `/finishing-a-development-branch Story #17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #17 | 12 | `/arfd-story-complete 17` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 1 | `/arfd-story-start 18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 2 | `/brainstorming Story #18: define messaging broker service for ARFD APIs and portals` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 3 | `/using-git-worktrees Story #18: branch m02-0009-messaging-broker` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 4 | `/writing-plans Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 5 | `/test-driven-development Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 6 | `/subagent-driven-development Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 7 | `/arfd-commit-push 18` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 8 | `/verification-before-completion Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 9 | `/requesting-code-review Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 10 | `/arfd-commit-push 18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 11 | `/finishing-a-development-branch Story #18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #18 | 12 | `/arfd-story-complete 18` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 1 | `/arfd-story-start 19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 2 | `/brainstorming Story #19: define orchestration runtime and DAG mount path for ARFD` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 3 | `/using-git-worktrees Story #19: branch m02-0010-orchestration-dags-mount` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 4 | `/writing-plans Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 5 | `/test-driven-development Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 6 | `/subagent-driven-development Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 7 | `/arfd-commit-push 19` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 8 | `/verification-before-completion Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 9 | `/requesting-code-review Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 10 | `/arfd-commit-push 19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 11 | `/finishing-a-development-branch Story #19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #19 | 12 | `/arfd-story-complete 19` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 1 | `/arfd-story-start 20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 2 | `/brainstorming Story #20: define S3-compatible object storage for the ARFD lake` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 3 | `/using-git-worktrees Story #20: branch m02-0011-object-storage` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 4 | `/writing-plans Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 5 | `/test-driven-development Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 6 | `/subagent-driven-development Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 7 | `/arfd-commit-push 20` after every task (repeat) | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 8 | `/verification-before-completion Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 9 | `/requesting-code-review Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 10 | `/arfd-commit-push 20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 11 | `/finishing-a-development-branch Story #20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| #20 | 12 | `/arfd-story-complete 20` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| Feature #11 | 1 | `/arfd-feature-complete 11` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| Feature #15 | 1 | `/arfd-feature-complete 15` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |
| Epic #10 | 1 | `/arfd-epic-complete 10` | Done | 2026-11-19 16:33 | 2026-11-19 16:33 |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- **D1 — Shared service reuse:** On this machine, if Apache Airflow, PostgreSQL, MySQL, or Redis is already healthy, lifecycle scripts **reuse** it (do not start a second copy). `all-down` stops only ARFD-started services unless `--including-shared`. See `docs/Design/DESIGN.md` (D1). Stories #12–#14, #16, #19 carry the acceptance criteria.

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
