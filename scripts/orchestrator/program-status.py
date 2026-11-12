#!/usr/bin/env -S python3 -I
"""Print the operator's state report of a program store in standing order 56's shape (regime-cutover U497).

The operator asked (2026-11-12 JST, order 57) whether the program is moving or stopped and could not tell from the
coordinator's prose. This lever answers from the store's tables alone: `program-status.py <store> [--ja]
[--now <ts>] [--progress-root <dir>]` prints one word of state and its reason, one signal line per goal element, the
operator's acts, the decisions only the operator can make, and what the agent runs; the coordinator's reply quotes
this output instead of composing it. Plain text, five headings, at most one line per item, no table, no colour, no
chronology, no commit hash, and no unit id outside the running-work section (order 56). Every input is a store file
with a fixed header, read by one reader each and refused on any other shape (order 21); nothing is written.

The report, line by line:
- `state: <word>: <reason>, last record <age> min ago`. The word is `done` when every tests table is green;
  `stopped` when no unit is in flight and an open decision or a pending operator act exists, or when a stall check
  beside this lever reports every in-flight unit `stalled` or `no-file`; otherwise `moving`. The reason is the first
  matching condition in words (`every table green`; `nothing in flight, waiting on <n> operator acts and <m>
  decisions`; `every in-flight worker silent`; `<n> units in flight`); the age is `--now` (else the clock, UTC) minus
  the last row's `ts` of `decisions.tsv` (header `ts phase decision why evidence result`), in whole minutes, a ts
  after now reading 0. A decisions table with no row is a refusal: the last recorded step is read from it.
- `elements`, then one line per `tests/<element>.tsv` in name order (header `id use_case source kind host command
  expected observed verdict ts`; a file under `tests/` not ending in `.tsv` is ignored):
  `<element>: <signal> <ok>/<rows> OK, <ng> NG, <pending> pending`, the signal `green` when every verdict is `OK`,
  `red` when any is `NG`, `yellow` when none is `NG` and one is `pending`, else `grey` (no row, or every verdict
  another word).
- `operator acts`, then every tests row whose `kind` is `operator` and whose verdict is `pending`, tables in name
  order and rows in file order: `<element> <id>: <command>` (the command cell holds the step as the handouts write
  it).
- `operator decisions`, then every `gates.md` row whose `result` cell is empty: `<id>: <gate> (<moment>; default
  <default>)`. The table is the one under the header line `| id | gate | moment | options | default | result |`; the
  separator row and lines that are no table row are skipped; the result is the text after the fifth cell, so a
  `||` typed into a row lands there; a row with fewer than six cells is a refusal naming the line.
- `agent running`, then every `units.tsv` row (header `id track state branch pr head_sha brief note`) whose state is
  `in-flight`, in file order: `<id> <track> pr <pr or -> progress: <column>`. When `stall-check.py` (U496) is a
  regular file beside this lever it is run once as `python3 -I <dir>/stall-check.py <store> [--progress-root <dir>]
  [--now <ts>]` with this lever's interpreter, and its rows, `unit<TAB>state<TAB>age_minutes<TAB>last_line` (an
  optional first row of those names is skipped), fill the column as `<state>, <age_minutes> min, <last_line>`; an
  in-flight unit it names no row for reads `progress: no row`; its exit 0 or 1 is a report, its exit 2 is a refusal
  of this report quoting its first stderr line, any other exit, a row of another width, a unit named twice, a time
  limit of 120 seconds or a start that fails is a refusal too. Without the file beside this one the column reads
  `progress: unknown`. Rows of units not in flight print nothing.
A section with no item prints `none`. `--ja` prints the five headings and the state word in the operator's forms
(状態 / 要素 / 操作者の作業 / 操作者の判断 / agent が動かしているもの; 進んでいる / 止まっている / 完了) and translates nothing else.

Exit 0 when the report printed. Exit 2 with one stderr line, `program-status.py: refused: <reason>`, and nothing on
stdout for every refusal: the self pin (below), a store that is no directory, `--now` not `<YYYY-MM-DD>T<HH:MM:SS>Z`,
a file that is missing, unreadable or not UTF-8, a tests table, `units.tsv` or `decisions.tsv` whose first line is not
its header or whose row has another number of cells or a carriage return, a `gates.md` without the header line or
with a short row, a `decisions.tsv` with no row or whose last ts is not a timestamp, a `tests` directory that is
missing, and the stall-check outcomes above. No file is written and no mode is changed.

Installed as `~/.local/bin/common/program-status.py` in `brief-check.py`'s form: `scripts/generate-agent-configs.py`
writes the same bytes to `home/dot_local/bin/common/executable_program-status.py` and pins their sha256 under
`claude.levers.sha256`; before anything else the file hashes itself against that pin, the deployed manifest
`~/.agents/agent-config.yaml` when its physical directory is the physical `~/.local/bin/common`, else the checkout's
`home/dot_agents/agent-config.yaml` two levels up, and refuses to run on a difference, so a rewritten copy prints no
report. The orchestrator seat's policy allows that installed path alone.
"""

