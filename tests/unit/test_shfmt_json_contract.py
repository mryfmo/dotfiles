#!/usr/bin/env python3
"""Exercise scripts/ci/shfmt_json_contract.py and the walkers that run it (regime-cutover U105, plan P-23).

The pinned shfmt must parse the fixtures under tests/fixtures/shfmt-json into the node table; the captured trees
beside them are the parser's own output, regenerated with

    cd tests/fixtures/shfmt-json && for f in contract.sh contract-backquotes; do
        shfmt -ln bash --to-json < "$f" > "${f%.sh}.json"; done

and are what the negative cases here alter. The decision rows need shfmt on PATH: the mise config installs it on the
hosts and CI puts the pinned version there.

The table is held to the walkers by extraction, not by a hand-written list: every field a walker reads from the tree
and every literal it compares against a field is collected from the walker's source (Python by its syntax tree, the
hook's jq programs by their paths), bound to the node kinds the walker's own Type tests establish for the variable
it reads, and must be in TABLE for each of those kinds (round 4).

The module's own reads are held the same way (round 7): STATUS_READS lists every status read of
scripts/ci/shfmt_json_contract.py (the pin check's status, shfmt's status and output, the JSON decode, each OSError
of a run or a file read) with the test that injects its failure; the list is checked against the module's source, so
a read added without an injection test fails the suite. The injections put a fake shfmt on PATH whose `--version`
satisfies the pin check, so they need no real shfmt.
"""

from __future__ import annotations

import ast
import contextlib
import io
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Iterator, NamedTuple
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ci"))
import shfmt_json_contract as contract  # noqa: E402

sys.path.insert(0, str(ROOT / "tests/unit"))
import test_sandbox_portability as sandbox  # noqa: E402

MODULE = ROOT / "scripts/ci/shfmt_json_contract.py"
FIXTURES = ROOT / "tests/fixtures/shfmt-json"
FIXTURE = FIXTURES / "contract.sh"
BACKQUOTES = FIXTURES / "contract-backquotes"
CAPTURES = {FIXTURE: FIXTURES / "contract.json", BACKQUOTES: FIXTURES / "contract-backquotes.json"}
CHECK = ROOT / "scripts/ci/masked-dirname-check.sh"
PRODUCER_CHECK = ROOT / "scripts/ci/producer-status-check.sh"
GIT_CHECK = ROOT / "scripts/ci/git-invocation-check.sh"
HOOK = ROOT / "home/dot_claude/hooks/executable_enforce-uv.sh"
LINT = ROOT / "scripts/lint-comparisons.py"
NESTED_LINE = 7  # contract.sh: the one command substitution that opens inside another
BACKQUOTES_LINE = 4  # contract-backquotes: the backquoted substitution, inside another
MESSAGE = "a command substitution inside another one loses its status; capture it first, or split a path in the shell"
# A file node whose statements carry no Cmd: the shape a renamed field leaves, which every walk must refuse to read as
# "no findings".
UNREADABLE_TREE = {"Type": "File", "Stmts": [{"Command": {"Type": "CallExpr"}}]}
# The walkers over shfmt's JSON, each with the language of its walk and the region of its source that holds it (None:
# the whole file). The extractor below reads them.
WALKERS = {
    CHECK: ("python", re.compile(r"cat << 'PY'\n(.*?)\nPY\n", re.DOTALL)),
    PRODUCER_CHECK: ("python", re.compile(r"cat << 'PY'\n(.*?)\nPY\n", re.DOTALL)),
    GIT_CHECK: ("python", re.compile(r"cat << 'PY'\n(.*?)\nPY\n", re.DOTALL)),
    HOOK: ("jq", re.compile(r"function split_segments\(\) \{\n(.*?)\n\}\n", re.DOTALL)),
    LINT: ("python", None),
    ROOT / "tests/unit/test_sandbox_portability.py": ("python", None),
}
# Reads the extractor finds that TABLE need not hold, each with its reason: the list may shrink, never grow, and the
# test asserts its exact contents. Empty: every read of every walker is in the table for its kind.
EXCEPTIONS: dict[str, str] = {}


def on_ci_runner() -> bool:
    """scripts/lib/ci-runner.sh decides, never the generic CI variable an agent shell exports."""
    probe = 'source "$1" && is_ci_runner'
    return (
        subprocess.run(["bash", "-c", probe, "_", str(ROOT / "scripts/lib/ci-runner.sh")], check=False).returncode == 0
    )


def pinned_version() -> str:
    return tomllib.loads((ROOT / "home/dot_mise/config.toml").read_text())["tools"]["http:shfmt"]["version"]


def captures() -> dict[str, str]:
    """The captured tree text of each fixture, by the fixture's name."""
    return {fixture.name: capture.read_text() for fixture, capture in CAPTURES.items()}


def hidden_tree(text: str) -> str:
    """The captured tree as the literal body of a quoted heredoc: every node is still there for the contract's reader,
    none for masked-dirname-check's walk, which skips such a body (the one place the two traversals differ)."""
    heredoc = {
        "Op": "<<",
        "Word": {"Parts": [{"Type": "SglQuoted", "Value": "EOF", "Pos": {"Line": 1}}]},
        "Hdoc": {"Parts": [json.loads(text)]},
    }
    stmt = {"Cmd": {"Type": "CallExpr", "Args": [], "Pos": {"Line": 1}}, "Pos": {"Line": 1}, "Redirs": [heredoc]}
    return json.dumps({"Type": "File", "Stmts": [stmt]})


# --- The extractor: what each walker reads from the tree, from its source -------------------------------------------

MISSING = object()  # a Read with no literal
FIELD = re.compile(r"[A-Z]\w*")  # every field of shfmt's JSON is spelled so; a lower-case key is some other dict's
SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
TESTS = (ast.Eq, ast.NotEq, ast.In, ast.NotIn)
JQ_PROGRAM = re.compile(r"jq -r '([^']*)'")
JQ_HAS = re.compile(r'has\("([A-Z]\w*)"\)')
JQ_PATH = re.compile(r'\.([A-Z]\w*(?:\.[A-Z]\w*)*)\??(?:\s*(?:==|!=)\s*"([^"]*)")?')


class Read(NamedTuple):
    """One read of shfmt's tree in a walker's source.

    kinds: the node kinds the walker's own Type and marker tests bind the variable to where the read happens; None
    when no test reaches it, so the table as a whole must hold the path.
    path: the dotted field path. strict: a subscript, which every bound kind must carry; else a tolerant read (.get, a
    key test, a jq path), which at least one bound kind must carry, since a read of a field none of them has reads
    nothing. literal: the value compared against the field, else MISSING."""

    kinds: frozenset[str] | None
    path: str
    strict: bool
    literal: object = MISSING


