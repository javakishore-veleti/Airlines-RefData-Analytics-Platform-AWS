#!/usr/bin/env python3
"""Create ARFD GitHub issues and docs/Project_Management/Issues/Milestone_XX.md files."""
from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISSUES_DIR = ROOT / "docs" / "Project_Management" / "Issues"


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def create_issue(title: str, body: str, milestone: str, labels: list[str]) -> int:
    cmd = [
        "gh",
        "issue",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--milestone",
        milestone,
    ]
    for lab in labels:
        cmd.extend(["--label", lab])
    url = run(cmd)
    return int(url.rstrip("/").split("/")[-1])


def story_workflow_rows(issue: int, key: str, title: str, branch: str, brainstorm: str) -> list[tuple]:
    """Return (issue_label, step, command) rows for a standard code story."""
    return [
        (f"#{issue}", 1, f"`/arfd-story-start {issue}`"),
        (f"#{issue}", 2, f"`/brainstorming Story #{issue}: {brainstorm}`"),
        (f"#{issue}", 3, f"`/using-git-worktrees Story #{issue}: branch {branch}`"),
        (f"#{issue}", 4, f"`/writing-plans Story #{issue}`"),
        (f"#{issue}", 5, f"`/test-driven-development Story #{issue}`"),
        (f"#{issue}", 6, f"`/subagent-driven-development Story #{issue}`"),
        (f"#{issue}", 7, f"`/arfd-commit-push {issue}` after every task (repeat)"),
        (f"#{issue}", 8, f"`/verification-before-completion Story #{issue}`"),
        (f"#{issue}", 9, f"`/requesting-code-review Story #{issue}`"),
        (f"#{issue}", 10, f"`/arfd-commit-push {issue}`"),
        (f"#{issue}", 11, f"`/finishing-a-development-branch Story #{issue}`"),
        (f"#{issue}", 12, f"`/arfd-story-complete {issue}`"),
    ]


def docs_only_workflow(issue: int, brainstorm: str) -> list[tuple]:
    return [
        (f"#{issue}", 1, f"`/arfd-story-start {issue}`"),
        (f"#{issue}", 2, f"`/brainstorming Story #{issue}: {brainstorm}`"),
        (f"#{issue}", 3, f"`/verification-before-completion Story #{issue}`"),
        (f"#{issue}", 4, f"`/arfd-commit-push {issue}`"),
        (f"#{issue}", 5, f"`/arfd-story-complete {issue}`"),
    ]


def workflow_table(rows: list[tuple], first_in_progress: bool = True) -> str:
    lines = [
        "| Issue | Step | Command | Status | Started | Completed |",
        "|---|---|---|---|---|---|",
    ]
    for i, (iss, step, cmd) in enumerate(rows):
        status = "In progress" if first_in_progress and i == 0 else "Planned"
        started = "-" if status == "Planned" else "-"
        lines.append(f"| {iss} | {step} | {cmd} | {status} | {started} | - |")
        # only first row of whole milestone section should be in progress - caller handles
    return "\n".join(lines)


