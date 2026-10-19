"""Generate a format-2 task skeleton from committed plan data and the bundled template.

Commands remain unverified text; no plan or Check command executes. The generated file is exclusively created
under .orchestration/tasks and receives a structural check without premise authority.
"""

import argparse
import importlib.util
import os
import pathlib
import re
import shutil
import sys

PLANS = ".orchestration/plans"
TEMPLATE = pathlib.Path(__file__).with_name("task-template.md")
NETWORK = r"\b(?:gh|curl)\b|https?://"
GLOB = r"[*?\[]"
helper = pathlib.Path(__file__).resolve().with_name("task-consistency-check.py").resolve()
if not os.path.samefile(helper.parent, pathlib.Path(__file__).resolve().parent):
    sys.exit("refused: checker outside the trusted script directory")
helper_data = helper.read_bytes()
spec = importlib.util.spec_from_file_location("checker", helper)
checker = importlib.util.module_from_spec(spec)
spec.loader.get_code = lambda _: compile(helper_data, str(helper), "exec")
spec.loader.exec_module(checker)
normalise_name = checker.normalise_name

import yaml


def git(root, *args):
    return checker.git(root, *args)


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
    return len(words) > 1 or ("/" not in normalise_name(words[0]) and shutil.which(words[0]) is not None)


def program(lines, n):
    start = next(i for i, l in enumerate(lines) if l.startswith(f"**({n}) "))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"\*\*\(\d+\) ", lines[i])), len(lines))
    return "\n".join(lines[start:end]).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("todo_id")
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--seat", help="the wave table column to read (for example a009)")
    parser.add_argument("--worktree", help="the seat's worktree, named in the task's opening line")
    args = parser.parse_args()
    root = checker.repository(".")
    # A clean committed plan binds provenance, not permission to execute its text.
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
    binding = checker.snapshot(TEMPLATE)
    try:
        template = checker.consume(binding).read_text().replace("<task_id>", tid)
    finally:
        binding[0].unlink()
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
    cand = [n.rstrip(".,") for n in names if "/" in normalise_name(n) and not normalise_name(n).startswith(("-", "~"))]
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
            if checker.applied(f) and f not in allowed and not normalise_name(f).startswith("tests/fixtures/"):
                rows_out.append({"control": f"{f} (matched by {g})", "disposition": f"residual: {completion}"})
    rows_out += bundled.get("threat_table") or []

    commands = [s for s in dict.fromkeys(spans("\n".join(items))) if is_command(s)]
    premises = [
        {"claim": f"verify: execution and verification pending: {cmd}", "command": cmd}
        for cmd in commands
        if cmd.split()[0] != "make"
    ]
    makes = [c for c in commands if c.split()[0] == "make"]
    checks = [
        f"- `{c}`: verify: not run; execution and verification pending"
        for c in dict.fromkeys((bundled.get("check") or []) + makes)
    ]

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

Generated by scripts/orchestrator/task-from-plan.py from `024-todo.md` row {args.todo_id} and its program items, read from the plan group at {rev}; wave {wave[0] if wave else "none"} ({seat}). Commands and Check observations are unverified; no output has been observed.

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
    directory = (root / ".orchestration/tasks").resolve()
    destination = out if out.is_absolute() else root / out
    if (
        not directory.is_relative_to(root)
        or not destination.resolve().is_relative_to(directory)
        or destination.is_symlink()
    ):
        sys.exit("refused: output must be a new confined file under .orchestration/tasks")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        sys.exit("refused: output already exists")
    with os.fdopen(fd, "w") as stream:
        stream.write(text)
    binding = checker.snapshot(checker.__file__, checker.hashlib.sha256(helper_data).digest())
    try:
        verdict = checker.launch(
            root,
            checker.executable("uv"),
            "run",
            "--no-config",
            "--no-project",
            "--offline",
            "--python",
            checker.PYTHON,
            "--with",
            "pyyaml",
            "python",
            "-I",
            checker.consume(binding),
            "--root",
            root,
            destination,
        )
    finally:
        binding[0].unlink()
    print(verdict.stdout + verdict.stderr, end="")
    return int(verdict.returncode != 0)


if __name__ == "__main__":
    sys.exit(main())