class Chain(NamedTuple):
    """A field access `base["A"]["B"]`, `base.get("A")`, `(base.get("A") or {}).get("B")`: the steps (each a set of
    alternatives, for `cmd["Y" if last else "X"]`), whether every step is a subscript, and the index and default
    expressions passed over, which may hold reads of their own."""

    base: ast.expr
    steps: list[frozenset[str]]
    strict: bool
    extras: list[ast.expr]


def string_set(expr: ast.expr, consts: dict[str, frozenset[str]]) -> frozenset[str] | None:
    """The strings of a string constant, a tuple, set or list of them, a name bound to one (the lint's LITS), or an
    if-expression between two of those; None for anything else."""
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return frozenset({expr.value})
    if isinstance(expr, (ast.Tuple, ast.Set, ast.List)):
        parts = [string_set(elt, consts) for elt in expr.elts]
        return frozenset().union(*parts) if parts and all(part is not None for part in parts) else None
    if isinstance(expr, ast.IfExp):
        yes, no = string_set(expr.body, consts), string_set(expr.orelse, consts)
        return yes | no if yes is not None and no is not None else None
    return consts.get(expr.id) if isinstance(expr, ast.Name) else None


def strip(expr: ast.expr) -> tuple[ast.expr, list[ast.expr]]:
    """expr without its `or {}` / `or []` defaults and its list indexes (`[-1]`, `[0]`, `[i]`), with those indexes."""
    extras: list[ast.expr] = []
    while True:
        if (
            isinstance(expr, ast.BoolOp)
            and isinstance(expr.op, ast.Or)
            and len(expr.values) == 2
            and isinstance(expr.values[1], (ast.Dict, ast.List, ast.Constant))
        ):
            expr = expr.values[0]
        elif isinstance(expr, ast.Subscript) and not fields(expr.slice):
            extras.append(expr.slice)
            expr = expr.value
        else:
            return expr, extras


def fields(expr: ast.expr) -> frozenset[str] | None:
    """The field names a subscript or .get key spells: a string constant or an if-expression between two, each a
    field spelling; None for a list index, a slice or a variable key."""
    keys = string_set(expr, {})
    return keys if keys and all(FIELD.fullmatch(key) for key in keys) else None


def chain(expr: ast.expr) -> Chain | None:
    """The field access chain expr is, else None."""
    steps: list[frozenset[str]] = []
    strict, extras = True, []
    while True:
        expr, passed = strip(expr)
        extras += passed
        if isinstance(expr, ast.Subscript) and (keys := fields(expr.slice)):
            steps.append(keys)
            expr = expr.value
        elif (
            isinstance(expr, ast.Call)
            and isinstance(expr.func, ast.Attribute)
            and expr.func.attr == "get"
            and expr.args
            and (keys := fields(expr.args[0]))
        ):
            steps.append(keys)
            strict = False
            extras += expr.args[1:]
            expr = expr.func.value
        else:
            break
    return Chain(expr, steps[::-1], strict, extras) if steps else None


def names(target: ast.expr, value: ast.expr) -> Iterator[tuple[str, ast.expr]]:
    """(name, expression) per name an assignment binds: `a = e`, `a, b = e1, e2`, `(a := e)`."""
    if isinstance(target, ast.Name):
        yield target.id, value
    elif isinstance(target, ast.Tuple) and isinstance(value, ast.Tuple) and len(target.elts) == len(value.elts):
        for inner, expr in zip(target.elts, value.elts):
            yield from names(inner, expr)


