"""Check a pull request against its task copies with the base's verifier: the regime CI job (plan 024 P1-11, T133 a02).

`uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha>
[--root <base checkout>]` runs from the base checkout and reads the head only through `git show`: it never checks out,
imports or executes head content. Each task whose `.orchestration/<t>/` the diff `<base>...<head>` touches and that has a
`task.md` copy at the head (of a reset_of lineage, only the latest copy) is checked: the base's task-consistency checker
on the base's dispatched text, the copy against the dispatched `.orchestration/tasks/<t>.md` at the base, whose text is the policy
(allowed_files, caps, reset_of), precheck.json's binding, allowed_files and the caps. Without dispatched text at the base
the copy is unverifiable, a warning until REGIME_REQUIRE_DISPATCHED=1 makes it a violation; result.txt and precheck.json
are the pull request's own claims. It prints one `regime-ci: <t>: <rule>: <detail>` line per violation and
`regime-ci: warning: ...` lines, and exits 1 on any violation, 2 when git cannot list the diff, else 0 after
`regime-ci: ok <n> task(s)`. A diff without a task copy passes as `no target (records-only)` only when every changed path
is under `.orchestration/`, or as `no target (program unit U<n>, D-024-131)` when the pull request body (`PR_BODY`, the
event payload's `pull_request.body`) carries its own line `Program-Unit: regime-cutover/U<n>`: operator decision
D-024-131 runs the regime-cutover program without task copies. No branch name grants anything.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("regime-ci: needs pyyaml: run with uv run --no-project --with pyyaml")
    sys.exit(2)

CHECKER = "scripts/orchestrator/task-consistency-check.py"
# --no-config: a uv.toml or pyproject.toml the pull request adds cannot steer this run
CHECKER_RUN = ["uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I", CHECKER]
RUNS = (CHECKER, "scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")
TOKEN_LIKE = re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}")
PROGRAM_UNIT = re.compile(r"^Program-Unit: regime-cutover/(U[0-9]+)$", re.MULTILINE)  # D-024-131, its own line


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
    m = re.search(rf"(?:^|\s){name}=(\S+)", text)  # lint-comparisons: allow name is the literal precheck or task_copy
    return m.group(1) if m else None


def allowed(path, entry):
    """Match an allowed_files entry: `<dir>/**` takes its prefix, `*` and `?` stay within one path segment."""
    if entry.endswith("/**"):  # lint-comparisons: allow glob-syntax test on an allowed_files entry, not a path
        return path.startswith(entry[:-2])  # lint-comparisons: allow git-listed relative path vs the entry dir prefix
    rx = "".join("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c) for c in entry)
    return re.fullmatch(rx, path) is not None


def caps(text, numstat):
    """Return (violations, warnings) for the `## Check` sentence's caps against the numstat rows."""
    check = text.split("\n## Check", 1)[1].split("\n## ", 1)[0] if "\n## Check" in text else ""
    outside = re.search(r"at most (\d+) changed lines(?: \([^)]*\))? outside ([^(\n]*)", check)
    tests = re.search(r"(\d+)\s+(?:added\s+|changed\s+)?(?:lines\s+)?under\s+`?tests/", check)
    missing = [
        f"no {n} cap in the copy's ## Check section" for n, m in (("outside", outside), ("tests/", tests)) if not m
    ]
    excluded = ["tests/", ".orchestration/"]
    if outside:
        excluded = re.findall(r"`([^`]+)`", re.split(r",\s*(?:and\s+)?\d", outside.group(2))[0]) or excluded

    def counted(path, prefixes):
        return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)  # lint-comparisons: allow git numstat repository-relative paths against the task text's literal cap prefixes  # fmt: skip

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
            for p in listed(root, "diff", "--name-only", "--no-renames", bound, head)
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


def policy(root, base, head, t):
    """Return (the policy bytes, its front matter or None, whether the base's dispatched text is the policy)."""
    dispatched = show(root, base, f".orchestration/tasks/{t}.md")
    data = show(root, head, f".orchestration/{t}/task.md") if dispatched is None else dispatched
    return data, front(data), dispatched is not None


def redact(text):
    """Mask the GH_TOKEN/GITHUB_TOKEN values and token-like literals in checker output (security review of a8c03fae)."""
    for value in filter(None, map(os.environ.get, ("GH_TOKEN", "GITHUB_TOKEN"))):
        text = text.replace(value, "[redacted]")
    return TOKEN_LIKE.sub("[redacted]", text)


def checker(root, data):
    """Return the base checker's violations on the base's dispatched bytes: it hands the text's literals to git (C8 to
    C10) and opens its design path (C6), so a pull request's own text never reaches it (worker review P0 of bcbd6949)."""
    with tempfile.TemporaryDirectory() as scratch:
        cmd = [*CHECKER_RUN, "--root", root, str(Path(scratch, "task.md"))]
        Path(cmd[-1]).write_bytes(data)
        run = subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)
    out = run.stdout.splitlines()  # the file is task.md, so C1 compares task_id with `task`; task-id checks <t>
    # only the checker's own verdict line with its exit code counts; a crash also exits 1, with no verdict line
    if (out[:1], run.returncode) not in ((["task.md: OK"], 0), (["task.md: FAIL"], 1)):
        return [("checker", f"no verdict (exit {run.returncode}): {redact(run.stdout + run.stderr).strip()[-300:]}")]
    lines = [redact(ln).strip() for ln in out[1:] if ln.strip()]
    return [("checker", ln) for ln in lines if not re.fullmatch(r"C1 task_id .* != file task", ln)]


