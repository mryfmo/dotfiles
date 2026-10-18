"""Check a pull request against its task copies: the regime CI job (plan 024 P1-11, programs item (6)).

`uv run --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha> [--root <dir>]`
takes the tasks whose `.orchestration/<t>/` directory the diff `<base>...<head>` touches and that carry a `task.md` copy
at `<head>`, and checks each one:

- the copy passes the tracked task-consistency checker, run as a subprocess from the checkout at `<head>`;
- the copy equals the dispatched `.orchestration/tasks/<t>.md`, or else result.txt's `task_copy=`;
- `precheck.json` is bound to the head, and its sha256 to result.txt's `precheck=`;
- every changed path is inside `allowed_files`;
- the changed lines stay within the caps of the copy's `## Check` sentence.

Output is one `regime-ci: <t>: <rule>: <detail>` line per violation and `regime-ci: warning: <t>: <detail>` lines.
It exits 1 on any violation, else prints `regime-ci: ok <n> task(s)`. A diff without a task copy passes as
`no target (records-only)` only when every path is under `.orchestration/` or the head branch is `orchestration/*`.

Pull-request content is read as data only (git show, yaml.safe_load, json). The one program run from the checkout is
the tracked checker, and a pull request that edits it shows the edit in its own diff.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    print("regime-ci: needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

CHECKER = "scripts/orchestrator/task-consistency-check.py"
CHECKER_RUN = ["uv", "run", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)


def show(root, head, path):
    """Return the bytes of path at head, or None when head has no such file."""
    out = git(root, "show", f"{head}:{path}")
    return out.stdout if out.returncode == 0 else None


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def token(text, name):
    m = re.search(rf"(?:^|\s){name}=(\S+)", text)
    return m.group(1) if m else None


def allowed(path, entry):
    """Match an allowed_files entry: `<dir>/**` takes its prefix, `*` and `?` stay within one path segment."""
    if entry.endswith("/**"):
        return path.startswith(entry[:-2])
    rx = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in entry)
    return re.fullmatch(rx, path) is not None


def caps(text, numstat):
    """Return (violations, warnings) for the `## Check` sentence's caps against the numstat rows."""
    check = text.split("\n## Check", 1)[1].split("\n## ", 1)[0] if "\n## Check" in text else ""
    outside = re.search(r"at most (\d+) changed lines outside ([^(\n]*)", check)
    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    if not outside and not tests:
        return [], ["no cap sentence in the copy's ## Check section"]
    excluded = ["tests/", ".orchestration/"]
    if outside:
        excluded = re.findall(r"`([^`]+)`", re.split(r",\s*(?:and\s+)?\d", outside.group(2))[0]) or excluded

    def counted(path, prefixes):
        return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)

    out_lines = sum(a + d for a, d, p in numstat if not counted(p, excluded))
    test_lines = sum(a + d for a, d, p in numstat if counted(p, ["tests/"]))
    found = []
    if outside and out_lines > int(outside.group(1)):
        found.append(f"{out_lines} changed lines outside {', '.join(excluded)} exceed {outside.group(1)}")
    if tests and test_lines > int(tests.group(1)):
        found.append(f"{test_lines} changed lines under tests/ exceed {tests.group(1)}")
    return found, []


def precheck(root, head, t, changed, result_text):
    """Return the violations of precheck.json's binding, or None when the task carries no precheck.json."""
    data = show(root, head, f".orchestration/{t}/precheck.json")
    if data is None:
        return None
    try:
        doc = json.loads(data)
    except ValueError as error:
        return [f"precheck.json is not JSON: {error}"]
    found = []
    bound = doc.get("head") if isinstance(doc, dict) else None
    resolved = git(root, "rev-parse", "--verify", "--quiet", f"{bound}^{{commit}}").stdout.decode().strip()
    if bound and resolved != head:
        # precheck.json cannot name the commit that adds it: it names the code commit, and the head may add only
        # this task's evidence on top (the evidence-only ancestor rule of verdict.sh condition 1)
        own = [p for p in changed if not p.startswith(f".orchestration/{t}/")]
        if not resolved or git(root, "merge-base", "--is-ancestor", resolved, head).returncode:
            found.append(f"precheck.json head {bound} is neither the head {head} nor its ancestor")
        elif own and (moved := git(root, "diff", "--name-only", "-z", resolved, head, "--", *own).stdout.decode()):
            found.append(
                f"precheck.json head {bound[:12]} differs from the head in {', '.join(filter(None, moved.split(chr(0))))}"
            )
    elif not bound:
        found.append("precheck.json names no head")
    if token(result_text, "precheck") != sha256(data):
        found.append(
            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
        )
    return found