class Scope:
    """One Python function (or the module body) of a walker: the names it binds to tree nodes, the kinds it tests them
    for, and every read it makes, bound to the kinds the tests establish where the read happens.

    A test narrows the variable for what it guards: the later operands of an `and`, the body of an `if` or of a
    conditional expression and the later clauses of a comprehension take the tested kinds; an `else` takes the rest of
    the kinds the scope tests the variable for, or no kind at all once they are exhausted. A read no test guards takes
    every kind the scope tests the variable for, since the walker reads it on each of them."""

    def __init__(self, root: ast.AST, consts: dict[str, frozenset[str]]) -> None:
        self.root = root
        self.consts = dict(consts)
        self.type_alias: dict[str, str] = {}  # `kind = part["Type"]`: kind -> part
        self.sub_alias: dict[str, tuple[str, str]] = {}  # `param = part.get("Param") or {}`: param -> (part, "Param")
        self.key_alias: dict[str, str] = {}  # `for key, value in node.items()`: key -> node
        self.kinds: dict[str, set[str]] = {}  # variable -> every kind the scope tests it for
        self.named: set[str] = set()  # every kind a Type test in the scope spells
        self.reads: list[Read] = []
        self.gather()
        self.visit(root, {})

    def own(self) -> Iterator[ast.AST]:
        """The scope's own nodes: a nested function is its own scope."""
        todo = [self.root]
        while todo:
            node = todo.pop()
            yield node
            todo.extend(c for c in ast.iter_child_nodes(node) if not isinstance(c, (*SCOPES, ast.ClassDef)))

    @staticmethod
    def var(expr: ast.expr) -> str | None:
        """The variable expr reads (its defaults and list indexes aside), else None."""
        expr, _ = strip(expr)
        return expr.id if isinstance(expr, ast.Name) else None

    def gather(self) -> None:
        for node in self.own():
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)) and node.value is not None:
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    for name, value in names(target, node.value):
                        if (strings := string_set(value, self.consts)) is not None:
                            self.consts[name] = strings
                        if (c := chain(value)) and (var := self.var(c.base)) and all(len(s) == 1 for s in c.steps):
                            path = [next(iter(s)) for s in c.steps]
                            if path == ["Type"]:
                                self.type_alias[name] = var
                            elif path[-1] != "Type":
                                self.sub_alias[name] = (var, ".".join(path))
            generators = (
                node.generators if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)) else []
            )
            for target, source in [(g.target, g.iter) for g in generators] + (
                [(node.target, node.iter)] if isinstance(node, ast.For) else []
            ):
                if (
                    isinstance(source, ast.Call)
                    and isinstance(source.func, ast.Attribute)
                    and source.func.attr in ("items", "keys")
                ):
                    source = source.func.value
                first = target.elts[0] if isinstance(target, ast.Tuple) and target.elts else target
                if isinstance(first, ast.Name) and (var := self.var(source)):
                    self.key_alias[first.id] = var
        for node in self.own():
            for var, kinds, _ in self.kind_tests(node):
                self.kinds.setdefault(var, set()).update(kinds)
                self.named.update(kinds)
        for name in [name for name in self.sub_alias if name in self.kinds]:  # a node of its own, not a sub-record
            del self.sub_alias[name]

    def type_var(self, expr: ast.expr) -> str | None:
        """The variable whose Type expr reads: `v["Type"]`, `v.get("Type")` or a name assigned from one."""
        if isinstance(expr, ast.Name):
            return self.type_alias.get(expr.id)
        c = chain(expr)
        return self.var(c.base) if c and c.steps == [frozenset({"Type"})] else None

    def kind_tests(self, expr: ast.expr) -> list[tuple[str, frozenset[str], bool]]:
        """(variable, kinds, positive) for the kind test expr is: a comparison of the variable's Type with kind
        spellings, a marker key test (`"Cmd" in n`), or `not` of one."""
        if isinstance(expr, ast.UnaryOp) and isinstance(expr.op, ast.Not):
            return [(var, kinds, not positive) for var, kinds, positive in self.kind_tests(expr.operand)]
        if not isinstance(expr, ast.Compare) or len(expr.ops) != 1 or not isinstance(expr.ops[0], TESTS):
            return []
        positive = isinstance(expr.ops[0], (ast.Eq, ast.In))
        left, right = expr.left, expr.comparators[0]
        if (
            isinstance(expr.ops[0], (ast.In, ast.NotIn))
            and isinstance(left, ast.Constant)
            and left.value in contract.UNTYPED
        ):
            var = self.var(right)
            return [(var, frozenset({contract.UNTYPED[left.value]}), positive)] if var else []
        var, kinds = self.type_var(left), string_set(right, self.consts)
        return [(var, kinds, positive)] if var and kinds is not None else []

    def bound(self, var: str, ctx: dict[str, frozenset[str] | None]) -> frozenset[str] | None:
        if var in ctx:
            return ctx[var]
        kinds = self.kinds.get(var)
        return frozenset(kinds) if kinds else None

    def narrow(self, ctx: dict, test: ast.expr, positive: bool) -> dict:
        """ctx for what test guards when it holds (positive) or fails."""
        tests = self.kind_tests(test)
        if not tests and isinstance(test, ast.BoolOp):
            if isinstance(test.op, ast.And) is positive:  # every operand of a true `and`, of a false `or`
                for value in test.values:
                    ctx = self.narrow(ctx, value, positive)
            return ctx
        ctx = dict(ctx)
        for var, kinds, holds in tests:
            if holds is positive:
                ctx[var] = kinds
            else:
                current = self.bound(var, ctx)
                ctx[var] = (current - kinds or None) if current is not None else None
        return ctx

    def emit(self, c: Chain, ctx: dict, literal: object = MISSING) -> None:
        var = self.var(c.base)
        if var is None:  # a dict some call returned, not a node
            return
        prefix: list[str] = []
        if var in self.sub_alias:
            var, path = self.sub_alias[var]
            prefix = path.split(".")
        kinds = self.bound(var, ctx)
        for steps in itertools.product(*c.steps):
            path = prefix + list(steps)
            if path[-1] == "Type":  # the discriminator, read to test a kind; its holder is the read
                path = path[:-1]
            if path:
                self.reads.append(Read(kinds, ".".join(path), c.strict, literal))

    def compare(self, node: ast.Compare, ctx: dict) -> None:
        """The literals node compares against a field, and the marker a marker test reads."""
        tests = self.kind_tests(node)
        if tests:
            if isinstance(node.left, ast.Constant) and node.left.value in contract.UNTYPED:
                self.reads.append(Read(self.bound(tests[0][0], ctx), node.left.value, False))
            return
        if len(node.ops) != 1 or not isinstance(node.ops[0], TESTS):
            return
        left, right = node.left, node.comparators[0]
        if (c := chain(left)) and (strings := string_set(right, self.consts)) is not None:
            for literal in sorted(strings):
                self.emit(c, ctx, literal)
        elif isinstance(left, ast.Constant) and isinstance(left.value, str):
            if isinstance(right, (ast.List, ast.Tuple, ast.Set)):
                elts = right.elts
            else:  # `"\\" in part["Value"]` asks whether the text holds a backslash, not what the field spells
                elts = [right] if isinstance(node.ops[0], (ast.Eq, ast.NotEq)) else []
            for elt in elts:
                if (c := chain(elt)) is not None:
                    self.emit(c, ctx, left.value)
        elif isinstance(left, ast.Name) and left.id in self.key_alias and (strings := string_set(right, self.consts)):
            kinds = self.bound(self.key_alias[left.id], ctx)
            self.reads.extend(Read(kinds, key, False) for key in sorted(strings) if FIELD.fullmatch(key))

    def visit(self, node: ast.AST, ctx: dict) -> None:
        if node is not self.root and isinstance(node, (*SCOPES, ast.ClassDef)):
            return
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
            for value in node.values:
                self.visit(value, ctx)
                ctx = self.narrow(ctx, value, True)
            return
        if isinstance(node, (ast.If, ast.IfExp, ast.While)):
            self.visit(node.test, ctx)
            yes, no = self.narrow(ctx, node.test, True), self.narrow(ctx, node.test, False)
            for child in node.body if isinstance(node.body, list) else [node.body]:
                self.visit(child, yes)
            for child in node.orelse if isinstance(node.orelse, list) else [node.orelse]:
                self.visit(child, no)
            return
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for generator in node.generators:
                self.visit(generator.iter, ctx)
                for cond in generator.ifs:
                    self.visit(cond, ctx)
                    ctx = self.narrow(ctx, cond, True)
            for elt in [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]:
                self.visit(elt, ctx)
            return
        if isinstance(node, ast.Compare):
            self.compare(node, ctx)
        elif (c := chain(node)) is not None:
            self.emit(c, ctx)
            for extra in c.extras:
                self.visit(extra, ctx)
            return
        for child in ast.iter_child_nodes(node):
            self.visit(child, ctx)


def python_reads(source: str) -> tuple[set[str], list[Read]]:
    """(the kinds the source spells in Type tests, its reads) for a Python walker."""
    module = ast.parse(source)
    consts: dict[str, frozenset[str]] = {}
    for node in module.body:
        names_bound = [t.id for t in node.targets if isinstance(t, ast.Name)] if isinstance(node, ast.Assign) else []
        if len(names_bound) == 1 and (strings := string_set(node.value, consts)) is not None:
            consts[names_bound[0]] = strings
    scopes = [Scope(module, consts)] + [Scope(node, consts) for node in ast.walk(module) if isinstance(node, SCOPES)]
    return set().union(*(scope.named for scope in scopes)), [read for scope in scopes for read in scope.reads]


