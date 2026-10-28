"""The Azure apt mirror is dropped before every CI apt use, every apt call a workflow runs ends inside its step, and
the Bats bounds name a stall before the step stops (regime-cutover U102, U109).

actions/runner-images#14823: a slow azure.archive.ubuntu.com node keeps sending data, so apt's 15 s timeout never
fires and apt never moves to the next mirror. scripts/ci/drop-azure-apt-mirror.py removes that entry; every job that
runs apt on a Ubuntu runner calls it first. After the drop every call goes to archive.ubuntu.com, which can print
nothing for 15 minutes during `apt-get update` (runner-images#15040), so each call runs under GNU timeout with apt's
own silence timeout and retries set, in one exact form, and the steps that hold them carry their own timeout-minutes.
The measured budgets below come from passing `test` jobs of October 2026.
"""

from __future__ import annotations

import math
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_workflow_orchestration_skip import jobs

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
SCRIPT = ROOT / "scripts/ci/drop-azure-apt-mirror.py"
WRAPPER = ROOT / "scripts/ci/run-bats.py"
# The system python3, as the workflows run it; a host without one (none of CI's) runs the test interpreter instead.
SYSTEM_PYTHON = "/usr/bin/python3" if Path("/usr/bin/python3").exists() else sys.executable
CALL = "/usr/bin/python3 -I -S scripts/ci/drop-azure-apt-mirror.py"
# A step uses apt on the runner when it runs apt-get or apt, setup.sh (its Ubuntu installers), or the install tests
# (scripts/run_unit_test.sh and run_bats, whose real-install cases run apt-get). `make apply-check` (apply-check.yml)
# runs apt only inside its Docker build, against the image's own sources, never the runner's mirror list.
APT_USE = re.compile(
    r"\bapt-get\b|\bapt\s+(?:install|update|upgrade)\b|\bbash\s+\S*setup\.sh\b|\./setup\.sh\b|run_unit_test\.sh|\brun_bats\b"
)
# The jobs that run apt on a Ubuntu runner today; a scan that found fewer would have lost one.
APT_JOBS = {
    ("test.yaml", "test"),
    ("remote.yaml", "public-bootstrap"),
    ("private-bootstrap.yaml", "private-bootstrap"),
    ("ubuntu.yaml", "build"),
}
# Measured, in seconds (passing Ubuntu client jobs, October 2026):
# the time a `Run unit test` step spends outside its slowest test: 88-135 s typically, 284 s at most (run
# 40314461046, where ghostty took 201 s on a slow mirror);
OTHER_TESTS_BUDGET = 300
# the time a `test` job spends before `Run unit test`: at most 409 s (run 40251900588); and after it: at most 10 s.
PRE_STEP_BUDGET = 480
POST_STEP_BUDGET = 60
# The files suite under ubuntu.yaml's and macos.yaml's `Test file existence` (under 1 s in test.yaml), plus the
# brew install of bats-core there.
FILES_STEP_BUDGET = 300
MIRRORS = (
    "http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\n"
    "https://archive.ubuntu.com/ubuntu/\tpriority:2\n"
    "https://security.ubuntu.com/ubuntu/\tpriority:3\n"
)
# U109: every apt call a workflow runs carries its own bound, in one exact form. `timeout` ends a call that keeps
# printing nothing at N seconds and kills it KILL_AFTER seconds later; apt's own options give up a connection or read
# silent for 15 s and move to the next mirror, three times. N is measured per step (the comment next to each call in
# the workflow) with twice the measured time and at least 120 s of margin, so never under MIN_APT_BOUND.
APT_CALL = re.compile(r"\bapt-get\b|\bapt\s+(?:install|update|upgrade|full-upgrade|dist-upgrade)\b")
APT_BOUND = re.compile(
    r"timeout --kill-after=10 ([0-9]+) sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 "
    r"(?:update|install)(?=\s|$)"
)
KILL_AFTER = 10
MIN_APT_BOUND = 120
# A shell word left on the line once the form is removed reopens the call when it starts with one of these, whether
# the value is attached (`-cfoo.conf`), separate, after `=` or quoted (apt reads them all) ...
APT_REOPEN_PREFIXES = {
    "-o": "an option",
    "-c": "a configuration file",
    "--option": "an option",
    "--config-file": "a configuration file",
}
# ... or holds one of these anywhere, in any case (`APT_CONFIG=` at the front, a second `timeout` after `;`).
APT_REOPEN_PARTS = {
    "acquire::": "an Acquire key",
    "apt_config": "the APT_CONFIG variable",
    "timeout": "a second timeout",
}
# (workflow file name, the whole stripped line, exactly) -> why the line may name apt without the form. Empty on this
# head: the three workflows that bootstrap through setup.sh run apt only inside the installers, whose downloads U99
# bounded, and no workflow comment names apt-get. A row must still match a line (test_no_apt_exemption_is_stale).
APT_EXEMPT: dict[tuple[str, str], str] = {}
# Measured, in seconds, outside the apt calls (passing `test` jobs, every matrix row, runs 40314863147 to
# 40610790312): "Install tools" at most 73 s (ubuntu-24.04 server, run 40338292845), 14 to 46 s elsewhere; "Run
# Python unit tests" at most 664 s (macos-15 client, run 40610790312), 189 to 388 s on the Ubuntu rows; "Setup for
# Codecov" under 1 s. Twice the maximum each, so a step bound ends a stall, never a slow passing run.
STEP_REST_BUDGET = {"Install tools": 150, "Run Python unit tests": 1330, "Setup for Codecov": 60}
# U109 round 3 (audit of 0a9fa727): the step check attaches names and timeout-minutes through the hand-written
# reader `jobs()` (CI's interpreter has no YAML parser), which returns a `run: |` body and a one-line plain scalar
# and silently returned no body for `run: |-` and `run: >`. A failed read is never an absence (standing order 21):
# every `run:` key the raw text holds is counted, and the reader must have returned exactly it, so a step in any
# other form (`|-`, `|+`, `>`, `|2`, a quoted scalar, a plain scalar that continues) is refused by file and line.
# The first character of a plain scalar: no block header, quote, flow bracket or other YAML indicator.
PLAIN_SCALAR = re.compile(r"""[^|>"'{}\[\],#&*!%@`\s]""")
READ_FORMS = "the reader returns `run: |` and a one-line plain scalar, nothing else"
# Round 4 (audit of 81fa7256): that census assumed the reader's own indentation (a dash at six spaces, keys at
# eight), so a step written with its dash at five and keys at seven, YAML the runner executes, was skipped by the
# census as by the reader, and an apt step there passed without timeout-minutes. The census now derives the shape
# from the text, places every line inside `jobs:` or refuses it by line, and names by its dash line every step the
# reader's rule does not reach.
READER_STEP_SHAPE = (6, 8)
READER_SHAPE = "the reader reads a step's dash at six spaces and its keys at eight, nothing else"
# Round 5 (audit of f4486ead): the round 4 census compared the literal `steps:`, so `steps: # comment` was an opaque
# value and a list at five and seven under it was skipped by both readers. The census now lexes every line inside
# `jobs:` (indent, dash, plain key, value, trailing comment) and places it by a closed grammar: at each level the
# keys the workflow schema allows and the value forms both readers read. Every other construct is refused by line,
# so no line the census cannot name becomes a silent value.
KEY_LINE = re.compile(r"([a-z0-9_-]+):(?:[ \t]+(.*))?")  # the reader's plain form: the colon right after the key
COMMENT = re.compile(r"(?:^|[ \t])#")  # a comment starts at a `#` that opens the value or follows a blank
KEY_FORM = "a plain `key:` line (lower-case letters, digits, `_` and `-`, the colon right after, then a blank or the line's end)"
JOBS_LINE = "the readers find the bare `jobs:` line, with nothing else on it"
# The keys the workflow schema allows on a job and on a step (docs.github.com, workflow syntax); any other key is
# refused, as the runner refuses it.
JOB_KEYS = frozenset(
    "name permissions needs if runs-on environment concurrency outputs env defaults steps timeout-minutes strategy "
    "continue-on-error container services uses with secrets".split()
)
STEP_KEYS = frozenset("id if name uses run working-directory shell with env continue-on-error timeout-minutes".split())
# A value's first character names its form. Both readers read a value that is empty (a nested block, a list or
# nothing follows), a plain scalar, a quoted scalar or a flow collection, since none of these moves a step or a `run:`
# body; `steps:` takes the empty form alone, and a `run:` value is compared with the reader's (READ_FORMS). The other
# forms are refused: an anchor or alias carries content from elsewhere in the file, a tag or a block header changes
# how the value is read, and the rest YAML reserves.
VALUE_INDICATORS = {
    "&": "an anchor",
    "*": "an alias",
    "!": "a tag",
    "|": "a block header",
    ">": "a block header",
    "%": "a reserved indicator",
    "@": "a reserved indicator",
    "`": "a reserved indicator",
    ",": "a flow indicator",
    "]": "a flow indicator",
    "}": "a flow indicator",
}
READ_VALUE_FORMS = ("empty", "a plain scalar", "a quoted scalar", "a flow collection")
READ_VALUES = "the readers read a value that is empty, a plain scalar, a quoted scalar or a flow collection"
STEPS_VALUE = "the list follows on its own lines"
RUN_COMMENT = "a comment after a one-line run:, which the reader returns inside the command"


def step_text(step: dict) -> str:
    """The step's commands, comment lines left out (a decision step names setup.sh in its comments and patterns)."""
    lines = f"{step.get('run', '')}\n{step.get('script', '')}".splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#"))


