#!/usr/bin/env python3
"""Refuse a retired term or path in the live tree (regime-cutover U72, audit be179c71 cluster A).

python3 -I scripts/lint-retired-terms.py [--list <tsv>] [--root <dir>] reads the one list of retired names,
`scripts/retired-terms.tsv`, and checks every file git lists in the root (tracked and untracked-not-ignored files that
exist in the worktree, the list file itself excepted) against it. Each hit is printed as `<file>:<line>: <text>` and the
exit status is 1; a clean tree exits 0; any other status (2) means the check could not run: an unreadable or malformed
list, a git failure, an unreadable file. The list's rows, tab-separated, `#` starting a comment line:

- `term <text> <reason>`: a retired name. A line of a scanned file that contains <text>, compared without regard to ASCII
  case, is a hit, unless an `allow` row names that exact file and that exact term.
- `allow <file> <term> <reason>`: a deliberate mention (history, compatibility, the retirement code). <file> is a path as
  git ls-files prints it and <term> one of the `term` rows, both compared exactly. A row whose file no longer exists or
  no longer contains its term is itself a hit, so the allow list never outlives what it allows.
- `skip <dir>/ <reason>`: a directory of records or generated snapshots that is not scanned; <dir>/ is compared as an
  exact prefix of the git path.
- `gone <path> <reason>`: a deleted source path; the path existing in the root is a hit.
- `removed <target> <reason>`: a deployed target the source no longer ships; `home/.chezmoiremove` must hold it as an
  exact line, so `chezmoi apply` removes the copy a host still has.

Hits on the list itself are reported at the list's own line.
"""

import argparse
import subprocess
import sys
from pathlib import Path

LIST = Path("scripts/retired-terms.tsv")
CHEZMOIREMOVE = Path("home/.chezmoiremove")
FIELDS = {"term": 3, "allow": 4, "skip": 3, "gone": 3, "removed": 3}


class Refusal(Exception):
    """The check could not run; the message names what failed."""


def parse_list(path: Path) -> dict[str, list[tuple[int, list[str]]]]:
    """Return the list's rows by kind, each as (line number, fields), refusing a malformed row."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise Refusal(f"cannot read the list {path}: {error}") from error
    rows: dict[str, list[tuple[int, list[str]]]] = {kind: [] for kind in FIELDS}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        kind = fields[0]
        if kind not in FIELDS:
            raise Refusal(f"{path}:{number}: unknown kind {kind!r}; expected one of {', '.join(FIELDS)}")
        if len(fields) != FIELDS[kind] or not all(fields):
            raise Refusal(f"{path}:{number}: a {kind} row has {FIELDS[kind]} non-empty tab-separated fields")
        rows[kind].append((number, fields[1:]))
    terms = [fields[0] for _, fields in rows["term"]]
    if len({term.lower() for term in terms}) != len(terms):
        raise Refusal(f"{path}: a term is listed twice")
    for number, (_, term, _) in rows["allow"]:
        if term not in terms:
            raise Refusal(f"{path}:{number}: allow row names {term!r}, which is no term row")
    for number, (prefix, _) in rows["skip"]:
        if not prefix.endswith("/"):  # lint-comparisons: allow a list row's text; skip rows are exact git-path prefixes
            raise Refusal(f"{path}:{number}: a skip row names a directory ending in /")
    return rows


def git_paths(root: Path, *args: str) -> list[str]:
    """Return the NUL-separated paths `git ls-files <args>` prints in root, refusing on a git failure."""
    try:
        run = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", *args], capture_output=True, check=False, timeout=60
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Refusal(f"git ls-files {' '.join(args)} could not run: {error}") from error
    if run.returncode != 0:
        raise Refusal(f"git ls-files {' '.join(args)} exited {run.returncode}: {run.stderr.decode(errors='replace')}")
    return [path for path in run.stdout.decode("utf-8", errors="surrogateescape").split("\0") if path]


def scanned_files(root: Path, list_path: str) -> list[str]:
    """Return the tracked and untracked-not-ignored paths that exist in the worktree, the list itself excepted."""
    deleted = set(git_paths(root, "--deleted"))
    listed = git_paths(root, "--cached", "--others", "--exclude-standard")
    return sorted({p for p in listed if p not in deleted and p != list_path})  # lint-comparisons: allow git paths


def file_lines(root: Path, path: str) -> list[bytes]:
    """Return a file's lines as bytes; a symlink is read as its target text, which is what git tracks."""
    full = root / path
    try:
        data = str(full.readlink()).encode() if full.is_symlink() else full.read_bytes()
    except OSError as error:
        raise Refusal(f"cannot read {path}: {error}") from error
    return data.split(b"\n")


