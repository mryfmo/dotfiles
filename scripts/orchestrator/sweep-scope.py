#!/usr/bin/env python3
"""The one predicate of the sweep rule by path class (regime-cutover U597, the operator's sweep rule C of 2026-11-18).

Until U597 the AGENTS.md Audit sweep rule asked one sweep of the `security-audit` skill of every unit at every head
(U147, U244), and `pr-merge.sh` refused any head without its `sweep` ledger row. Measured 2026-11-17 to 2026-11-18:
22 of 22 sweeps returned 0 findings while the Codex audit found filed findings in every round 1, and a sweep costs 10
minutes of seat time in the merge path (handouts/decisions-four-points-2026-11-18.md). Rule C: the sweep is required
before a merge only for a head whose changed paths touch a lever, a policy, credential handling or a deployed
executable; every other head merges on its Codex audit and CI alone; and main's head gets one full sweep per day, the
standing control, which `pr-merge.sh` never reads.

`sweep_required(paths)` is the predicate, defined here alone and read by `pr-merge.sh` (as `python3 -I -S
scripts/orchestrator/sweep-scope.py --stdin` over the changed paths `gh pr diff <pr> --name-only` lists, the lever
reading no local git object) and by `tests/unit/test_sweep_scope.py`. The classes are one frozen tuple of path
prefixes each (CLASSES, in order of precedence): `credential` (the seat launcher, the broker, the token placer and the
login preflight, in `scripts/orchestrator/` and as their deployed twins, and `home/.chezmoiscripts/`), `policy`
(`home/dot_agents/omp/policies/` and `home/dot_agents/agent-config.yaml`, whose `command_policy` block counts as the
whole manifest file), `lever` (`scripts/orchestrator/`, `home/dot_local/bin/common/`) and `deployed-executable`
(`home/dot_local/bin/`, `home/dot_dsh/plugins/`, `install/`). A prefix ending in `/` matches every path below it; any
other entry matches that one path. A head's class is the first class, in that order, that one of its changed paths
falls in; a path matching no class requires nothing, and a head of such paths alone is `not-required`.

CLI: `sweep-scope.py <base> <head>` lists the head's changed paths as `git diff --name-only --no-renames
<base>...<head>` (the paths changed since the merge base, renames shown as both paths, run in the current directory's
repository with replace refs off) and prints `required <class>` or `not-required`, exit 0; `sweep-scope.py --stdin`
reads the changed paths one per line from stdin, as `gh pr diff <pr> --name-only` prints them, and answers the same.
Exit 2 with one stderr line (`sweep-scope: ...`) on usage, a git that fails or cannot run, a listing that names no
path, an empty line, a path that is absolute or holds a control character or a `.`, `..` or empty component (not a
path git lists), or stdin that is not UTF-8: a failed or unreadable listing is never `not-required` (standing order
21), and the lever refuses on exit 2 and fails on any other status.
"""

from __future__ import annotations

import subprocess
import sys

# The classes in precedence order, each one frozen tuple of prefixes (`<dir>/`) and exact paths; the operator's
# classification (decisions-four-points-2026-11-18.md, sweep rule C), read as text against the paths git lists.
CREDENTIAL_PATHS = (
    "scripts/orchestrator/hcom-seat",
    "scripts/orchestrator/acp-broker",
    "scripts/orchestrator/seat-token-place",
    "scripts/orchestrator/seat-login-preflight",
    "home/dot_local/bin/common/executable_hcom-seat",
    "home/dot_local/bin/common/executable_acp-broker",
    "home/dot_local/bin/common/executable_seat-token-place",
    "home/dot_local/bin/common/executable_seat-login-preflight",
    "home/.chezmoiscripts/",
)
POLICY_PATHS = (
    "home/dot_agents/omp/policies/",
    "home/dot_agents/agent-config.yaml",
)
LEVER_PATHS = (
    "scripts/orchestrator/",
    "home/dot_local/bin/common/",
)
DEPLOYED_EXECUTABLE_PATHS = (
    "home/dot_local/bin/",
    "home/dot_dsh/plugins/",
    "install/",
)
CLASSES = (
    ("credential", CREDENTIAL_PATHS),
    ("policy", POLICY_PATHS),
    ("lever", LEVER_PATHS),
    ("deployed-executable", DEPLOYED_EXECUTABLE_PATHS),
)
CLASS_NAMES = tuple(name for name, _ in CLASSES)
REQUIRED = "required"
NOT_REQUIRED = "not-required"
USAGE = "usage: sweep-scope.py <base> <head> | sweep-scope.py --stdin"
# The git listing: NUL-separated names, renames as both paths, no external diff, no colour, replace refs off.
GIT_DIFF = (
    "git",
    "--no-replace-objects",
    "-c",
    "core.quotePath=false",
    "diff",
    "-z",
    "--name-only",
    "--no-renames",
    "--no-ext-diff",
    "--no-color",
    "--ignore-submodules=none",
)


