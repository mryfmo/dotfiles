"""A format-2 task file from one plan 024 todo row, every premise and Check command run (plan 024 programs (12)).

`uv run --offline --with pyyaml python -I scripts/orchestrator/task-from-plan.py <todo-id> [--out <task.md>]
[--seat <identity>] [--worktree <path>]` reads, under the current git toplevel, the row <todo-id> of
.orchestration/plans/024-todo.md, the items of 024-design-programs.md its work column names by (n), the wave row of
the plan's section 6 that names the id (in the --seat column when given) and the Q-A row of 024-design-quality.md
(security: true when it lists the id or a range holding it). It writes --out (default
.orchestration/tasks/<todo-id>.md), runs task-consistency-check.py on it, prints the checker's output and exits 0 when
the checker passes, 1 otherwise (the file stays for editing).
allowed_files: every path the row and its items name in backticks, every file `git grep -l` finds under scripts/
and tests/ for each named script or test (each listed as `# from: <hit>` in the Files section), and the task's own
evidence directory. threat_table: one draft row per path entry (residual: the row's completion), then the task-copy,
evidence, non-path and orchestrator-effect rows of dotfiles-T133-result-precheck-a01.md with its id replaced.
premises: every command the items quote in backticks, run once through the checker's rerun (C14's environment, so
C14 reproduces the pasted stdout); a nonzero exit is pasted as `verify:` with its code, and a gh, curl or URL command
is not run, as C14 skips it. Check: the commands of the Check section of the sibling task file (one whose title names
another todo id of the same wave row), each run once in a detached scratch worktree of origin/main with the caller's
PATH and pasted with its exit code; the worktree is removed with `git worktree remove --force`.
"""

import argparse
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
TEMPLATE_ID = "dotfiles-T133-result-precheck-a01"  # the regime's current wording of the non-path rows
COMPLETION = ".orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md"
NONPATH = (
    "task metadata",
    "metadata separators",
    "in-process effects",
    "workflow and",
    "new or renamed",
    "orchestrator effect",
)
NETWORK = r"\b(?:gh|curl)\b|https?://"
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


def is_command(span, root):
    word = span.split()[0]
    return " " in span and not re.search(r"[<>]", span) and (shutil.which(word) or (root / word).is_file())


def program(lines, n):
    start = next(i for i, l in enumerate(lines) if l.startswith(f"**({n}) "))
    end = next((i for i in range(start + 1, len(lines)) if not lines[i] or lines[i].startswith("**(")), len(lines))
    return " ".join(lines[start:end])