def check(root: Path, list_path: Path) -> list[str]:
    """Return every hit as `<file>:<line>: <text>`."""
    rel_list = list_path.relative_to(root).as_posix() if list_path.is_relative_to(root) else str(list_path)
    rows = parse_list(list_path)
    terms = {term: term.lower().encode() for _, (term, _) in rows["term"]}
    allowed = {(file, term): number for number, (file, term, _) in rows["allow"]}
    used: set[tuple[str, str]] = set()
    skips = tuple(prefix for _, (prefix, _) in rows["skip"])
    hits = []
    for path in scanned_files(root, rel_list):
        if path.startswith(skips):  # lint-comparisons: allow git ls-files paths against the list's exact prefixes
            continue
        for number, line in enumerate(file_lines(root, path), start=1):
            lowered = line.lower()
            found = [term for term, needle in terms.items() if needle in lowered]
            for term in found:
                if (path, term) in allowed:
                    used.add((path, term))
            refused = [term for term in found if (path, term) not in allowed]
            if refused:
                text = line.decode("utf-8", errors="replace").strip()
                text = text if len(text) <= 200 else text[:197] + "..."
                hits.append(f"{path}:{number}: retired {', '.join(map(repr, refused))}: {text}")
    for (file, term), number in sorted(allowed.items(), key=lambda item: item[1]):
        if (file, term) not in used:
            hits.append(f"{rel_list}:{number}: allow row {file} {term!r} matches nothing; remove the row")
    for number, (path, _) in rows["gone"]:
        if (root / path).exists() or (root / path).is_symlink():
            hits.append(f"{rel_list}:{number}: retired path {path} exists again")
    removals = root / CHEZMOIREMOVE
    try:
        entries = set(removals.read_text(encoding="utf-8").splitlines())
    except (OSError, UnicodeDecodeError) as error:
        raise Refusal(f"cannot read {CHEZMOIREMOVE}: {error}") from error
    for number, (target, _) in rows["removed"]:
        if target not in entries:
            hits.append(f"{rel_list}:{number}: {CHEZMOIREMOVE} has no line {target}, so hosts keep the retired copy")
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--root", type=Path, help="repository root (default: this checkout)")
    parser.add_argument("--list", type=Path, help="the list (default: <root>/scripts/retired-terms.tsv)")
    args = parser.parse_args()  # a usage error exits 2 on its own
    # Every filesystem step (resolving the paths, reading the list and the files, running git) is inside the handler:
    # any failure means the check did not run, so it exits 2, never 1 (read as hits) or 0 (read as clean).
    try:
        root = (args.root or Path(__file__).resolve().parents[1]).resolve(strict=True)
        list_path = (args.list or root / LIST).resolve()
        hits = check(root, list_path)
    except Refusal as error:
        print(f"lint-retired-terms: {error}", file=sys.stderr)
        return 2
    except Exception as error:  # noqa: BLE001
        # A traceback would exit 1, which the callers read as hits, so the class of the failure is irrelevant here.
        print(f"lint-retired-terms: the check failed: {error!r}", file=sys.stderr)
        return 2
    for hit in hits:
        print(hit)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
