#!/usr/bin/env python3
"""The one predicate of the sweep rule by path class (regime-cutover U597, the operator's sweep rule C of 2026-11-18).

Until U597 the AGENTS.md Audit sweep rule asked one sweep of the `security-audit` skill of every unit at every head
(U147, U244), and `pr-merge.sh` refused any head without its `sweep` ledger row. Measured 2026-11-17 to 2026-11-18:
22 of 22 sweeps returned 0 findings while the Codex audit found filed findings in every round 1, and a sweep costs 10
minutes of seat time in the merge path (handouts/decisions-four-points-2026-11-18.md). Rule C: the sweep is required
before a merge only for a head whose changed paths touch a lever, a policy, credential handling or a deployed
executable; every other head merges on its Codex audit and CI alone; and main's head gets one full sweep per day, the
standing control, whose newest row (`daily-sweeps.tsv`, read through `ledger.py daily`) `pr-merge.sh` requires within
24 hours before it skips the per-head row (round 4).

`sweep_required(paths)` is the predicate, defined here alone and read by `pr-merge.sh` (as `python3 -I -S
scripts/orchestrator/sweep-scope.py --files-json --changed-files <n>` over the audited head's changed files as the
GitHub compare API lists them keyed by the head's sha, `gh api 'repos/{owner}/{repo}/compare/main...<head>'
--paginate --jq '.files[] | [.status, .filename, (if has("previous_filename") then .previous_filename else null
end)] | @json'`, one JSON array per file, both paths of a rename counting, the lever reading no local git object) and
by `tests/unit/test_sweep_scope.py`.
The classes are one frozen tuple of path prefixes each (CLASSES, in order of precedence): `credential` (the seat
launcher, the broker, the token placer and the login preflight, in `scripts/orchestrator/` and as their deployed
twins, and `home/.chezmoiscripts/`), `policy`
(`home/dot_agents/omp/policies/` and `home/dot_agents/agent-config.yaml`, whose `command_policy` block counts as the
whole manifest file), `lever` (`scripts/orchestrator/`, `home/dot_local/bin/common/`) and `deployed-executable`
(`home/dot_local/bin/`, `home/dot_dsh/plugins/`, `install/`). A prefix ending in `/` matches every path below it; any
other entry matches that one path. A head's class is the first class, in that order, that one of its changed paths
falls in; a path matching no class requires nothing, and a head of such paths alone is `not-required`.

CLI: `sweep-scope.py <base> <head>` lists the head's changed paths as `git diff --name-only --no-renames
<base>...<head>` (the paths changed since the merge base, renames shown as both paths, run in the current directory's
repository with replace refs off, and with `-c diff.relative=false` and `--no-relative` so a `diff.relative` setting
or a run from a subdirectory neither narrows the listing nor strips a prefix; round 3) and prints `required <class>`
or `not-required`, exit 0; `sweep-scope.py --files-json [--changed-files <n>]` reads the head's files from stdin as
the lever's compare API read prints them, one JSON array `[status, filename, previous_filename]` per line: `status`
one of `added`, `removed`, `modified`, `renamed`, `copied`, `changed`, `unchanged`; `filename` a path;
`previous_filename` a path for `renamed` and `copied` and `null` for every other status (round 4: a value that is
neither a string nor null, a boolean `false` included, is refused before the status decides, so the lever's jq passes
the field through as it is, `if has("previous_filename") then .previous_filename else null end`, and never maps a
malformed value to null); both paths of a rename or a copy count; and with `--changed-files <n>` the count of
distinct `filename` entries must equal `n`, the pull request's `changedFiles` (a listing cut short, a page lost, or
a cap read as complete is never `not-required`), and it answers the same. Exit 2 with one stderr line
(`sweep-scope: ...`) on usage, a git that fails or cannot run, a listing that names no path, an empty line, a line
that is not JSON or not an array of three, an unknown status, a `previous_filename` that is neither a string nor
null, a rename or copy without its source, a source on any other status, a count that differs from
`--changed-files`, a path that is absolute or holds a control character (an embedded newline included, since the
decoded string holds it) or a `.`, `..` or empty component (not a path git lists), a path that starts with `"` or
holds a backslash (a C-quoted name, as git prints a path with a tab or a non-ASCII byte under `core.quotePath`, is
not the path itself; the API never quotes, so this guard is the reader's own, round 2 of U597), or stdin that is not
UTF-8: a failed or unreadable listing is never `not-required` (standing order 21), and the lever refuses on exit 2
and fails on any other status.
"""

from __future__ import annotations

