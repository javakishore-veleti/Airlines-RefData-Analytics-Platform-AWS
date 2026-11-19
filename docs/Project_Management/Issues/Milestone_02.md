# Milestone M02 - Runtime bootstrap

**Scope:** Lifecycle scripts and containerized platform services (database, streaming, messaging, orchestration, object storage) for development and CI environments.

**Status:** open. Epic #10; 2 features; 8 stories. 0 done; 8 left to build.

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
| #12 | 1 | `/arfd-story-start 12` | In progress | - | - |
| #12 | 2 | `/brainstorming Story #12: design docker-all-up.sh to start the ARFD platform services in order` | Planned | - | - |
| #12 | 3 | `/using-git-worktrees Story #12: branch m02-0003-docker-all-up` | Planned | - | - |
| #12 | 4 | `/writing-plans Story #12` | Planned | - | - |
| #12 | 5 | `/test-driven-development Story #12` | Planned | - | - |
| #12 | 6 | `/subagent-driven-development Story #12` | Planned | - | - |
| #12 | 7 | `/arfd-commit-push 12` after every task (repeat) | Planned | - | - |
| #12 | 8 | `/verification-before-completion Story #12` | Planned | - | - |
| #12 | 9 | `/requesting-code-review Story #12` | Planned | - | - |
| #12 | 10 | `/arfd-commit-push 12` | Planned | - | - |
| #12 | 11 | `/finishing-a-development-branch Story #12` | Planned | - | - |
| #12 | 12 | `/arfd-story-complete 12` | Planned | - | - |
| #13 | 1 | `/arfd-story-start 13` | Planned | - | - |
| #13 | 2 | `/brainstorming Story #13: design all-down.sh teardown behavior for ARFD services` | Planned | - | - |
| #13 | 3 | `/using-git-worktrees Story #13: branch m02-0004-all-down` | Planned | - | - |
| #13 | 4 | `/writing-plans Story #13` | Planned | - | - |
| #13 | 5 | `/test-driven-development Story #13` | Planned | - | - |
| #13 | 6 | `/subagent-driven-development Story #13` | Planned | - | - |
| #13 | 7 | `/arfd-commit-push 13` after every task (repeat) | Planned | - | - |
| #13 | 8 | `/verification-before-completion Story #13` | Planned | - | - |
| #13 | 9 | `/requesting-code-review Story #13` | Planned | - | - |
| #13 | 10 | `/arfd-commit-push 13` | Planned | - | - |
| #13 | 11 | `/finishing-a-development-branch Story #13` | Planned | - | - |
| #13 | 12 | `/arfd-story-complete 13` | Planned | - | - |
| #14 | 1 | `/arfd-story-start 14` | Planned | - | - |
| #14 | 2 | `/brainstorming Story #14: design all-status.sh health probes for ARFD services` | Planned | - | - |
| #14 | 3 | `/using-git-worktrees Story #14: branch m02-0005-all-status` | Planned | - | - |
| #14 | 4 | `/writing-plans Story #14` | Planned | - | - |
| #14 | 5 | `/test-driven-development Story #14` | Planned | - | - |
| #14 | 6 | `/subagent-driven-development Story #14` | Planned | - | - |
| #14 | 7 | `/arfd-commit-push 14` after every task (repeat) | Planned | - | - |
| #14 | 8 | `/verification-before-completion Story #14` | Planned | - | - |
| #14 | 9 | `/requesting-code-review Story #14` | Planned | - | - |
| #14 | 10 | `/arfd-commit-push 14` | Planned | - | - |
| #14 | 11 | `/finishing-a-development-branch Story #14` | Planned | - | - |
| #14 | 12 | `/arfd-story-complete 14` | Planned | - | - |
| #16 | 1 | `/arfd-story-start 16` | Planned | - | - |
| #16 | 2 | `/brainstorming Story #16: define operational database service and CDC prerequisites for ARFD` | Planned | - | - |
| #16 | 3 | `/using-git-worktrees Story #16: branch m02-0007-operational-database` | Planned | - | - |
| #16 | 4 | `/writing-plans Story #16` | Planned | - | - |
| #16 | 5 | `/test-driven-development Story #16` | Planned | - | - |
| #16 | 6 | `/subagent-driven-development Story #16` | Planned | - | - |
| #16 | 7 | `/arfd-commit-push 16` after every task (repeat) | Planned | - | - |
| #16 | 8 | `/verification-before-completion Story #16` | Planned | - | - |
| #16 | 9 | `/requesting-code-review Story #16` | Planned | - | - |
| #16 | 10 | `/arfd-commit-push 16` | Planned | - | - |
| #16 | 11 | `/finishing-a-development-branch Story #16` | Planned | - | - |
| #16 | 12 | `/arfd-story-complete 16` | Planned | - | - |
| #17 | 1 | `/arfd-story-start 17` | Planned | - | - |
| #17 | 2 | `/brainstorming Story #17: define streaming and CDC connector compose for ARFD` | Planned | - | - |
| #17 | 3 | `/using-git-worktrees Story #17: branch m02-0008-streaming-cdc-compose` | Planned | - | - |
| #17 | 4 | `/writing-plans Story #17` | Planned | - | - |
| #17 | 5 | `/test-driven-development Story #17` | Planned | - | - |
| #17 | 6 | `/subagent-driven-development Story #17` | Planned | - | - |
| #17 | 7 | `/arfd-commit-push 17` after every task (repeat) | Planned | - | - |
| #17 | 8 | `/verification-before-completion Story #17` | Planned | - | - |
| #17 | 9 | `/requesting-code-review Story #17` | Planned | - | - |
| #17 | 10 | `/arfd-commit-push 17` | Planned | - | - |
| #17 | 11 | `/finishing-a-development-branch Story #17` | Planned | - | - |
| #17 | 12 | `/arfd-story-complete 17` | Planned | - | - |
| #18 | 1 | `/arfd-story-start 18` | Planned | - | - |
| #18 | 2 | `/brainstorming Story #18: define messaging broker service for ARFD APIs and portals` | Planned | - | - |
| #18 | 3 | `/using-git-worktrees Story #18: branch m02-0009-messaging-broker` | Planned | - | - |
| #18 | 4 | `/writing-plans Story #18` | Planned | - | - |
| #18 | 5 | `/test-driven-development Story #18` | Planned | - | - |
| #18 | 6 | `/subagent-driven-development Story #18` | Planned | - | - |
| #18 | 7 | `/arfd-commit-push 18` after every task (repeat) | Planned | - | - |
| #18 | 8 | `/verification-before-completion Story #18` | Planned | - | - |
| #18 | 9 | `/requesting-code-review Story #18` | Planned | - | - |
| #18 | 10 | `/arfd-commit-push 18` | Planned | - | - |
| #18 | 11 | `/finishing-a-development-branch Story #18` | Planned | - | - |
| #18 | 12 | `/arfd-story-complete 18` | Planned | - | - |
| #19 | 1 | `/arfd-story-start 19` | Planned | - | - |
| #19 | 2 | `/brainstorming Story #19: define orchestration runtime and DAG mount path for ARFD` | Planned | - | - |
| #19 | 3 | `/using-git-worktrees Story #19: branch m02-0010-orchestration-dags-mount` | Planned | - | - |
| #19 | 4 | `/writing-plans Story #19` | Planned | - | - |
| #19 | 5 | `/test-driven-development Story #19` | Planned | - | - |
| #19 | 6 | `/subagent-driven-development Story #19` | Planned | - | - |
| #19 | 7 | `/arfd-commit-push 19` after every task (repeat) | Planned | - | - |
| #19 | 8 | `/verification-before-completion Story #19` | Planned | - | - |
| #19 | 9 | `/requesting-code-review Story #19` | Planned | - | - |
| #19 | 10 | `/arfd-commit-push 19` | Planned | - | - |
| #19 | 11 | `/finishing-a-development-branch Story #19` | Planned | - | - |
| #19 | 12 | `/arfd-story-complete 19` | Planned | - | - |
| #20 | 1 | `/arfd-story-start 20` | Planned | - | - |
| #20 | 2 | `/brainstorming Story #20: define S3-compatible object storage for the ARFD lake` | Planned | - | - |
| #20 | 3 | `/using-git-worktrees Story #20: branch m02-0011-object-storage` | Planned | - | - |
| #20 | 4 | `/writing-plans Story #20` | Planned | - | - |
| #20 | 5 | `/test-driven-development Story #20` | Planned | - | - |
| #20 | 6 | `/subagent-driven-development Story #20` | Planned | - | - |
| #20 | 7 | `/arfd-commit-push 20` after every task (repeat) | Planned | - | - |
| #20 | 8 | `/verification-before-completion Story #20` | Planned | - | - |
| #20 | 9 | `/requesting-code-review Story #20` | Planned | - | - |
| #20 | 10 | `/arfd-commit-push 20` | Planned | - | - |
| #20 | 11 | `/finishing-a-development-branch Story #20` | Planned | - | - |
| #20 | 12 | `/arfd-story-complete 20` | Planned | - | - |
| Feature #11 | 1 | `/arfd-feature-complete 11` | Planned | - | - |
| Feature #15 | 1 | `/arfd-feature-complete 15` | Planned | - | - |
| Epic #10 | 1 | `/arfd-epic-complete 10` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