def job_text(path: Path, name: str) -> str:
    text = path.read_text().split("\njobs:\n", 1)[1]
    body = text.split(f"\n  {name}:\n", 1)[1] if not text.startswith(f"  {name}:\n") else text
    return re.split(r"\n  [a-z][\w-]*:\n", body, maxsplit=1)[0]


def default_bound() -> int:
    return int(re.search(r"^DEFAULT_BOUND = ([0-9]+)$", WRAPPER.read_text(), re.MULTILINE).group(1))


def reopening_word(rest: str) -> str | None:
    """Why the first shell word of `rest` (a line with its bound forms removed) that reopens the call does so, or None.

    Audit of 9058072b: a token regex saw `-o` and `-c` only as separate words, so `-cfoo.conf` and
    `-oDebug::NoLocking=true` passed. Every word is read whole; a quote that never closes refuses the line, since
    its words cannot be told apart."""
    try:
        words = shlex.split(rest)
    except ValueError as error:
        return f"cannot be split into shell words: {error}"
    for word in words:
        lower = word.lower()
        for prefix, why in APT_REOPEN_PREFIXES.items():
            if lower.startswith(prefix):
                return f"{word!r} starts with {prefix!r}: {why}"
        for part, why in APT_REOPEN_PARTS.items():
            if part in lower:
                return f"{word!r} holds {part!r}: {why}"
    return None