def run_check_commands(root, commands, tid):
    if not commands:
        return []
    parent = pathlib.Path(tempfile.mkdtemp(prefix=f"{tid}."))
    scratch = parent / "origin-main"
    try:
        if git(root, "worktree", "add", "--detach", str(scratch), "origin/main").returncode:
            return [f"- `{c}` # not run: no origin/main worktree" for c in commands]
        try:
            return [
                f"- `{c}` # exit {checker.rerun(c, scratch, os.environ['PATH'])[1]} on origin/main" for c in commands
            ]
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
    read = lambda name: (root / name).read_text().splitlines()  # noqa: E731
    # The plan group, the template and the completion file are regime records a checkout may not hold yet.
    plans = ("todo", "design-programs", "design-quality", "omp-cutover-and-corrective-order")
    needed = [f"{PLANS}/024-{n}.md" for n in plans] + [f".orchestration/tasks/{TEMPLATE_ID}.md", COMPLETION]
    if missing := [n for n in needed if not (root / n).is_file()]:
        sys.exit(f"task-from-plan: missing under {root}: {', '.join(missing)}")
    out = args.out or pathlib.Path(f".orchestration/tasks/{args.todo_id}.md")
    tid, own = out.stem, f".orchestration/{out.stem}/"
    row = next(c for c in rows(read(f"{PLANS}/024-todo.md")) if c[0].split()[0] == args.todo_id)
    title, purpose, work, completion = row[0].split(" ", 1)[-1], row[1], row[2], row[-1]
    items = [program(read(f"{PLANS}/024-design-programs.md"), n) for n in dict.fromkeys(re.findall(r"\((\d+)\)", work))]
    qa = next((c for c in rows(read(f"{PLANS}/024-design-quality.md")) if c[0].startswith("Q-A")), [""])
    listed = " ".join(qa)
    num = re.fullmatch(r"P1-(\d+)", args.todo_id)
    in_range = num and any(int(a) <= int(num[1]) <= int(b) for a, b in re.findall(r"P1-(\d+)〜P1-(\d+)", listed))
    security = bool(re.search(rf"{re.escape(args.todo_id)}(?![\w-])", listed) or in_range)

    names = [s.split()[0] for s in spans(work + " " + " ".join(items))]
    # A path has a file extension or exists, so a ref such as origin/main is not proposed.
    cand = [n.rstrip(".,") for n in names if "/" in n and not n.startswith("-")]
    paths = [n for n in cand if re.fullmatch(r"[\w.@~/-]+", n) and ("." in n.rsplit("/", 1)[-1] or (root / n).exists())]
    hits = {}
    for script in dict.fromkeys(pathlib.Path(n).name for n in names if n.endswith((".sh", ".py"))):
        for hit in git(root, "grep", "-l", "-F", script, "--", "scripts", "tests").stdout.split():
            hits.setdefault(hit, script)
    allowed = list(dict.fromkeys(paths + list(hits))) + [f"{own}**"]

    template = (root / f".orchestration/tasks/{TEMPLATE_ID}.md").read_text()
    rows_out = [{"control": f"{p} ({title})", "disposition": f"residual: {completion}"} for p in allowed[:-1]]
    for r in checker.front(template).get("threat_table") or []:
        if f".orchestration/{TEMPLATE_ID}/" in r["control"] or r["control"].startswith(NONPATH):
            rows_out.append({k: v.replace(TEMPLATE_ID, tid) for k, v in r.items()})

    premises = []
    for cmd in dict.fromkeys(s for s in spans(" ".join(items)) if is_command(s, root)):
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
        claim = f"the program item quotes `{cmd}`" if code == 0 else f"verify: `{cmd}` exits {code}"
        premises.append({"claim": claim, "command": cmd, "output": (stdout or "").rstrip("\n")})

    plan = read(f"{PLANS}/024-omp-cutover-and-corrective-order.md")
    six = plan[next(i for i, l in enumerate(plan) if l.startswith("## 6.")) :]
    six = six[: next((i for i, l in enumerate(six) if l.startswith("## 7.")), len(six))]
    header = next((c for c in rows(six) if c and c[0] == "波"), [])
    col = header.index(args.seat) if args.seat in header else None
    wave = next(
        (c for c in rows(six) if args.todo_id in (c[col] if col is not None and col < len(c) else " ".join(c))), None
    )
    sibling, checks = None, []
    others = [i for i in dict.fromkeys(re.findall(r"\bP1-\d+[a-z]?\b", " ".join(wave or []))) if i != args.todo_id]
    for other in others:
        named = [
            p
            for p in sorted((root / ".orchestration/tasks").glob("*.md"))
            if re.search(rf"^# .*\b{other}\b", p.read_text(), re.M)
        ]
        if named:
            sibling = named[-1]
            text = sibling.read_text()
            body = text.split("\n## Check\n", 1)[1].split("\n## ", 1)[0] if "\n## Check\n" in text else ""
            checks = run_check_commands(root, [s for s in dict.fromkeys(spans(body)) if is_command(s, root)], tid)
            break

    front = {"format": 2, "task_id": tid, "kind": "code", "security": security, "allowed_files": allowed, "after": []}
    front |= {"threat_table": rows_out, "premises": premises}
    files = [f"{n}. {item}" for n, item in enumerate(items, 1)] + [
        f"# from: {h} (git grep -l {s})" for h, s in hits.items()
    ]
    seat = f" Seat: {args.seat or 'unassigned'}" + (f" ({args.worktree})." if args.worktree else ".")
    text = f"""---
{yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=1000)}---

# AGMSG-TASK {tid} — {title} (plan 024 {args.todo_id})

Generated by scripts/orchestrator/task-from-plan.py from `024-todo.md` row {args.todo_id} and its program items; wave {wave[0] if wave else "none"}.{seat} Every premise output is the command's own stdout.

## Goal

{purpose}

## Files

{chr(10).join(files)}

## Out of scope

Everything the todo row {args.todo_id} and its program items do not name.

## Check

{chr(10).join(checks) if checks else f"No sibling task file names another todo id of wave {wave[0] if wave else 'none'}: write the Check and run each command once before dispatch."}
{f"(the Check commands of {sibling.name})" if sibling else ""}

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `{COMPLETION}` applies as written, with `{tid}-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of {own}task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    verdict = subprocess.run(
        [sys.executable, "-I", checker.__file__, "--root", str(root), str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    print(verdict.stdout + verdict.stderr, end="")
    return 0 if verdict.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
