"""Check a pull request for its program-unit marker with the base's verifier: the regime CI job (plan 024 P1-11, U26).

`uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base <ref> --head <sha>
[--root <base checkout>]` runs from the base checkout and reads the head only through `git diff`: it never checks out,
imports or executes head content. A diff passes as `no target (records-only)` only when every changed path is under
`.orchestration/`, or as `no target (program unit U<n>, D-024-131)` when the pull request body (`PR_BODY`, the event
payload's `pull_request.body`) carries its own line `Program-Unit: regime-cutover/U<n>`: operator decision D-024-131 runs
the regime-cutover program without task copies, and the task-copy rule left with the old regime's tooling (U26).
It exits 1 on any other diff or when the checkout is not at the base, 2 when git cannot resolve the refs or list the
diff. No branch name grants anything.
"""

import argparse
import os
import re
import subprocess
import sys

RUNS = ("scripts/orchestrator/regime-ci.py", ".github/workflows/regime.yml")
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
    at = git(root, "rev-parse", "HEAD").stdout.decode().strip()  # the verifier that runs must be the base's
    if at != base:
        print(
            f"regime-ci: checkout: {root} is at {at[:12]}, not the base {base[:12]}, so the code run would not be the base's"
        )
        return 1
    try:
        changed = listed(root, "diff", "--name-only", "--no-renames", f"{base}...{head}")
    except GitError as error:
        print(f"regime-ci: {error}")
        return 2
    for path in sorted(set(changed) & set(RUNS)):
        print(
            f"regime-ci: warning: the diff changes {path}; this run executed the base's version, the audit reads the change"
        )
    stray = [p for p in changed if not p.startswith(".orchestration/")]  # lint-comparisons: allow git-listed repository-relative paths against the literal .orchestration/ prefix  # fmt: skip
    if not stray:  # content alone decides: a branch name is the pull request's own claim
        print("regime-ci: no target (records-only)")
        return 0
    if unit := PROGRAM_UNIT.search(os.environ.get("PR_BODY", "").replace("\r\n", "\n")):  # github.com edits add CR
        print(f"regime-ci: no target (program unit {unit.group(1)}, D-024-131)")
        return 0
    print(
        f"regime-ci: no target: {len(stray)} changed path(s) outside .orchestration/ and no Program-Unit line, first {stray[0]}"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
