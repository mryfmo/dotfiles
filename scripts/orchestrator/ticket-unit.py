#!/usr/bin/env -S python3 -I
"""Bind the Router's pull request to one program unit from its ticket, the request text as data (regime-cutover U493).

The three gate levers (the `regime` check, pr-audit.sh, pr-merge.sh) resolve a pull request's unit from the one body
line `Program-Unit: <program>/U<n>`, and a pull request the Router's account opens for a ticket carries none: PR 777
(ticket bf72b83b) failed the required check and could not enter the gates (handoff/44-u493-ticket-unit-design.md,
table row f25). The ticket is the unit. `ticket-unit.py <store> --db <orchestrator.sqlite> --pr <n> --branch <name>
--head <sha> [--lock-wait <seconds>]` reads the ticket whose `follows` names that pull request from the Router's
sqlite (read-only), renders the ticket's request text into a brief under `briefs/U<n>-ticket-<id>.md` as data,
appends the unit's row to `units.tsv`, and prints the line the coordinator writes into the pull request's body with
pr-body-edit.sh. The gate levers do not change; the lever runs no `gh` and no git (the coordinator reads the pull
request's branch and head and passes them).

The binding is two-sided and both sides are the Router's own facts: exactly one ticket's `follows` holds `thread ==
"github:<pr>"` with `own` true (none or two is a refusal naming the count), and `--branch` equals `agent/` plus the
ticket's `execution.name` (else a refusal). The sqlite table `ticket (id TEXT PRIMARY KEY, value TEXT)` holds one
JSON document per ticket, read with the `sqlite3` module over the URI `file:<db>?mode=ro` and the `json` module
(parser-module form; nothing hand-written over the text); a value that is not a JSON object, or a `follows` that is
not a list of objects, is a refusal naming the ticket. The fields used are each held to a grammar before use: `id`
(32 lowercase hex, equal to the row's key), `title` and `mandate.scope` (text, data), `mandate.basis.sender` and
`mandate.actor.id` (`[A-Za-z0-9-]+`), `channels[0].thread` (`[a-z]+:[0-9]+`), `execution.name` (`[A-Za-z0-9._-]+`),
`decisionId` (32 hex), `createdAt` (`<YYYY-MM-DD>T<HH:MM:SS>[.<fraction>]Z`). The arguments: `--pr` 1 to 9 digits
with no leading zero, `--head` 40 lowercase hex, `--branch` over `[A-Za-z0-9._/-]`, `--lock-wait` a non-negative
finite number (default 30); every element of argv round-trips through strict UTF-8 and holds no tab, newline or
carriage return before argparse runs (ledger-row.py's argument rule). The store is a directory of this user whose
basename is the program, held to regime-init's grammar `[a-z0-9][a-z0-9_-]{0,63}`; the sqlite is a regular file.

`units.tsv` is read by the one grammar: the header `id track state branch pr head_sha brief note`, tab-separated,
eight cells per row, no carriage return; another shape is a refusal naming the file and the line, and the file, the
`briefs` directory and the brief are reached through real directories alone (each component `os.lstat`ed, no link,
the realpath under the store's). Idempotence: a row whose `brief` cell is `briefs/U<n>-ticket-<id>.md` for this
ticket makes the lever print `state=existing` with that unit and write nothing; that row's id must be its `U<n>` and
its brief a regular file under the store, two such rows or a brief file of that name with no row are refusals (the
store is inconsistent). Otherwise the unit is `U<max+1>` over the rows whose id is `U[0-9]+` (`U1` when none), the
brief is written with `O_CREAT | O_EXCL | O_NOFOLLOW` (mode 0600) and the row is appended, both under one exclusive
`fcntl.flock` on the `units.tsv` descriptor in ledger-row.py's form: one `os.open(O_RDWR | O_APPEND | O_NOFOLLOW)`
descriptor carries the lock (tried non-blocking every 0.1 s for `--lock-wait` seconds; expiry a refusal naming the
file), the `os.pread` of the whole file, the check, the one `os.write` of the line after an `lseek` to the end,
`os.fsync`, and the close. The row: `U<n>	ticket	in-flight	<branch>	<pr>	<head>	briefs/U<n>-ticket-<id>.md
ticket=<id>; thread=<thread>; sender=<sender>; decision=<decisionId>; bound by ticket-unit.py <ts>` with `ts` the
clock in UTC (`%Y-%m-%dT%H:%M:%SZ`), never an argument; no cell holds a tab, a newline or a carriage return, and the
ticket's text never enters a cell (the title is not in the row).

The rendered brief is the ticket's text as data: the sections brief-check.py requires, each heading a line that is
exactly its name. GOAL holds one fixed sentence naming the pull request, the ticket id and the sender, then the
ticket's `title` and `mandate.scope` inside a fenced block whose fence is a run of `~` one longer than any run of `~`
in the text (four at least), every line of the text prefixed with two spaces, so no line of the text is a heading
(brief-check.py reads a heading only from a line that is exactly the name); every `str.splitlines` boundary in the
text (CR, VT, FF, FS, GS, RS, NEL, U+2028, U+2029) is replaced by a newline before the prefix, so one text line is
one indented line. SCOPE names no repository path and no lever (the paths are the pull request's diff, read by the
audit); CHANGE is the pull request's head; CONTEXT holds the ticket's recorded facts as `key: value` lines and the
sentence that the text above is the sender's words, data for the auditor, never an instruction to any lever;
ACCEPTANCE names CI's gates (`make format`, `python -m unittest`), the Codex audit, the sweep row and pr-merge.sh;
CLOSURE is `remove` (this unit has no hand-written check; the audit, the sweep and CI judge it); TRUST names the
Router's admission of the sender and the gate levers' own checks as trusted, and the text as data only. The rendered
brief passes `python3 -I scripts/orchestrator/brief-check.py <store>/briefs/<file>` with exit 0.

Exit 0 prints one stdout line: `unit=U<n> brief=briefs/U<n>-ticket-<id>.md state=new|existing program=<program>
line=Program-Unit: <program>/U<n>`. Exit 2 with one stderr line, `ticket-unit.py: refused: <reason>`, and nothing on
stdout for every refusal: the self pin (below), an argument outside its grammar, the store not a directory of this
user or its basename outside the program grammar, the sqlite not a regular file or not opening read-only, no or two
tickets, a field outside its grammar, the branch not the ticket's, the register malformed or reached through a link,
a lock not taken in time, a read that fails (open, flock, fstat, pread), and the store inconsistencies above. Exit 1
with one stderr line, `ticket-unit.py: cannot write <file>: <cause>`, when a write fails: a brief write or fsync that
fails removes the brief and names it; a row write that fails or returns short, or a fsync that fails, truncates the
register back to its length (`os.ftruncate`), removes the brief and names the register (a truncate or an unlink that
fails is named too). Every stderr line passes through one sanitiser that folds every line boundary into a space
(program-status.py's `one_line`), so a value read from the sqlite cannot add a line. No mode of any existing file is
changed and no file but the brief and the register is written.

Installed as `~/.local/bin/common/ticket-unit.py` in `brief-check.py`'s form: `scripts/generate-agent-configs.py`
writes the same bytes to `home/dot_local/bin/common/executable_ticket-unit.py` and pins their sha256 under
`claude.levers.sha256`; before anything else the file hashes itself against that pin, the deployed manifest
`~/.agents/agent-config.yaml` when its physical directory is the physical `~/.local/bin/common`, else the checkout's
`home/dot_agents/agent-config.yaml` two levels up, and refuses to run on a difference. The orchestrator seat's policy
allows that installed path alone.
"""

