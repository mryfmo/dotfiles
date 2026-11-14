#!/usr/bin/env -S python3 -I
"""Name every in-flight worker of a program store that is silent past its deadline (regime-cutover U496, round 2 U496b,
round 3 U496c and U496d, round 4 U496e, round 5 the bare done line and the `malformed` row, round 7 U496h the refusal
printer's fold).

Measured 2026-11-06 to 2026-11-12: eleven worker stalls, each a Task subagent silent after a tool call for 30 to 45
minutes, each found because the coordinator remembered to read the progress files by hand (standing order 57). This
lever is that reading as a command: `stall-check.py <store> [--progress-root <dir>] [--deadline-minutes <n>]
[--now <ts>]` reads the store's `units.tsv`, takes every row whose `state` cell is `in-flight` and whose `track` is not
`sweep` (a sweep seat reports on the bus, not in a file), reads each unit's progress file
`<progress-root>/<unit>-progress.txt` and prints one row per unit, in the register's order, tab-separated:

    unit<TAB>state<TAB>age_minutes<TAB>last_line

the contract `program-status.py` (U497) reads; nothing else goes to stdout, and the rows go out together at the end,
so a refusal leaves stdout empty. A progress file is an append-only text file whose lines start with an ISO-8601 UTC
timestamp `YYYY-MM-DDTHH:MM:SSZ`, a space and free text, and may end with the bare completion line the coordinator's
worker contract prescribes, `done, head=<40 hex>` with no timestamp (round 5, Codex review P1 of round 1's `:342`,
still refused at ad3128dc: the workers write exactly that line, U516c and U512b measured 2026-11-13); the last line
decides. The states, one table (STATES):

- `moving`: the last line's age in whole minutes is at most `--deadline-minutes` (default 10);
- `stalled`: older;
- `done`: the last line's text after the timestamp starts with `done,`, or with the row's own unit id, a space and
  `done,` (the form the workers write, `U495 done, head=<sha>`, measured 2026-11-12); or the last line is the bare
  `done, head=<40 hex>` (BARE_DONE, exactly that), whose age is the preceding timestamped line's, the last line before
  it that has the timestamp and the space; the age is printed as well;
- `no-file`: no progress file at the path, the worker never wrote its first line; `age_minutes` and `last_line` are
  `-`, and the row counts as a stall;
- `unreadable`: that one unit's row, `age_minutes` and `last_line` `-`, never a refusal that hides every other unit
  (verdict U496-d1256438 P1; the one run-level refusal a file earns is a store that cannot be read): the file yields
  no text (a directory, a link, a FIFO, a device or a socket at the name, a mode that denies the read, bytes that are
  not UTF-8); the row's exit code is 2;
- `malformed`: that one unit's row as well (round 5: one worker's file never hides another's stall), `age_minutes`
  `-` and `last_line` the reason folded to one line, the worker's own line after a colon where there is one, so the
  coordinator sees what the worker wrote: the file is empty, its last line is blank, carries no timestamp of the
  form and a space (the bare `U<n> done, head=<sha>` without a timestamp, or any other text), a date that is none or
  a time after the clock; or it is the bare done line with no timestamped line before it, or with one whose date is
  none or whose time is after the clock. The row's exit code is 2.

`age_minutes` is the integer floor of the age in minutes, the number the state is judged by, so a printed `10` is
moving under the default and `11` is stalled; a tab or a carriage return inside the worker's free text is one space in
the cell, so the row keeps its four cells. `--now <ts>` injects the clock in the lines' own form (tests; the default is
the UTC wall clock). The progress root defaults to the temporary directory (`$TMPDIR` when it is set and not empty,
else the system default) plus `<slug>-wt`, `<slug>` the parent directory name of the store path as given, cleaned and
not resolved (`dotfiles` for `.../regime-store/dotfiles/regime-cutover`, whatever that `dotfiles` is a link to: the
root the operator sees, verdict U496-8cdd9a40 P2 :476), the worktree root `worker-worktree.sh` uses, read in one
statement by the spelling `tests/unit/test_sandbox_portability.py` sanctions (round 3, U496c: CI's portability guard
refuses a spelled temporary path, and the sandbox's writable temporary directory is `$TMPDIR`).

Exit 0 when every row is `moving` or `done` (an empty in-flight set prints nothing and is 0); exit 1 when any row is
`stalled` or `no-file`; exit 2 when any row is `unreadable` or `malformed` (the rows printed first, the code the
maximum over the rows), and
exit 2 with one stderr line, `stall-check.py: refused: <reason>`, and nothing on stdout for every refusal (standing
order 21, fail closed on every producer): a `units.tsv` that is absent, cannot be read or opened, is a link or no
regular file, is not UTF-8, has not the header `id track state branch pr head_sha brief note` tab-separated, has a row
of other than eight cells, a row holding a carriage return, or a row whose id is not `U<n>` or `U<n><letter>` (the id
names the file read, so no other shape reaches a path); a bad `--now`; a `--deadline-minutes` that is not 1 to 10
decimal digits without a leading zero (judged as text before `int()` sees it: a 4301-digit value raised `int()`'s
digit limit as a traceback, verdict U496-d1256438 P2) or is outside 1 to 1440 (24 hours), the bound every integer
option of this lever shares; a store or progress root that is not an absolute path, holds an empty, `.` or `..`
component (a trailing or repeated separator included), or is not a real directory entry at the end of its walk (a
missing progress root is a wrong root, never an empty set of workers); any argument that is not strict UTF-8 or holds
a tab, a newline or a carriage return; and argparse's own usage errors, printed in the same one-line form. The printer
folds every line boundary `str.splitlines` knows (newline, carriage return, VT, FF, FS, GS, RS, NEL, U+2028, U+2029)
inside the reason to a space before it writes, so a walked path whose link target holds one (an argument never does,
`argument_rule` refuses it; a target is read from the file system) is still one stderr line (round 7, U496h, verdict
U496f-0eecc2a9 P3).

Every path is walked by descriptors from `/` (round 4, U496e; verdict U496-8cdd9a40 P1 :319: every earlier round
validated the root by path and then opened it by path, so an ancestor replaced by a symbolic link between the two was
followed through, `O_NOFOLLOW` guarding the last component alone). `held_path` opens `/` once and then each component
of the cleaned path on the previous directory's descriptor, `os.open(name, flags, dir_fd=fd)` with
`O_RDONLY | O_NOFOLLOW | O_CLOEXEC` and `O_DIRECTORY` for every step but a file leaf, each judged by `os.fstat` on its
own descriptor, the previous descriptor closed once the next is held. A component the kernel refuses as a link (ELOOP;
ENOTDIR under `O_DIRECTORY` on macOS) is read with `os.readlink(name, dir_fd=fd)` and its target's components are
walked the same way, from `/` when the target is absolute, else on the held directory (`.` skipped, `..` opened as the
held directory's own parent), at most LINK_HOPS links on one walk; so the temporary directory's links on macOS (`tmp`
and `var` under `/` point into `private`) and an aliased store parent are followed as the kernel would follow them, on
descriptors the lever holds and never through a path string. The leaf, the store or the progress root, is a real
directory entry: a link there is a refusal, as it is for every file below it. The leaf's descriptor is the held
directory, and once the walk has begun no path string, `realpath` or `lstat` reaches the kernel. Every file below it
is its bare entry name (`units.tsv`, `<unit>-progress.txt`, no separator) opened on that descriptor by the same step
with `O_RDONLY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK` and judged by `os.fstat` on its descriptor a regular file (a link
is ELOOP; a FIFO, a device or a socket at the name cannot hold the open under `O_NONBLOCK`, verdict U496-8cdd9a40 P1
:359: a regular file swapped for a FIFO held the blocking `os.open` until an alarm; either is that unit's `unreadable`
row or the register's refusal), `O_NONBLOCK` cleared with `fcntl` before the text is read from that descriptor, never
from a path (verdict U496-d1256438 P1 :281). The lever judges the entry it holds: a regular file at the unit's name is
that unit's progress file whatever path it had before. A platform whose `os.open` or `os.readlink` lacks `dir_fd`
(judged once at import by `os.supports_dir_fd`; macOS and Linux have it) is a refusal naming it. No file is written
and no mode is changed.

Before anything else the file hashes itself against its `claude.levers.sha256.stall-check.py` pin in the manifest
beside it (the deployed `~/.agents/agent-config.yaml` for the copy under the physical `~/.local/bin/common`, else the
checkout's `home/dot_agents/agent-config.yaml` two levels up) and refuses to run when the digest differs, in the form
`brief-check.py` uses; `python3 -I` ignores the script directory and the PYTHON* variables, so no planted module
answers first. Installed as `~/.local/bin/common/stall-check.py` by the generator's copy and pin and allowed by the
orchestrator policy at that path; `tests/unit/test_stall_check.py` runs it as a subprocess over a scratch store.
"""

