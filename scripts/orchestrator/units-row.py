#!/usr/bin/env -S python3 -I
"""Write one `units.tsv` row of the program store by the readers' grammar, in place under its lock (regime-cutover U505).

On 2026-11-13T00:29Z a coordinator cell opened the live register with mode `w` and raised mid-write, leaving a
7203-byte file of 659 rows that only the kernel's memory restored (decisions.tsv lesson row 2026-11-13T00:29:54Z).
This lever is `ledger-row.py`'s form for the other register: the coordinator adds or changes one row through it and
never opens `units.tsv` from a Python cell again.

The register is one table: the header exactly `id track state branch pr head_sha brief note`, tab-separated, eight
cells per row, LF line ends, no carriage return anywhere (the readers: brief-check.py `taken_unit_id`, pr-merge.sh
`unit_row_exists`, program-status.py, ticket-unit.py). A register of another shape is exit 2 naming the file and the
line, and nothing is written. The lever holds every cell it writes to a closed class before the write: `id`
`U<digits>[a-z]*`; `track` and `state` `[a-z][a-z0-9-]*` (a character class, not a word list: the live register
holds 30 tracks and 15 states the coordinator named over a month, and the hcom-orchestration SKILL's state list is
stale, a docs finding this unit records and does not fix); `branch` empty or over `[A-Za-z0-9._/-]`; `pr` empty or
`[1-9][0-9]{0,8}`; `head_sha` empty or 40 lowercase hex; `brief` empty or `briefs/<id>-[A-Za-z0-9._-]+.md` with
`<id>` this row's id; `note` any text without a tab or a line boundary `str.splitlines` knows (the readers split the
file with it, so a U+2028 in a note would split the row). The cells a `set` leaves alone are kept as they are: the
live register holds 8-hex heads and brief cells from before the store move, which the readers accept and this lever
does not re-judge. Every element of argv round-trips through strict UTF-8 and holds no tab, newline or carriage
return before argparse runs (ledger-row.py's argument rule).

`units-row.py <store> add --id U<n>[a-z]* --track <t> --state <s> [--branch <b>] [--pr <n>] [--head <sha>]
[--brief <path>] --note <text> [--lock-wait <seconds>]` appends the row; a row with that id exists is a refusal
naming its line (the U436 class, a duplicated id), unless that row is byte-equal to the one asked for, which prints
`unchanged <id>` and writes nothing. `units-row.py <store> set --id U<n>[a-z]* [--track <t>] [--state <s>]
[--branch <b>] [--pr <n>] [--head <sha>] [--brief <path>] [--note-append <text>] [--lock-wait <seconds>]` replaces
each named cell of the one row with that id (none or two rows is a refusal naming the count and the lines; no option
after `--id` is a refusal, nothing to set); `--note-append` appends `; <text>` to the note, or sets it when the note
is empty. Idempotence: a `set` whose every named value already equals the cell's, `--note-append` counting as equal
when the note is the text or already ends with `; <text>`, prints `unchanged <id>` and writes nothing, so the second
run of one command is a no-op.

The write is ledger-row.py round 4's form with the in-place rewrite `set` needs. One `os.open(units, O_RDWR |
O_NOFOLLOW)` descriptor carries `fcntl.flock(LOCK_EX | LOCK_NB)`, tried every 0.1 s for `--lock-wait` seconds
(default 30; expiry a refusal naming the file), the `os.fstat` for the length n0 and the owner (this user, a regular
file), the `os.pread` of the whole text from 0 until n0 bytes, the parse by the one grammar, the new text composed
and parsed again before anything is written, then for `add` one `os.pwrite` of the line at n0, for `set` one
`os.pwrite` of the whole new text at 0 followed by `os.ftruncate` to its length when shorter, then `os.fsync`, and
the close, which releases the lock. A write that fails or returns short, or a fsync that fails, restores the old
text (`os.pwrite` of the old bytes at 0 until all are written, `os.ftruncate` to n0, `os.fsync`) and is exit 1
naming the file and the error; a restore that fails is named too (`the register <path> may hold a torn text`). Why
in place and not a temporary file renamed over the register: ticket-unit.py and ledger-row.py lock the register's own
descriptor, and a replaced inode would leave a concurrent appender writing to the old file; the store's own walks
(records-sync.sh, regime-store-move) refuse a name beginning with `.`, and a sync may list the store at any moment.
The lock is advisory and the readers take none; a reader that meets a torn line fails closed (program-status.py
refused a torn last line on 2026-11-12, by design). No file but the register is written and no mode is changed.

Exit 0 prints one stdout line: `added <id> line <n>`, `set <id> line <n> cells=<comma list of the cells changed, in
the header's order>`, or `unchanged <id>`. Exit 2 with one stderr line, `units-row.py: refused: <reason>`, and
nothing on stdout for every refusal: the self pin (below), an argument outside its class, an unknown subcommand or
option (argparse's usage block is folded into the one line), the store not a directory of this user, the register
not a regular file of this user or reached through a symbolic link, the register malformed, a lock not taken in
time, and a read that fails (open, flock, fstat, pread). Exit 1 with one stderr line, `units-row.py: cannot write
<file>: <cause>`, when the write, the fsync or the close fails. Every stderr line passes through one sanitiser that
folds every line boundary `str.splitlines` knows into a space (ticket-unit.py's `one_line`), so a quoted value
cannot add a line.

Installed as `~/.local/bin/common/units-row.py` in `brief-check.py`'s form: `scripts/generate-agent-configs.py`
writes the same bytes to `home/dot_local/bin/common/executable_units-row.py` and pins their sha256 under
`claude.levers.sha256`; before anything else the file hashes itself against that pin, the deployed manifest
`~/.agents/agent-config.yaml` when its physical directory is the physical `~/.local/bin/common`, else the checkout's
`home/dot_agents/agent-config.yaml` two levels up, and refuses to run on a difference. The orchestrator seat's policy
allows that installed path alone; the worker and audit policies deny the lever by name (standing order 27: the store
has one writer). The lever runs no `gh`, no git and no network.
"""