class Unreadable(Exception):
    """The changed paths cannot be read; the message is the one stderr line."""


def path_class(path: str) -> str | None:
    """The first class, in CLASSES order, whose prefix tuple holds `path`, or None."""
    for name, prefixes in CLASSES:
        for prefix in prefixes:
            if prefix.endswith("/"):  # lint-comparisons: allow the table's own shape, a directory entry ends in /
                if path.startswith(prefix):  # lint-comparisons: allow git's path text against the prefix table
                    return name
            elif path == prefix:  # lint-comparisons: allow the same table, an exact entry
                return name
    return None


def sweep_required(paths) -> str | None:
    """The class that requires the sweep for a head whose changed paths are `paths`, the first in CLASSES order that
    one path falls in; None when no path falls in any class."""
    found = {path_class(path) for path in paths}
    for name in CLASS_NAMES:
        if name in found:
            return name
    return None


def check_path(path: str) -> str:
    """`path` as git lists it, or Unreadable: a relative path of non-empty components other than `.` and `..`, with
    no control character; anything else is not a listing of changed paths."""
    if not path:
        raise Unreadable("the listing holds an empty line; it is not a listing of changed paths")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in path):
        raise Unreadable("a listed path holds a control character; it is not a path git lists")
    if path.startswith("/"):  # lint-comparisons: allow the listing's text is judged for its shape, nothing is resolved
        raise Unreadable(f"a listed path is absolute: {path}; git lists paths relative to the repository")
    if any(part in ("", ".", "..") for part in path.split("/")):
        raise Unreadable(f"a listed path holds a '.', '..' or empty component: {path}; it is not a path git lists")
    return path


def paths_from_listing(text: str, separator: str) -> list[str]:
    """The paths of a listing separated by `separator` with one trailing separator at most; an empty listing or an
    empty entry is Unreadable."""
    entries = text.split(separator)
    if entries and entries[-1] == "":
        entries.pop()
    if not entries:
        raise Unreadable("the listing names no changed path; an empty listing is a failed read, never not-required")
    return [check_path(entry) for entry in entries]


def changed_paths_from_git(base: str, head: str) -> list[str]:
    """`git diff --name-only --no-renames <base>...<head>` in the current directory's repository, its status read."""
    for rev in (base, head):
        if not rev or rev.startswith("-"):
            raise Unreadable(f"{rev!r} is not a revision")
    command = [*GIT_DIFF, f"{base}...{head}", "--"]
    try:
        out = subprocess.run(command, capture_output=True, check=False)
    except OSError as error:
        raise Unreadable(f"cannot run git: {error.strerror}") from None
    if out.returncode:
        detail = out.stderr.decode(errors="replace").strip().splitlines()
        raise Unreadable(
            f"git diff --name-only {base}...{head} exited {out.returncode}: {detail[0][:200] if detail else 'no output'}"
        )
    try:
        text = out.stdout.decode()
    except UnicodeDecodeError:
        raise Unreadable("git listed a path that is not UTF-8") from None
    return paths_from_listing(text, "\0")


def changed_paths_from_stdin() -> list[str]:
    """The paths on stdin, one per line, as `gh pr diff <pr> --name-only` prints them."""
    try:
        text = sys.stdin.buffer.read().decode()
    except OSError as error:
        raise Unreadable(f"cannot read stdin: {error.strerror}") from None
    except UnicodeDecodeError:
        raise Unreadable("stdin is not UTF-8") from None
    return paths_from_listing(text, "\n")


def answer(paths) -> str:
    """`required <class>` or `not-required` for the changed paths."""
    name = sweep_required(paths)
    return f"{REQUIRED} {name}" if name else NOT_REQUIRED


def main(argv: list[str]) -> int:
    try:
        if argv == ["--stdin"]:
            paths = changed_paths_from_stdin()
        elif len(argv) == 2 and not argv[0].startswith("-"):
            paths = changed_paths_from_git(argv[0], argv[1])
        else:
            raise Unreadable(USAGE)
    except Unreadable as error:
        print(f"sweep-scope: {error}", file=sys.stderr)
        return 2
    print(answer(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
