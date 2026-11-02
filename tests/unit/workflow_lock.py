"""The workflows' lockfile, `.github/workflows/actions.lock`, read by a YAML loader that refuses a repeated key
(regime-cutover U134 round 2).

`gh actions-lock` writes the file and GitHub's runner enforces it; the repository's own invariant over it is the
coverage test of tests/unit/test_workflow_security.py. Two things are shared from here.

The reader runs PyYAML under uv (the test interpreter has none: `uv run python` of a tree with no project) with a
SafeLoader whose construct_mapping refuses a duplicate mapping key. PyYAML's own SafeLoader keeps the last value and
says nothing, so a lockfile with two entries for one action read as one entry (the round-1 audit, U134-2d9e0a8c); a
merge key (`<<`) is refused with it, since a workflow or a lockfile has no use for one and a merged mapping is another
document than the file shows. A refused file is reported by name with PyYAML's message, which names the key and both
lines.

expected_uses() is the one place the regime tests take an action's `uses:` reference from: the lockfile's entry for
`<owner>/<repo>`, which `gh actions-lock` and a Dependabot bump regenerate with the workflow's tag, so a bump that
moves the tag needs no test edit (the stall of #548 was a hand-edited pin constant).
"""

import functools
import json
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
LOCKFILE = WORKFLOWS / "actions.lock"
UV = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
# Run by the uv interpreter: each file named on the command line as JSON, `{"document": ...}` when the loader took it
# and `{"error": "<PyYAML's message>"}` when it refused the file.
READER = '''
import json
import sys

import yaml

MERGE = "tag:yaml.org,2002:merge"


class Loader(yaml.SafeLoader):
    """SafeLoader without its silence over a repeated key: the second occurrence is a ConstructorError that names the
    key and the line of the first, as a syntax error names its line."""

    def construct_mapping(self, node, deep=False):
        seen = {}
        for key_node, _ in node.value:
            if key_node.tag == MERGE:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark, "found a merge key", key_node.start_mark
                )
            key = self.construct_object(key_node, deep=deep)
            try:
                first = seen.get(key)
            except TypeError:  # an unhashable key; the parent class refuses it by name
                continue
            if first is not None:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}, first at line {first}",
                    key_node.start_mark,
                )
            seen[key] = key_node.start_mark.line + 1
        return super().construct_mapping(node, deep=deep)


read = {}
for name in sys.argv[1:]:
    with open(name, encoding="utf-8") as handle:
        try:
            read[name] = {"document": yaml.load(handle, Loader=Loader)}
        except yaml.YAMLError as error:
            read[name] = {"error": str(error)}
print(json.dumps(read, default=str))
'''


class Read(NamedTuple):
    document: object
    error: str | None


class RefusedYaml(Exception):
    """The loader refused the file: a duplicate key, a merge key or a syntax error, with PyYAML's message."""


def read_yaml(paths: Iterable[Path]) -> dict[Path, Read]:
    """Every file parsed in one uv run, each either a document or the loader's refusal."""
    paths = list(paths)
    result = subprocess.run([*UV, "-c", READER, *map(str, paths)], capture_output=True, text=True, check=True)
    read = json.loads(result.stdout)
    return {path: Read(read[str(path)].get("document"), read[str(path)].get("error")) for path in paths}


def load_yaml(path: Path) -> object:
    """The one file's document, or RefusedYaml naming the file and PyYAML's message."""
    (read,) = read_yaml([path]).values()
    if read.error is not None:
        raise RefusedYaml(f"{path.name}: {read.error}")
    return read.document


@functools.cache
def lockfile() -> dict:
    lock = load_yaml(LOCKFILE)
    if not isinstance(lock, dict) or not isinstance(lock.get("dependencies"), dict):
        raise AssertionError(f"{LOCKFILE.name} holds no dependencies mapping: {lock!r}")
    return lock


def expected_uses(owner_repo: str) -> str:
    """The `uses:` reference the lockfile holds for one action, `<owner>/<repo>@<tag>`: the one entry keyed by that
    owner and repo. Two entries (a bump that left the old one behind) or none are refused by name, not chosen from."""
    keys = [key for key in lockfile()["dependencies"] if isinstance(key, str) and key.rpartition("@")[0] == owner_repo]
    if len(keys) != 1:
        raise AssertionError(f"{LOCKFILE.name} holds {len(keys)} entries for {owner_repo}, not one: {keys}")
    return keys[0]
