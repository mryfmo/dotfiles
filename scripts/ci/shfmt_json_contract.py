#!/usr/bin/env python3
"""Prove that the pinned shfmt still produces the JSON nodes the repository's walkers read (regime-cutover U105).

`shfmt --to-json` has no stability statement and its wire format changed in 3.6.0 and 3.14.0. The walkers over it
(scripts/ci/masked-dirname-check.sh, the enforce-uv hook, scripts/lint-comparisons.py and
tests/unit/test_sandbox_portability.py) read fields with `.get()`, so a renamed field after a bump would yield no nodes,
no findings and a silent pass. Each of them runs this contract before its walk: the pinned shfmt
(scripts/ci/pinned-tool-version.sh) parses the fixtures under tests/fixtures/shfmt-json with `-ln bash --to-json`, and
their trees must hold, for every row of TABLE, a node of that kind carrying each listed field, and each listed value at
least once. The first difference is named and the exit status is 2: "could not judge", never "clean".

TABLE is the one place the node kinds, field names and the operator spellings the walkers read are written down;
tests/unit/test_shfmt_json_contract.py holds every walker's source to it. The fixtures are contract.sh, which the
formatting gate keeps formatted, and contract-backquotes, which holds the backquoted substitution that gate would
rewrite.

    python3 -I scripts/ci/shfmt_json_contract.py                        # the pinned shfmt on PATH, the fixtures
    python3 -I scripts/ci/shfmt_json_contract.py --tree A.json --tree B.json  # captured trees instead (the tests)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = (ROOT / "tests/fixtures/shfmt-json/contract.sh", ROOT / "tests/fixtures/shfmt-json/contract-backquotes")
PIN_CHECK = ROOT / "scripts/ci/pinned-tool-version.sh"
PIN_CONFIG = ROOT / "home/dot_mise/config.toml"
SHFMT = ("shfmt", "-ln", "bash", "--to-json")


class Kind(NamedTuple):
    """One node kind the walkers read.

    marker: None when the node carries `"Type": <kind>`; else the field whose presence, with no `Type`, names an untyped
    node (a statement, a redirect, a comment, a word).
    fields: the field names the walkers read, a nested one as a dotted path; shfmt omits an empty or false field, so
    each must appear on at least one node of the kind in the fixtures.
    values: field -> the literal values the walkers compare against, each produced at least once by the fixtures."""

    marker: str | None
    fields: tuple[str, ...]
    values: dict[str, tuple[object, ...]] = {}


TABLE: dict[str, Kind] = {
    "File": Kind(None, ("Stmts",)),
    "Stmt": Kind("Cmd", ("Cmd", "Pos.Line", "Pos.Offset", "End.Line", "End.Offset", "Redirs")),
    # `2> f` is Op ">" with the descriptor in N; the fixture's `2>` pins that spelling.
    "Redirect": Kind("Op", ("Op", "N", "Word", "Hdoc", "Pos.Offset", "End.Offset"), {"Op": (">", "<<")}),
    "Comment": Kind("Hash", ("Hash.Line", "Text", "Pos.Offset", "End.Offset")),
    "Word": Kind("Parts", ("Parts", "Pos.Line", "End.Line", "Pos.Offset", "End.Offset")),
    "CallExpr": Kind(None, ("Args", "Assigns", "Pos.Line")),
    "CmdSubst": Kind(None, ("Stmts", "Backquotes", "Pos.Line"), {"Backquotes": (True,)}),
    "ProcSubst": Kind(None, ("Stmts", "Op"), {"Op": ("<(",)}),
    "DblQuoted": Kind(None, ("Parts", "Pos.Line")),
    "SglQuoted": Kind(None, ("Value", "Dollar", "Pos.Line"), {"Dollar": (True,)}),
    "Lit": Kind(None, ("Value", "Pos.Line", "Pos.Offset", "End.Offset"), {"Value": ("a\\ b",)}),
    "ParamExp": Kind(None, ("Param.Value", "Length", "Index"), {"Length": (True,)}),
    "ExtGlob": Kind(None, ("Pattern.Value",)),
    "BinaryCmd": Kind(None, ("Op", "X", "Y"), {"Op": ("|", "&&")}),
    "TestClause": Kind(None, ("X",)),
    "BinaryTest": Kind(None, ("Op", "X", "Y"), {"Op": ("==",)}),
    "CaseClause": Kind(None, ("Word", "In", "Items")),
    "FuncDecl": Kind(None, ("Name", "Body")),
    "Block": Kind(None, ("Stmts",)),
    "Subshell": Kind(None, ("Stmts",)),
    "ArithmExp": Kind(None, ("X",)),
}
UNTYPED = {row.marker: kind for kind, row in TABLE.items() if row.marker}


class ContractError(Exception):
    """The parser's output does not match TABLE, or could not be produced; str() names the first difference."""