import argparse
import errno
import fcntl
import hashlib
import math
import os
import re
import stat
import sys
import time

LEVER = "units-row.py"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py, U136).
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")
# The line boundaries `str.splitlines` knows; `one_line` replaces each with a space in every refusal, and no cell
# holds one (the readers split the register with `splitlines`).
LINE_BREAK = re.compile(r"[\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]")


def one_line(text):
    """`text` with every line boundary `str.splitlines` knows a space: the one sanitiser of every stderr line, so a
    path or a quoted value that holds one cannot add a line."""
    return LINE_BREAK.sub(" ", text)


def refuse(reason):
    """One stderr line in the levers' words, exit 2; nothing was written."""
    print(f"{LEVER}: refused: {one_line(reason)}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `units-row.py`
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

# The write's lock is `LOCK_EX` on the register's own descriptor, tried non-blocking every LOCK_POLL seconds for
# LOCK_WAIT seconds (`--lock-wait` sets the wait); advisory, so the readers, which take no lock, are unaffected.
LOCK_WAIT = 30.0
LOCK_POLL = 0.1
# The three characters no argument holds: the register is tab-separated lines (the cells refuse every line boundary).
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))
# The register's one grammar (brief-check.py, pr-merge.sh, program-status.py, ticket-unit.py): the header, eight cells.
UNITS_FILE = "units.tsv"
UNITS_HEADER = ("id", "track", "state", "branch", "pr", "head_sha", "brief", "note")
# The closed class of each cell this lever writes (the module docstring); a `None` class is the note's rule alone.
UNIT_ID = re.compile(r"U[0-9]+[a-z]*")
WORD = re.compile(r"[a-z][a-z0-9-]*")
BRANCH = re.compile(r"[A-Za-z0-9._/-]+")
PR = re.compile(r"[1-9][0-9]{0,8}")
HEAD = re.compile(r"[0-9a-f]{40}")
BRIEF = re.compile(r"briefs/(U[0-9]+[a-z]*)-[A-Za-z0-9._-]+\.md")
CELL_CLASSES = {
    "id": (UNIT_ID, False, "U<digits>[a-z]*"),
    "track": (WORD, False, "[a-z][a-z0-9-]*"),
    "state": (WORD, False, "[a-z][a-z0-9-]*"),
    "branch": (BRANCH, True, "empty or over [A-Za-z0-9._/-]"),
    "pr": (PR, True, "empty or 1 to 9 digits without a leading zero"),
    "head_sha": (HEAD, True, "empty or 40 lowercase hex"),
    "brief": (BRIEF, True, "empty or briefs/<this row's id>-<[A-Za-z0-9._-]+>.md"),
    "note": (None, True, "text without a tab or a line boundary"),
}
# The option of each cell a subcommand may name; `note` is `--note` on add and `--note-append` on set.
CELL_OPTIONS = {
    "track": "--track",
    "state": "--state",
    "branch": "--branch",
    "pr": "--pr",
    "head_sha": "--head",
    "brief": "--brief",
}
NOTE_SEPARATOR = "; "