from __future__ import annotations

import argparse
import errno
import fcntl
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
# A bare entry name under a held directory (`units.tsv`, `<unit>-progress.txt`): no separator, not `.` or `..`, so
# every open through `dir_fd` names one entry of that directory and nothing above or beside it.
ENTRY_NAME = re.compile(r"^(?!\.\.?$)[^/]+$")
# `--deadline-minutes`: 1 to 10 decimal digits without a leading zero, judged as text before `int()` sees it, then the
# bound every integer option of this lever shares, 1 to BOUNDED_MINUTES (24 hours).
DEADLINE_SHAPE = re.compile(r"^(0|[1-9][0-9]{0,9})$")
BOUNDED_MINUTES = 1440
# The progress lines' clock: an ISO-8601 UTC timestamp, then one space, then the worker's free text.
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
TS_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PROGRESS_LINE = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (.*)$", re.DOTALL)
TS_PREFIX = "YYYY-MM-DDTHH:MM:SSZ"
DEADLINE_MINUTES = 10
DONE_PREFIX = "done,"
# The bare completion line the worker contract prescribes, exactly: no timestamp, `done, head=` and the 40-hex sha.
BARE_DONE = re.compile(r"^done, head=[0-9a-f]{40}$")
# The three characters no argument holds: the output is tab-separated lines.
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))
# The line boundaries `str.splitlines` knows; `one_line` replaces each with a space in every refusal, so a walked path
# (a link target, never an argument) that holds one prints as one stderr line (round 7, U496h).
LINE_BREAK = re.compile(r"[\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]")