import argparse
import errno
import fcntl
import hashlib
import json
import math
import os
import re
import sqlite3
import stat
import sys
import time
import urllib.parse
from datetime import datetime, timezone

LEVER = "ticket-unit.py"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py, U136).
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")
# The line boundaries `str.splitlines` knows; `one_line` replaces each with a space in every refusal, and the brief
# renderer replaces each with a newline before the indent, so one text line is one indented line.
LINE_BREAK = re.compile(r"[\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]")


def one_line(text):
    """`text` with every line boundary `str.splitlines` knows a space: the one sanitiser of every stderr line, so a
    ticket id, a path or a quoted value that holds one cannot add a line."""
    return LINE_BREAK.sub(" ", text)


def refuse(reason):
    """One stderr line in the levers' words, exit 2; nothing was written."""
    print(f"{LEVER}: refused: {one_line(reason)}", file=sys.stderr)
    sys.exit(2)


def lever_self_check():
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `ticket-unit.py`
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
# The three characters no cell and no argument holds: the register is tab-separated lines.
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))
# The arguments' grammars (the shell reads nothing: every value is held to a closed class before use).
PR = re.compile(r"[1-9][0-9]{0,8}")
HEAD = re.compile(r"[0-9a-f]{40}")
BRANCH = re.compile(r"[A-Za-z0-9._/-]+")
# regime-init's program grammar: the store directory's basename is the program.
PROGRAM = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
# The ticket's fields, each a closed class (the title and the scope are text, data; they have no grammar).
HEX32 = re.compile(r"[0-9a-f]{32}")
ACCOUNT = re.compile(r"[A-Za-z0-9-]+")
THREAD = re.compile(r"[a-z]+:[0-9]+")
EXECUTION_NAME = re.compile(r"[A-Za-z0-9._-]+")
CREATED_AT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,6})?Z")
# The Router's branch for a ticket: `agent/` and the execution name.
BRANCH_PREFIX = "agent/"
# The Router's thread name for a pull request.
THREAD_PREFIX = "github:"
# The register's one grammar (brief-check.py, program-status.py): the header, eight cells, the plain unit id.
UNITS_FILE = "units.tsv"
UNITS_HEADER = ("id", "track", "state", "branch", "pr", "head_sha", "brief", "note")
UNIT_ID = re.compile(r"U([0-9]+)")
BRIEFS_DIR = "briefs"
TRACK = "ticket"
STATE = "in-flight"
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
# The fence is a run of `~` one longer than the text's longest, four at least (a fenced block opens with three).
FENCE_CHARACTER = "~"
FENCE_MINIMUM = 4
TILDE_RUN = re.compile(r"~+")
INDENT = "  "


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


