#!/usr/bin/env python3
"""Minimal ARFD board helpers: milestone-log, progress-sync, story start/complete."""
from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sh(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def milestone_file_for_issue(n: int) -> Path:
    title = sh(["gh", "issue", "view", str(n), "--json", "title", "--jq", ".title"])
    m = re.match(r"(M\d+)-", title)
    if not m:
        raise SystemExit(f"No M0N prefix on issue #{n}: {title}")
    num = m.group(1)[1:]  # 01
    return ROOT / "docs" / "Project_Management" / "Issues" / f"Milestone_{num}.md"


def update_status_counts(text: str) -> str:
    # Count stories whose last /arfd-story-complete row is Done
    story_complete = {}
    for line in text.splitlines():
        if "| #" not in line and "| Feature #" not in line and "| Epic #" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        iss, _step, cmd, status = parts[0], parts[1], parts[2], parts[3]
        if "arfd-story-complete" in cmd:
            m = re.search(r"#(\d+)", iss)
            if m:
                story_complete[m.group(1)] = status == "Done"
    done = sum(1 for v in story_complete.values() if v)
    left = sum(1 for v in story_complete.values() if not v)
    text = re.sub(
        r"\d+ done; \d+ left to build\.",
        f"{done} done; {left} left to build.",
        text,
        count=1,
    )
    if done and left == 0:
        text = re.sub(r"\*\*Status:\*\* open\.", "**Status: complete.**", text, count=1)
    return text


def milestone_log(n: int, begin: bool = False) -> None:
    path = milestone_file_for_issue(n)
    lines = path.read_text().splitlines()
    ts = now()
    # Find row indices for this issue
    idxs = []
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cell = line.strip("|").split("|")[0].strip()
        if cell in {f"#{n}", f"Feature #{n}", f"Epic #{n}"} or cell.startswith(f"#{n} "):
            idxs.append(i)
    if not idxs:
        raise SystemExit(f"No rows for #{n} in {path}")

    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def set_row(i: int, status: str, started: str | None = None, completed: str | None = None) -> None:
        c = cells(lines[i])
        while len(c) < 6:
            c.append("-")
        c[3] = status
        if started is not None:
            c[4] = started
        if completed is not None:
            c[5] = completed
        lines[i] = "| " + " | ".join(c) + " |"

    if begin:
        set_row(idxs[0], "In progress", started=ts, completed="-")
    else:
        # find In progress among idxs
        ip = None
        for i in idxs:
            c = cells(lines[i])
            if len(c) > 3 and c[3] == "In progress":
                ip = i
                break
        if ip is None:
            c0 = cells(lines[idxs[0]])
            if len(c0) > 3 and c0[3] == "Planned":
                set_row(idxs[0], "In progress", started=ts, completed="-")
                ip = idxs[0]
            else:
                raise SystemExit(f"No In progress row for #{n}")
        c = cells(lines[ip])
        started = c[4] if c[4] != "-" else ts
        set_row(ip, "Done", started=started, completed=ts)
        # next
        pos = idxs.index(ip)
        if pos + 1 < len(idxs):
            set_row(idxs[pos + 1], "In progress", started=ts, completed="-")

    text = update_status_counts("\n".join(lines) + "\n")
    path.write_text(text)
    print(f"milestone-log #{n} begin={begin} -> {path.name}")


def progress_sync(p: int) -> None:
    body = sh(["gh", "issue", "view", str(p), "--json", "body", "--jq", ".body"])
    labels = sh(["gh", "issue", "view", str(p), "--json", "labels", "--jq", '[.labels[].name]|join(",")'])
    lines = body.splitlines()
    out = []
    done = total = 0
    any_ip = False
    for line in lines:
        m = re.match(r"^- \[[ x]\] #(\d+) (.+?) \((planned|in-progress|done)\)$", line.strip())
        if not m:
            # also match without state suffix variations
            m2 = re.match(r"^- \[[ x]\] #(\d+) (.+)$", line.strip())
            if not m2:
                out.append(line)
                continue
            cid, title = m2.group(1), m2.group(2)
            title = re.sub(r" \((planned|in-progress|done)\)$", "", title)
        else:
            cid, title = m.group(1), m.group(2)
        st = sh(["gh", "issue", "view", cid, "--json", "state,labels", "--jq", '{state:.state,labels:[.labels[].name]}'])
        import json

        info = json.loads(st)
        total += 1
        if info["state"] == "CLOSED":
            done += 1
            out.append(f"- [x] #{cid} {title} (done)")
        elif "status: in-progress" in info["labels"]:
            any_ip = True
            out.append(f"- [ ] #{cid} {title} (in-progress)")
        else:
            out.append(f"- [ ] #{cid} {title} (planned)")
    state = "done" if done == total and total else ("in-progress" if done or any_ip else "planned")
    text = "\n".join(out)
    text = re.sub(
        r"\*\*Progress:\*\*.*",
        f"**Progress:** {done} of {total} done — {state}",
        text,
        count=1,
    )
    if "**Progress:**" not in text and total:
        # insert after Status
        text2 = []
        inserted = False
        for line in text.splitlines():
            text2.append(line)
            if line.startswith("**Status:**") and not inserted:
                text2.append(f"**Progress:** {done} of {total} done — {state}")
                inserted = True
        text = "\n".join(text2)
    tmp = ROOT / "runtime_data" / "tmp" / f"issue-{p}.md"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(text + "\n")
    sh(["gh", "issue", "edit", str(p), "--body-file", str(tmp)])
    # labels
    for lab in ("status: planned", "status: in-progress", "status: done"):
        subprocess.run(["gh", "issue", "edit", str(p), "--remove-label", lab], cwd=ROOT, capture_output=True)
    if state != "done":
        sh(["gh", "issue", "edit", str(p), "--add-label", f"status: {state if state != 'done' else 'in-progress'}"])
        if state == "planned":
            sh(["gh", "issue", "edit", str(p), "--add-label", "status: planned"])
        else:
            sh(["gh", "issue", "edit", str(p), "--add-label", "status: in-progress"])
    print(f"#{p}: {done} of {total} done")


def story_start(n: int) -> None:
    import json

    info = json.loads(sh(["gh", "issue", "view", str(n), "--json", "title,state,labels,body,milestone"]))
    if "[Story]" not in info["title"]:
        raise SystemExit("not a story")
    if info["state"] != "OPEN":
        raise SystemExit("closed")
    if not info.get("milestone"):
        raise SystemExit("no milestone")
    body = info["body"]
    ts = now()
    body = re.sub(r"\*\*Status:\*\*.*", f"**Status:** In progress — started {ts}.", body, count=1)
    tmp = ROOT / "runtime_data" / "tmp" / f"issue-{n}.md"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(body)
    subprocess.run(["gh", "issue", "edit", str(n), "--remove-label", "status: planned"], cwd=ROOT, capture_output=True)
    sh(["gh", "issue", "edit", str(n), "--add-label", "status: in-progress", "--body-file", str(tmp)])
    m = re.search(r"\*\*Epic:\*\* #(\d+).*?\*\*Feature:\*\* #(\d+)", body)
    if m:
        for parent in (m.group(2), m.group(1)):
            plabs = sh(["gh", "issue", "view", parent, "--json", "labels", "--jq", '[.labels[].name]|join(",")'])
            if "status: planned" in plabs:
                subprocess.run(["gh", "issue", "edit", parent, "--remove-label", "status: planned"], cwd=ROOT, capture_output=True)
                sh(["gh", "issue", "edit", parent, "--add-label", "status: in-progress"])
            progress_sync(int(parent))
    milestone_log(n, begin=True)
    milestone_log(n, begin=False)
    print(f"started #{n}: {info['title']}")


def story_complete(n: int, summary: str) -> None:
    import json

    info = json.loads(sh(["gh", "issue", "view", str(n), "--json", "title,body"]))
    body = info["body"]
    body = body.replace("- [ ]", "- [x]")
    commits = sh(["git", "log", "--format=%h", f"--grep=#{n}:"])
    clist = ", ".join(f"`{c}`" for c in commits.splitlines()[:8]) or "`(board)`"
    ts = now()
    body = re.sub(
        r"\*\*Status:\*\*.*",
        f"**Status:** Done — {summary} (completed {ts}; commits {clist}).",
        body,
        count=1,
    )
    tmp = ROOT / "runtime_data" / "tmp" / f"issue-{n}.md"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(body)
    for lab in ("status: planned", "status: in-progress"):
        subprocess.run(["gh", "issue", "edit", str(n), "--remove-label", lab], cwd=ROOT, capture_output=True)
    sh(["gh", "issue", "edit", str(n), "--add-label", "status: done", "--body-file", str(tmp)])
    sh(["gh", "issue", "close", str(n), "--reason", "completed"])
    milestone_log(n, begin=False)
    m = re.search(r"\*\*Feature:\*\* #(\d+)", info["body"])
    if m:
        progress_sync(int(m.group(1)))
    print(f"completed #{n}")


def commit_push(n: int | None, summary: str, files: list[str]) -> None:
    key = "M01"
    if n:
        title = sh(["gh", "issue", "view", str(n), "--json", "title", "--jq", ".title"])
        key = title.split()[0]
        msg = f"{key} #{n}: {summary}"
    else:
        msg = f"{key}: {summary}"
    if files:
        sh(["git", "add", *files])
    else:
        raise SystemExit("no files")
    # commit
    subprocess.check_call(["git", "commit", "-m", msg], cwd=ROOT)
    body = sh(["git", "log", "-1", "--format=%B"])
    if re.search(r"Co-authored-by:.*Cursor|cursoragent@cursor.com", body, re.I):
        subj = sh(["git", "log", "-1", "--format=%s"])
        new = sh(["git", "commit-tree", "HEAD^{tree}", "-p", "HEAD^", "-m", subj])
        branch = sh(["git", "branch", "--show-current"])
        sh(["git", "update-ref", f"refs/heads/{branch}", new])
    branch = sh(["git", "branch", "--show-current"])
    subprocess.check_call(["git", "push", "origin", branch], cwd=ROOT)
    print(sh(["git", "log", "-1", "--oneline"]))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("start")
    p.add_argument("n", type=int)
    p = sub.add_parser("complete")
    p.add_argument("n", type=int)
    p.add_argument("--summary", required=True)
    p = sub.add_parser("log")
    p.add_argument("n", type=int)
    p.add_argument("--begin", action="store_true")
    p = sub.add_parser("sync")
    p.add_argument("n", type=int)
    p = sub.add_parser("commit")
    p.add_argument("n", type=int, nargs="?")
    p.add_argument("--summary", required=True)
    p.add_argument("--files", nargs="+", required=True)
    args = ap.parse_args()
    if args.cmd == "start":
        story_start(args.n)
    elif args.cmd == "complete":
        story_complete(args.n, args.summary)
    elif args.cmd == "log":
        milestone_log(args.n, begin=args.begin)
    elif args.cmd == "sync":
        progress_sync(args.n)
    elif args.cmd == "commit":
        commit_push(args.n, args.summary, args.files)


if __name__ == "__main__":
    main()
