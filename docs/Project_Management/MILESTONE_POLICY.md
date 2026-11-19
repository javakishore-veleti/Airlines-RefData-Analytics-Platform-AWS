# Milestone policy — working increment first

**Applies to:** ARFD GitHub Milestones M01 forward

## Rule

Every **GitHub Milestone** must deliver a **working product increment** an operator or user can demo — not documentation alone.

Docs, ADRs, and Superpowers specs/plans still happen — as **stories or acceptance criteria inside** a product milestone (via the Superpowers path + `/arfd-*` wrappers). They do not get their own milestone unless tied to a shippable outcome.

## Done-when

1. A named runtime artifact works (lake table with rows, job success, API response, UI screen, etc.)
2. Operator proof is recorded
3. Stories used `/arfd-story-start` → Superpowers natives → `/arfd-story-complete`
4. Hard gate held: no product code without milestoned `[Story]` + story-start