def parser():
    top = argparse.ArgumentParser(prog=LEVER, description=__doc__.splitlines()[0])
    top.add_argument("store", help="the program store directory; its basename is the program")
    top.add_argument("--db", required=True, help="the Router's orchestrator.sqlite, opened read-only")
    top.add_argument("--pr", required=True, help="the pull request number the ticket's `follows` names, 1 to 9 digits")
    top.add_argument("--branch", required=True, help="the pull request's branch, agent/<execution.name>")
    top.add_argument("--head", required=True, help="the pull request's head, 40 lowercase hex")
    top.add_argument(
        "--lock-wait",
        default=str(LOCK_WAIT),
        help=f"seconds to wait for the register's lock (default {LOCK_WAIT:g})",
    )
    return top


def check_arguments(args):
    try:
        args.lock_wait = float(args.lock_wait)
    except ValueError:
        refuse(f"--lock-wait {args.lock_wait!r} is not a non-negative number of seconds")
    if not 0 <= args.lock_wait < math.inf:
        refuse(f"--lock-wait {args.lock_wait!r} is not a non-negative number of seconds")
    if PR.fullmatch(args.pr) is None:
        refuse(f"--pr {args.pr!r} is not 1 to 9 digits without a leading zero")
    if HEAD.fullmatch(args.head) is None:
        refuse(f"--head {args.head!r} is not 40 lowercase hex")
    if BRANCH.fullmatch(args.branch) is None:
        refuse(f"--branch {args.branch!r} is not over [A-Za-z0-9._/-]")


def store_dir(argument):
    """The store's realpath and the program, its basename: a directory owned by this user, the basename in the
    program grammar; any other outcome is a refusal naming the store."""
    store = os.path.realpath(argument)
    try:
        status = os.lstat(store)
    except OSError as error:
        refuse(f"the store {store} cannot be read: {error.strerror}")
    if not stat.S_ISDIR(status.st_mode):
        refuse(f"the store {store} is not a directory")
    if status.st_uid != os.getuid():
        refuse(f"the store {store} is not a directory of this user (owner uid {status.st_uid}, not {os.getuid()})")
    program = os.path.basename(store)
    if PROGRAM.fullmatch(program) is None:
        refuse(f"the store's basename {program!r} is not a program name ([a-z0-9][a-z0-9_-]{{0,63}})")
    return store, program


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
    """The regular file `<store>/<relative>` by `store_path`, else a refusal naming it."""
    current, status = store_path(store, relative, label)
    if status is None:
        refuse(f"the {label} {current} is not a regular file under the store: No such file or directory")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the {label} {current} is not a regular file under the store")
    return current