def check_task(root, base, head, t, changed, numstat):
    """Return (violations, warnings) for one task, each violation a (rule, detail) pair."""
    copy_path = f".orchestration/{t}/task.md"
    copy = show(root, head, copy_path)
    if (fm := front(copy)) is None:
        return [("front-matter", f"{copy_path} is unreadable or has no front matter mapping")], []
    data, rules, dispatched = policy(root, base, head, t)
    if rules is None:
        return [("front-matter", f"the base's .orchestration/tasks/{t}.md has no front matter mapping")], []
    found, warnings = [], []
    if fm.get("task_id") != t:
        found.append(("task-id", f"the copy's task_id {fm.get('task_id')!r} is not its directory {t}"))
    result = show(root, head, f".orchestration/{t}/result.txt")
    result_text = result.decode(errors="replace") if result is not None else ""
    if dispatched:
        if data != copy:
            found.append(("task-copy", f"{copy_path} differs from the base's dispatched .orchestration/tasks/{t}.md"))
    else:  # the copy's own policy is provisional: a head file or a result.txt token is a claim, never authentication
        unverifiable = "task copy unverifiable (no dispatched text at base)"
        found += [("task-copy", unverifiable)] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else []
        warnings += [] if os.environ.get("REGIME_REQUIRE_DISPATCHED") == "1" else [unverifiable]
        warnings.append("checker skipped: the copy is unverifiable, and the base's checker reads only the base's text")
        if result is not None and token(result_text, "task_copy") != sha256(copy):
            found.append(
                ("task-copy", f"sha256 {sha256(copy)} is not result.txt's task_copy={token(result_text, 'task_copy')}")
            )
    found += checker(root, data) if dispatched else []
    exempt = tuple(f".orchestration/{p}/" for p in rules.get("reset_of") or [] if isinstance(p, str))
    bound = precheck(root, head, t, result_text, exempt)
    if bound is None:
        warnings.append("precheck absent")
    found += [("precheck", detail) for detail in bound or []]
    entries = [a for a in rules.get("allowed_files") or [] if isinstance(a, str)]
    found += [
        ("allowed-files", f"{p} is outside allowed_files")
        for p in changed
        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)
    ]
    exceeded, cap_warnings = caps(data.decode(errors="replace"), numstat)
    found += [("caps", detail) for detail in exceeded]
    return found, warnings + cap_warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="the base ref, such as origin/main")
    parser.add_argument("--head", required=True, help="the pull request's head commit")
    parser.add_argument("--root", help="the base checkout (default: the current git toplevel)")
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
    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the verifier and the checker must be the base's
    if at != base:
        print(
            f"regime-ci: checkout: {root} is at {at[:12]}, not the base {base[:12]}, so the code run would not be the base's"
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
        print(
            f"regime-ci: warning: the diff changes {path}; this run executed the base's version, the audit reads the change"
        )
    dirs = sorted({m.group(1) for p in changed if (m := re.match(r"\.orchestration/([^/]+)/", p))})
    targets = [t for t in dirs if show(root, head, f".orchestration/{t}/task.md") is not None]
    if not targets:
        stray = [p for p in changed if not p.startswith(".orchestration/")]  # lint-comparisons: allow git-listed repository-relative paths against the literal .orchestration/ prefix  # fmt: skip
        if not stray:  # content alone decides: a branch name is the pull request's own claim
            print("regime-ci: no target (records-only)")
            return 0
        if unit := PROGRAM_UNIT.search(os.environ.get("PR_BODY", "").replace("\r\n", "\n")):  # github.com edits add CR
            print(f"regime-ci: no target (program unit {unit.group(1)}, D-024-131)")
            return 0
        print(
            f"regime-ci: no target: {len(stray)} changed path(s) outside .orchestration/ and no task copy, first {stray[0]}"
        )
        return 1
    # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target, when both verify
    policies = {t: policy(root, base, head, t) for t in targets}
    exact = {t: policies[t][2] and show(root, head, f".orchestration/{t}/task.md") == policies[t][0] for t in targets}
    later = {
        p: t
        for t, (_, rules, _) in policies.items()
        for p in (rules or {}).get("reset_of") or []
        if p in policies and p != t and exact[t] and exact[p]  # both head copies equal their base texts
    }
    for p, t in sorted(later.items()):
        print(f"regime-ci: warning: {p}: predecessor copy .orchestration/{p}/task.md (reset_of of {t})")
    targets = [t for t in targets if t not in later]
    failed = False
    for t in targets:
        try:
            found, warnings = check_task(root, base, head, t, changed, numstat)
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