def apt_violations(relative: str, text: str, exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The lines of one workflow that name apt outside the bound form, as `file:line: text (why)`."""
    exempt = APT_EXEMPT if exempt is None else exempt
    bad = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        calls = len(APT_CALL.findall(line))
        if not calls or (relative, line) in exempt:
            continue
        where = f"{relative}:{number}: {line}"
        bounds = APT_BOUND.findall(line)
        if len(bounds) != calls:
            bad.append(f"{where} ({calls} apt call(s), {len(bounds)} in the bound form)")
            continue
        low = [n for n in bounds if int(n) < MIN_APT_BOUND]
        if low:
            bad.append(f"{where} (a bound under {MIN_APT_BOUND} s: {low})")
        if line.endswith("\\"):
            bad.append(f"{where} (continues onto the next line, where an option could reopen the call)")
        reopens = reopening_word(APT_BOUND.sub(" ", line.removesuffix("\\")))
        if reopens:
            bad.append(f"{where} (outside the form, {reopens})")
    return bad


def apt_stale(files: dict[str, str], exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The exemptions whose workflow no longer holds their whole line, exactly."""
    exempt = APT_EXEMPT if exempt is None else exempt
    lines = {name: {line.strip() for line in text.splitlines()} for name, text in files.items()}
    return [f"{name}: {line}" for name, line in exempt if line not in lines.get(name, set())]


class Census(NamedTuple):
    """Every job's steps from the raw text, `{job: [{"line", "dash", "keys", "runs": [{"line", "header", "body"}]}]}`
    ("dash" and "keys" the step's indents), and the lines inside `jobs:` the census could not place, `(line, why)`."""

    steps: dict[str, list[dict]]
    refused: list[tuple[int, str]]


class Lexed(NamedTuple):
    """One line taken apart: its indent in spaces, whether it opens a list entry (`- `), the plain key it holds (None
    when it holds none), that key's value with its trailing comment removed, the comment, the key's header as written
    (a `run:` header is compared whole), the stripped text, and the fault that stops the lexing (a tab in the
    indentation)."""

    indent: int
    dash: bool
    key: str | None
    value: str
    comment: str
    header: str
    text: str
    fault: str | None


def lex(line: str) -> Lexed:
    text = line.strip()
    indent = len(line) - len(line.lstrip(" "))
    fault = "a tab in the indentation" if text and "\t" in line[: len(line) - len(line.lstrip())] else None
    dash = text.startswith("- ")
    entry = text[2:].lstrip(" ") if dash else text
    match = KEY_LINE.fullmatch(entry)
    header = (match.group(2) or "").strip() if match else ""
    comment = COMMENT.search(header)
    value, note = (header[: comment.start()].rstrip(), header[comment.start() :].strip()) if comment else (header, "")
    return Lexed(indent, dash, match.group(1) if match else None, value, note, header, text, fault)


def value_form(value: str) -> str:
    """The form a value's first character gives it: one of READ_VALUE_FORMS, or the name of a refused indicator."""
    if not value:
        return "empty"
    first = value[0]
    if first in "\"'":
        return "a quoted scalar"
    if first in "[{":
        return "a flow collection"
    if first in "-?:" and (len(value) == 1 or value[1] in " \t"):
        return {"-": "a sequence entry", "?": "a complex key", ":": "a mapping value"}[first]
    return VALUE_INDICATORS.get(first, "a plain scalar")


def key_problem(lexed: Lexed, allowed: frozenset[str], seen: set[str], level: str, entry: bool = False) -> str | None:
    """Why a job key or step key line (`entry`: the key on a step's dash line) is outside the grammar, or None."""
    if lexed.key is None or (lexed.dash and not entry):
        return f"not {KEY_FORM}"
    if lexed.key not in allowed:
        return f"{lexed.key}: is not a {level} key; the {level} keys are {', '.join(sorted(allowed))}"
    if lexed.key in seen:
        return f"a second {lexed.key}: key in one {level}"
    seen.add(lexed.key)
    form = value_form(lexed.value)
    if lexed.key == "run":
        return RUN_COMMENT if lexed.comment and form == "a plain scalar" else None
    if lexed.key == "steps":
        return None if form == "empty" else f"steps: holds {form}; {STEPS_VALUE}"
    return None if form in READ_VALUE_FORMS else f"{lexed.key}: holds {form}; {READ_VALUES}"


def census(text: str) -> Census:
    """Every step of every job, from the raw text alone, at whatever indentation the file uses.

    The shape is derived, never assumed: the first key after `jobs:` sets the jobs' indent, the first key under a
    job its keys', the first dash under `steps:` the dashes', and each dash line its own keys' (the column after
    `- `). Any other line inside `jobs:` is the value of the key above it when it is indented past that key (a
    `run: |` body, a nested `with:` mapping; a `run:` there is not a key) and is refused by line otherwise. Every
    line the shape places is lexed and held to the grammar (KEY_LINE, JOB_KEYS, STEP_KEYS, the value forms) or
    refused by line with its construct named. A `run:` key's body is every following line indented past the step's
    keys, blank lines included, up to the first that is not; so the body is collected in any scalar form, whatever
    the reader makes of the form."""
    steps_by_job: dict[str, list[dict]] = {}
    refused: list[tuple[int, str]] = []
    steps: list[dict] = []
    job_keys: set[str] = set()
    step_keys: set[str] = set()
    jobs_at = keys_at = dash_at = value_at = step = body = body_at = None
    in_steps = False
    state = "before"
    for number, line in enumerate(text.split("\n"), 1):
        lexed = lex(line)
        if state == "before":
            if lexed.indent == 0 and lexed.key == "jobs":
                state = "jobs"
                if line != "jobs:":
                    refused.append((number, f"{lexed.text} ({JOBS_LINE})"))
            continue
        if state == "after":
            if lexed.indent == 0 and lexed.key == "jobs":
                refused.append((number, f"{lexed.text} (a second jobs: key)"))
            continue
        if "\r" in line:
            refused.append((number, f"{lexed.text} (a carriage return; the workflows are LF-only)"))
        if value_at is not None and (not lexed.text or lexed.indent > value_at):
            if body is not None:
                body.append(line)
                if lexed.text and body_at is None:
                    body_at = lexed.indent
                elif lexed.text and lexed.indent < body_at:
                    refused.append(
                        (
                            number,
                            f"{lexed.text} (indented {lexed.indent} inside a block whose first line is at {body_at})",
                        )
                    )
            continue
        if body is not None:
            body = body_at = value_at = None  # a less indented line, a comment too, ends a block body (YAML 8.1.1)
        if not lexed.text or lexed.text.startswith("#"):
            continue
        if lexed.fault:
            refused.append((number, f"{lexed.text} ({lexed.fault})"))
            continue
        if lexed.indent == 0:
            state = "after"
            if lexed.key is None or lexed.dash:
                refused.append(
                    (number, f"{lexed.text} (not {KEY_FORM}; both readers stop at the first unindented line)")
                )
            elif lexed.key == "jobs":
                refused.append((number, f"{lexed.text} (a second jobs: key)"))
            continue
        if jobs_at is None:
            jobs_at = lexed.indent
        dash = in_steps and lexed.dash and dash_at in (None, lexed.indent) and lexed.indent >= keys_at
        problem = None
        step_key = False
        if lexed.indent == jobs_at:
            name = lexed.key or lexed.text
            if lexed.key is None or lexed.dash:
                problem = f"not {KEY_FORM}"
            elif lexed.value:
                problem = "a job line with a value; the job's keys follow on their own lines"
            elif name in steps_by_job:
                problem = f"a second job named {name}"
            steps_by_job[name] = steps = []
            job_keys = set()
            keys_at = dash_at = step = value_at = None
            in_steps = False
        elif dash:
            dash_at = lexed.indent
            keys = lexed.indent + len(lexed.text) - len(lexed.text[2:].lstrip(" "))
            step = {"line": number, "dash": lexed.indent, "keys": keys, "runs": []}
            steps.append(step)
            step_keys = set()
            problem = key_problem(lexed, STEP_KEYS, step_keys, "step", entry=True)
            step_key = True
            value_at = keys
        elif lexed.indent > jobs_at and (keys_at is None or lexed.indent == keys_at):
            keys_at = lexed.indent
            problem = key_problem(lexed, JOB_KEYS, job_keys, "job")
            in_steps = lexed.key == "steps" and not lexed.dash
            dash_at = step = None
            value_at = None if in_steps else lexed.indent
        elif in_steps and step is not None and lexed.indent == step["keys"]:
            problem = key_problem(lexed, STEP_KEYS, step_keys, "step")
            step_key = True
            value_at = lexed.indent
        else:
            levels = [f"a job at {jobs_at}"]
            if keys_at is not None:
                levels.append(f"a job key at {keys_at}")
            if in_steps and dash_at is None:
                levels.append(f"a step's dash at or past {keys_at}")
            elif dash_at is not None:
                levels.append(f"a step's dash at {dash_at}")
            if step is not None:
                levels.append(f"a step key at {step['keys']}")
            if value_at is not None:
                levels.append(f"a value past {value_at}")
            problem = f"indented {lexed.indent}, where the shape has {', '.join(levels)}"
        if problem:
            refused.append((number, f"{lexed.text} ({problem})"))
        if step_key and lexed.key == "run":
            body, body_at = [], None
            step["runs"].append({"line": number, "header": lexed.header, "body": body})
    if state == "before":
        refused.append((1, f"no `jobs:` line in the file ({JOBS_LINE})"))
    for steps in steps_by_job.values():
        for run in (run for step in steps for run in step["runs"]):
            while run["body"] and not run["body"][-1].strip():
                run["body"].pop()  # the blank lines after a body belong to no key
    return Census(steps_by_job, refused)


def text_steps(text: str) -> dict[str, list[dict]]:
    """The census's steps alone, for a caller that has already taken its refusals (census_problems names them)."""
    return census(text).steps


def reader_reaches(step: dict) -> bool:
    """Whether the reader's fixed indentation rule returns this text step at all."""
    return (step["dash"], step["keys"]) == READER_STEP_SHAPE


def run_text(step: dict) -> str:
    """A text step's commands as written (the `run:` key's value and the lines under it), comment lines left out."""
    lines = [line for run in step["runs"] for line in (run["header"], *run["body"])]
    return "\n".join(line for line in lines if line.strip() and not line.lstrip().startswith("#"))


def census_problems(name: str, text: str, parsed: dict[str, list[dict]]) -> list[str]:
    """Every line of one workflow the census could not place and every `run:` key in its raw text that the reader
    did not return whole, by `file:line`.

    The text is the census and the reader must agree with it job by job and step by step: the same steps, and for
    each `run:` the same body (`run: |`) or the same one-line value (a plain scalar). A step at an indentation the
    reader's rule does not reach is refused on its dash line, since the reader returns nothing for it; any other
    form is refused, since the reader returns nothing for it or returns it undecoded."""
    found = census(text)
    problems = [f"{name}:{number}: {why}" for number, why in found.refused]
    by_job = found.steps
    if list(by_job) != list(parsed):
        problems.append(f"{name}: the text holds jobs {list(by_job)}, the reader returned {list(parsed)}")
    for job, steps in by_job.items():
        read = parsed.get(job)
        if read is None:
            continue  # named above
        readable = []
        for step in steps:
            if reader_reaches(step):
                readable.append(step)
            else:
                problems.append(
                    f"{name}:{step['line']}: a step with its dash at {step['dash']} spaces and its keys at "
                    f"{step['keys']} ({READER_SHAPE})"
                )
        if len(read) != len(readable):
            problems.append(f"{name}: {job}: {len(readable)} steps in the text, {len(read)} from the reader")
            continue
        for step, got in zip(readable, read):
            if not step["runs"]:
                if "run" in got:
                    problems.append(f"{name}:{step['line']}: the reader returned a run: the text does not hold")
                continue
            if len(step["runs"]) > 1:
                continue  # the census refused the second run: key by line
            (run,) = step["runs"]
            where = f"{name}:{run['line']}: run: {run['header']}".rstrip()
            lines = [line.strip() for line in run["body"] if line.strip()]
            if run["header"] == "|":
                script = [line.strip() for line in got.get("script", "").splitlines() if line.strip()]
                if got.get("run") != "|" or script != lines:
                    problems.append(
                        f"{where} (the reader's body is not the text's: {len(script)} line(s) read, {len(lines)} written)"
                    )
            elif not PLAIN_SCALAR.match(run["header"]):
                problems.append(f"{where} ({READ_FORMS})")
            elif lines:
                problems.append(f"{where} (continues onto {len(lines)} more line(s); {READ_FORMS})")
            elif got.get("run") != run["header"]:
                problems.append(f"{where} (the reader returned {got.get('run')!r})")
    return problems


def bounded_steps() -> list[dict]:
    """Three steps in the bound form with the timeout-minutes the formula gives for STEP_REST_BUDGET."""
    form = "timeout --kill-after=10 {} sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 {}"
    return [
        {
            "name": "Install tools",
            "timeout-minutes": "10",
            "run": f"{form.format(180, 'update')}\n{form.format(180, 'install -y bats curl')}",
        },
        {
            "name": "Run Python unit tests",
            "timeout-minutes": "29",
            "run": f"{form.format(150, 'update')}\n{form.format(150, 'install -y jq zsh')}",
        },
        {"name": "Setup for Codecov", "timeout-minutes": "5", "run": form.format(150, "install -y jq curl")},
    ]


def render(steps_by_job: dict[str, list[dict]], shape: tuple[int, int, int, int] = (2, 4, 6, 8)) -> str:
    """Workflow text for in-memory steps: every `run` as a `run: |` block, the other keys plain, in the step's order,
    at `shape`: the indents of a job, its keys, a step's dash and its keys (the reader's by default), bodies two past."""
    job_at, key_at, dash_at, step_at = shape
    lines = ["name: x", "on: push", "jobs:"]
    for job, steps in steps_by_job.items():
        lines += [f"{' ' * job_at}{job}:", f"{' ' * key_at}runs-on: ubuntu-24.04", f"{' ' * key_at}steps:"]
        for step in steps:
            for position, (key, value) in enumerate(step.items()):
                lead = " " * dash_at + "-" + " " * (step_at - dash_at - 1) if position == 0 else " " * step_at
                if key == "run":
                    lines.append(f"{lead}run: |")
                    lines += [f"{' ' * (step_at + 2)}{line}" for line in value.splitlines()]
                else:
                    lines.append(f"{lead}{key}: {value}")
    return "\n".join(lines) + "\n"


def dash_lines(text: str, dash_at: int = 6) -> list[int]:
    """The line of each step's dash at `dash_at` spaces, in step order."""
    return [number for number, line in enumerate(text.splitlines(), 1) if line.startswith(" " * dash_at + "- ")]


def parsed_steps(path: Path) -> dict[str, list[dict]]:
    return {job: body["steps"] for job, body in jobs(path).items()}


def apt_step_problems(texts: dict[str, str], parsed: dict[str, dict[str, list[dict]]]) -> list[str]:
    """What would let a stalled apt call outlive its step's name, for `{workflow: text}` and the reader's steps.

    The steps that run apt are found in the raw text (the `run:` key and the lines under it, comment lines left
    out), once the census has shown the reader returned every `run:`; the reader's structure only attaches the name
    and timeout-minutes, its steps matched in order to the text steps its rule reaches (the census has named the
    others). Steps are keyed by (workflow, job, index), the name carried for the message, so no step replaces
    another; a name used twice in one job is refused on its own, since STEP_REST_BUDGET refers to steps by name.
    Then every apt step has a budget row and the timeout-minutes the formula gives, and every budget row has its
    step."""
    problems, found = [], {}
    for workflow, text in texts.items():
        by_job = parsed.get(workflow, {})
        problems.extend(census_problems(workflow, text, by_job))
        for job, steps in text_steps(text).items():
            read = iter(by_job.get(job, []))
            seen: dict[str, int] = {}
            for index, step in enumerate(steps):
                got = next(read, {}) if reader_reaches(step) else {}
                name = got.get("name")
                label = name or f"step {index}"
                where = f"{workflow}:{step['line']}: {job}: step {index} {label!r}"
                if name is not None and name in seen:
                    problems.append(f"{where} repeats the name of step {seen[name]}")
                elif name is not None:
                    seen[name] = index
                commands = run_text(step)
                if APT_CALL.search(commands):
                    bounds = [int(n) for n in APT_BOUND.findall(commands)]
                    found[where] = (name, sum(n + KILL_AFTER for n in bounds), got)
    names = {name for name, _, _ in found.values()}
    problems.extend(f"budget row {name!r} has no step that runs apt" for name in STEP_REST_BUDGET if name not in names)
    for where, (name, apt_seconds, step) in found.items():
        if name not in STEP_REST_BUDGET:
            problems.append(f"{where} runs apt with no STEP_REST_BUDGET row")
        elif "timeout-minutes" not in step:
            problems.append(f"{where} has no timeout-minutes")
        else:
            expected = math.ceil((apt_seconds + STEP_REST_BUDGET[name]) / 60) + 1
            if int(step["timeout-minutes"]) != expected:
                problems.append(f"{where} has timeout-minutes {step['timeout-minutes']}, the formula gives {expected}")
    return problems


def workflow_problems(paths: list[Path]) -> list[str]:
    """The census and step problems of whole workflow files, as the tests see the real ones."""
    return apt_step_problems({p.name: p.read_text() for p in paths}, {p.name: parsed_steps(p) for p in paths})


def workflow_texts() -> dict[str, str]:
    return {path.name: path.read_text() for path in sorted(WORKFLOWS.glob("*.y*ml"))}


class MirrorScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="apt-mirror-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.temp)], check=False))
        self.list = self.temp / "apt-mirrors.txt"
        (self.temp / "bin").mkdir()
        # A sudo that refuses, so no case can reach the host's own list.
        self.fake("sudo", "echo 'sudo refused by the test' >&2\nexit 1")

    def fake(self, name: str, body: str) -> None:
        path = self.temp / "bin" / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def read_only(self) -> None:
        """Make the list root's to this user, so the script writes it through `sudo -n tee`."""
        self.list.chmod(0o444)
        self.addCleanup(self.list.chmod, 0o644)
        if os.access(self.list, os.W_OK):
            self.skipTest("running as a user who can write a read-only file")

    def through_sudo(self, tee_body: str) -> None:
        """A sudo that runs its command (after checking -n) and a fake tee."""
        self.read_only()
        self.fake("sudo", '[ "$1" = -n ] || exit 64\nshift\nexec "$@"')
        self.fake("tee", tee_body)

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [SYSTEM_PYTHON, "-I", "-S", str(SCRIPT), *args],
            env={"PATH": f"{self.temp / 'bin'}:/usr/bin:/bin", "HOME": str(self.temp)},
            capture_output=True, text=True, timeout=30, check=False,
        )  # fmt: skip

    def assert_refused(self, result: subprocess.CompletedProcess[str], reason: str) -> None:
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(result.stderr.splitlines()), result.stderr)
        self.assertIn(reason, result.stderr)

    def test_the_azure_entry_is_removed_and_the_others_kept(self) -> None:
        self.list.write_text(MIRRORS)
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(MIRRORS.split("\n", 1)[1], self.list.read_text())
        self.assertIn("before:", result.stdout)
        self.assertIn("after:", result.stdout)

    def test_a_list_without_the_entry_or_no_list_is_left_alone(self) -> None:
        kept = MIRRORS.split("\n", 1)[1]
        self.list.write_text(kept)
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(kept, self.list.read_text())
        self.assertIn("nothing to change", result.stdout)
        absent = self.run_script(str(self.temp / "absent.txt"))
        self.assertEqual(0, absent.returncode, absent.stderr)
        self.assertIn("absent", absent.stdout)

    def test_a_list_that_would_be_left_empty_is_refused_unchanged(self) -> None:
        only = MIRRORS.split("\n", 1)[0] + "\n"
        self.list.write_text(only)
        self.assert_refused(self.run_script(str(self.list)), "no apt mirror would be left")
        self.assertEqual(only, self.list.read_text())

    def test_only_a_missing_list_is_absent(self) -> None:
        # Audit of db045676: os.path.lexists() read EACCES and ENAMETOOLONG as "absent". Only ENOENT is absent now.
        missing = self.run_script(str(self.temp / "no-such-dir" / "apt-mirrors.txt"))
        self.assertEqual(0, missing.returncode, missing.stderr)
        self.assertIn("is absent", missing.stdout)
        overlong = self.temp / ("x" * 300)
        self.assert_refused(self.run_script(str(overlong)), "File name too long")
        locked = self.temp / "locked"
        locked.mkdir()
        (locked / "apt-mirrors.txt").write_text(MIRRORS)
        locked.chmod(0o000)
        self.addCleanup(locked.chmod, 0o755)
        if os.access(locked / "apt-mirrors.txt", os.R_OK):
            self.skipTest("running as a user who can search a mode-000 directory")
        self.assert_refused(
            self.run_script(str(locked / "apt-mirrors.txt")), f"cannot read {locked}/apt-mirrors.txt: Permission denied"
        )

    def test_a_list_that_cannot_be_read_fails_named_and_is_not_written(self) -> None:
        # Audit of 9a885470: bash's read took a read error for the end of the file. A mode-000 file and a directory.
        self.fake("tee", f'echo tee ran >> "{self.temp}/tee.log"; cat > /dev/null')
        directory = self.temp / "list.d"
        directory.mkdir()
        self.assert_refused(self.run_script(str(directory)), f"cannot read {directory}: Is a directory")
        self.list.write_text(MIRRORS)
        self.list.chmod(0o000)
        self.addCleanup(self.list.chmod, 0o644)
        if not os.access(self.list, os.R_OK):
            self.assert_refused(self.run_script(str(self.list)), f"cannot read {self.list}: Permission denied")
        self.assertFalse((self.temp / "tee.log").exists())

    def test_a_failed_write_fails_named_and_leaves_the_list(self) -> None:
        self.list.write_text(MIRRORS)
        self.read_only()
        self.assert_refused(self.run_script(str(self.list)), "sudo -n tee exited 1: sudo refused by the test")
        self.assertEqual(MIRRORS, self.list.read_text())
        # sudo runs, and tee fails.
        self.through_sudo("cat > /dev/null; echo 'tee: disk full' >&2; exit 5")
        self.assert_refused(self.run_script(str(self.list)), "sudo -n tee exited 5: tee: disk full")
        self.assertEqual(MIRRORS, self.list.read_text())

    def test_a_write_through_sudo_is_read_back_and_kept(self) -> None:
        self.list.write_text(MIRRORS)
        self.through_sudo('chmod 644 "$1" && cat > "$1"')
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(MIRRORS.split("\n", 1)[1], self.list.read_text())

    def test_a_write_that_reads_back_differently_fails_named(self) -> None:
        # tee reports success but leaves other bytes (a truncated or interleaved write).
        self.list.write_text(MIRRORS)
        self.through_sudo('cat > /dev/null; chmod 644 "$1" && printf truncated > "$1"')
        self.assert_refused(self.run_script(str(self.list)), f"{self.list} read back differs from what was written")

    def test_the_only_external_command_is_the_checked_write(self) -> None:
        # Audits of 52035104 and 9a885470: no producer but the write decides anything, and it is checked and bounded.
        text = SCRIPT.read_text()
        self.assertEqual(1, text.count("subprocess.run("))
        self.assertIn('["sudo", "-n", "tee", path]', text)
        self.assertIn("check=True, timeout=WRITE_TIMEOUT", text)
        self.assertNotRegex(text, r"os\.system|os\.popen|shell=True|check=False")

    def test_the_default_list_is_the_runner_image_one(self) -> None:
        self.assertIn('DEFAULT = "/etc/apt/apt-mirrors.txt"', SCRIPT.read_text())
        self.assertIn("actions/runner-images#14823", SCRIPT.read_text())

    def test_the_drop_names_its_re_check(self) -> None:
        # The drop has an exit condition, not an expiry: #14823 was declared mirror-side and healthy on 2026-10-27.
        text = SCRIPT.read_text()
        self.assertIn("when actions/runner-images#14823 is closed", text)
        self.assertIn("three `test (ubuntu-24.04, client)` runs with the drop disabled", text)
        self.assertIn("within 20 percent", text)