# The states, one table: the state word and the exit code a row of it contributes; `unreadable` (a file that yields no
# text, round 2, U496b) and `malformed` (text outside the grammar, round 5) are one unit's row of exit 2, while a
# refusal (exit 2 through `refuse`, nothing printed) is the store's alone.
MOVING, STALLED, DONE, NO_FILE, UNREADABLE, MALFORMED = (
    "moving",
    "stalled",
    "done",
    "no-file",
    "unreadable",
    "malformed",
)
STATES = {MOVING: 0, DONE: 0, STALLED: 1, NO_FILE: 1, UNREADABLE: 2, MALFORMED: 2}
# The two kinds of leaf a walk ends at: the held directory (the store, the progress root) or a regular file.
DIRECTORY, REGULAR = "directory", "regular file"
# Symbolic links followed on one walk before it refuses: macOS's MAXSYMLINKS; Linux allows 40.
LINK_HOPS = 32
# The kind of entry a mode describes, for the reasons; the first test that holds names it.
KINDS = (
    (stat.S_ISDIR, "a directory"),
    (stat.S_ISLNK, "a symbolic link"),
    (stat.S_ISFIFO, "a FIFO"),
    (stat.S_ISSOCK, "a socket"),
    (stat.S_ISCHR, "a device"),
    (stat.S_ISBLK, "a device"),
    (stat.S_ISREG, "a regular file"),
)
# The relative opens and the link reads need `dir_fd` on `os.open` and `os.readlink`, judged once at import (the run
# refuses without it).
DIR_FD_SUPPORTED = {os.open, os.readlink} <= os.supports_dir_fd


class Unreadable(Exception):
    """A file that exists but yields no held text: the reason as a verb phrase (`is a symbolic link`, `cannot be
    read: ...`), for the caller to name after the file, or to fold into the unit's `unreadable` row."""


