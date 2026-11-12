#!/usr/bin/env -S python3 -I
"""Name every in-flight worker of a program store that is silent past its deadline (regime-cutover U496).

Measured 2026-11-06 to 2026-11-12: eleven worker stalls, each a Task subagent silent after a tool call for 30 to 45
minutes, each found because the coordinator remembered to read the progress files by hand (standing order 57). This
lever is that reading as a command: `stall-check.py <store> [--progress-root <dir>] [--deadline-minutes <n>]
[--now <ts>]` reads the store's `units.tsv`, takes every row whose `state` cell is `in-flight` and whose `track` is not
`sweep` (a sweep seat reports on the bus, not in a file), reads each unit's progress file
`<progress-root>/<unit>-progress.txt` and prints one row per unit, in the register's order, tab-separated:

    unit<TAB>state<TAB>age_minutes<TAB>last_line

the contract `program-status.py` (U497) reads; nothing else goes to stdout, and the rows go out together at the end,
so a refusal leaves stdout empty. A progress file is an append-only text file whose lines start with an ISO-8601 UTC
timestamp `YYYY-MM-DDTHH:MM:SSZ`, a space and free text; the last line decides. The states, one table (STATES):

- `moving`: the last line's age in whole minutes is at most `--deadline-minutes` (default 10);
- `stalled`: older;
- `done`: the last line's text after the timestamp starts with `done,`, or with the row's own unit id, a space and
  `done,` (the form the workers write, `U495 done, head=<sha>`, measured 2026-11-12); the age is printed as well;
- `no-file`: no progress file at the path, the worker never wrote its first line; `age_minutes` and `last_line` are
  `-`, and the row counts as a stall;
- `unreadable`: a file that exists but cannot be read (a directory, a link, a mode that denies the read, bytes that
  are not UTF-8), or whose last line carries no timestamp of the form, no space after it, a date that is none, or a
  time after the clock: a refusal of the run naming the file and the unit, never a row and never a guess.

`age_minutes` is the integer floor of the age in minutes, the number the state is judged by, so a printed `10` is
moving under the default and `11` is stalled; a tab or a carriage return inside the worker's free text is one space in
the cell, so the row keeps its four cells. `--now <ts>` injects the clock in the lines' own form (tests; the default is
the UTC wall clock). The progress root defaults to `/tmp/<slug>-wt`, `<slug>` the store path's parent directory name
(`dotfiles` for `.../regime-store/dotfiles/regime-cutover`, the worktree root `worker-worktree.sh` uses).

Exit 0 when every row is `moving` or `done` (an empty in-flight set prints nothing and is 0); exit 1 when any row is
`stalled` or `no-file`; exit 2 with one stderr line, `stall-check.py: refused: <reason>`, and nothing on stdout for every
refusal (standing order 21, fail closed on every producer): a `units.tsv` that is absent, cannot be read, is not UTF-8,
has not the header `id track state branch pr head_sha brief note` tab-separated, has a row of other than eight cells,
a row holding a carriage return, or a row whose id is not `U<n>` or `U<n><letter>` (the id names the file read, so no
other shape reaches a path); an unreadable progress file as above; a bad `--now` or `--deadline-minutes` (a decimal
count of minutes, `0` or without a leading zero); a store or progress root that is not an absolute path, holds an
empty, `.` or `..` component (a trailing or repeated separator included), or is not a directory once resolved (a
missing progress root is a wrong root, never an empty set of workers); any argument that is not strict UTF-8 or holds
a tab, a newline or a carriage return; and argparse's own usage errors, printed in the same one-line form. Every file
under the store or the root is reached by one path rule (`ledger-row.py`'s): the root is its own realpath, each
component below it is `os.lstat`ed and none is a symbolic link, and the end is a regular file. No file is written and
no mode is changed.

Before anything else the file hashes itself against its `claude.levers.sha256.stall-check.py` pin in the manifest
beside it (the deployed `~/.agents/agent-config.yaml` for the copy under the physical `~/.local/bin/common`, else the
checkout's `home/dot_agents/agent-config.yaml` two levels up) and refuses to run when the digest differs, in the form
`brief-check.py` uses; `python3 -I` ignores the script directory and the PYTHON* variables, so no planted module
answers first. Installed as `~/.local/bin/common/stall-check.py` by the generator's copy and pin and allowed by the
orchestrator policy at that path; `tests/unit/test_stall_check.py` runs it as a subprocess over a scratch store.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
from datetime import datetime, timezone

LEVER = "stall-check.py"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py, U136).
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")

# The register's one header, as pr-merge.sh and brief-check.py read it; every row has its eight cells.
HEADER = ("id", "track", "state", "branch", "pr", "head_sha", "brief", "note")
IN_FLIGHT = "in-flight"
SWEEP = "sweep"
# A unit id, the body's `U<n>` or a fix unit `U<n><letter>` (standing order 24): the one shape that names a file.
UNIT = re.compile(r"^U[0-9]+[a-z]?$")
DIGITS = re.compile(r"^(0|[1-9][0-9]*)$")
# The progress lines' clock: an ISO-8601 UTC timestamp, then one space, then the worker's free text.
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TS_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PROGRESS_LINE = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (.*)$", re.DOTALL)
DEADLINE_MINUTES = 10
DONE_PREFIX = "done,"
# The three characters no argument holds: the output is tab-separated lines.
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))

# The states, one table: the state word and the exit code a row of it contributes; `unreadable` is a refusal of the
# run (exit 2 through `refuse`, nothing printed), so it never reaches a row.
MOVING, STALLED, DONE, NO_FILE, UNREADABLE = "moving", "stalled", "done", "no-file", "unreadable"
STATES = {MOVING: 0, DONE: 0, STALLED: 1, NO_FILE: 1, UNREADABLE: 2}


class Unreadable(Exception):
    """A file that exists but yields no text: the reason, for the caller to name with the file and the unit."""


def refuse(reason):
    """Print the refusal in the shell levers' words on stderr and exit 2; nothing was printed on stdout."""
    print(f"{LEVER}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `stall-check.py`
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


class Parser(argparse.ArgumentParser):
    """argparse with its usage errors in the lever's one-line refusal form (exit 2, nothing on stdout)."""

    def error(self, message):
        refuse(message)


def parser():
    top = Parser(prog=LEVER, description=__doc__.splitlines()[0])
    top.add_argument("store", help="the program store directory holding units.tsv")
    top.add_argument(
        "--progress-root",
        help="the directory of the <unit>-progress.txt files (default /tmp/<slug>-wt, the slug the store's parent name)",
    )
    top.add_argument(
        "--deadline-minutes",
        default=str(DEADLINE_MINUTES),
        help=f"the age in whole minutes a moving worker's last line may have (default {DEADLINE_MINUTES})",
    )
    top.add_argument("--now", help="the clock, YYYY-MM-DDTHH:MM:SSZ (default the UTC wall clock)")
    return top


def argument_rule(argv):
    """The one rule every element of argv passes before argparse runs (ledger-row.py's): the element round-trips
    through strict UTF-8 (Python decodes argv with surrogateescape) and holds neither a tab, a newline nor a carriage
    return. The refusal names the element's position."""
    for index, value in enumerate(argv, 1):
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as error:
            refuse(f"argument {index} holds a byte that is not UTF-8 at offset {error.start}: {value!r}")
        for character, label in CONTROL:
            if character in value:
                refuse(f"argument {index} holds {label}; the output is tab-separated lines")


def clock(value):
    """The clock as an aware UTC datetime: `--now` in the progress lines' own form, else the wall clock."""
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0)
    if not TS_SHAPE.match(value):
        refuse(f"--now {value!r} is not a timestamp of the form YYYY-MM-DDTHH:MM:SSZ")
    try:
        return datetime.strptime(value, TS_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        refuse(f"--now {value!r} is no date")


def deadline(value):
    if not DIGITS.match(value):
        refuse(f"--deadline-minutes {value!r} is not a decimal count of minutes")
    return int(value)


def clean_directory(given, label):
    """A clean absolute path (no empty, `.` or `..` component, so no trailing or repeated separator), resolved to its
    realpath by this lever alone, and a directory there; any other outcome is a refusal naming the argument."""
    parts = given.split("/")
    if parts[0] != "" or len(parts) < 2:
        refuse(f"the {label} {given!r} is not an absolute path")
    for part in parts[1:]:
        if part in ("", ".", ".."):
            refuse(
                f"the {label} {given!r} is not a clean path: an empty, `.` or `..` component (a trailing separator included)"
            )
    real = os.path.realpath(given)
    try:
        status = os.lstat(real)
    except OSError as error:
        refuse(f"the {label} {given!r} ({real}) cannot be read: {error.strerror}")
    if not stat.S_ISDIR(status.st_mode):
        refuse(f"the {label} {given!r} ({real}) is not a directory")
    return real


def default_root(store):
    """`/tmp/<slug>-wt`, the slug the resolved store path's parent directory name (`dotfiles` for
    `.../regime-store/dotfiles/regime-cutover`), held like a given root."""
    slug = os.path.basename(os.path.dirname(store))
    if not slug:
        refuse(f"the store {store} has no parent directory name to derive the progress root from")
    return clean_directory(f"/tmp/{slug}-wt", "progress root")


def held_file(root, name, label):
    """The regular file `<root>/<name>` by the levers' one path rule (ledger-row.py's `store_file`): `root` is its own
    realpath, the component is `os.lstat`ed and no link, the end a regular file. Returns None when there is no entry
    (the caller's `no-file` or absence refusal); every other outcome but a regular file is a refusal naming the path."""
    path = os.path.join(root, name)
    try:
        status = os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as error:
        refuse(f"the {label} {path} cannot be read: {error.strerror}")
    if stat.S_ISLNK(status.st_mode):
        refuse(f"the {label} {path} is a symbolic link; a file under the root is read through real entries alone")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the {label} {path} is not a regular file")
    return path


def file_text(path):
    """The file's whole text, strict UTF-8; a read or a decode that fails raises Unreadable with the reason."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as error:
        raise Unreadable(error.strerror or str(error)) from None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Unreadable(f"not UTF-8: {error.reason}") from None


def in_flight_units(store):
    """The ids of the register's in-flight rows that are not sweep seats, in file order, after the whole register
    passes its grammar: the header, eight cells per row, no carriage return, every id a unit id."""
    path = held_file(store, "units.tsv", "register")
    if path is None:
        refuse(f"the register {os.path.join(store, 'units.tsv')} is absent")
    try:
        text = file_text(path)
    except Unreadable as error:
        refuse(f"the register {path} cannot be read: {error}")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # the trailing newline of the last row
    header = "\t".join(HEADER)
    if not lines or lines[0] != header:
        refuse(f"the register {path} has not the header `{' '.join(HEADER)}` tab-separated")
    units = []
    for number, line in enumerate(lines[1:], 2):
        if "\r" in line:
            refuse(f"line {number} of the register {path} holds a carriage return")
        cells = line.split("\t")
        if len(cells) != len(HEADER):
            refuse(f"line {number} of the register {path} has {len(cells)} cells, not {len(HEADER)}")
        unit, track, state = cells[0], cells[1], cells[2]
        if not UNIT.match(unit):
            refuse(f"line {number} of the register {path}: the id {unit!r} is not U<n> or U<n><letter>")
        if state == IN_FLIGHT and track != SWEEP:
            units.append(unit)
    return units


def judge(root, unit, now, limit):
    """The unit's row as (state, age text, last line text) from its progress file under the root: `no-file` for no
    entry; an unreadable file, or a last line outside the grammar, a refusal naming the file and the unit."""
    name = f"{unit}-progress.txt"
    path = held_file(root, name, f"progress file of {unit}")
    if path is None:
        return NO_FILE, "-", "-"
    try:
        text = file_text(path)
    except Unreadable as error:
        refuse(f"the progress file {path} of {unit} is {UNREADABLE}: {error}")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        refuse(f"the progress file {path} of {unit} is {UNREADABLE}: it is empty")
    last = lines[-1]
    match = PROGRESS_LINE.match(last)
    if match is None:
        refuse(
            f"the progress file {path} of {unit} is {UNREADABLE}: its last line carries no `YYYY-MM-DDTHH:MM:SSZ ` prefix"
        )
    try:
        written = datetime.strptime(match.group(1), TS_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        refuse(
            f"the progress file {path} of {unit} is {UNREADABLE}: its last line's timestamp {match.group(1)} is no date"
        )
    seconds = (now - written).total_seconds()
    if seconds < 0:
        refuse(
            f"the progress file {path} of {unit} is {UNREADABLE}: its last line's timestamp {match.group(1)} is after the "
            f"clock {now.strftime(TS_FORMAT)}"
        )
    age = int(seconds // 60)
    body = match.group(2)
    if body.startswith(DONE_PREFIX) or body.startswith(f"{unit} {DONE_PREFIX}"):
        state = DONE
    elif age <= limit:
        state = MOVING
    else:
        state = STALLED
    return state, str(age), last.replace("\t", " ").replace("\r", " ")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    argument_rule(argv)
    args = parser().parse_args(argv)
    now = clock(args.now)
    limit = deadline(args.deadline_minutes)
    store = clean_directory(args.store, "store")
    root = default_root(store) if args.progress_root is None else clean_directory(args.progress_root, "progress root")
    rows = []
    code = 0
    for unit in in_flight_units(store):
        state, age, last = judge(root, unit, now, limit)
        rows.append(f"{unit}\t{state}\t{age}\t{last}\n")
        code = max(code, STATES[state])
    sys.stdout.write("".join(rows))
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    lever_self_check()
    sys.exit(main())