class AptJobTest(unittest.TestCase):
    def test_every_job_that_runs_apt_on_ubuntu_drops_the_mirror_first(self) -> None:
        found, late = set(), []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for name, job in jobs(path).items():
                if "ubuntu" not in job["keys"].get("runs-on", "") + job_text(path, name):
                    continue
                steps = job["steps"]
                uses = [index for index, step in enumerate(steps) if APT_USE.search(step_text(step))]
                if not uses:
                    continue
                found.add((path.name, name))
                calls = [index for index, step in enumerate(steps) if step.get("run") == CALL]
                if not calls or calls[0] > uses[0]:
                    late.append(f"{path.name}: {name}: first apt use at step {uses[0]}, mirror step at {calls[:1]}")
        self.assertEqual([], late)
        self.assertEqual(APT_JOBS, found)

    def test_the_mirror_is_dropped_in_one_place(self) -> None:
        # One definition: no workflow edits the list itself.
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                self.assertNotIn("apt-mirrors.txt", path.read_text())
                self.assertNotIn("azure.archive", path.read_text().replace("azure\\.archive", ""))


class AptBoundRuleTest(unittest.TestCase):
    """Every apt call a workflow runs ends inside its step: the exact bound form on its own line, or an exemption row
    with a reason. Closed-world, as U99's download rule (decisions.tsv `treadmill-u99-scanner`): the text is matched,
    never parsed."""

    FORM = "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"

    def test_every_apt_call_in_a_workflow_carries_the_bound_or_is_exempted(self) -> None:
        bad = [hit for name, text in workflow_texts().items() for hit in apt_violations(name, text)]
        self.assertEqual([], bad)

    def test_no_apt_exemption_is_stale(self) -> None:
        texts = workflow_texts()
        self.assertEqual([], apt_stale(texts))
        # The table is the only way out, so a scan that saw fewer calls than test.yaml's two updates and three
        # installs would be a broken scan.
        bounded = sum(len(APT_BOUND.findall(line)) for text in texts.values() for line in text.splitlines())
        self.assertGreaterEqual(bounded, 5)

    def test_the_bypasses_fail(self) -> None:
        for snippet in (
            "sudo apt-get update",
            "sudo apt install -y jq",
            f"{self.FORM} update && sudo apt-get install -y jq",
            "timeout 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=0 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 0 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 60 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=0 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 180 sudo apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=15 update",
            f"{self.FORM} -o acquire::http::timeout=0 update",
            f"{self.FORM} install -y -o Acquire::Retries=0 jq",
            f"{self.FORM} install -y jq -c /tmp/apt.conf",
            f"{self.FORM} install -y jq --config-file=/tmp/apt.conf",
            f"APT_CONFIG=/tmp/apt.conf {self.FORM} update",
            f"{self.FORM} update \\",
            f"{self.FORM} update; timeout 5 true",
            f"{self.FORM} upgrade -y",
            "# sudo apt-get update",
            'echo "apt-get update"',
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual(1, len(apt_violations("x.yaml", snippet + "\n", {})), snippet)

    def test_the_bound_form_passes(self) -> None:
        for snippet in (
            f"{self.FORM} update",
            f"{self.FORM} install -y bats curl iproute2 parallel ruby",
            f"{self.FORM} update && {self.FORM} install -y jq zsh",
            "apt-mirrors.txt and drop-azure-apt-mirror.py are other words",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)

    def test_an_exemption_needs_its_exact_line(self) -> None:
        table = {("x.yaml", "# apt-get runs inside setup.sh"): "comment; names the tool without running it"}
        self.assertEqual([], apt_violations("x.yaml", "  # apt-get runs inside setup.sh\n", table))
        self.assertEqual(1, len(apt_violations("x.yaml", "# apt-get runs inside setup.sh now\n", table)))
        self.assertEqual([], apt_stale({"x.yaml": "  # apt-get runs inside setup.sh\n"}, table))
        self.assertEqual(
            ["x.yaml: # apt-get runs inside setup.sh"],
            apt_stale({"x.yaml": "# apt-get runs inside setup.sh now\n"}, table),
        )

    def test_a_reopening_word_fails_attached_separate_after_equals_or_quoted(self) -> None:
        # Audit of 9058072b: `-cfoo.conf` and `-oDebug::NoLocking=true` passed a regex that saw `-c` and `-o` only
        # as separate words. Each table entry is shown failing in every spelling apt reads, with its cause named.
        for prefix, why in APT_REOPEN_PREFIXES.items():
            value = "Debug::NoLocking=true" if prefix in ("-o", "--option") else "foo.conf"
            for tail in (
                f"{prefix}{value}",
                f"{prefix} {value}",
                f"{prefix}={value}",
                f'"{prefix}{value}"',
                f"'{prefix}' {value}",
                f"{prefix.upper()}{value}",
            ):
                with self.subTest(tail=tail):
                    bad = apt_violations("x.yaml", f"{self.FORM} install -y jq {tail}\n", {})
                    self.assertEqual(1, len(bad), bad)
                    self.assertIn(f"starts with {prefix!r}: {why}", bad[0])
        for part, why in APT_REOPEN_PARTS.items():
            for tail in (part, f"{part.upper()}=0", f"x{part}y", f'"{part} 5"', f"'{part}'"):
                with self.subTest(tail=tail):
                    bad = apt_violations("x.yaml", f"{self.FORM} install -y jq {tail}\n", {})
                    self.assertEqual(1, len(bad), bad)
                    self.assertIn(f"holds {part!r}: {why}", bad[0])
        with self.subTest(tail="an unclosed quote"):
            bad = apt_violations("x.yaml", f'{self.FORM} install -y "jq\n', {})
            self.assertEqual(1, len(bad), bad)
            self.assertIn("cannot be split into shell words: No closing quotation", bad[0])


class BoundOrderTest(unittest.TestCase):
    """A stalled test is named, and its diagnosis printed, before any step or job timeout stops it."""

    def step(self, workflow: str, job: str, name: str) -> dict:
        (step,) = [s for s in jobs(WORKFLOWS / workflow)[job]["steps"] if s.get("name") == name]
        return step

    def test_a_slow_test_then_a_stalled_one_are_both_inside_the_unit_test_step(self) -> None:
        # PR #559: ghostty took 832 s (under the old 1200 s bound) on a slow mirror, then misc stalled; the step's
        # 35 minutes ran out 25 s before misc's bound, so nothing named it. The step holds one earlier test as slow
        # as the bound allows, the stalled test's bound and the other tests' measured time.
        step_seconds = int(self.step("test.yaml", "test", "Run unit test")["timeout-minutes"]) * 60
        self.assertLess(2 * default_bound() + OTHER_TESTS_BUDGET, step_seconds)

    def test_the_unit_test_step_and_the_rest_of_the_job_fit_in_the_job(self) -> None:
        step_seconds = int(self.step("test.yaml", "test", "Run unit test")["timeout-minutes"]) * 60
        job_seconds = int(jobs(WORKFLOWS / "test.yaml")["test"]["keys"]["timeout-minutes"]) * 60
        self.assertLess(PRE_STEP_BUDGET + step_seconds + POST_STEP_BUDGET, job_seconds)

    def test_the_files_steps_fit_the_bound(self) -> None:
        for workflow in ("ubuntu.yaml", "macos.yaml"):
            with self.subTest(workflow=workflow):
                step_seconds = int(self.step(workflow, "build", "Test file existence")["timeout-minutes"]) * 60
                self.assertLess(default_bound() + FILES_STEP_BUDGET, step_seconds)

    def test_no_workflow_raises_the_per_test_bound(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                self.assertNotIn("BATS_PER_TEST_TIMEOUT:", path.read_text())
                self.assertNotIn("BATS_PER_TEST_TIMEOUT=", path.read_text())

    def test_every_step_that_runs_apt_ends_a_stall_inside_its_own_bound(self) -> None:
        # The step's timeout-minutes is the ceiling of its apt bounds (each N plus the kill delay) plus the measured
        # rest of the step, plus one minute: a stall ends under the step's name, never at the job's timeout.
        self.assertEqual([], workflow_problems(sorted(WORKFLOWS.glob("*.y*ml"))))

    def problems(self, steps_by_job: dict[str, list[dict]]) -> tuple[list[str], list[int]]:
        """The step problems of in-memory steps, written and read back through the reader, and their dash lines."""
        text = render(steps_by_job)
        path = Path(tempfile.mkdtemp(prefix="apt-steps-")) / "x.yaml"
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(path.parent)], check=False))
        path.write_text(text)
        return apt_step_problems({"x.yaml": text}, {"x.yaml": parsed_steps(path)}), dash_lines(text)

    def test_a_step_without_its_bound_cannot_hide_behind_a_later_step_of_the_same_name(self) -> None:
        # Audit of 9058072b: the registry was keyed by step name, so a later "Setup for Codecov" that carried
        # timeout-minutes replaced the earlier one that ran apt without it. Steps are keyed by (job, index) now, and
        # a name used twice in one job is refused on its own, since the budget table refers to steps by name.
        steps = bounded_steps()
        self.assertEqual(([], [7, 12, 17]), self.problems({"test": steps}))
        del steps[2]["timeout-minutes"]
        later = {**bounded_steps()[2], "run": "echo later\n" + bounded_steps()[2]["run"]}
        problems, at = self.problems({"test": [*steps, later]})
        self.assertEqual(
            [
                f"x.yaml:{at[3]}: test: step 3 'Setup for Codecov' repeats the name of step 2",
                f"x.yaml:{at[2]}: test: step 2 'Setup for Codecov' has no timeout-minutes",
            ],
            problems,
        )
        # The same name in another job is another step; unnamed steps have no name to collide.
        unnamed = {"run": "echo unnamed"}
        problems, _ = self.problems({"test": [*bounded_steps(), unnamed, unnamed], "other": [later]})
        self.assertEqual([], problems)

    def test_a_bounded_step_off_the_formula_or_outside_the_budget_table_is_named(self) -> None:
        steps = bounded_steps()
        steps[0]["timeout-minutes"] = "9"
        problems, at = self.problems({"test": steps})
        self.assertEqual(
            [f"x.yaml:{at[0]}: test: step 0 'Install tools' has timeout-minutes 9, the formula gives 10"], problems
        )
        steps = bounded_steps()
        steps[2]["name"] = "Upload coverage"
        problems, at = self.problems({"test": steps})
        self.assertEqual(
            [
                "budget row 'Setup for Codecov' has no step that runs apt",
                f"x.yaml:{at[2]}: test: step 2 'Upload coverage' runs apt with no STEP_REST_BUDGET row",
            ],
            problems,
        )
        steps = bounded_steps()
        del steps[1]["name"]
        problems, at = self.problems({"test": steps})
        self.assertEqual(
            [
                "budget row 'Run Python unit tests' has no step that runs apt",
                f"x.yaml:{at[1]}: test: step 1 'step 1' runs apt with no STEP_REST_BUDGET row",
            ],
            problems,
        )