def check_task(root, head, t, changed, numstat):
    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
    copy_path = f".orchestration/{t}/task.md"
    copy = show(root, head, copy_path)
    try:
        text = copy.decode()
        fm = yaml.safe_load(text.split("\n---\n", 1)[0].lstrip("-\n"))
    except (UnicodeDecodeError, yaml.YAMLError) as error:
        return [("front-matter", f"{copy_path} is unreadable: {error}")], []
    if not isinstance(fm, dict):
        return [("front-matter", f"{copy_path} has no front matter mapping")], []
    found, warnings = [], []
    if fm.get("task_id") != t:
        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
    run = subprocess.run(
        [*CHECKER_RUN, "--root", root, copy_path], cwd=root, capture_output=True, text=True, check=False
    )
    # the copy is named task.md, so the checker's C1 compares task_id with `task`; task-id above checks the directory
    lines = [
        ln.strip() for ln in run.stdout.splitlines()[1:] if ln.strip() and ln.strip() != f"C1 task_id {t} != file task"
    ]
    found += [("checker", ln) for ln in lines]
    if run.returncode not in (0, 1):
        found.append(("checker", f"exit {run.returncode}: {(run.stdout + run.stderr).strip()[-300:]}"))
    dispatched = show(root, head, f".orchestration/tasks/{t}.md")
    result = show(root, head, f".orchestration/{t}/result.txt")
    result_text = result.decode(errors="replace") if result is not None else ""
    if dispatched is not None:
        if dispatched != copy:
            found.append(("task-copy", f"{copy_path} differs from the dispatched .orchestration/tasks/{t}.md"))
    elif result is not None:
        if token(result_text, "task_copy") != sha256(copy):
            found.append(
                ("task-copy", f"sha256 {sha256(copy)} is not result.txt's task_copy={token(result_text, 'task_copy')}")
            )
    else:
        warnings.append("task copy unverifiable (no dispatched text at head, no result.txt)")
    bound = precheck(root, head, t, changed, result_text)
    if bound is None:
        warnings.append("precheck absent")
    found += [("precheck", detail) for detail in bound or []]
    entries = [a for a in fm.get("allowed_files") or [] if isinstance(a, str)]
    found += [
        ("allowed-files", f"{p} is outside allowed_files") for p in changed if not any(allowed(p, a) for a in entries)
    ]
    exceeded, cap_warnings = caps(text, numstat)
    found += [("caps", detail) for detail in exceeded]
    return found, warnings + cap_warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="the base ref, such as origin/main")
    parser.add_argument("--head", required=True, help="the pull request's head commit")
    parser.add_argument("--root", help="the checkout at the head (default: the current git toplevel)")
    args = parser.parse_args(argv)
    root = args.root or git(".", "rev-parse", "--show-toplevel").stdout.decode().strip() or "."
    shas = [
        git(root, "rev-parse", "--verify", "--quiet", f"{r}^{{commit}}").stdout.decode().strip()
        for r in (args.base, args.head)
    ]
    if not all(shas):
        print(f"regime-ci: cannot resolve --base {args.base} or --head {args.head} in {root}")
        return 2
    base, head = shas
    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()
    if at != head:
        print(
            f"regime-ci: checkout: {root} is at {at[:12]}, not the head {head[:12]}, so the checker would read other files"
        )
        return 1
    changed = [
        p
        for p in git(root, "diff", "--name-only", "--no-renames", "-z", f"{base}...{head}").stdout.decode().split("\0")
        if p
    ]
    numstat = []
    for row in git(root, "diff", "--numstat", "--no-renames", "-z", f"{base}...{head}").stdout.decode().split("\0"):
        if row.count("\t") == 2:
            added, deleted, path = row.split("\t")
            numstat.append((int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0, path))
    dirs = sorted({m.group(1) for p in changed if (m := re.match(r"\.orchestration/([^/]+)/", p))})
    targets = [t for t in dirs if show(root, head, f".orchestration/{t}/task.md") is not None]
    if not targets:
        stray = [p for p in changed if not p.startswith(".orchestration/")]
        if not stray or os.environ.get("GITHUB_HEAD_REF", "").startswith("orchestration/"):
            print("regime-ci: no target (records-only)")
            return 0
        print(
            f"regime-ci: no target: {len(stray)} changed path(s) outside .orchestration/ and no task copy, first {stray[0]}"
        )
        return 1
    failed = False
    for t in targets:
        found, warnings = check_task(root, head, t, changed, numstat)
        for detail in warnings:
            print(f"regime-ci: warning: {t}: {detail}")
        for rule, detail in found:
            print(f"regime-ci: {t}: {rule}: {detail}")
        failed |= bool(found)
    if not failed:
        print(f"regime-ci: ok {len(targets)} task(s)")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