def read_tickets(argument):
    """Every `(id, value)` of the sqlite's `ticket` table, read over the read-only URI; the file must be a regular
    file and every sqlite error is a refusal naming it."""
    db = os.path.realpath(argument)
    try:
        status = os.stat(db)
    except OSError as error:
        refuse(f"the sqlite {db} cannot be read: {error.strerror}")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the sqlite {db} is not a regular file")
    uri = "file:" + urllib.parse.quote(db) + "?mode=ro"
    try:
        connection = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as error:
        refuse(f"the sqlite {db} does not open read-only: {error}")
    try:
        rows = connection.execute("SELECT id, value FROM ticket ORDER BY id").fetchall()
    except sqlite3.Error as error:
        refuse(f"the sqlite {db} cannot be read: {error}")
    finally:
        connection.close()
    return rows


def document_of(ticket_id, value):
    """The ticket's JSON object, through the json module alone; anything else is a refusal naming the ticket."""
    try:
        document = json.loads(value)
    except (TypeError, ValueError) as error:
        refuse(f"ticket {ticket_id!r}: the value is not JSON: {error}")
    if not isinstance(document, dict):
        refuse(f"ticket {ticket_id!r}: the value is not a JSON object")
    return document


def follows_pr(ticket_id, document, thread):
    """Whether the ticket's `follows` holds an entry with this thread and `own` true; a `follows` that is not a list
    of objects is a refusal naming the ticket (standing order 21: a shape the reader cannot judge is no pass)."""
    follows = document.get("follows")
    if follows is None:
        return False
    if not isinstance(follows, list):
        refuse(f"ticket {ticket_id!r}: `follows` is not a list")
    found = False
    for entry in follows:
        if not isinstance(entry, dict):
            refuse(f"ticket {ticket_id!r}: a `follows` entry is not an object")
        if entry.get("thread") == thread and entry.get("own") is True:
            found = True
    return found


def binding_ticket(rows, pr):
    """The one `(id, document)` whose `follows` names `github:<pr>` with `own` true; none or two is a refusal naming
    the count."""
    thread = f"{THREAD_PREFIX}{pr}"
    matches = []
    for ticket_id, value in rows:
        document = document_of(ticket_id, value)
        if follows_pr(ticket_id, document, thread):
            matches.append((ticket_id, document))
    if not matches:
        refuse(f"no ticket follows {thread} with own true (0 of {len(rows)} tickets)")
    if len(matches) > 1:
        names = ", ".join(str(ticket_id) for ticket_id, _ in matches)
        refuse(f"{len(matches)} tickets follow {thread} with own true, not one: {names}")
    return matches[0]


def field(ticket_id, document, *keys):
    """The value at `keys` in the document, each step an object (a list index as an int); a missing step is a
    refusal naming the field."""
    value = document
    for key in keys:
        if isinstance(key, int):
            if not isinstance(value, list) or len(value) <= key:
                refuse(f"ticket {ticket_id!r}: {field_name(keys)} is missing")
        elif not isinstance(value, dict) or key not in value:
            refuse(f"ticket {ticket_id!r}: {field_name(keys)} is missing")
        value = value[key]
    return value


def field_name(keys):
    name = ""
    for key in keys:
        name += f"[{key}]" if isinstance(key, int) else (f".{key}" if name else key)
    return name


def text_field(ticket_id, document, *keys):
    value = field(ticket_id, document, *keys)
    if not isinstance(value, str):
        refuse(f"ticket {ticket_id!r}: {field_name(keys)} is not text")
    return value


def held_field(ticket_id, document, grammar, grammar_text, *keys):
    value = text_field(ticket_id, document, *keys)
    if grammar.fullmatch(value) is None:
        refuse(f"ticket {ticket_id!r}: {field_name(keys)} {value!r} is not {grammar_text}")
    return value


