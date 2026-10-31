"""regime.yml keeps the properties that make pull_request_target safe for it (regime-cutover U103, plan P-01 part 1).

GitHub's default Actions event policy blocks pull_request_target in public repositories from 2026-12-02, and the
operator allows it for this repository by an explicit policy (gate G-23). That allowance rests on the workflow running
only the base's code with a read-only token and reading the pull request as data. Each property is one check here,
and each check is shown to go red on a copy of the workflow with that property taken away.

The YAML is read as data. Each `run` script is read from the syntax tree of the pinned shfmt and must equal, statement
by statement, word by word, part by part, the shape SCRIPTS holds for it; nothing else is admitted, and no text scan
stands in for the parser (decision of 2026-10-28T12:12Z, after two rounds of regexes over the run text were each
passed by a text-level edit: a quoted gap in `git`, a commented-out fetch, an option the reader discarded).

Each step's `env:` and `with:` must equal, key for key and value for value, the mapping INPUTS holds for it, and the
workflow and the job carry no `env:` at all: bash reads BASH_ENV before a script's first word, so a variable the table
does not hold runs code the tree never sees (the round-4 audit ran the fetched head from a job-level BASH_ENV).

The whole document must equal DOCUMENT, key for key and value for value down to each scalar's type, with the run
scripts left to the tree reader: a key no table names (`container`, `services`, a second job, a step's `if`) is
refused by its path (the round-5 audit ran a container image taken from the pull request's title), and `false` is
never `0` (PyYAML reads them as different inputs and Actions passes them as different strings; `==` has them equal).

The YAML is read by a loader whose booleans are YAML 1.2's (`true` and `false` in their three spellings, nothing
else), so the key `on` is the string `on`: PyYAML's own YAML 1.1 resolver reads `on`, `yes` and `true` as one boolean
key, and a workflow whose trigger key was `true:` or `yes:` read as this one while GitHub found no trigger (the
round-6 audit renamed `on:` to `true:` past every check).

The file itself must equal WORKFLOW_BYTES, byte for byte, with the sha256 WORKFLOW_SHA256 (round 8). Seven audits each
found a new way the parsed form stood for a file GitHub reads otherwise: regexes over the run text, unpinned channels
(`defaults`, `env`, `with`, `container`), a bool conflated with an int, YAML 1.1 booleans, and duplicate keys, which
SafeLoader overwrites in silence (the round-7 audit's edit). The premise they shared, that the test can read the YAML as
GitHub does, is dropped: nothing a parser reads differently survives a byte comparison. The byte pin is the control for
the parser layer, and the property checks are the explanation layer: they run on the parsed form of the same bytes and
say which property a change took away, so an editor knows what to restore before updating the pin.
"""

from __future__ import annotations

import copy
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from collections.abc import Callable
from itertools import zip_longest
from pathlib import Path
from typing import NamedTuple, NoReturn
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/regime.yml"
# PATH's shfmt is the reader, and it must be the version home/dot_mise/config.toml pins ([tools."http:shfmt"], U97):
# the guard the lint gates run first. Another version, or none, fails every run-script check instead of skipping it.
PIN_GUARD = ROOT / "scripts/ci/pinned-tool-version.sh"
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
# The file's exact bytes and their sha256, written once from the file at this head and never read from the file: the
# control for the parser layer. A duplicate key, a boolean spelling, an indentation, a line ending or a byte order mark
# reads one way in PyYAML and another in GitHub, and none survives a byte comparison. A change to regime.yml updates
# both constants in the same commit, once the property checks pass on the new text; a reviewer verifies the pin with
# `shasum -a 256 .github/workflows/regime.yml` without reading the literal.
WORKFLOW_SHA256 = "2b62a44213e0f82de2f8319d77d5cbaaece61de14aece523b11b2aaaac3a1b06"
WORKFLOW_BYTES = """\
name: regime

# The regime job: the base's scripts/orchestrator/regime-ci.py reads the pull request's diff and body, and runs only
# git. A pull request passes when it changes records alone (every path under .orchestration/), or when its body carries
# its own line `Program-Unit: <program>/U<n>` for a program whose store the base holds and its author is the owner, a
# member or a collaborator (operator decision D-024-131; U71). pull_request_target runs this workflow as it is on the
# base; the pull request's head is fetched as data and is never checked out or executed. The verdict depends on the
# body, so an edit re-runs it (`edited`); only pull requests into main run it, so no other base branch's verifier
# decides (U71). It is an optional check until the operator adds `regime` to the ruleset's required contexts (gate G10).
on:
  pull_request_target:
    types: [opened, edited, synchronize, reopened, ready_for_review]
    branches: [main]

concurrency:
  group: regime-pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  regime:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          fetch-depth: 0
          # The base branch's tip at run time: the event's recorded base sha can lag the branch (on PR #420 it was the
          # head's fork point, from before this verifier; ci:39185982423:1). The pull request cannot move this branch.
          ref: refs/heads/${{ github.base_ref }}
          persist-credentials: false
      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: false
      - name: Fetch the pull request's head as data
        env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: |
          git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"
          test "$(git rev-parse refs/regime/pr-head)" = "${HEAD_SHA}"
      - name: Check the pull request with the base's verifier
        env:
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          # the program marker (D-024-131) is read from the event payload as data, never interpolated into run:
          PR_BODY: ${{ github.event.pull_request.body }}
          # who wrote the pull request (U71, F152): only an owner, member or collaborator's Program-Unit line counts
          PR_AUTHOR_ASSOCIATION: ${{ github.event.pull_request.author_association }}
        # the base sha is read into a variable with its producer's status checked (standing order 21): a git that
        # prints a sha and exits non-zero ends the step before the verifier runs
        run: |
          set -euo pipefail
          base=$(git rev-parse HEAD) || exit 1
          uv run --no-config --no-project python -I scripts/orchestrator/regime-ci.py --base "${base}" --head "${HEAD_SHA}"
      - name: Check the round cap over the records the pull request's head carries
        # standing order 36 (U120): the base's rounds-check.py reads the head's ledger.tsv and decisions.tsv as data
        # (git cat-file blob) and checks every unit; a head whose two files are its merge base's blobs is nothing to check
        timeout-minutes: 2
        env:
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
        run: |
          set -euo pipefail
          base=$(git rev-parse HEAD) || exit 1
          uv run --no-config --no-project python -I scripts/orchestrator/rounds-check.py --all .orchestration/orchestrate/regime-cutover --base "${base}" --head "${HEAD_SHA}"
"""
BASE_BRANCH = "refs/heads/${{ github.base_ref }}"
BODY_VARIABLE = "PR_BODY"
# The body on its own: not a literal that names it, not an expression computed from it. The script reads this value.
BODY_CARRIER = "${{ github.event.pull_request.body }}"
HEAD_EXPRESSION = "${{ github.event.pull_request.head.sha }}"
NUMBER_EXPRESSION = "${{ github.event.pull_request.number }}"
AUTHOR_EXPRESSION = "${{ github.event.pull_request.author_association }}"
# GitHub expands an expression before the shell reads the script, so a run holding one is another text than the tree
# reads; it is refused before parsing. The body and every other field reach the script through env: alone.
EXPRESSION = "${{"
HEAD_REF = "refs/regime/pr-head"
HEAD_REFSPEC = "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"
VERIFIER = "scripts/orchestrator/regime-ci.py"
ROUNDS_CHECK = "scripts/orchestrator/rounds-check.py"  # U120: the round cap over the head's store, read as data
CHECKED_BASE = "base=$(git rev-parse HEAD) || exit 1"  # round 3: the base sha with its producer's status read
STORE = ".orchestration/orchestrate/regime-cutover"
UNSAFE_OPTION = "allow-unsafe-pr-checkout"
READ_ONLY = {"contents": "read"}
POSITION = {"Offset", "Line", "Col"}
TITLE_EXPRESSION = "${{ github.event.pull_request.title }}"
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_UV_ACTION = "astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7"
EVENT_TYPES = ["opened", "edited", "synchronize", "reopened", "ready_for_review"]
MISSING = object()
# The reader's booleans are YAML 1.2's: these six spellings and nothing else. PyYAML's own YAML 1.1 resolver also reads
# yes, no, on and off as booleans (DROPPED_FORMS), so `on:`, `true:` and `yes:` were one key here and the round-6
# audit renamed `on:` to `true:` past every check while GitHub found no trigger. Each form is now its own string.
BOOLEANS = "true|True|TRUE|false|False|FALSE"
DROPPED_FORMS = ["yes", "Yes", "YES", "no", "No", "NO", "on", "On", "ON", "off", "Off", "OFF"]
# Run by the uv interpreter that has PyYAML (the test interpreter has none): the document as JSON on stdout.
READER = f"""
import json, re, sys, yaml


class Loader(yaml.SafeLoader):
    pass


BOOL = "tag:yaml.org,2002:bool"
Loader.yaml_implicit_resolvers = {{
    first: [(tag, regexp) for tag, regexp in found if tag != BOOL]
    for first, found in yaml.SafeLoader.yaml_implicit_resolvers.items()
}}
Loader.add_implicit_resolver(BOOL, re.compile(r"^(?:{BOOLEANS})$"), list("tTfF"))
with open(sys.argv[1]) as handle:
    print(json.dumps(yaml.load(handle, Loader=Loader), default=str))
"""