def nodes(tree: object) -> Iterator[dict]:
    """Every JSON object at or below tree, iteratively: a long && chain nests deeper than Python recurses."""
    todo = [tree]
    while todo:
        node = todo.pop()
        if isinstance(node, dict):
            yield node
            todo.extend(node.values())
        elif isinstance(node, list):
            todo.extend(node)


def kind(node: dict) -> str | None:
    """The TABLE kind of one node: its exact `Type`, else the untyped kind its marker field names; None otherwise."""
    if "Type" in node:
        return node["Type"] if node["Type"] in TABLE else None
    return next((UNTYPED[marker] for marker in UNTYPED if marker in node), None)


def count(tree: object) -> Counter[str]:
    """How many nodes of each TABLE kind the tree holds."""
    return Counter(k for node in nodes(tree) if (k := kind(node)) is not None)


def field(node: object, path: str) -> object:
    """The value at a dotted path, or None where any step is missing."""
    for step in path.split("."):
        if not isinstance(node, dict) or step not in node:
            return None
        node = node[step]
    return node


def check(trees: dict[str, object]) -> str | None:
    """The first difference between the trees (source name -> parsed JSON) and TABLE, or None when every row is
    satisfied by their nodes together."""
    where = ", ".join(trees)
    seen: dict[str, list[dict]] = {name: [] for name in TABLE}
    for source, tree in trees.items():
        if not isinstance(tree, dict) or tree.get("Type") != "File":
            return f"the root of {source} is no node with Type File"
        for node in nodes(tree):
            if (k := kind(node)) is not None:
                seen[k].append(node)
    for name, row in TABLE.items():
        if not seen[name]:
            return f"{where} holds no {name} node"
        for path in row.fields:
            if all(field(node, path) is None for node in seen[name]):
                return f"no {name} node of {where} has the field {path}"
        for path, values in row.values.items():
            for value in values:
                if not any(field(node, path) == value for node in seen[name]):
                    return f"no {name} node of {where} has {path} = {value!r}"
    return None


def pinned_shfmt() -> None:
    """Refuse unless PATH's shfmt is the version home/dot_mise/config.toml pins, by the repository's own check."""
    try:
        run = subprocess.run(
            ["bash", str(PIN_CHECK), str(PIN_CONFIG), "shfmt"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        raise ContractError(f"cannot run {PIN_CHECK.name}: {error}") from None
    if run.returncode != 0:
        raise ContractError(run.stderr.strip() or f"{PIN_CHECK.name} exited {run.returncode}")


def parse(text: bytes, source: str) -> dict:
    """The pinned shfmt's JSON tree of text, or a ContractError naming what failed."""
    try:
        run = subprocess.run(SHFMT, input=text, capture_output=True, check=False)
    except OSError as error:
        raise ContractError(f"cannot run shfmt: {error}") from None
    if run.returncode != 0:
        raise ContractError(f"shfmt cannot parse {source}: {run.stderr.decode(errors='replace').strip()}")
    try:
        tree = json.loads(run.stdout)
    except ValueError as error:
        raise ContractError(f"shfmt gave no JSON for {source}: {error}") from None
    if not isinstance(tree, dict):
        raise ContractError(f"shfmt gave no JSON object for {source}")
    return tree


def verify() -> Counter[str]:
    """Run the contract: the pinned shfmt parses the fixtures and their trees match TABLE. Returns the node counts
    the fixtures produced; raises ContractError naming the first difference."""
    pinned_shfmt()
    trees: dict[str, object] = {}
    for fixture in FIXTURES:
        source = str(fixture.relative_to(ROOT))
        try:
            text = fixture.read_bytes()
        except OSError as error:
            raise ContractError(f"cannot read {source}: {error}") from None
        trees[source] = parse(text, source)
    if (difference := check(trees)) is not None:
        raise ContractError(difference)
    return sum((count(tree) for tree in trees.values()), Counter())


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--tree", type=Path, action="append", metavar="FILE", help="check these captured JSON trees instead of parsing"
    )
    args = parser.parse_args(argv)
    try:
        if not args.tree:
            verify()
            return 0
        trees: dict[str, object] = {}
        for path in args.tree:
            try:
                trees[str(path)] = json.loads(path.read_text())
            except (OSError, ValueError) as error:
                raise ContractError(f"cannot read a JSON tree from {path}: {error}") from None
        if (difference := check(trees)) is not None:
            raise ContractError(difference)
        return 0
    except ContractError as error:
        print(f"shfmt-json-contract: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
