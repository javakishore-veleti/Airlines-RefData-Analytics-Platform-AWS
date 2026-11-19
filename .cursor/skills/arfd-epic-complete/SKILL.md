---
name: arfd-epic-complete
description: Completes an ARFD (Airlines Reference Data) GitHub epic once all its features are done - marks it done, closes it and marks the milestone file complete. Use when the user runs /arfd-epic-complete N. Board wrapper around Superpowers.
disable-model-invocation: true
---

# arfd-epic-complete

**Role:** ARFD board wrapper. Closes the epic and updates the milestone markdown after all features completed via Superpowers + `/arfd-feature-complete`.

Input: epic issue number `N`. Run `gh` from the repository root: it reads the repository from the git remote, so never type the owner or repository name. Scratch files go in `runtime_data/tmp/`.

1. Run `arfd-progress-sync` on `N`.
2. If any feature in the checklist is not closed, stop and list it. Do not change the epic.
3. Body: replace or append the `**Status:** Done — All F features are done: #a, #b, #c.` line.
4. `gh issue edit N --remove-label "status: planned" --remove-label "status: in-progress" --add-label "status: done" --body-file runtime_data/tmp/issue-N.md`, then `gh issue close N --reason completed`.
5. Run `arfd-milestone-log N`.
6. In the matching `docs/Project_Management/Issues/Milestone_MM.md` (from the epic title prefix), change the `**Status:**` line to `**Status: complete.**` with the final epic, feature and story counts.
7. Run `arfd-commit-push` with the message `M0N: mark milestone complete` (use the milestone prefix from the epic title).