class ReaderCensusTest(unittest.TestCase):
    """Standing order 21 on the workflow reader: every `run:` the text holds is one the reader returned whole, or the
    step is named by file and line. Audit of 0a9fa727: `jobs()` returned no body for `run: |-` and `run: >`, so an
    apt step added in that form passed the step check without timeout-minutes. Audit of 81fa7256: the census read
    only the reader's indentation, so a step at five and seven spaces passed both. Audit of f4486ead: the census
    compared the literal `steps:`, so `steps: # comment` hid a list at five and seven from both."""

    FORM = "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update"
    MARKER = "      - name: Upload coverage to Codecov\n"
    # Each form the reader does not return, as the value of an added step's `run:` key, with `{}` for the command.
    FORMS = (("|-", "|-\n          {}"), (">", ">\n          {}"), ("|2", "|2\n          {}"), ('"..."', '"{}"'))
    BASE = "name: x\non: push\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    steps:\n"

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="apt-census-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.temp)], check=False))

    def written(self, text: str, name: str = "x.yaml") -> Path:
        path = self.temp / name
        path.write_text(text)
        return path

    def added_step(self, form: str, command: str) -> tuple[Path, int, int]:
        """test.yaml with a step `Added` in `form` holding `command` before the Codecov upload: (path, dash line, index)."""
        text = (WORKFLOWS / "test.yaml").read_text()
        self.assertEqual(1, text.count(self.MARKER))
        before = text[: text.index(self.MARKER)]
        added = f"      - name: Added\n        run: {dict(self.FORMS)[form].format(command)}\n\n"
        return (
            self.written(before + added + self.MARKER + text[len(before) + len(self.MARKER) :], "test.yaml"),
            before.count("\n") + 1,
            len(dash_lines(before)),
        )

    def test_every_run_key_in_the_text_is_one_the_reader_returned(self) -> None:
        runs = 0
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                text = path.read_text()
                self.assertEqual([], census_problems(path.name, text, parsed_steps(path)))
                runs += sum(len(step["runs"]) for steps in text_steps(text).values() for step in steps)
        # test.yaml alone writes 14 `run: |` blocks and 4 one-line scalars; a census that found fewer saw nothing.
        self.assertGreaterEqual(runs, 18)

    def test_an_apt_step_in_a_form_the_reader_does_not_return_is_refused_by_line(self) -> None:
        # The auditor's step, in each of the four forms, with the unbounded call and with the exact bound form: the
        # census names the `run:` line, the step check names the step's line, and the apt rule names the call.
        for form, header in (("|-", "|-"), (">", ">"), ("|2", "|2"), ('"..."', '"sudo apt-get update"')):
            for command in ("sudo apt-get update", self.FORM):
                with self.subTest(form=form, command=command.split()[0]):
                    path, dash, index = self.added_step(form, command)
                    problems = workflow_problems([path])
                    expected_header = (
                        header if command == "sudo apt-get update" else header.replace("sudo apt-get update", self.FORM)
                    )
                    self.assertIn(f"test.yaml:{dash + 1}: run: {expected_header} ({READ_FORMS})", problems)
                    self.assertIn(
                        f"test.yaml:{dash}: test: step {index} 'Added' runs apt with no STEP_REST_BUDGET row", problems
                    )
                    self.assertEqual(2, len(problems), problems)
                    violations = apt_violations("test.yaml", path.read_text())
                    if command == self.FORM and form != '"..."':
                        self.assertEqual(
                            [], violations
                        )  # the bound form itself passes the line rule: the step check is the stop
                    else:
                        call_line = dash + 1 if form == '"..."' else dash + 2
                        self.assertEqual(1, len(violations), violations)
                        self.assertTrue(violations[0].startswith(f"test.yaml:{call_line}: "), violations[0])
        # The same step as `run: |` is read, and fails only the step check, on its line.
        path, dash, index = self.added_step("|-", self.FORM)
        path.write_text(path.read_text().replace("run: |-\n          timeout", "run: |\n          timeout"))
        self.assertEqual(
            [f"test.yaml:{dash}: test: step {index} 'Added' runs apt with no STEP_REST_BUDGET row"],
            workflow_problems([path]),
        )

    def test_a_reader_that_returns_less_than_the_text_holds_is_named(self) -> None:
        text = render({"test": bounded_steps()})
        good = parsed_steps(self.written(text))
        self.assertEqual([], census_problems("x.yaml", text, good))
        at = dash_lines(text)
        one_line = {**good["test"][1], "script": good["test"][1]["script"].splitlines()[0] + "\n"}
        for case, parsed, expected in (
            ("a job", {}, "x.yaml: the text holds jobs ['test'], the reader returned []"),
            ("a step", {"test": good["test"][:2]}, "x.yaml: test: 3 steps in the text, 2 from the reader"),
            (
                "a body line",
                {"test": [good["test"][0], one_line, good["test"][2]]},
                f"x.yaml:{at[1] + 2}: run: | (the reader's body is not the text's: 1 line(s) read, 2 written)",
            ),
            (
                "a plain value",
                {"test": [good["test"][0], good["test"][1], {**good["test"][2], "run": "echo", "script": ""}]},
                f"x.yaml:{at[2] + 2}: run: | (the reader's body is not the text's: 0 line(s) read, 1 written)",
            ),
        ):
            with self.subTest(case=case):
                self.assertEqual([expected], census_problems("x.yaml", text, parsed))
        with self.subTest(case="a run the text does not hold"):
            only_name = self.BASE + "      - name: Only a name\n"
            self.assertEqual([], census_problems("x.yaml", only_name, {"test": [{"name": "Only a name"}]}))
            self.assertEqual(
                ["x.yaml:7: the reader returned a run: the text does not hold"],
                census_problems("x.yaml", only_name, {"test": [{"name": "Only a name", "run": "echo"}]}),
            )

    def test_a_run_the_reader_misreads_is_named_by_line(self) -> None:
        # Through the real reader: the forms it returns in part or not at all, each refused with its line.
        for case, step, expected in (
            (
                "a second run: key",
                "      - name: Two\n        run: echo one\n        run: echo two\n",
                ["x.yaml:9: run: echo two (a second run: key in one step)"],
            ),
            (
                "a block line indented nine spaces",
                "      - run: |\n          echo ten\n         echo nine\n",
                [
                    "x.yaml:9: echo nine (indented 9 inside a block whose first line is at 10)",
                    "x.yaml:7: run: | (the reader's body is not the text's: 1 line(s) read, 2 written)",
                ],
            ),
            (
                "a plain scalar that continues",
                "      - run: echo a\n          echo b\n",
                [f"x.yaml:7: run: echo a (continues onto 1 more line(s); {READ_FORMS})"],
            ),
            ("an empty run:", "      - run:\n", [f"x.yaml:7: run: ({READ_FORMS})"]),
            ("a single-quoted scalar", "      - run: 'echo a'\n", [f"x.yaml:7: run: 'echo a' ({READ_FORMS})"]),
            ("a keep block", "      - run: |+\n          echo a\n", [f"x.yaml:7: run: |+ ({READ_FORMS})"]),
            ("a folded strip block", "      - run: >-\n          echo a\n", [f"x.yaml:7: run: >- ({READ_FORMS})"]),
            (
                "a block with a comment after the header",
                "      - run: | # why\n          echo a\n",
                [f"x.yaml:7: run: | # why ({READ_FORMS})"],
            ),
        ):
            with self.subTest(case=case):
                path = self.written(self.BASE + step)
                self.assertEqual(expected, census_problems("x.yaml", path.read_text(), parsed_steps(path)))
        # And the two forms the reader returns pass, on the dash line as under it.
        for step in (
            "      - run: echo a\n",
            "      - run: |\n          echo a\n\n          echo b\n",
            "      - name: A\n        run: echo a\n",
        ):
            with self.subTest(step=step):
                path = self.written(self.BASE + step)
                self.assertEqual([], census_problems("x.yaml", path.read_text(), parsed_steps(path)))

    def added_job_at(self, dash: int, keys: int, command: str, steps_key: str = "steps:") -> tuple[Path, int]:
        """test.yaml with a job `added` after `test`, its one step `Added` a `run: |` holding `command`, the step list
        with its dash at `dash` spaces and its keys at `keys` (a list's dashes share one indent, so the shape is the
        list's, not one step's), under `steps_key` as the key line: (path, dash line)."""
        text = (WORKFLOWS / "test.yaml").read_text()
        lead = " " * dash + "-" + " " * (keys - dash - 1)
        job = f"\n  added:\n    runs-on: ubuntu-24.04\n    {steps_key}\n{lead}name: Added\n{' ' * keys}run: |\n{' ' * (keys + 2)}{command}\n"
        return self.written(text + job, "test.yaml"), len(text.splitlines()) + 5

    def agrees_with_yaml(self, text: str) -> None:
        """Where PyYAML is installed, it reads the same jobs, steps and run bodies as the census; elsewhere nothing."""
        try:
            import yaml
        except ImportError:
            return
        document = yaml.safe_load(text)
        found = text_steps(text)
        self.assertEqual(list(document["jobs"]), list(found))
        for job, steps in found.items():
            parsed = document["jobs"][job]["steps"]
            self.assertEqual(len(parsed), len(steps), job)
            for step, got in zip(steps, parsed):
                self.assertEqual("run" in got, bool(step["runs"]), (job, step["line"]))
                for run in step["runs"]:
                    written = (
                        [line.strip() for line in run["body"] if line.strip()]
                        if run["header"] == "|"
                        else [run["header"]]
                    )
                    self.assertEqual(
                        written,
                        [line.strip() for line in str(got["run"]).splitlines() if line.strip()],
                        (job, run["line"]),
                    )

    def test_the_text_census_agrees_with_a_yaml_parser_when_one_is_present(self) -> None:
        # Not a dependency: CI's interpreter has none. Where PyYAML is installed, it is a second reader of the same
        # files, and the census must see every step and every run body it sees.
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("no PyYAML in this interpreter (the CI form)")
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                self.agrees_with_yaml(path.read_text())

    def test_the_auditors_step_at_five_and_seven_is_refused_by_its_dash_line(self) -> None:
        # Audit of 81fa7256: a step list whose dashes are at five spaces and keys at seven is YAML the runner
        # executes, and the reader returns no step for it; the round 3 census, fixed at six and eight, skipped it the
        # same way. The census now reads it (as PyYAML does) and names each step; the step check then names the apt
        # step it holds, and a step that only sleeps is named by the census alone.
        for dash, keys in ((5, 7), (7, 9)):
            for command in ("sudo apt-get update", self.FORM, "sleep 7200"):
                with self.subTest(dash=dash, keys=keys, command=command.split()[0]):
                    path, at = self.added_job_at(dash, keys, command)
                    text = path.read_text()
                    (step,) = text_steps(text)["added"]
                    self.assertEqual([], parsed_steps(path)["added"])  # the hole: the reader's silent skip
                    self.assertEqual((at, dash, keys), (step["line"], step["dash"], step["keys"]))
                    self.assertEqual([command], [line.strip() for line in step["runs"][0]["body"]])
                    self.agrees_with_yaml(text)
                    expected = [
                        f"test.yaml:{at}: a step with its dash at {dash} spaces and its keys at {keys} ({READER_SHAPE})"
                    ]
                    if command != "sleep 7200":
                        expected.append(f"test.yaml:{at}: added: step 0 'step 0' runs apt with no STEP_REST_BUDGET row")
                    self.assertEqual(expected, workflow_problems([path]))
                    violations = apt_violations("test.yaml", text)
                    if command == "sudo apt-get update":
                        self.assertEqual(
                            [f"test.yaml:{at + 2}: {command} (1 apt call(s), 0 in the bound form)"], violations
                        )
                    else:
                        self.assertEqual([], violations)
        # Written at six and eight, the same job is read by both and fails only the step check, on the step's line.
        path, at = self.added_job_at(6, 8, self.FORM)
        self.assertEqual(
            [f"test.yaml:{at}: added: step 0 'Added' runs apt with no STEP_REST_BUDGET row"], workflow_problems([path])
        )

    def test_a_run_inside_a_value_is_not_a_key(self) -> None:
        # A `run:` indented past the step's keys is the value of the key above it: a block body line, or an entry of
        # a nested mapping. It is one run or none, never a second key, at the reader's shape and at any other.
        inner = "run: sudo apt-get update"
        for case, step, runs, problems in (
            ("a block body line", f"      - run: |\n          echo a\n          {inner}\n", [["echo a", inner]], []),
            ("a with: mapping", f"      - uses: x/y@v1\n        with:\n          {inner}\n", [], []),
            ("an env: mapping after a plain run", f"      - run: echo a\n        env:\n          {inner}\n", [[]], []),
            (
                "a block body line at five and seven",
                f"     - run: |\n         echo a\n         {inner}\n",
                [["echo a", inner]],
                [f"x.yaml:7: a step with its dash at 5 spaces and its keys at 7 ({READER_SHAPE})"],
            ),
        ):
            with self.subTest(case=case):
                text = self.BASE + step
                found = census(text)
                self.assertEqual([], found.refused)
                (only,) = found.steps["test"]
                self.assertEqual(runs, [[line.strip() for line in run["body"]] for run in only["runs"]])
                self.assertEqual(problems, census_problems("x.yaml", text, parsed_steps(self.written(text))))
                self.agrees_with_yaml(text)

    def test_the_census_reads_steps_at_any_shape_and_the_reader_only_its_own(self) -> None:
        # The three bounded steps written at other indents: the census reads each whole and agrees with PyYAML where
        # present; the reader returns the steps at its own shape, skips those at five and seven (named by the census
        # on each dash line) and raises on the rest.
        for shape, reader in (
            ((2, 4, 6, 8), "returns"),
            ((2, 4, 5, 7), "skips"),
            ((2, 4, 7, 9), "skips"),
            ((2, 4, 4, 6), "raises"),
            ((2, 4, 6, 10), "raises"),
            ((1, 2, 3, 5), "raises"),
            ((4, 8, 12, 14), "raises"),
        ):
            with self.subTest(shape=shape):
                text = render({"test": bounded_steps()}, shape)
                path = self.written(text)
                found = census(text)
                self.assertEqual([], found.refused)
                steps = found.steps["test"]
                self.assertEqual(dash_lines(text, shape[2]), [step["line"] for step in steps])
                self.assertEqual([shape[2:]] * 3, [(step["dash"], step["keys"]) for step in steps])
                self.assertEqual(
                    [step["run"].splitlines() for step in bounded_steps()],
                    [[line.strip() for line in step["runs"][0]["body"]] for step in steps],
                )
                self.agrees_with_yaml(text)
                if reader == "returns":
                    self.assertEqual([], census_problems("x.yaml", text, parsed_steps(path)))
                elif reader == "skips":
                    parsed = parsed_steps(path)
                    self.assertEqual([], parsed["test"])
                    self.assertEqual(
                        [
                            f"x.yaml:{step['line']}: a step with its dash at {shape[2]} spaces and its keys at {shape[3]} "
                            f"({READER_SHAPE})"
                            for step in steps
                        ],
                        census_problems("x.yaml", text, parsed),
                    )
                else:
                    with self.assertRaises(ValueError):
                        parsed_steps(path)

    def test_a_line_off_the_shape_is_refused_by_line(self) -> None:
        # A line inside `jobs:` at none of the derived indents and not past the key above it is named, never skipped.
        at_step = "a job at 2, a job key at 4, a step's dash at 6, a step key at 8"
        no_dash = "a job at 2, a job key at 4, a step's dash at or past 4"
        for case, step, expected, yaml_raises, reader_raises in (
            (
                "between the keys and the dash",
                "      - run: echo a\n     odd: 1\n",
                [(8, "odd: 1", 5, at_step)],
                True,
                False,
            ),
            (
                "between the dash and the keys",
                "      - run: echo a\n       odd: 1\n",
                [(8, "odd: 1", 7, at_step)],
                True,
                False,
            ),
            ("before the job's keys", "      - run: echo a\n   odd: 1\n", [(8, "odd: 1", 3, at_step)], True, False),
            (
                "a dash off the list's indent",
                "      - run: echo a\n     - run: echo b\n",
                [(8, "- run: echo b", 5, at_step)],
                True,
                False,
            ),
            ("under steps:, no dash", "        name: no dash\n", [(7, "name: no dash", 8, no_dash)], False, True),
            (
                "a bare dash",
                "      -\n        run: echo a\n",
                [(7, "-", 6, no_dash), (8, "run: echo a", 8, no_dash)],
                False,
                True,
            ),
            (
                "a body line after a comment ended the block",
                "      - run: |\n          echo a\n      # c\n          echo b\n",
                [(10, "echo b", 10, at_step)],
                True,
                False,
            ),
        ):
            with self.subTest(case=case):
                text = self.BASE + step
                refused = [
                    (number, f"{line} (indented {indent}, where the shape has {levels})")
                    for number, line, indent, levels in expected
                ]
                self.assertEqual(refused, census(text).refused)
                path = self.written(text)
                if reader_raises:  # the reader is loud there on its own; the census refuses the same lines
                    with self.assertRaises(ValueError):
                        parsed_steps(path)
                else:
                    problems = census_problems("x.yaml", text, parsed_steps(path))
                    self.assertEqual([f"x.yaml:{number}: {why}" for number, why in refused], problems[: len(refused)])
                if yaml_raises:
                    try:
                        import yaml
                    except ImportError:
                        continue
                    with self.assertRaises(yaml.YAMLError):
                        yaml.safe_load(text)

    def test_steps_with_a_comment_after_it_is_the_steps_key(self) -> None:
        # Audit of f4486ead: the round 4 census compared the literal `steps:`, so `steps: # comment` was an opaque
        # value whose list at five and seven was skipped by both readers (the reader takes the key with its comment
        # and skips the shape). The lexer takes the key the same way: the list is counted at every shape, refused on
        # its dash line where the reader does not reach it, and bounded or named where it does.
        for dash, keys in ((5, 7), (6, 8)):
            for command in ("sudo apt-get update", self.FORM, "sleep 7200"):
                with self.subTest(dash=dash, keys=keys, command=command.split()[0]):
                    path, at = self.added_job_at(dash, keys, command, "steps: # comment")
                    text = path.read_text()
                    (step,) = text_steps(text)["added"]
                    self.assertEqual((at, dash, keys), (step["line"], step["dash"], step["keys"]))
                    self.assertEqual([command], [line.strip() for line in step["runs"][0]["body"]])
                    self.agrees_with_yaml(text)
                    expected = []
                    if (dash, keys) == (5, 7):
                        self.assertEqual([], parsed_steps(path)["added"])  # the hole: the reader's silent skip
                        expected.append(
                            f"test.yaml:{at}: a step with its dash at 5 spaces and its keys at 7 ({READER_SHAPE})"
                        )
                        label = "'step 0'"
                    else:
                        (read,) = parsed_steps(path)["added"]
                        self.assertEqual(("Added", "|", command), (read["name"], read["run"], read["script"].strip()))
                        label = "'Added'"
                    if command != "sleep 7200":
                        expected.append(f"test.yaml:{at}: added: step 0 {label} runs apt with no STEP_REST_BUDGET row")
                    self.assertEqual(expected, workflow_problems([path]))
        # The real file with a comment after its own steps: key reads the same, step for step.
        text = (WORKFLOWS / "test.yaml").read_text()
        self.assertEqual(1, text.count("\n    steps:\n"))
        commented = text.replace("\n    steps:\n", "\n    steps: # the steps\n")
        self.assertEqual(text_steps(text), text_steps(commented))
        self.assertEqual([], workflow_problems([self.written(commented, "test.yaml")]))
        self.agrees_with_yaml(commented)

    def test_every_construct_outside_the_grammar_is_refused_by_line(self) -> None:
        # The closed grammar, construct by construct: each row is a workflow holding one construct outside it, the
        # refusals the census must name (line, text and why) and what PyYAML makes of the document where it is
        # present ("reads": YAML the runner could execute, the rows that matter; "raises"; None: not asserted). The
        # reader, where it does not raise on its own, is cross-checked and names the same lines first.
        head = "name: x\non: push\njobs:\n"
        job = head + "  test:\n    runs-on: ubuntu-24.04\n"
        base = job + "    steps:\n"
        update = "sudo apt-get update"
        not_key = f"not {KEY_FORM}"
        step_keys, job_keys = ", ".join(sorted(STEP_KEYS)), ", ".join(sorted(JOB_KEYS))
        rows = (
            # the value of steps:
            (
                "a flow list on steps:",
                job + f"    steps: [{{run: {update}}}]\n",
                [(6, f"steps: [{{run: {update}}}] (steps: holds a flow collection; {STEPS_VALUE})")],
                "reads",
            ),
            (
                "an alias on steps:",
                "name: x\non: &s push\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    steps: *s\n",
                [(6, f"steps: *s (steps: holds an alias; {STEPS_VALUE})")],
                "reads",
            ),
            (
                "an anchor on steps:",
                job + f"    steps: &s\n      - run: {update}\n",
                [(6, f"steps: &s (steps: holds an anchor; {STEPS_VALUE})")],
                "reads",
            ),
            (
                "a tag on steps:",
                job + f"    steps: !!seq\n      - run: {update}\n",
                [(6, f"steps: !!seq (steps: holds a tag; {STEPS_VALUE})")],
                "reads",
            ),
            (
                "a block header on steps:",
                job + f"    steps: |\n      - run: {update}\n",
                [(6, f"steps: | (steps: holds a block header; {STEPS_VALUE})")],
                "reads",
            ),
            (
                "a plain value on steps:",
                job + "    steps: none\n",
                [(6, f"steps: none (steps: holds a plain scalar; {STEPS_VALUE})")],
                "reads",
            ),
            # the key itself
            (
                "a quoted steps key",
                job + f'    "steps":\n      - run: {update}\n',
                [(6, f'"steps": ({not_key})')],
                "reads",
            ),
            (
                "a complex steps key",
                job + f"    ? steps\n    : - run: {update}\n",
                [(6, f"? steps ({not_key})"), (7, f": - run: {update} ({not_key})")],
                "reads",
            ),
            (
                "a merge key",
                f"name: x\non: &base\n  steps:\n    - run: {update}\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    <<: *base\n",
                [(8, f"<<: *base ({not_key})")],
                "reads",
            ),
            (
                "an upper-case steps key",
                job + f"    Steps:\n      - run: {update}\n",
                [(6, f"Steps: ({not_key})")],
                "reads",
            ),
            (
                "no blank after the colon",
                job + f"    steps:- run: {update}\n",
                [(6, f"steps:- run: {update} ({not_key})")],
                None,
            ),
            # a job line
            (
                "a job line with an anchor",
                head + f"  test: &job\n    runs-on: ubuntu-24.04\n    steps:\n      - run: {update}\n",
                [(4, "test: &job (a job line with a value; the job's keys follow on their own lines)")],
                "reads",
            ),
            (
                "a quoted job key",
                head + f'  "test":\n    runs-on: ubuntu-24.04\n    steps:\n      - run: {update}\n',
                [(4, f'"test": ({not_key})')],
                "reads",
            ),
            (
                "a second job of one name",
                base + f"      - run: echo a\n  test:\n    runs-on: ubuntu-24.04\n    steps:\n      - run: {update}\n",
                [(8, "test: (a second job named test)")],
                "reads",
            ),
            (
                "a list at the jobs' indent",
                head + "  - test:\n      runs-on: ubuntu-24.04\n",
                [(4, f"- test: ({not_key})")],
                "reads",
            ),
            # a step entry
            ("a scalar step", base + "      - echo\n", [(7, f"- echo ({not_key})")], "reads"),
            (
                "a flow-mapping step",
                base + f"      - {{run: {update}}}\n",
                [(7, f"- {{run: {update}}} ({not_key})")],
                "reads",
            ),
            (
                "a nested list step",
                base + f"      - - run: {update}\n",
                [(7, f"- - run: {update} ({not_key})")],
                "reads",
            ),
            (
                "an alias step",
                f"name: x\non: &s {{run: {update}}}\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    steps:\n      - *s\n",
                [(7, f"- *s ({not_key})")],
                "reads",
            ),
            (
                "an anchored step",
                base + f"      - &s run: {update}\n",
                [(7, f"- &s run: {update} ({not_key})")],
                "reads",
            ),
            (
                "a quoted step key",
                base + f'      - "run": {update}\n',
                [(7, f'- "run": {update} ({not_key})')],
                "reads",
            ),
            # a step key
            (
                "a key the schema gives no step",
                base + "      - run: echo a\n        foo: 1\n",
                [(8, f"foo: 1 (foo: is not a step key; the step keys are {step_keys})")],
                "reads",
            ),
            (
                "a second name: key in one step",
                base + "      - name: a\n        name: b\n",
                [(8, "name: b (a second name: key in one step)")],
                "reads",
            ),
            (
                "a comment after a one-line run:",
                base + "      - run: echo a # c\n",
                [(7, f"- run: echo a # c ({RUN_COMMENT})")],
                "reads",
            ),
            (
                "an anchor on a step key",
                base + "      - name: &n x\n",
                [(7, f"- name: &n x (name: holds an anchor; {READ_VALUES})")],
                "reads",
            ),
            (
                "an alias on a step key",
                "name: x\non: &u push\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    steps:\n      - uses: *u\n",
                [(7, f"- uses: *u (uses: holds an alias; {READ_VALUES})")],
                "reads",
            ),
            (
                "a block scalar on if:",
                base + "      - run: echo a\n        if: |\n          true\n",
                [(8, f"if: | (if: holds a block header; {READ_VALUES})")],
                "reads",
            ),
            (
                "a tag on a step key",
                base + "      - name: !!str x\n",
                [(7, f"- name: !!str x (name: holds a tag; {READ_VALUES})")],
                "reads",
            ),
            (
                "a sequence entry as a value",
                base + "      - name: - x\n",
                [(7, f"- name: - x (name: holds a sequence entry; {READ_VALUES})")],
                "raises",
            ),
            (
                "a reserved indicator as a value",
                base + "      - name: @x\n",
                [(7, f"- name: @x (name: holds a reserved indicator; {READ_VALUES})")],
                "raises",
            ),
            # a job key
            (
                "a key the schema gives no job",
                job + "    foo: 1\n    steps:\n      - run: echo a\n",
                [(6, f"foo: 1 (foo: is not a job key; the job keys are {job_keys})")],
                "reads",
            ),
            (
                "a second steps: key in one job",
                base + f"      - run: echo a\n    steps:\n      - run: {update}\n",
                [(8, "steps: (a second steps: key in one job)")],
                "reads",
            ),
            (
                "an alias on a job key",
                "name: x\non: &e {}\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    env: *e\n    steps:\n      - run: echo a\n",
                [(6, f"env: *e (env: holds an alias; {READ_VALUES})")],
                "reads",
            ),
            (
                "a block scalar on runs-on:",
                head + "  test:\n    runs-on: |\n      ubuntu-24.04\n    steps:\n      - run: echo a\n",
                [(5, f"runs-on: | (runs-on: holds a block header; {READ_VALUES})")],
                "reads",
            ),
            # the file
            (
                "a tab as the indentation",
                base + f"\t- run: {update}\n",
                [(7, f"- run: {update} (a tab in the indentation)")],
                "raises",
            ),
            (
                "a tab after the spaces",
                base + f"      \t- run: {update}\n",
                [(7, f"- run: {update} (a tab in the indentation)")],
                "raises",
            ),
            (
                "a carriage return",
                base + f"      - run: {update}\r\n",
                [(7, f"- run: {update} (a carriage return; the workflows are LF-only)")],
                "reads",
            ),
            (
                "a document marker",
                base + f"      - run: echo a\n---\n  other:\n    steps:\n      - run: {update}\n",
                [(8, f"--- (not {KEY_FORM}; both readers stop at the first unindented line)")],
                "raises",
            ),
            (
                "a second jobs: key",
                f"name: x\non: push\njobs:\n  a:\n    runs-on: ubuntu-24.04\njobs:\n  test:\n    steps:\n      - run: {update}\n",
                [(6, "jobs: (a second jobs: key)")],
                "reads",
            ),
            (
                "jobs: with a comment",
                f"name: x\non: push\njobs: # c\n  test:\n    steps:\n      - run: {update}\n",
                [(3, f"jobs: # c ({JOBS_LINE})")],
                "reads",
            ),
            ("no jobs: line", "name: x\non: push\n", [(1, f"no `jobs:` line in the file ({JOBS_LINE})")], "reads"),
            (
                "a block line indented less than its first",
                base + "      - run: |\n          echo ten\n         echo nine\n",
                [(9, "echo nine (indented 9 inside a block whose first line is at 10)")],
                "raises",
            ),
        )
        self.assertEqual(len(rows), len({case for case, _, _, _ in rows}))
        for case, text, refused, yaml_reads in rows:
            with self.subTest(case=case):
                self.assertEqual(refused, census(text).refused)
                try:
                    parsed = parsed_steps(self.written(text))
                except (ValueError, IndexError):
                    parsed = None  # the reader is loud there on its own
                if parsed is not None:
                    problems = census_problems("x.yaml", text, parsed)
                    self.assertEqual([f"x.yaml:{number}: {why}" for number, why in refused], problems[: len(refused)])
                if yaml_reads is None:
                    continue
                try:
                    import yaml
                except ImportError:
                    continue
                if yaml_reads == "reads":
                    yaml.safe_load(text)
                else:
                    with self.assertRaises(yaml.YAMLError):
                        yaml.safe_load(text)


if __name__ == "__main__":
    unittest.main()
