# Superpowers (vendored)

Vendored from [obra/superpowers](https://github.com/obra/superpowers) for in-repo agent methodology.

- **Version:** see [`VERSION`](VERSION)
- **Skills:** [`skills/`](skills/)
- **Cursor plugin metadata:** [`cursor-plugin/`](cursor-plugin/)
- **Hooks:** [`hooks/`](hooks/)

## Workflow (run **one milestone at a time**, in order)

1. `skills/brainstorming` — clarify intent → design doc (human approves)
2. `skills/writing-plans` — bite-sized implementation plan
3. `skills/using-git-worktrees` — isolated branch / worktree
4. `skills/subagent-driven-development` **or** `skills/executing-plans`
5. `skills/test-driven-development` — during every implementation task
6. `skills/requesting-code-review` — between tasks / before merge
7. `skills/finishing-a-development-branch` — merge/PR/cleanup

Do **not** start the next milestone until the current milestone’s stories are closed.

## Cursor install

1. Prefer marketplace hooks: in Agent chat run `/add-plugin superpowers`
2. Keep this `superpowers/` tree in the repo so skills remain available offline and version-pinned
3. Project rule: see [`../cursor/rules/superpowers-workflow.mdc`](../cursor/rules/superpowers-workflow.mdc) (copy into `.cursor/rules/` if your Cursor setup reads that path)

Upstream license: MIT — see [`LICENSE`](LICENSE).