class Malformed(Exception):
    """A progress file whose text is outside the grammar: the reason as one line (`the file is empty`, `the last
    line has no YYYY-MM-DDTHH:MM:SSZ timestamp and a space before its text: <line>`), the unit's `malformed` row's
    line cell."""


def one_line(text):
    """`text` with every line boundary `str.splitlines` knows (newline, carriage return, VT, FF, FS, GS, RS, NEL,
    U+2028, U+2029) replaced by a space, so a refusal is one stderr line whatever a walked path holds."""
    return LINE_BREAK.sub(" ", text)


def refuse(reason):
    """Print the refusal in the shell levers' words on stderr and exit 2; nothing was printed on stdout. The reason is
    folded to one line (`one_line`): the arguments are clean by `argument_rule`, but a walked path is read from the
    file system and an ancestor link's target may hold a newline (verdict U496f-0eecc2a9 P3)."""
    print(f"{LEVER}: refused: {one_line(reason)}", file=sys.stderr)
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
        help=(
            "the directory of the <unit>-progress.txt files (default: the temporary directory, $TMPDIR else the system"
            " default, plus <slug>-wt, the slug the store's parent name)"
        ),
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
    """`--deadline-minutes` as an int: DEADLINE_SHAPE on the text first, so `int()` never sees a value of more digits
    than it converts (the 4301-digit traceback of verdict U496-d1256438 P2), then 1 to BOUNDED_MINUTES. A long value is
    named by its first characters and its length, so the refusal stays one line."""
    shown = repr(value) if len(value) <= 20 else f"{value[:20]!r}... ({len(value)} characters)"
    if not DEADLINE_SHAPE.match(value):
        refuse(f"--deadline-minutes {shown} is not a decimal count of minutes of 1 to 10 digits without a leading zero")
    minutes = int(value)
    if not 1 <= minutes <= BOUNDED_MINUTES:
        refuse(f"--deadline-minutes {shown} is outside 1 to {BOUNDED_MINUTES} (24 hours)")
    return minutes


def clean_directory(given, label):
    """A clean absolute path as text (no empty, `.` or `..` component, so no trailing or repeated separator), the text
    grammar alone: no `realpath`, no `lstat`, nothing of the path reaches the kernel here, since `held_root` walks it by
    descriptors (round 4, U496e); any other shape is a refusal naming the argument."""
    parts = given.split("/")
    if parts[0] != "" or len(parts) < 2:
        refuse(f"the {label} {given!r} is not an absolute path")
    for part in parts[1:]:
        if part in ("", ".", ".."):
            refuse(
                f"the {label} {given!r} is not a clean path: an empty, `.` or `..` component (a trailing separator included)"
            )
    return given


def default_root(store):
    """The temporary directory (`$TMPDIR` when set and not empty, else the system default, the `${TMPDIR:-...}` rule
    `worker-worktree.sh` applies) plus `<slug>-wt`, the slug the parent directory name of the store path as given,
    cleaned and not resolved (`dotfiles` for `.../regime-store/dotfiles/regime-cutover`, whatever that `dotfiles` is a
    link to: the root the operator sees and the workers write, verdict U496-8cdd9a40 P2 :476), cleaned like a given
    root; the walk and the refusal naming it are `held_root`'s."""
    slug = os.path.basename(os.path.dirname(store))
    if not slug:
        refuse(f"the store {store} has no parent directory name to derive the progress root from")
    root = os.path.join(os.environ.get("TMPDIR") or "/tmp", f"{slug}-wt")
    return clean_directory(root, "progress root")


def kind_of(mode):
    """The kind of entry `mode` describes, in the reasons' words (KINDS), `no regular file` for any other."""
    for test, kind in KINDS:
        if test(mode):
            return kind
    return "no regular file"


