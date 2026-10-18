"""A format-2 task file from one plan 024 todo row, every premise and Check command run (plan 024 programs (12)).

`uv run --offline --with pyyaml python -I scripts/orchestrator/task-from-plan.py <todo-id> [--out <task.md>]
[--seat <identity>] [--worktree <path>]` refuses, before it runs or writes anything, while the
.orchestration/plans/024-* group under the current git toplevel has a staged, unstaged or untracked change. Otherwise it
reads, at the committed revision HEAD (named in the task's opening line), the row <todo-id> of
.orchestration/plans/024-todo.md, the items of 024-design-programs.md its work column names by (n) (each through the
next **(<n>) heading or the end of the file), the wave row of the plan's section 6 whose cell (the --seat column's when
given) holds the whole id <todo-id>, and the Q-A row of 024-design-quality.md (security: true when it lists the id or a
range holding it). task-template.md beside this script supplies the control rows, the common Check commands and the
Completion section; no file under .orchestration/tasks/ is read. It writes --out (default
.orchestration/tasks/<todo-id>.md), runs task-consistency-check.py on it with --premises-sha of the written bytes,
prints the checker's output and exits 0 when the checker passes, 1 otherwise (the file stays for editing).
allowed_files: every path or glob scope the row and its items name in backticks (a literal has a file extension or
exists, inside the checkout), every file `git grep -l -F` finds under scripts/ and tests/ for each named script or test
(each listed as `# from: <hit>` in the Files section), and the task's own evidence directory. threat_table: one draft
row per entry (residual: the row's completion), one per executed or applied file a glob entry matches (C12), then the
template's rows with <task_id> replaced.
A backticked span is a command by its form: its first word is a lowercase name, a / or ./ path, or a .sh or .py path,
and it holds no <placeholder>; a lone word is one only when PATH holds it (a lone path is a scope). premises: every
command the items quote but `make`, run once through the checker's rerun (C14's environment, so C14 reproduces the
pasted stdout); a nonzero exit is pasted as `verify:` with its code, and a gh, curl or URL command is not run, as C14
skips it. Check: the template's commands and the items' `make` commands, each run once in a detached scratch worktree of
origin/main with the caller's PATH and pasted with its exit code, the revision and its last 20 output lines; the
worktree is removed with `git worktree remove --force` and its temporary parent deleted.
"""

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

PLANS = ".orchestration/plans"
TEMPLATE = pathlib.Path(__file__).with_name("task-template.md")
NETWORK = r"\b(?:gh|curl)\b|https?://"
GLOB = r"[*?\[]"
spec = importlib.util.spec_from_file_location("checker", pathlib.Path(__file__).with_name("task-consistency-check.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def rows(lines):
    return [
        [c.strip() for c in l.strip().strip("|").split("|")]
        for l in lines
        if l.startswith("|") and not re.match(r"\|\s*-{3}", l)
    ]


def spans(text):
    return re.findall(r"`([^`\n]+)`", text)


def is_command(span):
    words = span.split() or [""]
    if re.search(r"<[^<>\s]+>", span) or not re.fullmatch(
        r"[a-z][\w.+-]*|\.?\.?/[\w./-]+|[\w./-]+\.(?:sh|py)", words[0]
    ):
        return False
    return len(words) > 1 or ("/" not in words[0] and shutil.which(words[0]) is not None)


def program(lines, n):
    start = next(i for i, l in enumerate(lines) if l.startswith(f"**({n}) "))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"\*\*\(\d+\) ", lines[i])), len(lines))
    return "\n".join(lines[start:end]).strip()


