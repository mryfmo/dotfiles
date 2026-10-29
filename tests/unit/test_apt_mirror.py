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

import argparse
import functools
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Iterator, NamedTuple
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_workflow_orchestration_skip import jobs

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/ci"))
import shfmt_json_contract as contract  # noqa: E402  (round 10: the run bodies are read from shfmt's tree)

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
# U109: every apt call a workflow runs carries its own bound, in one exact form. `/usr/bin/timeout` ends a call that
# keeps printing nothing at N seconds and kills it KILL_AFTER seconds later; apt's own options give up a connection or
# read silent for 15 s and move to the next mirror, three times. N is measured per step (the comment next to each call
# in the workflow) with twice the measured time and at least 120 s of margin, so never under MIN_APT_BOUND.
APT_CALL = re.compile(r"\bapt-get\b|\bapt\s+(?:install|update|upgrade|full-upgrade|dist-upgrade)\b")
# Round 9 (audit of ecde33b9): the form was matched anywhere on a line, so `ci_timeout --kill-after=10 180 sudo
# apt-get ...`, with `ci_timeout() { shift 2; "$@"; }` defined on the line above, held the form as the tail of another
# command's name and ran apt with no GNU timeout past every check. Round 10 (audit of 15c4afa8): the `run:` command
# start was not anchored, so `ci.run: timeout ...` counted with a function `ci.run:` defined above it, and `time\` at
# the end of one line with `out() { ... }` on the next is a `timeout` function to bash that a check of physical lines
# never saw. The first word of the form is now coreutils' path, TIMEOUT_PATH: no alias (an alias name takes no `/`),
# no `hash -p` and no PATH entry stands in for a path. A function can be named by a path in bash (`/usr/bin/timeout()
# { ...; }` runs in place of the binary), so the tree rule below refuses every function definition in an apt step. The
# text rule stays as the superset: the form counts where TIMEOUT_PATH is whole (TIMEOUT_WORD: no letter, digit, `_`,
# `.`, `/` or `-` touches it) and the first word of its command: at the start of the line (after a `- ` dash or a
# `run:` key there, LINE_STARTS) or after one of COMMAND_STARTS, with nothing but whitespace between. A form anywhere
# else fails the line naming its position: the longer word, the bare name, or the text the form follows.
TIMEOUT_PATH = "/usr/bin/timeout"
TIMEOUT_WORD = r"(?<![\w./-])/usr/bin/timeout(?![\w./-])"
TIMEOUT_NAME = r"(?<![\w./-])(?:/usr/bin/)?timeout(?![\w./-])"  # the name a definition gives, bare or by the path
APT_FORM = (
    r" --kill-after=10 ([0-9]+) sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 "
    r"(?:update|install)(?=\s|$)"
)
COMMAND_STARTS = ("&&", "||", ";", "|", "(")
LINE_STARTS = ("", "- ", "run: ", "- run: ")
COMMAND_START = r"(?:^[ \t]*(?:-[ \t]+)?(?:run:[ \t]+)?|&&|\|\||;|\||\()\s*"
APT_BOUND = re.compile(COMMAND_START + TIMEOUT_WORD + APT_FORM, re.MULTILINE)  # `^`: each line of a step's commands
APT_FORM_ANYWHERE = re.compile("timeout" + APT_FORM)
COMMAND_WORD = (
    "the form counts where `/usr/bin/timeout` is a whole word and the first word of its command: at the start of the "
    "line (after a `- ` dash or a `run:` key there) or after `&&`, `||`, `;`, `|` or `(`, with only whitespace between"
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
# And no logical line of any workflow (physical lines ending in a backslash joined, as bash joins them) gives
# `timeout`, bare or by its path, another meaning in the shell that runs the form. APT_REDEFINITIONS is the closed
# table of those constructs, each a pattern refused by line with its reason. A `hash -p`, an `enable -f`, a file
# written into a PATH directory and a PATH edit bind what the shell finds for a bare name, never for a path, so the
# form's first word is out of their reach; the tree rule (round 10) refuses them in an apt step all the same.
APT_REDEFINITIONS = {
    "a `function timeout` definition": (
        rf"\bfunction[ \t]+{TIMEOUT_NAME}",
        "bash runs the function in place of GNU timeout",
    ),
    "a `timeout()` definition": (
        rf"(?<!function[ \t]){TIMEOUT_NAME}[ \t]*\([ \t]*\)",  # the `function timeout()` spelling is the row above
        "bash runs the function in place of GNU timeout",
    ),
    "an `alias timeout=`": (
        r"\balias\b[^\n]*?(?<![\w-])timeout=",
        "a shell with aliases expanded runs the alias in place of GNU timeout",
    ),
}
REDEFINED = {construct: (re.compile(pattern), why) for construct, (pattern, why) in APT_REDEFINITIONS.items()}
REDEFINITION = "no workflow line gives `timeout` another meaning"
# (workflow file name, the whole stripped line, exactly) -> why the line may name apt without the form. Empty on this
# head: the three workflows that bootstrap through setup.sh run apt only inside the installers, whose downloads U99
# bounded, and no workflow comment names apt-get. A row must still match a line (test_no_apt_exemption_is_stale).
APT_EXEMPT: dict[tuple[str, str], str] = {}
# Measured, in seconds, outside the apt calls (passing `test` jobs, every matrix row, runs 40314863147 to
# 40610790312): "Install tools" at most 73 s (ubuntu-24.04 server, run 40338292845), 14 to 46 s elsewhere; "Run
# Python unit tests" at most 664 s (macos-15 client, run 40610790312), 189 to 388 s on the Ubuntu rows. Twice the
# maximum each, so a step bound ends a stall, never a slow passing run. Round 12: every apt call runs in a step of its
# own that holds nothing else (the tree rule below), so an apt step's rest is 0 and its bound is its calls alone;
# the two steps that held the calls keep the formula over their measured rest (REST_ONLY_BUDGET, BoundOrderTest).
STEP_REST_BUDGET = {
    "Install apt packages": 0,
    "Install apt packages for the unit tests": 0,
    "Install apt packages for Codecov": 0,
}
REST_ONLY_BUDGET = {"Install tools": 150, "Run Python unit tests": 1330}
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
# Round 6 (audit of 56e41f9b): the round 5 grammar began at the `jobs:` line and read nothing before it, so a
# top-level `name: "x` whose quoted value continued onto a `jobs:` line at the margin handed both readers a jobs key
# inside the string, and the real `"jobs":` mapping under a quoted key (YAML the runner executes) was never read: an
# apt step there passed. The grammar now covers the whole document: every line at the margin is a plain key the
# workflow schema allows (TOP_KEYS) whose value is a read form and complete on its line (a quoted scalar closes, a
# flow collection balances; a `#` inside either is content), `jobs:` is bare and once, and a line indented under any
# other top-level key is its value. No line of the file is unread.
TOP_KEYS = frozenset("name run-name on permissions env defaults concurrency jobs".split())
TOP_STOP = "both readers stop at the first unindented line"
# Round 7 (audit of 8c1d334a): the census split the text at LF alone and took Python's notion of a blank, while
# PyYAML (YAML 1.1) also breaks a line at U+0085, U+2028 and U+2029, so a comment line that went on after one of
# them held a second job and its apt step that the census and the reader read as comment text. Before any line is
# read, every character of the file is held to the printable set YAML 1.2 (5.1) gives a document, less the three
# YAML 1.1 line breaks and the byte order mark: a tab, LF and the printable characters (U+0020 to U+007E, U+00A0 to
# U+D7FF, U+E000 to U+FFFD and the supplementary planes). Every other character is refused by line and column with
# its class named (REFUSED_CHARACTERS, a closed table; a byte that is not UTF-8 arrives as the lone surrogate
# `surrogateescape` gives it), and a file with a refused character has no lines: nothing after the scan reads it.
# The lexer's blank is YAML's (6.1: a space or a tab), never Python's, so no printable character is stripped.
WHITE = " \t"
REFUSED_CHARACTERS = {
    "a carriage return": "\r",
    "a C0 control character": "\x00-\x08\x0b\x0c\x0e-\x1f",
    "a delete character": "\x7f",
    "a next line, a line break to a YAML 1.1 reader": "\x85",
    "a C1 control character": "\x80-\x84\x86-\x9f",
    "a line separator, a line break to a YAML 1.1 reader": "\u2028",
    "a paragraph separator, a line break to a YAML 1.1 reader": "\u2029",
    "a byte that is not UTF-8": "\udc80-\udcff",
    "a surrogate code point": "\ud800-\udc7f\udd00-\udfff",
    "a byte order mark": "\ufeff",
    "a noncharacter": "\ufffe\uffff",
}
REFUSED_CHARACTER = re.compile(f"[{''.join(REFUSED_CHARACTERS.values())}]")
CHARACTER_CLASS = {name: re.compile(f"[{body}]") for name, body in REFUSED_CHARACTERS.items()}
CHARACTER_SET = "the file is held to a tab, LF and the printable characters before any line is read"
# Round 8 (audit of 046aebb1): node_end saw no quote right after the `?` indicator, so `env: {?"x}` was a flow
# collection complete on its line to the census and the reader, while to PyYAML `"x}` opens a double-quoted key that
# runs across the lines that follow to the next `"`: a phantom step and its timeout-minutes, which both hand-written
# readers counted and the step check attached to the real apt step, were text inside the key, and the real step had
# no timeout-minutes. Rounds 5 to 7 completed the lexer corner by corner; the gate is now a real parser: every
# workflow the step check reads must agree with PyYAML, run in a child the uv idiom starts (CI's interpreter has no
# YAML parser; regime.yml's tests read their workflow the same way), on the job set, each job's step count, each
# step's run body, name and timeout-minutes, any difference a failure named by job and step. The closed grammar stays
# as the explanation layer: it names the line and the construct where it can, the parser decides. Round 9 (audit of
# ecde33b9): that child was long-lived and its answer was read before its exit status, which the stop at exit
# discarded, so a child that answered and then exited nonzero was trusted. The child is now one per document (the
# answer is cached by text): it reads the document as one JSON string, prints PyYAML's document or its refusal as
# one JSON line and exits; the status is read first, and a nonzero status, no answer, more than one, or an answer
# in another shape is a failure naming the status, the output and stderr, never a document (standing order 21).
UV_PYYAML = [shutil.which("uv") or "uv", "run", "--no-config", "--no-project", "--with", "pyyaml", "python", "-I"]
PARSER = """\
import json, sys, yaml

try:
    reply = json.dumps({"document": yaml.safe_load(json.loads(sys.stdin.read()))}, default=str)
except Exception as error:  # PyYAML refuses the document, or JSON cannot carry it (a key that is not a scalar)
    reply = json.dumps({"error": f"{type(error).__name__}: {' '.join(str(error).split())}"})
print(reply)
"""
PARSER_GATE = "the step check reads a workflow only where PyYAML reads the same jobs, steps and run bodies"


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


def misplaced_forms(line: str) -> list[str]:
    """Why each bound form on `line` that is not counted is not, by position: its first word is a longer word that
    ends in `timeout`, the bare name, or the path after text that does not start a command."""
    counted = {match.end() for match in APT_BOUND.finditer(line)}
    found = []
    for match in APT_FORM_ANYWHERE.finditer(line):
        if match.end() in counted:
            continue
        before = line[: match.start()]
        head = re.search(r"[\w./-]+$", before)  # the characters that make `timeout` the tail of a longer word
        word = (head.group() if head else "") + "timeout"
        column = (head.start() if head else match.start()) + 1
        if word == TIMEOUT_PATH:
            start = before[: head.start()]
            found.append(f"the form at column {column} follows {start!r}, not a command start; {COMMAND_WORD}")
        elif head:
            found.append(
                f"`timeout` at column {column} is the tail of the word {word!r}, not `{TIMEOUT_PATH}`; {COMMAND_WORD}"
            )
        else:
            found.append(f"`timeout` at column {column} is the bare name, not `{TIMEOUT_PATH}`; {COMMAND_WORD}")
    return found


def redefinitions(line: str) -> list[str]:
    """Every construct on `line` that gives `timeout` another meaning, with its reason."""
    return [
        f"{construct}: {why}; {REDEFINITION}" for construct, (pattern, why) in REDEFINED.items() if pattern.search(line)
    ]


def logical_lines(text: str) -> list[tuple[int, int, str]]:
    """The lines of `text` as bash reads them: a line ending in a backslash is joined with the next, the backslash
    and the newline removed, and the next line's indentation with them (a `run: |` body loses its block indentation
    before bash reads it, so the join is made as if every continuation stood at the block's margin; a continuation
    indented past it is then read as closer to a definition than bash reads it, never further).
    `(first physical line, how many physical lines, the joined text, stripped)`."""
    joined, start, count, parts = [], 1, 0, []
    for number, raw in enumerate(text.split("\n"), 1):
        if not parts:
            start = number
        parts.append(raw.rstrip("\r") if not parts else raw.rstrip("\r").lstrip(WHITE))
        count += 1
        if parts[-1].endswith("\\") and number < text.count("\n") + 1:
            parts[-1] = parts[-1][:-1]
            continue
        joined.append((start, count, "".join(parts).strip()))
        parts, count = [], 0
    return joined


def apt_violations(relative: str, text: str, exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The lines of one workflow that name apt outside the bound form, or give a name the form runs another meaning,
    as `file:line: text (why)`. A redefinition is looked for on the logical line (round 10: `time\\` and a newline
    before `out() { ...; }` is one `timeout` definition to bash), named at its first physical line."""
    exempt = APT_EXEMPT if exempt is None else exempt
    bad = []
    for number, count, line in logical_lines(text):
        if (relative, line) in exempt:
            continue
        joined = f"; joined from {count} lines ending in a backslash" if count > 1 else ""
        bad.extend(f"{relative}:{number}: {line} ({why}{joined})" for why in redefinitions(line))
    for number, raw in enumerate(text.split("\n"), 1):
        line = raw.strip()
        if (relative, line) in exempt:
            continue
        where = f"{relative}:{number}: {line}"
        calls = len(APT_CALL.findall(line))
        if not calls:
            continue
        bounds = APT_BOUND.findall(line)
        if len(bounds) != calls:
            misplaced = "".join(f"; {why}" for why in misplaced_forms(line))
            bad.append(f"{where} ({calls} apt call(s), {len(bounds)} in the bound form{misplaced})")
            continue
        low = [n for n in bounds if int(n) < MIN_APT_BOUND]
        if low:
            bad.append(f"{where} (a bound under {MIN_APT_BOUND} s: {low})")
        if line.endswith("\\"):
            bad.append(f"{where} (continues onto the next line, where an option could reopen the call)")
        reopens = reopening_word(APT_BOUND.sub(" ", line.removesuffix("\\")))
        if reopens:
            bad.append(f"{where} (outside the form, {reopens})")
    return sorted(bad, key=lambda hit: int(hit.split(":", 2)[1]))


def apt_stale(files: dict[str, str], exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The exemptions whose workflow no longer holds their whole line, exactly."""
    exempt = APT_EXEMPT if exempt is None else exempt
    lines = {name: {line.strip() for line in text.splitlines()} for name, text in files.items()}
    return [f"{name}: {line}" for name, line in exempt if line not in lines.get(name, set())]


class Census(NamedTuple):
    """Every job's steps from the raw text, `{job: [{"line", "dash", "keys", "runs": [{"line", "header", "body"}]}]}`
    ("dash" and "keys" the step's indents), and the lines of the file the census could not place, `(line, why)`."""

    steps: dict[str, list[dict]]
    refused: list[tuple[int, str]]


class Lexed(NamedTuple):
    """One line taken apart: its indent in spaces, whether it opens a list entry (`- `), the plain key it holds (None
    when it holds none), that key's value with its trailing comment removed (a `#` inside a quoted scalar or a flow
    collection's quoted string is content), the comment, the key's header as written (a `run:` header is compared
    whole), the stripped text, and the fault that stops the lexing (a tab in the indentation)."""

    indent: int
    dash: bool
    key: str | None
    value: str
    comment: str
    header: str
    text: str
    fault: str | None


def workflow_text(path: Path) -> str:
    """A workflow's text as the census reads it: UTF-8, with a byte that is not UTF-8 kept as the lone surrogate
    `surrogateescape` gives it (U+DC80 to U+DCFF), so the character scan refuses it by line and column where a
    strict decoder would raise with neither."""
    return path.read_bytes().decode("utf-8", "surrogateescape")


def character_class(char: str) -> str:
    """The REFUSED_CHARACTERS class of a refused character, with its code point (a byte that is not UTF-8: the byte)."""
    name = next(name for name, pattern in CHARACTER_CLASS.items() if pattern.fullmatch(char))
    if name == "a byte that is not UTF-8":
        return f"{name} (0x{ord(char) - 0xDC00:02X})"
    return f"{name} (U+{ord(char):04X})"


def refused_characters(text: str) -> list[tuple[int, str]]:
    """Every character of `text` outside the census's character set, in file order, as `(line, why)` with the
    column named; the line is counted at LF alone and both count from 1."""
    faults = []
    for match in REFUSED_CHARACTER.finditer(text):
        start = match.start()
        line = text.count("\n", 0, start) + 1
        column = start - text.rfind("\n", 0, start)
        faults.append((line, f"{character_class(match.group())} at column {column}; {CHARACTER_SET}"))
    return faults


def node_end(header: str) -> int | None:
    """The index after the close of the quoted scalar or flow collection that opens `header`, or None when the line
    ends first. A `"` scalar escapes with a backslash and a `'` scalar doubles its quote; inside a flow collection a
    quote opens a string after an opener, a `,`, a `:`, a `?` (round 8: the key indicator, which PyYAML takes in a
    flow collection whatever follows it) or a blank, and a `#` after a blank opens a comment that runs to the line's
    end (YAML 7.3, 7.4)."""
    quote: str | None = None
    depth = 0
    index = 0
    while index < len(header):
        char = header[index]
        if quote:
            if quote == '"' and char == "\\":
                index += 2
                continue
            if char == quote:
                if quote == "'" and header[index + 1 : index + 2] == "'":
                    index += 2
                    continue
                quote = None
                if depth == 0:
                    return index + 1
        elif char in "\"'" and (index == 0 or header[index - 1] in " \t,[{:?"):
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
            if depth == 0:
                return index + 1
        elif char == "#" and header[index - 1] in " \t":
            return None
        index += 1
    return None


def split_header(header: str) -> tuple[str, str]:
    """A key's header as its value and its trailing comment. A `#` that opens the header or follows a blank starts
    the comment, except inside the quoted scalar or flow collection the header opens, where it is content; when that
    node never closes on the line the whole header is the value, and value_form names it."""
    start = 0
    if header and header[0] in "\"'[{":
        end = node_end(header)
        if end is None:
            return header, ""
        start = end
    comment = COMMENT.search(header, start)
    if comment is None:
        return header, ""
    return header[: comment.start()].rstrip(WHITE), header[comment.start() :].strip(WHITE)


def lex(line: str) -> Lexed:
    text = line.strip(WHITE)
    indent = len(line) - len(line.lstrip(" "))
    fault = "a tab in the indentation" if text and "\t" in line[: len(line) - len(line.lstrip(WHITE))] else None
    dash = text.startswith("- ")
    entry = text[2:].lstrip(" ") if dash else text
    match = KEY_LINE.fullmatch(entry)
    header = (match.group(2) or "").strip(WHITE) if match else ""
    value, note = split_header(header)
    return Lexed(indent, dash, match.group(1) if match else None, value, note, header, text, fault)


def value_form(value: str) -> str:
    """The form a value's first character gives it: one of READ_VALUE_FORMS, the name of a refused indicator, or a
    quoted scalar or flow collection the line does not complete (it never closes, or text follows its close): YAML
    reads the lines after such a value as the rest of it, the readers as the next keys."""
    if not value:
        return "empty"
    first = value[0]
    if first in "\"'[{":
        form = "a quoted scalar" if first in "\"'" else "a flow collection"
        end = node_end(value)
        if end is None:
            return f"{form} that does not close on its line"
        if value[end:].strip(WHITE):
            return f"text after {form}"
        return form
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

    The whole document is read. A line at the margin is a plain key the workflow schema allows (TOP_KEYS), its value
    in a read form and complete on its line; `jobs:` is bare and appears once; a line indented under any other
    top-level key is that key's value (a nested block, a list, a continuation). Inside `jobs:` the shape is derived,
    never assumed: the first key after `jobs:` sets the jobs' indent, the first key under a job its keys', the first
    dash under `steps:` the dashes', and each dash line its own keys' (the column after `- `). Any other line inside
    `jobs:` is the value of the key above it when it is indented past that key (a `run: |` body, a nested `with:`
    mapping; a `run:` there is not a key) and is refused by line otherwise. Every line the shape places is lexed and
    held to the grammar (KEY_LINE, JOB_KEYS, STEP_KEYS, the value forms) or refused by line with its construct named.
    A `run:` key's body is every following line indented past the step's keys, blank lines included, up to the first
    that is not; so the body is collected in any scalar form, whatever the reader makes of the form. Before any of
    this, every character is held to the census's character set: a file with one outside it (REFUSED_CHARACTERS)
    is refused by line and column, and no line of it is read."""
    faults = refused_characters(text)
    if faults:
        return Census({}, faults)
    steps_by_job: dict[str, list[dict]] = {}
    refused: list[tuple[int, str]] = []
    steps: list[dict] = []
    top_keys: set[str] = set()
    job_keys: set[str] = set()
    step_keys: set[str] = set()
    jobs_at = keys_at = dash_at = value_at = step = body = body_at = None
    in_steps = inside = False  # `inside`: between the `jobs:` line and the next line at the margin
    for number, line in enumerate(text.split("\n"), 1):
        lexed = lex(line)
        if inside and value_at is not None and (not lexed.text or lexed.indent > value_at):
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
            if lexed.key is None or lexed.dash:
                stop = f"; {TOP_STOP}" if inside else ""
                refused.append((number, f"{lexed.text} (not {KEY_FORM}{stop})"))
            elif lexed.key != "jobs":
                problem = key_problem(lexed, TOP_KEYS, top_keys, "workflow")
                if problem:
                    refused.append((number, f"{lexed.text} ({problem})"))
            elif "jobs" in top_keys:
                refused.append((number, f"{lexed.text} (a second jobs: key)"))
            else:
                top_keys.add("jobs")
                if line != "jobs:":
                    refused.append((number, f"{lexed.text} ({JOBS_LINE})"))
                inside = True
                continue
            inside = False
            value_at = None
            continue
        if not inside:
            if not top_keys:
                refused.append((number, f"{lexed.text} (indented {lexed.indent} before any top-level key)"))
            continue  # the value of the top-level key above it
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
    if "jobs" not in top_keys:
        refused.append((1, f"no `jobs:` line in the file ({JOBS_LINE})"))
    for steps in steps_by_job.values():
        for run in (run for step in steps for run in step["runs"]):
            while run["body"] and not run["body"][-1].strip(WHITE):
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
    if refused_characters(text):
        return problems  # the file has no lines, so the reader is held to nothing of it
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


class Parser:
    """PyYAML in a child the uv idiom starts, one per document (CI's interpreter has no YAML parser, and uv is set up
    before the unit tests run, as regime.yml's tests rely on). The document goes in as one JSON string; the child
    answers with one JSON line, PyYAML's document or its refusal, and exits. The exit status is read before the
    answer: a child that exits nonzero, answers nothing, answers more than once or answers in another shape is a
    failure naming the status, the output and stderr, never a document. Answers are cached by document text."""

    command = [*UV_PYYAML, "-c", PARSER]
    answers: dict[str, tuple[object, str | None]] = {}

    @classmethod
    def read(cls, text: str) -> tuple[object, str | None]:
        """PyYAML's reading of `text`: (document, None), or (None, why) when PyYAML refuses the document or JSON
        cannot carry it (a key that is not a scalar). RuntimeError when the child did not answer in good standing."""
        if text in cls.answers:
            return cls.answers[text]
        run = subprocess.run(
            cls.command, input=json.dumps(text), capture_output=True, text=True, encoding="utf-8", check=False
        )
        if run.returncode != 0:
            raise RuntimeError(
                f"the PyYAML child exited with status {run.returncode}; its output {run.stdout!r} is not read; "
                f"stderr: {run.stderr.strip()}"
            )
        lines = run.stdout.splitlines()
        if len(lines) != 1:
            raise RuntimeError(
                f"the PyYAML child exited with status 0 and {len(lines)} line(s) of output instead of one answer: "
                f"{run.stdout!r}; stderr: {run.stderr.strip()}"
            )
        try:
            reply = json.loads(lines[0])
        except ValueError as error:
            raise RuntimeError(
                f"the PyYAML child answered with a line that is not JSON ({error}): {lines[0]!r}"
            ) from None
        if not isinstance(reply, dict) or set(reply) not in ({"document"}, {"error"}):
            raise RuntimeError(f"the PyYAML child answered in another shape than a document or an error: {lines[0]!r}")
        cls.answers[text] = (reply.get("document"), reply.get("error"))
        return cls.answers[text]


def census_run(step: dict) -> list[str] | None:
    """A text step's `run:` as PyYAML would hold it, by stripped non-blank line: a one-line value is the line as
    written (PyYAML unquotes a quoted one, so the two part there), a block header is not content, the body lines
    are; None when the step has no `run:` key."""
    if not step["runs"]:
        return None
    lines = []
    for run in step["runs"]:
        if run["header"][:1] not in ("|", ">"):
            lines.append(run["header"])
        lines += run["body"]
    return [line.strip() for line in lines if line.strip()]


def summary(lines: list[str] | None) -> str:
    """A run body for a message: its line count and first line, or `no run:`."""
    if lines is None:
        return "no run:"
    if not lines:
        return "an empty run:"
    return f"{len(lines)} line(s) from {lines[0][:60]!r}"


def parser_problems(name: str, text: str, parsed: dict[str, list[dict]] | None = None) -> list[str]:
    """Where PyYAML's reading of one workflow differs from the census and the reader, by `file:line`, job and step.

    The job set and order, each job's step count, and each step's `run:` body (as the census holds it) are PyYAML's
    or named; where the reader's steps are given, each step the reader reaches has PyYAML's name and timeout-minutes
    too, since the step check attaches both from the reader. A job whose step count differs is named with the first
    step where the two readings part. A document PyYAML refuses, or one whose `jobs:` is not a mapping of jobs with
    step lists, is named as a whole."""
    document, error = Parser.read(text)
    if error is not None:
        return [f"{name}: PyYAML refuses the file ({error}); {PARSER_GATE}"]
    found = text_steps(text)
    read_jobs = document.get("jobs") if isinstance(document, dict) else None
    if not isinstance(read_jobs, dict):
        return [f"{name}: the text holds jobs {list(found)}, PyYAML reads no jobs mapping; {PARSER_GATE}"]
    problems = []
    if list(read_jobs) != list(found):
        problems.append(f"{name}: the text holds jobs {list(found)}, PyYAML reads {list(read_jobs)}; {PARSER_GATE}")
    for job, steps in found.items():
        if job not in read_jobs:
            continue  # named above
        read = read_jobs[job].get("steps") if isinstance(read_jobs[job], dict) else None
        if not isinstance(read, list):
            problems.append(f"{name}: {job}: PyYAML reads no step list; {PARSER_GATE}")
            continue
        reader = iter(parsed.get(job, [])) if parsed is not None else None
        differing: list[tuple[str, str]] = []  # (the step, what differs)
        for index, (step, got) in enumerate(zip(steps, read)):
            where = f"{name}:{step['line']}: {job}: step {index}"
            mine = next(reader, {}) if reader is not None and reader_reaches(step) else {}
            if not isinstance(got, dict):
                differing.append((where, f"is not a mapping to PyYAML ({got!r})"))
                continue
            written = census_run(step)
            parsed_run = (
                [line.strip() for line in str(got["run"]).splitlines() if line.strip()] if "run" in got else None
            )
            if written != parsed_run:
                differing.append((where, f"runs {summary(written)} in the text, {summary(parsed_run)} to PyYAML"))
            for key in ("name", "timeout-minutes"):
                if mine and mine.get(key) != (str(got[key]) if key in got else None):
                    differing.append((where, f"has {key} {mine.get(key)!r} to the reader, {got.get(key)!r} to PyYAML"))
        if len(read) != len(steps):
            part = f", parting at {differing[0][0]}" if differing else ""
            problems.append(
                f"{name}: {job}: {len(steps)} steps in the text, {len(read)} to PyYAML{part}; {PARSER_GATE}"
            )
        else:
            problems.extend(f"{where} {what}; {PARSER_GATE}" for where, what in differing)
    return problems


def step_minutes(apt_seconds: int, rest: int) -> int:
    """The step bound the formula gives: the ceiling in minutes of the apt bounds (each N plus the kill delay) and the
    measured rest of the step, plus one minute."""
    return math.ceil((apt_seconds + rest) / 60) + 1


def bounded_steps() -> list[dict]:
    """The three apt steps in the bound form with the timeout-minutes the formula gives for STEP_REST_BUDGET."""
    form = "/usr/bin/timeout --kill-after=10 {} sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 {}"
    return [
        {
            "name": "Install apt packages",
            "timeout-minutes": "8",
            "run": f"{form.format(180, 'update')}\n{form.format(180, 'install -y bats curl')}",
        },
        {
            "name": "Install apt packages for the unit tests",
            "timeout-minutes": "7",
            "run": f"{form.format(150, 'update')}\n{form.format(150, 'install -y jq zsh')}",
        },
        {
            "name": "Install apt packages for Codecov",
            "timeout-minutes": "4",
            "run": form.format(150, "install -y jq curl"),
        },
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
    out), once the census has shown the reader returned every `run:` and PyYAML (round 8, parser_problems) read the
    same jobs, steps, run bodies, names and timeout-minutes; the reader's structure only attaches the name and
    timeout-minutes, its steps matched in order to the text steps its rule reaches (the census has named the
    others). Steps are keyed by (workflow, job, index), the name carried for the message, so no step replaces
    another; a name used twice in one job is refused on its own, since STEP_REST_BUDGET refers to steps by name.
    Then every apt step has a budget row and the timeout-minutes the formula gives, and every budget row has its
    step. A file with a refused character has no lines: the census names the characters and nothing else of the
    file is read, and the budget rows are held against the steps of the set only once every file in it was read."""
    problems, found, unread = [], {}, []
    for workflow, text in texts.items():
        by_job = parsed.get(workflow, {})
        problems.extend(census_problems(workflow, text, by_job))
        if refused_characters(text):
            unread.append(workflow)
            continue  # the file has no lines: PyYAML is not asked about it either
        problems.extend(parser_problems(workflow, text, by_job))
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
    if not unread:
        problems.extend(
            f"budget row {name!r} has no step that runs apt" for name in STEP_REST_BUDGET if name not in names
        )
    for where, (name, apt_seconds, step) in found.items():
        if name not in STEP_REST_BUDGET:
            problems.append(f"{where} runs apt with no STEP_REST_BUDGET row")
        elif "timeout-minutes" not in step:
            problems.append(f"{where} has no timeout-minutes")
        else:
            expected = step_minutes(apt_seconds, STEP_REST_BUDGET[name])
            if int(step["timeout-minutes"]) != expected:
                problems.append(f"{where} has timeout-minutes {step['timeout-minutes']}, the formula gives {expected}")
    return problems


def workflow_problems(paths: list[Path]) -> list[str]:
    """The census and step problems of whole workflow files, as the tests see the real ones. The reader is asked
    about a file only once the character scan passed it: a file with no lines has nothing it could read."""
    texts = {path.name: workflow_text(path) for path in paths}
    parsed = {path.name: parsed_steps(path) for path in paths if not refused_characters(texts[path.name])}
    return apt_step_problems(texts, parsed)


def workflow_texts() -> dict[str, str]:
    return {path.name: workflow_text(path) for path in sorted(WORKFLOWS.glob("*.y*ml"))}


# --- Rounds 10 to 14: the run bodies are read from shfmt's syntax tree ---------------------------------------------
#
# Audit of 15c4afa8 (round 10): rounds 2, 8 and 9 each tightened the text rule above, and the auditor found two more
# ways past it (`ci.run:`, `time\` and a newline). A regex over shell text cannot bound what bash executes; shfmt's
# tree, under the U105 contract (scripts/ci/shfmt_json_contract.py, run first; the pinned shfmt, never a skip), reads
# it as bash does: backslash-newlines joined, quotes resolved into parts, every command a CallExpr with its words.
# Rounds 10 and 11 read the apt steps as steps that also did other work, with a table of the commands that can give a
# word another meaning (eval, source, alias, the wrappers that hand a command on), and the audits of 4d09be21 and
# 21d53583 each found the next member (`'eval'`, `builtin eval`, a `source` after a `cd`). Round 12 (decisions row
# 2026-10-29T12:16Z) writes that premise down as wrong: a rule cannot enumerate what else an apt step may do, so the
# apt steps do nothing else. The rule over a step's tree:
#   (a) An apt step is a step whose body holds an apt token (APT_TOKEN on every `Lit` and quoted value and on the
#       known text of every word, so `'apt'`, `"apt-get"` and `ap""t-get` count) or the form's first word
#       TIMEOUT_PATH anywhere, or whose text names apt (APT_CALL). Every top-level statement of an apt step is
#       exactly the bound form: a CallExpr with no assignment, in a statement with no redirection, `!`, `&` or
#       coprocess, whose words are bare literals (one `Lit` part over KNOWN_CHARACTERS) equal to FORM_WORDS, a
#       decimal N of at least MIN_APT_BOUND, the verb, and after `install` exactly `-y` and one or more package
#       names. Any other statement (a FuncDecl, an IfClause, a BinaryCmd, a `cd`, a `source`, an `echo`, anything)
#       is a problem naming its line and node. No table of commands is needed, since nothing but the form is
#       accepted.
#   (b) In every step, apt or not, a command word with no known text is a problem naming the step and line: the
#       first word of every CallExpr, and the word a `sudo` hands on (sudo is how a step reaches root, which apt
#       needs to touch the image; SUDO_FLAGS and SUDO_VALUED are the options read before its command, any other
#       option refused, so no option's value stands where the command is read). A word's text is known (word_text,
#       round 13) when every part is a bare `Lit` over KNOWN_CHARACTERS, a plain single-quoted string, or double
#       quotes around literals (any character there) and such strings, or when the whole word is one bare `Lit` part
#       spelling one of TEST_BUILTIN_WORDS (test_builtin_word, round 14: the exemption is the word's, never a part's);
#       a bare literal holding a glob character, a brace, a tilde, `$`, a backquote, a backslash or whitespace, an
#       expansion, a substitution, an ANSI-C or locale string has none, and nothing is decoded (the audit of
#       e161f194 ran `sudo /usr/bin/a[p]t-get update` past round 12, which read a bare literal as its text; the audit
#       of 0fec5c91 ran `sudo "/usr/bin/"["a"]"pt-get" update` past round 13, which exempted `[` and `]` as parts).
#       UNKNOWN_COMMAND_EXEMPT, keyed by workflow, step name and the exact line, names the lines where that word is a
#       path from a variable the workflow set from a literal tool name and checked, each with its reason; a row must
#       match a line. A comment ending in a backslash is a problem in every step too: shfmt joins the next line into
#       the comment and bash runs it, so the tree would not show that line.
#   (c) An apt token outside the form is a problem wherever it stands, since the step holding it is an apt step
#       under (a). A bare literal among a call's words that bash expands (unknown_characters) is a possible apt token
#       too (`a[p]t-get`, `apt-g?t`, `ap*t` spell apt once bash has read them), named by line, so such a step is held
#       to (a) as well; a case pattern or a `[[ ]]` operand is matched, never run, and is not one; a `[` or `]` part
#       of a word with other parts (`"ap"[t]"-get"`) is one, only the whole test word is not (round 14). An apt step's
#       `if:` is one of APT_STEP_IFS, whole (the macOS rows have no apt and no /usr/bin/timeout; the audit of
#       e161f194 appended `|| true` past a substring check), and the tree holds as many form statements as the text
#       rule counted bound forms.
# tests/unit/test_shfmt_json_contract.py extracts every field and literal this walk reads and holds TABLE to them.
APT_TOKEN = re.compile(APT_CALL.pattern + r"|(?<=/)apt\Z|\Aapt\Z")
FORM_WORDS = (
    TIMEOUT_PATH,
    "--kill-after=10",
    None,
    "sudo",
    "apt-get",
    "-o",
    "Acquire::http::Timeout=15",
    "-o",
    "Acquire::Retries=3",
)
FORM_N = "a decimal of at least 120"  # the third word, where FORM_WORDS holds None
VERBS = ("update", "install")
PACKAGE = re.compile(r"[a-z0-9][a-z0-9.+-]*\Z")  # Debian policy 5.6.1; after `install`, `-y` is the one option allowed
POSITION = frozenset({"Offset", "Line", "Col"})
STATEMENT_FIELDS = ("Type", "Cmd", "Semicolon", "Comments")  # Redirs, Negated, Background and Coprocess are not
CALL_FIELDS = ("Type", "Args")  # Assigns is not
COMMENT_JOIN = "shfmt joins the next line to the command before the comment, bash runs that line on its own"
DOUBLE_QUOTE_ESCAPES = '$`"\\\n'  # bash 3.1.2.3: the characters a backslash quotes inside double quotes
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")  # a `NAME=value` word sudo takes before the command
# Bash reads a bare literal over this set as written; a glob character, a brace, a tilde, `$`, a backquote, a
# backslash or whitespace is expanded or stripped first, so such a word's text is not known here and nothing is
# decoded (the rule scripts/ci/producer-status-check.sh adopted in U112 round 4). Inside double quotes bash expands
# none of them, so the set does not apply there.
KNOWN_CHARACTERS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./:=+@%,")
# The words of the test builtin `[ ... ]` that bash reads as written although a character is outside the set: an
# unmatched `[` and a lone `]` are no pattern to bash (pathname expansion needs the pair) and `!` expands nothing in
# a script (history expansion is off), so every `if [ ! "$x" != y ]` of the workflows runs as spelled. The exemption
# is a whole word's (test_builtin_word, round 14): exactly one bare `Lit` part spelling one of them. A `[` or `]`
# part of a word with other parts is half of a pair bash completes once the quotes are gone: the audit of 0fec5c91
# ran `sudo "/usr/bin/"["a"]"pt-get" update`, five parts bash expands to `/usr/bin/apt-get`, past a per-part read.
TEST_BUILTIN_WORDS = frozenset({"[", "]", "!", "!="})
UNKNOWN_COMMAND = (
    "a command word must have a known text: a bare literal over the known characters, single-quoted or "
    "double-quoted literals, nothing bash expands"
)
EXPANDED_WORD = "a bare literal bash expands among a call's words is a possible apt token, and its step an apt step"
SUDO = "sudo"
SUDO_FLAGS = frozenset({"-E", "-H", "-n"})  # take no value
SUDO_VALUED = frozenset({"-u", "-g"})  # take the next word
APT_STEP = "an apt step holds nothing but bound apt calls, one exact form per statement"
# The if: expressions an apt step carries, whole: the one the two apt steps of test.yaml's test job share, and the
# Codecov step's, which adds the upload step's conditions. The set is the data, not a pattern: an expression with
# anything added, removed or reordered is refused (the audit of e161f194 appended `|| true` past a substring check).
APT_STEP_IFS = (
    "${{ steps.decide.outputs.should_test == 'true' && runner.os == 'Linux' }}",
    "${{ steps.decide.outputs.should_test == 'true' && runner.os == 'Linux' && matrix.os == 'ubuntu-24.04' && !endsWith(github.actor, '[bot]') }}",
)
APT_STEP_GUARD = (
    f"an apt step's if: is one of the {len(APT_STEP_IFS)} APT_STEP_IFS expressions, whole; the macOS rows have no "
    f"apt and no {TIMEOUT_PATH}"
)
NODE_TABLE = "the pinned shfmt's JSON does not match the pinned node table"
TREE_COUNT = "every apt call the tree holds is one the text counted as the form, and the reverse"
# (workflow file, step name, the whole stripped line, exactly) -> why its command word, a quoted path, may have no
# known text. In test.yaml each path comes from a variable the workflow set from a literal tool name (`mise which
# bun`, `command -v chezmoi`) and checked, and a test outside this unit pins the line's text, so the line is not
# rewritten; the other three lines are in workflows this unit does not own (brief SCOPE), each a path the step built
# from a literal. A row must match a line (test_an_unknown_command_exemption_needs_its_exact_step_and_line).
UNKNOWN_COMMAND_EXEMPT: dict[tuple[str, str, str], str] = {
    ("test.yaml", "Run the omp TypeScript tests", '"${bun_bin}" --version'): (
        "bun_bin is `mise which bun` from the copied config; tests/unit/test_ci_workflows.py pins the step's bun lines"
    ),
    ("test.yaml", "Run the omp TypeScript tests", 'PATH="${bun_bin_dir}:${PATH}" "${bun_bin}" test "./${tests}"'): (
        "bun_bin is `mise which bun` from the copied config; tests/unit/test_ci_workflows.py pins this exact line"
    ),
    ("test.yaml", "Prepare public dotfiles fixture", 'CI=true HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \\'): (
        "FILES_TEST_CHEZMOI is `command -v chezmoi` as Install tools checked and exported it (absolute, outside mise "
        "shims, at the release's version); tests/unit/test_files_fixture.py counts the two lines that run it"
    ),
    ("test.yaml", "Prepare public dotfiles fixture", 'HOME="${files_test_home}" "${FILES_TEST_CHEZMOI}" \\'): (
        "FILES_TEST_CHEZMOI is `command -v chezmoi` as Install tools checked and exported it (absolute, outside mise "
        "shims, at the release's version); tests/unit/test_files_fixture.py counts the two lines that run it"
    ),
    ("macos.yaml", "Run benchmark", "$(chezmoi source-path)/../scripts/run_benchmark.sh > result.json"): (
        "the checkout's benchmark script by chezmoi's source path, after `brew install chezmoi`; macos.yaml is not "
        "this unit's (brief SCOPE)"
    ),
    ("remote.yaml", "Install chezmoi for the scratch apply", '| (cd "${RUNNER_TEMP}" && "${sha256_check[@]}")'): (
        "the checksum array set from literals two lines above (test.yaml spelled the same lines out in round 11); "
        "remote.yaml is not this unit's (brief SCOPE)"
    ),
    (
        "remote.yaml",
        "Install chezmoi for the scratch apply",
        '"${RUNNER_TEMP}/chezmoi-bin/chezmoi" --version | grep -F "v${chezmoi_version}"',
    ): "the release binary the line above extracted into the runner's temp directory; remote.yaml is not this unit's (brief SCOPE)",
}


class Walked(NamedTuple):
    """What one walk over a step's tree found: the apt tokens that make it an apt step (empty for another step), the
    `(line, what)` of every statement of an apt step that is not the form and of every comment that hides a line,
    the `(line, what)` of every command word with no known text (exemptable by step and line), and how many form
    statements it holds."""

    tokens: tuple[str, ...]
    problems: list[tuple[object, str]]
    unknown: list[tuple[object, str]]
    apt_calls: int


@functools.lru_cache(maxsize=None)
def contract_trees() -> dict[str, dict]:
    """The contract's fixture trees, once per process: the pinned shfmt on PATH parses the fixtures and their trees
    match TABLE, else a RuntimeError naming the first difference (a missing or unpinned shfmt fails, never skips)."""
    try:
        return contract.verified_trees()
    except contract.ContractError as error:
        raise RuntimeError(f"{NODE_TABLE}: {error}") from None


def script_tree(text: str, source: str) -> dict:
    """The pinned shfmt's tree of a script, after the contract held; ContractError when shfmt refuses the text. A
    tree that lists statements none of which the walk can read (a renamed field) is a failure, never an absence."""
    contract_trees()
    tree = contract.parse(text.encode("utf-8"), source)
    listed = len(tree.get("Stmts") or [])
    if listed and not any("Cmd" in node for node, _ in tree_nodes(tree)):
        raise RuntimeError(f"the tree of {source} lists {listed} statement(s) but the walk saw none")
    return tree


def tree_nodes(root: object) -> Iterator[tuple[dict, dict | None]]:
    """Every JSON object at or below root with the object that holds it (lists are transparent), iteratively."""
    todo: list[tuple[object, dict | None]] = [(root, None)]
    while todo:
        node, parent = todo.pop()
        if isinstance(node, dict):
            yield node, parent
            todo.extend((child, node) for child in reversed(list(node.values())))
        elif isinstance(node, list):
            todo.extend((child, parent) for child in reversed(node))


def line_of(node: dict) -> object:
    """The line of the node's position in its script, or `?`."""
    pos = node.get("Pos") or {}
    return pos.get("Line", "?")


def unescaped(value: str) -> str:
    """A double-quoted literal's value without the backslashes bash removes when it reads the word: before one of
    DOUBLE_QUOTE_ESCAPES. A backslash-newline is already joined by shfmt (the `time\\` and newline case of round
    10)."""
    out: list[str] = []
    index = 0
    while index < len(value):
        if value[index] == "\\" and index + 1 < len(value) and value[index + 1] in DOUBLE_QUOTE_ESCAPES:
            index += 1
        out.append(value[index])
        index += 1
    return "".join(out)


def unknown_characters(value: str) -> str:
    """The characters of a bare literal outside KNOWN_CHARACTERS, each once in order; empty when bash reads the
    literal as written. No value is exempt here: TEST_BUILTIN_WORDS applies to a whole word (test_builtin_word)."""
    return "".join(dict.fromkeys(char for char in value if char not in KNOWN_CHARACTERS))


def test_builtin_word(word: dict) -> str | None:
    """The text of a word that is exactly one bare `Lit` part spelling one of TEST_BUILTIN_WORDS, which bash reads as
    written; None for any other word. The exemption is the whole word's, never a part's (round 14, audit of
    0fec5c91): in `"/usr/bin/"["a"]"pt-get"` and `"ap"[t]"-get"` the bare `[` and `]` stand among quoted parts, and
    bash expands the word to `/usr/bin/apt-get` and `apt-get`; every bare part of such a word is held to
    KNOWN_CHARACTERS, so the word is a glob, not a text, and nothing is decoded."""
    parts = word.get("Parts") or []
    if len(parts) != 1 or parts[0].get("Type") != "Lit":
        return None
    value = str(parts[0].get("Value") or "")
    return value if value in TEST_BUILTIN_WORDS else None


def word_text(word: dict, in_double_quotes: bool = False) -> str | None:
    """The known text of a word: every part a bare `Lit` bash reads as written (unknown_characters empty), a plain
    single-quoted string, or double quotes around literals (any character there, their escapes removed) and such
    strings (`apt-get`, `'apt-get'`, `"apt-get"`, `ap""t-get` and `"a[p]t"` are texts), or the whole word one of
    TEST_BUILTIN_WORDS (test_builtin_word; `[` is a text, `"ap"[t]"-get"` is none). None for any other word, whose
    text exists only when it runs: a bare literal with a glob character, a brace, a tilde, `$`, a backquote, a
    backslash or whitespace, an expansion, a substitution, arithmetic, a process substitution, an ANSI-C `$'...'` or
    a locale `$"..."` string (shfmt's Dollar). Nothing is decoded."""
    if not in_double_quotes and test_builtin_word(word) is not None:
        return test_builtin_word(word)
    text = ""
    for part in word.get("Parts") or []:
        kind = part.get("Type")
        if kind == "Lit":
            value = str(part.get("Value") or "")
            if in_double_quotes:
                text += unescaped(value)
            elif not unknown_characters(value):
                text += value
            else:
                return None
        elif kind == "SglQuoted" and not part.get("Dollar"):
            text += str(part.get("Value") or "")  # shfmt writes no Value for ''
        elif kind == "DblQuoted" and not part.get("Dollar"):
            inner = word_text(part, True)
            if inner is None:
                return None
            text += inner
        else:
            return None
    return text


def bare_text(word: dict) -> str | None:
    """The text of a word written as the form's words are, one bare `Lit` part bash reads as written (over
    KNOWN_CHARACTERS, or one of TEST_BUILTIN_WORDS as the whole word); None otherwise."""
    parts = word.get("Parts") or []
    if len(parts) != 1 or parts[0].get("Type") != "Lit":
        return None
    value = str(parts[0].get("Value") or "")
    return None if unknown_characters(value) and value not in TEST_BUILTIN_WORDS else value


def lits(node: dict) -> list[str]:
    """Every text at or below node that could name apt: each `Lit` and `SglQuoted` value as shfmt holds it (inside
    quotes, expansions and substitutions too, `$'...'` included), and the known text of every word (word_text), so
    `'apt'`, `"apt-get"` and `ap""t-get` are read as what they are."""
    found: list[str] = []
    for part, _ in tree_nodes(node):
        if part.get("Type") in ("Lit", "SglQuoted"):
            found.append(str(part.get("Value") or ""))
        elif contract.kind(part) == "Word":
            text = word_text(part)
            if text is not None:
                found.append(text)
    return found


def expansion(word: dict) -> tuple[str, str]:
    """The bare text of a word (its `Lit` parts joined as written, shfmt splits `a[p]t` into `a` and `[p]t`; the
    other parts left out, so `"ap"[t]"-get"` is spelled `[t]`) and the characters of it bash expands, each once in
    order; the second empty when bash reads every bare literal of the word as written, or the whole word is one of
    TEST_BUILTIN_WORDS (test_builtin_word; a `[` or `]` part of a longer word counts, round 14)."""
    values = [str(part.get("Value") or "") for part in word.get("Parts") or [] if part.get("Type") == "Lit"]
    if test_builtin_word(word) is not None:
        return "".join(values), ""
    outside = "".join(dict.fromkeys(char for value in values for char in unknown_characters(value)))
    return "".join(values), outside


def shown_characters(outside: str) -> str:
    """The characters for a message, each in backquotes, comma-separated."""
    return ", ".join(f"`{char}`" for char in outside)


def expanded_words(tree: dict) -> list[tuple[object, str, str]]:
    """`(line, spelled, characters)` of every word among a call's words holding a bare literal bash expands before
    the call runs (expansion): `a[p]t-get`, `apt-g?t`, `ap*t`, `ap\\t-get`, `{apt,x}-get`, `~+/apt` may spell apt
    once read. A case pattern, a `[[ ]]` operand, a `for` list or a redirect target is matched, tested or opened,
    never run, so a glob there is not one."""
    found: list[tuple[object, str, str]] = []
    for node, _ in tree_nodes(tree):
        if node.get("Type") == "CallExpr":
            for word in node.get("Args") or []:
                spelled, outside = expansion(word)
                if outside:
                    found.append((line_of(node), spelled, outside))
    return found


def apt_tokens(tree: dict) -> tuple[str, ...]:
    """The tokens that make a step an apt step, sorted: every APT_TOKEN match in the texts lits() finds, TIMEOUT_PATH
    where one of them holds the form's first word, and every spelled word expanded_words() finds."""
    found: set[str] = set()
    for value in lits(tree):
        found.update(match.group() for match in APT_TOKEN.finditer(value))
        if TIMEOUT_PATH in value:
            found.add(TIMEOUT_PATH)
    found.update(spelled for _, spelled, _ in expanded_words(tree))
    return tuple(sorted(found))


def names_apt(script: str) -> bool:
    """Whether the text of a step body names apt outside its comment lines (the text rule's token), so a step whose
    tree shows no token (a comment after a command) is still held to the apt step's rule."""
    return (
        APT_CALL.search("\n".join(line for line in script.splitlines() if not line.lstrip().startswith("#")))
        is not None
    )


def describe(word: dict) -> str:
    """A word with no known text, or not written bare, by the kinds of its parts: the parts inside double quotes in
    parentheses, a `$'...'` or `$"..."` string by its Dollar; a word holding a bare literal bash expands adds its
    spelling and the characters bash expands."""
    kinds = []
    for part in word.get("Parts") or []:
        kind = str(part.get("Type", "untyped"))
        if kind == "DblQuoted":
            kind += f"({', '.join(str(inner.get('Type', 'untyped')) for inner in part.get('Parts') or [])})"
        if part.get("Type") in ("SglQuoted", "DblQuoted") and part.get("Dollar"):
            kind += " with Dollar"
        kinds.append(kind)
    text = f"a word of {', '.join(kinds)} part(s)" if kinds else "an empty word"
    spelled, outside = expansion(word)
    if outside:
        text += f" spelling `{spelled}`, which bash expands ({shown_characters(outside)})"
    return text


def shown(words: list[dict], texts: list[str | None], position: int) -> str:
    """A word for a message: its known text, or its parts."""
    return describe(words[position]) if texts[position] is None else repr(texts[position])


def set_fields(node: dict, known: tuple[str, ...]) -> list[str]:
    """The fields of node that are set beyond the known ones and its positions (shfmt omits an empty or false one)."""
    return [
        key
        for key, value in node.items()
        if key not in known
        and value not in (None, False, 0, "", [])
        and not (isinstance(value, dict) and set(value) == POSITION)
    ]


def form_fault(words: list[dict]) -> str | None:
    """Why the words of a call are not the exact bound form, by position and text, or None when they are: the nine
    FORM_WORDS and the verb as bare literals, then nothing after `update`, and after `install` exactly `-y` and one
    or more package names, in that order."""
    texts = [bare_text(word) for word in words]
    for position, want in enumerate(FORM_WORDS):
        number = position + 1
        if position >= len(words):
            return f"has {len(words)} word(s); word {number} of the form is `{want or FORM_N}`"
        got = texts[position]
        if got is None:
            return f"word {number} is {describe(words[position])}, not the bare literal `{want or FORM_N}`"
        if want is None:
            if not got.isdigit() or int(got) < MIN_APT_BOUND:
                return f"word {number} `{got}` is not {FORM_N}"
        elif got != want:
            return f"word {number} is `{got}`, not `{want}`"
    verb_at = len(FORM_WORDS)
    if verb_at >= len(words):
        return f"has {len(words)} word(s); word {verb_at + 1} of the form is the verb `update` or `install`"
    verb = texts[verb_at]
    if verb not in VERBS:
        got = f"`{verb}`" if verb is not None else describe(words[verb_at])
        return f"word {verb_at + 1} is {got}, not the verb `update` or `install`"
    rest = list(range(verb_at + 1, len(words)))
    if verb == "update":
        if rest:
            return f"word {rest[0] + 1} {shown(words, texts, rest[0])} follows `update`, which takes none"
        return None
    if not rest:
        return f"has {len(words)} word(s); word {verb_at + 2} of the form is `-y`"
    if texts[rest[0]] != "-y":
        return f"word {rest[0] + 1} {shown(words, texts, rest[0])} after `install` is not `-y`"
    if len(rest) == 1:
        return f"has {len(words)} word(s); word {verb_at + 3} of the form is a package name"
    for position in rest[1:]:
        got = texts[position]
        if got is None or not PACKAGE.match(got):
            return f"word {position + 1} {shown(words, texts, position)} after `install -y` is not a package name"
    return None


def article(kind: object) -> str:
    """`an IfClause`, `a Block`: a node kind for a message."""
    name = str(kind)
    return f"an {name}" if name[:1] in "AEIOU" else f"a {name}"


def statement_fault(statement: dict) -> str | None:
    """Why one top-level statement of an apt step is not the bound form, naming its node, or None when it is."""
    call = statement.get("Cmd")
    if not isinstance(call, dict):
        return "a statement with no command"
    kind = call.get("Type")
    if kind == "FuncDecl":
        return f"a FuncDecl `{(call.get('Name') or {}).get('Value', '')}`"
    if kind == "BinaryCmd":
        return f"a BinaryCmd `{call.get('Op')}`"
    if kind != "CallExpr":
        return article(kind)
    for field in set_fields(statement, STATEMENT_FIELDS):
        return f"a CallExpr in a statement with {field}"
    for field in set_fields(call, CALL_FIELDS):
        return f"a CallExpr with {field}"
    fault = form_fault(call.get("Args") or [])
    return (
        None
        if fault is None
        else f"a CallExpr that {fault}"
        if fault.startswith("has")
        else f"a CallExpr whose {fault}"
    )


def sudo_fault(words: list[dict], texts: list[str | None], at: int) -> str | None:
    """Why the command the `sudo` at words[at] runs has no known text, or None when it has one or sudo stands alone:
    after sudo come its flags, its valued options with their values, and `NAME=value` words, then the command."""
    at += 1
    while at < len(words):
        text = texts[at]
        if text is None:
            return f"`sudo` followed by {describe(words[at])}, which has no known text, before its command word"
        if text in SUDO_VALUED:
            at += 1
            if at < len(words) and texts[at] is None:
                return f"`sudo {text}` with a value that is {describe(words[at])}, with no known text"
        elif text.startswith("-") and len(text) > 1 and text not in SUDO_FLAGS:
            return f"`sudo` with the option `{text}`, outside the options the rule reads for it"
        elif not (text in SUDO_FLAGS or ASSIGNMENT.match(text)):
            return None
        at += 1
    return None


def command_problems(words: list[dict], line: object) -> list[tuple[object, str]]:
    """The command words of one call that have no known text: its first word, and the word every `sudo` among its
    words hands on (sudo_fault). An argument of any other command is that command's: a word it reads, not one the
    shell runs."""
    if not words:
        return []  # an assignment alone runs nothing
    problems: list[tuple[object, str]] = []
    texts = [word_text(word) for word in words]
    if texts[0] is None:
        problems.append((line, f"{describe(words[0])} in command position: {UNKNOWN_COMMAND}"))
    for at, text in enumerate(texts):
        if text is not None and (text == SUDO or text.endswith("/" + SUDO)):
            why = sudo_fault(words, texts, at)
            if why is not None:
                problems.append((line, why))
    return problems


def walk(tree: dict, source: str, text_names_apt: bool = False) -> Walked:
    """One step body's tree under the round 12 rule: an apt step (apt_tokens, or `text_names_apt` from the text)
    accepts only form statements at its top level, each named by line and node otherwise, and every bare literal
    bash expands among a call's words is named by line (round 13); every step is read for command words with no
    known text and for comments that hide the next line. `source` names the script in messages that have no
    line."""
    tokens = apt_tokens(tree)
    problems: list[tuple[object, str]] = []
    unknown: list[tuple[object, str]] = []
    apt_calls = 0
    if tokens or text_names_apt:
        for statement in tree.get("Stmts") or []:
            fault = statement_fault(statement)
            if fault is None:
                apt_calls += 1
            else:
                problems.append((line_of(statement), f"{fault}: {APT_STEP}"))
    problems.extend(
        (line, f"`{spelled}` holds {shown_characters(outside)}: {EXPANDED_WORD}")
        for line, spelled, outside in expanded_words(tree)
    )
    for node, _ in tree_nodes(tree):
        if "Hash" in node:
            if str(node.get("Text", "")).rstrip("\n").endswith("\\"):
                problems.append((line_of(node), f"a comment ending in a backslash: {COMMENT_JOIN}"))
        elif node.get("Type") == "CallExpr":
            unknown.extend(command_problems(node.get("Args") or [], line_of(node)))
    return Walked(tokens, problems, unknown, apt_calls)


def body_line(run: dict, line: object) -> object:
    """The workflow line of a script line: under a block header the body starts on the next line; a one-line run is
    its header's line."""
    if not isinstance(line, int):
        return "?"
    return run["line"] + line if run["header"].startswith("|") else run["line"]


def script_line(script: str, line: object) -> str:
    """The stripped text of a script line, for the exemption key; empty when the line is unknown."""
    lines = script.splitlines()
    return lines[line - 1].strip() if isinstance(line, int) and 0 < line <= len(lines) else ""


def tree_problems(name: str, text: str) -> list[str]:
    """Every refusal the tree rule makes over one workflow, by `file:line`, job and step: a `shell:` other than bash
    (the tree reads the runner's bash), a `${{` in a run body (GitHub expands it before bash reads the text), a body
    shfmt refuses, each statement of an apt step that is not the form, each bare literal bash expands among a call's
    words, each comment that hides a line, each command word with no known text in any step unless
    UNKNOWN_COMMAND_EXEMPT names its step and line, an apt step whose stripped `if:` is not one of APT_STEP_IFS
    whole, and a step whose tree holds another number of form statements than the text holds bound forms. The
    bodies are PyYAML's (Parser), the lines the census's; a file the census or the parser gate refuses is named
    there and not read here."""
    if refused_characters(text) or parser_problems(name, text):
        return []
    document, _ = Parser.read(text)
    found = text_steps(text)
    problems = []
    for job, body in document["jobs"].items():
        for index, step in enumerate(body["steps"]):
            if "run" not in step:
                continue
            text_step = found[job][index]
            runs = text_step["runs"]
            run = runs[0] if len(runs) == 1 else {"line": text_step["line"], "header": ""}
            label = step.get("name") or f"step {index}"
            where = f"{name}:{{}}: {job}: step {index} {label!r}"
            script = str(step["run"])
            shell = step.get("shell")
            if shell is not None and str(shell) != "bash":
                problems.append(
                    f"{where.format(text_step['line'])}: shell: {shell!r}: the tree reads the runner's bash"
                )
                continue
            if "${{" in script:
                at = next(number for number, line in enumerate(script.splitlines(), 1) if "${{" in line)
                problems.append(
                    f"{where.format(body_line(run, at))}: `${{{{` in the run body: GitHub expands it before bash reads the text"
                )
                continue
            try:
                walked = walk(script_tree(script, f"{name} {job} step {index}"), name, names_apt(script))
            except contract.ContractError as error:
                problems.append(f"{where.format(run['line'])}: {error}")
                continue
            problems.extend(f"{where.format(body_line(run, at))}: {what}" for at, what in walked.problems)
            problems.extend(
                f"{where.format(body_line(run, at))}: {what}"
                for at, what in walked.unknown
                if (name, label, script_line(script, at)) not in UNKNOWN_COMMAND_EXEMPT
            )
            if (walked.tokens or names_apt(script)) and str(step.get("if") or "").strip() not in APT_STEP_IFS:
                problems.append(f"{where.format(text_step['line'])}: if: {step.get('if')!r}: {APT_STEP_GUARD}")
            bounds = len(APT_BOUND.findall("\n".join(l for l in script.splitlines() if not l.lstrip().startswith("#"))))
            if walked.apt_calls != bounds:
                problems.append(
                    f"{where.format(run['line'])}: {walked.apt_calls} apt call(s) in the tree, {bounds} bound form(s) in the text; {TREE_COUNT}"
                )
    return problems


def unknown_exemption_stale(texts: dict[str, str]) -> list[str]:
    """The UNKNOWN_COMMAND_EXEMPT rows whose workflow, step and exact line `texts` does not hold (a file the parser
    gate refuses holds no step for this purpose)."""
    held: set[tuple[str, str, str]] = set()
    for name, text in texts.items():
        if refused_characters(text) or parser_problems(name, text):
            continue
        document, _ = Parser.read(text)
        for body in document["jobs"].values():
            for index, step in enumerate(body["steps"]):
                label = step.get("name") or f"step {index}"
                held.update((name, label, line.strip()) for line in str(step.get("run", "")).splitlines())
    return [f"{name}: {step}: {line}" for name, step, line in UNKNOWN_COMMAND_EXEMPT if (name, step, line) not in held]


def tree_main(argv: list[str]) -> int:
    """The tree rule over one shell file as a step body (tests/unit/test_shfmt_json_contract.py runs every walker so):
    0 clean, 1 with each refused node on stdout, 2 when the contract or the parse refuses, with the cause on stderr."""
    parser = argparse.ArgumentParser(description="the apt bound rule over one shell file, from shfmt's tree")
    parser.add_argument("--script", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        script = args.script.read_text()
        walked = walk(script_tree(script, str(args.script)), str(args.script), names_apt(script))
    except (contract.ContractError, RuntimeError, OSError) as error:
        print(f"apt-bound-tree: {error}", file=sys.stderr)
        return 2
    for line, what in walked.problems + walked.unknown:
        print(f"{args.script}:{line}: {what}")
    return 1 if walked.problems or walked.unknown else 0


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

    FORM = "/usr/bin/timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"
    BARE = "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"

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
            f"{self.BARE} update",
            "/usr/bin/timeout 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "/usr/bin/timeout --kill-after=0 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "/usr/bin/timeout --kill-after=10 0 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "/usr/bin/timeout --kill-after=10 60 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "/usr/bin/timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=0 -o Acquire::Retries=3 update",
            "/usr/bin/timeout --kill-after=10 180 sudo apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=15 update",
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
            f"ci_{self.BARE} update",
            f"my{self.BARE} update",
            f"./{self.BARE} update",
            f"/usr/local/bin/{self.BARE} update",
            f"sudo {self.FORM} update",
            f"ci.run: {self.FORM} update",
            'function timeout { shift 2; "$@"; }',
            'timeout() { shift 2; "$@"; }',
            '/usr/bin/timeout() { shift 2; "$@"; }',
            "alias timeout='command true'",
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

    def test_a_form_that_is_not_the_first_word_of_its_command_is_named_by_position(self) -> None:
        # Audit of ecde33b9: the form matched anywhere on a line, so `ci_timeout --kill-after=10 180 sudo apt-get
        # ...` (a function defined on the line above that drops the first two words) held the form as the tail of
        # another command's name. Audit of 15c4afa8: the `run:` start was not anchored, so `ci.run: timeout ...`
        # counted. The form counts only as the whole path that begins its command; every other position is named:
        # the longer word, the bare name, or the text the path follows.
        path = TIMEOUT_PATH
        for snippet, position in (
            (f"ci_{self.BARE} update", f"`timeout` at column 1 is the tail of the word 'ci_timeout', not `{path}`"),
            (f"my{self.BARE} update", f"`timeout` at column 1 is the tail of the word 'mytimeout', not `{path}`"),
            (f"./{self.BARE} update", f"`timeout` at column 1 is the tail of the word './timeout', not `{path}`"),
            (
                f"/usr/local/bin/{self.BARE} update",
                f"`timeout` at column 1 is the tail of the word '/usr/local/bin/timeout', not `{path}`",
            ),
            (f"x-{self.BARE} update", f"`timeout` at column 1 is the tail of the word 'x-timeout', not `{path}`"),
            (f"-{self.BARE} update", f"`timeout` at column 1 is the tail of the word '-timeout', not `{path}`"),
            (f"{self.BARE} update", f"`timeout` at column 1 is the bare name, not `{path}`"),
            (f"sudo {self.BARE} update", f"`timeout` at column 6 is the bare name, not `{path}`"),
            (f"sudo {self.FORM} update", "the form at column 6 follows 'sudo ', not a command start"),
            (f"env {self.FORM} update", "the form at column 5 follows 'env ', not a command start"),
            (f"true & {self.FORM} update", "the form at column 8 follows 'true & ', not a command start"),
            (f"echo {self.FORM} update", "the form at column 6 follows 'echo ', not a command start"),
            (f"A={self.FORM} update", "the form at column 3 follows 'A=', not a command start"),
            (f"pre-run: {self.FORM} update", "the form at column 10 follows 'pre-run: ', not a command start"),
            (f"ci.run: {self.FORM} update", "the form at column 9 follows 'ci.run: ', not a command start"),
            (f"true run: {self.FORM} update", "the form at column 11 follows 'true run: ', not a command start"),
            (f"x - {self.FORM} update", "the form at column 5 follows 'x - ', not a command start"),
        ):
            with self.subTest(snippet=snippet):
                bad = apt_violations("x.yaml", snippet + "\n", {})
                self.assertEqual(1, len(bad), bad)
                self.assertIn(f"(1 apt call(s), 0 in the bound form; {position}; {COMMAND_WORD})", bad[0])
        # The auditors' bodies: a definition line that is not a `timeout` definition runs no apt, and the call line
        # is refused on its own line, whether the function's name ends in `timeout` or in `run:`.
        for body, call in (
            (f'ci_timeout() {{ shift 2; "$@"; }}\nci_{self.BARE} update\n', f"ci_{self.BARE} update"),
            (f'ci.run:() {{ shift 3; "$@"; }}\nci.run: {self.FORM} update\n', f"ci.run: {self.FORM} update"),
        ):
            with self.subTest(body=body.splitlines()[0]):
                (hit,) = apt_violations("x.yaml", body, {})
                self.assertTrue(hit.startswith(f"x.yaml:2: {call} ("), hit)
        # Each command start in the closed set counts the form, with any whitespace between; a dash and a `run:` key
        # count only at the start of the line.
        for start in COMMAND_STARTS:
            for snippet in (f"true {start} {self.FORM} update", f"true {start}{self.FORM} update"):
                with self.subTest(start=start, snippet=snippet):
                    self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)
        for start in LINE_STARTS:
            for snippet in (f"{start}{self.FORM} update", f"  {start} {self.FORM} update"):
                with self.subTest(start=start, snippet=snippet):
                    self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)
        for snippet in (
            f"\t{self.FORM} update",
            f"run: |\u2028          {self.FORM} update",  # a YAML 1.1 line break, refused by the character scan
            f"( {self.FORM} update )",
            f"cat list | {self.FORM} install -y jq",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)

    def test_a_tree_rule_refusal_is_not_a_text_rule_pass(self) -> None:
        # Round 10: the text rule stays the superset the tree rule refines. These pass it and are refused by the
        # tree (TreeRuleTest), so the text rule alone is never the stop.
        for snippet in (
            f"{self.FORM} update && {self.FORM} install -y jq zsh",
            f"{self.FORM} update | cat",
            f"{self.FORM} update 2> /dev/null",
            f"{self.FORM} install -y jq $pkg",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)

    def test_a_timeout_redefinition_is_refused_by_line_with_its_reason(self) -> None:
        # A function or an alias named `timeout`, bare or by the form's path, anywhere in a workflow is refused on
        # its line, with the construct and its reason, whether or not that line runs apt; the names that only
        # contain `timeout` are not.
        spellings = {
            "a `function timeout` definition": (
                'function timeout { shift 2; "$@"; }',
                'function timeout() { shift 2; "$@"; }',
                "function\ttimeout {",
                "function /usr/bin/timeout { :; }",
            ),
            "a `timeout()` definition": (
                'timeout() { shift 2; "$@"; }',
                "timeout () {",
                "timeout ( ) { :; }",
                "true; timeout(){ :; }",
                "/usr/bin/timeout() { :; }",
            ),
            "an `alias timeout=`": (
                "alias timeout='command true'",
                "alias -- timeout=true",
                "alias ls=x timeout=y",
                "shopt -s expand_aliases; alias timeout=true",
            ),
        }
        self.assertEqual(set(APT_REDEFINITIONS), set(spellings))
        for construct, lines in spellings.items():
            why = APT_REDEFINITIONS[construct][1]
            for line in lines:
                with self.subTest(construct=construct, line=line):
                    bad = apt_violations("x.yaml", line + "\n", {})
                    self.assertEqual([f"x.yaml:1: {line} ({construct}: {why}; {REDEFINITION})"], bad)
                # The definition and the real form in one body: the definition's line alone is refused.
                body = f"{lines[0]}\n{self.FORM} update\n"
                (hit,) = apt_violations("x.yaml", body, {})
                self.assertTrue(hit.startswith(f"x.yaml:1: {lines[0]} ({construct}"), hit)
        for line in (
            'ci_timeout() { shift 2; "$@"; }',
            "function ci_timeout { :; }",
            "alias ci_timeout=true",
            "alias x=timeout",
            "echo timeout=5",
            "# GNU timeout cuts a call that prints nothing",
        ):
            with self.subTest(line=line):
                self.assertEqual([], apt_violations("x.yaml", line + "\n", {}), line)

    def test_a_definition_split_by_a_backslash_is_refused_on_its_first_line(self) -> None:
        # Audit of 15c4afa8: `time\` at the end of one line and `out() { shift 2; "$@"; }` on the next is one
        # `timeout` definition to bash, which joins a backslash-newline before it reads the words; a check of
        # physical lines saw neither half. The logical line is checked and named at its first physical line, with
        # the count of lines joined; the bare and the path spellings alike, and the real form after it stands.
        why = APT_REDEFINITIONS["a `timeout()` definition"][1]
        for first, second, joined in (
            ("time\\", 'out() { shift 2; "$@"; }', 'timeout() { shift 2; "$@"; }'),
            ("/usr/bin/time\\", 'out() { shift 2; "$@"; }', '/usr/bin/timeout() { shift 2; "$@"; }'),
            ("/usr/bin/timeout(\\", ") { :; }", "/usr/bin/timeout() { :; }"),
            ("function \\", "timeout { :; }", "function timeout { :; }"),
            ("time\\", "            out() { :; }", "timeout() { :; }"),  # the continuation at the block's indent
        ):
            with self.subTest(first=first):
                body = f"{first}\n{second}\n{self.FORM} update\n"
                bad = apt_violations("x.yaml", body, {})
                construct = (
                    "a `function timeout` definition" if first.startswith("function") else "a `timeout()` definition"
                )
                self.assertEqual(
                    [
                        f"x.yaml:1: {joined} ({construct}: {why}; {REDEFINITION}; joined from 2 lines ending in a backslash)"
                    ],
                    bad,
                )
        self.assertEqual([(1, 2, "ab"), (3, 1, "c"), (4, 1, "d\\")], logical_lines("a\\\nb\nc\nd\\"))

    def test_every_apt_call_in_every_workflow_is_the_form_in_the_tree_of_its_step(self) -> None:
        # Rounds 10 to 12: the real workflows, read from shfmt's tree under the contract. Every apt step holds
        # nothing but form statements under the Linux guard, every command word of every step has a known text or
        # an exemption row, and each tree holds as many form statements as its text holds bound forms. A walk that
        # found fewer calls than test.yaml's five would be a broken walk.
        problems, calls = [], 0
        for name, text in workflow_texts().items():
            with self.subTest(workflow=name):
                problems.extend(tree_problems(name, text))
                document, _ = Parser.read(text)
                for job in document["jobs"].values():
                    for step in job["steps"]:
                        if "run" not in step:
                            continue
                        script = str(step["run"])
                        try:
                            calls += walk(script_tree(script, name), name, names_apt(script)).apt_calls
                        except contract.ContractError:
                            pass  # a body shfmt refuses: tree_problems named it above
        self.assertEqual([], problems)
        self.assertGreaterEqual(calls, 5)

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


class TreeRuleTest(unittest.TestCase):
    """Rounds 10 to 14: the run bodies are read from shfmt's tree under the U105 contract. Round 12 (audit of
    21d53583, decisions row 2026-10-29T12:16Z): an apt step holds nothing but the form, so the auditors' constructs
    (`builtin eval`, a `source` after a `cd`, an ANSI-C `apt` in a step no detector counted) and every other
    statement are refused by line and node with no table of commands; a command word with no known text is refused
    in every step; the real workflows pass; a parser or contract that cannot be read is a failure, never an
    absence. Round 13 (audit of e161f194): a bare literal is a text only over KNOWN_CHARACTERS, so the auditor's
    `sudo /usr/bin/a[p]t-get update` is refused as an unknown word, as a possible apt token and as a non-form
    statement; an apt step's `if:` is one of APT_STEP_IFS whole, so `|| true` appended is refused. Round 14 (audit
    of 0fec5c91): the test builtin's exemption is a whole word's, so `sudo "/usr/bin/"["a"]"pt-get" update`, whose
    bare `[` and `]` parts stand among quoted parts, is refused the same three ways."""

    FORM = "/usr/bin/timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"
    NAME = "Install apt packages"
    GUARD = APT_STEP_IFS[0]
    STEP = "x.yaml:{}: test: step 0 'Install apt packages': "

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="apt-tree-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.temp)], check=False))

    def body(self, script: str) -> list[tuple[object, str]]:
        """Every refusal the walk makes over one step body, in line order: the statements of an apt step that are
        not the form, the comments that hide a line, the command words with no known text."""
        walked = walk(script_tree(script, "x"), "x", names_apt(script))
        return sorted(
            walked.problems + walked.unknown, key=lambda found: (isinstance(found[0], str), found[0], found[1])
        )

    def step(self, script: str, **keys: str) -> tuple[str, int, int]:
        """A workflow with one guarded step `Install apt packages` holding `script` as its `run: |`: (text, the
        body's first line, the step's dash line)."""
        step = {"name": self.NAME, "timeout-minutes": "8", "if": self.GUARD, **keys, "run": script}
        text = render({"test": [step]})
        found = text_steps(text)["test"][0]
        return text, found["runs"][0]["line"] + 1, found["line"]

    def test_an_apt_step_holds_nothing_but_the_form(self) -> None:
        # The auditors' constructs of rounds 10 to 12 and every other statement an apt step could hold, each refused
        # by its line and node; no table of commands is consulted, so `builtin`, `eval`, `source` and `cd` are
        # refused as what they are: statements that are not the form.
        form = self.FORM
        tail = form[len(TIMEOUT_PATH) + 1 :]
        off = f": {APT_STEP}"
        first = "a CallExpr whose word 1 is `{}`, not `/usr/bin/timeout`" + off
        quoted = "a CallExpr whose word 1 is a word of {} part(s), not the bare literal `/usr/bin/timeout`" + off
        unknown = f"a word of DblQuoted(ParamExp) part(s) in command position: {UNKNOWN_COMMAND}"
        expanded = "`{}` holds {}: " + EXPANDED_WORD
        handed = "`sudo` followed by {}, which has no known text, before its command word"
        command = "{} in command position: " + UNKNOWN_COMMAND
        expands = (
            "a CallExpr whose word 1 is a word of {} part(s) spelling `{}`, which bash expands ({}), not the bare "
            "literal `/usr/bin/timeout`" + off
        )
        for case, script, expected in (
            (
                "the auditor's builtin eval",
                f"builtin eval '/usr/bin/time''out() {{ shift 2; \"$@\"; }}'\n{form} update\n",
                [(1, first.format("builtin"))],
            ),
            (
                "the auditor's quoted eval",
                f"'eval' '/usr/bin/time''out() {{ shift 2; \"$@\"; }}'\n{form} update\n",
                [(1, quoted.format("SglQuoted"))],
            ),
            (
                "the auditor's cd then source",
                f'cd "$RUNNER_TEMP"\nsource scripts/lib/github-release.sh\n{form} update\n',
                [(1, first.format("cd")), (2, first.format("source"))],
            ),
            ("the auditor's quoted apt", "sudo 'apt' update\n", [(1, first.format("sudo"))]),
            ("a second statement", f"{form} update\necho ok\n", [(2, first.format("echo"))]),
            ("a statement before the form", f"echo ok\n{form} update\n", [(1, first.format("echo"))]),
            (
                "a function",
                f'timeout() {{ shift 2; "$@"; }}\n{form} update\n',
                [(1, f"a FuncDecl `timeout`{off}"), (1, unknown)],
            ),
            (
                "a path-named function",
                f"/usr/bin/timeout() {{ :; }}\n{form} update\n",
                [(1, f"a FuncDecl `/usr/bin/timeout`{off}")],
            ),
            (
                "the round 10 auditor's ci.run: function",
                f'ci.run:() {{ shift 3; "$@"; }}\nci.run: {form} update\n',
                [(1, f"a FuncDecl `ci.run:`{off}"), (1, unknown), (2, first.format("ci.run:"))],
            ),
            (
                "time, a backslash and a newline",
                f'time\\\nout() {{ shift 2; "$@"; }}\n{form} update\n',
                [(1, f"a FuncDecl `timeout`{off}"), (2, unknown)],
            ),
            (
                "an if around the form",
                f'if [[ "${{OS}}" == ubuntu-* ]]; then\n  {form} update\nfi\n',
                [(1, f"an IfClause{off}")],
            ),
            ("a block", f"{{ {form} update; }}\n", [(1, f"a Block{off}")]),
            ("a subshell", f"( {form} update )\n", [(1, f"a Subshell{off}")]),
            ("a loop", f"for i in 1; do {form} update; done\n", [(1, f"a ForClause{off}")]),
            ("a case", f"case x in x) {form} update ;; esac\n", [(1, f"a CaseClause{off}")]),
            ("a pipeline", f"{form} update | cat\n", [(1, f"a BinaryCmd `|`{off}")]),
            ("a stderr pipeline", f"{form} update |& cat\n", [(1, f"a BinaryCmd `|&`{off}")]),
            ("two forms joined by &&", f"{form} update && {form} install -y jq\n", [(1, f"a BinaryCmd `&&`{off}")]),
            ("a redirection", f"{form} update 2> /dev/null\n", [(1, f"a CallExpr in a statement with Redirs{off}")]),
            ("a negation", f"! {form} update\n", [(1, f"a CallExpr in a statement with Negated{off}")]),
            ("a background job", f"{form} update &\n", [(1, f"a CallExpr in a statement with Background{off}")]),
            ("an assignment before the word", f"A=1 {form} update\n", [(1, f"a CallExpr with Assigns{off}")]),
            ("an assignment holding apt", 'cmd="sudo apt-get update"\n', [(1, f"a CallExpr with Assigns{off}")]),
            ("apt in a substitution", 'x="$(sudo apt-get update)"\n', [(1, f"a CallExpr with Assigns{off}")]),
            (
                "eval of a variable holding apt",
                'cmd="sudo apt-get update"\neval "$cmd"\n',
                [(1, f"a CallExpr with Assigns{off}"), (2, first.format("eval"))],
            ),
            ("exec", f"exec {form} update\n", [(1, first.format("exec"))]),
            (
                "alias, hash, enable, trap and source",
                "alias timeout=true\nhash -p /tmp/x timeout\nenable -f /tmp/x.so timeout\n"
                f"trap 'sudo apt-get update' RETURN\nsource /etc/hosts\n{form} update\n",
                [
                    (number, first.format(word))
                    for number, word in enumerate(("alias", "hash", "enable", "trap", "source"), 1)
                ],
            ),
            (
                "PATH before a bare timeout",
                f"PATH=/tmp/x:$PATH\n{form.replace('/usr/bin/', '')} update\n",
                [(1, f"a CallExpr with Assigns{off}"), (2, first.format("timeout"))],
            ),
            (
                "a comment ending in a backslash",
                f"echo x # c \\\n{form} update\n",
                [(1, f"a comment ending in a backslash: {COMMENT_JOIN}"), (1, first.format("echo"))],
            ),
            (
                "a heredoc holding the form",
                f"cat << EOF\n{form} update\nEOF\n",
                [(1, f"a CallExpr in a statement with Redirs{off}")],
            ),
            ("apt in a quoted word", 'echo "apt-get update"\n', [(1, first.format("echo"))]),
            ("apt by its path", "sudo /usr/bin/apt install x\n", [(1, first.format("sudo"))]),
            ("a split spelling of apt-get", 'ap""t-get update\n', [(1, quoted.format("Lit, DblQuoted(), Lit"))]),
            (
                "the form's path around another command",
                f"{TIMEOUT_PATH} 5 sleep 1\n",
                [(1, f"a CallExpr whose word 2 is `5`, not `--kill-after=10`{off}")],
            ),
            (
                "a second -o",
                f"{form} -o Acquire::Retries=0 update\n",
                [(1, f"a CallExpr whose word 10 is `-o`, not the verb `update` or `install`{off}")],
            ),
            (
                "an option after install",
                f"{form} install -y -o Debug::NoLocking=true jq\n",
                [(1, f"a CallExpr whose word 12 '-o' after `install -y` is not a package name{off}")],
            ),
            (
                "a word after update",
                f"{form} update jq\n",
                [(1, f"a CallExpr whose word 11 'jq' follows `update`, which takes none{off}")],
            ),
            (
                "an expansion as a package",
                f"{form} install -y jq $pkg\n",
                [
                    (
                        1,
                        f"a CallExpr whose word 13 a word of ParamExp part(s) after `install -y` is not a package name{off}",
                    )
                ],
            ),
            (
                "install without -y",
                f"{form} install jq zsh\n",
                [(1, f"a CallExpr whose word 11 'jq' after `install` is not `-y`{off}")],
            ),
            (
                "-yq",
                f"{form} install -yq jq\n",
                [(1, f"a CallExpr whose word 11 '-yq' after `install` is not `-y`{off}")],
            ),
            (
                "-y and no package",
                f"{form} install -y\n",
                [(1, f"a CallExpr that has 11 word(s); word 12 of the form is a package name{off}")],
            ),
            (
                "-y twice",
                f"{form} install -y -y jq\n",
                [(1, f"a CallExpr whose word 12 '-y' after `install -y` is not a package name{off}")],
            ),
            (
                "an option after the packages",
                f"{form} install -y jq --fix-missing\n",
                [(1, f"a CallExpr whose word 13 '--fix-missing' after `install -y` is not a package name{off}")],
            ),
            (
                "no verb",
                f"{form}\n",
                [(1, f"a CallExpr that has 9 word(s); word 10 of the form is the verb `update` or `install`{off}")],
            ),
            ("the whole form in one quoted word", f'"{form}" update\n', [(1, quoted.format("DblQuoted(Lit)"))]),
            ("the path single-quoted", f"'{TIMEOUT_PATH}' {tail} update\n", [(1, quoted.format("SglQuoted"))]),
            ("the path double-quoted", f'"{TIMEOUT_PATH}" {tail} update\n', [(1, quoted.format("DblQuoted(Lit)"))]),
            (
                "a quoted verb",
                f"{form} 'update'\n",
                [
                    (
                        1,
                        f"a CallExpr whose word 10 is a word of SglQuoted part(s), not the verb `update` or `install`{off}",
                    )
                ],
            ),
            (
                "an ANSI-C verb",
                f"{form} $'update'\n",
                [
                    (
                        1,
                        f"a CallExpr whose word 10 is a word of SglQuoted with Dollar part(s), not the verb `update` or `install`{off}",
                    )
                ],
            ),
            (
                "a backslash in the path",
                f"{form.replace('timeout', 'time\\out')} update\n",
                [
                    (1, expands.format("Lit", "/usr/bin/time\\out", "`\\`")),
                    (1, expanded.format("/usr/bin/time\\out", "`\\`")),
                    (
                        1,
                        command.format(
                            "a word of Lit part(s) spelling `/usr/bin/time\\out`, which bash expands (`\\`)"
                        ),
                    ),
                ],
            ),
            # Round 13 (audit of e161f194): a bare literal bash expands is read as no text, named as a possible apt
            # token, and the step is an apt step; in command position or after sudo it is refused there too.
            (
                "the auditor's glob spelling of apt-get",
                "sudo /usr/bin/a[p]t-get update\n",
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("/usr/bin/a[p]t-get", "`[`, `]`")),
                    (
                        1,
                        handed.format(
                            "a word of Lit, Lit part(s) spelling `/usr/bin/a[p]t-get`, which bash expands (`[`, `]`)"
                        ),
                    ),
                ],
            ),
            (
                "a ? in apt-get",
                "sudo apt-g?t update\n",
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("apt-g?t", "`?`")),
                    (1, handed.format("a word of Lit part(s) spelling `apt-g?t`, which bash expands (`?`)")),
                ],
            ),
            (
                "a * in apt",
                "sudo ap*t update\n",
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("ap*t", "`*`")),
                    (1, handed.format("a word of Lit part(s) spelling `ap*t`, which bash expands (`*`)")),
                ],
            ),
            (
                "a glob handed to env, which runs its arguments",
                "env a[p]t-get update\n",
                [(1, first.format("env")), (1, expanded.format("a[p]t-get", "`[`, `]`"))],
            ),
            (
                "a brace spelling and a tilde path as the command",
                "ap{t,x}-get update\n~+/apt-get update\n",
                [
                    (1, expands.format("Lit", "ap{t,x}-get", "`{`, `}`")),
                    (1, expanded.format("ap{t,x}-get", "`{`, `}`")),
                    (1, command.format("a word of Lit part(s) spelling `ap{t,x}-get`, which bash expands (`{`, `}`)")),
                    (2, expands.format("Lit", "~+/apt-get", "`~`")),
                    (2, expanded.format("~+/apt-get", "`~`")),
                    (2, command.format("a word of Lit part(s) spelling `~+/apt-get`, which bash expands (`~`)")),
                ],
            ),
            (
                "a glob as an argument of echo",
                "echo *\n",
                [(1, first.format("echo")), (1, expanded.format("*", "`*`"))],
            ),
            # Round 14 (audit of 0fec5c91): the test builtin's words are exempt as whole words only; a bare `[`, `]`
            # or `?` part of a word with quoted parts is a glob, named by its bare parts joined, nothing decoded.
            (
                "the auditor's bracket glob among quoted parts",
                'sudo "/usr/bin/"["a"]"pt-get" update\n',
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("[]", "`[`, `]`")),
                    (
                        1,
                        handed.format(
                            "a word of DblQuoted(Lit), Lit, DblQuoted(Lit), Lit, DblQuoted(Lit) part(s) spelling "
                            "`[]`, which bash expands (`[`, `]`)"
                        ),
                    ),
                ],
            ),
            (
                "a bracket glob between quoted parts",
                'sudo "ap"[t]"-get" update\n',
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("[t]", "`[`, `]`")),
                    (
                        1,
                        handed.format(
                            "a word of DblQuoted(Lit), Lit, DblQuoted(Lit) part(s) spelling `[t]`, which bash "
                            "expands (`[`, `]`)"
                        ),
                    ),
                ],
            ),
            (
                "a ? after a quoted part",
                'sudo apt"-"g?t update\n',
                [
                    (1, first.format("sudo")),
                    (1, expanded.format("aptg?t", "`?`")),
                    (
                        1,
                        handed.format(
                            "a word of Lit, DblQuoted(Lit), Lit part(s) spelling `aptg?t`, which bash expands (`?`)"
                        ),
                    ),
                ],
            ),
            (
                "apt-get fully quoted: a known text that names apt, no glob part",
                'sudo "/usr/bin/apt-get" update\n',
                [(1, first.format("sudo"))],
            ),
            (
                "a bound under 120",
                f"{form.replace('180', '60')} update\n",
                [(1, f"a CallExpr whose word 3 `60` is not {FORM_N}{off}")],
            ),
            (
                "a bound that is not a number",
                f"{form.replace('180', '$N')} update\n",
                [(1, f"a CallExpr whose word 3 is a word of ParamExp part(s), not the bare literal `{FORM_N}`{off}")],
            ),
        ):
            with self.subTest(case=case):
                self.assertEqual(sorted(expected), self.body(script), case)

    def test_the_form_and_the_real_apt_steps_pass(self) -> None:
        form = self.FORM
        for case, script, calls in (
            ("update", f"{form} update\n", 1),
            ("install", f"{form} install -y bats curl iproute2 parallel ruby\n", 1),
            ("a semicolon", f"{form} update;\n", 1),
            ("two calls", f"{form} update\n{form} install -y jq\n", 2),
            ("a comment above", f"# the index is fetched again\n{form} update\n", 1),
            ("a comment after", f"{form} update # once\n", 1),
            ("other words, in a step that runs no apt", "echo apt-mirrors.txt and drop-azure-apt-mirror.py\n", 0),
        ):
            with self.subTest(case=case):
                self.assertEqual([], self.body(script), case)
                self.assertEqual(calls, walk(script_tree(script, "x"), "x", names_apt(script)).apt_calls)
        # The apt steps of test.yaml, as PyYAML returns them: every statement the form, as many as the lines, each
        # under the Linux guard.
        document, _ = Parser.read(workflow_text(WORKFLOWS / "test.yaml"))
        steps = {step.get("name"): step for step in document["jobs"]["test"]["steps"]}
        for name in STEP_REST_BUDGET:
            with self.subTest(step=name):
                script = str(steps[name]["run"])
                walked = walk(script_tree(script, name), name, names_apt(script))
                self.assertEqual(
                    ([], [], len(script.splitlines())), (walked.problems, walked.unknown, walked.apt_calls)
                )
                self.assertIn(str(steps[name]["if"]).strip(), APT_STEP_IFS)

    def test_a_command_word_with_no_known_text_is_refused_in_every_step(self) -> None:
        # Rule (b), in steps that run no apt: the first word of every call and the word a `sudo` hands on must have a
        # known text; an argument of any other command is that command's. The round 11 auditor's `sudo $'\x61pt'
        # update`, in a step no detector counted, is refused here before anything decodes it.
        unknown = f"in command position: {UNKNOWN_COMMAND}"
        handed = "`sudo` followed by {}, which has no known text, before its command word"
        param = "a word of DblQuoted(ParamExp) part(s)"
        for case, script, expected in (
            ("an expansion as the command", '"$cmd" --version\n', [(1, f"{param} {unknown}")]),
            ("a bare expansion as the command", "$cmd --version\n", [(1, f"a word of ParamExp part(s) {unknown}")]),
            (
                "the auditor's ANSI-C apt after sudo",
                "sudo $'\\x61pt' update\n",
                [(1, handed.format("a word of SglQuoted with Dollar part(s)"))],
            ),
            ("an expansion handed on by sudo", 'sudo "$cmd" update\n', [(1, handed.format(param))]),
            ("sudo by its path", '/usr/bin/sudo "$cmd" update\n', [(1, handed.format(param))]),
            ("sudo after another word", 'env -i sudo "$cmd"\n', [(1, handed.format(param))]),
            (
                "an expansion as the value of sudo -u",
                'sudo -u "$user" make x\n',
                [(1, "`sudo -u` with a value that is a word of DblQuoted(ParamExp) part(s), with no known text")],
            ),
            (
                "an option of sudo outside its row",
                "sudo -s make x\n",
                [(1, "`sudo` with the option `-s`, outside the options the rule reads for it")],
            ),
            (
                "a locale string as the command",
                '$"make" x\n',
                [(1, f"a word of DblQuoted(Lit) with Dollar part(s) {unknown}")],
            ),
            ("an array as the command in a subshell", '(cd "$dir" && "${check[@]}")\n', [(1, f"{param} {unknown}")]),
            ("an expansion run inside a function", 'f() {\n  "$@"\n}\n', [(2, f"{param} {unknown}")]),
            ("an expansion run inside a substitution", 'x="$("$cmd" -v)"\n', [(1, f"{param} {unknown}")]),
            (
                "a comment ending in a backslash",
                "echo x # c \\\necho y\n",
                [(1, f"a comment ending in a backslash: {COMMENT_JOIN}")],
            ),
        ):
            with self.subTest(case=case):
                self.assertEqual(sorted(expected), self.body(script), case)
        # What a step that runs no apt may do: a literal command word in any quoting form with any arguments, sudo
        # handing on a literal through its options, a function, a trap, a source, a PATH set on the line.
        for case, script in (
            (
                "sudo handing on a command with expansion arguments",
                'sudo install -m 0755 "${RUNNER_TEMP}/chezmoi" /usr/local/bin/chezmoi\n',
            ),
            ("sudo handing an array to unshare", 'sudo unshare --net -- "${smoke[@]}" || smoke_failed\n'),
            ("sudo with its options", "sudo -n -E -u root -g root HOME=/root make x\n"),
            ("sudo alone", "sudo -n\n"),
            ("command -v", "command -v jq > /dev/null 2>&1 || brew install jq\n"),
            ("env, nice and nohup", 'env -i FOO=1 nice -n 5 nohup make "$target"\n'),
            ("quoted and split command words", '\'make\' x\n"make" y\nma""ke z\n'),
            (
                "a function and a case",
                'skippable() {\n  case "$1" in\n    *) return 1 ;;\n  esac\n}\nskippable "${path}" || exit 1\n',
            ),
            ("a PATH set on the line before a literal command", 'PATH="${claude_bin_dir}:${PATH}" claude --version\n'),
            ("a trap and a source", "trap 'rm -f x' EXIT\nsource scripts/lib/github-release.sh\n"),
            ("an expansion as an argument", 'echo "${OS} is not supported" >&2\n'),
            (
                "the test builtin's words",
                'if [ -n "${x}" ] && [ ! -s f ] && [ "${y}" != z ]; then echo yes; fi\n',
            ),
            ("the test builtin's words as whole words, and a [[ ]] negation (round 14)", "[ -f x ]\n[[ ! -f x ]]\n"),
            (
                "a case pattern, a [[ operand and a for list, matched or listed, never run",
                'case "${OS}" in macos-*) : ;; *) : ;; esac\n[[ "${OS}" == ubuntu-* ]] || true\nfor f in *.md; do echo "$f"; done\n',
            ),
        ):
            with self.subTest(case=case):
                self.assertEqual([], self.body(script), case)
        # word_text over the closed set: a bare literal with a character outside it has no text, nothing is decoded;
        # the test builtin's words and a double-quoted glob are texts.
        for value in ("ap\\ t-get", "a[p]t-get", "apt-g?t", "ap*t", "ap{t,x}-get", "~+/apt", "$", "`", "apt\t"):
            self.assertIsNone(word_text({"Parts": [{"Type": "Lit", "Value": value}]}), value)
        for value in ("apt-get", "/usr/bin/timeout", "--kill-after=10", "Acquire::http::Timeout=15", "a,b@c%d+e_f"):
            self.assertEqual(value, word_text({"Parts": [{"Type": "Lit", "Value": value}]}), value)
        for value in TEST_BUILTIN_WORDS:
            self.assertEqual(value, word_text({"Parts": [{"Type": "Lit", "Value": value}]}), value)
        # Round 14: the exemption is a whole word's; `[`, `]` or `!` as a part of a word with other parts is a glob.
        quoted = {"Type": "DblQuoted", "Parts": [{"Type": "Lit", "Value": "a"}]}
        for parts in (
            [quoted, {"Type": "Lit", "Value": "["}, quoted, {"Type": "Lit", "Value": "]"}, quoted],
            [quoted, {"Type": "Lit", "Value": "[t]"}, quoted],
            [{"Type": "Lit", "Value": "["}, {"Type": "Lit", "Value": "]"}],
            [{"Type": "Lit", "Value": "!"}, quoted],
        ):
            self.assertIsNone(word_text({"Parts": parts}), parts)
            self.assertIsNone(bare_text({"Parts": parts}), parts)
            self.assertTrue(expansion({"Parts": parts})[1], parts)
        for value in TEST_BUILTIN_WORDS:
            self.assertEqual(value, bare_text({"Parts": [{"Type": "Lit", "Value": value}]}), value)
            self.assertEqual((value, ""), expansion({"Parts": [{"Type": "Lit", "Value": value}]}), value)
        self.assertEqual(
            "a[p]t", word_text({"Parts": [{"Type": "DblQuoted", "Parts": [{"Type": "Lit", "Value": "a[p]t"}]}]})
        )
        self.assertEqual(("/usr/bin/a[p]t-get",), apt_tokens(script_tree("sudo /usr/bin/a[p]t-get update\n", "x")))
        self.assertEqual(("[]",), apt_tokens(script_tree('sudo "/usr/bin/"["a"]"pt-get" update\n', "x")))
        self.assertEqual(("[t]",), apt_tokens(script_tree('sudo "ap"[t]"-get" update\n', "x")))
        self.assertEqual((), apt_tokens(script_tree("[ -f x ]\n[[ ! -f x ]]\n", "x")))
        self.assertEqual((), apt_tokens(script_tree("case x in *) : ;; esac\n[[ x == a* ]]\n[ ! x != y ]\n", "x")))
        self.assertEqual(
            'a"$b', word_text({"Parts": [{"Type": "DblQuoted", "Parts": [{"Type": "Lit", "Value": 'a\\"\\$b'}]}]})
        )
        self.assertEqual("", word_text({"Parts": [{"Type": "SglQuoted"}]}))

    def test_an_unknown_command_exemption_needs_its_exact_step_and_line(self) -> None:
        # A row applies to one step name and the whole stripped line, exactly; a row with no such line is stale.
        line = '"${bun_bin}" --version'
        table = {("x.yaml", "Tools", line): "bun_bin is `mise which bun`"}
        step = {"name": "Tools", "run": f"bun_bin=x\n{line}\n"}
        text = render({"test": [step]})
        at = text_steps(text)["test"][0]["runs"][0]["line"] + 2
        refused = f"x.yaml:{at}: test: step 0 'Tools': a word of DblQuoted(ParamExp) part(s) in command position: {UNKNOWN_COMMAND}"
        with mock.patch.object(sys.modules[__name__], "UNKNOWN_COMMAND_EXEMPT", table):
            self.assertEqual([], tree_problems("x.yaml", text))
            self.assertEqual([], unknown_exemption_stale({"x.yaml": text}))
            other = render({"test": [{**step, "name": "Other"}]})
            self.assertEqual([refused.replace("'Tools'", "'Other'")], tree_problems("x.yaml", other))
            self.assertEqual([f"x.yaml: Tools: {line}"], unknown_exemption_stale({"x.yaml": other}))
            longer = render({"test": [{**step, "run": f"bun_bin=x\n{line} --help\n"}]})
            self.assertEqual([refused], tree_problems("x.yaml", longer))
        with mock.patch.object(sys.modules[__name__], "UNKNOWN_COMMAND_EXEMPT", {}):
            self.assertEqual([refused], tree_problems("x.yaml", text))
        # The real table: seven rows, each the line of a real step, and the real workflows pass with it alone.
        self.assertEqual(7, len(UNKNOWN_COMMAND_EXEMPT))
        self.assertEqual([], unknown_exemption_stale(workflow_texts()))

    def test_the_auditors_mutations_are_refused_by_line_in_the_workflow(self) -> None:
        form = self.FORM
        off = f": {APT_STEP}"
        with self.subTest(case="builtin eval above the calls (audit of 21d53583)"):
            text, first, _ = self.step(f"builtin eval '/usr/bin/time''out() {{ shift 2; \"$@\"; }}'\n{form} update\n")
            self.assertEqual(
                [self.STEP.format(first) + f"a CallExpr whose word 1 is `builtin`, not `/usr/bin/timeout`{off}"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="cd into RUNNER_TEMP, then source a repository path (audit of 21d53583)"):
            text, first, _ = self.step(f'cd "$RUNNER_TEMP"\nsource scripts/lib/github-release.sh\n{form} update\n')
            self.assertEqual(
                [
                    self.STEP.format(first) + f"a CallExpr whose word 1 is `cd`, not `/usr/bin/timeout`{off}",
                    self.STEP.format(first + 1) + f"a CallExpr whose word 1 is `source`, not `/usr/bin/timeout`{off}",
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="a new step running sudo $'\\x61pt' update (audit of 21d53583)"):
            text = render({"test": [{"name": "Added", "run": "sudo $'\\x61pt' update\n"}]})
            first = text_steps(text)["test"][0]["runs"][0]["line"] + 1
            self.assertEqual(
                [
                    f"x.yaml:{first}: test: step 0 'Added': `sudo` followed by a word of SglQuoted with Dollar part(s), "
                    "which has no known text, before its command word"
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="a second statement in an apt step"):
            text, first, _ = self.step(f"{form} update\necho ok\n")
            self.assertEqual(
                [self.STEP.format(first + 1) + f"a CallExpr whose word 1 is `echo`, not `/usr/bin/timeout`{off}"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="an apt step without the if: guard"):
            text = render({"test": [{"name": self.NAME, "timeout-minutes": "8", "run": f"{form} update\n"}]})
            dash = text_steps(text)["test"][0]["line"]
            self.assertEqual([self.STEP.format(dash) + f"if: None: {APT_STEP_GUARD}"], tree_problems("x.yaml", text))
            text = render(
                {"test": [{"name": self.NAME, "if": "${{ matrix.os == 'ubuntu-24.04' }}", "run": f"{form} update\n"}]}
            )
            self.assertEqual(
                [self.STEP.format(dash) + f"if: \"${{{{ matrix.os == 'ubuntu-24.04' }}}}\": {APT_STEP_GUARD}"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="the guard with anything added, or another expression (audit of e161f194)"):
            for guard in (
                f"{self.GUARD} || true",
                "${{ runner.os == 'Linux' }}",
                "${{ true && steps.decide.outputs.should_test == 'true' && runner.os == 'Linux' }}",
                self.GUARD.replace(" }}", "  }}"),
                APT_STEP_IFS[1].replace(" && !endsWith(github.actor, '[bot]')", ""),
            ):
                text, _, dash = self.step(f"{form} update\n", **{"if": guard})
                self.assertEqual(
                    [self.STEP.format(dash) + f"if: {guard!r}: {APT_STEP_GUARD}"], tree_problems("x.yaml", text), guard
                )
            for guard in APT_STEP_IFS:
                text, _, _ = self.step(f"{form} update\n", **{"if": guard})
                self.assertEqual([], tree_problems("x.yaml", text), guard)
        with self.subTest(case="a new step running sudo /usr/bin/a[p]t-get update (audit of e161f194)"):
            text = render({"test": [{"name": "Added", "run": "sudo /usr/bin/a[p]t-get update\n"}]})
            found = text_steps(text)["test"][0]
            first, dash = found["runs"][0]["line"] + 1, found["line"]
            at = "x.yaml:{}: test: step 0 'Added': "
            self.assertEqual(
                [
                    at.format(first) + f"a CallExpr whose word 1 is `sudo`, not `/usr/bin/timeout`{off}",
                    at.format(first) + f"`/usr/bin/a[p]t-get` holds `[`, `]`: {EXPANDED_WORD}",
                    at.format(first)
                    + "`sudo` followed by a word of Lit, Lit part(s) spelling `/usr/bin/a[p]t-get`, which bash expands "
                    "(`[`, `]`), which has no known text, before its command word",
                    at.format(dash) + f"if: None: {APT_STEP_GUARD}",
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case='a new step running sudo "/usr/bin/"["a"]"pt-get" update (audit of 0fec5c91)'):
            text = render({"test": [{"name": "Added", "run": 'sudo "/usr/bin/"["a"]"pt-get" update\n'}]})
            found = text_steps(text)["test"][0]
            first, dash = found["runs"][0]["line"] + 1, found["line"]
            at = "x.yaml:{}: test: step 0 'Added': "
            self.assertEqual(
                [
                    at.format(first) + f"a CallExpr whose word 1 is `sudo`, not `/usr/bin/timeout`{off}",
                    at.format(first) + f"`[]` holds `[`, `]`: {EXPANDED_WORD}",
                    at.format(first)
                    + "`sudo` followed by a word of DblQuoted(Lit), Lit, DblQuoted(Lit), Lit, DblQuoted(Lit) part(s) "
                    "spelling `[]`, which bash expands (`[`, `]`), which has no known text, before its command word",
                    at.format(dash) + f"if: None: {APT_STEP_GUARD}",
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case='"$cmd" --version in a step that runs no apt'):
            text = render({"test": [{"name": "Tools", "run": 'cmd=/usr/bin/true\n"$cmd" --version\n'}]})
            first = text_steps(text)["test"][0]["runs"][0]["line"] + 1
            self.assertEqual(
                [
                    f"x.yaml:{first + 1}: test: step 0 'Tools': a word of DblQuoted(ParamExp) part(s) in command position: "
                    f"{UNKNOWN_COMMAND}"
                ],
                tree_problems("x.yaml", text),
            )
        # Round 11's three, still refused: `sudo 'apt' update` as a step of its own, `'eval'` above the form, and
        # `install jq zsh`; the text rule counts the last as a form, the tree does not, and the two counts disagree.
        with self.subTest(case="sudo 'apt' update as a step (audit of 4d09be21)"):
            text, first, _ = self.step("sudo 'apt' update\n")
            self.assertEqual(
                [self.STEP.format(first) + f"a CallExpr whose word 1 is `sudo`, not `/usr/bin/timeout`{off}"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="'eval' above the form and install without -y (audit of 4d09be21)"):
            text, first, _ = self.step(
                f"'eval' '/usr/bin/time''out() {{ shift 2; \"$@\"; }}'\n{form} update\n{form} install jq zsh\n"
            )
            self.assertEqual(
                [
                    self.STEP.format(first)
                    + f"a CallExpr whose word 1 is a word of SglQuoted part(s), not the bare literal `/usr/bin/timeout`{off}",
                    self.STEP.format(first + 2) + f"a CallExpr whose word 11 'jq' after `install` is not `-y`{off}",
                    self.STEP.format(first - 1)
                    + f"1 apt call(s) in the tree, 2 bound form(s) in the text; {TREE_COUNT}",
                ],
                tree_problems("x.yaml", text),
            )

    def test_a_step_the_tree_cannot_read_as_bash_is_refused_with_its_cause(self) -> None:
        form = self.FORM
        with self.subTest(case="a shell other than bash"):
            text, _, dash = self.step(f"{form} update\n", shell="sh")
            self.assertEqual(
                [self.STEP.format(dash) + "shell: 'sh': the tree reads the runner's bash"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="shell: bash"):
            text, _, _ = self.step(f"{form} update\n", shell="bash")
            self.assertEqual([], tree_problems("x.yaml", text))
        with self.subTest(case="an expression in the body"):
            text, first, _ = self.step(f"echo ${{{{ github.token }}}}\n{form} update\n")
            self.assertEqual(
                [self.STEP.format(first) + "`${{` in the run body: GitHub expands it before bash reads the text"],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="a body shfmt refuses"):
            text, first, _ = self.step(f"if true; then\n{form} update\n")
            (problem,) = tree_problems("x.yaml", text)
            self.assertTrue(
                problem.startswith(self.STEP.format(first - 1) + "shfmt cannot parse x.yaml test step 0 (exited 1): "),
                problem,
            )
        with self.subTest(case="a one-line run"):
            text = render({"test": [{"name": self.NAME, "timeout-minutes": "8", "if": self.GUARD}]}).replace(
                f"if: {self.GUARD}\n", f"if: {self.GUARD}\n        run: {form} update | cat\n"
            )
            line = text_steps(text)["test"][0]["runs"][0]["line"]
            self.assertEqual(
                [
                    self.STEP.format(line) + f"a BinaryCmd `|`: {APT_STEP}",
                    self.STEP.format(line) + f"0 apt call(s) in the tree, 1 bound form(s) in the text; {TREE_COUNT}",
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="a heredoc holding the form"):
            text, first, _ = self.step(f"cat << EOF\n{form} update\nEOF\n")
            self.assertEqual(
                [
                    self.STEP.format(first) + f"a CallExpr in a statement with Redirs: {APT_STEP}",
                    self.STEP.format(first - 1)
                    + f"0 apt call(s) in the tree, 1 bound form(s) in the text; {TREE_COUNT}",
                ],
                tree_problems("x.yaml", text),
            )
        with self.subTest(case="a file the census or the parser gate refuses is not read here"):
            text, _, _ = self.step(f"{form} update | cat\n")
            self.assertEqual([], tree_problems("x.yaml", text.replace("name: x\n", 'name: "x\n')))
            self.assertEqual([], tree_problems("x.yaml", text.replace("runs-on", "runs-on" + chr(0x2028))))

    def test_a_contract_or_parser_that_cannot_be_read_is_a_failure_not_an_absence(self) -> None:
        # Standing order 21: the contract refusing the pinned shfmt, and a tree whose statements the walk cannot read
        # (a renamed field), each raise naming the cause; neither is an empty problem list. The tree the real shfmt
        # gives is read again once the contract holds.
        contract_trees.cache_clear()
        self.addCleanup(contract_trees.cache_clear)
        with mock.patch.object(contract, "verified_trees", side_effect=contract.ContractError("injected")):
            with self.assertRaisesRegex(RuntimeError, f"{re.escape(NODE_TABLE)}: injected"):
                self.body(f"{self.FORM} update\n")
        contract_trees.cache_clear()
        contract_trees()  # the fixtures are read by the real parser; the injected tree below reaches the walk alone
        unreadable = {"Type": "File", "Stmts": [{"Command": {"Type": "CallExpr"}}]}
        with mock.patch.object(contract, "parse", return_value=unreadable):
            with self.assertRaisesRegex(RuntimeError, r"the tree of x lists 1 statement\(s\) but the walk saw none"):
                self.body("echo\n")
        self.assertEqual([], self.body(f"{self.FORM} update\n"))
        # The walker's own entry, as the contract test runs every walker: 0 clean, 1 with the nodes, 2 cannot judge.
        script = self.temp / "step.sh"
        script.write_text(f"{self.FORM} update\n")
        module = ROOT / "tests/unit/test_apt_mirror.py"
        clean = subprocess.run(
            [sys.executable, "-I", str(module), "--script", str(script)], capture_output=True, text=True, check=False
        )
        self.assertEqual((0, "", ""), (clean.returncode, clean.stdout, clean.stderr))
        script.write_text(f"timeout() {{ :; }}\n{self.FORM} update | cat\n")
        found = subprocess.run(
            [sys.executable, "-I", str(module), "--script", str(script)], capture_output=True, text=True, check=False
        )
        self.assertEqual(1, found.returncode, found.stderr)
        self.assertEqual(
            f"{script}:1: a FuncDecl `timeout`: {APT_STEP}\n{script}:2: a BinaryCmd `|`: {APT_STEP}\n",
            found.stdout,
        )
        script.write_text("if true; then\n")
        refused = subprocess.run(
            [sys.executable, "-I", str(module), "--script", str(script)], capture_output=True, text=True, check=False
        )
        self.assertEqual((2, ""), (refused.returncode, refused.stdout))
        self.assertIn("apt-bound-tree: shfmt cannot parse", refused.stderr)


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
        return workflow_problems([path]), dash_lines(text)

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
                f"x.yaml:{at[3]}: test: step 3 'Install apt packages for Codecov' repeats the name of step 2",
                f"x.yaml:{at[2]}: test: step 2 'Install apt packages for Codecov' has no timeout-minutes",
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
            [f"x.yaml:{at[0]}: test: step 0 'Install apt packages' has timeout-minutes 9, the formula gives 8"],
            problems,
        )
        steps = bounded_steps()
        steps[2]["name"] = "Upload coverage"
        problems, at = self.problems({"test": steps})
        self.assertEqual(
            [
                "budget row 'Install apt packages for Codecov' has no step that runs apt",
                f"x.yaml:{at[2]}: test: step 2 'Upload coverage' runs apt with no STEP_REST_BUDGET row",
            ],
            problems,
        )
        steps = bounded_steps()
        del steps[1]["name"]
        problems, at = self.problems({"test": steps})
        self.assertEqual(
            [
                "budget row 'Install apt packages for the unit tests' has no step that runs apt",
                f"x.yaml:{at[1]}: test: step 1 'step 1' runs apt with no STEP_REST_BUDGET row",
            ],
            problems,
        )

    def test_the_steps_that_lost_their_apt_calls_keep_the_formula_over_their_rest(self) -> None:
        # Round 12: "Install tools" and "Run Python unit tests" run no apt; each keeps timeout-minutes at the formula
        # over its measured rest alone (REST_ONLY_BUDGET), and the apt steps' rest is 0 (STEP_REST_BUDGET).
        for name, rest in REST_ONLY_BUDGET.items():
            with self.subTest(step=name):
                step = self.step("test.yaml", "test", name)
                self.assertIsNone(APT_CALL.search(step_text(step)))
                self.assertEqual(step_minutes(0, rest), int(step["timeout-minutes"]))
        self.assertEqual({0}, set(STEP_REST_BUDGET.values()))
        self.assertEqual((8, 7, 4), tuple(int(step["timeout-minutes"]) for step in bounded_steps()))


class ReaderCensusTest(unittest.TestCase):
    """Standing order 21 on the workflow reader: every `run:` the text holds is one the reader returned whole, or the
    step is named by file and line. Audit of 0a9fa727: `jobs()` returned no body for `run: |-` and `run: >`, so an
    apt step added in that form passed the step check without timeout-minutes. Audit of 81fa7256: the census read
    only the reader's indentation, so a step at five and seven spaces passed both. Audit of f4486ead: the census
    compared the literal `steps:`, so `steps: # comment` hid a list at five and seven from both. Audit of 56e41f9b:
    the grammar began at `jobs:`, so a quoted top-level `name` that ran on across a `jobs:` line hid the real
    `"jobs":` mapping from both. Audit of 8c1d334a: the census split the text at LF alone, so a comment line that
    went on after U+0085, U+2028 or U+2029 (line breaks to PyYAML) hid a whole job from both. Audit of 046aebb1:
    node_end saw no quote right after `?`, so `env: {?"x}` closed on its line for both while PyYAML read a key that
    swallowed the next step and its timeout-minutes. Round 8 gates every workflow on agreement with PyYAML itself,
    run in a child the uv idiom starts (Parser), so the grammar explains and the parser decides."""

    FORM = "/usr/bin/timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update"
    MARKER = "      - name: Upload coverage to Codecov\n"
    # Each form the reader does not return, as the value of an added step's `run:` key, with `{}` for the command.
    FORMS = (("|-", "|-\n          {}"), (">", ">\n          {}"), ("|2", "|2\n          {}"), ('"..."', '"{}"'))
    BASE = "name: x\non: push\njobs:\n  test:\n    runs-on: ubuntu-24.04\n    steps:\n"

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="apt-census-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.temp)], check=False))

    def written(self, text: str, name: str = "x.yaml") -> Path:
        path = self.temp / name
        path.write_bytes(text.encode("utf-8", "surrogateescape"))  # a bad byte in a fixture, as its surrogate
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
                text = workflow_text(path)
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
                    if form == '"..."':  # round 8: PyYAML unquotes the value, the census holds it as written
                        self.assertIn(
                            f"test.yaml:{dash}: test: step {index} runs 1 line(s) from {expected_header[:60]!r} in the "
                            f"text, 1 line(s) from {command[:60]!r} to PyYAML; {PARSER_GATE}",
                            problems,
                        )
                    self.assertEqual(3 if form == '"..."' else 2, len(problems), problems)
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
        path.write_text(path.read_text().replace("run: |-\n          /usr/bin/", "run: |\n          /usr/bin/"))
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
        """PyYAML, in the child, reads the same jobs, steps and run bodies as the census."""
        self.assertEqual([], parser_problems("x.yaml", text))

    def test_the_text_census_agrees_with_pyyaml_on_every_workflow(self) -> None:
        # Round 8: the gate. PyYAML runs in a child the uv idiom starts, as regime.yml's tests read their workflow,
        # so the agreement holds in CI's interpreter too, which has no YAML parser of its own; it is never skipped.
        # Every workflow's jobs, steps, run bodies, names and timeout-minutes are PyYAML's, and PyYAML saw them: a
        # parser that returned nothing would differ from the census, which counts test.yaml's 18 runs on its own.
        steps = 0
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                text = workflow_text(path)
                self.assertEqual([], parser_problems(path.name, text, parsed_steps(path)))
                document, _ = Parser.read(text)
                steps += sum(len(job["steps"]) for job in document["jobs"].values())
        self.assertGreaterEqual(steps, 23)  # test.yaml's one job alone

    def test_the_parser_gate_names_a_document_the_hand_written_readers_misread(self) -> None:
        # Each difference the gate can see, named by file, line, job and step: the job set, a step list, a step that
        # is not a mapping, a run body, a name or timeout-minutes the reader holds otherwise, and a document PyYAML
        # refuses. The round 6 and round 8 documents are in their own tests.
        folded = self.BASE + "      - run: >\n          echo a\n          echo b\n"
        for case, text, parsed, expected in (
            (
                "a folded run",
                folded,
                None,
                [
                    f"x.yaml:7: test: step 0 runs 2 line(s) from 'echo a' in the text, 1 line(s) from 'echo a echo b' "
                    f"to PyYAML; {PARSER_GATE}"
                ],
            ),
            (
                "a step that is not a mapping",
                self.BASE + "      - echo a\n",
                None,
                [f"x.yaml:7: test: step 0 is not a mapping to PyYAML ('echo a'); {PARSER_GATE}"],
            ),
            (
                "a quoted name, which the reader returns quoted",
                self.BASE + '      - name: "A"\n        run: echo a\n',
                {"test": [{"name": '"A"', "run": "echo a"}]},
                [f"""x.yaml:7: test: step 0 has name '"A"' to the reader, 'A' to PyYAML; {PARSER_GATE}"""],
            ),
            (
                "timeout-minutes the reader holds and PyYAML does not",
                self.BASE + "      - run: echo a\n",
                {"test": [{"run": "echo a", "timeout-minutes": "5"}]},
                [f"x.yaml:7: test: step 0 has timeout-minutes '5' to the reader, None to PyYAML; {PARSER_GATE}"],
            ),
            (
                "jobs: that is not a mapping",
                "name: x\non: push\njobs: 1\n",
                None,
                [f"x.yaml: the text holds jobs [], PyYAML reads no jobs mapping; {PARSER_GATE}"],
            ),
            (
                "a job without a step list",
                "name: x\non: push\njobs:\n  test:\n    runs-on: ubuntu-24.04\n",
                None,
                [f"x.yaml: test: PyYAML reads no step list; {PARSER_GATE}"],
            ),
        ):
            with self.subTest(case=case):
                self.assertEqual(expected, parser_problems("x.yaml", text, parsed))
        with self.subTest(case="a document PyYAML refuses"):
            (problem,) = parser_problems("x.yaml", self.BASE + "      - run: echo a\n     odd: 1\n")
            self.assertTrue(problem.startswith("x.yaml: PyYAML refuses the file (ParserError: "), problem)
            self.assertTrue(problem.endswith(f"; {PARSER_GATE}"), problem)
        with self.subTest(case="the same step to every reader"):
            text = self.BASE + "      - name: A\n        timeout-minutes: 5\n        run: |\n          echo a\n"
            self.assertEqual([], parser_problems("x.yaml", text, parsed_steps(self.written(text))))

    def test_a_parser_child_that_exits_nonzero_or_answers_nothing_is_a_failure_not_an_absence(self) -> None:
        # Standing order 21. Audit of ecde33b9 (round 9): the round 8 child was long-lived and its answer was read
        # before its exit status, which the stop at exit discarded, so a child that printed a valid document and then
        # exited 3 was trusted and the gate reported no problem. The child is one per document now and its status is
        # read first: a nonzero status is refused naming the status and stderr with the output unread; status 0 with
        # no output is refused too. Neither answer is cached, and the real child answers the same text afterwards.
        text = "round9: injected\n"
        answer = json.dumps({"document": {"jobs": {"test": {"steps": []}}}})
        live = Parser.command
        for case, program, expected in (
            (
                "a valid answer, then exit 3",
                f"import sys; print({answer!r}); print('boom', file=sys.stderr); sys.exit(3)",
                [f"the PyYAML child exited with status 3; its output {answer + chr(10)!r} is not read; stderr: boom"],
            ),
            (
                "exit 0 with no output",
                "pass",
                ["the PyYAML child exited with status 0 and 0 line(s) of output instead of one answer: ''"],
            ),
            (
                "exit 0 with two answers",
                f"print({answer!r}); print({answer!r})",
                ["the PyYAML child exited with status 0 and 2 line(s) of output instead of one answer"],
            ),
            (
                "exit 0 with a line that is not JSON",
                "print('not json')",
                ["the PyYAML child answered with a line that is not JSON", "'not json'"],
            ),
            (
                "exit 0 with JSON in another shape",
                "print('{\"jobs\": {}}')",
                ["the PyYAML child answered in another shape than a document or an error"],
            ),
        ):
            with self.subTest(case=case):
                Parser.command = [sys.executable, "-I", "-c", program]
                try:
                    with self.assertRaises(RuntimeError) as caught:
                        parser_problems("x.yaml", text)
                finally:
                    Parser.command = live
                for part in expected:
                    self.assertIn(part, str(caught.exception))
                self.assertNotIn(text, Parser.answers)
        self.assertEqual(({"round9": "injected"}, None), Parser.read(text))
        self.assertEqual(
            [f"x.yaml: the text holds jobs [], PyYAML reads no jobs mapping; {PARSER_GATE}"],
            parser_problems("x.yaml", text),
        )

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
                    self.assertIsNotNone(Parser.read(text)[1])

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

    def auditors_document(
        self, command: str, quoted_name: bool = True, quoted_jobs: bool = True
    ) -> tuple[Path, int, int]:
        """The audit's test.yaml, in whole or in part: the `name:` value opened with a double quote and continued,
        across a `jobs:` line at the margin and a copy of the real `test` job (its backslashes and double quotes
        escaped, as the scalar needs), to a closing quote on an added last step; the real header after it; then the
        real jobs block with a job `added` appended (its one step a `run: |` holding `command` at the reader's shape)
        under `"jobs":`. With `quoted_name` or `quoted_jobs` false that half is as written. Returns (path, the line
        of the real jobs key, the added step's dash line)."""
        text = (WORKFLOWS / "test.yaml").read_text()
        head, block = text.split("\njobs:\n", 1)
        title, header = head.split("\n", 1)
        self.assertEqual("name: Unit test", title)
        copy = block.replace("\\", "\\\\").replace('"', '\\"')
        name = f'name: "Unit test\njobs:\n{copy}      - run: echo hi"' if quoted_name else title
        key = '"jobs":' if quoted_jobs else "jobs:"
        added = f"  added:\n    runs-on: ubuntu-24.04\n    steps:\n      - name: Added\n        run: |\n          {command}\n"
        before = f"{name}\n{header}"
        jobs_line = before.count("\n") + 2
        return (
            self.written(f"{before}\n{key}\n{block}{added}", "test.yaml"),
            jobs_line,
            jobs_line + block.count("\n") + 4,
        )

    def yaml_reads_the_added_job(self, text: str, command: str, quoted_name: bool) -> None:
        """PyYAML's document holds the real jobs and `added`, whose step holds `command`; with the quoted name, the
        copy of the test job is inside the name."""
        document, error = Parser.read(text)
        self.assertIsNone(error)
        self.assertEqual([*text_steps((WORKFLOWS / "test.yaml").read_text()), "added"], list(document["jobs"]))
        self.assertEqual(command, document["jobs"]["added"]["steps"][0]["run"].strip())
        self.assertEqual(quoted_name, document["name"].startswith("Unit test jobs: test:"))

    def test_the_auditors_quoted_name_and_quoted_jobs_key_are_refused_by_line(self) -> None:
        # Audit of 56e41f9b: the round 5 grammar began at `jobs:`. A `name: "Unit test` that ran on, across a `jobs:`
        # line at the margin and a copy of the test job, to a closing quote gave both readers that copy, and the real
        # `"jobs":` mapping (a quoted key, YAML the runner executes) was never read, so an apt step added there
        # passed every check. Each half is now refused on its own line, and the real job is counted when neither is
        # written.
        name_refused = f'name: "Unit test (name: holds a quoted scalar that does not close on its line; {READ_VALUES})'
        quoted_key = f'"jobs": (not {KEY_FORM})'
        # Round 8: the parser gate alone sees the real jobs and one step fewer in `test` (the copy inside the name
        # ends on the added `echo hi"` step), parting at the first step whose escaped body differs from the real one.
        real = text_steps((WORKFLOWS / "test.yaml").read_text())
        jobs_differ = f"test.yaml: the text holds jobs ['test'], PyYAML reads {[*real, 'added']}; {PARSER_GATE}"
        parting = re.compile(
            rf"test\.yaml: test: {len(real['test']) + 1} steps in the text, {len(real['test'])} to PyYAML, parting at "
            rf"test\.yaml:[0-9]+: test: step [0-9]+; {re.escape(PARSER_GATE)}"
        )
        for command in ("sudo apt-get update", self.FORM, "sleep 7200"):
            short = command.split()[0]
            unbounded = [f"test.yaml:{{}}: {command} (1 apt call(s), 0 in the bound form)"] if short == "sudo" else []
            with self.subTest(command=short, written="both"):
                path, jobs_line, at = self.auditors_document(command)
                text = path.read_text()
                found = census(text)
                self.assertEqual([(1, name_refused), (jobs_line, quoted_key)], found.refused)
                self.assertEqual(["test"], list(found.steps))  # the copy inside the name, closed by its last step
                self.assertEqual(['echo hi"'], [run["header"] for run in found.steps["test"][-1]["runs"]])
                read = jobs(path)  # the reader reads the same copy: the hole on 56e41f9b
                self.assertEqual(["test"], list(read))
                self.assertEqual({"run": 'echo hi"'}, read["test"]["steps"][-1])
                problems = workflow_problems([path])
                self.assertEqual(
                    [f"test.yaml:1: {name_refused}", f"test.yaml:{jobs_line}: {quoted_key}", jobs_differ], problems[:3]
                )
                self.assertEqual([True], [parting.match(problem) is not None for problem in problems[3:]])
                self.assertEqual([line.format(at + 2) for line in unbounded], apt_violations("test.yaml", text))
                self.yaml_reads_the_added_job(text, command, quoted_name=True)
            with self.subTest(command=short, written="the quoted name alone"):
                path, jobs_line, at = self.auditors_document(command, quoted_jobs=False)
                found = census(path.read_text())
                self.assertEqual([(1, name_refused), (jobs_line, "jobs: (a second jobs: key)")], found.refused)
                self.assertEqual(["test"], list(found.steps))
                self.assertEqual(["test"], list(jobs(path)))
                problems = workflow_problems([path])
                self.assertEqual(
                    [f"test.yaml:1: {name_refused}", f"test.yaml:{jobs_line}: jobs: (a second jobs: key)", jobs_differ],
                    problems[:3],
                )
                self.assertEqual([True], [parting.match(problem) is not None for problem in problems[3:]])
                self.yaml_reads_the_added_job(path.read_text(), command, quoted_name=True)
            with self.subTest(command=short, written="the quoted jobs key alone"):
                path, jobs_line, at = self.auditors_document(command, quoted_name=False)
                found = census(path.read_text())
                self.assertEqual(
                    [(jobs_line, quoted_key), (1, f"no `jobs:` line in the file ({JOBS_LINE})")], found.refused
                )
                self.assertEqual({}, found.steps)
                with self.assertRaises(IndexError):  # the reader finds no `jobs:` line and is loud on its own
                    jobs(path)
                self.yaml_reads_the_added_job(path.read_text(), command, quoted_name=False)
            with self.subTest(command=short, written="neither"):
                path, jobs_line, at = self.auditors_document(command, quoted_name=False, quoted_jobs=False)
                text = path.read_text()
                (step,) = text_steps(text)["added"]
                self.assertEqual((at, [command]), (step["line"], [line.strip() for line in step["runs"][0]["body"]]))
                expected = (
                    []
                    if short == "sleep"
                    else [f"test.yaml:{at}: added: step 0 'Added' runs apt with no STEP_REST_BUDGET row"]
                )
                self.assertEqual(expected, workflow_problems([path]))
                self.assertEqual([line.format(at + 2) for line in unbounded], apt_violations("test.yaml", text))
                self.agrees_with_yaml(text)

    def test_a_hash_inside_a_quoted_value_or_a_flow_string_is_content(self) -> None:
        # YAML 7.3: a `#` inside a quoted scalar, or inside a quoted string of a flow collection, is content; a `#`
        # after a blank anywhere else opens a comment. The census reads both as PyYAML does (a comment rule that
        # stopped at the first blank `#` would read `name: "a #b"` as an unclosed quote and refuse a value the
        # readers return whole), and the reader takes a step key's quoted value whole.
        for case, text, value, comment in (
            ("a quoted name", 'name: "a #b"', '"a #b"', ""),
            ("a quoted name with a comment", 'name: "a #b" # c', '"a #b"', "# c"),
            (
                "a flow collection with a quoted string",
                "on: {push: {branches: ['a #b']}}",
                "{push: {branches: ['a #b']}}",
                "",
            ),
            ("a doubled single quote", "name: 'it''s #1'", "'it''s #1'", ""),
            ("an escaped double quote", 'name: "a \\" #b"', '"a \\" #b"', ""),
            ("a plain scalar", "name: a #b", "a", "#b"),
            ("a flow collection with a comment", "on: [push] # c", "[push]", "# c"),
        ):
            with self.subTest(case=case):
                lexed = lex(text)
                self.assertEqual((value, comment), (lexed.value, lexed.comment))
                self.assertIn(value_form(value), READ_VALUE_FORMS)
        text = (
            'name: "Unit #1"\non: {push: {branches: ["a #b"]}}\njobs:\n  test:\n    runs-on: ubuntu-24.04\n'
            '    steps:\n      - name: "a #b"\n        run: echo a\n'
        )
        path = self.written(text)
        self.assertEqual([], census(text).refused)
        self.assertEqual([], census_problems("x.yaml", text, parsed_steps(path)))
        self.assertEqual('"a #b"', jobs(path)["test"]["steps"][0]["name"])
        self.agrees_with_yaml(text)

    def hidden_job(self, separator: str, command: str) -> tuple[Path, int, list[int]]:
        """The audit's test.yaml: a job `added` appended after a comment, the whole job on one LF line with its lines
        joined by `separator` (a line break to PyYAML; to the census and the reader, text inside the comment), its
        one step a `run: |` holding `command` at the reader's shape. Returns (path, that line, the columns of the
        separators on it)."""
        text = (WORKFLOWS / "test.yaml").read_text()
        self.assertTrue(text.endswith("\n"))
        pieces = (
            "  # a note",
            "  added:",
            "    runs-on: ubuntu-24.04",
            "    steps:",
            "      - name: Added",
            "        run: |",
            f"          {command}",
        )
        columns, column = [], 0
        for piece in pieces[:-1]:
            column += len(piece) + 1
            columns.append(column)
        return self.written(text + separator.join(pieces) + "\n", "test.yaml"), text.count("\n") + 1, columns

    def test_the_auditors_job_after_a_yaml_1_1_line_break_is_refused_by_line_and_column(self) -> None:
        # Audit of 8c1d334a: the census split the text at LF alone, as the reader does, while PyYAML (YAML 1.1) also
        # breaks a line at U+0085, U+2028 and U+2029. A comment line that went on after one of them held a whole
        # job, read as comment text by both readers and as the job `added` by PyYAML, so its bounded apt step passed
        # every check without timeout-minutes or a budget row. Each separator is now refused by line and column
        # before any line is read; the same job on its own lines is read by both and named by the step check.
        breaks = (("\x85", "a next line"), ("\u2028", "a line separator"), ("\u2029", "a paragraph separator"))
        for separator, name in breaks:
            for command in ("sudo apt-get update", self.FORM, "sleep 7200"):
                with self.subTest(separator=f"U+{ord(separator):04X}", command=command.split()[0]):
                    path, line, columns = self.hidden_job(separator, command)
                    text = workflow_text(path)
                    why = f"{name}, a line break to a YAML 1.1 reader (U+{ord(separator):04X})"
                    expected = [(line, f"{why} at column {column}; {CHARACTER_SET}") for column in columns]
                    found = census(text)
                    self.assertEqual((expected, {}), (found.refused, found.steps))
                    self.assertEqual(["test"], list(jobs(path)))  # the hole: the reader reads the line as a comment
                    self.assertEqual(
                        [f"test.yaml:{line}: {message}" for _, message in expected], workflow_problems([path])
                    )
                    violations = apt_violations("test.yaml", text)
                    if command.startswith("sudo"):
                        self.assertEqual(1, len(violations), violations)
                        self.assertTrue(violations[0].startswith(f"test.yaml:{line}: "), violations[0])
                        self.assertTrue(violations[0].endswith("(1 apt call(s), 0 in the bound form)"), violations[0])
                    else:
                        self.assertEqual([], violations)
                    self.yaml_reads_the_added_job(text, command, quoted_name=False)
        # On its own lines the job is read by both readers, and the step check names its apt step.
        for command in ("sudo apt-get update", self.FORM, "sleep 7200"):
            with self.subTest(separator="LF", command=command.split()[0]):
                path, line, _ = self.hidden_job("\n", command)
                text = workflow_text(path)
                (step,) = text_steps(text)["added"]
                self.assertEqual(
                    (line + 4, [command]), (step["line"], [body.strip() for body in step["runs"][0]["body"]])
                )
                (read,) = jobs(path)["added"]["steps"]
                self.assertEqual(("Added", "|", command), (read["name"], read["run"], read["script"].strip()))
                expected = (
                    []
                    if command.startswith("sleep")
                    else [f"test.yaml:{line + 4}: added: step 0 'Added' runs apt with no STEP_REST_BUDGET row"]
                )
                self.assertEqual(expected, workflow_problems([path]))
                self.agrees_with_yaml(text)

    # Round 7: one character of each refused class (REFUSED_CHARACTERS), spelled as the census names it; the last two
    # are bytes that are not UTF-8 as `surrogateescape` decodes them, the first of those a UTF-8 sequence cut short.
    CHARACTERS = (
        ("\x00", ["a C0 control character (U+0000)"]),
        ("\x07", ["a C0 control character (U+0007)"]),
        ("\x0b", ["a C0 control character (U+000B)"]),
        ("\x0c", ["a C0 control character (U+000C)"]),
        ("\r", ["a carriage return (U+000D)"]),
        ("\x1b", ["a C0 control character (U+001B)"]),
        ("\x1f", ["a C0 control character (U+001F)"]),
        ("\x7f", ["a delete character (U+007F)"]),
        ("\x80", ["a C1 control character (U+0080)"]),
        ("\x85", ["a next line, a line break to a YAML 1.1 reader (U+0085)"]),
        ("\x9f", ["a C1 control character (U+009F)"]),
        ("\u2028", ["a line separator, a line break to a YAML 1.1 reader (U+2028)"]),
        ("\u2029", ["a paragraph separator, a line break to a YAML 1.1 reader (U+2029)"]),
        ("\ufeff", ["a byte order mark (U+FEFF)"]),
        ("\ufffe", ["a noncharacter (U+FFFE)"]),
        ("\uffff", ["a noncharacter (U+FFFF)"]),
        ("\udce2\udc80", ["a byte that is not UTF-8 (0xE2)", "a byte that is not UTF-8 (0x80)"]),
        ("\udcff", ["a byte that is not UTF-8 (0xFF)"]),
    )
    # Characters the set keeps: a tab in content, a no-break space, a box-drawing character (two real workflows hold
    # them in comments), a supplementary-plane character and the replacement character.
    KEPT = ("\t", "\xa0", "\u2502", "\U0001f600", "\ufffd")

    def offsets(self, text: str) -> dict[str, int]:
        """Seven places in test.yaml to plant a character: by name, the offset at which it goes in."""
        comment = re.search(r"^ *# .*$", text, re.MULTILINE)
        body = re.search(r"^ {10}(?!.*apt)\S.*$", text, re.MULTILINE)  # a run body line that holds no apt call
        self.assertTrue(comment and body)
        return {
            "the first character of the file": 0,
            "the end of the name: line": text.index("\n"),
            "after the jobs: key": text.index("\njobs:\n") + 6,
            "the end of a comment": comment.end(),
            "a step's indentation": text.index(self.MARKER) + 3,
            "the end of a run body line": body.end(),
            "after the last line break": len(text),
        }

    def test_every_refused_character_is_named_by_line_and_column_wherever_planted(self) -> None:
        # One character of each class at each of seven places in the real test.yaml: the census refuses the file on
        # that character's line and column and reads no step, the step check names that and nothing else (the reader
        # is not asked about a file with no lines), and the line rule is unchanged (no place holds an apt call). The
        # kept characters pass the scan, and the census and PyYAML read the file as before.
        text = (WORKFLOWS / "test.yaml").read_text()
        self.assertEqual([], refused_characters(text))
        for char, names in self.CHARACTERS:
            for place, offset in self.offsets(text).items():
                with self.subTest(char=f"U+{ord(char[0]):04X}", place=place):
                    planted = text[:offset] + char + text[offset:]
                    line = text.count("\n", 0, offset) + 1
                    column = offset - text.rfind("\n", 0, offset)
                    expected = [
                        (line, f"{name} at column {column + index}; {CHARACTER_SET}")
                        for index, name in enumerate(names)
                    ]
                    path = self.written(planted, "test.yaml")
                    self.assertEqual(planted, workflow_text(path))  # the bytes round-trip, a bad byte as its surrogate
                    found = census(planted)
                    self.assertEqual((expected, {}), (found.refused, found.steps))
                    self.assertEqual(
                        [f"test.yaml:{number}: {why}" for number, why in expected], workflow_problems([path])
                    )
                    self.assertEqual([], apt_violations("test.yaml", planted))
        offset = self.offsets(text)["the end of a comment"]
        for char in self.KEPT:
            with self.subTest(char=f"U+{ord(char):04X}"):
                planted = text[:offset] + char + text[offset:]
                self.assertEqual([], refused_characters(planted))
                self.assertEqual([], workflow_problems([self.written(planted, "test.yaml")]))
                self.agrees_with_yaml(planted)

    INSTALL = "/usr/bin/timeout --kill-after=10 150 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 install -y jq curl"

    def complex_key_document(self, command: str, key: str = '{?"x}') -> tuple[Path, int, int]:
        """The audit's test.yaml: the Codecov apt step rewritten with its `run: |` holding `command` first,
        then `env: {key}` and its timeout-minutes, then a step `Phantom` whose one body line `CLOSE: end": value}`
        closes a quote. With the auditor's `{?"x}`, PyYAML takes `"x}` after the `?` indicator as a double-quoted key
        that runs to `end"`: the timeout-minutes and the Phantom step are text inside it, and the real step has `run`
        and `env` and no timeout-minutes. With a plain `{x: y}` the mapping closes on its line and every reader
        agrees. Returns (path, the Codecov step's dash line, the Phantom step's dash line)."""
        text = (WORKFLOWS / "test.yaml").read_text()
        start = text.index("      - name: Install apt packages for Codecov\n")
        end = text.index(self.MARKER)
        (condition,) = [line for line in text[start:end].splitlines() if line.startswith("        if:")]
        rewritten = (
            f"      - name: Install apt packages for Codecov\n{condition}\n        run: |\n          {command}\n"
            f"        env: {key}\n        timeout-minutes: 4\n"
            '      - name: Phantom\n        run: |\n          CLOSE: end": value}\n\n'
        )
        dash = text[:start].count("\n") + 1
        return self.written(text[:start] + rewritten + text[end:], "test.yaml"), dash, dash + 6

    def test_the_auditors_quoted_complex_key_fails_the_parser_agreement(self) -> None:
        # Audit of 046aebb1: node_end saw no quote right after `?`, so `env: {?"x}` was a flow collection complete on
        # its line to the census and the reader; both counted the Phantom step and attached the timeout-minutes to
        # the Codecov step, while to PyYAML the quote opens a key that swallows both and the real apt step has no
        # timeout-minutes. The parser is the gate: PyYAML's reading must match the census step for step, and the
        # step where they part is named; the grammar names the line as the explanation.
        env_refused = f'env: {{?"x}} (env: holds a flow collection that does not close on its line; {READ_VALUES})'
        for command in ("sudo apt-get update", self.INSTALL, "sleep 7200"):
            with self.subTest(command=command.split()[0]):
                path, dash, phantom = self.complex_key_document(command)
                text = workflow_text(path)
                found = census(text)
                self.assertEqual([(dash + 4, env_refused)], found.refused)  # the explanation layer
                read = jobs(path)["test"]["steps"]
                # The hole: both hand-written readers count the Phantom step and give the Codecov step its timeout.
                self.assertEqual(len(read), len(found.steps["test"]))
                codecov, swallowed = read[-3], read[-2]
                self.assertEqual(
                    ("Install apt packages for Codecov", "4"), (codecov["name"], codecov["timeout-minutes"])
                )
                self.assertEqual(("Phantom", phantom), (swallowed["name"], found.steps["test"][-2]["line"]))
                self.assertEqual(
                    [f"test.yaml:{dash + 4}: {env_refused}"], census_problems("test.yaml", text, parsed_steps(path))
                )
                # PyYAML: one step fewer, the Codecov step with the command and the env key holding the rest.
                document, error = Parser.read(text)
                self.assertIsNone(error)
                steps = document["jobs"]["test"]["steps"]
                self.assertEqual(len(read) - 1, len(steps))
                (parsed,) = [step for step in steps if step.get("name") == "Install apt packages for Codecov"]
                self.assertNotIn("timeout-minutes", parsed)
                self.assertEqual(command, parsed["run"].strip())
                (key,) = parsed["env"]
                self.assertTrue(key.startswith("x} timeout-minutes: 4 - name: Phantom run: | CLOSE: end"), key)
                parting = f"test.yaml:{dash}: test: step {len(read) - 3}"
                extra = {
                    # an unbounded call: the step holds timeout-minutes 4 to the reader, and the formula gives 1
                    "sudo": [
                        f"{parting} 'Install apt packages for Codecov' has timeout-minutes 4, the formula gives 1"
                    ],
                    "/usr/bin/timeout": [],
                    "sleep": ["budget row 'Install apt packages for Codecov' has no step that runs apt"],
                }[command.split()[0]]
                self.assertEqual(
                    [
                        f"test.yaml:{dash + 4}: {env_refused}",
                        f"test.yaml: test: {len(read)} steps in the text, {len(steps)} to PyYAML, parting at {parting}; "
                        f"{PARSER_GATE}",
                        *extra,
                    ],
                    workflow_problems([path]),
                )
                violations = apt_violations("test.yaml", text)
                if command.startswith("sudo"):
                    self.assertEqual(
                        [f"test.yaml:{dash + 3}: {command} (1 apt call(s), 0 in the bound form)"], violations
                    )
                else:
                    self.assertEqual([], violations)
        # With a plain flow mapping in the key's place every reader agrees: the Phantom step is a step to all three,
        # the Codecov step keeps its timeout-minutes, and the file passes.
        path, dash, phantom = self.complex_key_document(self.INSTALL, key="{x: y}")
        text = workflow_text(path)
        self.assertEqual([], census(text).refused)
        self.assertEqual(phantom, text_steps(text)["test"][-2]["line"])
        self.assertEqual([], workflow_problems([path]))
        self.agrees_with_yaml(text)

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
        unclosed_quote = "a quoted scalar that does not close on its line"
        unclosed_flow = "a flow collection that does not close on its line"
        no_jobs = (1, f"no `jobs:` line in the file ({JOBS_LINE})")
        test_job = f"  test:\n    runs-on: ubuntu-24.04\n    steps:\n      - run: {update}\n"
        complex_value = f"{{test: {{runs-on: ubuntu-24.04, steps: [{{run: {update}}}]}}}}"
        step_keys, job_keys = ", ".join(sorted(STEP_KEYS)), ", ".join(sorted(JOB_KEYS))
        top_keys = ", ".join(sorted(TOP_KEYS))
        nel = "a next line, a line break to a YAML 1.1 reader (U+0085)"
        ls = "a line separator, a line break to a YAML 1.1 reader (U+2028)"
        ps = "a paragraph separator, a line break to a YAML 1.1 reader (U+2029)"

        def at(line: int, column: int, name: str) -> tuple[int, str]:
            return (line, f"{name} at column {column}; {CHARACTER_SET}")

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
                [
                    (2, f"on: &s push (on: holds an anchor; {READ_VALUES})"),
                    (6, f"steps: *s (steps: holds an alias; {STEPS_VALUE})"),
                ],
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
                [(2, f"on: &base (on: holds an anchor; {READ_VALUES})"), (8, f"<<: *base ({not_key})")],
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
                [(2, f"on: &s {{run: {update}}} (on: holds an anchor; {READ_VALUES})"), (7, f"- *s ({not_key})")],
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
                [
                    (2, f"on: &u push (on: holds an anchor; {READ_VALUES})"),
                    (7, f"- uses: *u (uses: holds an alias; {READ_VALUES})"),
                ],
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
                [
                    (2, f"on: &e {{}} (on: holds an anchor; {READ_VALUES})"),
                    (6, f"env: *e (env: holds an alias; {READ_VALUES})"),
                ],
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
                [at(7, 33, "a carriage return (U+000D)")],
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
            # the top level (round 6)
            (
                "a quoted jobs key",
                f'name: x\non: push\n"jobs":\n{test_job}',
                [(3, f'"jobs": ({not_key})'), no_jobs],
                "reads",
            ),
            (
                "a quoted name that continues onto a jobs: line",
                f'name: "x\njobs:\n  fake:\n    runs-on: ubuntu-24.04\n    steps:\n      - run: echo hi"\non: push\n'
                f'"jobs":\n{test_job}',
                [(1, f'name: "x (name: holds {unclosed_quote}; {READ_VALUES})'), (8, f'"jobs": ({not_key})')],
                "reads",
            ),
            (
                "a single-quoted name that continues",
                f"name: 'x\njobs:\n{test_job[:-1]}'\non: push\n",
                [(1, f"name: 'x (name: holds {unclosed_quote}; {READ_VALUES})")],
                "reads",
            ),
            (
                "a flow collection that continues onto a jobs: line",
                "name: x\non: {push: 1,\njobs: 2}\n",
                [(2, f"on: {{push: 1, (on: holds {unclosed_flow}; {READ_VALUES})"), (3, f"jobs: 2}} ({JOBS_LINE})")],
                "reads",
            ),
            (
                "text after a quoted scalar",
                f'name: "x" y\non: push\njobs:\n{test_job}',
                [(1, f'name: "x" y (name: holds text after a quoted scalar; {READ_VALUES})')],
                "raises",
            ),
            (
                "a key the schema gives no workflow",
                f"name: x\nfoo: 1\non: push\njobs:\n{test_job}",
                [(2, f"foo: 1 (foo: is not a workflow key; the workflow keys are {top_keys})")],
                "reads",
            ),
            (
                "a second name: key",
                f"name: x\nname: y\non: push\njobs:\n{test_job}",
                [(2, "name: y (a second name: key in one workflow)")],
                "reads",
            ),
            (
                "a complex jobs key",
                f"name: x\non: push\n? jobs\n: {complex_value}\n",
                [(3, f"? jobs ({not_key})"), (4, f": {complex_value} ({not_key})"), no_jobs],
                "reads",
            ),
            (
                "a merge key at the top",
                f"name: x\non: &b\n  jobs:\n    test:\n      runs-on: ubuntu-24.04\n      steps:\n        - run: {update}\n"
                "<<: *b\n",
                [(2, f"on: &b (on: holds an anchor; {READ_VALUES})"), (8, f"<<: *b ({not_key})"), no_jobs],
                "reads",
            ),
            (
                "an alias on jobs:",
                f"name: x\non: &j\n{test_job}jobs: *j\n",
                [(2, f"on: &j (on: holds an anchor; {READ_VALUES})"), (7, f"jobs: *j ({JOBS_LINE})")],
                "reads",
            ),
            (
                "a tag on jobs:",
                f"name: x\non: push\njobs: !!map\n{test_job}",
                [(3, f"jobs: !!map ({JOBS_LINE})")],
                "reads",
            ),
            (
                "a blank before the jobs colon",
                f"name: x\non: push\njobs :\n{test_job}",
                [(3, f"jobs : ({not_key})"), no_jobs],
                "reads",
            ),
            ("a document start marker", f"---\n{head}{test_job}", [(1, f"--- ({not_key})")], "reads"),
            (
                "an indented first line",
                f"  name: x\non: push\njobs:\n{test_job}",
                [(1, "name: x (indented 2 before any top-level key)")],
                "raises",
            ),
            (
                "a block scalar on name:",
                f"name: |\n  x\non: push\njobs:\n{test_job}",
                [(1, f"name: | (name: holds a block header; {READ_VALUES})")],
                "reads",
            ),
            (
                "a carriage return at the top",
                f"name: x\r\non: push\njobs:\n{test_job}",
                [at(1, 8, "a carriage return (U+000D)")],
                "reads",
            ),
            (
                "a tab before a top-level key",
                f"\tname: x\non: push\njobs:\n{test_job}",
                [(1, "name: x (a tab in the indentation)")],
                "raises",
            ),
            # a value that continues inside jobs (round 6)
            (
                "a quoted step value that continues",
                base + f'      - name: "a\n        run: {update}"\n',
                [(7, f'- name: "a (name: holds {unclosed_quote}; {READ_VALUES})')],
                "reads",
            ),
            (
                "a flow collection that continues on a step key",
                base + "      - uses: x/y@v1\n        with: {a: 1,\n          b: 2}\n",
                [(8, f"with: {{a: 1, (with: holds {unclosed_flow}; {READ_VALUES})")],
                "reads",
            ),
            (
                "a flow collection that continues on a job key",
                job + "    env: {A: 1,\n      B: 2}\n    steps:\n      - run: echo a\n",
                [(6, f"env: {{A: 1, (env: holds {unclosed_flow}; {READ_VALUES})")],
                "reads",
            ),
            # the quote after the ? indicator (round 8)
            (
                "a quoted key opened after ? in a flow mapping",
                base + '      - run: echo a\n        env: {?"x}\n      - run: |\n          end": v}\n',
                [(8, f'env: {{?"x}} (env: holds {unclosed_flow}; {READ_VALUES})')],
                "reads",
            ),
            (
                "a quoted key opened after ? in a flow sequence",
                base + "      - run: echo a\n        with: [?'x]\n      - run: |\n          end': v]\n",
                [(8, f"with: [?'x] (with: holds {unclosed_flow}; {READ_VALUES})")],
                "reads",
            ),
            # the characters (round 7)
            (
                "a next line after a comment",
                base + f"      - run: echo a\n  # c\x85  added:\x85    steps:\x85      - run: {update}\n",
                [at(8, 6, nel), at(8, 15, nel), at(8, 26, nel)],
                "reads",
            ),
            (
                "a line separator after a comment",
                base + f"      - run: echo a\n  # c\u2028  added:\u2028    steps:\u2028      - run: {update}\n",
                [at(8, 6, ls), at(8, 15, ls), at(8, 26, ls)],
                "reads",
            ),
            (
                "a paragraph separator after a comment",
                base + f"      - run: echo a\n  # c\u2029  added:\u2029    steps:\u2029      - run: {update}\n",
                [at(8, 6, ps), at(8, 15, ps), at(8, 26, ps)],
                "reads",
            ),
            (
                "a line separator in a run body",
                base + f"      - run: |\n          echo a\u2028  added:\n    steps:\n      - run: {update}\n",
                [at(8, 17, ls)],
                "reads",
            ),
            ("a NUL", base + "      - run: echo a\x00\n", [at(7, 20, "a C0 control character (U+0000)")], "raises"),
            (
                "an escape in a comment",
                base + "      - run: echo a # \x1b\n",
                [at(7, 23, "a C0 control character (U+001B)")],
                "raises",
            ),
            (
                "a form feed in the indentation",
                base + "     \x0c- run: echo a\n",
                [at(7, 6, "a C0 control character (U+000C)")],
                "raises",
            ),
            (
                "a delete character",
                base + "      - run: echo a\x7f\n",
                [at(7, 20, "a delete character (U+007F)")],
                "raises",
            ),
            (
                "a C1 control character",
                base + "      - run: echo a\x9f\n",
                [at(7, 20, "a C1 control character (U+009F)")],
                "raises",
            ),
            (
                "a byte order mark at the start",
                "\ufeff" + base + "      - run: echo a\n",
                [at(1, 1, "a byte order mark (U+FEFF)")],
                "reads",
            ),
            (
                "a byte order mark in a comment",
                base + "      - run: echo a # \ufeff\n",
                [at(7, 23, "a byte order mark (U+FEFF)")],
                "reads",
            ),
            ("a noncharacter", base + "      - run: echo a\ufffe\n", [at(7, 20, "a noncharacter (U+FFFE)")], "raises"),
            (
                "a byte that is not UTF-8",
                base + "      - run: echo a\udcff\n",
                [at(7, 20, "a byte that is not UTF-8 (0xFF)")],
                "raises",
            ),
            (
                "a no-break space before a job name",
                base + f"      - run: echo a\n  \xa0added:\n    steps:\n      - run: {update}\n",
                [(8, f"\xa0added: ({not_key})")],
                "reads",
            ),
            (
                "a no-break space after the jobs colon",
                f"name: x\non: push\njobs:\xa0\n{test_job}",
                [(3, f"jobs:\xa0 ({not_key})"), no_jobs],
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
                _, error = Parser.read(text)
                if yaml_reads == "reads":
                    self.assertIsNone(error)
                else:
                    self.assertIsNotNone(error)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--script"]:  # the walker's own entry, as the other walkers over shfmt's JSON have one
        sys.exit(tree_main(sys.argv[1:]))
    unittest.main()
