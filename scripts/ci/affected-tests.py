#!/usr/bin/env python3
"""Print the test modules a change can reach, one per line, or the word `all` (regime-cutover U623).

python3 -I scripts/ci/affected-tests.py --base <rev> --head <rev> [--start tests/unit] [--pattern 'test*.py'] [--explain]

The map is built at run time from the tree in the working directory, the repository root. Each test module under
--start (a file matching --pattern, the runner's discovery pattern) reaches the repository modules it imports (an
`import` or `from` that resolves to a file under scripts/ or tests/ from the root or from the importing file's own
directory, as `python -m unittest discover` resolves them; a relative import from the file's package), followed
through the imported files, and every repository path a string literal of those files names: a whole literal that is
a path in the tree (`scripts/orchestrator/pr-merge.sh`; a directory such as `home/dot_agents/skills`, which reaches
everything under it), a slash-bearing token inside a longer literal (`"bash -c 'source scripts/lib/x.sh'"`), and the
directory before the first glob character or f-string field (`home/dot_local/bin/common/executable_*`,
f"home/dot_agents/skills/{skill}/SKILL.md"). A changed path selects every module whose reach holds it or one of its
parent directories, and a changed test module selects itself. A lever under scripts/orchestrator/ and its deployed
twin home/dot_local/bin/common/executable_<name> count as one path, so a change to either selects the tests of both.

A changed path under --start that is no test module (a helper, a fixture, `__init__.py`), a change under scripts/ci/
or .github/workflows/, or to Makefile, pyproject.toml or uv.lock answers `all`: the selection itself, the runner, the
workflow and the code every module shares are not mapped, so the full suite runs. A change nothing reaches selects
nothing (an empty answer, exit 0).

The changed paths are `git diff -z --no-renames --name-only <base>...<head>`, the merge base to the head with both
sides of a rename. A diff that fails, a start directory without a module, or a module that cannot be read or parsed is
exit 2 with the cause on stderr, never an empty answer (standing order 21). --explain prints to stderr why each module
was selected, or why the answer is `all`, and which changed paths reach nothing; stdout stays the list. Nothing but
the standard library is imported: the workflow runs this before any tool is installed, on the runner's python3.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import subprocess
import sys
import warnings
from pathlib import Path

# A change here runs the full suite: the selection, the runner and the lints under scripts/ci/, the workflows, and the
# files that build the environment the tests run in.
ALL_PREFIXES = ("scripts/ci/", ".github/workflows/")
ALL_NAMES = ("Makefile", "pyproject.toml", "uv.lock")
# An import reaches a file under these prefixes only: a third-party or standard-library module is no repository path.
IMPORT_PREFIXES = ("scripts/", "tests/")
# A lever and its deployed twin (AGENTS.md, the audit section): the same program under two paths.
LEVERS = "scripts/orchestrator/"
TWINS = "home/dot_local/bin/common/executable_"
# A bare literal with one of these is a pattern, read up to the character as a directory prefix.
GLOB = "*?[{"
# A literal starting with one of these is an absolute path, a home or variable reference or an option, no repository path.
OUTSIDE_STARTS = ("/", "~", "$", "-")
# Punctuation prose puts around a path inside a longer literal.
TRIM = "\"'`()[]{}<>,.:;!"
SLASH = "/"
PROGRAM = "affected-tests"


def fail(message: str) -> None:
    print(f"{PROGRAM}: {message}", file=sys.stderr)
    sys.exit(2)


def changed_paths(base: str, head: str) -> list[str]:
    """The paths `git diff` lists from the merge base of `base` and `head` to `head`; a failed diff is exit 2."""
    run = subprocess.run(
        ["git", "diff", "-z", "--no-renames", "--name-only", f"{base}...{head}"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if run.returncode != 0:
        detail = run.stderr.decode("utf-8", "replace").strip()
        fail(f"git diff {base}...{head} failed with exit {run.returncode}: {detail}")
    return [entry for entry in run.stdout.decode("utf-8", "surrogateescape").split("\0") if entry]


def repository_module(root: Path, target: Path) -> str | None:
    """`target` relative to `root` as a posix string when it is a file under IMPORT_PREFIXES, else None."""
    try:
        rel = target.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    return rel if rel.startswith(IMPORT_PREFIXES) and target.is_file() else None


def normalise(text: str, token: bool) -> tuple[str, str] | None:
    """`text` as a repository path candidate `(path, kind)`, or None when it cannot be one.

    The kind is `dir` for a pattern (a glob character or an f-string field; read up to the character, then to its
    last slash) or a literal ending in a slash, `file` for a bare word (`Makefile`; a top-level directory's name alone
    is a word of prose, never a prefix: `home` would reach everything), `any` for a slash-bearing path. A token from
    inside a longer literal counts only with a slash in it. An absolute path, a home or variable reference, a URL, an
    option or a parent reference is none.
    """
    text = text.strip()
    if token:
        text = text.strip(TRIM)
    kind = "any"
    pattern = min((text.index(char) for char in GLOB if char in text), default=-1)
    if pattern >= 0:
        # The word the pattern is attached to, never an earlier word of a longer literal.
        words = text[:pattern].split()
        attached = words[-1] if words and pattern > 0 and not text[pattern - 1].isspace() else ""
        text = attached.rpartition(SLASH)[0] + SLASH
        kind = "dir"
    if not text or any(char.isspace() or ord(char) < 32 for char in text) or len(text) > 240:
        return None
    if text.startswith(OUTSIDE_STARTS) or text.find("://") >= 0 or (token and text.count(SLASH) == 0):
        return None
    if text.endswith(SLASH):
        kind = "dir"
    text = text.removeprefix("./").rstrip(SLASH)
    if not text or any(part in ("", ".", "..") for part in text.split(SLASH)):
        return None
    if kind == "any" and text.count(SLASH) == 0:
        kind = "file"
    return text, kind


def twin(changed: str) -> str | None:
    """The other path of a lever: its deployed twin, or the lever of a twin; None for every other path."""
    if changed.startswith(LEVERS) and changed[len(LEVERS) :].count(SLASH) == 0:
        return TWINS + changed[len(LEVERS) :]
    if changed.startswith(TWINS) and changed[len(TWINS) :].count(SLASH) == 0:
        return LEVERS + changed[len(TWINS) :]
    return None


def ancestors(changed: str) -> list[str]:
    """`a/`, `a/b/`, ... for `a/b/c`: the directory prefixes a reach may hold."""
    parts = changed.split(SLASH)
    return [SLASH.join(parts[:count]) + SLASH for count in range(1, len(parts))]


class Mapper:
    """The reach of each file, read once per file from its syntax tree and kept."""

    def __init__(self, root: Path, changed: set[str]) -> None:
        self.root = root
        self.changed = changed
        self.trees: dict[str, ast.Module] = {}
        self.known: dict[str, tuple[list[str], dict[str, str]]] = {}

    def tree(self, rel: str) -> ast.Module:
        if rel not in self.trees:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", SyntaxWarning)
                    self.trees[rel] = ast.parse((self.root / rel).read_bytes(), filename=rel)
            except OSError as error:
                fail(f"cannot read {rel}: {error.strerror}")
            except (SyntaxError, ValueError) as error:
                fail(f"cannot parse {rel}: {error}")
        return self.trees[rel]

    def imports(self, rel: str) -> list[str]:
        """The repository files `rel` imports, in source order, each once."""
        here = (self.root / rel).parent
        found: list[str] = []
        for node in ast.walk(self.tree(rel)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found += self.resolve([self.root, here], alias.name.split("."))
            elif isinstance(node, ast.ImportFrom):
                parts = node.module.split(".") if node.module else []
                if node.level:
                    base = here
                    for _ in range(node.level - 1):
                        base = base.parent
                    bases = [base]
                else:
                    bases = [self.root, here]
                found += self.resolve(bases, parts)
                for alias in node.names:
                    found += self.resolve(bases, parts + [alias.name])
        return list(dict.fromkeys(found))

    def resolve(self, bases: list[Path], parts: list[str]) -> list[str]:
        """The repository module `parts` names from one of `bases`: the module file or the package's __init__."""
        if not parts:
            return []
        found = []
        for base in bases:
            candidate = base.joinpath(*parts)
            for target in (candidate.with_name(candidate.name + ".py"), candidate / "__init__.py"):
                rel = repository_module(self.root, target)
                if rel is not None:
                    found.append(rel)
        return found

    def candidates(self, rel: str) -> dict[str, tuple[str, str]]:
        """Every path-like text a string literal of `rel` spells, as `normalised: (spelled, kind)`."""
        found: dict[str, tuple[str, str]] = {}
        for node in ast.walk(self.tree(rel)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                texts = [(node.value, False)] + [(token, True) for token in node.value.split()]
            elif isinstance(node, ast.JoinedStr) and node.values:
                first = node.values[0]
                if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
                    continue
                texts = [(first.value + "{", False)]
            else:
                continue
            for text, token in texts:
                normalised = normalise(text, token)
                if normalised is not None:
                    found.setdefault(normalised[0], (text.strip(), normalised[1]))
        return found

    def file_reach(self, rel: str) -> tuple[list[str], dict[str, str]]:
        """What `rel` alone reaches: its imports, and each imported file and named path (`path/` for a directory)
        with how it is reached."""
        if rel not in self.known:
            imports = self.imports(rel)
            reach: dict[str, str] = {}
            for imported in imports:
                reach.setdefault(imported, f"imported by {rel}")
            for text, (spelled, kind) in self.candidates(rel).items():
                target = self.root / text
                if kind != "file" and target.is_dir():
                    reach.setdefault(text + SLASH, f"named as `{spelled}` in {rel}")
                elif kind != "dir" and (target.is_file() or text in self.changed):
                    reach.setdefault(text, f"named as `{spelled}` in {rel}")
            self.known[rel] = (imports, reach)
        return self.known[rel]

    def reach(self, module: str) -> dict[str, str]:
        """Everything `module` reaches, through the files it imports and the files they import."""
        reach: dict[str, str] = {}
        seen: set[str] = set()
        todo = [module]
        while todo:
            rel = todo.pop(0)
            if rel in seen:
                continue
            seen.add(rel)
            imports, found = self.file_reach(rel)
            for key, how in found.items():
                reach.setdefault(key, how if rel == module else f"{how} (imported)")
            todo += imports
        return reach


def test_modules(root: Path, start: Path, pattern: str) -> list[str]:
    """The test modules under `start`, as paths relative to the root, sorted; exit 2 when there is none."""
    if not start.is_dir():
        fail(f"{start} is not a directory")
    found = sorted(
        candidate.resolve().relative_to(root.resolve()).as_posix()
        for candidate in start.rglob("*.py")
        if candidate.is_file() and fnmatch.fnmatch(candidate.name, pattern)
    )
    if not found:
        fail(f"no module matching {pattern} under {start}")
    return found


def select(root: Path, start: Path, pattern: str, changed: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """The modules the changed paths reach: `(["all"] or the sorted modules, {module or "all" or "": reasons})`.

    `start` is relative to `root`. The reasons name each decision; "" holds the changed paths that reach no module.
    """
    start = root / start
    try:
        start_prefix = start.resolve().relative_to(root.resolve()).as_posix() + SLASH
    except ValueError:
        fail(f"{start} is not under {root}")
    modules = test_modules(root, start, pattern)
    mapper = Mapper(root, set(changed))
    reasons: dict[str, list[str]] = {}
    for entry in changed:
        if entry.startswith(start_prefix) and not fnmatch.fnmatch(entry.rpartition(SLASH)[2], pattern):
            reasons.setdefault("all", []).append(f"{entry} is under {start_prefix} and no test module: shared code")
        elif entry.startswith(ALL_PREFIXES):
            reasons.setdefault("all", []).append(f"{entry} is under {entry[: entry.index(SLASH) + 1]}")
        elif entry in ALL_NAMES:
            reasons.setdefault("all", []).append(f"{entry} builds the environment every module runs in")
    if "all" in reasons:
        return ["all"], {"all": reasons["all"]}
    for entry in changed:
        other = twin(entry)
        aliases = [entry] if other is None else [entry, other]
        reached = False
        if entry in modules:
            reasons.setdefault(entry, []).append(f"{entry} is the module itself")
            reached = True
        for module in modules:
            reach = mapper.reach(module)
            for alias in aliases:
                shown = alias if alias == entry else f"{alias} (the twin of {entry})"
                for key in [alias] + ancestors(alias):
                    if key in reach:
                        reasons.setdefault(module, []).append(f"{shown} is {key}, {reach[key]}")
                        reached = True
                        break
        if not reached:
            reasons.setdefault("", []).append(f"{entry} reaches no module")
    selected = sorted(module for module in reasons if module in modules)
    return selected, reasons


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="the base revision (the merge base with --head is the start)")
    parser.add_argument("--head", required=True, help="the head revision whose changes are read")
    parser.add_argument("--start", default="tests/unit", type=Path, help="the test modules' directory")
    parser.add_argument("--pattern", default="test*.py", help="the runner's discovery pattern for a module")
    parser.add_argument("--explain", action="store_true", help="print why each module was selected to stderr")
    args = parser.parse_args(argv)
    root = Path.cwd()
    changed = changed_paths(args.base, args.head)
    selected, reasons = select(root, args.start, args.pattern, changed)
    if args.explain:
        print(f"{PROGRAM}: {len(changed)} changed paths from {args.base}...{args.head}", file=sys.stderr)
        for key in sorted(reasons, key=lambda name: (name != "all", name == "", name)):
            for reason in reasons[key]:
                print(f"{PROGRAM}: {key or 'nothing'}: {reason}", file=sys.stderr)
        total = len(test_modules(root, root / args.start, args.pattern))
        count = "all modules" if selected == ["all"] else f"{len(selected)} of {total} modules"
        print(f"{PROGRAM}: {count} selected", file=sys.stderr)
    for module in selected:
        print(module)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
