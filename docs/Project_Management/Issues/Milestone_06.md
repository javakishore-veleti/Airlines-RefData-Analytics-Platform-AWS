# Milestone M06 - Airlines-RD-Intelligence

**Scope:** Intelligence portal for analysts, risk managers, and data managers to view and query lake-backed reference data.

**Status:** open. Epic #44; 1 features; 4 stories. 0 done; 4 left to build.

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
| 1 | #44 | M06-0001 | Epic | Airlines-RD-Intelligence | Parent of the features below |
| 2 | #45 | M06-0002 | Feature | Intelligence portal application | Parent of the stories below |
| 3 | #46 | M06-0003 | Story | App shell and role-oriented navigation | Portal foundation |
| 4 | #47 | M06-0004 | Story | Browse and filter reference data | Primary read path |
| 5 | #48 | M06-0005 | Story | Query and saved views | Analyst workflows |
| 6 | #49 | M06-0006 | Story | Wire Intelligence portal to Middleware/API-Services | End-to-end intelligence path |

## 2. The same issues grouped by epic and feature

```
Epic #44  M06-0001  Airlines-RD-Intelligence
|
+-- Feature #45  M06-0002  Intelligence portal application
\     +-- #46  App shell and role-oriented navigation
\     +-- #47  Browse and filter reference data
\     +-- #48  Query and saved views
\     +-- #49  Wire Intelligence portal to Middleware/API-Services
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #46 | 1 | `/arfd-story-start 46` | In progress | - | - |
| #46 | 2 | `/brainstorming Story #46: scaffold Airlines-RD-Intelligence shell and role-oriented nav` | Planned | - | - |
| #46 | 3 | `/using-git-worktrees Story #46: branch m06-0003-intel-app-shell` | Planned | - | - |
| #46 | 4 | `/writing-plans Story #46` | Planned | - | - |
| #46 | 5 | `/test-driven-development Story #46` | Planned | - | - |
| #46 | 6 | `/subagent-driven-development Story #46` | Planned | - | - |
| #46 | 7 | `/arfd-commit-push 46` after every task (repeat) | Planned | - | - |
| #46 | 8 | `/verification-before-completion Story #46` | Planned | - | - |
| #46 | 9 | `/requesting-code-review Story #46` | Planned | - | - |
| #46 | 10 | `/arfd-commit-push 46` | Planned | - | - |
| #46 | 11 | `/finishing-a-development-branch Story #46` | Planned | - | - |
| #46 | 12 | `/arfd-story-complete 46` | Planned | - | - |
| #47 | 1 | `/arfd-story-start 47` | Planned | - | - |
| #47 | 2 | `/brainstorming Story #47: build browse/filter experience for RD Intelligence` | Planned | - | - |
| #47 | 3 | `/using-git-worktrees Story #47: branch m06-0004-browse-filter-refdata` | Planned | - | - |
| #47 | 4 | `/writing-plans Story #47` | Planned | - | - |
| #47 | 5 | `/test-driven-development Story #47` | Planned | - | - |
| #47 | 6 | `/subagent-driven-development Story #47` | Planned | - | - |
| #47 | 7 | `/arfd-commit-push 47` after every task (repeat) | Planned | - | - |
| #47 | 8 | `/verification-before-completion Story #47` | Planned | - | - |
| #47 | 9 | `/requesting-code-review Story #47` | Planned | - | - |
| #47 | 10 | `/arfd-commit-push 47` | Planned | - | - |
| #47 | 11 | `/finishing-a-development-branch Story #47` | Planned | - | - |
| #47 | 12 | `/arfd-story-complete 47` | Planned | - | - |
| #48 | 1 | `/arfd-story-start 48` | Planned | - | - |
| #48 | 2 | `/brainstorming Story #48: define and implement query/saved views for RD Intelligence` | Planned | - | - |
| #48 | 3 | `/using-git-worktrees Story #48: branch m06-0005-query-saved-views` | Planned | - | - |
| #48 | 4 | `/writing-plans Story #48` | Planned | - | - |
| #48 | 5 | `/test-driven-development Story #48` | Planned | - | - |
| #48 | 6 | `/subagent-driven-development Story #48` | Planned | - | - |
| #48 | 7 | `/arfd-commit-push 48` after every task (repeat) | Planned | - | - |
| #48 | 8 | `/verification-before-completion Story #48` | Planned | - | - |
| #48 | 9 | `/requesting-code-review Story #48` | Planned | - | - |
| #48 | 10 | `/arfd-commit-push 48` | Planned | - | - |
| #48 | 11 | `/finishing-a-development-branch Story #48` | Planned | - | - |
| #48 | 12 | `/arfd-story-complete 48` | Planned | - | - |
| #49 | 1 | `/arfd-story-start 49` | Planned | - | - |
| #49 | 2 | `/brainstorming Story #49: wire Airlines-RD-Intelligence to Middleware/API-Services` | Planned | - | - |
| #49 | 3 | `/using-git-worktrees Story #49: branch m06-0006-intel-api-wire` | Planned | - | - |
| #49 | 4 | `/writing-plans Story #49` | Planned | - | - |
| #49 | 5 | `/test-driven-development Story #49` | Planned | - | - |
| #49 | 6 | `/subagent-driven-development Story #49` | Planned | - | - |
| #49 | 7 | `/arfd-commit-push 49` after every task (repeat) | Planned | - | - |
| #49 | 8 | `/verification-before-completion Story #49` | Planned | - | - |
| #49 | 9 | `/requesting-code-review Story #49` | Planned | - | - |
| #49 | 10 | `/arfd-commit-push 49` | Planned | - | - |
| #49 | 11 | `/finishing-a-development-branch Story #49` | Planned | - | - |
| #49 | 12 | `/arfd-story-complete 49` | Planned | - | - |
| Feature #45 | 1 | `/arfd-feature-complete 45` | Planned | - | - |
| Epic #44 | 1 | `/arfd-epic-complete 44` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
