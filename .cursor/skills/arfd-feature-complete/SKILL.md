---
name: arfd-feature-complete
description: Completes an ARFD (Airlines Reference Data) GitHub feature once all its stories are done - marks it done, closes it and refreshes the epic. Use when the user runs /arfd-feature-complete N. Board wrapper around Superpowers story completion.
disable-model-invocation: true
---

# arfd-feature-complete

**Role:** ARFD board wrapper. Does not replace Superpowers; closes the feature only when every child story already finished the full Superpowers path + `/arfd-story-complete`.

Input: feature issue number `N`. Run `gh` from the repository root: it reads the repository from the git remote, so never type the owner or repository name. Scratch files go in `runtime_data/tmp/`.

1. Run `arfd-progress-sync` on `N`.
2. Read the checklist. If any story is not closed, stop and list the open ones with their numbers. Do not change the feature.
3. Body: replace or append the `**Status:**` line with `**Status:** Done — All T stories are done: #a, #b, #c.` (T is the story count).
4. `gh issue edit N --remove-label "status: planned" --remove-label "status: in-progress" --add-label "status: done" --body-file runtime_data/tmp/issue-N.md`, then `gh issue close N --reason completed`.
5. Run `arfd-milestone-log N`, then `arfd-commit-push` with the message `M0N: complete feature #N` (use the milestone prefix from the feature title).
6. Read `**Epic:** #E` and run `arfd-progress-sync` on `E`. If every feature of `E` is done, end with: "All features of #E are done. Run `/arfd-epic-complete E`."