import argparse
import hashlib
import os
import re
import stat
import subprocess
import sys
from datetime import datetime, timezone

LEVER = "program-status.py"
STALL_CHECK = "stall-check.py"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py, U136).
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")

TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TESTS_HEADER = ("id", "use_case", "source", "kind", "host", "command", "expected", "observed", "verdict", "ts")
UNITS_HEADER = ("id", "track", "state", "branch", "pr", "head_sha", "brief", "note")
DECISIONS_HEADER = ("ts", "phase", "decision", "why", "evidence", "result")
GATES_HEADER = "| id | gate | moment | options | default | result |"
GATES_WIDTH = 6
SEPARATOR_CELL = re.compile(r"^:?-+:?$")
STALL_HEADER = ("unit", "state", "age_minutes", "last_line")
STALL_TIMEOUT = 120
# The stall check's states that mean the worker is silent (U496).
SILENT = frozenset({"stalled", "no-file"})

HEADINGS = {
    "en": ("state", "elements", "operator acts", "operator decisions", "agent running"),
    "ja": ("状態", "要素", "操作者の作業", "操作者の判断", "agent が動かしているもの"),
}
WORDS = {
    "en": {"moving": "moving", "stopped": "stopped", "done": "done"},
    "ja": {"moving": "進んでいる", "stopped": "止まっている", "done": "完了"},
}


def refuse(reason):
    """One stderr line in the levers' words, exit 2; nothing was printed."""
    print(f"{LEVER}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `program-status.py`
    entry: one entry is the pin, none or two is a refusal. Every read is checked and a failed one is a refusal, never
    a pass (preferences.md standing order 21); the reader is brief-check.py's, spelled the same.
    """
    directory = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    self_path = os.path.join(directory, os.path.basename(__file__))
    home = os.environ.get("HOME", "")
    if home and os.path.isdir(home) and directory == os.path.realpath(os.path.join(home, ".local/bin/common")):
        manifest = os.path.join(home, ".agents/agent-config.yaml")
    else:
        manifest = os.path.join(directory, "../../home/dot_agents/agent-config.yaml")
    if not os.access(manifest, os.R_OK):
        refuse(f"manifest unreadable: {manifest}")
    try:
        with open(manifest, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        refuse(f"cannot read {manifest}")
    pins = [digest for name, digest in manifest_levers(lines, manifest) if name == LEVER]
    if len(pins) != 1:
        refuse(f"no single sha256 pin for {LEVER} in {manifest}")
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse(f"cannot hash {self_path}")
    if digest != pins[0]:
        refuse(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


def manifest_levers(lines, manifest):
    """The `(name, sha256)` pins under the manifest's `claude.levers.sha256` mapping, in file order (brief-check.py,
    U136): the mapping keys are walked by indentation, so `levers:` counts only under the top-level `claude:` and
    `sha256:` only under that `levers:`; inside the block, blank and comment lines are skipped, the entries share the
    indentation of the first pin, and the list ends at the first line indented less. An entry that is not
    `<name>: <64 hex>` is a refusal naming the line; no entry at all is the missing-block refusal."""
    pins = []
    keys = []  # the open mapping keys as (indentation, key), outermost first
    block = None  # the indentation of the `sha256:` key once the path is open
    entries = None  # the indentation of the pin lines, fixed by the first
    for number, line in enumerate(lines, 1):
        text = line.lstrip(" ")
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        if block is not None:
            if indent <= block or (entries is not None and indent < entries):
                break
            match = LEVER_PIN.match(text)
            if match is None or (entries is not None and indent != entries):
                refuse(f"line {number} of {manifest} is not a `<name>: <sha256>` pin under claude.levers.sha256")
            entries = indent
            pins.append((match.group(1), match.group(2)))
            continue
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if tuple(key for _, key in keys) == LEVERS_KEYS:
                block = indent
    if not pins:
        refuse(f"no claude.levers.sha256 block in {manifest}")
    return tuple(pins)


lever_self_check()


def read_text(path):
    """The whole file as strict UTF-8; a file that is missing, unreadable or not UTF-8 is a refusal naming it."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        refuse(f"{path} is missing; the report is read from the store's tables")
    except OSError as error:
        refuse(f"cannot read {path}: {error.strerror}")
    except UnicodeDecodeError as error:
        refuse(f"{path} is not UTF-8: {error.reason}")