def ticket_facts(ticket_id, document):
    """The ticket's fields the lever uses, each held to its grammar before use, as a dict; the title and the scope
    are text, data, and have none."""
    if not isinstance(ticket_id, str) or HEX32.fullmatch(ticket_id) is None:
        refuse(f"ticket {ticket_id!r}: the row's id is not 32 lowercase hex")
    facts = {
        "id": held_field(ticket_id, document, HEX32, "32 lowercase hex", "id"),
        "title": text_field(ticket_id, document, "title"),
        "scope": text_field(ticket_id, document, "mandate", "scope"),
        "sender": held_field(ticket_id, document, ACCOUNT, "over [A-Za-z0-9-]", "mandate", "basis", "sender"),
        "actor": held_field(ticket_id, document, ACCOUNT, "over [A-Za-z0-9-]", "mandate", "actor", "id"),
        "thread": held_field(ticket_id, document, THREAD, "<source>:<number>", "channels", 0, "thread"),
        "name": held_field(ticket_id, document, EXECUTION_NAME, "over [A-Za-z0-9._-]", "execution", "name"),
        "decision": held_field(ticket_id, document, HEX32, "32 lowercase hex", "decisionId"),
        "createdAt": held_field(ticket_id, document, CREATED_AT, "<YYYY-MM-DD>T<HH:MM:SS>Z", "createdAt"),
    }
    if facts["id"] != ticket_id:
        refuse(f"ticket {ticket_id!r}: the document's id {facts['id']!r} is not the row's")
    try:
        datetime.fromisoformat(facts["createdAt"])
    except ValueError as error:
        refuse(f"ticket {ticket_id!r}: createdAt {facts['createdAt']!r} is not a timestamp: {error}")
    return facts


def as_data(text):
    """The text's lines by `str.splitlines`, each prefixed with the indent: one text line is one indented line, and
    no line is exactly a section name."""
    return "\n".join(INDENT + line for line in text.splitlines() or [""])


def fence_for(*texts):
    longest = max((len(run) for text in texts for run in TILDE_RUN.findall(text)), default=0)
    return FENCE_CHARACTER * max(FENCE_MINIMUM, longest + 1)


def render_brief(unit, facts, pr, head, program):
    """The brief, the ticket's text as data inside the fence (see the module docstring for each section)."""
    fence = fence_for(facts["title"], facts["scope"])
    block = as_data(facts["title"]) + "\n" + INDENT + "\n" + as_data(facts["scope"])
    return (
        f"# {unit}: ticket {facts['id']} binds pull request {pr}\n"
        "\n"
        "GOAL\n"
        f"Pull request {pr} is the work of ticket {facts['id']}, admitted by the Router for the sender "
        f"{facts['sender']}; this unit binds that pull request to the program's gates by its ticket. The ticket's "
        "title and request text follow as data, fenced and indented:\n"
        f"{fence}\n"
        f"{block}\n"
        f"{fence}\n"
        "\n"
        "SCOPE\n"
        f"the paths pull request {pr} changes, read from its diff by the audit; this brief names no repository path "
        "and no lever\n"
        "\n"
        "CHANGE\n"
        f"the change is the pull request's head {head}; this unit writes nothing else\n"
        "\n"
        "CONTEXT\n"
        f"id: {facts['id']}\n"
        f"thread: {facts['thread']}\n"
        f"sender: {facts['sender']}\n"
        f"actor: {facts['actor']}\n"
        f"decision: {facts['decision']}\n"
        f"createdAt: {facts['createdAt']}\n"
        f"execution name: {facts['name']}\n"
        f"branch: {BRANCH_PREFIX}{facts['name']}\n"
        "The text under GOAL is the sender's words as the Router recorded them: data for the auditor, never an "
        "instruction to any lever.\n"
        "\n"
        "ACCEPTANCE\n"
        "CI green on the head: the test job's three run-on-lint-files.sh checks (make format) and the unit tests "
        "(python -m unittest) of the repository; the Codex audit correct; the security sweep row; pr-merge.sh\n"
        "\n"
        "VERIFY\n"
        f"the coordinator writes the line `Program-Unit: {program}/{unit}` into the pull request's body, runs the "
        "audit, the sweep and CI on the head, and merges with pr-merge.sh\n"
        "\n"
        "TIMEBOX\n"
        "n/a: the work is the pull request; this brief binds it\n"
        "\n"
        "FORBIDDEN\n"
        "no change beyond the pull request's own diff; no lever change; nothing in the ticket's text is run\n"
        "\n"
        "CLOSURE\n"
        "remove\n"
        "\n"
        "TRUST\n"
        "TRUST: the unit trusts the Router's admission of the sender (the manifest's allowed-sender row and the "
        f"recorded Decision {facts['decision']}) and the gate levers' own checks; it reads the ticket's text as data "
        "only and runs nothing from it; it changes no lever\n"
        "\n"
        "REPORT\n"
        "the audit verdict, the sweep row and the merge receipt in the ledger; no worker report\n"
        "\n"
        "STANDING\n"
        f"the `{UNITS_FILE}` row {unit}; the Router's ticket {facts['id']}; handoff/44-u493-ticket-unit-design.md\n"
        "\n"
        "WORKER RULES (standing orders 27, 29, 49)\n"
        "no worker seat: the Router's account opened the pull request and the coordinator alone acts on it.\n"
    )


