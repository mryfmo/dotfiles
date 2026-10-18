"""Check a pull request against its task copies: the regime CI job (plan 024 P1-11, programs item (6)).

`uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha>
[--root <dir>]` checks each task whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that has a `task.md`
copy at `<head>` (of a reset_of lineage, only the latest copy): the tracked task-consistency checker on the copy (a
subprocess from the checkout at `<head>`), the copy against the dispatched `.orchestration/tasks/<t>.md` or result.txt's
`task_copy=`, precheck.json's binding to the head and to result.txt's `precheck=`, `allowed_files`, and the caps of the
copy's `## Check` sentence. It prints one `regime-ci: <t>: <rule>: <detail>` line per violation and
`regime-ci: warning: ...` lines, and exits 1 on any violation, 2 when git cannot list the diff, else 0 after
`regime-ci: ok <n> task(s)`. A diff without a task copy passes as `no target (records-only)` only when every path is
under `.orchestration/` or the head branch is `orchestration/*`. Pull-request content is read as data only (git show,
yaml.safe_load, json); the one program run from the checkout is the tracked checker, whose edits show in the diff.
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
# --no-config: a uv.toml or pyproject.toml the pull request adds cannot steer this run
CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
RUNS = (CHECKER, "scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")


class GitError(Exception):
    pass


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)


def listed(root, *args):
    """Return the NUL-separated output of a git listing command, or raise GitError: no listing passes by being empty."""
    out = git(root, *args, "-z")
    if out.returncode:
        raise GitError(f"git {' '.join(args)} failed: {out.stderr.decode(errors='replace').strip()[:200]}")
    return [item for item in out.stdout.decode().split("\0") if item]


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
    outside = re.search(r"at most (\d+) changed lines(?: \([^)]*\))? outside ([^(\n]*)", check)
    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    missing = [
        f"no {name} cap in the copy's ## Check section"
        for name, m in (("outside", outside), ("tests/", tests))
        if not m
    ]
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
    return found, missing


def front(data):
    """Return a copy's front matter mapping, or None when it is unreadable or not a mapping."""
    try:
        fm = yaml.safe_load(data.decode().split("\n---\n", 1)[0].lstrip("-\n"))
    except (UnicodeDecodeError, yaml.YAMLError):
        return None
    return fm if isinstance(fm, dict) else None


def precheck(root, head, t, result_text, exempt=()):
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
    if not isinstance(bound, str) or not re.fullmatch(r"[0-9a-f]{40}", bound):
        found.append(f"precheck.json head {bound!r} is not a 40-hex commit id")
    elif bound != head:
        # precheck.json cannot name the commit that adds it: it names the code commit, and the head may add only
        # this task's evidence on top (the evidence-only ancestor rule of verdict.sh condition 1)
        if git(root, "merge-base", "--is-ancestor", bound, head).returncode:
            found.append(f"precheck.json head {bound} is neither the head {head} nor its ancestor")
        elif other := [
            p
            for p in listed(root, "diff", "--name-only", bound, head)
            if not p.startswith((f".orchestration/{t}/", *exempt))
        ]:
            found.append(
                f"precheck.json head {bound[:12]} differs from the head outside .orchestration/{t}/: {', '.join(other)}"
            )
    if token(result_text, "precheck") != sha256(data):
        found.append(
            f"precheck.json sha256 {sha256(data)} is not result.txt's precheck={token(result_text, 'precheck')}"
        )
    return found


def check_task(root, head, t, changed, numstat, exempt=()):
    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
    copy_path = f".orchestration/{t}/task.md"
    copy = show(root, head, copy_path)
    if (fm := front(copy)) is None:
        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
    text = copy.decode()
    found, warnings = [], []
    if fm.get("task_id") != t:
        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
    run = subprocess.run(
        [*CHECKER_RUN, "--root", root, copy_path], cwd=root, capture_output=True, text=True, check=False
    )
    # the copy is named task.md, so the checker's C1 compares task_id with `task`; task-id above checks the directory
    out = run.stdout.splitlines()
    lines = [ln.strip() for ln in out[1:] if ln.strip() and not re.fullmatch(r"C1 task_id .* != file task", ln.strip())]
    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
        found.append(("checker", f"no verdict (exit {run.returncode}): {(run.stdout + run.stderr).strip()[-300:]}"))
    else:
        found += [("checker", ln) for ln in lines]
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
    bound = precheck(root, head, t, result_text, exempt)
    if bound is None:
        warnings.append("precheck absent")
    found += [("precheck", detail) for detail in bound or []]
    entries = [a for a in fm.get("allowed_files") or [] if isinstance(a, str)]
    found += [
        ("allowed-files", f"{p} is outside allowed_files")
        for p in changed
        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)
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
    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the checker reads the working tree
    if at != head:
        print(
            f"regime-ci: checkout: {root} is at {at[:12]}, not the head {head[:12]}, so the checker would read other files"
        )
        return 1
    try:
        changed = listed(root, "diff", "--name-only", "--no-renames", f"{base}...{head}")
        numstat = []
        for row in listed(root, "diff", "--numstat", "--no-renames", f"{base}...{head}"):
            added, deleted, path = row.split("\t", 2)  # a path may hold a tab; a binary file counts 0 lines
            numstat.append((int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0, path))
    except GitError as error:
        print(f"regime-ci: {error}")
        return 2
    for path in sorted(set(changed) & set(RUNS)):
        print(f"regime-ci: warning: the diff changes {path}, which this job runs; the audit reads that change")
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
    # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target
    fronts = {t: front(show(root, head, f".orchestration/{t}/task.md")) or {} for t in targets}
    later = {p: t for t in targets for p in fronts[t].get("reset_of") or [] if p in fronts and p != t}
    exempt = tuple(f".orchestration/{p}/" for p in later)
    for p, t in sorted(later.items()):
        print(f"regime-ci: warning: {p}: predecessor copy .orchestration/{p}/task.md (reset_of of {t})")
    targets = [t for t in targets if t not in later]
    failed = False
    for t in targets:
        try:
            found, warnings = check_task(root, head, t, changed, numstat, exempt)
        except GitError as error:
            found, warnings = [("git", str(error))], []
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