def write_milestone(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)
    ids: dict[str, int] = {}

    # -------- M01 --------
    ms1 = "M01 — Foundation & Superpowers (ARFD)"
    ids["e01"] = create_issue(
        "M01-0001 [Epic] Foundation and Superpowers",
        textwrap.dedent(
            """\
            **Status:** Planned

            **Progress:** 0 of 2 done — planned

            Establish ARFD methodology, docs, and repository skeleton.

            **Features:**
            - [ ] #F1 Superpowers and agent contract (planned)
            - [ ] #F2 Repository skeleton (planned)
            """
        ),
        ms1,
        ["type:epic", "area:foundation", "status: planned"],
    )
    ids["f01"] = create_issue(
        "M01-0002 [Feature] Superpowers and agent contract",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']}

            **Status:** Planned

            **Progress:** 0 of 3 done — planned

            Vendor Superpowers, ARFD wrappers, and agent contract docs.

            **Stories:**
            - [ ] #S1 Confirm Superpowers plugin and vendored skills (planned)
            - [ ] #S2 ARFD agent contract (AGENTS.md and Cursor rules) (planned)
            - [ ] #S3 Document /arfd-* wrappers vs Superpowers natives (planned)
            """
        ),
        ms1,
        ["type:feature", "area:foundation", "status: planned"],
    )
    ids["s01"] = create_issue(
        "M01-0003 [Story] Confirm Superpowers plugin and vendored skills",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f01']}

            **Status:** Planned

            Confirm `.cursor/settings.json` enables Superpowers, `superpowers/` is present, and `/add-plugin superpowers` is documented.

            **Acceptance**
            - [ ] Superpowers enabled in `.cursor/settings.json`
            - [ ] Vendored skills under `superpowers/skills/`
            - [ ] README or AGENTS.md documents plugin install
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )
    ids["s02"] = create_issue(
        "M01-0004 [Story] ARFD agent contract (AGENTS.md and Cursor rules)",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f01']}

            **Status:** Planned

            Keep AGENTS.md and `.cursor/rules` aligned: one milestone at a time, hard gate, arfd wrappers around Superpowers.

            **Acceptance**
            - [ ] AGENTS.md describes ARFD workflow
            - [ ] Hard-gate rule present
            - [ ] Superpowers workflow rule present
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )
    ids["s03"] = create_issue(
        "M01-0005 [Story] Document /arfd-* wrappers vs Superpowers natives",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f01']}

            **Status:** Planned

            Document that `/arfd-*` skills wrap board/git/milestone logging and do not replace Superpowers natives.

            **Acceptance**
            - [ ] README Superpowers section lists natives and wrappers
            - [ ] Each `.cursor/skills/arfd-*/SKILL.md` states wrapper role
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )
    ids["f02"] = create_issue(
        "M01-0006 [Feature] Repository skeleton",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']}

            **Status:** Planned

            **Progress:** 0 of 3 done — planned

            Placeholder trees for CICD, Middleware, and Portals.

            **Stories:**
            - [ ] #S4 CICD/Local path stubs (planned)
            - [ ] #S5 Middleware path stubs (planned)
            - [ ] #S6 Portals path stubs (planned)
            """
        ),
        ms1,
        ["type:feature", "area:foundation", "status: planned"],
    )
    ids["s04"] = create_issue(
        "M01-0007 [Story] CICD/Local path stubs",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f02']}

            **Status:** Planned

            Add placeholders for `docker-all-up.sh`, `all-down.sh`, `all-status.sh`, and `Kafka/docker-compose.yaml`.

            **Acceptance**
            - [ ] Paths exist under `CICD/Local/`
            - [ ] Short README notes intent (no live services required yet)
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )
    ids["s05"] = create_issue(
        "M01-0008 [Story] Middleware path stubs",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f02']}

            **Status:** Planned

            Add `Middleware/API-Services` and `Middleware/DAGs` placeholders.

            **Acceptance**
            - [ ] Both directories exist with README notes
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )
    ids["s06"] = create_issue(
        "M01-0009 [Story] Portals path stubs",
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']} · **Feature:** #{ids['f02']}

            **Status:** Planned

            Add `Portals/Airlines-RD-Admin` and `Portals/Airlines-RD-Intelligence` placeholders.

            **Acceptance**
            - [ ] Both portal directories exist with README notes
            """
        ),
        ms1,
        ["type:story", "area:foundation", "status: planned"],
    )

    # Patch M01 feature/epic bodies with real child numbers
    def edit_body(n: int, body: str) -> None:
        p = ROOT / "runtime_data" / "tmp" / f"issue-{n}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        run(["gh", "issue", "edit", str(n), "--body-file", str(p)])

    edit_body(
        ids["f01"],
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']}

            **Status:** Planned

            **Progress:** 0 of 3 done — planned

            Vendor Superpowers, ARFD wrappers, and agent contract docs.

            **Stories:**
            - [ ] #{ids['s01']} Confirm Superpowers plugin and vendored skills (planned)
            - [ ] #{ids['s02']} ARFD agent contract (AGENTS.md and Cursor rules) (planned)
            - [ ] #{ids['s03']} Document /arfd-* wrappers vs Superpowers natives (planned)
            """
        ),
    )
    edit_body(
        ids["f02"],
        textwrap.dedent(
            f"""\
            **Epic:** #{ids['e01']}

            **Status:** Planned

            **Progress:** 0 of 3 done — planned

            Placeholder trees for CICD, Middleware, and Portals.

            **Stories:**
            - [ ] #{ids['s04']} CICD/Local path stubs (planned)
            - [ ] #{ids['s05']} Middleware path stubs (planned)
            - [ ] #{ids['s06']} Portals path stubs (planned)
            """
        ),
    )
    edit_body(
        ids["e01"],
        textwrap.dedent(
            f"""\
            **Status:** Planned

            **Progress:** 0 of 2 done — planned

            Establish ARFD methodology, docs, and repository skeleton.

            **Features:**
            - [ ] #{ids['f01']} Superpowers and agent contract (planned)
            - [ ] #{ids['f02']} Repository skeleton (planned)
            """
        ),
    )

    # Write Milestone_01.md
    m01_rows = []
    m01_rows += docs_only_workflow(
        ids["s01"],
        "confirm Superpowers plugin enablement and vendored skills layout for ARFD",
    )
    m01_rows += docs_only_workflow(
        ids["s02"],
        "align AGENTS.md and Cursor rules for ARFD hard gate and one-milestone workflow",
    )
    m01_rows += docs_only_workflow(
        ids["s03"],
        "document that /arfd-* wrappers do not replace Superpowers natives",
    )
    m01_rows += story_workflow_rows(
        ids["s04"],
        "M01-0007",
        "CICD stubs",
        "m01-0007-cicd-local-path-stubs",
        "add CICD/Local placeholders for lifecycle scripts and Kafka compose path",
    )
    m01_rows += story_workflow_rows(
        ids["s05"],
        "M01-0008",
        "Middleware stubs",
        "m01-0008-middleware-path-stubs",
        "add Middleware/API-Services and Middleware/DAGs placeholders",
    )
    m01_rows += story_workflow_rows(
        ids["s06"],
        "M01-0009",
        "Portals stubs",
        "m01-0009-portals-path-stubs",
        "add Airlines-RD-Admin and Airlines-RD-Intelligence portal placeholders",
    )
    m01_rows.append((f"Feature #{ids['f01']}", 1, f"`/arfd-feature-complete {ids['f01']}`"))
    m01_rows.append((f"Feature #{ids['f02']}", 1, f"`/arfd-feature-complete {ids['f02']}`"))
    m01_rows.append((f"Epic #{ids['e01']}", 1, f"`/arfd-epic-complete {ids['e01']}`"))

    def wf_table(rows: list[tuple]) -> str:
        lines = [
            "| Issue | Step | Command | Status | Started | Completed |",
            "|---|---|---|---|---|---|",
        ]
        for i, (iss, step, cmd) in enumerate(rows):
            status = "In progress" if i == 0 else "Planned"
            lines.append(f"| {iss} | {step} | {cmd} | {status} | - | - |")
        return "\n".join(lines)

    write_milestone(
        ISSUES_DIR / "Milestone_01.md",
        f"""# Milestone M01 - Foundation and Superpowers

**Scope:** ARFD methodology (Superpowers + `/arfd-*` wrappers), product docs alignment, and repository skeleton for CICD, Middleware, and Portals. No AWS stack creates in this milestone.

**Status:** open. Epic #{ids['e01']}; features #{ids['f01']}, #{ids['f02']}; 6 stories. 0 done; 6 left to build.

How to read this file:
- `#{ids['e01']}` is the GitHub issue number. The `M01-00NN` key is the sequence tag at the start of the issue title. Keys are not in build order.
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
| 1 | #{ids['e01']} | M01-0001 | Epic | Foundation and Superpowers | Parent of the features below |
| 2 | #{ids['f01']} | M01-0002 | Feature | Superpowers and agent contract | Parent of the stories below |
| 3 | #{ids['s01']} | M01-0003 | Story | Confirm Superpowers plugin and vendored skills | Plugin must be enabled before story work |
| 4 | #{ids['s02']} | M01-0004 | Story | ARFD agent contract (AGENTS.md and Cursor rules) | Hard gate and workflow contract |
| 5 | #{ids['s03']} | M01-0005 | Story | Document /arfd-* wrappers vs Superpowers natives | Wrappers wrap natives; do not replace them |

### Phase 2 - Repository skeleton

| # | Issue | Key | Type | Title | Why here |
|---|---|---|---|---|---|
| 6 | #{ids['f02']} | M01-0006 | Feature | Repository skeleton | Parent of the stories below |
| 7 | #{ids['s04']} | M01-0007 | Story | CICD/Local path stubs | Runtime lifecycle paths |
| 8 | #{ids['s05']} | M01-0008 | Story | Middleware path stubs | API and DAGs homes |
| 9 | #{ids['s06']} | M01-0009 | Story | Portals path stubs | Admin and Intelligence homes |

## 2. The same issues grouped by epic and feature

```
Epic #{ids['e01']}  M01-0001  Foundation and Superpowers
|
+-- Feature #{ids['f01']}  M01-0002  Superpowers and agent contract
|     +-- #{ids['s01']}  Confirm Superpowers plugin and vendored skills
|     +-- #{ids['s02']}  ARFD agent contract (AGENTS.md and Cursor rules)
|     +-- #{ids['s03']}  Document /arfd-* wrappers vs Superpowers natives
|
+-- Feature #{ids['f02']}  M01-0006  Repository skeleton
      +-- #{ids['s04']}  CICD/Local path stubs
      +-- #{ids['s05']}  Middleware path stubs
      +-- #{ids['s06']}  Portals path stubs
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

{wf_table(m01_rows)}

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
""",
    )

    # -------- Helper for remaining milestones (epic+feature+stories, thinner) --------
    def create_ms(
        file_name: str,
        ms_title: str,
        heading: str,
        scope: str,
        area: str,
        epic_key: str,
        epic_title: str,
        features: list[dict],
    ) -> None:
        """features: [{key, title, stories:[{key,title,acceptance,brainstorm,branch,docs_only}]}]"""
        e = create_issue(
            f"{epic_key} [Epic] {epic_title}",
            f"**Status:** Planned\n\n**Progress:** 0 of {len(features)} done — planned\n\n{scope}\n\n**Features:**\n",
            ms_title,
            ["type:epic", area, "status: planned"],
        )
        feat_ids = []
        all_story_meta = []
        tree_lines = [f"Epic #{e}  {epic_key}  {epic_title}", "|"]
        toc_rows = []
        seq = 1
        toc_rows.append((seq, e, epic_key, "Epic", epic_title, "Parent of the features below"))
        seq += 1
        for fdef in features:
            f = create_issue(
                f"{fdef['key']} [Feature] {fdef['title']}",
                f"**Epic:** #{e}\n\n**Status:** Planned\n\n**Progress:** 0 of {len(fdef['stories'])} done — planned\n\n**Stories:**\n",
                ms_title,
                ["type:feature", area, "status: planned"],
            )
            feat_ids.append((f, fdef))
            toc_rows.append((seq, f, fdef["key"], "Feature", fdef["title"], "Parent of the stories below"))
            seq += 1
            tree_lines.append(f"+-- Feature #{f}  {fdef['key']}  {fdef['title']}")
            story_ids = []
            for sdef in fdef["stories"]:
                s = create_issue(
                    f"{sdef['key']} [Story] {sdef['title']}",
                    textwrap.dedent(
                        f"""\
                        **Epic:** #{e} · **Feature:** #{f}

                        **Status:** Planned

                        {sdef.get('blurb', sdef['title'])}

                        **Acceptance**
                        {chr(10).join('- [ ] ' + a for a in sdef['acceptance'])}
                        """
                    ),
                    ms_title,
                    ["type:story", area, "status: planned"],
                )
                story_ids.append((s, sdef))
                toc_rows.append((seq, s, sdef["key"], "Story", sdef["title"], sdef.get("why", "Build in order")))
                seq += 1
                tree_lines.append(f"|     +-- #{s}  {sdef['title']}")
                all_story_meta.append((s, sdef, f))
            # indent fix for tree last feature
            tree_lines[-len(fdef["stories"]) - 1] = tree_lines[-len(fdef["stories"]) - 1].replace("+--", "+--" if fdef != features[-1] else "+--")
            edit_body(
                f,
                textwrap.dedent(
                    f"""\
                    **Epic:** #{e}

                    **Status:** Planned

                    **Progress:** 0 of {len(story_ids)} done — planned

                    **Stories:**
                    {chr(10).join(f"- [ ] #{sid} {sd['title']} (planned)" for sid, sd in story_ids)}
                    """
                ),
            )
            all_story_meta[-len(story_ids) :]  # noqa: keep
        edit_body(
            e,
            textwrap.dedent(
                f"""\
                **Status:** Planned

                **Progress:** 0 of {len(feat_ids)} done — planned

                {scope}

                **Features:**
                {chr(10).join(f"- [ ] #{fid} {fd['title']} (planned)" for fid, fd in feat_ids)}
                """
            ),
        )

        # rebuild tree cleanly
        tree = [f"Epic #{e}  {epic_key}  {epic_title}", "|"]
        for i, (fid, fdef) in enumerate(feat_ids):
            prefix = "+--" if True else "+--"
            tree.append(f"{prefix} Feature #{fid}  {fdef['key']}  {fdef['title']}")
            stories_for_f = [(s, sd) for s, sd, pf in all_story_meta if pf == fid]
            for j, (sid, sd) in enumerate(stories_for_f):
                branch = "\\" if i == len(feat_ids) - 1 else "|"
                tree.append(f"{branch}     +-- #{sid}  {sd['title']}")

        wf_rows: list[tuple] = []
        for s, sdef, _f in all_story_meta:
            if sdef.get("docs_only"):
                wf_rows += docs_only_workflow(s, sdef["brainstorm"])
            else:
                wf_rows += story_workflow_rows(
                    s,
                    sdef["key"],
                    sdef["title"],
                    sdef["branch"],
                    sdef["brainstorm"],
                )
        for fid, _ in feat_ids:
            wf_rows.append((f"Feature #{fid}", 1, f"`/arfd-feature-complete {fid}`"))
        wf_rows.append((f"Epic #{e}", 1, f"`/arfd-epic-complete {e}`"))

        toc = [
            "| # | Issue | Key | Type | Title | Why here |",
            "|---|---|---|---|---|---|",
        ]
        for num, iss, key, typ, title, why in toc_rows:
            toc.append(f"| {num} | #{iss} | {key} | {typ} | {title} | {why} |")

        n_stories = len(all_story_meta)
        content = f"""# Milestone {heading}

**Scope:** {scope}

**Status:** open. Epic #{e}; {len(feat_ids)} features; {n_stories} stories. 0 done; {n_stories} left to build.

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

{chr(10).join(toc)}

## 2. The same issues grouped by epic and feature

```
{chr(10).join(tree)}
```

## 3. Superpowers workflow

One chat per story. `/arfd-*` are board wrappers; `/brainstorming`, `/using-git-worktrees`, `/writing-plans`, `/test-driven-development`, `/subagent-driven-development`, `/verification-before-completion`, `/requesting-code-review`, and `/finishing-a-development-branch` are Superpowers natives.

{wf_table(wf_rows)}

## 4. Project skills (`arfd-` = Airlines Reference Data)

See `Milestone_01.md` section 4 for the full `/arfd-*` command table. Same skills apply here.

## 5. Notes

- Hard gate: open `[Story]` + GitHub Milestone + `/arfd-story-start N` before product code.
- Run milestones in order; do not start the next milestone until this one is complete (or explicitly parallelized by the team).
"""
        write_milestone(ISSUES_DIR / file_name, content)
        print(f"Wrote {file_name} epic=#{e}")

    create_ms(
        "Milestone_02.md",
        "M02 — Local platform bootstrap (ARFD)",
        "M02 - Runtime bootstrap",
        "Lifecycle scripts and containerized platform services (database, streaming, messaging, orchestration, object storage) for development and CI environments.",
        "area:cicd-local",
        "M02-0001",
        "Runtime bootstrap",
        [
            {
                "key": "M02-0002",
                "title": "Lifecycle control scripts",
                "stories": [
                    {
                        "key": "M02-0003",
                        "title": "docker-all-up.sh",
                        "acceptance": ["Script starts the composed services in dependency order", "Documented usage in CICD/Local README"],
                        "brainstorm": "design docker-all-up.sh to start the ARFD platform services in order",
                        "branch": "m02-0003-docker-all-up",
                        "why": "Bring the stack up",
                    },
                    {
                        "key": "M02-0004",
                        "title": "all-down.sh",
                        "acceptance": ["Script stops the composed services cleanly", "Documented usage"],
                        "brainstorm": "design all-down.sh teardown behavior for ARFD services",
                        "branch": "m02-0004-all-down",
                        "why": "Tear the stack down",
                    },
                    {
                        "key": "M02-0005",
                        "title": "all-status.sh",
                        "acceptance": ["Script reports health for each required service", "Non-zero exit when unhealthy"],
                        "brainstorm": "design all-status.sh health probes for ARFD services",
                        "branch": "m02-0005-all-status",
                        "why": "Operator visibility",
                    },
                ],
            },
            {
                "key": "M02-0006",
                "title": "Platform compose services",
                "stories": [
                    {
                        "key": "M02-0007",
                        "title": "Operational database with CDC-ready configuration",
                        "acceptance": ["Database service defined", "CDC prerequisites documented", "Seed reference data available"],
                        "brainstorm": "define operational database service and CDC prerequisites for ARFD",
                        "branch": "m02-0007-operational-database",
                        "why": "Source of reference data",
                    },
                    {
                        "key": "M02-0008",
                        "title": "Streaming and CDC connector compose",
                        "acceptance": ["Streaming cluster defined under CICD/Local/Kafka", "CDC connector service defined"],
                        "brainstorm": "define streaming and CDC connector compose for ARFD",
                        "branch": "m02-0008-streaming-cdc-compose",
                        "why": "CDC path",
                    },
                    {
                        "key": "M02-0009",
                        "title": "Messaging broker for APIs and portals",
                        "acceptance": ["Broker service defined", "Credentials documented for Middleware"],
                        "brainstorm": "define messaging broker service for ARFD APIs and portals",
                        "branch": "m02-0009-messaging-broker",
                        "why": "Async messaging",
                    },
                    {
                        "key": "M02-0010",
                        "title": "Orchestration runtime with Middleware/DAGs mount",
                        "acceptance": ["Orchestration service defined", "Middleware/DAGs mounted by relative path"],
                        "brainstorm": "define orchestration runtime and DAG mount path for ARFD",
                        "branch": "m02-0010-orchestration-dags-mount",
                        "why": "Batch apply home",
                    },
                    {
                        "key": "M02-0011",
                        "title": "S3-compatible object storage for the lake",
                        "acceptance": ["Object storage service defined", "Bucket/prefix conventions documented"],
                        "brainstorm": "define S3-compatible object storage for the ARFD lake",
                        "branch": "m02-0011-object-storage",
                        "why": "Lake storage",
                    },
                ],
            },
        ],
    )

    create_ms(
        "Milestone_03.md",
        "M03 — CDC to Iceberg local (ARFD)",
        "M03 - CDC to analytics lake",
        "Stream operational reference-data changes into the analytics lake with correct insert/update/delete semantics.",
        "area:cdc",
        "M03-0001",
        "CDC to analytics lake",
        [
            {
                "key": "M03-0002",
                "title": "CDC connector for reference data",
                "stories": [
                    {
                        "key": "M03-0003",
                        "title": "Configure CDC for market_rule",
                        "acceptance": ["Connector captures insert/update/delete for market_rule", "Config checked into repo"],
                        "brainstorm": "configure CDC for market_db.market_rule without locking stack choices in the issue prose",
                        "branch": "m03-0003-cdc-market-rule",
                        "why": "Source capture",
                    },
                    {
                        "key": "M03-0004",
                        "title": "Topic naming and key partitioning strategy",
                        "acceptance": ["Naming documented", "Partition-by-key strategy documented"],
                        "brainstorm": "decide topic naming and key partitioning for ARFD CDC",
                        "branch": "m03-0004-topic-partitioning",
                        "why": "Ordering and scale",
                        "docs_only": True,
                    },
                ],
            },
            {
                "key": "M03-0005",
                "title": "Batch apply to the lake",
                "stories": [
                    {
                        "key": "M03-0006",
                        "title": "Batch consumer job under Middleware/DAGs",
                        "acceptance": ["Job consumes CDC batches", "Mounted from Middleware/DAGs"],
                        "brainstorm": "design batch consumer job under Middleware/DAGs for ARFD CDC",
                        "branch": "m03-0006-batch-consumer-dag",
                        "why": "Apply path",
                    },
                    {
                        "key": "M03-0007",
                        "title": "Map CDC operations to lake insert/update/delete",
                        "acceptance": ["Insert/update/delete semantics verified on a unique key"],
                        "brainstorm": "map CDC operations to lake row semantics for ARFD",
                        "branch": "m03-0007-cdc-op-mapping",
                        "why": "Correctness",
                    },
                    {
                        "key": "M03-0008",
                        "title": "Write and validate lake tables",
                        "acceptance": ["Tables written to object storage", "Validation query path documented"],
                        "brainstorm": "write and validate ARFD lake tables after CDC apply",
                        "branch": "m03-0008-write-validate-lake",
                        "why": "Prove end to end",
                    },
                ],
            },
        ],
    )

    create_ms(
        "Milestone_04.md",
        "M04 — Middleware (ARFD)",
        "M04 - Middleware",
        "API services for portals and stable DAG packaging for the orchestration runtime.",
        "area:middleware",
        "M04-0001",
        "Middleware",
        [
            {
                "key": "M04-0002",
                "title": "API Services",
                "stories": [
                    {
                        "key": "M04-0003",
                        "title": "API service skeleton (health, config, OpenAPI)",
                        "acceptance": ["Health endpoint", "Config loading", "OpenAPI published"],
                        "brainstorm": "scaffold Middleware/API-Services with health, config, OpenAPI",
                        "branch": "m04-0003-api-skeleton",
                        "why": "API foundation",
                    },
                    {
                        "key": "M04-0004",
                        "title": "Reference-data write APIs for Admin",
                        "acceptance": ["Create/update/deactivate paths for market rules", "Tests for happy path"],
                        "brainstorm": "design RefData write APIs for Airlines-RD-Admin",
                        "branch": "m04-0004-refdata-write-apis",
                        "why": "Admin needs writes",
                    },
                    {
                        "key": "M04-0005",
                        "title": "Lake read / query façade for Intelligence",
                        "acceptance": ["Read APIs for lake-backed RefData", "Tests for happy path"],
                        "brainstorm": "design lake read/query façade APIs for Airlines-RD-Intelligence",
                        "branch": "m04-0005-lake-read-apis",
                        "why": "Intelligence needs reads",
                    },
                    {
                        "key": "M04-0006",
                        "title": "Async messaging integration",
                        "acceptance": ["Publish/consume path for at least one notification or job"],
                        "brainstorm": "integrate async messaging for ARFD middleware",
                        "branch": "m04-0006-async-messaging",
                        "why": "Decouple portal/API work",
                    },
                ],
            },
            {
                "key": "M04-0007",
                "title": "DAG packaging",
                "stories": [
                    {
                        "key": "M04-0008",
                        "title": "Document Middleware/DAGs mount contract",
                        "acceptance": ["Relative mount path documented for orchestration container"],
                        "brainstorm": "document Middleware/DAGs relative mount contract",
                        "branch": "m04-0008-dags-mount-contract",
                        "why": "Stable path",
                        "docs_only": True,
                    },
                    {
                        "key": "M04-0009",
                        "title": "Shared CDC parse and lake writer libraries",
                        "acceptance": ["Shared libs used by DAGs", "Unit tests for parse/mapping"],
                        "brainstorm": "extract shared CDC parse and lake writer libraries for ARFD DAGs",
                        "branch": "m04-0009-shared-cdc-lake-libs",
                        "why": "Reuse across jobs",
                    },
                ],
            },
        ],
    )

    create_ms(
        "Milestone_05.md",
        "M05 — Airlines-RD-Admin (ARFD)",
        "M05 - Airlines-RD-Admin",
        "Reference Data Admin portal for operators who manage source reference data.",
        "area:portal-admin",
        "M05-0001",
        "Airlines-RD-Admin",
        [
            {
                "key": "M05-0002",
                "title": "Admin portal application",
                "stories": [
                    {
                        "key": "M05-0003",
                        "title": "App shell and auth stub",
                        "acceptance": ["App boots", "Auth stub documented"],
                        "brainstorm": "scaffold Airlines-RD-Admin app shell and auth stub",
                        "branch": "m05-0003-admin-app-shell",
                        "why": "Portal foundation",
                    },
                    {
                        "key": "M05-0004",
                        "title": "Market rules management UI",
                        "acceptance": ["List/create/update/deactivate market rules"],
                        "brainstorm": "build market rules management UI for RD Admin",
                        "branch": "m05-0004-market-rules-ui",
                        "why": "Core admin job",
                    },
                    {
                        "key": "M05-0005",
                        "title": "Pipeline health summary view",
                        "acceptance": ["Shows CDC/pipeline health summary from APIs"],
                        "brainstorm": "add pipeline health summary view to RD Admin",
                        "branch": "m05-0005-pipeline-health-view",
                        "why": "Ops visibility",
                    },
                    {
                        "key": "M05-0006",
                        "title": "Wire Admin portal to Middleware/API-Services",
                        "acceptance": ["UI calls Middleware APIs end to end"],
                        "brainstorm": "wire Airlines-RD-Admin to Middleware/API-Services",
                        "branch": "m05-0006-admin-api-wire",
                        "why": "End-to-end admin path",
                    },
                ],
            },
        ],
    )

    create_ms(
        "Milestone_06.md",
        "M06 — Airlines-RD-Intelligence (ARFD)",
        "M06 - Airlines-RD-Intelligence",
        "Intelligence portal for analysts, risk managers, and data managers to view and query lake-backed reference data.",
        "area:portal-intel",
        "M06-0001",
        "Airlines-RD-Intelligence",
        [
            {
                "key": "M06-0002",
                "title": "Intelligence portal application",
                "stories": [
                    {
                        "key": "M06-0003",
                        "title": "App shell and role-oriented navigation",
                        "acceptance": ["Nav supports analyst / risk / data manager personas"],
                        "brainstorm": "scaffold Airlines-RD-Intelligence shell and role-oriented nav",
                        "branch": "m06-0003-intel-app-shell",
                        "why": "Portal foundation",
                    },
                    {
                        "key": "M06-0004",
                        "title": "Browse and filter reference data",
                        "acceptance": ["Users can browse and filter lake-backed RefData"],
                        "brainstorm": "build browse/filter experience for RD Intelligence",
                        "branch": "m06-0004-browse-filter-refdata",
                        "why": "Primary read path",
                    },
                    {
                        "key": "M06-0005",
                        "title": "Query and saved views",
                        "acceptance": ["Query or saved-view scope agreed in brainstorm and implemented"],
                        "brainstorm": "define and implement query/saved views for RD Intelligence",
                        "branch": "m06-0005-query-saved-views",
                        "why": "Analyst workflows",
                    },
                    {
                        "key": "M06-0006",
                        "title": "Wire Intelligence portal to Middleware/API-Services",
                        "acceptance": ["UI calls Middleware read APIs end to end"],
                        "brainstorm": "wire Airlines-RD-Intelligence to Middleware/API-Services",
                        "branch": "m06-0006-intel-api-wire",
                        "why": "End-to-end intelligence path",
                    },
                ],
            },
        ],
    )

    create_ms(
        "Milestone_07.md",
        "M07 — AWS cloud parity (ARFD)",
        "M07 - AWS deployment",
        "Deploy the same CDC → stream → apply → lake pattern using AWS native and managed services. Start only with explicit go-ahead.",
        "area:aws",
        "M07-0001",
        "AWS deployment",
        [
            {
                "key": "M07-0002",
                "title": "Infrastructure as code and cutover",
                "stories": [
                    {
                        "key": "M07-0003",
                        "title": "Parameterized CloudFormation for the managed path",
                        "acceptance": ["Template parameterized for ARFD", "No deploy without approval"],
                        "brainstorm": "parameterize CloudFormation for ARFD AWS managed path",
                        "branch": "m07-0003-cfn-parameterized",
                        "why": "IaC",
                    },
                    {
                        "key": "M07-0004",
                        "title": "Application-stack to AWS cutover runbook",
                        "acceptance": ["Runbook maps application stack roles to AWS services"],
                        "brainstorm": "write cutover runbook from application stack to AWS managed services",
                        "branch": "m07-0004-cutover-runbook",
                        "why": "Operations",
                        "docs_only": True,
                    },
                    {
                        "key": "M07-0005",
                        "title": "Monitoring and cleanup procedures",
                        "acceptance": ["Monitoring checklist", "Cleanup order documented"],
                        "brainstorm": "define monitoring and cleanup procedures for ARFD on AWS",
                        "branch": "m07-0005-monitoring-cleanup",
                        "why": "Operate safely",
                        "docs_only": True,
                    },
                ],
            },
        ],
    )

    # Index + policy
    (ROOT / "docs" / "Project_Management" / "MILESTONE_POLICY.md").write_text(
        textwrap.dedent(
            """\
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
            """
        ),
        encoding="utf-8",
    )

    index = ISSUES_DIR / "README.md"
    index.write_text(
        textwrap.dedent(
            """\
            # ARFD milestone boards

            One markdown file per GitHub Milestone, same layout as the Consumer Complaints Agentic App boards:

            | File | GitHub Milestone |
            |---|---|
            | [Milestone_01.md](Milestone_01.md) | M01 — Foundation & Superpowers |
            | [Milestone_02.md](Milestone_02.md) | M02 — Runtime bootstrap |
            | [Milestone_03.md](Milestone_03.md) | M03 — CDC to analytics lake |
            | [Milestone_04.md](Milestone_04.md) | M04 — Middleware |
            | [Milestone_05.md](Milestone_05.md) | M05 — Airlines-RD-Admin |
            | [Milestone_06.md](Milestone_06.md) | M06 — Airlines-RD-Intelligence |
            | [Milestone_07.md](Milestone_07.md) | M07 — AWS deployment |

            Run stories with `/arfd-story-start N` then Superpowers natives, logging progress with `/arfd-milestone-log N`.
            """
        ),
        encoding="utf-8",
    )

    print("Done. Issue count:", run(["gh", "issue", "list", "--limit", "200", "--json", "number", "--jq", "length"]))


if __name__ == "__main__":
    main()