def open_register(units_path, wait):
    """The register's own descriptor, `O_RDWR | O_APPEND | O_NOFOLLOW`, locked `LOCK_EX` (ledger-row.py round 4):
    the one descriptor the lock, the read and the write go through, released by its close. The lock is tried
    non-blocking every LOCK_POLL seconds for `wait` seconds; a lock not taken by then is a refusal naming the file."""
    try:
        descriptor = os.open(units_path, os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW)
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
    """The whole text through the locked descriptor: `os.fstat` for the length n0, `os.pread` from offset 0 looped
    until n0 bytes, decoded as strict UTF-8. Every failure is a refusal naming the register. Returns (n0, text)."""
    try:
        status = os.fstat(descriptor)
    except OSError as error:
        refuse(f"cannot read the register {units_path}: fstat: {error.strerror}")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the register {units_path} is not a regular file")
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
    try:
        return length, b"".join(chunks).decode("utf-8")
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


def existing_unit(store, units_path, rows, ticket_id):
    """The unit whose row's brief cell is this ticket's brief, after the store's consistency checks, or None."""
    pattern = re.compile(re.escape(f"{BRIEFS_DIR}/U") + r"([0-9]+)" + re.escape(f"-ticket-{ticket_id}.md"))
    found = [(number, cells, match) for number, cells in rows if (match := pattern.fullmatch(cells[6]))]
    if not found:
        return None
    if len(found) > 1:
        lines = ", ".join(str(number) for number, _, _ in found)
        refuse(f"{len(found)} rows of {units_path} (lines {lines}) name {found[0][1][6]}; the store is inconsistent")
    number, cells, match = found[0]
    unit = f"U{match.group(1)}"
    if cells[0] != unit:
        refuse(f"{units_path}:{number} has id {cells[0]!r} but its brief cell {cells[6]} names {unit}; inconsistent")
    store_file(store, cells[6], "brief")
    return unit


def next_unit(rows):
    numbers = [int(match.group(1)) for _, cells in rows if (match := UNIT_ID.fullmatch(cells[0]))]
    return f"U{max(numbers, default=0) + 1}"


def cell_check(name, value):
    """A cell holds neither a tab nor a line break: the register is tab-separated lines."""
    for character, label in CONTROL:
        if character in value:
            refuse(f"the {name} holds {label}; a cell holds neither a tab nor a newline")