def read_tsv(path, header):
    """The rows of a tab-separated table whose first line is exactly `header`, each row with the header's number of
    cells and no carriage return; any other shape is a refusal naming the file and the line."""
    lines = read_text(path).split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[0] != "\t".join(header):
        refuse(f"{path} does not start with the header `{' '.join(header)}`")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        if "\r" in line:
            refuse(f"line {number} of {path} holds a carriage return")
        cells = line.split("\t")
        if len(cells) != len(header):
            refuse(f"line {number} of {path} has {len(cells)} cells, not the header's {len(header)}")
        rows.append(cells)
    return rows


def elements(store):
    """One (element, signal, ok, ng, pending, rows) per `tests/*.tsv` in name order, and the operator's pending acts
    as (element, id, command) in table then file order."""
    tests = os.path.join(store, "tests")
    try:
        names = sorted(os.listdir(tests))
    except FileNotFoundError:
        refuse(f"{tests} is missing; one goal element per table is read from it")
    except OSError as error:
        refuse(f"cannot list {tests}: {error.strerror}")
    signals = []
    acts = []
    for name in names:
        if not name.endswith(".tsv"):
            continue
        element = name[: -len(".tsv")]
        rows = read_tsv(os.path.join(tests, name), TESTS_HEADER)
        verdicts = [row[8] for row in rows]
        ok = verdicts.count("OK")
        ng = verdicts.count("NG")
        pending = verdicts.count("pending")
        if rows and ok == len(rows):
            signal = "green"
        elif ng:
            signal = "red"
        elif pending:
            signal = "yellow"
        else:
            signal = "grey"
        signals.append((element, signal, ok, ng, pending, len(rows)))
        acts.extend((element, row[0], row[5]) for row in rows if row[3] == "operator" and row[8] == "pending")
    return signals, acts


def open_gates(store):
    """The (id, gate, moment, default) of every row under the gates header whose result cell is empty."""
    path = os.path.join(store, "gates.md")
    lines = read_text(path).split("\n")
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == GATES_HEADER)
    except StopIteration:
        refuse(f"{path} holds no header line `{GATES_HEADER}`")
    opened = []
    for number, line in enumerate(lines[start + 1 :], start + 2):
        text = line.strip()
        if not text.startswith("|"):
            continue
        if not text.endswith("|"):
            refuse(f"line {number} of {path} starts a table row and does not end one")
        cells = [cell.strip() for cell in text[1:-1].split("|")]
        if all(SEPARATOR_CELL.match(cell) for cell in cells):
            continue
        if len(cells) < GATES_WIDTH:
            refuse(f"line {number} of {path} has {len(cells)} cells, fewer than the header's {GATES_WIDTH}")
        result = "|".join(cells[GATES_WIDTH - 1 :]).strip("| ")
        if not result:
            opened.append((cells[0], cells[1], cells[2], cells[4]))
    return opened


def in_flight(store):
    """The (id, track, pr or -) of every `in-flight` row of units.tsv, in file order."""
    rows = read_tsv(os.path.join(store, "units.tsv"), UNITS_HEADER)
    return [(row[0], row[1], row[4] or "-") for row in rows if row[2] == "in-flight"]