def jq_reads(source: str) -> tuple[set[str], list[Read]]:
    """(the kinds the jq programs compare a Type with, their reads) for the hook: each `jq -r '...'` program is one
    scope, its object bound to the untyped kind a marker it tests or reads names."""
    named: set[str] = set()
    reads: list[Read] = []
    for program in JQ_PROGRAM.findall(source):
        kinds: set[str] = set()
        found: list[tuple[str, bool, object]] = []
        for marker in JQ_HAS.findall(program):
            kinds.update([contract.UNTYPED[marker]] if marker in contract.UNTYPED else [])
            found.append((marker, False, MISSING))
        for match in JQ_PATH.finditer(program):
            steps, literal = match[1].split("."), match[2]
            if steps[0] in contract.UNTYPED:
                kinds.add(contract.UNTYPED[steps[0]])
            if steps[-1] == "Type":
                named.update([literal] if literal is not None else [])
                steps, literal = steps[:-1], None
            if steps:
                found.append((".".join(steps), True, MISSING if literal is None else literal))
        reads += [Read(frozenset(kinds) or None, path, strict, literal) for path, strict, literal in found]
    return named, reads


def walker_reads(path: Path) -> tuple[set[str], list[Read]]:
    language, region = WALKERS[path]
    text = path.read_text()
    if region is not None:
        match = region.search(text)
        assert match is not None, f"{path.name}: the walker's source region was not found"
        text = match.group(1)
    return (python_reads if language == "python" else jq_reads)(text)


def holds(kind: str, read: Read) -> bool:
    """Whether TABLE's row for kind carries the read's path (or a path below it), and its literal if it has one."""
    row = contract.TABLE[kind]
    if read.literal is MISSING:
        return any(field == read.path or field.startswith(read.path + ".") for field in row.fields)
    return read.literal in row.values.get(read.path, ())


def misses(walker: str, named: set[str], reads: list[Read]) -> set[str]:
    """Each kind, field or literal the walker reads that TABLE lacks for the kind it is bound to, named."""
    out = {f"{walker}: kind {name}" for name in named - set(contract.TABLE)}
    for read in reads:
        suffix = "" if read.literal is MISSING else f" = {read.literal!r}"
        kinds = sorted(kind for kind in read.kinds or () if kind in contract.TABLE)
        if not kinds:
            if not any(holds(kind, read) for kind in contract.TABLE):
                out.add(f"{walker}: {read.path}{suffix}")
        elif read.strict:
            out.update(f"{walker}: {kind}.{read.path}{suffix}" for kind in kinds if not holds(kind, read))
        elif not any(holds(kind, read) for kind in kinds):
            out.add(f"{walker}: {'|'.join(kinds)}.{read.path}{suffix}")
    return out


def module_check(*trees: str) -> subprocess.CompletedProcess[str]:
    """The module's CLI over captured tree files."""
    with tempfile.TemporaryDirectory() as temp:
        args = []
        for n, text in enumerate(trees):
            path = Path(temp) / f"tree-{n}.json"
            path.write_text(text)
            args += ["--tree", str(path)]
        return subprocess.run([sys.executable, "-I", str(MODULE), *args], capture_output=True, text=True, check=False)


# --- The module's own reads: every status read, and the test that injects its failure -------------------------------

# One row per status read in scripts/ci/shfmt_json_contract.py, as status_reads() extracts them from its source: the
# function that reads, what it reads (`status`: a returncode test; `output`: the bytes a run printed; `json`: a JSON
# decode; `OSError`: a run or a file read that raised), and the test (`Class.method` in this module) that injects the
# failure. A read with no row, a row no read needs, or a named test that does not exist fails the suite.
STATUS_READS: dict[tuple[str, str], str] = {
    (
        "pinned_shfmt",
        "OSError",
    ): "ContractReadTest.test_a_pin_check_that_cannot_run_or_exits_without_a_diagnostic_is_refused",
    (
        "pinned_shfmt",
        "status",
    ): "ContractReadTest.test_a_shfmt_that_is_not_the_pin_is_refused_before_any_fixture_is_parsed",
    (
        "parse",
        "OSError",
    ): "ContractReadTest.test_a_shfmt_that_cannot_be_run_or_a_fixture_that_cannot_be_read_is_refused",
    ("parse", "status"): "ContractReadTest.test_a_fixture_parse_that_exits_nonzero_is_refused_naming_the_status",
    ("parse", "output"): "ContractReadTest.test_a_fixture_parse_that_prints_no_tree_or_no_json_object_is_refused",
    ("parse", "json"): "ContractReadTest.test_a_fixture_parse_that_prints_no_tree_or_no_json_object_is_refused",
    ("verified_trees", "OSError"): (
        "ContractReadTest.test_a_shfmt_that_cannot_be_run_or_a_fixture_that_cannot_be_read_is_refused"
    ),
    ("main", "OSError"): "ContractReadTest.test_a_tree_file_that_cannot_be_read_is_refused_naming_it",
    ("main", "json"): "ContractTableTest.test_a_tree_that_is_no_json_object_is_refused",
}
# A shfmt on a test's PATH: `--version` runs the version answer (the pin check reads it), any other call the answer.
FAKE_SHFMT = """#!/bin/sh
[ "$1" = --version ] && {{ {version}; }}
{answer}
"""


def status_reads(source: str) -> set[tuple[str, str]]:
    """(function, read) per status read in a Python source: a `returncode` test, a `stdout` read, a `.loads` call and
    an `except` clause that catches OSError, each in the function whose body makes it."""
    out: set[tuple[str, str]] = set()
    for function in ast.walk(ast.parse(source)):
        if not isinstance(function, ast.FunctionDef):
            continue
        for node in ast.walk(function):
            if isinstance(node, ast.Attribute) and node.attr in ("returncode", "stdout"):
                out.add((function.name, "status" if node.attr == "returncode" else "output"))
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "loads":
                out.add((function.name, "json"))
            elif isinstance(node, ast.ExceptHandler) and node.type is not None:
                caught = node.type.elts if isinstance(node.type, ast.Tuple) else [node.type]
                if any(isinstance(name, ast.Name) and name.id == "OSError" for name in caught):
                    out.add((function.name, "OSError"))
    return out