def argument_rule(argv):
    """The one rule every element of argv passes before argparse runs (ledger-row.py rounds 3 and 4): the element
    round-trips through strict UTF-8 (Python decodes argv with surrogateescape, so a byte that is not UTF-8 arrives
    as a lone surrogate that would fail only at the write) and holds neither a tab, a newline nor a carriage return
    (a check of the parsed strings alone would let `--lock-wait`, which argparse converts to a float, escape it).
    The refusal names the element's position and the option before it, or the store for the positional element."""
    positional = 0
    for index, value in enumerate(argv):
        if value.startswith("--"):
            where = f"argument {index + 1} (the option {value.split('=', 1)[0]!r})"
        elif index and argv[index - 1].startswith("--"):
            where = f"argument {index + 1} (the value of {argv[index - 1]})"
        else:
            positional += 1
            where = f"argument {index + 1}" + (" (the store)" if positional == 1 else "")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as error:
            refuse(f"{where} holds a byte that is not UTF-8 at offset {error.start}: {value!r}")
        for character, label in CONTROL:
            if character in value:
                refuse(f"{where} holds {label}; a cell holds neither a tab nor a newline")


class Parser(argparse.ArgumentParser):
    """argparse with no option abbreviation (`--note` is not `--note-append`) and its errors as one refusal line:
    no usage block, exit 2 through `refuse`."""

    def __init__(self, **kwargs):
        kwargs["allow_abbrev"] = False
        super().__init__(**kwargs)

    def error(self, message):
        refuse(f"{message} (the form: {LEVER} <store> add|set --id U<n> ...)")


def parser():
    top = Parser(prog=LEVER, description=__doc__.splitlines()[0], add_help=False)
    top.add_argument("store", help="the program store directory")
    kinds = top.add_subparsers(dest="kind", required=True, parser_class=Parser)
    add = kinds.add_parser("add", help="append one row; the id must be new", add_help=False)
    add.add_argument("--id", required=True)
    add.add_argument("--track", required=True)
    add.add_argument("--state", required=True)
    add.add_argument("--branch", default="")
    add.add_argument("--pr", default="")
    add.add_argument("--head", default="")
    add.add_argument("--brief", default="")
    add.add_argument("--note", required=True)
    setter = kinds.add_parser("set", help="replace the named cells of the one row with the id", add_help=False)
    setter.add_argument("--id", required=True)
    for option in ("--track", "--state", "--branch", "--pr", "--head", "--brief", "--note-append"):
        setter.add_argument(option, default=None)
    for sub in (add, setter):
        sub.add_argument(
            "--lock-wait",
            default=str(LOCK_WAIT),
            help=f"seconds to wait for the register's lock (default {LOCK_WAIT:g})",
        )
    return top


def check_lock_wait(args):
    try:
        args.lock_wait = float(args.lock_wait)
    except ValueError:
        refuse(f"--lock-wait {args.lock_wait!r} is not a non-negative number of seconds")
    if not 0 <= args.lock_wait < math.inf:
        refuse(f"--lock-wait {args.lock_wait!r} is not a non-negative number of seconds")