# A shape is a run script with every position dropped and four kinds of part admitted, each pinned in full:
#   ("lit", text)              a literal fragment of a word
#   ("var", name)              a plain parameter expansion, ${name} or $name: no operator, index, slice or length
#   ("dq", (part, ...))        a double-quoted group of parts
#   ("sub", (statement, ...))  a $(...) substitution whose statements are shapes themselves
# A word is a tuple of parts, a statement a tuple of words (a plain call: no assignment, redirect, negation, background
# or operator), a script a tuple of statements. Every other node, field or kind of shfmt's tree is refused by name.
Part = tuple
Word = tuple[Part, ...]
Statement = tuple[Word, ...]
Script = tuple[Statement, ...]
# A checked statement, `name=$(statement) || exit 1`, is the one compound statement admitted (Checked below): an
# assignment whose producer's status is read, so a failure ends the step before the name is used (standing order 21).


def lit(text: str) -> Part:
    return ("lit", text)


def var(name: str) -> Part:
    return ("var", name)


def dq(*parts: Part) -> Part:
    return ("dq", parts)


def sub(*statements: Statement) -> Part:
    return ("sub", statements)


def call(*words: str | Part) -> Statement:
    """A statement from its words: a string is a literal word, a part is a word of that one part."""
    return tuple((lit(word),) if isinstance(word, str) else (word,) for word in words)


def rev_parse(ref: str) -> Statement:
    return call("git", "rev-parse", ref)


class Checked(NamedTuple):
    """`name=$(statement) || exit 1`: one plain assignment of one substitution of one statement, with the producer's
    status read and a failure ending the step with status 1 (standing order 21, round 3). The producer is a shape."""

    name: str
    producer: Statement


EXIT_1 = call("exit", "1")


class Row(NamedTuple):
    """One run step's script: the regime.yml text a message points at, and the shape the step must have."""

    protects: str
    script: Script


# The table: the run steps of the workflow, in order, each pinned to the last part. The first fetches the pull
# request's own `/head` ref (not `/merge`, which GitHub builds from the head and the base) into the data ref, from
# origin, with no option but --no-tags, and checks the ref against the event's head sha. The second and the third read
# the base's HEAD into `base` with the producer's status checked (standing order 21; round 3) and run the base's
# verifier, then its round-cap check, on that sha and the event's head sha. No statement moves HEAD or the work tree,
# and nothing else runs.
SCRIPTS = (
    Row(
        HEAD_REFSPEC,
        (
            call(
                "git", "fetch", "--no-tags", "origin", dq(lit("refs/pull/"), var("PR_NUMBER"), lit(f"/head:{HEAD_REF}"))
            ),
            call("test", dq(sub(rev_parse(HEAD_REF))), "=", dq(var("HEAD_SHA"))),
        ),
    ),
    Row(
        f"python -I {VERIFIER}",
        (
            call("set", "-euo", "pipefail"),
            Checked("base", rev_parse("HEAD")),
            call(
                *("uv", "run", "--no-config", "--no-project", "python", "-I", VERIFIER),
                *("--base", dq(var("base")), "--head", dq(var("HEAD_SHA"))),
            ),
        ),
    ),
    Row(
        f"python -I {ROUNDS_CHECK}",
        (
            call("set", "-euo", "pipefail"),
            Checked("base", rev_parse("HEAD")),
            call(
                *("uv", "run", "--no-config", "--no-project", "python", "-I", ROUNDS_CHECK, "--all", STORE),
                *("--base", dq(var("base")), "--head", dq(var("HEAD_SHA"))),
            ),
        ),
    ),
)


class Inputs(NamedTuple):
    """One step's input channels: the regime.yml text a message points at, and the exact env: and with: mappings the
    step carries, key for key and value for value; None where the step has no such key."""

    protects: str
    env: dict[str, str] | None
    options: dict[str, object] | None


# The steps of the workflow, in order, each pinned to the last key of its two input channels. bash reads BASH_ENV,
# ENV and PATH from the environment before a script's first word, git reads GIT_DIR and GIT_CONFIG_*, python reads
# PYTHONSTARTUP and PYTHONPATH, uv reads UV_*: a variable the table does not hold runs or redirects code the tree
# never sees. The workflow and the job carry no env: (every step would inherit it), the action steps carry no env:,
# the run steps carry no with:, and the body reaches the verifier through the one PR_BODY the table holds.
INPUTS = (
    Inputs("persist-credentials: false", None, {"fetch-depth": 0, "ref": BASE_BRANCH, "persist-credentials": False}),
    Inputs("enable-cache: false", None, {"enable-cache": False}),
    Inputs(f"PR_NUMBER: {NUMBER_EXPRESSION}", {"PR_NUMBER": NUMBER_EXPRESSION, "HEAD_SHA": HEAD_EXPRESSION}, None),
    Inputs(
        f"{BODY_VARIABLE}: {BODY_CARRIER}",
        {"HEAD_SHA": HEAD_EXPRESSION, BODY_VARIABLE: BODY_CARRIER, "PR_AUTHOR_ASSOCIATION": AUTHOR_EXPRESSION},
        None,
    ),
    Inputs("timeout-minutes: 2", {"HEAD_SHA": HEAD_EXPRESSION}, None),
)


class RunScript:
    """Marks a step's run in DOCUMENT: the text is read from the shfmt tree by check_run_scripts, not compared here."""

    def __repr__(self) -> str:
        return "a run script (read by the run-script check)"


SCRIPT = RunScript()

# The table of the whole document, as the reader hands it over: every key at every level, with the env: and with:
# mappings taken from INPUTS and the run texts left to SCRIPTS. A key no table holds (`container`, `services`, a
# second job, a `strategy`, a step's `if` or `working-directory`) runs code or moves the step in a way no other check
# sees: the round-5 audit ran a container image taken from the pull request's title past every check. The trigger
# key is the string `on`, as the file spells it; `true` or `yes` in its place is another key.
DOCUMENT = {
    "name": "regime",
    "on": {"pull_request_target": {"types": EVENT_TYPES, "branches": ["main"]}},
    "concurrency": {"group": f"regime-pr-{NUMBER_EXPRESSION}", "cancel-in-progress": True},
    "permissions": READ_ONLY,
    "jobs": {
        "regime": {
            "runs-on": "ubuntu-24.04",
            "timeout-minutes": 10,
            "steps": [
                {"uses": CHECKOUT_ACTION, "with": INPUTS[0].options},
                {"uses": SETUP_UV_ACTION, "with": INPUTS[1].options},
                {"name": "Fetch the pull request's head as data", "env": INPUTS[2].env, "run": SCRIPT},
                {"name": "Check the pull request with the base's verifier", "env": INPUTS[3].env, "run": SCRIPT},
                {
                    "name": "Check the round cap over the records the pull request's head carries",
                    "timeout-minutes": 2,
                    "env": INPUTS[4].env,
                    "run": SCRIPT,
                },
            ],
        }
    },
}


def load(path: Path) -> dict:
    """The workflow parsed by PyYAML under uv (as test_regime_ci.py reads it, but with READER's YAML 1.2 booleans)."""
    uv = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
    result = subprocess.run([*uv, "-c", READER, str(path)], capture_output=True, text=True, check=True)
    doc = json.loads(result.stdout)
    if not isinstance(doc, dict):
        raise AssertionError(f"{path} is not a mapping: {doc!r}")
    return doc


def line(text: str) -> str:
    """`regime.yml:<n>` of the line that holds `text`, or a note that it is gone: the message names what to restore."""
    for number, content in enumerate(WORKFLOW.read_text().splitlines(), 1):
        if text in content:
            return f"regime.yml:{number} ({text})"
    return f"regime.yml (no line holds {text!r} any more)"


def require(condition: object, protects: str, detail: str) -> None:
    if not condition:
        raise AssertionError(f"{line(protects)}: {detail}")


def mapping(value: object, protects: str) -> dict:
    require(isinstance(value, dict), protects, f"expected a mapping, found {value!r}")
    return value  # type: ignore[return-value]


def jobs(doc: dict) -> dict[str, dict]:
    return {name: mapping(job, f"{name}:") for name, job in mapping(doc.get("jobs"), "jobs:").items()}


def steps(doc: dict) -> list[dict]:
    found = [step for job in jobs(doc).values() for step in job.get("steps") or []]
    require(found, "steps:", "the workflow has no steps")
    return [mapping(step, "steps:") for step in found]


class Owner(NamedTuple):
    """A scope whose keys every step inherits: the name a message gives it, its mapping, and the line to point at."""

    label: str
    scope: dict
    protects: str


def owners(doc: dict) -> list[Owner]:
    return [
        Owner("the workflow", doc, "jobs:"),
        *(Owner(f"the job {name}", job, f"{name}:") for name, job in jobs(doc).items()),
    ]


def step_name(step: dict) -> str:
    return str(step.get("name", step.get("uses", step.get("run"))))


