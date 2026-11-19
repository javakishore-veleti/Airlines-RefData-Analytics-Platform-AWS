# Milestone M01 - Foundation and Superpowers

**Scope:** ARFD methodology (Superpowers + `/arfd-*` wrappers), product docs alignment, and repository skeleton for CICD, Middleware, and Portals. No AWS stack creates in this milestone.

**Status:** open. Epic #1; features #2, #6; 6 stories. 0 done; 6 left to build.

How to read this file:
- `#1` is the GitHub issue number. The `M01-00NN` key is the sequence tag at the start of the issue title. Keys are not in build order.
- Section 1 is the table of contents in the order the work should be built. Section 2 groups the same issues as epic, feature and story.
- Section 3 has the Superpowers commands to run for each story, one after the other. Section 4 explains the project skills (`arfd-`) those commands use.

## Contents

- [1. Table of contents (build order)](#1-table-of-contents-build-order)
- [2. The same issues grouped by epic and feature](#2-the-same-issues-grouped-by-epic-and-feature)
- [3. Superpowers workflow](#3-superpowers-workflow)
- [4. Project skills](#4-project-skills-arfd----airlines-reference-data)
- [5. Notes](#5-notes)

## 1. Table of contents (build order)

### Phase 1 - Superpowers and agent contract

| # | Issue | Key | Type | Title | Why here |
|---|---|---|---|---|---|
| 1 | #1 | M01-0001 | Epic | Foundation and Superpowers | Parent of the features below |
| 2 | #2 | M01-0002 | Feature | Superpowers and agent contract | Parent of the stories below |
| 3 | #3 | M01-0003 | Story | Confirm Superpowers plugin and vendored skills | Plugin must be enabled before story work |
| 4 | #4 | M01-0004 | Story | ARFD agent contract (AGENTS.md and Cursor rules) | Hard gate and workflow contract |
| 5 | #5 | M01-0005 | Story | Document /arfd-* wrappers vs Superpowers natives | Wrappers wrap natives; do not replace them |

### Phase 2 - Repository skeleton

| # | Issue | Key | Type | Title | Why here |
|---|---|---|---|---|---|
| 6 | #6 | M01-0006 | Feature | Repository skeleton | Parent of the stories below |
| 7 | #7 | M01-0007 | Story | CICD/Local path stubs | Runtime lifecycle paths |
| 8 | #8 | M01-0008 | Story | Middleware path stubs | API and DAGs homes |
| 9 | #9 | M01-0009 | Story | Portals path stubs | Admin and Intelligence homes |

## 2. The same issues grouped by epic and feature

```
Epic #1  M01-0001  Foundation and Superpowers
|
+-- Feature #2  M01-0002  Superpowers and agent contract
|     +-- #3  Confirm Superpowers plugin and vendored skills
|     +-- #4  ARFD agent contract (AGENTS.md and Cursor rules)
|     +-- #5  Document /arfd-* wrappers vs Superpowers natives
|
+-- Feature #6  M01-0006  Repository skeleton
      +-- #7  CICD/Local path stubs
      +-- #8  Middleware path stubs
      +-- #9  Portals path stubs
```

## 3. Superpowers workflow

One chat per story. Run the commands of a story from top to bottom. `/arfd-*` are the project skills (section 4); the others come from the Superpowers plugin.

Every command has its own row with a **Status** (`Planned`, `In progress` or `Done`), a **Started** date and a **Completed** date (`-` until set). The step that is `In progress` is the one to run next. You do not edit the table: when a step finishes, `/arfd-milestone-log N` marks it `Done` with today's date and starts the next step. `/arfd-story-start` and `/arfd-story-complete` log their own step. The change is saved in the next `/arfd-commit-push`.

Standard code story, with `N` as the issue number:

| Step | Command | What it does |
|---|---|---|
| 1 | `/arfd-story-start N` | Marks the issue in progress and refreshes the feature and epic |
| 2 | `/brainstorming Story #N ...` | Confirms the design against the issue |
| 3 | `/using-git-worktrees Story #N: branch ...` | Creates an isolated workspace on a new branch for the story |
| 4 | `/writing-plans Story #N` | Breaks the story into small tasks with exact files and verification steps |
| 5 | `/test-driven-development Story #N` | Loads RED-GREEN-REFACTOR rules for step 6 |
| 6 | `/subagent-driven-development Story #N` | Builds each task with a fresh subagent (or `/executing-plans Story #N`) |
| 7 | `/arfd-commit-push N` | After every task of step 6 (repeat for each task) |
| 8 | `/verification-before-completion Story #N` | Runs checks and acceptance items |
| 9 | `/requesting-code-review Story #N` | Reviews the story against the plan |
| 10 | `/arfd-commit-push N` | Commits the review fixes |
| 11 | `/finishing-a-development-branch Story #N` | Merge/PR/cleanup |
| 12 | `/arfd-story-complete N` | Closes the story and refreshes the feature |

If a test fails and you do not know why, run `/systematic-debugging Story #N` before changing code.

### Phase 1 and Phase 2 - all M01 stories

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #3 | 1 | `/arfd-story-start 3` | Done | 2026-11-19 16:23 | 2026-11-19 16:24 |
| #3 | 2 | `/brainstorming Story #3: confirm Superpowers plugin enablement and vendored skills layout for ARFD` | Done | 2026-11-19 16:24 | 2026-11-19 16:24 |
| #3 | 3 | `/verification-before-completion Story #3` | Done | 2026-11-19 16:24 | 2026-11-19 16:24 |
| #3 | 4 | `/arfd-commit-push 3` | Done | 2026-11-19 16:24 | 2026-11-19 16:24 |
| #3 | 5 | `/arfd-story-complete 3` | In progress | 2026-11-19 16:24 | - |
| #4 | 1 | `/arfd-story-start 4` | Done | 2026-11-19 16:25 | 2026-11-19 16:25 |
| #4 | 2 | `/brainstorming Story #4: align AGENTS.md and Cursor rules for ARFD hard gate and one-milestone workflow` | Done | 2026-11-19 16:25 | 2026-11-19 16:25 |
| #4 | 3 | `/verification-before-completion Story #4` | Done | 2026-11-19 16:25 | 2026-11-19 16:25 |
| #4 | 4 | `/arfd-commit-push 4` | Done | 2026-11-19 16:25 | 2026-11-19 16:25 |
| #4 | 5 | `/arfd-story-complete 4` | In progress | 2026-11-19 16:25 | - |
| #5 | 1 | `/arfd-story-start 5` | Done | 2026-11-19 16:26 | 2026-11-19 16:26 |
| #5 | 2 | `/brainstorming Story #5: document that /arfd-* wrappers do not replace Superpowers natives` | Done | 2026-11-19 16:26 | 2026-11-19 16:26 |
| #5 | 3 | `/verification-before-completion Story #5` | Done | 2026-11-19 16:26 | 2026-11-19 16:26 |
| #5 | 4 | `/arfd-commit-push 5` | In progress | 2026-11-19 16:26 | - |
| #5 | 5 | `/arfd-story-complete 5` | Planned | - | - |
| #7 | 1 | `/arfd-story-start 7` | Planned | - | - |
| #7 | 2 | `/brainstorming Story #7: add CICD/Local placeholders for lifecycle scripts and Kafka compose path` | Planned | - | - |
| #7 | 3 | `/using-git-worktrees Story #7: branch m01-0007-cicd-local-path-stubs` | Planned | - | - |
| #7 | 4 | `/writing-plans Story #7` | Planned | - | - |
| #7 | 5 | `/test-driven-development Story #7` | Planned | - | - |
| #7 | 6 | `/subagent-driven-development Story #7` | Planned | - | - |
| #7 | 7 | `/arfd-commit-push 7` after every task (repeat) | Planned | - | - |
| #7 | 8 | `/verification-before-completion Story #7` | Planned | - | - |
| #7 | 9 | `/requesting-code-review Story #7` | Planned | - | - |
| #7 | 10 | `/arfd-commit-push 7` | Planned | - | - |
| #7 | 11 | `/finishing-a-development-branch Story #7` | Planned | - | - |
| #7 | 12 | `/arfd-story-complete 7` | Planned | - | - |
| #8 | 1 | `/arfd-story-start 8` | Planned | - | - |
| #8 | 2 | `/brainstorming Story #8: add Middleware/API-Services and Middleware/DAGs placeholders` | Planned | - | - |
| #8 | 3 | `/using-git-worktrees Story #8: branch m01-0008-middleware-path-stubs` | Planned | - | - |
| #8 | 4 | `/writing-plans Story #8` | Planned | - | - |
| #8 | 5 | `/test-driven-development Story #8` | Planned | - | - |
| #8 | 6 | `/subagent-driven-development Story #8` | Planned | - | - |
| #8 | 7 | `/arfd-commit-push 8` after every task (repeat) | Planned | - | - |
| #8 | 8 | `/verification-before-completion Story #8` | Planned | - | - |
| #8 | 9 | `/requesting-code-review Story #8` | Planned | - | - |
| #8 | 10 | `/arfd-commit-push 8` | Planned | - | - |
| #8 | 11 | `/finishing-a-development-branch Story #8` | Planned | - | - |
| #8 | 12 | `/arfd-story-complete 8` | Planned | - | - |
| #9 | 1 | `/arfd-story-start 9` | Planned | - | - |
| #9 | 2 | `/brainstorming Story #9: add Airlines-RD-Admin and Airlines-RD-Intelligence portal placeholders` | Planned | - | - |
| #9 | 3 | `/using-git-worktrees Story #9: branch m01-0009-portals-path-stubs` | Planned | - | - |
| #9 | 4 | `/writing-plans Story #9` | Planned | - | - |
| #9 | 5 | `/test-driven-development Story #9` | Planned | - | - |
| #9 | 6 | `/subagent-driven-development Story #9` | Planned | - | - |
| #9 | 7 | `/arfd-commit-push 9` after every task (repeat) | Planned | - | - |
| #9 | 8 | `/verification-before-completion Story #9` | Planned | - | - |
| #9 | 9 | `/requesting-code-review Story #9` | Planned | - | - |
| #9 | 10 | `/arfd-commit-push 9` | Planned | - | - |
| #9 | 11 | `/finishing-a-development-branch Story #9` | Planned | - | - |
| #9 | 12 | `/arfd-story-complete 9` | Planned | - | - |
| Feature #2 | 1 | `/arfd-feature-complete 2` | Planned | - | - |
| Feature #6 | 1 | `/arfd-feature-complete 6` | Planned | - | - |
| Epic #1 | 1 | `/arfd-epic-complete 1` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

The skills live in `.cursor/skills/`. Each takes a GitHub issue number. They are **wrappers** around Superpowers natives for board, git, and milestone logging.

| Command | When | What it does |
|---|---|---|
| `/arfd-story-start N` | Before the first Superpowers command of a story | Sets the story to `status: in-progress`, refreshes feature and epic |
| `/arfd-story-complete N` | After review and the final commit | Ticks acceptance, closes the story, refreshes the feature |
| `/arfd-feature-complete N` | When every story of the feature is done | Marks the feature done and closes it |
| `/arfd-epic-complete N` | When every feature of the epic is done | Marks the epic done and marks this file complete |
| `/arfd-milestone-log N` | After each workflow step finishes | Marks the `In progress` step Done and starts the next |
| `/arfd-commit-push N` | After every task, and at the end of each story | Lint/tests when applicable, commit as repo owner, push |
| `/arfd-progress-sync N` | Used by the skills above | Rebuilds feature/epic checklist from child issues |

## 5. Notes

- **One branch and worktree per code story.** `/using-git-worktrees` creates the story branch in `.worktrees/` (git-ignored). Decision/docs-only stories may stay shorter (no worktree).
- **Hard gate:** no product code without an open `[Story]` on a GitHub Milestone and `/arfd-story-start N`.
- **Next milestone:** M02 runtime bootstrap (`Milestone_02.md`).