def cell_rule(name, value, unit):
    """`value` in the closed class of the cell `name` (the brief's id equal to `unit`), else a refusal naming the
    cell, the value and the class. Every cell refuses a tab and every line boundary `str.splitlines` knows."""
    if "\t" in value:
        refuse(f"the {name} {value!r} holds a tab; a cell holds neither a tab nor a line boundary")
    if LINE_BREAK.search(value):
        refuse(f"the {name} {value!r} holds a line boundary; a cell holds neither a tab nor a line boundary")
    pattern, may_be_empty, grammar = CELL_CLASSES[name]
    if value == "":
        if may_be_empty:
            return
        refuse(f"the {name} {value!r} is not {grammar}")
    if pattern is None:
        return
    match = pattern.fullmatch(value)
    if match is None:
        refuse(f"the {name} {value!r} is not {grammar}")
    if name == "brief" and match.group(1) != unit:
        refuse(f"the brief {value!r} names the unit {match.group(1)}, not this row's id {unit}")


def store_dir(argument):
    """The store's realpath: a directory owned by this user; any other outcome is a refusal naming the store."""
    store = os.path.realpath(argument)
    try:
        status = os.lstat(store)
    except OSError as error:
        refuse(f"the store {store} cannot be read: {error.strerror}")
    if not stat.S_ISDIR(status.st_mode):
        refuse(f"the store {store} is not a directory")
    if status.st_uid != os.getuid():
        refuse(f"the store {store} is not a directory of this user (owner uid {status.st_uid}, not {os.getuid()})")
    return store


def store_path(store, relative, label):
    """`<store>/<relative>` by the one path rule every file under the store follows (ledger-row.py round 2): `store`
    is already its own realpath; each component below it is `os.lstat`ed and none is a link (a symlinked parent out
    of the store is named by its component); the realpath lies under the store. Returns (path, lstat result or None
    when the last component does not exist); any other failure is a refusal naming the path."""
    current = store
    parts = relative.split("/")
    status = None
    for index, part in enumerate(parts):
        current = os.path.join(current, part)
        try:
            status = os.lstat(current)
        except FileNotFoundError:
            if index == len(parts) - 1:
                return current, None
            refuse(f"the {label}'s directory {current} does not exist under the store")
        except OSError as error:
            refuse(f"the {label} {current} cannot be read: {error.strerror}")
        if stat.S_ISLNK(status.st_mode):
            refuse(
                f"the {label}'s component {current} is a symbolic link; a file under the store is reached through "
                "real directories alone"
            )
        if index < len(parts) - 1 and not stat.S_ISDIR(status.st_mode):
            refuse(f"the {label}'s directory {current} is not a directory")
    if not os.path.realpath(current).startswith(store + os.sep):
        refuse(f"the {label} {current} resolves outside the store {store}")
    return current, status


def store_file(store, relative, label):
    """The regular file `<store>/<relative>` of this user by `store_path`, else a refusal naming it."""
    current, status = store_path(store, relative, label)
    if status is None:
        refuse(f"the {label} {current} is not a regular file under the store: No such file or directory")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the {label} {current} is not a regular file under the store")
    if status.st_uid != os.getuid():
        refuse(f"the {label} {current} is not a regular file of this user (owner uid {status.st_uid})")
    return current


def open_register(units_path, wait):
    """The register's own descriptor, `O_RDWR | O_NOFOLLOW` without the append flag (`set` rewrites at offset 0, and
    Linux puts every write of an append-mode descriptor at the end), locked `LOCK_EX` (ledger-row.py round 4): the
    one descriptor the lock, the read and the write go through, released by its close. The lock is tried every
    LOCK_POLL seconds for `wait` seconds; a lock not taken by then is a refusal naming the file."""
    try:
        descriptor = os.open(units_path, os.O_RDWR | os.O_NOFOLLOW)
    except OSError as error:
        refuse(f"cannot open the register {units_path} for the write: {error.strerror}")
    deadline = time.monotonic() + wait
    while True:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return descriptor
        except OSError as error:
            if error.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                refuse(f"cannot lock the register {units_path}: {error.strerror}")
            if time.monotonic() >= deadline:
                refuse(
                    f"the register {units_path} is held by another writer after {wait:g} second"
                    f"{'' if wait == 1 else 's'}; nothing is written (--lock-wait sets the wait)"
                )
            time.sleep(LOCK_POLL)