def fake_shfmt_env(temp: Path, answer: str, version: str | None = None) -> dict[str, str]:
    """An environment whose PATH holds the pin check's tools (bash, awk) and a shfmt whose `--version` runs version
    (by default it prints the pin and exits 0) and whose every other call runs answer; a fresh directory under temp."""
    bin_dir = Path(tempfile.mkdtemp(dir=temp))
    for tool in ("bash", "awk"):
        (bin_dir / tool).symlink_to(shutil.which(tool))
    fake = bin_dir / "shfmt"
    fake.write_text(FAKE_SHFMT.format(version=version or f"echo v{pinned_version()}; exit 0", answer=answer))
    fake.chmod(0o755)
    return {"PATH": str(bin_dir), "HOME": str(temp)}


def module_run(env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    """The module's CLI under env (the parser is whatever shfmt env's PATH holds)."""
    return subprocess.run(
        [sys.executable, "-I", str(MODULE), *args], capture_output=True, text=True, check=False, env=env
    )


class ContractTableTest(unittest.TestCase):
    """The table against the captured trees: no shfmt needed."""

    def loaded(self, **altered: str) -> dict[str, object]:
        texts = {**captures(), **altered}
        return {name: json.loads(text) for name, text in texts.items()}

    def test_the_captured_trees_satisfy_every_row(self) -> None:
        trees = self.loaded()
        self.assertIsNone(contract.check(trees))
        counts = sum((contract.count(tree) for tree in trees.values()), contract.Counter())
        self.assertEqual(set(contract.TABLE), {kind for kind in counts if counts[kind]})
        self.assertGreaterEqual(contract.count(trees[FIXTURE.name])["CmdSubst"], 2, "a nested substitution needs two")

    def test_renaming_type_in_the_capture_fails_the_contract(self) -> None:
        renamed = captures()[FIXTURE.name].replace('"Type"', '"type"')
        self.assertEqual(
            f"the root of {FIXTURE.name} is no node with Type File",
            contract.check(self.loaded(**{FIXTURE.name: renamed})),
        )
        result = module_check(renamed, captures()[BACKQUOTES.name])
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertRegex(
            result.stderr, r"^shfmt-json-contract: the root of \S+/tree-0.json is no node with Type File\n$"
        )
        self.assertEqual("", result.stdout)

    def test_a_missing_field_or_a_changed_spelling_is_named(self) -> None:
        where = f"{FIXTURE.name}, {BACKQUOTES.name}"
        cases = {
            ('"Backquotes"', '"Backquote"'): f"no CmdSubst node of {where} has the field Backquotes",
            ('"Op": "|"', '"Op": "pipe"'): f"no BinaryCmd node of {where} has Op = '|'",
            ('"Op": "!="', '"Op": "!=="'): f"no BinaryTest node of {where} has Op = '!='",
            ('"Type": "CmdSubst"', '"Type": "CommandSubstitution"'): f"{where} holds no CmdSubst node",
            ('"Hdoc"', '"Heredoc"'): f"no Redirect node of {where} has the field Hdoc",
            ('"Cmd"', '"Command"'): f"{where} holds no Stmt node",
        }
        for (old, new), expected in cases.items():
            with self.subTest(change=f"{old} -> {new}"):
                altered = {name: text.replace(old, new) for name, text in captures().items()}
                self.assertNotEqual(altered, captures())
                self.assertEqual(expected, contract.check(self.loaded(**altered)))

    def test_a_tree_that_is_no_json_object_is_refused(self) -> None:
        where = r"\S+/tree-0\.json"
        cases = {
            "not-json": rf"cannot read a JSON tree from {where}: Expecting value: line 1 column 1 \(char 0\)",
            "null": rf"the root of {where} is no node with Type File",
            "[]": rf"the root of {where} is no node with Type File",
            '{"Type": "Word"}': rf"the root of {where} is no node with Type File",
        }
        for tree, cause in cases.items():
            with self.subTest(tree=tree):
                result = module_check(tree, captures()[BACKQUOTES.name])
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertRegex(result.stderr, rf"^shfmt-json-contract: {cause}\n$")
                self.assertEqual("", result.stdout)

    def test_the_extractor_binds_each_read_to_the_kinds_the_walker_tests(self) -> None:
        # Every shape the walkers use: an alias of Type, an `and` guard, an if/elif whose else exhausts the tested
        # kinds, a sub-record alias, an unguarded strict read (every kind the function tests), a comprehension
        # guard with literals, a key alias over a tuple of names, a marker test and an if-expression key.
        sample = """
LITS = ("Lit", "SglQuoted")


def walk(node, part):
    kind = node["Type"]
    if kind == "CmdSubst":
        return node["Pos"]["Line"]
    elif node.get("Hdoc"):
        return node["Word"]
    param = part.get("Param") or {}
    line = part["Pos"]["Line"]
    return part["Type"] in LITS and param.get("Value") == "TMPDIR" or part.get("Type") == "ParamExp" and line


def tests(cmd):
    at = cmd["Pos"]["Line"]
    found = [n for n in nodes(cmd) if n.get("Type") == "BinaryTest" and n["Op"] in ("==", "!=")]
    keep = ("X", "Y") if cmd.get("Type") == "BinaryCmd" else ("Cmd",)
    return at, [v for k, v in cmd.items() if k in keep], found, "Cmd" in cmd, cmd["Y" if at else "X"]
"""
        named, reads = python_reads(sample)
        self.assertEqual({"CmdSubst", "Lit", "SglQuoted", "ParamExp", "BinaryTest", "BinaryCmd", "Stmt"}, named)
        parts, stmts = frozenset({"Lit", "SglQuoted", "ParamExp"}), frozenset({"BinaryCmd", "Stmt"})
        expected = {
            Read(frozenset({"CmdSubst"}), "Pos.Line", True),
            Read(None, "Hdoc", False),
            Read(None, "Word", True),
            Read(parts, "Param", False),
            Read(parts, "Pos.Line", True),
            Read(frozenset({"Lit", "SglQuoted"}), "Param.Value", False),
            Read(frozenset({"Lit", "SglQuoted"}), "Param.Value", False, "TMPDIR"),
            Read(stmts, "Pos.Line", True),
            Read(frozenset({"BinaryTest"}), "Op", True),
            Read(frozenset({"BinaryTest"}), "Op", True, "=="),
            Read(frozenset({"BinaryTest"}), "Op", True, "!="),
            Read(stmts, "Cmd", False),
            Read(stmts, "X", False),
            Read(stmts, "Y", False),
            Read(stmts, "X", True),
            Read(stmts, "Y", True),
        }
        self.assertEqual(expected, set(reads))
        # A strict read is named per kind that lacks it, a tolerant one once, for the kinds none of which has it.
        self.assertEqual(
            {
                "sample: Stmt.X",
                "sample: Stmt.Y",
                "sample: Lit|SglQuoted.Param.Value",
                "sample: Lit|SglQuoted.Param.Value = 'TMPDIR'",
            },
            misses("sample", named, reads),
        )
        hook = """
    listed=$(jq -r '.Stmts // [] | length' <<< "$tree") || return 1
    spans=$(jq -r '.. | objects | select(.Cmd.Type? == "CallExpr") | "\\(.Pos.Offset) \\(.End.Offset)"' <<< "$tree")
"""
        stmt = frozenset({"Stmt"})
        self.assertEqual(
            (
                {"CallExpr"},
                [
                    Read(None, "Stmts", True),
                    Read(stmt, "Cmd", True),
                    Read(stmt, "Pos.Offset", True),
                    Read(stmt, "End.Offset", True),
                ],
            ),
            jq_reads(hook),
        )

    def test_every_field_and_literal_a_walker_reads_is_in_the_table_for_its_kind(self) -> None:
        found: set[str] = set()
        for path in WALKERS:
            named, reads = walker_reads(path)
            self.assertTrue(reads, f"{path.name}: the extractor found no read")
            found |= misses(path.relative_to(ROOT).as_posix(), named, reads)
        # The two omissions the round-3 audit found by hand are among the reads, so the binding is not vacuous.
        _, lint = walker_reads(LINT)
        self.assertIn(Read(frozenset({"BinaryTest"}), "Op", True, "!="), lint)
        self.assertIn(Read(frozenset({"Lit", "SglQuoted", "ExtGlob"}), "Pos.Line", True), lint)
        self.assertEqual(
            sorted(EXCEPTIONS),
            sorted(found),
            f"outside TABLE: {sorted(found - set(EXCEPTIONS))}; exceptions no walker needs: "
            f"{sorted(set(EXCEPTIONS) - found)}",
        )


@unittest.skipUnless(shutil.which("shfmt") or on_ci_runner(), "needs shfmt off the CI runner (CI puts the pin on PATH)")
class ContractRunTest(unittest.TestCase):
    """The pinned parser on PATH against the fixtures, and the walkers that run the contract first."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="shfmt-json-contract-"))
        self.addCleanup(shutil.rmtree, self.temp)

    def test_the_pinned_shfmt_satisfies_the_contract(self) -> None:
        result = subprocess.run([sys.executable, "-I", str(MODULE)], capture_output=True, text=True, check=False)
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_verified_trees_are_the_fixtures_trees_by_repository_path(self) -> None:
        trees = contract.verified_trees()
        self.assertEqual({str(fixture.relative_to(ROOT)) for fixture in CAPTURES}, set(trees))
        for fixture, capture in CAPTURES.items():
            self.assertEqual(json.loads(capture.read_text()), trees[str(fixture.relative_to(ROOT))])
        self.assertEqual(sum((contract.count(tree) for tree in trees.values()), contract.Counter()), contract.verify())

    def test_the_captured_trees_are_the_pinned_parsers_output(self) -> None:
        for fixture, capture in CAPTURES.items():
            with self.subTest(fixture=fixture.name):
                run = subprocess.run(
                    ["shfmt", "-ln", "bash", "--to-json"], input=fixture.read_bytes(), capture_output=True, check=True
                )
                self.assertEqual(json.loads(run.stdout), json.loads(capture.read_text()), f"regenerate {capture.name}")

    def test_each_fixture_yields_one_finding_at_its_nested_substitution(self) -> None:
        for fixture, line in ((FIXTURE, NESTED_LINE), (BACKQUOTES, BACKQUOTES_LINE)):
            with self.subTest(fixture=fixture.name):
                result = subprocess.run(["bash", str(CHECK), str(fixture)], capture_output=True, text=True, check=False)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(f"{fixture}:{line}: {MESSAGE}\n", result.stdout)
                self.assertEqual("", result.stderr)

    def test_the_heredoc_caveats_keep_their_status(self) -> None:
        # An ANSI-C escaped delimiter is a heredoc shfmt cannot terminate: refused, as ShellCheck refuses it. A
        # partly quoted delimiter makes the body literal in bash, so its nested substitution is no finding.
        ansi = subprocess.run(
            ["bash", str(CHECK), str(FIXTURES / "heredoc-ansi-c-delimiter")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(2, ansi.returncode, ansi.stdout + ansi.stderr)
        self.assertIn("shfmt cannot parse", ansi.stderr)
        self.assertEqual("", ansi.stdout)
        partly = subprocess.run(
            ["bash", str(CHECK), str(FIXTURE), str(FIXTURES / "heredoc-partly-quoted-delimiter")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, partly.returncode, partly.stdout + partly.stderr)
        self.assertEqual(f"{FIXTURE}:{NESTED_LINE}: {MESSAGE}\n", partly.stdout, "the literal bodies add nothing")

    def path_with_fake_shfmt(self, fixture_trees: dict[str, str], other_tree: str) -> dict[str, str]:
        """An environment whose PATH holds the tools the walkers need and a shfmt that reports the pinned version,
        answers each fixture its tree from fixture_trees (by fixture name) and other_tree to any other input."""
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        for tool in ("bash", "sh", "awk", "python3", "jq", "sed", "xargs", "cat"):
            (bin_dir / tool).symlink_to(shutil.which(tool))
        answers = ""
        for fixture in CAPTURES:
            (self.temp / f"{fixture.name}.json").write_text(fixture_trees[fixture.name])
            answers += f'[ "$input" = "$(/bin/cat "{fixture}")" ] && exec /bin/cat "{self.temp}/{fixture.name}.json"\n'
        (self.temp / "other.json").write_text(other_tree)
        fake = bin_dir / "shfmt"
        fake.write_text(
            "#!/bin/sh\n"
            f'[ "$1" = --version ] && {{ echo v{pinned_version()}; exit 0; }}\n'
            f'input=$(/bin/cat)\n{answers}exec /bin/cat "{self.temp}/other.json"\n'
        )
        fake.chmod(0o755)
        return {"PATH": str(bin_dir), "HOME": str(self.temp)}

    def walkers(self, env: dict[str, str]) -> dict[str, subprocess.CompletedProcess[str]]:
        """One run of each walker over a small conforming input, under env."""
        script = self.temp / "lever.sh"
        script.write_text('#!/usr/bin/env bash\ndir=$(dirname "$0")\necho "$dir"\n')
        reader = self.temp / "reader.sh"
        reader.write_text('#!/usr/bin/env bash\nset -euo pipefail\ndir=$(pwd -P) || exit 1\necho "$dir"\n')
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "python script.py"}})
        return {
            "masked-dirname-check": subprocess.run(
                ["bash", str(CHECK), str(script)], capture_output=True, text=True, check=False, env=env
            ),
            "producer-status-check": subprocess.run(
                ["bash", str(PRODUCER_CHECK), str(reader)], capture_output=True, text=True, check=False, env=env
            ),
            "git-invocation-check": subprocess.run(
                ["bash", str(GIT_CHECK), str(script)], capture_output=True, text=True, check=False, env=env
            ),
            "enforce-uv": subprocess.run(
                ["bash", str(HOOK)], input=payload, capture_output=True, text=True, check=False, env=env
            ),
            "lint-comparisons": subprocess.run(
                [sys.executable, "-I", str(LINT), "--baseline", str(self.temp / "none.tsv"), "lever.sh", "--changed"],
                cwd=self.temp,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            ),
        }

    def test_each_walker_refuses_a_parser_whose_output_does_not_match(self) -> None:
        renamed = {name: text.replace('"Type"', '"type"') for name, text in captures().items()}
        results = self.walkers(self.path_with_fake_shfmt(renamed, renamed[FIXTURE.name]))
        for name, result in results.items():
            with self.subTest(walker=name):
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn("does not match the pinned node table", result.stderr)
                self.assertEqual("", result.stdout, "no finding and no decision stands in for the refusal")

    def test_each_walker_refuses_a_run_that_saw_no_node_the_fixture_holds(self) -> None:
        # The parser satisfies the contract, then hands every real file a tree whose statements the walk cannot
        # read: "no findings" would be "saw nothing", so the hook and the lint exit 2 naming what they did not see.
        # masked-dirname-check's self-check rests on the fixtures instead (the test below): a listed file with no
        # command substitution is a clean file, so this tree is clean to it.
        results = self.walkers(self.path_with_fake_shfmt(captures(), json.dumps(UNREADABLE_TREE)))
        expected = {
            "enforce-uv": "lists 1 statement(s) but the walk saw none",
            "lint-comparisons": "saw no statement in 1 shell file(s)",
            "producer-status-check": "saw none of the 1 top-level statement(s)",
        }
        for name, message in expected.items():
            with self.subTest(walker=name):
                result = results[name]
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual("", result.stdout)
        check = results["masked-dirname-check"]
        self.assertEqual((0, "", ""), (check.returncode, check.stdout, check.stderr))
        invocation = results["git-invocation-check"]  # the same self-check on the fixtures, so the same clean verdict
        self.assertEqual((0, "", ""), (invocation.returncode, invocation.stdout, invocation.stderr))

    def test_masked_dirname_check_refuses_fixtures_in_which_its_walk_sees_no_substitution(self) -> None:
        # The contract holds (every node is still in each tree), but the walk skips a quoted heredoc's body, so its
        # own visit of the fixtures counts no command substitution: refused before the listed file is read, whose
        # nested substitution therefore yields no finding line.
        hidden = {name: hidden_tree(text) for name, text in captures().items()}
        lever = self.temp / "lever.sh"
        lever.write_text('#!/usr/bin/env bash\ndir=$(cd "$(dirname "$0")" && pwd -P)\n')
        env = self.path_with_fake_shfmt(hidden, captures()[FIXTURE.name])

        result = subprocess.run(["bash", str(CHECK), str(lever)], capture_output=True, text=True, check=False, env=env)

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("the walk visited no command substitution in the contract fixtures", result.stderr)
        self.assertEqual("", result.stdout)

    def test_the_walkers_judge_a_conforming_tree_as_before(self) -> None:
        results = self.walkers({**os.environ})
        check = results["masked-dirname-check"]
        self.assertEqual((0, "", ""), (check.returncode, check.stdout, check.stderr))
        producer = results["producer-status-check"]
        self.assertEqual((0, "", ""), (producer.returncode, producer.stdout, producer.stderr))
        hook = results["enforce-uv"]
        self.assertEqual(0, hook.returncode, hook.stderr)
        self.assertIn('"permissionDecision":"deny"', hook.stdout)
        lint = results["lint-comparisons"]
        self.assertEqual((0, "", ""), (lint.returncode, lint.stdout, lint.stderr))
        invocation = results["git-invocation-check"]
        self.assertEqual((0, "", ""), (invocation.returncode, invocation.stdout, invocation.stderr))

    def test_the_sandbox_guard_refuses_what_the_other_walkers_refuse(self) -> None:
        # tests/unit/test_sandbox_portability.py walks the same JSON in process: a contract mismatch and a run whose
        # shell files held no statement node are errors there, never an empty hit list.
        sandbox.shfmt.cache_clear()
        self.addCleanup(sandbox.shfmt.cache_clear)
        with mock.patch.object(contract, "verify", side_effect=contract.ContractError("injected")):
            with self.assertRaisesRegex(RuntimeError, "does not match the pinned node table: injected"):
                sandbox.findings("a.sh", "#!/usr/bin/env bash\necho\n")
        sandbox.shfmt.cache_clear()
        tracked = [("scripts/a.sh", "#!/usr/bin/env bash\necho\n")]
        with mock.patch.object(sandbox, "tracked", return_value=tracked):
            with mock.patch.object(sandbox, "shell_tree", return_value=UNREADABLE_TREE):
                with self.assertRaisesRegex(RuntimeError, "saw no statement in 1 shell file"):
                    sandbox.guard(ROOT)
            self.assertEqual([], sandbox.guard(ROOT))


class ContractReadTest(unittest.TestCase):
    """Every status read of the module with its failure injected: a fake shfmt on PATH (its `--version` satisfies the
    pin check), or an unrunnable path in process. No real shfmt is needed. Each refusal is exit 2, nothing on stdout
    and the cause on stderr: the fixture, the status, the tool's own diagnostic or the text it printed."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="shfmt-json-contract-reads-"))
        self.addCleanup(shutil.rmtree, self.temp)

    def refusal(self, answer: str, version: str | None = None) -> str:
        """The stderr of the module run over the fixtures with a shfmt that answers so, once it has exited 2 with
        nothing on stdout."""
        result = module_run(fake_shfmt_env(self.temp, answer, version))
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout, "no clean verdict stands in for the refusal")
        return result.stderr

    def test_every_status_read_of_the_module_has_an_injection_test(self) -> None:
        sample = (
            "def f(p):\n"
            "    try:\n"
            "        r, t = run(), json.loads(p.read_text())\n"
            "    except (OSError, ValueError):\n"
            "        pass\n"
            "    return r.returncode, r.stdout\n"
            "def g(r):\n"
            "    return r.stderr\n"
        )
        self.assertEqual({("f", "OSError"), ("f", "json"), ("f", "status"), ("f", "output")}, status_reads(sample))
        reads = status_reads(MODULE.read_text())
        self.assertEqual(
            set(STATUS_READS),
            reads,
            f"reads without a row: {sorted(reads - set(STATUS_READS))}; rows no read needs: "
            f"{sorted(set(STATUS_READS) - reads)}",
        )
        for test in sorted(set(STATUS_READS.values())):
            cls, _, method = test.partition(".")
            self.assertTrue(callable(getattr(globals()[cls], method, None)), f"{test} does not exist")

    def test_a_fake_shfmt_that_answers_the_captures_passes_the_contract(self) -> None:
        """The control: the module reads the shfmt on this PATH and nothing else, so each refusal below comes from
        the injected answer, not from the PATH idiom."""
        answer = "input=$(/bin/cat)\n"
        for fixture, capture in CAPTURES.items():
            answer += f'[ "$input" = "$(/bin/cat "{fixture}")" ] && exec /bin/cat "{capture}"\n'
        result = module_run(fake_shfmt_env(self.temp, answer + "exit 1\n"))
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_a_fixture_parse_that_exits_nonzero_is_refused_naming_the_status(self) -> None:
        """The status is what counts, not the presence of a tree: a full tree printed and then exit 3 is a failed read
        with shfmt's own diagnostic kept, and a bare exit 1 names the absence of one."""
        source = FIXTURE.relative_to(ROOT)
        cases = {
            f'/bin/cat "{CAPTURES[FIXTURE]}"\necho "shfmt: injected failure" >&2\nexit 3': (
                "(exited 3): shfmt: injected failure"
            ),
            "exit 1": "(exited 1): no diagnostic",
        }
        for answer, cause in cases.items():
            with self.subTest(cause=cause):
                self.assertEqual(f"shfmt-json-contract: shfmt cannot parse {source} {cause}\n", self.refusal(answer))

    def test_a_fixture_parse_that_prints_no_tree_or_no_json_object_is_refused(self) -> None:
        """Exit 0 with nothing (or only whitespace) printed, text that is no JSON, and JSON that is no object each name
        the fixture and what was printed; none is read as an empty tree or as the fixture's tree."""
        source = FIXTURE.relative_to(ROOT)
        cases = {
            "exit 0": f"shfmt printed no tree for {source} (exited 0)",
            "echo; echo '  '": f"shfmt printed no tree for {source} (exited 0)",
            "echo not json": f"shfmt gave no JSON for {source}: Expecting value: line 1 column 1 (char 0)",
            "echo null": f"shfmt gave no JSON object for {source}: null",
            "echo '[]'": f"shfmt gave no JSON object for {source}: []",
            "echo '\"File\"'": f'shfmt gave no JSON object for {source}: "File"',
        }
        for answer, cause in cases.items():
            with self.subTest(answer=answer):
                self.assertEqual(f"shfmt-json-contract: {cause}\n", self.refusal(answer))

    def test_a_shfmt_that_is_not_the_pin_is_refused_before_any_fixture_is_parsed(self) -> None:
        """The pin check's status: another version, and a `--version` that fails, each refuse with the check's own
        line, and no fixture reaches the parser (the parse answer would leave a mark)."""
        mark = self.temp / "parsed"
        answer = f'touch "{mark}"\nexit 0'
        pin, config = pinned_version(), contract.PIN_CONFIG
        cases = {
            "echo v3.13.0; exit 0": (
                f"pinned-tool-version: the shfmt on PATH is version 3.13.0, but {config} pins shfmt {pin};"
            ),
            "exit 9": f'pinned-tool-version: "shfmt --version" failed; {config} pins shfmt {pin}',
        }
        for version, cause in cases.items():
            with self.subTest(version=version):
                stderr = self.refusal(answer, version)
                self.assertTrue(stderr.startswith(f"shfmt-json-contract: {cause}"), stderr)
                self.assertFalse(mark.exists(), "the pin check refused before a fixture was parsed")

    def test_a_pin_check_that_cannot_run_or_exits_without_a_diagnostic_is_refused(self) -> None:
        """In process: a check that exits nonzero with nothing on stderr is named by its status (and main maps it to
        exit 2 as any difference), and a check that cannot be run is named too; neither is "the pin holds"."""
        silent = self.temp / "pin-check.sh"
        silent.write_text("exit 7\n")
        with mock.patch.object(contract, "PIN_CHECK", silent):
            with self.assertRaisesRegex(contract.ContractError, r"^pin-check\.sh exited 7$"):
                contract.pinned_shfmt()
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(2, contract.main([]))
            self.assertEqual("shfmt-json-contract: pin-check.sh exited 7\n", stderr.getvalue())
        with mock.patch.object(contract.subprocess, "run", side_effect=OSError("injected")):
            with self.assertRaisesRegex(contract.ContractError, r"^cannot run pinned-tool-version\.sh: injected$"):
                contract.pinned_shfmt()

    def test_a_shfmt_that_cannot_be_run_or_a_fixture_that_cannot_be_read_is_refused(self) -> None:
        """In process, the pin check satisfied: a shfmt that is not there to run, and a fixture that cannot be read,
        are each named with the system's error; neither is an empty tree."""
        with mock.patch.object(contract, "pinned_shfmt"):
            with mock.patch.object(contract, "SHFMT", (str(self.temp / "no-shfmt"), *contract.SHFMT[1:])):
                with self.assertRaisesRegex(contract.ContractError, r"^cannot run shfmt: \[Errno 2\] .*no-shfmt"):
                    contract.verified_trees()
            absent = ROOT / "tests/fixtures/shfmt-json/absent"
            with mock.patch.object(contract, "FIXTURES", (absent,)):
                cause = r"^cannot read tests/fixtures/shfmt-json/absent: \[Errno 2\] .*absent"
                with self.assertRaisesRegex(contract.ContractError, cause):
                    contract.verified_trees()

    def test_a_tree_file_that_cannot_be_read_is_refused_naming_it(self) -> None:
        absent = self.temp / "absent.json"
        result = module_run({**os.environ}, "--tree", str(absent))
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertRegex(
            result.stderr,
            rf"^shfmt-json-contract: cannot read a JSON tree from {re.escape(str(absent))}: \[Errno 2\] .*\n$",
        )


if __name__ == "__main__":
    unittest.main()