def timestamp(text, what):
    try:
        return datetime.strptime(text, TS_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        refuse(f"{what} {text!r} is not <YYYY-MM-DD>T<HH:MM:SS>Z")


def last_record_age(store, now):
    """Whole minutes from the last decisions row's ts to now; a table with no row is a refusal."""
    path = os.path.join(store, "decisions.tsv")
    rows = read_tsv(path, DECISIONS_HEADER)
    if not rows:
        refuse(f"{path} holds no row; the last recorded step is read from it")
    last = timestamp(rows[-1][0], f"the last row's ts of {path}")
    return max(0, int((now - last).total_seconds() // 60))


def stall_rows(here, store, args):
    """The stall check's rows by unit as (state, age_minutes, last_line), or None when no `stall-check.py` is beside
    this lever; its exit 2 and every other failure of the run or of a row's shape is a refusal."""
    path = os.path.join(here, STALL_CHECK)
    try:
        status = os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as error:
        refuse(f"cannot stat {path}: {error.strerror}")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"{path} is not a regular file")
    command = [sys.executable, "-I", path, store]
    if args.progress_root is not None:
        command += ["--progress-root", args.progress_root]
    if args.now is not None:
        command += ["--now", args.now]
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=STALL_TIMEOUT, check=False)
    except subprocess.TimeoutExpired:
        refuse(f"{STALL_CHECK} gave no answer within {STALL_TIMEOUT} seconds")
    except OSError as error:
        refuse(f"cannot run {path}: {error.strerror}")
    first = run.stderr.strip().split("\n", 1)[0] if run.stderr.strip() else "no reason given"
    if run.returncode == 2:
        refuse(f"{STALL_CHECK} refused this report: {first}")
    if run.returncode not in (0, 1):
        refuse(f"{STALL_CHECK} exited {run.returncode}: {first}")
    rows = {}
    for number, line in enumerate(run.stdout.split("\n"), 1):
        if not line:
            continue
        cells = line.split("\t")
        if tuple(cells) == STALL_HEADER:
            continue
        if len(cells) != len(STALL_HEADER):
            refuse(f"line {number} of {STALL_CHECK}'s output has {len(cells)} cells, not {' '.join(STALL_HEADER)}")
        if cells[0] in rows:
            refuse(f"{STALL_CHECK} names the unit {cells[0]} twice")
        rows[cells[0]] = (cells[1], cells[2], cells[3])
    return rows


def progress_column(unit, rows):
    if rows is None:
        return "unknown"
    if unit not in rows:
        return "no row"
    state, age, last_line = rows[unit]
    return f"{state}, {age} min, {last_line}"


def state_word(signals, acts, opened, running, rows):
    """The word and its reason, the first matching condition in order: done, stopped (nothing in flight), stopped
    (every worker silent), moving."""
    if signals and all(signal == "green" for _, signal, *_ in signals):
        return "done", "every table green"
    if not running and (acts or opened):
        return "stopped", f"nothing in flight, waiting on {len(acts)} operator acts and {len(opened)} decisions"
    if running and rows is not None and all(unit in rows and rows[unit][0] in SILENT for unit, _, _ in running):
        return "stopped", "every in-flight worker silent"
    return "moving", f"{len(running)} units in flight"


def section(lines, heading, items):
    lines.append(heading)
    lines.extend(items or ["none"])


def report(store, here, args):
    language = "ja" if args.ja else "en"
    now = timestamp(args.now, "--now") if args.now is not None else datetime.now(timezone.utc)
    signals, acts = elements(store)
    opened = open_gates(store)
    running = in_flight(store)
    age = last_record_age(store, now)
    rows = stall_rows(here, store, args)
    word, reason = state_word(signals, acts, opened, running, rows)
    headings = HEADINGS[language]
    lines = [f"{headings[0]}: {WORDS[language][word]}: {reason}, last record {age} min ago"]
    section(
        lines,
        headings[1],
        [
            f"{element}: {signal} {ok}/{count} OK, {ng} NG, {pending} pending"
            for element, signal, ok, ng, pending, count in signals
        ],
    )
    section(lines, headings[2], [f"{element} {row_id}: {command}" for element, row_id, command in acts])
    section(
        lines,
        headings[3],
        [f"{gate_id}: {gate} ({moment}; default {default})" for gate_id, gate, moment, default in opened],
    )
    section(
        lines,
        headings[4],
        [f"{unit} {track} pr {pr} progress: {progress_column(unit, rows)}" for unit, track, pr in running],
    )
    return "\n".join(lines) + "\n"


def parser():
    top = argparse.ArgumentParser(prog=LEVER, description=__doc__.splitlines()[0])
    top.add_argument("store", help="the program store directory (tests/, gates.md, units.tsv, decisions.tsv)")
    top.add_argument("--ja", action="store_true", help="the five headings and the state word in the operator's forms")
    top.add_argument("--now", help="the clock as <YYYY-MM-DD>T<HH:MM:SS>Z, for the ages and the stall check")
    top.add_argument("--progress-root", help="passed through to stall-check.py")
    return top


def main(argv=None):
    args = parser().parse_args(sys.argv[1:] if argv is None else list(argv))
    if args.now is not None:
        timestamp(args.now, "--now")
    store = os.path.realpath(args.store)
    try:
        status = os.lstat(store)
    except OSError as error:
        refuse(f"the store {store} cannot be read: {error.strerror}")
    if not stat.S_ISDIR(status.st_mode):
        refuse(f"the store {store} is not a directory")
    here = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    sys.stdout.write(report(store, here, args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