def read_register(descriptor, units_path):
    """The whole text through the locked descriptor: `os.fstat` for the length n0 (a regular file of this user),
    `os.pread` from offset 0 looped until n0 bytes, decoded as strict UTF-8. Every failure is a refusal naming the
    register. Returns (n0, the bytes, the text)."""
    try:
        status = os.fstat(descriptor)
    except OSError as error:
        refuse(f"cannot read the register {units_path}: fstat: {error.strerror}")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the register {units_path} is not a regular file")
    if status.st_uid != os.getuid():
        refuse(f"the register {units_path} is not a regular file of this user (owner uid {status.st_uid})")
    length = status.st_size
    chunks = []
    offset = 0
    while offset < length:
        try:
            chunk = os.pread(descriptor, length - offset, offset)
        except OSError as error:
            refuse(f"cannot read the register {units_path}: pread at offset {offset}: {error.strerror}")
        if not chunk:
            refuse(f"the register {units_path} holds {offset} bytes, fewer than its length {length} under the lock")
        chunks.append(chunk)
        offset += len(chunk)
    data = b"".join(chunks)
    try:
        return length, data, data.decode("utf-8")
    except UnicodeDecodeError as error:
        refuse(f"{units_path}: not UTF-8: {error.reason}")


def parse_register(units_path, text):
    """The rows of the register by the one grammar: line 1 the header, every other line eight cells, no carriage
    return; a last line without a newline is a row too. Returns [(line number, cells)]."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines:
        refuse(f"{units_path}:1 is not the header ({' '.join(UNITS_HEADER)}); the file is empty")
    rows = []
    for number, line in enumerate(lines, 1):
        if "\r" in line:
            refuse(f"{units_path}:{number} holds a carriage return")
        if number == 1:
            if line != "\t".join(UNITS_HEADER):
                refuse(f"{units_path}:1 is not the header ({' '.join(UNITS_HEADER)})")
            continue
        cells = line.split("\t")
        if len(cells) != len(UNITS_HEADER):
            refuse(f"{units_path}:{number} has {len(cells)} cells, not {len(UNITS_HEADER)}")
        rows.append((number, cells))
    return rows


def rows_with_id(rows, unit):
    return [(number, cells) for number, cells in rows if cells[0] == unit]


def added_text(args, units_path, text, rows):
    """`add`: the new text and the stdout line, or (None, `unchanged <id>`) when the byte-equal row exists."""
    cells = (args.id, args.track, args.state, args.branch, args.pr, args.head, args.brief, args.note)
    for name, value in zip(UNITS_HEADER, cells):
        cell_rule(name, value, args.id)
    existing = rows_with_id(rows, args.id)
    if existing:
        number, old = existing[0]
        if len(existing) == 1 and tuple(old) == cells:
            return None, f"unchanged {args.id}"
        lines = ", ".join(str(number) for number, _ in existing)
        refuse(f"a row with the id {args.id} exists: line{'s' if len(existing) > 1 else ''} {lines} of {units_path}")
    lead = "" if text == "" or text.endswith("\n") else "\n"
    line = "\t".join(cells) + "\n"
    number = text.count("\n") + (0 if lead == "" else 1) + 1
    return (lead + line).encode("utf-8"), f"added {args.id} line {number}"


def set_text(args, units_path, text, rows):
    """`set`: the whole new text and the stdout line, or (None, `unchanged <id>`) when every named value equals."""
    cell_rule("id", args.id, args.id)
    named = {name: getattr(args, option.lstrip("-")) for name, option in CELL_OPTIONS.items()}
    named = {name: value for name, value in named.items() if value is not None}
    if args.note_append is not None:
        named["note"] = args.note_append
    if not named:
        refuse(
            f"nothing to set for {args.id}: name at least one of --track --state --branch --pr --head --brief "
            "--note-append"
        )
    for name, value in named.items():
        cell_rule(name, value, args.id)
    found = rows_with_id(rows, args.id)
    if len(found) != 1:
        lines = ", ".join(str(number) for number, _ in found)
        where = f" (lines {lines})" if found else ""
        refuse(f"{len(found)} rows of {units_path} have the id {args.id}{where}; set needs exactly one")
    number, old = found[0]
    new = list(old)
    changed = []
    for index, name in enumerate(UNITS_HEADER):
        if name not in named:
            continue
        value = named[name]
        if name == "note":
            note = old[index]
            if note == value or note.endswith(NOTE_SEPARATOR + value):
                continue
            value = value if note == "" else note + NOTE_SEPARATOR + value
            cell_rule("note", value, args.id)
        if value == old[index]:
            continue
        new[index] = value
        changed.append(name)
    if not changed:
        return None, f"unchanged {args.id}"
    lines = text.split("\n")
    lines[number - 1] = "\t".join(new)
    new_text = "\n".join(lines)
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text.encode("utf-8"), f"set {args.id} line {number} cells={','.join(changed)}"


def restore(descriptor, units_path, old, cause):
    """The recovery of a failed write and its one line: the old bytes written back at 0 until all are written, the
    file truncated to their length and synced, or the restore's own failure named (`may hold a torn text`)."""
    try:
        offset = 0
        while offset < len(old):
            written = os.pwrite(descriptor, old[offset:], offset)
            if written <= 0:
                raise OSError(errno.EIO, "short write")
            offset += written
        os.ftruncate(descriptor, len(old))
        os.fsync(descriptor)
    except OSError as error:
        return (
            f"cannot write {units_path}: {cause}; the register {units_path} may hold a torn text, the restore of its "
            f"{len(old)} bytes failed: {error.strerror}"
        )
    return f"cannot write {units_path}: {cause}; restored its {len(old)} bytes"


