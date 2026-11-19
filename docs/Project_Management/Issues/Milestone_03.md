# Milestone M03 - CDC to analytics lake

**Scope:** Stream operational reference-data changes into the analytics lake with correct insert/update/delete semantics.

**Status:** open. Epic #21; 2 features; 5 stories. 0 done; 5 left to build.

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
| 1 | #21 | M03-0001 | Epic | CDC to analytics lake | Parent of the features below |
| 2 | #22 | M03-0002 | Feature | CDC connector for reference data | Parent of the stories below |
| 3 | #23 | M03-0003 | Story | Configure CDC for market_rule | Source capture |
| 4 | #24 | M03-0004 | Story | Topic naming and key partitioning strategy | Ordering and scale |
| 5 | #25 | M03-0005 | Feature | Batch apply to the lake | Parent of the stories below |
| 6 | #26 | M03-0006 | Story | Batch consumer job under Middleware/DAGs | Apply path |
| 7 | #27 | M03-0007 | Story | Map CDC operations to lake insert/update/delete | Correctness |
| 8 | #28 | M03-0008 | Story | Write and validate lake tables | Prove end to end |

## 2. The same issues grouped by epic and feature

```
Epic #21  M03-0001  CDC to analytics lake
|
+-- Feature #22  M03-0002  CDC connector for reference data
|     +-- #23  Configure CDC for market_rule
|     +-- #24  Topic naming and key partitioning strategy
+-- Feature #25  M03-0005  Batch apply to the lake
\     +-- #26  Batch consumer job under Middleware/DAGs
\     +-- #27  Map CDC operations to lake insert/update/delete
\     +-- #28  Write and validate lake tables
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #23 | 1 | `/arfd-story-start 23` | Done | 2026-11-19 17:22 | 2026-11-19 17:22 |
| #23 | 2 | `/brainstorming Story #23: configure CDC for market_db.market_rule without locking stack choices in the issue prose` | In progress | 2026-11-19 17:22 | - |
| #23 | 3 | `/using-git-worktrees Story #23: branch m03-0003-cdc-market-rule` | Planned | - | - |
| #23 | 4 | `/writing-plans Story #23` | Planned | - | - |
| #23 | 5 | `/test-driven-development Story #23` | Planned | - | - |
| #23 | 6 | `/subagent-driven-development Story #23` | Planned | - | - |
| #23 | 7 | `/arfd-commit-push 23` after every task (repeat) | Planned | - | - |
| #23 | 8 | `/verification-before-completion Story #23` | Planned | - | - |
| #23 | 9 | `/requesting-code-review Story #23` | Planned | - | - |
| #23 | 10 | `/arfd-commit-push 23` | Planned | - | - |
| #23 | 11 | `/finishing-a-development-branch Story #23` | Planned | - | - |
| #23 | 12 | `/arfd-story-complete 23` | Planned | - | - |
| #24 | 1 | `/arfd-story-start 24` | Planned | - | - |
| #24 | 2 | `/brainstorming Story #24: decide topic naming and key partitioning for ARFD CDC` | Planned | - | - |
| #24 | 3 | `/verification-before-completion Story #24` | Planned | - | - |
| #24 | 4 | `/arfd-commit-push 24` | Planned | - | - |
| #24 | 5 | `/arfd-story-complete 24` | Planned | - | - |
| #26 | 1 | `/arfd-story-start 26` | Planned | - | - |
| #26 | 2 | `/brainstorming Story #26: design batch consumer job under Middleware/DAGs for ARFD CDC` | Planned | - | - |
| #26 | 3 | `/using-git-worktrees Story #26: branch m03-0006-batch-consumer-dag` | Planned | - | - |
| #26 | 4 | `/writing-plans Story #26` | Planned | - | - |
| #26 | 5 | `/test-driven-development Story #26` | Planned | - | - |
| #26 | 6 | `/subagent-driven-development Story #26` | Planned | - | - |
| #26 | 7 | `/arfd-commit-push 26` after every task (repeat) | Planned | - | - |
| #26 | 8 | `/verification-before-completion Story #26` | Planned | - | - |
| #26 | 9 | `/requesting-code-review Story #26` | Planned | - | - |
| #26 | 10 | `/arfd-commit-push 26` | Planned | - | - |
| #26 | 11 | `/finishing-a-development-branch Story #26` | Planned | - | - |
| #26 | 12 | `/arfd-story-complete 26` | Planned | - | - |
| #27 | 1 | `/arfd-story-start 27` | Planned | - | - |
| #27 | 2 | `/brainstorming Story #27: map CDC operations to lake row semantics for ARFD` | Planned | - | - |
| #27 | 3 | `/using-git-worktrees Story #27: branch m03-0007-cdc-op-mapping` | Planned | - | - |
| #27 | 4 | `/writing-plans Story #27` | Planned | - | - |
| #27 | 5 | `/test-driven-development Story #27` | Planned | - | - |
| #27 | 6 | `/subagent-driven-development Story #27` | Planned | - | - |
| #27 | 7 | `/arfd-commit-push 27` after every task (repeat) | Planned | - | - |
| #27 | 8 | `/verification-before-completion Story #27` | Planned | - | - |
| #27 | 9 | `/requesting-code-review Story #27` | Planned | - | - |
| #27 | 10 | `/arfd-commit-push 27` | Planned | - | - |
| #27 | 11 | `/finishing-a-development-branch Story #27` | Planned | - | - |
| #27 | 12 | `/arfd-story-complete 27` | Planned | - | - |
| #28 | 1 | `/arfd-story-start 28` | Planned | - | - |
| #28 | 2 | `/brainstorming Story #28: write and validate ARFD lake tables after CDC apply` | Planned | - | - |
| #28 | 3 | `/using-git-worktrees Story #28: branch m03-0008-write-validate-lake` | Planned | - | - |
| #28 | 4 | `/writing-plans Story #28` | Planned | - | - |
| #28 | 5 | `/test-driven-development Story #28` | Planned | - | - |
| #28 | 6 | `/subagent-driven-development Story #28` | Planned | - | - |
| #28 | 7 | `/arfd-commit-push 28` after every task (repeat) | Planned | - | - |
| #28 | 8 | `/verification-before-completion Story #28` | Planned | - | - |
| #28 | 9 | `/requesting-code-review Story #28` | Planned | - | - |
| #28 | 10 | `/arfd-commit-push 28` | Planned | - | - |
| #28 | 11 | `/finishing-a-development-branch Story #28` | Planned | - | - |
| #28 | 12 | `/arfd-story-complete 28` | Planned | - | - |
| Feature #22 | 1 | `/arfd-feature-complete 22` | In progress | 2026-11-19 17:22 | - |
| Feature #25 | 1 | `/arfd-feature-complete 25` | Planned | - | - |
| Epic #21 | 1 | `/arfd-epic-complete 21` | In progress | 2026-11-19 17:22 | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team). M04 board stories (#31, #55, #56, …) may exist ahead of time but product work starts only after M03 completes (or explicit parallel) **and** `/arfd-story-start N`.
