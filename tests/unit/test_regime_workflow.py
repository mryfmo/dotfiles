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
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
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
UNSAFE_OPTION = "allow-unsafe-pr-checkout"
READ_ONLY = {"contents": "read"}
POSITION = {"Offset", "Line", "Col"}

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


class Row(NamedTuple):
    """One run step's script: the regime.yml text a message points at, and the shape the step must have."""

    protects: str
    script: Script


# The table: the run steps of the workflow, in order, each pinned to the last part. The first fetches the pull
# request's own `/head` ref (not `/merge`, which GitHub builds from the head and the base) into the data ref, from
# origin, with no option but --no-tags, and checks the ref against the event's head sha. The second runs the base's
# verifier on the base's HEAD and that sha. No statement moves HEAD or the work tree, and nothing else runs.
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
            call(
                *("uv", "run", "--no-config", "--no-project", "python", "-I", VERIFIER),
                *("--base", dq(sub(rev_parse("HEAD"))), "--head", dq(var("HEAD_SHA"))),
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
)


def load(path: Path) -> dict:
    """The workflow parsed by PyYAML under uv (as test_regime_ci.py reads it): the test interpreter has no YAML parser."""
    read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
    uv = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
    result = subprocess.run([*uv, "-c", read, str(path)], capture_output=True, text=True, check=True)
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

    def statement(self, node: dict) -> Statement:
        self.comments(node, "Comments")
        self.fields(node, "statement", "Cmd", "Comments")  # Negated, Background, Coprocess and Redirs are refused
        # shfmt sets Semicolon for `;` (and for `&`, refused above as Background) and leaves it out at a newline. A `;`
        # between two pinned statements is another text than the table's: refused, not skipped as a position.
        if node.get("Semicolon"):
            self.refuse(node, "a semicolon")
        command = node.get("Cmd")
        if not isinstance(command, dict) or command.get("Type") != "CallExpr":
            kind = command.get("Type", "untyped") if isinstance(command, dict) else "empty"
            self.refuse(node, f"a {kind} statement")
        self.fields(command, "call", "Args")  # an assignment before the command word is refused
        words = command.get("Args") or []
        if not words:
            self.refuse(command, "a call with no word")
        return tuple(self.word(word) for word in words)

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


def render(statement: Statement) -> str:
    """A shape written back as shell text, for a message: the form the table holds, not the text the file had."""
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


def check_trigger(doc: dict) -> None:
    # PyYAML reads the key `on` as the boolean true, which JSON spells "true".
    on = mapping(doc.get("true", doc.get("on")), "pull_request_target:")
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


def differences(found: dict, held: dict) -> str:
    """The keys the step and the table disagree on, each named with what was found and what the table holds."""
    lines = []
    for key in sorted(set(found) | set(held)):
        if key not in found or key not in held or found[key] != held[key]:
            got = repr(found[key]) if key in found else "no such key"
            kept = repr(held[key]) if key in held else "no such key"
            lines.append(f"{key}: found {got}, the table holds {kept}")
    return "; ".join(lines)


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
            detail = f"the {key}: of the step {name!r} is not the table's: {differences(given, held)}"
            require(given == held, row.protects, detail)


def check_cancel_in_progress(doc: dict) -> None:
    group = mapping(doc.get("concurrency"), "cancel-in-progress: true")
    require(group.get("cancel-in-progress") is True, "cancel-in-progress: true", f"concurrency is {group!r}")


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
    return doc.get("true", doc.get("on"))


def set_in(getter: Callable[[dict], dict], key: str, value: object) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        getter(doc)[key] = value

    return mutate


def delete_in(getter: Callable[[dict], dict], key: str) -> Callable[[dict], None]:
    def mutate(doc: dict) -> None:
        del getter(doc)[key]

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
        "the head sha inlined into run": Mutation(replace_run(verify_step, "${HEAD_SHA}", HEAD_EXPRESSION), EXPRESSION),
        "the body inlined into run": Mutation(append_run(verify_step, f' --body "{BODY_CARRIER}"'), EXPRESSION),
        "another shell": Mutation(set_in(verify_step, "shell", "python"), "shell"),
        # a shell or directory every run step inherits: the workflow's or the job's defaults: mapping
        "a default shell for the workflow": Mutation(set_in(lambda d: d, "defaults", INHERITED_SHELL), "bash {0}"),
        "a default shell for the job": Mutation(set_in(regime_job, "defaults", INHERITED_SHELL), "bash {0}"),
        "a default directory for the job": Mutation(
            set_in(regime_job, "defaults", {"run": {"working-directory": "/other"}}), "working-directory"
        ),
        "a third run step": Mutation(add_step({"run": f"git checkout {HEAD_REF}\n"}), "3 run steps"),
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
        "a fifth step": Mutation(add_step({"uses": "actions/setup-node@v4"}), "5 steps"),
    },
)
CANCEL_IN_PROGRESS = Invariant(
    check_cancel_in_progress,
    {
        "cancel-in-progress: false": Mutation(
            set_in(lambda d: d["concurrency"], "cancel-in-progress", False), "'cancel-in-progress': False"
        ),
        "no concurrency group": Mutation(delete_in(lambda d: d, "concurrency"), "found None"),
    },
)


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
                self.assertFalse(self.doc == broken, f"regime.yml already carries this edit: {label}")
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


if __name__ == "__main__":
    unittest.main()