def write_brief(brief_path, text):
    """The brief created `O_CREAT | O_EXCL | O_NOFOLLOW` at mode 0600, written whole and synced. Returns None, or
    the failure text naming the brief after the partial file is removed (exit 1 is the caller's)."""
    try:
        descriptor = os.open(brief_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        refuse(f"the brief {brief_path} exists but no row of the register names it; the store is inconsistent")
    except OSError as error:
        return f"cannot write {brief_path}: open: {error.strerror}"
    data = text.encode("utf-8")
    failure = None
    try:
        offset = 0
        while offset < len(data):
            written = os.write(descriptor, data[offset:])
            if written <= 0:
                raise OSError(errno.EIO, "short write")
            offset += written
        os.fsync(descriptor)
    except OSError as error:
        failure = f"cannot write {brief_path}: {error.strerror}"
    try:
        os.close(descriptor)
    except OSError as error:
        failure = failure or f"cannot write {brief_path}: close: {error.strerror}"
    if failure is not None:
        return remove_brief(brief_path, failure)
    return None


def remove_brief(brief_path, failure):
    try:
        os.unlink(brief_path)
    except OSError as error:
        return f"{failure}; the brief {brief_path} could not be removed: {error.strerror}"
    return f"{failure}; the brief is removed"


def append_line(descriptor, units_path, length, line):
    """One `os.write` of the line's bytes after an `lseek` to the end (O_APPEND puts it there whatever the offset;
    XNU applies RLIMIT_FSIZE at the descriptor's offset, so the seat makes a size limit cut the write on both
    kernels), its count compared with the line's length, then `os.fsync`. A failure truncates the file back to
    `length`. Returns None, or the failure text naming the register."""
    data = line.encode("utf-8")
    try:
        os.lseek(descriptor, 0, os.SEEK_END)
        written = os.write(descriptor, data)
    except OSError as error:
        return truncate_back(descriptor, units_path, length, f"write: {error.strerror}")
    if written != len(data):
        return truncate_back(descriptor, units_path, length, f"short write, {written} of {len(data)} bytes")
    try:
        os.fsync(descriptor)
    except OSError as error:
        return truncate_back(descriptor, units_path, length, f"fsync: {error.strerror}")
    return None


def truncate_back(descriptor, units_path, length, cause):
    try:
        os.ftruncate(descriptor, length)
    except OSError as error:
        return (
            f"cannot write {units_path}: {cause}; the register {units_path} may hold a partial last line: "
            f"{error.strerror}"
        )
    return f"cannot write {units_path}: {cause}; truncated back to {length} bytes"


def now():
    return datetime.now(timezone.utc).strftime(TS_FORMAT)


def bind(args, store, program, facts, units_path, descriptor):
    """The critical section, under the lock the descriptor holds: the register read and parsed, the existing unit
    answered, else the brief written and the row appended. Returns (0, the stdout line) or (1, the failure text)."""
    length, text = read_register(descriptor, units_path)
    rows = parse_register(units_path, text)
    unit = existing_unit(store, units_path, rows, facts["id"])
    state = "existing"
    if unit is None:
        state = "new"
        unit = next_unit(rows)
        relative = f"{BRIEFS_DIR}/{unit}-ticket-{facts['id']}.md"
        brief_path, status = store_path(store, relative, "brief")
        if status is not None:
            refuse(f"the brief {relative} exists but no row of the register names it; the store is inconsistent")
        cells = (
            unit,
            TRACK,
            STATE,
            args.branch,
            args.pr,
            args.head,
            relative,
            f"ticket={facts['id']}; thread={facts['thread']}; sender={facts['sender']}; decision={facts['decision']}; "
            f"bound by {LEVER} {now()}",
        )
        for name, value in zip(UNITS_HEADER, cells):
            cell_check(f"{name} cell", value)
        line = "\t".join(cells) + "\n"
        lead = "" if text == "" or text.endswith("\n") else "\n"
        failure = write_brief(brief_path, render_brief(unit, facts, args.pr, args.head, program))
        if failure is not None:
            return 1, failure
        failure = append_line(descriptor, units_path, length, lead + line)
        if failure is not None:
            return 1, remove_brief(brief_path, failure)
    else:
        relative = f"{BRIEFS_DIR}/{unit}-ticket-{facts['id']}.md"
    return 0, f"unit={unit} brief={relative} state={state} program={program} line=Program-Unit: {program}/{unit}"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    argument_rule(argv)
    args = parser().parse_args(argv)
    check_arguments(args)
    store, program = store_dir(args.store)
    ticket_id, document = binding_ticket(read_tickets(args.db), args.pr)
    facts = ticket_facts(ticket_id, document)
    expected = f"{BRANCH_PREFIX}{facts['name']}"
    if args.branch != expected:
        refuse(f"the branch {args.branch!r} is not the ticket's {expected}")
    units_path = store_file(store, UNITS_FILE, "register")
    descriptor = open_register(units_path, args.lock_wait)
    try:
        code, text = bind(args, store, program, facts, units_path, descriptor)
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
            text = f"the register {units_path} was appended ({text}) but its close failed: {error.strerror}"
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