def run_check_commands(root, commands, tid):
    parent = pathlib.Path(tempfile.mkdtemp(prefix=f"{tid}."))
    scratch = parent / "origin-main"
    try:
        if git(root, "worktree", "add", "--detach", str(scratch), "origin/main").returncode:
            return [f"- `{c}`: not run (no origin/main worktree)" for c in commands]
        try:
            rev, out = git(scratch, "rev-parse", "HEAD").stdout.strip(), []
            for c in commands:
                stdout, code, stderr = checker.rerun(c, scratch, os.environ["PATH"])
                tail = ["```", *((stdout or "") + stderr).splitlines()[-20:], "```"]
                out.append(f"- `{c}`: exit {code} on origin/main {rev[:12]}" + "".join(f"\n  {l}" for l in tail))
            return out
        finally:
            git(root, "worktree", "remove", "--force", str(scratch))
    finally:
        shutil.rmtree(parent, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("todo_id")
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--seat", help="the wave table column to read (for example a009)")
    parser.add_argument("--worktree", help="the seat's worktree, named in the task's opening line")
    args = parser.parse_args()
    root = pathlib.Path(git(".", "rev-parse", "--show-toplevel").stdout.strip())
    # The plan's commands are the orchestrator's own text, so they run only as committed.
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all", "--", f":(glob){PLANS}/024-*")
    if status.returncode or status.stdout:
        sys.exit(
            f"task-from-plan: refused: the plan group has uncommitted changes; commit them first:\n{status.stdout}"
        )
    rev = git(root, "rev-parse", "HEAD").stdout.strip()

    def read(name):
        shown = git(root, "show", f"{rev}:{PLANS}/{name}")
        if shown.returncode:
            sys.exit(f"task-from-plan: {PLANS}/{name} is not in the commit {rev}")
        return shown.stdout.splitlines()

    out = args.out or pathlib.Path(f".orchestration/tasks/{args.todo_id}.md")
    tid, own = out.stem, f".orchestration/{out.stem}/"
    template = TEMPLATE.read_text().replace("<task_id>", tid)
    bundled = checker.front(template)
    row = next(c for c in rows(read("024-todo.md")) if c[0].split()[0] == args.todo_id)
    title, purpose, work, completion = row[0].split(" ", 1)[-1], row[1], row[2], row[-1]
    items = [program(read("024-design-programs.md"), n) for n in dict.fromkeys(re.findall(r"\((\d+)\)", work))]
    qa = next((c for c in rows(read("024-design-quality.md")) if c[0].startswith("Q-A")), [""])
    listed = " ".join(qa)
    num = re.fullmatch(r"P1-(\d+)", args.todo_id)
    in_range = num and any(int(a) <= int(num[1]) <= int(b) for a, b in re.findall(r"P1-(\d+)〜P1-(\d+)", listed))
    security = bool(re.search(rf"{re.escape(args.todo_id)}(?![\w-])", listed) or in_range)

    names = [s.split()[0] for s in spans(work + "\n" + "\n".join(items)) if s.split()]
    # A literal has a file extension or exists, so a ref such as origin/main is not proposed; a glob stays a scope.
    cand = [n.rstrip(".,") for n in names if "/" in n and not n.startswith(("-", "~"))]
    paths = [
        n
        for n in cand
        if re.fullmatch(r"[\w.@/*?\[\]-]+", n)
        and checker.confined(root, n)
        and (re.search(GLOB, n) or "." in n.rsplit("/", 1)[-1] or (root / n).exists())
    ]
    hits = {}
    for script in dict.fromkeys(
        pathlib.Path(n).name for n in names if n.endswith((".sh", ".py")) and not re.search(GLOB, n)
    ):
        for hit in git(root, "grep", "-l", "-F", "-e", script, "--", "scripts", "tests").stdout.split():
            hits.setdefault(hit, script)
    allowed = list(dict.fromkeys(paths + list(hits))) + [f"{own}**"]

    rows_out = [{"control": f"{p} ({title})", "disposition": f"residual: {completion}"} for p in allowed[:-1]]
    for g in (a for a in allowed[:-1] if re.search(GLOB, a)):  # C12: every executed or applied file a glob matches
        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){g}").stdout.split("\0")):
            if checker.applied(f) and f not in allowed and not f.startswith("tests/fixtures/"):  # an entry has its row
                rows_out.append({"control": f"{f} (matched by {g})", "disposition": f"residual: {completion}"})
    rows_out += bundled.get("threat_table") or []

    commands = [s for s in dict.fromkeys(spans("\n".join(items))) if is_command(s)]
    premises = []
    for cmd in (c for c in commands if c.split()[0] != "make"):
        if re.search(NETWORK, cmd):
            premises.append(
                {
                    "claim": f"verify: {cmd} is a network command, not run here (C14 skips it)",
                    "command": cmd,
                    "output": "",
                }
            )
            continue
        stdout, code, _ = checker.rerun(cmd, root)
        claim = f"the program item's `{cmd}` exits 0" if code == 0 else f"verify: `{cmd}` exits {code}"
        premises.append({"claim": claim, "command": cmd, "output": (stdout or "").rstrip("\n")})
    makes = [c for c in commands if c.split()[0] == "make"]
    checks = run_check_commands(root, list(dict.fromkeys((bundled.get("check") or []) + makes)), tid)

    plan = read("024-omp-cutover-and-corrective-order.md")
    six = plan[next(i for i, l in enumerate(plan) if l.startswith("## 6.")) :]
    six = six[: next((i for i, l in enumerate(six) if l.startswith("## 7.")), len(six))]
    header = next((c for c in rows(six) if c and c[0] == "波"), [])
    col = header.index(args.seat) if args.seat in header else None
    whole = re.compile(rf"(?<![\w-]){re.escape(args.todo_id)}(?![\w-])")
    wave = next(
        (c for c in rows(six) if whole.search(c[col] if col is not None and col < len(c) else " ".join(c))), None
    )

    front = {"format": 2, "task_id": tid, "kind": "code", "security": security, "allowed_files": allowed, "after": []}
    front |= {"threat_table": rows_out, "premises": premises}
    files = [f"{n}. {item}" for n, item in enumerate(items, 1)] + [
        f"# from: {h} (git grep -l {s})" for h, s in hits.items()
    ]
    seat = f"seat {args.seat or 'unassigned'}" + (f", worktree {args.worktree}" if args.worktree else "")
    text = f"""---
{yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)}---

# AGMSG-TASK {tid} — {title} (plan 024 {args.todo_id})

Generated by scripts/orchestrator/task-from-plan.py from `024-todo.md` row {args.todo_id} and its program items, read from the plan group at {rev}; wave {wave[0] if wave else "none"} ({seat}). Every premise output is the command's own stdout.

## Goal

{purpose}

## Files

{chr(10).join(files)}

## Out of scope

Everything the todo row {args.todo_id} and its program items do not name.

## Check

{chr(10).join(checks)}

## Completion

{template.split(chr(10) + "## Completion" + chr(10), 1)[1].strip()}

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    # The generator's own text, whose premises it has just run itself, is the trusted text C14 reruns.
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    verdict = subprocess.run(
        [sys.executable, "-I", checker.__file__, "--root", str(root), "--premises-sha", sha, str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    print(verdict.stdout + verdict.stderr, end="")
    return 0 if verdict.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
