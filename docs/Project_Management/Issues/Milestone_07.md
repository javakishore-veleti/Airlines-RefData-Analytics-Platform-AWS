# Milestone M07 - AWS deployment

**Scope:** Deploy the same CDC → stream → apply → lake pattern using AWS native and managed services. Start only with explicit go-ahead.

**Status:** open. Epic #50; 1 features; 3 stories. 0 done; 3 left to build.

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
| 1 | #50 | M07-0001 | Epic | AWS deployment | Parent of the features below |
| 2 | #51 | M07-0002 | Feature | Infrastructure as code and cutover | Parent of the stories below |
| 3 | #52 | M07-0003 | Story | Parameterized CloudFormation for the managed path | IaC |
| 4 | #53 | M07-0004 | Story | Application-stack to AWS cutover runbook | Operations |
| 5 | #54 | M07-0005 | Story | Monitoring and cleanup procedures | Operate safely |

## 2. The same issues grouped by epic and feature

```
Epic #50  M07-0001  AWS deployment
|
+-- Feature #51  M07-0002  Infrastructure as code and cutover
\     +-- #52  Parameterized CloudFormation for the managed path
\     +-- #53  Application-stack to AWS cutover runbook
\     +-- #54  Monitoring and cleanup procedures
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

| Issue | Step | Command | Status | Started | Completed |
|---|---|---|---|---|---|
| #52 | 1 | `/arfd-story-start 52` | In progress | - | - |
| #52 | 2 | `/brainstorming Story #52: parameterize CloudFormation for ARFD AWS managed path` | Planned | - | - |
| #52 | 3 | `/using-git-worktrees Story #52: branch m07-0003-cfn-parameterized` | Planned | - | - |
| #52 | 4 | `/writing-plans Story #52` | Planned | - | - |
| #52 | 5 | `/test-driven-development Story #52` | Planned | - | - |
| #52 | 6 | `/subagent-driven-development Story #52` | Planned | - | - |
| #52 | 7 | `/arfd-commit-push 52` after every task (repeat) | Planned | - | - |
| #52 | 8 | `/verification-before-completion Story #52` | Planned | - | - |
| #52 | 9 | `/requesting-code-review Story #52` | Planned | - | - |
| #52 | 10 | `/arfd-commit-push 52` | Planned | - | - |
| #52 | 11 | `/finishing-a-development-branch Story #52` | Planned | - | - |
| #52 | 12 | `/arfd-story-complete 52` | Planned | - | - |
| #53 | 1 | `/arfd-story-start 53` | Planned | - | - |
| #53 | 2 | `/brainstorming Story #53: write cutover runbook from application stack to AWS managed services` | Planned | - | - |
| #53 | 3 | `/verification-before-completion Story #53` | Planned | - | - |
| #53 | 4 | `/arfd-commit-push 53` | Planned | - | - |
| #53 | 5 | `/arfd-story-complete 53` | Planned | - | - |
| #54 | 1 | `/arfd-story-start 54` | Planned | - | - |
| #54 | 2 | `/brainstorming Story #54: define monitoring and cleanup procedures for ARFD on AWS` | Planned | - | - |
| #54 | 3 | `/verification-before-completion Story #54` | Planned | - | - |
| #54 | 4 | `/arfd-commit-push 54` | Planned | - | - |
| #54 | 5 | `/arfd-story-complete 54` | Planned | - | - |
| Feature #51 | 1 | `/arfd-feature-complete 51` | Planned | - | - |
| Epic #50 | 1 | `/arfd-epic-complete 50` | Planned | - | - |

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