def shfmt_tree(script: str, protects: str) -> dict:
    """The script's typed JSON tree from PATH's shfmt, after the pin guard accepted that shfmt (U97, one reader)."""
    guard = [str(PIN_GUARD), str(MISE_CONFIG), "shfmt"]
    accepted = subprocess.run(guard, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    require(accepted.returncode == 0, protects, f"no pinned shfmt reads the run scripts: {accepted.stderr.strip()}")
    parse = ["shfmt", "-ln", "bash", "--to-json"]
    parsed = subprocess.run(parse, input=script, capture_output=True, text=True, check=False)
    status = f"shfmt exited {parsed.returncode} on the run script: {parsed.stderr.strip() or 'no message on stderr'}"
    require(parsed.returncode == 0, protects, status)
    try:
        tree = json.loads(parsed.stdout)
    except ValueError:
        tree = None
    require(isinstance(tree, dict) and tree.get("Type") == "File", protects, "shfmt gave no JSON syntax tree")
    return tree


def position(node: dict) -> object:
    """The line of the node's first position, for a message; shfmt names the field differently per node kind."""
    for value in node.values():
        if isinstance(value, dict) and set(value) == POSITION:
            return value["Line"]
    return "?"


class Reader:
    """Reduces one run script's tree to its shape, refusing by name every node, field or kind outside the grammar."""

    def __init__(self, step: str, protects: str) -> None:
        self.step = step
        self.protects = protects

    def refuse(self, node: dict, what: str) -> NoReturn:
        detail = f"line {position(node)} of the step {self.step!r}: {what}, a form the table has no shape for"
        raise AssertionError(f"{line(self.protects)}: {detail}")

    def comments(self, node: dict, key: str) -> None:
        # shfmt 3.14.1 joins the line after a comment ending in a backslash to the command before it; bash runs that
        # line on its own. A comment is refused whatever its text, so the tree reads what the shell runs.
        if node.get(key):
            self.refuse(node[key][0], "a comment")

    def fields(self, node: dict, kind: str, *known: str) -> None:
        """Every field of the node beyond the known ones must be empty, false or a position; a set one is refused.
        Semicolon, the one position that is syntax, is read by statement() before this skip."""
        for key, value in node.items():
            if key == "Type" or key in known or value in (None, False, 0, "", []):
                continue
            if isinstance(value, dict) and set(value) == POSITION:
                continue
            self.refuse(node, f"a {kind} with {key}")

    def script(self, tree: dict) -> Script:
        self.comments(tree, "Last")
        self.fields(tree, "script", "Name", "Stmts", "Last")
        return tuple(self.statement(node) for node in tree.get("Stmts") or [])

    def statement(self, node: dict) -> Statement | Checked:
        self.comments(node, "Comments")
        self.fields(node, "statement", "Cmd", "Comments")  # Negated, Background, Coprocess and Redirs are refused
        # shfmt sets Semicolon for `;` (and for `&`, refused above as Background) and leaves it out at a newline. A `;`
        # between two pinned statements is another text than the table's: refused, not skipped as a position.
        if node.get("Semicolon"):
            self.refuse(node, "a semicolon")
        command = node.get("Cmd")
        kind = command.get("Type", "untyped") if isinstance(command, dict) else "empty"
        if kind == "BinaryCmd":
            return self.checked(command)
        if kind != "CallExpr":
            self.refuse(node, f"a {kind} statement")
        self.fields(command, "call", "Args")  # an assignment before the command word is refused
        words = command.get("Args") or []
        if not words:
            self.refuse(command, "a call with no word")
        return tuple(self.word(word) for word in words)

    def checked(self, node: dict) -> Checked:
        """`name=$(statement) || exit 1`, the one binary command admitted: `||` with one plain assignment of one
        substitution of one statement on its left and `exit 1` on its right. Every other operator (`&&`, `|`), a
        second assignment, a command word after the assignment, `+=`, an array, an index, a `local` or `declare`
        clause and a right side other than `exit 1` are refused by name, so the producer's status is read and a
        failure ends the step (standing order 21)."""
        self.fields(node, "BinaryCmd", "Op", "X", "Y")
        if node.get("Op") != "||":
            self.refuse(node, f"a BinaryCmd joined by {node.get('Op')}")
        left, right = node.get("X") or {}, node.get("Y") or {}
        if self.statement(right) != EXIT_1:
            self.refuse(right, "a `||` whose right side is not `exit 1`")
        self.comments(left, "Comments")
        self.fields(left, "statement", "Cmd", "Comments")
        assignment = left.get("Cmd")
        kind = assignment.get("Type", "untyped") if isinstance(assignment, dict) else "empty"
        if kind != "CallExpr":
            self.refuse(left, f"a {kind} on the left of `||`")
        self.fields(assignment, "assignment", "Assigns")  # a command word after the assignment (Args) is refused
        assigns = assignment.get("Assigns") or []
        if len(assigns) != 1:
            self.refuse(assignment, f"{len(assigns)} assignments on the left of `||`")
        self.fields(assigns[0], "assignment", "Name", "Value")  # Append (+=), Naked, Index and Array are refused
        name = (assigns[0].get("Name") or {}).get("Value")
        if not isinstance(name, str) or not name:
            self.refuse(assigns[0], "an assignment with no name")
        value = assigns[0].get("Value")
        word = self.word(value) if isinstance(value, dict) else ()
        if len(word) != 1 or word[0][0] != "sub" or len(word[0][1]) != 1:
            self.refuse(assigns[0], "an assignment whose value is not one substitution of one statement")
        return Checked(name, word[0][1][0])

    def word(self, node: dict) -> Word:
        self.fields(node, "word", "Parts")
        parts = node.get("Parts") or []
        if not parts:
            self.refuse(node, "an empty word")
        return tuple(self.part(part) for part in parts)

    def part(self, node: dict) -> Part:
        kind = node.get("Type")
        if kind == "Lit":
            self.fields(node, kind, "Value")
            text = node.get("Value")
            if not isinstance(text, str) or not text:
                self.refuse(node, "an empty literal")
            return lit(text)
        if kind == "ParamExp":
            # Short is `$name` for `${name}`, the same expansion; every operator, index, slice or length is refused.
            self.fields(node, kind, "Param", "Short")
            param = node.get("Param")
            name = param.get("Value") if isinstance(param, dict) else None
            if not isinstance(name, str) or not name:
                self.refuse(node, "a parameter expansion with no name")
            return var(name)
        if kind == "DblQuoted":
            self.fields(node, kind, "Parts")  # the locale form $"..." is refused
            parts = node.get("Parts") or []
            if not parts:
                self.refuse(node, "an empty double-quoted string")
            return dq(*(self.part(part) for part in parts))
        if kind == "CmdSubst":
            self.comments(node, "Last")
            self.fields(node, kind, "Stmts", "Last")  # backquotes and the mksh forms are refused
            statements = node.get("Stmts") or []
            if not statements:
                self.refuse(node, "an empty substitution")
            return sub(*(self.statement(statement) for statement in statements))
        self.refuse(node, f"a {kind or 'untyped'} part")


def render(statement: Statement | Checked) -> str:
    """A shape written back as shell text, for a message: the form the table holds, not the text the file had."""
    if isinstance(statement, Checked):
        return f"{statement.name}=$({render(statement.producer)}) || exit 1"
    return " ".join("".join(render_part(part) for part in word) for word in statement)


def render_part(part: Part) -> str:
    kind, value = part
    if kind == "lit":
        return value
    if kind == "var":
        return "${" + value + "}"
    if kind == "dq":
        return '"' + "".join(render_part(inner) for inner in value) + '"'
    return "$(" + "; ".join(render(statement) for statement in value) + ")"


def shown(raw: bytes) -> str:
    """A line of the file for a message, with its ending and every invisible byte spelled out (`\\r\\n`, `\\ufeff`, a
    trailing space), or a note that there is no such line."""
    return repr(raw.decode("utf-8", errors="backslashreplace")) if raw else "no such line"


def check_bytes(path: Path) -> None:
    """The file is WORKFLOW_BYTES, byte for byte, and their sha256 is WORKFLOW_SHA256: the control for the parser
    layer. A duplicate key, a boolean spelling, an indentation, a line ending or a byte order mark reads one way in
    PyYAML and another in GitHub (the round-7 audit's duplicate `run:` was the table's document to SafeLoader), and
    none survives a byte comparison. The message shows the file against the pin as a unified diff, names the first
    differing line, both digests, and the way to change the workflow: update the pin in the same commit."""
    found = path.read_bytes()
    pin = WORKFLOW_BYTES.encode()
    digest = hashlib.sha256(found).hexdigest()
    if found == pin and digest == WORKFLOW_SHA256:
        return
    if found == pin:
        detail = f"the file is the pinned bytes, but their sha256 is {digest} and WORKFLOW_SHA256 is {WORKFLOW_SHA256}"
        raise AssertionError(f"regime.yml:1 (name: regime): {detail}; the two constants are updated together")
    found_lines, pin_lines = found.splitlines(keepends=True), pin.splitlines(keepends=True)
    pairs = enumerate(zip_longest(found_lines, pin_lines, fillvalue=b""), 1)
    number, (got, held) = next((number, pair) for number, pair in pairs if pair[0] != pair[1])
    diff = difflib.unified_diff(
        [visible(raw) for raw in pin_lines],
        [visible(raw) for raw in found_lines],
        fromfile="WORKFLOW_BYTES (the pin)",
        tofile="regime.yml (the file)",
        lineterm="",
    )
    detail = (
        f"regime.yml:{number}: the file is not the pinned bytes: its sha256 is {digest}, the pin's is {WORKFLOW_SHA256};"
        f" the first difference is line {number}: found {shown(got)}, the pin holds {shown(held)}. A change to"
        " regime.yml updates WORKFLOW_BYTES and WORKFLOW_SHA256 in tests/unit/test_regime_workflow.py in the same"
        " commit, once the property checks pass on the new text (shasum -a 256 .github/workflows/regime.yml gives"
        " the digest).\n"
    )
    raise AssertionError(detail + "\n".join(diff))


def visible(raw: bytes) -> str:
    """A line for the diff: decoded, its newline dropped, every other invisible byte spelled out (`\\r`, `\\ufeff`)."""
    return raw.decode("utf-8", errors="backslashreplace").removesuffix("\n").encode("unicode_escape").decode()


def check_trigger(doc: dict) -> None:
    # `on` is the string `on` here (the reader's booleans are YAML 1.2's): a trigger key spelled true: or yes:, which
    # PyYAML's own resolver would fold into `on`, is a missing key, as it is for GitHub.
    require("on" in doc, "on:", f"the workflow has no on: key; the keys are {list(doc)!r}")
    on = mapping(doc["on"], "pull_request_target:")
    require(list(on) == ["pull_request_target"], "pull_request_target:", f"the triggers are {list(on)!r}")
    event = mapping(on["pull_request_target"], "pull_request_target:")
    require(
        event.get("branches") == ["main"], "branches: [main]", f"branches is {event.get('branches')!r}, not ['main']"
    )


def check_permissions(doc: dict) -> None:
    require(doc.get("permissions") == READ_ONLY, "contents: read", f"the token is {doc.get('permissions')!r}")
    for name, job in jobs(doc).items():
        granted = job.get("permissions", {})
        widened = not isinstance(granted, dict) or not set(granted.items()) <= set(READ_ONLY.items())
        require(not widened, "contents: read", f"job {name} grants {granted!r}")


def check_checkout(doc: dict) -> None:
    checkouts = [step for step in steps(doc) if str(step.get("uses", "")).startswith("actions/checkout@")]
    require(checkouts, "uses: actions/checkout@", "no step checks anything out, so nothing pins the base")
    for step in checkouts:
        given = mapping(step.get("with"), f"ref: {BASE_BRANCH}")
        require(
            given.get("ref") == BASE_BRANCH, f"ref: {BASE_BRANCH}", f"ref is {given.get('ref')!r}, not {BASE_BRANCH!r}"
        )
        persist = given.get("persist-credentials")
        require(persist is False, "persist-credentials: false", f"persist-credentials is {persist!r}, not False")


def check_no_unsafe_checkout(doc: dict) -> None:
    for step in steps(doc):
        require(UNSAFE_OPTION not in json.dumps(step), "uses: actions/checkout@", f"a step names it: {step!r}")


def check_run_scripts(doc: dict) -> None:
    """Every run step is a row of SCRIPTS, in order, down to the last part of its tree; nothing else runs."""
    # A defaults: mapping of the workflow or a job gives every run step a shell (`bash -c '...; bash {0}'` runs its
    # own text before the script) or a directory other than the checkout. It is refused whatever it holds, as a
    # step's own shell: key is, so the tree reads what the runner's bash runs in the base's checkout.
    for owner in owners(doc):
        detail = f"{owner.label} sets defaults: {owner.scope.get('defaults')!r}; the tree reads the runner's bash"
        require("defaults" not in owner.scope, owner.protects, detail)
    found = [step for step in steps(doc) if "run" in step]
    require(len(found) == len(SCRIPTS), "steps:", f"{len(found)} run steps; the table holds {len(SCRIPTS)}")
    for step, row in zip(found, SCRIPTS):
        name = str(step.get("name", step["run"]))
        script = step["run"]
        require(isinstance(script, str), row.protects, f"the run of the step {name!r} is {script!r}, not a script")
        shell = step.get("shell")
        require(
            shell is None, row.protects, f"the step {name!r} sets shell: {shell!r}; the tree reads the runner's bash"
        )
        require(
            EXPRESSION not in script, row.protects, f"an expression is inlined into the run of {name!r}: {script!r}"
        )
        shape = Reader(name, row.protects).script(shfmt_tree(script, row.protects))
        for index, (got, held) in enumerate(zip_longest(shape, row.script), 1):
            if got != held:
                got_text = f"`{render(got)}`" if got else "missing"
                held_text = f"`{render(held)}`" if held else "nothing"
                detail = f"statement {index} of the step {name!r} is {got_text}; the table holds {held_text} there"
                raise AssertionError(f"{line(row.protects)}: {detail}")


def describe(value: object) -> str:
    """A value with its type, for a message: 0 and False, 1 and True, 10 and '10' read alike without the type."""
    return f"{value!r} ({type(value).__name__})"


def differences(found: object, held: object, path: str = "") -> list[str]:
    """Every point where the document and the table disagree, named by its path (`jobs.regime.steps[0].with.ref`)
    with what was found and what the table holds. The types must agree: PyYAML reads `false` and `0` as different
    inputs and Actions hands an action different strings for them, so a bool is never an int, a str or a float here,
    as `==` would have it (the round-5 audit passed `fetch-depth: false` and `enable-cache: 0` through `==`)."""
    if held is SCRIPT:
        return [] if isinstance(found, str) else [f"{path}: found {describe(found)}, the table holds {held!r}"]
    if type(found) is not type(held):
        return [f"{path}: found {describe(found)}, the table holds {describe(held)}"]
    lines: list[str] = []
    if isinstance(held, dict):
        # the table's keys first: a message points at the line of the key the file holds (`on:` for a renamed `ON:`)
        for key in sorted(set(found) | set(held), key=lambda name: (name not in held, name)):
            at = f"{path}.{key}" if path else key
            if key not in held:
                lines.append(f"{at}: found {describe(found[key])}, the table holds no such key")
            elif key not in found:
                lines.append(f"{at}: found no such key, the table holds {describe(held[key])}")
            else:
                lines.extend(differences(found[key], held[key], at))
    elif isinstance(held, list):
        for index, (got, kept) in enumerate(zip_longest(found, held, fillvalue=MISSING)):
            at = f"{path}[{index}]"
            if kept is MISSING:
                lines.append(f"{at}: found {describe(got)}, the table holds no such item")
            elif got is MISSING:
                lines.append(f"{at}: found no such item, the table holds {describe(kept)}")
            else:
                lines.extend(differences(got, kept, at))
    elif found != held:
        lines.append(f"{path}: found {describe(found)}, the table holds {describe(held)}")
    return lines


def key_line(path: str) -> str:
    """`regime.yml:<n>` of the deepest key of the path the file still holds, so a message points at the mapping an
    added key sits in (`jobs.regime.container` points at `regime:`) or at the key whose value changed."""
    for component in reversed([part.split("[")[0] for part in path.split(".")]):
        key = f"{component}:"
        for number, content in enumerate(WORKFLOW.read_text().splitlines(), 1):
            if content.strip().removeprefix("- ").startswith(key):
                return f"regime.yml:{number} ({key})"
    return "regime.yml:1 (name: regime)"


def check_document(doc: dict) -> None:
    """The document is DOCUMENT and nothing else: every key at every level, every value down to its type, with the
    run texts left to check_run_scripts. The property checks name what each line is for; this one closes the rest."""
    found = differences(doc, DOCUMENT)
    if found:
        path = found[0].split(":", 1)[0]
        raise AssertionError(f"{key_line(path)}: the document is not the table's: {'; '.join(found)}")


def check_step_inputs(doc: dict) -> None:
    """Every step's env: and with: are its row of INPUTS, key for key and value for value, and no env: is inherited:
    no variable the table does not hold reaches a step's shell, and the body reaches the verifier through the one
    PR_BODY the table holds (a run reading it as an expression is refused by check_run_scripts before parsing)."""
    for owner in owners(doc):
        detail = f"{owner.label} sets env: {owner.scope.get('env')!r}; every step's shell would read it first"
        require("env" not in owner.scope, owner.protects, detail)
    found = steps(doc)
    require(len(found) == len(INPUTS), "steps:", f"{len(found)} steps; the table holds {len(INPUTS)}")
    for step, row in zip(found, INPUTS):
        name = step_name(step)
        for key, held in (("env", row.env), ("with", row.options)):
            if held is None:
                detail = f"the step {name!r} sets {key}: {step.get(key)!r}; the table holds no {key}: for it"
                require(key not in step, row.protects, detail)
                continue
            require(key in step, row.protects, f"the step {name!r} has no {key}:; the table holds {held!r}")
            given = mapping(step[key], row.protects)
            found_lines = differences(given, held)
            detail = f"the {key}: of the step {name!r} is not the table's: {'; '.join(found_lines)}"
            require(not found_lines, row.protects, detail)


def check_cancel_in_progress(doc: dict) -> None:
    group = mapping(doc.get("concurrency"), "cancel-in-progress: true")
    require(group.get("cancel-in-progress") is True, "cancel-in-progress: true", f"concurrency is {group!r}")


# The parsed checks in module order: the explanation layer, each naming the property a change took away.
PARSED_CHECKS = (
    check_trigger,
    check_permissions,
    check_checkout,
    check_no_unsafe_checkout,
    check_run_scripts,
    check_document,
    check_step_inputs,
    check_cancel_in_progress,
)


def regime_job(doc: dict) -> dict:
    return doc["jobs"]["regime"]


def regime_steps(doc: dict) -> list[dict]:
    return regime_job(doc)["steps"]


def run_step(doc: dict, index: int) -> dict:
    return [step for step in regime_steps(doc) if "run" in step][index]


def fetch_step(doc: dict) -> dict:
    return run_step(doc, 0)


def verify_step(doc: dict) -> dict:
    return run_step(doc, 1)


def rounds_step(doc: dict) -> dict:
    return run_step(doc, 2)


def edits(*mutations: Callable[[dict], None]) -> Callable[[dict], None]:
    """Several edits of one copy, applied in order."""

    def mutate(doc: dict) -> None:
        for mutation in mutations:
            mutation(doc)

    return mutate


def checkout_step(doc: dict) -> dict:
    return next(step for step in regime_steps(doc) if step.get("uses", "").startswith("actions/checkout@"))


def checkout_options(doc: dict) -> dict:
    return checkout_step(doc)["with"]


def setup_options(doc: dict) -> dict:
    return next(step["with"] for step in regime_steps(doc) if step.get("uses", "").startswith("astral-sh/setup-uv@"))


def fetch_env(doc: dict) -> dict:
    return fetch_step(doc)["env"]


def body_env(doc: dict) -> dict:
    return verify_step(doc)["env"]


def triggers(doc: dict) -> dict:
    return doc["on"]


def set_in(getter: Callable[[dict], dict], key: str, value: object) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)[key] = value

    return mutate