import json
import re
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
USAGE = "usage: sweep-scope.py <base> <head> | sweep-scope.py --files-json [--changed-files <n>]"
# The statuses the GitHub pull request files API gives a file, and the two that carry the file's source as
# `previous_filename` (docs.github.com, REST API, pulls, list pull requests files).
STATUSES = frozenset(("added", "removed", "modified", "renamed", "copied", "changed", "unchanged"))
SOURCED_STATUSES = frozenset(("renamed", "copied"))
COUNT = re.compile(r"[0-9]+")
# The git listing: NUL-separated names, renames as both paths, no external diff, no colour, replace refs off, and
# paths from the toplevel whatever `diff.relative` says or where the command runs (round 3).
GIT_DIFF = (
    "git",
    "--no-replace-objects",
    "-c",
    "core.quotePath=false",
    "-c",
    "diff.relative=false",
    "diff",
    "-z",
    "--name-only",
    "--no-renames",
    "--no-relative",
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
    no control character, not C-quoted and holding no backslash; anything else is not a listing of changed paths."""
    if not path:
        raise Unreadable("the listing holds an empty line; it is not a listing of changed paths")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in path):
        raise Unreadable("a listed path holds a control character; it is not a path git lists")
    quoted = (
        f"a listed path is C-quoted or holds a backslash: {path}; a quoted listing is not a listing of changed paths"
    )
    if path.startswith('"'):  # lint-comparisons: allow the listing's text is judged for its shape, nothing is resolved
        raise Unreadable(quoted)
    if "\\" in path:  # lint-comparisons: allow the listing's text is judged for its shape, nothing is resolved
        raise Unreadable(quoted)
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


def file_entry(line: str, number: int) -> tuple[str, str, str | None]:
    """Line `number` of the files listing as the compare API's `[status, filename, previous_filename]`, each checked:
    the status one of STATUSES, the filename a path, the source a string or null before anything else (round 4: a
    boolean `false` is neither, and the lever's jq no longer maps it to null), then a path for a rename or a copy and
    null otherwise. Any other shape is Unreadable naming the line."""
    where = f"line {number} of the files listing"
    shown = line if len(line) <= 200 else line[:200] + "..."
    try:
        entry = json.loads(line)
    except ValueError:
        raise Unreadable(f"{where} is not JSON: {shown!r}; it is not the files API read as data") from None
    if not isinstance(entry, list) or len(entry) != 3:
        raise Unreadable(f"{where} is not an array of three (status, filename, previous_filename): {shown!r}")
    status, filename, previous = entry
    if not isinstance(status, str) or status not in STATUSES:
        raise Unreadable(
            f"{where} has the status {status!r}, not one of {', '.join(sorted(STATUSES))}; it is not the files API read"
            " as data"
        )
    if not isinstance(filename, str):
        raise Unreadable(f"{where} has no filename string: {shown!r}; it is not the files API read as data")
    check_path(filename)
    if previous is not None and not isinstance(previous, str):
        raise Unreadable(
            f"{where} has a previous_filename that is neither a string nor null: {previous!r}; it is not the files API"
            " read as data"
        )
    if status in SOURCED_STATUSES:
        if previous is None:
            raise Unreadable(
                f"{where} is {status} without its source (previous_filename): {shown!r}; a rename or a copy lists both"
                " paths"
            )
        check_path(previous)
    elif previous is not None:
        raise Unreadable(
            f"{where} is {status} yet carries a previous_filename: {shown!r}; only a rename or a copy has a source"
        )
    return status, filename, previous


def paths_from_files_json(text: str, count: int | None) -> list[str]:
    """The paths of the files listing, one JSON array per line with one trailing newline at most: every filename and
    every rename's or copy's source. An empty listing or an empty line is Unreadable, as is a count of distinct
    filenames other than `count` when one is given (the pull request's `changedFiles`)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        raise Unreadable("the files listing names no file; an empty listing is a failed read, never not-required")
    paths: list[str] = []
    filenames: set[str] = set()
    for number, line in enumerate(lines, 1):
        if not line:
            raise Unreadable(f"line {number} of the files listing is empty; it is not the files API read as data")
        _, filename, previous = file_entry(line, number)
        filenames.add(filename)
        paths.append(filename)
        if previous is not None:
            paths.append(previous)
    if count is not None and len(filenames) != count:
        raise Unreadable(
            f"the files listing names {len(filenames)} distinct filenames, not the {count} changedFiles of the pull"
            " request; a listing cut short, a page lost or GitHub's 3,000-file cap read as complete is never"
            " not-required"
        )
    return paths


def changed_paths_from_files_json(options: list[str]) -> list[str]:
    """The files listing on stdin as the lever's compare API read prints it (`gh api
    'repos/{owner}/{repo}/compare/main...<head>' --paginate --jq '.files[] | [.status, .filename, (if
    has("previous_filename") then .previous_filename else null end)] | @json'`), `options` empty or
    `--changed-files <n>`."""
    count = None
    if options:
        if len(options) != 2 or options[0] != "--changed-files" or not COUNT.fullmatch(options[1]):
            raise Unreadable(USAGE)
        count = int(options[1])
    try:
        text = sys.stdin.buffer.read().decode()
    except OSError as error:
        raise Unreadable(f"cannot read stdin: {error.strerror}") from None
    except UnicodeDecodeError:
        raise Unreadable("stdin is not UTF-8") from None
    return paths_from_files_json(text, count)


def answer(paths) -> str:
    """`required <class>` or `not-required` for the changed paths."""
    name = sweep_required(paths)
    return f"{REQUIRED} {name}" if name else NOT_REQUIRED


def main(argv: list[str]) -> int:
    try:
        if argv and argv[0] == "--files-json":
            paths = changed_paths_from_files_json(argv[1:])
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