def held_step(dir_fd, name, kind):
    """One entry `name` of the held directory `dir_fd` (None for `/` itself) opened on that descriptor and judged by
    `os.fstat` on its own: a DIRECTORY step opens with `O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC`; the REGULAR
    leaf with `O_RDONLY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK`, so a FIFO or a device at the name cannot hold the open
    (verdict U496-8cdd9a40 P1 :359), and `O_NONBLOCK` is cleared with `fcntl` once `fstat` has shown a regular file.
    Returns the descriptor. An `os.open` that fails raises its OSError unchanged (the walker reads a link on ELOOP or
    ENOTDIR, the callers name ENOENT and ELOOP); a descriptor of another kind, or an `fstat` or `fcntl` that fails,
    raises Unreadable with the reason, the descriptor closed."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
    flags |= os.O_DIRECTORY if kind == DIRECTORY else os.O_NONBLOCK
    descriptor = os.open(name, flags, dir_fd=dir_fd)
    try:
        held = os.fstat(descriptor)
        if kind == DIRECTORY:
            if not stat.S_ISDIR(held.st_mode):
                raise Unreadable("is not a directory")
        else:
            if not stat.S_ISREG(held.st_mode):
                raise Unreadable(f"is {kind_of(held.st_mode)}, not a regular file")
            fcntl.fcntl(descriptor, fcntl.F_SETFL, fcntl.fcntl(descriptor, fcntl.F_GETFL) & ~os.O_NONBLOCK)
    except OSError as error:
        os.close(descriptor)
        raise Unreadable(f"cannot be read: {error.strerror or error}") from None
    except Unreadable:
        os.close(descriptor)
        raise
    return descriptor


def held_slash():
    """The descriptor on `/`, the one step every walk starts from; a `/` that cannot be held is Unreadable naming it."""
    try:
        return held_step(None, "/", DIRECTORY)
    except OSError as error:
        raise Unreadable(f"(/) cannot be read: {error.strerror or error}") from None


def link_target(dir_fd, name, error):
    """The target text of the link `name` under `dir_fd` when `error`, the OSError of its open, is the kernel's
    refusal of a link (ELOOP; ENOTDIR under `O_DIRECTORY` on macOS) and `os.readlink` on the held directory reads it;
    None when the entry is no link (the open's error stands) or has gone."""
    if error.errno not in (errno.ELOOP, errno.ENOTDIR):
        return None
    try:
        return os.readlink(name, dir_fd=dir_fd)
    except OSError:
        return None


def open_reason(error):
    """The reason an open's OSError gives a step that is no link: `is not a directory` for ENOTDIR, else the kernel's."""
    if error.errno == errno.ENOTDIR:
        return "is not a directory"
    return f"cannot be read: {error.strerror or error}"


def held_path(given, leaf_kind):
    """The walk (round 4, U496e): `given` is a clean absolute path (`clean_directory`'s text) and `leaf_kind` DIRECTORY
    or REGULAR. `/` is opened once, then each component on the previous directory's descriptor by `held_step` (every
    step but the leaf a directory), the previous descriptor closed once the next is held, so a change to the path above
    a held component reaches nothing the lever reads (verdict U496-8cdd9a40 P1 :319). A component the kernel refuses as
    a link is read with `os.readlink` on the held directory and its target's components are walked the same way: from
    `/` when the target is absolute, else on the held directory, `.` skipped and `..` opened as the held directory's
    own parent, at most LINK_HOPS links on one walk; the leaf is a real entry, a link there a refusal. Returns
    `(descriptor, walked)`, `walked` the text of the path the descriptors walked (the given path with every link
    replaced by what it held, named in the refusals beside the given text); raises Unreadable `(<walked>) <reason>` with
    every descriptor closed."""
    pending = given.split("/")[1:]
    walked = ""
    hops = 0
    descriptor = held_slash()
    try:
        while pending:
            name = pending.pop(0)
            if name in ("", "."):
                continue  # a link target's empty or `.` component
            leaf = all(part in ("", ".") for part in pending)
            try:
                held = held_step(descriptor, name, leaf_kind if leaf else DIRECTORY)
            except Unreadable as error:
                raise Unreadable(f"({walked}/{name}) {error}") from None
            except OSError as error:
                target = link_target(descriptor, name, error)
                if target is None:
                    raise Unreadable(f"({walked}/{name}) {open_reason(error)}") from None
                if leaf:
                    raise Unreadable(
                        f"({walked}/{name}) is a symbolic link; the held {leaf_kind} is a real entry (its ancestors the"
                        " walk follows)"
                    ) from None
                hops += 1
                if hops > LINK_HOPS:
                    raise Unreadable(
                        f"({walked}/{name}) is the link past LINK_HOPS ({LINK_HOPS}) on one walk; too many levels of"
                        " symbolic links"
                    ) from None
                parts = target.split("/")
                if parts[0] == "":
                    os.close(descriptor)
                    descriptor = None
                    descriptor = held_slash()
                    walked = ""
                    pending = parts[1:] + pending
                else:
                    pending = parts + pending
                continue
            os.close(descriptor)
            descriptor = held
            walked = walked.rpartition("/")[0] if name == ".." else f"{walked}/{name}"
    except BaseException:
        if descriptor is not None:
            os.close(descriptor)
        raise
    return descriptor, walked


def held_root(given, label):
    """`(descriptor, walked)` of the directory `given` (the store or the progress root, `clean_directory`'s text) by
    `held_path`; a platform without `dir_fd` on `os.open` or `os.readlink`, or a walk that ends anywhere but at a real
    directory entry, is a refusal naming the argument as given and as walked."""
    if not DIR_FD_SUPPORTED:
        refuse("this platform's os.open or os.readlink lacks dir_fd; the paths cannot be walked by descriptors")
    try:
        return held_path(given, DIRECTORY)
    except Unreadable as error:
        refuse(f"the {label} {given!r} {error}")


def held_file(root_fd, name):
    """An open read-only descriptor on the regular file `name` under the held directory `root_fd` by the walk's own
    step: `name` is a bare entry name (no separator), opened on the descriptor with
    `O_RDONLY | O_NOFOLLOW | O_CLOEXEC | O_NONBLOCK` (no path is looked up; a link at the name is ELOOP; a FIFO or a
    device cannot hold the open, verdict U496-8cdd9a40 P1 :359) and judged by `os.fstat` on its descriptor a regular
    file, `O_NONBLOCK` then cleared; the caller reads this descriptor and never a path (verdict U496-d1256438 P1 :281).
    The lever judges the entry it holds: a regular file at the name is the file, whatever path it had before (round 2's
    `lstat` before the open and its inode match are gone with the walk; they saw no swap made before the `lstat`
    either). Returns None when there is no entry (the caller's `no-file` or absence refusal); every other outcome but
    the held regular file raises Unreadable with the reason, the descriptor closed."""
    if not ENTRY_NAME.match(name):
        raise Unreadable("is not a bare entry name under the held directory")
    try:
        return held_step(root_fd, name, REGULAR)
    except FileNotFoundError:
        return None
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise Unreadable("is a symbolic link; a file under the root is read through real entries alone") from None
        raise Unreadable(f"cannot be opened: {error.strerror or error}") from None


def file_text(descriptor):
    """The whole text behind the held descriptor, strict UTF-8, the descriptor closed either way; a read or a decode
    that fails raises Unreadable with the reason."""
    try:
        with os.fdopen(descriptor, "rb") as handle:
            data = handle.read()
    except OSError as error:
        raise Unreadable(f"cannot be read: {error.strerror or error}") from None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Unreadable(f"is not UTF-8: {error.reason}") from None


def cell(text):
    """The worker's free text as one cell of a tab-separated row: a tab or a carriage return is one space."""
    return text.replace("\t", " ").replace("\r", " ")


def in_flight_units(store, store_fd):
    """The ids of the register's in-flight rows that are not sweep seats, in file order, after the whole register
    passes its grammar: the header, eight cells per row, no carriage return, every id a unit id. The register is read
    relative to the held store descriptor; `store` names it in the refusals."""
    path = os.path.join(store, "units.tsv")
    try:
        descriptor = held_file(store_fd, "units.tsv")
    except Unreadable as error:
        refuse(f"the register {path} {error}")
    if descriptor is None:
        refuse(f"the register {path} is absent")
    try:
        text = file_text(descriptor)
    except Unreadable as error:
        refuse(f"the register {path} {error}")
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


def line_clock(line, now, which):
    """The aware UTC datetime and the text after it of the progress line `line`, `which` naming the line in the
    reason (`the last line`, `the timestamped line before the bare done line`); a line without the timestamp and the
    space, with a date that is none or with a time after the clock `now` is Malformed naming the line."""
    match = PROGRESS_LINE.match(line)
    if match is None:
        raise Malformed(f"{which} has no {TS_PREFIX} timestamp and a space before its text: {cell(line)}")
    try:
        written = datetime.strptime(match.group(1), TS_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        raise Malformed(f"{which} has no such date: {cell(line)}") from None
    if written > now:
        raise Malformed(f"{which} has a time after the clock {now.strftime(TS_FORMAT)}: {cell(line)}")
    return written, match.group(2)


def last_clock(lines, now):
    """`(written, body, bare)` of the file's last line, `lines` the file's lines without the trailing newline's empty
    element: `written` the clock the age is measured from, `body` the text after the timestamp (the bare done line's
    own text, since it has no timestamp) and `bare` whether the last line is the bare `done, head=<40 hex>`, whose
    clock is the preceding timestamped line's, the last line before it with the timestamp and the space (round 5);
    an empty file, a blank last line, a last line outside the grammar or a bare done line with no timestamped line
    before it is Malformed with the reason."""
    if not lines:
        raise Malformed("the file is empty")
    last = lines[-1]
    if last == "":
        raise Malformed("the last line is blank")
    if BARE_DONE.match(last) is None:
        written, body = line_clock(last, now, "the last line")
        return written, body, False
    for earlier in reversed(lines[:-1]):
        if PROGRESS_LINE.match(earlier) is not None:
            written, _ = line_clock(earlier, now, "the timestamped line before the bare done line")
            return written, last, True
    raise Malformed(f"the bare done line has no timestamped line before it: {cell(last)}")


def judge(root_fd, unit, now, limit):
    """The unit's row as (state, age text, last line text) from its progress file under the held root descriptor,
    never a refusal (round 2, U496b; the one run-level refusal left is a store that cannot be read): `no-file` for no
    entry; `unreadable` with `-` for the age and the line when the file yields no text; `malformed` with `-` for the
    age and the reason for the line when the text is outside the grammar (round 5: the reason names the worker's
    line, so the coordinator sees what the worker wrote, and every other unit's row still prints); else the age and
    the `done,` forms decide, the bare `done, head=<40 hex>` aged by the timestamped line before it."""
    try:
        descriptor = held_file(root_fd, f"{unit}-progress.txt")
        if descriptor is None:
            return NO_FILE, "-", "-"
        text = file_text(descriptor)
    except Unreadable:
        return UNREADABLE, "-", "-"
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    try:
        written, body, bare = last_clock(lines, now)
    except Malformed as reason:
        return MALFORMED, "-", str(reason)
    age = int((now - written).total_seconds() // 60)
    if bare or body.startswith(DONE_PREFIX) or body.startswith(f"{unit} {DONE_PREFIX}"):
        state = DONE
    elif age <= limit:
        state = MOVING
    else:
        state = STALLED
    return state, str(age), cell(lines[-1])


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    argument_rule(argv)
    args = parser().parse_args(argv)
    now = clock(args.now)
    limit = deadline(args.deadline_minutes)
    store = clean_directory(args.store, "store")
    root = default_root(store) if args.progress_root is None else clean_directory(args.progress_root, "progress root")
    store_fd = root_fd = None
    rows = []
    code = 0
    try:
        store_fd, store_walked = held_root(store, "store")
        root_fd, _ = held_root(root, "progress root")
        for unit in in_flight_units(store_walked, store_fd):
            state, age, last = judge(root_fd, unit, now, limit)
            rows.append(f"{unit}\t{state}\t{age}\t{last}\n")
            code = max(code, STATES[state])
    finally:
        for descriptor in (root_fd, store_fd):
            if descriptor is not None:
                os.close(descriptor)
    sys.stdout.write("".join(rows))
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    lever_self_check()
    sys.exit(main())