def delete_in(getter: Callable[[dict], dict], key: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        del getter(doc)[key]

    return mutate


def spell_trigger(spelling: str) -> Callable[[dict], None]:
    """The trigger key written another way in its place: what PyYAML's own resolver reads as `on` (true, yes, On)."""

    def mutate(doc: dict) -> None:
        items = [(spelling if key == "on" else key, value) for key, value in doc.items()]
        doc.clear()
        doc.update(items)

    return mutate


def append_run(getter: Callable[[dict], dict], text: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)["run"] += text

    return mutate


def replace_run(getter: Callable[[dict], dict], old: str, new: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)["run"] = getter(doc)["run"].replace(old, new)

    return mutate


def add_step(step: dict) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        regime_steps(doc).append(step)

    return mutate


class Mutation(NamedTuple):
    """One edit that takes a property away, and a fragment the refusal must name: the message says what was refused."""

    edit: Callable[[dict], None]
    names: str


class Invariant(NamedTuple):
    """One safety property: the check that holds on the head, and the edits that must each turn it red."""

    check: Callable[[dict], None]
    breaks: dict[str, Mutation]


REFMAP = "--no-tags --update-head-ok --refmap=+refs/pull/${PR_NUMBER}/head:refs/heads/main"
# the defaults.run.shell the round-3 audit ran: the runner's bash checks the head out, then runs the step's script
INHERITED_SHELL = {"run": {"shell": f"bash -c 'git checkout {HEAD_REF}; bash {{0}}'"}}
TRIGGER = Invariant(
    check_trigger,
    {
        "a second trigger": Mutation(set_in(triggers, "push", {"branches": ["main"]}), "'push'"),
        "a wider branch filter": Mutation(
            set_in(lambda d: triggers(d)["pull_request_target"], "branches", ["main", "release"]), "'release'"
        ),
        "no branch filter": Mutation(delete_in(lambda d: triggers(d)["pull_request_target"], "branches"), "None"),
        # the round-6 audit's edit: PyYAML's own resolver read `true:` as the key `on` and every check passed
        "the trigger key spelled true": Mutation(spell_trigger("true"), "no on: key; the keys are ['name', 'true'"),
        "the trigger key spelled yes": Mutation(spell_trigger("yes"), "no on: key; the keys are ['name', 'yes'"),
        "the trigger key spelled On": Mutation(spell_trigger("On"), "no on: key; the keys are ['name', 'On'"),
    },
)
PERMISSIONS = Invariant(
    check_permissions,
    {
        "contents: write": Mutation(set_in(lambda d: d["permissions"], "contents", "write"), "'write'"),
        "a second scope": Mutation(set_in(lambda d: d["permissions"], "pull-requests", "write"), "'pull-requests'"),
        "a job that writes": Mutation(set_in(regime_job, "permissions", {"contents": "write"}), "job regime grants"),
        "a job with write-all": Mutation(set_in(regime_job, "permissions", "write-all"), "'write-all'"),
    },
)
CHECKOUT = Invariant(
    check_checkout,
    {
        "no ref": Mutation(delete_in(checkout_options, "ref"), "ref is None"),
        "the head as ref": Mutation(set_in(checkout_options, "ref", HEAD_EXPRESSION), "head.sha"),
        "no persist-credentials": Mutation(delete_in(checkout_options, "persist-credentials"), "is None"),
        "persist-credentials: true": Mutation(set_in(checkout_options, "persist-credentials", True), "is True"),
    },
)
UNSAFE_CHECKOUT = Invariant(
    check_no_unsafe_checkout,
    {
        "the option on the checkout": Mutation(set_in(checkout_options, UNSAFE_OPTION, True), UNSAFE_OPTION),
        "the option in a run": Mutation(append_run(verify_step, f" --{UNSAFE_OPTION}"), UNSAFE_OPTION),
    },
)
RUN_SCRIPTS = Invariant(
    check_run_scripts,
    {
        # the fetch: another target, source, option set or repository
        "a fetch into a branch": Mutation(replace_run(fetch_step, HEAD_REF, "refs/heads/pr"), "refs/heads/pr"),
        "a fetch of the merge ref": Mutation(replace_run(fetch_step, "/head:", "/merge:"), "/merge:"),
        "a refmap that moves main": Mutation(replace_run(fetch_step, "--no-tags", REFMAP), "--update-head-ok"),
        "a fetch into another repository": Mutation(replace_run(fetch_step, "git", "GIT_DIR=/other git"), "Assigns"),
        "a fetch from another directory": Mutation(replace_run(fetch_step, "git fetch", "git -C /other fetch"), "-C"),
        "a second fetch of the head": Mutation(
            append_run(fetch_step, 'git fetch origin "${HEAD_SHA}"\n'), 'git fetch origin "${HEAD_SHA}"'
        ),
        "no fetch at all": Mutation(set_in(fetch_step, "run", "true\n"), "`true`"),
        "an empty fetch step": Mutation(set_in(fetch_step, "run", "\n"), "is missing"),
        # a statement that moves HEAD or the work tree, in every form the two text readers accepted
        "a checkout of the fetched head": Mutation(
            append_run(fetch_step, f"git checkout {HEAD_REF}\n"), f"git checkout {HEAD_REF}"
        ),
        "HEAD moved onto the fetched head": Mutation(
            append_run(fetch_step, f"git update-ref --no-deref HEAD {HEAD_REF}\n"), "update-ref --no-deref HEAD"
        ),
        "git spelled around an empty quote": Mutation(
            append_run(fetch_step, f"g''it update-ref --no-deref HEAD {HEAD_REF}\n"), "SglQuoted"
        ),
        "the fetch commented out": Mutation(replace_run(fetch_step, "git fetch", "# git fetch"), "a comment"),
        "a comment ending in a backslash": Mutation(
            replace_run(fetch_step, "\ntest", f" # as data \\\ngit checkout {HEAD_REF}\ntest"), "a comment"
        ),
        "a checkout chained to the fetch": Mutation(
            replace_run(fetch_step, "\ntest", f" && git checkout {HEAD_REF}\ntest"), "BinaryCmd"
        ),
        "a checkout after a semicolon": Mutation(
            replace_run(fetch_step, "\ntest", f"; git checkout {HEAD_REF}\ntest"), "a semicolon"
        ),
        "a semicolon between the pinned statements": Mutation(
            replace_run(fetch_step, "\ntest", "; test"), "a semicolon"
        ),
        "a semicolon ending the fetch": Mutation(replace_run(fetch_step, "\ntest", ";\ntest"), "a semicolon"),
        "a checkout in a substitution": Mutation(
            replace_run(fetch_step, f"rev-parse {HEAD_REF}", f"checkout {HEAD_REF}"), f"git checkout {HEAD_REF}"
        ),
        "the fetch's output redirected": Mutation(replace_run(fetch_step, "\ntest", " > log\ntest"), "Redirs"),
        # the verifier: another base, script, expansion or shell
        "the base taken from the fetched head": Mutation(
            replace_run(verify_step, "rev-parse HEAD", f"rev-parse {HEAD_REF}"), f"rev-parse {HEAD_REF}"
        ),
        "another verifier": Mutation(replace_run(verify_step, VERIFIER, "scripts/other.py"), "scripts/other.py"),
        "a default for the head sha": Mutation(replace_run(verify_step, "${HEAD_SHA}", "${HEAD_SHA:-HEAD}"), "Exp"),
        "the base in backquotes": Mutation(
            replace_run(verify_step, "$(git rev-parse HEAD)", "`git rev-parse HEAD`"), "Backquotes"
        ),
        # the base sha's status (standing order 21, round 3): unread, ignored, softened, or the assignment in another form
        "the base's status unread": Mutation(
            edits(
                replace_run(verify_step, f"{CHECKED_BASE}\n", ""),
                replace_run(verify_step, '"${base}"', '"$(git rev-parse HEAD)"'),
            ),
            f"`{CHECKED_BASE}` there",
        ),
        "the base's status ignored": Mutation(replace_run(verify_step, "|| exit 1", "|| true"), "not `exit 1`"),
        "the base's failure softened to exit 0": Mutation(
            replace_run(verify_step, "|| exit 1", "|| exit 0"), "not `exit 1`"
        ),
        "the base chained with &&": Mutation(
            replace_run(verify_step, "|| exit 1", "&& true"), "BinaryCmd joined by &&"
        ),
        "a command word after the assignment": Mutation(
            replace_run(verify_step, "$(git rev-parse HEAD) ||", "$(git rev-parse HEAD) true ||"), "Args"
        ),
        "a second assignment": Mutation(replace_run(verify_step, "\nbase=$(", "\nother=1 base=$("), "2 assignments"),
        "the base appended": Mutation(replace_run(verify_step, "base=$(", "base+=$("), "Append"),
        "the base as an array": Mutation(
            replace_run(verify_step, "base=$(git rev-parse HEAD)", "base=($(git rev-parse HEAD))"), "Array"
        ),
        "the base declared local": Mutation(replace_run(verify_step, "\nbase=$(", "\nlocal base=$("), "DeclClause"),
        "the base read through a pipeline": Mutation(
            replace_run(verify_step, "$(git rev-parse HEAD)", "$(git rev-parse HEAD | cat)"), "BinaryCmd joined by |"
        ),
        "the base unquoted": Mutation(replace_run(verify_step, '"${base}"', "${base}"), "--base ${base} --head"),
        "no set -euo pipefail": Mutation(
            replace_run(verify_step, "set -euo pipefail\n", ""), "`set -euo pipefail` there"
        ),
        # the round-cap step: the same status, and its base taken from the fetched head
        "the round cap's base status unread": Mutation(
            edits(
                replace_run(rounds_step, f"{CHECKED_BASE}\n", ""),
                replace_run(rounds_step, '"${base}"', '"$(git rev-parse HEAD)"'),
            ),
            f"`{CHECKED_BASE}` there",
        ),
        "the round cap's base taken from the fetched head": Mutation(
            replace_run(rounds_step, "rev-parse HEAD", f"rev-parse {HEAD_REF}"), f"rev-parse {HEAD_REF}"
        ),
        "the head sha inlined into run": Mutation(replace_run(verify_step, "${HEAD_SHA}", HEAD_EXPRESSION), EXPRESSION),
        "the body inlined into run": Mutation(append_run(verify_step, f' --body "{BODY_CARRIER}"'), EXPRESSION),
        "another shell": Mutation(set_in(verify_step, "shell", "python"), "shell"),
        # a shell or directory every run step inherits: the workflow's or the job's defaults: mapping
        "a default shell for the workflow": Mutation(set_in(lambda d: d, "defaults", INHERITED_SHELL), "bash {0}"),
        "a default shell for the job": Mutation(set_in(regime_job, "defaults", INHERITED_SHELL), "bash {0}"),
        "a default directory for the job": Mutation(
            set_in(regime_job, "defaults", {"run": {"working-directory": "/other"}}), "working-directory"
        ),
        "a fourth run step": Mutation(add_step({"run": f"git checkout {HEAD_REF}\n"}), "4 run steps"),
    },
)
# the round-4 audit's edit: bash reads BASH_ENV at the start of every non-interactive shell, so the verifier step ran
# on the fetched head while its run text, its tree and every other check were unchanged
STARTUP = f"$(git checkout {HEAD_REF})"
BASE_EXPRESSION = "${{ github.event.pull_request.base.sha }}"
STEP_INPUTS = Invariant(
    check_step_inputs,
    {
        # a variable every step inherits: the workflow's or the job's env: mapping
        "BASH_ENV in the job's env": Mutation(set_in(regime_job, "env", {"BASH_ENV": STARTUP}), "BASH_ENV"),
        "BASH_ENV in the workflow's env": Mutation(set_in(lambda d: d, "env", {"BASH_ENV": STARTUP}), "BASH_ENV"),
        "a second env carries the body": Mutation(
            set_in(regime_job, "env", {BODY_VARIABLE: BODY_CARRIER}), f"sets env: {{'{BODY_VARIABLE}'"
        ),
        # a variable added to one step's env, or an env: on a step the table holds none for
        "BASH_ENV in the verifier step's env": Mutation(set_in(body_env, "BASH_ENV", STARTUP), "BASH_ENV: found"),
        "BASH_ENV in the fetch step's env": Mutation(set_in(fetch_env, "BASH_ENV", STARTUP), "BASH_ENV: found"),
        "BASH_ENV in the checkout step's env": Mutation(
            set_in(checkout_step, "env", {"BASH_ENV": STARTUP}), "sets env: {'BASH_ENV'"
        ),
        "PATH in the verifier step's env": Mutation(set_in(body_env, "PATH", "/tmp/head/bin:/usr/bin"), "PATH: found"),
        "GIT_DIR in the verifier step's env": Mutation(
            set_in(body_env, "GIT_DIR", "/tmp/other/.git"), "GIT_DIR: found"
        ),
        "the env as a string": Mutation(set_in(verify_step, "env", f"BASH_ENV={STARTUP}"), "found 'BASH_ENV="),
        # another value or source for a pinned variable, or a pinned variable gone
        "the base sha as the head sha": Mutation(
            set_in(body_env, "HEAD_SHA", BASE_EXPRESSION), f"HEAD_SHA: found {BASE_EXPRESSION!r}"
        ),
        "another pull request's number": Mutation(set_in(fetch_env, "PR_NUMBER", "1"), "PR_NUMBER: found '1'"),
        "no env carries the body": Mutation(delete_in(body_env, BODY_VARIABLE), f"{BODY_VARIABLE}: found no such key"),
        "the body's name as a literal": Mutation(
            set_in(body_env, BODY_VARIABLE, "github.event.pull_request.body"),
            f"{BODY_VARIABLE}: found 'github.event.pull_request.body'",
        ),
        "a boolean of the body": Mutation(
            set_in(body_env, BODY_VARIABLE, "${{ github.event.pull_request.body != '' }}"), f"{BODY_VARIABLE}: found"
        ),
        "no env on the verifier step": Mutation(delete_in(verify_step, "env"), "has no env:"),
        # the other input channel: a with: on a run step, a changed or missing with: on an action step
        "a with: on the verifier step": Mutation(set_in(verify_step, "with", {"ref": HEAD_REF}), "sets with: {'ref'"),
        "a with: on the fetch step": Mutation(set_in(fetch_step, "with", {"ref": HEAD_REF}), "sets with: {'ref'"),
        "a deeper checkout": Mutation(set_in(checkout_options, "fetch-depth", 1), "fetch-depth: found 1"),
        "submodules on the checkout": Mutation(set_in(checkout_options, "submodules", True), "submodules: found True"),
        "no checkout options": Mutation(delete_in(checkout_step, "with"), "has no with:"),
        "a cache for setup-uv": Mutation(set_in(setup_options, "enable-cache", True), "enable-cache: found True"),
        # the round-5 audit's edits: `==` has False equal to 0 and True to 1, and Actions passes the strings apart
        "fetch-depth as a boolean": Mutation(
            set_in(checkout_options, "fetch-depth", False), "fetch-depth: found False (bool), the table holds 0 (int)"
        ),
        "enable-cache as a number": Mutation(
            set_in(setup_options, "enable-cache", 0), "enable-cache: found 0 (int), the table holds False (bool)"
        ),
        "persist-credentials as a string": Mutation(
            set_in(checkout_options, "persist-credentials", "false"), "found 'false' (str), the table holds False"
        ),
        "a sixth step": Mutation(add_step({"uses": "actions/setup-node@v4"}), "6 steps"),
    },
)
CANCEL_IN_PROGRESS = Invariant(
    check_cancel_in_progress,
    {
        "cancel-in-progress: false": Mutation(
            set_in(lambda d: d["concurrency"], "cancel-in-progress", False), "'cancel-in-progress': False"
        ),
        "no concurrency group": Mutation(delete_in(lambda d: d, "concurrency"), "found None"),
        # what the reader hands over for `cancel-in-progress: yes`: the string, not PyYAML's own True
        "cancel-in-progress: yes": Mutation(
            set_in(lambda d: d["concurrency"], "cancel-in-progress", "yes"), "'cancel-in-progress': 'yes'"
        ),
    },
)
# the round-5 audit's edit: a container whose image the pull request names runs every step inside code of the pull
# request's choosing, while the steps, their scripts, their env: and their with: are unchanged
CONTAINER = {"image": TITLE_EXPRESSION}
DOCUMENT_SHAPE = Invariant(
    check_document,
    {
        # a key of the job no table holds: it runs or hosts code, or moves the job, past every other check
        "a container from the pull request's title": Mutation(
            set_in(regime_job, "container", CONTAINER), "jobs.regime.container: found {'image'"
        ),
        "a container image as a string": Mutation(set_in(regime_job, "container", "node:20"), "jobs.regime.container"),
        "a service from the pull request's title": Mutation(
            set_in(regime_job, "services", {"db": CONTAINER}), "jobs.regime.services"
        ),
        "a strategy matrix": Mutation(
            set_in(regime_job, "strategy", {"matrix": {"ref": [HEAD_REF]}}), "jobs.regime.strategy"
        ),
        "an environment for the job": Mutation(set_in(regime_job, "environment", "release"), "jobs.regime.environment"),
        "a job that continues on error": Mutation(
            set_in(regime_job, "continue-on-error", True), "jobs.regime.continue-on-error"
        ),
        "a runner from the pull request's title": Mutation(
            set_in(regime_job, "runs-on", TITLE_EXPRESSION), "jobs.regime.runs-on"
        ),
        "a self-hosted runner": Mutation(
            set_in(regime_job, "runs-on", ["self-hosted"]), "jobs.regime.runs-on: found ['self-hosted'] (list)"
        ),
        "no timeout": Mutation(delete_in(regime_job, "timeout-minutes"), "jobs.regime.timeout-minutes: found no such"),
        # a second job, a key of the workflow, or a trigger beside the one
        "a second job": Mutation(
            set_in(lambda d: d["jobs"], "build", {"runs-on": "ubuntu-24.04", "steps": [{"run": "make\n"}]}),
            "jobs.build",
        ),
        "a run-name from the pull request's title": Mutation(
            set_in(lambda d: d, "run-name", TITLE_EXPRESSION), "run-name: found"
        ),
        "a manual trigger": Mutation(set_in(triggers, "workflow_dispatch", {}), "on.workflow_dispatch"),
        "a shorter types list": Mutation(
            set_in(lambda d: triggers(d)["pull_request_target"], "types", ["opened"]),
            "on.pull_request_target.types[1]: found no such item",
        ),
        # the round-6 audit's edit, as the reader now hands it over: another key where the table holds `on`
        "the trigger key spelled true": Mutation(spell_trigger("true"), "on: found no such key"),
        "the trigger key spelled yes": Mutation(spell_trigger("yes"), "on: found no such key"),
        # a key of a step no table holds, or an action other than the pinned one
        "another checkout action": Mutation(
            set_in(checkout_step, "uses", "actions/checkout@v4"), "jobs.regime.steps[0].uses"
        ),
        "a local action": Mutation(
            set_in(lambda d: regime_steps(d)[1], "uses", "./.github/actions/setup-uv"), "jobs.regime.steps[1].uses"
        ),
        "a condition on the verifier step": Mutation(
            set_in(verify_step, "if", "github.event.pull_request.draft == false"), "jobs.regime.steps[3].if"
        ),
        "a working directory for the verifier": Mutation(
            set_in(verify_step, "working-directory", "/tmp/head"), "jobs.regime.steps[3].working-directory"
        ),
        "a step that continues on error": Mutation(
            set_in(fetch_step, "continue-on-error", True), "jobs.regime.steps[2].continue-on-error"
        ),
        "the fetch run as a list": Mutation(
            set_in(fetch_step, "run", ["git", "fetch"]), "jobs.regime.steps[2].run: found ['git', 'fetch'] (list)"
        ),
        # the round-5 audit's other edits: a value whose type differs from the table's, equal under `==`
        "fetch-depth as a boolean": Mutation(
            set_in(checkout_options, "fetch-depth", False),
            "jobs.regime.steps[0].with.fetch-depth: found False (bool), the table holds 0 (int)",
        ),
        "enable-cache as a number": Mutation(
            set_in(setup_options, "enable-cache", 0),
            "jobs.regime.steps[1].with.enable-cache: found 0 (int), the table holds False (bool)",
        ),
        "persist-credentials as a string": Mutation(
            set_in(checkout_options, "persist-credentials", "false"),
            "jobs.regime.steps[0].with.persist-credentials: found 'false' (str), the table holds False (bool)",
        ),
        "fetch-depth as a float": Mutation(
            set_in(checkout_options, "fetch-depth", 0.0),
            "jobs.regime.steps[0].with.fetch-depth: found 0.0 (float), the table holds 0 (int)",
        ),
        "the timeout as a string": Mutation(
            set_in(regime_job, "timeout-minutes", "10"),
            "jobs.regime.timeout-minutes: found '10' (str), the table holds 10 (int)",
        ),
        "cancel-in-progress as a number": Mutation(
            set_in(lambda d: d["concurrency"], "cancel-in-progress", 1),
            "concurrency.cancel-in-progress: found 1 (int), the table holds True (bool)",
        ),
        # the YAML 1.1 forms the reader no longer reads as booleans: each is a string where the table holds a bool
        "cancel-in-progress as the word yes": Mutation(
            set_in(lambda d: d["concurrency"], "cancel-in-progress", "yes"),
            "concurrency.cancel-in-progress: found 'yes' (str), the table holds True (bool)",
        ),
        "persist-credentials as the word off": Mutation(
            set_in(checkout_options, "persist-credentials", "off"),
            "jobs.regime.steps[0].with.persist-credentials: found 'off' (str), the table holds False (bool)",
        ),
        "enable-cache as the word no": Mutation(
            set_in(setup_options, "enable-cache", "no"),
            "jobs.regime.steps[1].with.enable-cache: found 'no' (str), the table holds False (bool)",
        ),
    },
)


class BytePinTest(unittest.TestCase):
    """The first check: the head's regime.yml is the pinned bytes with the pinned sha256, before anything is parsed."""

    def test_the_file_is_the_pinned_bytes_and_their_sha256(self) -> None:
        check_bytes(WORKFLOW)
        self.assertEqual(hashlib.sha256(WORKFLOW_BYTES.encode()).hexdigest(), WORKFLOW_SHA256)

    def test_a_sha256_that_is_not_the_bytes_is_refused_naming_both(self) -> None:
        # The two constants change together: a pin whose literal was updated and whose digest was not is refused
        # although the file is the literal's bytes, so a reviewer's `shasum -a 256` always agrees with the module.
        with mock.patch.object(sys.modules[__name__], "WORKFLOW_SHA256", "0" * 64):
            with self.assertRaises(AssertionError) as caught:
                check_bytes(WORKFLOW)
        message = str(caught.exception)
        self.assertIn(f"the file is the pinned bytes, but their sha256 is {WORKFLOW_SHA256}", message)
        self.assertIn(f"WORKFLOW_SHA256 is {'0' * 64}", message)


class RegimeWorkflowTest(unittest.TestCase):
    """The head's regime.yml holds every property; a failure message names the line to restore."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)

    def test_the_only_trigger_is_pull_request_target_into_main(self) -> None:
        check_trigger(self.doc)

    def test_the_token_is_contents_read_and_no_job_widens_it(self) -> None:
        check_permissions(self.doc)

    def test_every_checkout_takes_the_base_branch_without_credentials(self) -> None:
        check_checkout(self.doc)

    def test_no_step_names_the_unsafe_pr_checkout_option(self) -> None:
        check_no_unsafe_checkout(self.doc)

    def test_the_run_scripts_are_the_table_s_statements_and_nothing_else(self) -> None:
        check_run_scripts(self.doc)

    def test_every_step_s_env_and_with_are_the_table_s_and_no_env_is_inherited(self) -> None:
        check_step_inputs(self.doc)

    def test_a_newer_head_cancels_the_older_run(self) -> None:
        check_cancel_in_progress(self.doc)

    def test_the_document_is_the_table_s_and_nothing_else(self) -> None:
        check_document(self.doc)


class RedCopyTest(unittest.TestCase):
    """Each check goes red on a copy of the workflow with its property taken away, so a regression cannot pass."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)

    def goes_red(self, invariant: Invariant) -> None:
        self.assertTrue(invariant.breaks)
        for label, mutation in invariant.breaks.items():
            with self.subTest(label):
                broken = copy.deepcopy(self.doc)
                mutation.edit(broken)
                # the strict comparison: `==` would read `fetch-depth: false` as the file's own 0
                self.assertTrue(differences(broken, self.doc), f"regime.yml already carries this edit: {label}")
                with self.assertRaises(AssertionError) as caught:
                    invariant.check(broken)
                self.assertIn("regime.yml", str(caught.exception))
                self.assertIn(mutation.names, str(caught.exception))

    def test_the_trigger_check_goes_red(self) -> None:
        self.goes_red(TRIGGER)

    def test_the_permissions_check_goes_red(self) -> None:
        self.goes_red(PERMISSIONS)

    def test_the_checkout_check_goes_red(self) -> None:
        self.goes_red(CHECKOUT)

    def test_the_unsafe_option_check_goes_red(self) -> None:
        self.goes_red(UNSAFE_CHECKOUT)

    def test_the_run_script_check_goes_red(self) -> None:
        self.goes_red(RUN_SCRIPTS)

    def test_the_step_input_check_goes_red(self) -> None:
        self.goes_red(STEP_INPUTS)

    def test_the_cancel_in_progress_check_goes_red(self) -> None:
        self.goes_red(CANCEL_IN_PROGRESS)

    def test_the_document_check_goes_red(self) -> None:
        self.goes_red(DOCUMENT_SHAPE)

    def test_a_workflow_the_parser_cannot_read_fails_instead_of_passing(self) -> None:
        # Standing order 21: a failed read is never an absence. A parse error stops the suite, and a document that is
        # not a mapping is refused before any check could read its missing keys as "nothing to widen".
        with tempfile.TemporaryDirectory() as temp:
            broken = Path(temp) / "regime.yml"
            broken.write_text("on: [\n")
            with self.assertRaises(subprocess.CalledProcessError):
                load(broken)
            broken.write_text("- a list\n")
            with self.assertRaises(AssertionError):
                load(broken)


class RawEdit(NamedTuple):
    """One edit of the file's text that the parsed form may hide: the edit on the bytes, the regime.yml line the byte
    check must name first, and whether every property check passes on the parsed copy (then the byte check is the only
    control for it; otherwise the property checks also explain it)."""

    edit: Callable[[bytes], bytes]
    line: int
    parses_the_same: bool


def swap(old: str, new: str) -> Callable[[bytes], bytes]:
    """The one occurrence of `old` in the file replaced by `new`: an edit of the text, not of a parsed copy."""

    def edit(text: bytes) -> bytes:
        count = text.count(old.encode())
        if count != 1:
            raise AssertionError(f"{old!r} occurs {count} times in the pinned bytes, not once")
        return text.replace(old.encode(), new.encode())

    return edit


STRAY_RUN = f"        run: git checkout {HEAD_REF}\n"
# The edits the parser cannot tell from the file, or tells apart only by chance: the round-7 audit's two duplicate
# keys (SafeLoader keeps the last value and says nothing, so the parsed copy is the table's while GitHub reads another
# file or refuses it), the round-6 audit's spelling, and the text-level changes no parsed check could ever see.
RAW_EDITS = {
    "a duplicate run: key on the verifier step (the auditor's edit)": RawEdit(
        swap(
            f"        run: |\n          set -euo pipefail\n          {CHECKED_BASE}\n          uv run --no-config"
            f" --no-project python -I {VERIFIER}",
            f"{STRAY_RUN}        run: |\n          set -euo pipefail\n          {CHECKED_BASE}\n          uv run"
            f" --no-config --no-project python -I {VERIFIER}",
        ),
        53,
        True,
    ),
    "a duplicate run: key on the fetch step": RawEdit(
        swap("        run: |\n          git fetch", f"{STRAY_RUN}        run: |\n          git fetch"), 41, True
    ),
    "a duplicate permissions: key (the auditor's edit)": RawEdit(
        swap("\npermissions:\n", "\npermissions: write-all\npermissions:\n"), 19, True
    ),
    "the trigger key spelled true": RawEdit(swap("\non:\n", "\ntrue:\n"), 10, False),
    "a trailing space": RawEdit(swap("  contents: read\n", "  contents: read \n"), 20, True),
    "an indentation that parses the same": RawEdit(
        swap(
            f"  group: regime-pr-{NUMBER_EXPRESSION}\n  cancel-in-progress: true\n",
            f"    group: regime-pr-{NUMBER_EXPRESSION}\n    cancel-in-progress: true\n",
        ),
        16,
        True,
    ),
    "a comment": RawEdit(swap("\npermissions:\n", "\n# the token\npermissions:\n"), 19, True),
    "CRLF line endings": RawEdit(lambda text: text.replace(b"\n", b"\r\n"), 1, True),
    "a byte order mark": RawEdit(lambda text: b"\xef\xbb\xbf" + text, 1, True),
}


class RawTextTest(unittest.TestCase):
    """Each edit of the file's text fails the byte check with the diff naming its first line, whether or not the parsed
    copy still passes every property check: for most of these edits it does, and the byte check is the one control."""

    def edited(self, label: str, raw: RawEdit) -> Path:
        text = raw.edit(WORKFLOW_BYTES.encode())
        self.assertNotEqual(text, WORKFLOW_BYTES.encode(), f"the edit changed nothing: {label}")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        edited = Path(temp.name) / "regime.yml"
        edited.write_bytes(text)
        return edited

    def test_every_raw_text_edit_fails_the_byte_check_with_a_diff_naming_its_first_line(self) -> None:
        for label, raw in RAW_EDITS.items():
            with self.subTest(label):
                edited = self.edited(label, raw)
                with self.assertRaises(AssertionError) as caught:
                    check_bytes(edited)
                message = str(caught.exception)
                self.assertTrue(message.startswith(f"regime.yml:{raw.line}: the file is not the pinned bytes"), message)
                self.assertIn(f"the first difference is line {raw.line}: found ", message)
                self.assertIn(f"its sha256 is {hashlib.sha256(edited.read_bytes()).hexdigest()}", message)
                self.assertIn(f"the pin's is {WORKFLOW_SHA256}", message)
                self.assertIn("updates WORKFLOW_BYTES and WORKFLOW_SHA256", message)
                for marker in ("\n--- WORKFLOW_BYTES (the pin)", "\n+++ regime.yml (the file)", "\n@@ -", "\n+", "\n-"):
                    self.assertIn(marker, message)

    def test_the_property_checks_see_only_the_edits_the_table_says_they_see(self) -> None:
        # The explanation layer's reach, measured: the parsed copy of most edits passes every property check (the
        # parser hands over the table's document), so no check but the byte check stands between them and the suite.
        for label, raw in RAW_EDITS.items():
            with self.subTest(label):
                doc = load(self.edited(label, raw))
                refused = []
                for check in PARSED_CHECKS:
                    try:
                        check(doc)
                    except AssertionError as error:
                        refused.append(f"{check.__name__}: {error}")
                if raw.parses_the_same:
                    self.assertEqual(refused, [], f"a property check sees {label}; the table says none does")
                else:
                    self.assertTrue(refused, f"no property check sees {label}; the table says one does")


class LoaderTest(unittest.TestCase):
    """The reader's booleans are YAML 1.2's: `on` is the key `on`, and a trigger key spelled another way is refused."""

    def test_the_dropped_forms_read_as_strings_and_true_and_false_as_booleans(self) -> None:
        # PyYAML's own resolver reads every DROPPED_FORMS entry as a boolean, as a key and as a value; this reader
        # hands each over as the string the file spells, and keeps the six spellings of true and false.
        with tempfile.TemporaryDirectory() as temp:
            forms = Path(temp) / "forms.yml"
            forms.write_text("".join(f"{form}: {form}\n" for form in DROPPED_FORMS))
            self.assertEqual(load(forms), {form: form for form in DROPPED_FORMS})
            forms.write_text("".join(f"key{index}: {form}\n" for index, form in enumerate(BOOLEANS.split("|"))))
            self.assertEqual(list(load(forms).values()), [True, True, True, False, False, False])

    def test_a_trigger_key_spelled_true_or_yes_is_refused_naming_on(self) -> None:
        # The round-6 audit's edit, as text: `on:` renamed to `true:` in the file read as the key `on` and every
        # check passed, while GitHub found no trigger. Each spelling is now a missing `on`, named by both checks.
        text = WORKFLOW.read_text()
        self.assertEqual(text.count("\non:\n"), 1)
        with tempfile.TemporaryDirectory() as temp:
            edited = Path(temp) / "regime.yml"
            for spelling in ("true", "yes", "True", "ON"):
                with self.subTest(spelling):
                    edited.write_text(text.replace("\non:\n", f"\n{spelling}:\n"))
                    doc = load(edited)
                    self.assertNotIn("on", doc)
                    for check, names in ((check_trigger, "no on: key"), (check_document, "on: found no such key")):
                        with self.assertRaises(AssertionError) as caught:
                            check(doc)
                        self.assertIn(line("on:"), str(caught.exception))
                        self.assertIn(names, str(caught.exception))


class PinnedParserTest(unittest.TestCase):
    """Read by the pinned shfmt alone: no shfmt, another version, a nonzero status or no tree fails instead of passing."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)
        cls.pin = tomllib.loads(MISE_CONFIG.read_text())["tools"]["http:shfmt"]["version"]

    def path_with(self, shfmt: str | None) -> str:
        """A PATH holding what the pin guard runs (bash, awk) and the given shfmt script, or no shfmt at all."""
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        for tool in ("bash", "awk"):
            found = shutil.which(tool)
            self.assertIsNotNone(found, tool)
            os.symlink(found, Path(temp.name) / tool)
        if shfmt is not None:
            fake = Path(temp.name) / "shfmt"
            fake.write_text(shfmt)
            fake.chmod(0o755)
        return temp.name

    def refusal(self, path: str) -> str:
        with mock.patch.dict(os.environ, {"PATH": path}), self.assertRaises(AssertionError) as caught:
            check_run_scripts(self.doc)
        return str(caught.exception)

    def test_no_shfmt_on_path_fails_the_check(self) -> None:
        message = self.refusal(self.path_with(None))
        self.assertIn("regime.yml", message)
        self.assertIn(f'"shfmt --version" failed; {MISE_CONFIG} pins shfmt {self.pin}', message)

    def test_a_shfmt_that_is_not_the_pin_fails_the_check_naming_both(self) -> None:
        message = self.refusal(self.path_with("#!/bin/sh\necho v0.0.1\n"))
        self.assertIn(f"the shfmt on PATH is version 0.0.1, but {MISE_CONFIG} pins shfmt {self.pin}", message)

    def test_a_shfmt_that_gives_no_tree_fails_the_check(self) -> None:
        # The pinned version, answering with no JSON tree: refused, never read as a script with nothing in it.
        fake = f'#!/bin/sh\n[ "$1" = --version ] && {{ echo v{self.pin}; exit 0; }}\necho "[]"\n'
        self.assertIn("shfmt gave no JSON syntax tree", self.refusal(self.path_with(fake)))

    def test_a_shfmt_that_exits_nonzero_with_a_tree_fails_the_check_naming_the_status(self) -> None:
        # Standing order 21: the status is read before the output. The pinned version printing the real tree and
        # exiting 3 is refused with the status named, never read as a tree that happens to match the table.
        real = shutil.which("shfmt")
        self.assertIsNotNone(real, "shfmt")
        fake = f'#!/bin/sh\n[ "$1" = --version ] && {{ echo v{self.pin}; exit 0; }}\n"{real}" "$@"\nexit 3\n'
        message = self.refusal(self.path_with(fake))
        self.assertIn("shfmt exited 3 on the run script", message)


# the shas the step-run fixtures hand the steps: the fake git prints BASE_FIXTURE, env: carries HEAD_FIXTURE
BASE_FIXTURE = "a" * 40
HEAD_FIXTURE = "b" * 40


class StepRunTest(unittest.TestCase):
    """The two verifier steps' scripts, run as the runner's bash runs them, read the status of the git that produces
    the base sha (standing order 21): a git that prints a sha and exits non-zero ends the step before the verifier
    runs. On 05a48d78 the sha went into `--base "$(git rev-parse HEAD)"` and the status was lost."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load(WORKFLOW)

    def run_step(self, index: int, git_status: int) -> tuple[subprocess.CompletedProcess[str], Path]:
        """The step's script under `bash -e` with a PATH holding a git that prints BASE and exits `git_status`, and a
        uv that records its arguments instead of running; HEAD_SHA is the one env: variable both steps hold."""
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        tools = root / "bin"
        tools.mkdir()
        recorded = root / "uv-arguments"
        (tools / "git").write_text(f"#!/bin/sh\necho {BASE_FIXTURE}\nexit {git_status}\n")
        (tools / "uv").write_text(f"#!/bin/sh\nprintf '%s\\n' \"$@\" > '{recorded}'\n")
        for tool in (tools / "git", tools / "uv"):
            tool.chmod(0o755)
        script = root / "step.sh"
        script.write_text(run_step(self.doc, index)["run"])
        bash = shutil.which("bash")
        self.assertIsNotNone(bash, "bash")
        run = subprocess.run(
            [str(bash), "-e", str(script)],
            env={"PATH": str(tools), "HEAD_SHA": HEAD_FIXTURE},
            capture_output=True,
            text=True,
            cwd=root,
            check=False,
        )
        return run, recorded

    def test_a_git_that_prints_a_sha_and_exits_nonzero_ends_the_step_before_the_verifier(self) -> None:
        for index, name in ((1, VERIFIER), (2, ROUNDS_CHECK)):
            with self.subTest(name):
                run, recorded = self.run_step(index, 77)
                self.assertNotEqual(0, run.returncode, f"the step passed with its base sha's status unread: {run}")
                self.assertFalse(recorded.exists(), f"{name} ran on a base sha whose producer failed: {run}")

    def test_a_git_that_exits_zero_hands_the_verifier_the_base_and_head_shas(self) -> None:
        for index, name in ((1, VERIFIER), (2, ROUNDS_CHECK)):
            with self.subTest(name):
                run, recorded = self.run_step(index, 0)
                self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
                arguments = recorded.read_text().split("\n")
                self.assertIn(name, arguments)
                self.assertEqual(
                    [BASE_FIXTURE, HEAD_FIXTURE],
                    [arguments[arguments.index(flag) + 1] for flag in ("--base", "--head")],
                )


if __name__ == "__main__":
    unittest.main()