def write_text(descriptor, units_path, old, data, offset):
    """One `os.pwrite` of `data` at `offset` (n0 for an appended line, 0 for a rewritten text), its count compared
    with the length, `os.ftruncate` to the new length when the text shrank, then `os.fsync`. A failure restores the
    old bytes. Returns None, or the failure text naming the register."""
    try:
        written = os.pwrite(descriptor, data, offset)
    except OSError as error:
        return restore(descriptor, units_path, old, f"write: {error.strerror}")
    if written != len(data):
        return restore(descriptor, units_path, old, f"short write, {written} of {len(data)} bytes")
    try:
        if offset + len(data) < len(old):
            os.ftruncate(descriptor, offset + len(data))
        os.fsync(descriptor)
    except OSError as error:
        return restore(descriptor, units_path, old, f"fsync: {error.strerror}")
    return None


def write_row(args, units_path, descriptor):
    """The critical section, under the lock the descriptor holds: the register read and parsed through it, the new
    text composed and parsed again, the one write. Returns (0, the stdout line) or (1, the failure text)."""
    length, old, text = read_register(descriptor, units_path)
    rows = parse_register(units_path, text)
    if args.kind == "add":
        data, line = added_text(args, units_path, text, rows)
        offset = length
        whole = old + data if data is not None else None
    else:
        data, line = set_text(args, units_path, text, rows)
        offset = 0
        whole = data
    if data is None:
        return 0, line
    parse_register(units_path, whole.decode("utf-8"))
    failure = write_text(descriptor, units_path, old, data, offset)
    if failure is not None:
        return 1, failure
    return 0, line


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    argument_rule(argv)
    args = parser().parse_args(argv)
    check_lock_wait(args)
    store = store_dir(args.store)
    units_path = store_file(store, UNITS_FILE, "register")
    descriptor = open_register(units_path, args.lock_wait)
    try:
        code, text = write_row(args, units_path, descriptor)
    except BaseException:  # a refusal (SystemExit) or an unexpected error: the close releases the lock
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise
    try:
        os.close(descriptor)
    except OSError as error:
        if code == 0:
            text = f"the register {units_path} was written ({text}) but its close failed: {error.strerror}"
        else:
            text = f"{text}; the close failed too: {error.strerror}"
        code = 1
    if code == 0:
        print(text)
    else:
        print(f"{LEVER}: {one_line(text)}", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
