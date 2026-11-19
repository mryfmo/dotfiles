#!/usr/bin/env -S python3 -I
"""Write one coordinator row of the program store's `ledger.tsv` by the reader's grammar (regime-cutover U222).

Every row the coordinator wrote by hand had four ways of being wrong that the readers found later: a merge row whose
verifier cell carried a note hid three merges from `rounds-check.py` (a merge row is one whose verifier is exactly
`pr-merge.sh`; decisions 2026-11-06T00:18:19Z); a `-` receipt row written against an audited head became the newest
row of that head and voided every later carry from it, since `pr-merge.sh` reads the newest row of the earlier head
whatever its verdict (2026-11-05T23:53:08Z); a verdict file stored under a fix unit's name while the row named the
parent unit refused the next audit (2026-11-07T12:39:21Z); a carried row whose digest ended with a semicolon failed
the merge gate's whole-word regex (2026-11-04T07:04:58Z). This lever composes the row from named arguments and the
clock, fixes the verdict and the verifier's words per kind so no caller types them, refuses each of those shapes by
name, re-reads the ledger plus the new line through `ledger.parse_ledger` before anything is written, and appends
the one line. It states no grammar of its own: `ledger.py` beside it is the one reader, imported from that path alone
(as `audit-carry.py` imports it), and a row the reader would refuse is never written.

`ledger-row.py <store> <kind> ...`, one subcommand per kind; `ts` is now in UTC under the reader's `TS_FORMAT` (the
`daily` kind's is its `--swept-at`, the sweep's own time; round 6):
- `merged --pr <pr> --head <sha> --unit <unit> --receipt <line> [--note <text>]`: verdict `-`, verifier exactly
  `pr-merge.sh`, evidence the `pr-merge.sh` receipt (`merged pr=<pr> head=<sha8 or sha40> commit=<40 hex>`, whose pr
  and head must equal the arguments) then `; <note>`.
- `carried --pr --head --unit --line <audit-carry.py stdout> --note <text> [--evidence-note <text>]`: verdict
  `carried`, verifier `audit-carry.py (<note>)`, evidence the line, which must hold `carried <earlier> <head> <sha256>`
  as the merge gate reads it (the digest followed by the end, whitespace, `;`, `,`, `.` or `)`; U180) with the second
  sha the head, then `; <evidence note>`.
- `sweep --head --unit --seat <seat> --run <n> --task <U<n>> --findings sweeps/<dir>/findings.json --count <n>
  [--pr <pr>]`: pr cell `-`, verdict `sweep`, verifier `security-audit-skill <pin8> (full audit mode on the srt worker
  seat <seat>, run-<n>; TASK <U<n>>)` with `<pin8>` the first 8 characters of the manifest's
  `assets.security-audit-skill.pin` (`~/.agents/agent-config.yaml`, the deployed manifest alone since U597 round 9,
  read as text by `pr-merge.sh`'s `sweep_pin_probe` reads it: no PyYAML under `-S`), evidence `<findings>; pr <pr or
  none>; <count> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS`; the findings path must be a
  regular file under the store.
- `audit --pr --head --unit --verdict-file verdicts/<unit>-<sha8>.md --verifier <text> [--class <word>]`: the verdict
  word is the file's last line (`Verdict: correct` or `Verdict: incorrect`), never an argument; the file is named by
  the row's unit and the head's first 8, is a regular file under the store and is scored (one `Filed: <n>` line,
  `audit-carry.py`'s predicate); the verifier starts with `pr-audit.sh`; evidence `class=<word> <file>: Blocking: <n>;
  Filed: <n>; Verdict: incorrect` (the class required; standing order 39) or the same without the class for correct.
- `pushed --pr <pr or -> --head --unit --how <text> --what <text>`: verdict `pushed`, verifier `coordinator (<how>)`,
  evidence the what.
- `receipt --pr <pr> --head <sha or -> --unit --lever <name> --receipt <line> [--note <text>]`: verdict `-`, verifier
  the lever name alone, one of `pr-update-branch.sh`, `pr-close.sh`, `records-sync.sh`; evidence the receipt then `;
  <note>`.
- `daily --head <40 hex> --seat <seat> --run <n> --task daily-<YYYY-MM-DD> --findings
  sweeps/<dir>/findings.json --swept-at <YYYY-MM-DDTHH:MM:SSZ>` (regime-cutover U597 round 4): not a ledger row but
  the one row of the store's `daily-sweeps.tsv` (header `ts head_sha verifier evidence`, the file `ledger.py daily`
  reads and `pr-merge.sh` requires within 24 hours before a head outside every sweep class skips its own sweep row),
  ts the sweep's own time (round 6, verdicts/U597-10d46fe0.md: `--swept-at`, the RESULT message's bus timestamp the
  coordinator passes, under the reader's strict form, refused when later than the clock at the write (round 7: no
  future slack in the writer; the reader's 60-second allowance is for rows written by another host's clock) or more
  than 24 hours before it, since such a row would be born stale; round 5 dated the row by the clock, so a delayed
  recording granted a fresh window), head main's head the sweep ran at, verifier as the `sweep` kind composes it
  (`security-audit-skill <pin8> (full audit mode on the srt worker seat <seat>, run-<n>; TASK <task>)`), evidence the
  daily row's own six fields in this order (round 9, the grammar `ledger.parse_daily` requires field by field, so a
  row of a unit's sweep shape is a malformed store, never a daily row): `<findings>; <count> findings;
  validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; validators sha256 <8 hex> <8 hex>; recorded <ts>`,
  with the findings path a regular file of this user under the store that the writer opens itself (round 6:
  `O_NOFOLLOW`, `fstat` a regular file of this uid, strict UTF-8, JSON, a list whose every element is an object, else
  a refusal naming the file; `<count>` is that list's length and `--count` is gone from this kind), the two PASS words
  earned (round 7) by running the installed skill's two validators itself, `validate-findings.cjs` over the findings
  file and `validate-coverage-ledger.cjs` over the `coverage-ledger.json` beside it: since round 9 each validator and
  the `report-schema.json` that `validate-findings.cjs` loads from its own directory is read from the manifest's
  `assets.security-audit-skill` install `~/.agents/skills/security-audit` alone (round 8: `--skill-dir` is gone; each
  file is reached from `HOME` through real directories, no component a symlink, opened with no link followed, a
  regular file of this user), copied into a private directory the writer makes under TMPDIR (`tempfile.mkdtemp`,
  mode 0700, removed on every exit), the copy hashed against the manifest's
  `assets.security-audit-skill.validators_sha256.<file>` pin (three pins: the two validators and the schema), the
  validator copies scanned for a sibling they load (`require("./…")`, `path.join(__dirname, "…")`) that has no pin,
  and `node` run on the copies, so what is hashed is what runs and a concurrent skill update changes nothing the
  row records (round 8 ran node on the installed path after the hash, and loaded the schema from the installation
  directory unhashed); a differing digest, a missing or doubled pin, a missing file, an unpinned sibling, a copy that
  cannot be made or hashed is a refusal naming the file and, for a digest, both digests, with nothing written; each
  validator runs from `/` with the environment reduced to PATH, stdin closed and a timeout, its status read, and no
  `node` on PATH, a missing coverage ledger or a validator exiting non-zero is a refusal naming the validator's first
  stderr line with nothing written; `validators sha256 <8 hex> <8 hex>` the first 8 hex of the two validator pins
  the copies were held to, in the order validate-findings.cjs, validate-coverage-ledger.cjs (round 9: `pr-merge.sh`
  compares them with the manifest's pins, so a row whose validators were checked against other digests admits no
  exemption); `recorded <ts>` the clock at the write). The task is the coordinator's daily dispatch id alone,
  `daily-<YYYY-MM-DD>` (round 8, verdict U597-a28e4793 P2 at :468: a unit id was accepted, so an ordinary unit's sweep
  could stand as the day's full sweep of main's head; a unit's sweep is a `sweep` row of the ledger, never a daily
  row), whose day is the UTC day `--swept-at` falls on or the day before it (round 9, verdict U597-c37800e3 P2 at
  :543: the id is fixed at dispatch, and a full sweep that crosses midnight finishes under the id it was dispatched
  with; any other day is refused naming both days). The manifest is `~/.agents/agent-config.yaml` alone (round 9:
  `--manifest <path>` is gone from the interface, since a caller-selected manifest let the row carry the expected
  skill pin while its validators were checked against other digests; the tests set `HOME` to a scratch home holding
  a manifest). Round 5 (verdicts/U597-1b3c4b1d.md): the
  day's first file, the header and the first row, is written whole through a temporary file of the store directory
  and `os.replace` under the ledger's lock (so two first writers serialise and the second appends), and appears whole
  or not at all, where round 4's `O_CREAT | O_EXCL` header write left a malformed file after a short write that no
  retry repaired; a later row is read, checked through `ledger.parse_daily` and appended as one write under the daily
  file's own lock as the ledger is; a file whose header is malformed is refused naming the line, never repaired; and a
  `--findings` path an existing daily row already names (the evidence's first `;`-separated field) or a `(seat, run)`
  one already carries (the verifier's `seat <seat>, run-<n>;` fields; round 6, since the same run's findings copied
  to another path refreshed the window) is refused naming that row's ts and line, so a finished run is not
  re-recorded.

Two refusals cross rows, before any write (standing order 21): a `pushed` or `receipt` row whose head is 40 hex while
`ledger.already_audited` names an audit row of the same pull request at that head is refused naming that row's ts (the
`merged` kind is exempt: the merge is the last row of a head); and any cell holding a tab, a newline or a carriage
return, or any other control character (round 7, with the reader), is refused naming the cell, the store argument
included. A store whose ledger does not parse is exit 2 naming
the line. Exit 0 prints one line, `appended <ts> line <n>`; every refusal is exit 2 with one stderr line; a write that
fails is exit 1 naming the file. Round 2 (U222b, verdicts/U222-9187830e.md): every file read under the store
(`ledger.tsv`, the verdict file, the findings file) follows one path rule, its `os.path.realpath` under the realpath of
the store, each component `os.lstat`ed and no link, a regular file at the end; the findings directory name is
`[A-Za-z0-9._-]` alone (the sweep reader splits the evidence on `;`); the deployed manifest is opened, and any failure
to open or read it is a refusal naming the file (round 9: a missing one too, with no fall-through to the checkout's
copy and no `--manifest`); the carried separator class is the
gate's literal set under `re.ASCII`; and the import of `ledger.py` writes no bytecode (`sys.dont_write_bytecode`).
Round 3 (U222c, verdicts/U222-0fc41a81.md): the read, the check and the write run under one exclusive lock, so two
levers writing at once never lose each other's row, and every argument round-trips through strict UTF-8 before
anything is read (Python decodes argv with surrogateescape). Round 4 (U222d, verdicts/U222-238f0f55.md): the lever
makes no file but the ledger (rounds 2 and 3 each wrote a helper file in the store, a temporary and a lock file, and
the store's own walks refuse a name beginning with `.`), and since U597 round 4 the `daily-sweeps.tsv` the `daily`
kind writes, on the first daily row whole through a temporary file `daily-sweeps.tsv.<random>.tmp` of the store
directory that `os.replace` renames onto the name (U597 round 5; a failed first write removes it, so no partial file
and no temporary stays). One descriptor, `os.open(<file>, O_RDWR | O_APPEND)`,
carries the lock, the read and the write: `fcntl.flock(LOCK_EX | LOCK_NB)` tried every 0.1 s for `--lock-wait`
seconds (default 30), expiry a refusal naming the ledger (advisory: the readers, `ledger.py` and `pr-merge.sh`, open
the file without a lock and are unaffected); under it `os.fstat` gives the length n0, `os.pread` from 0 until n0 bytes
gives the text, the row is composed and checked, the text plus the line is parsed, then one `os.write` of the line
(O_APPEND puts it at the end), its count compared with the line's length, `os.fsync`, and the close, which releases
the lock. A write that fails or returns short, or a fsync that fails, truncates the file back to n0 (`os.ftruncate`)
and exits 1 naming the ledger and the error; a truncate that fails is named too (`the ledger <path> may hold a
partial last line: <error>`), exit 1. Every `OSError` of the sequence is one stderr line, never a traceback: exit 2
before the write (open, flock, fstat, pread: a read refusal, standing order 21), exit 1 from the write on (write,
fsync, ftruncate, close). Every element of `sys.argv` passes the one argument rule (strict UTF-8; no tab, newline or
carriage return) before argparse runs, so an option argparse converts (`--lock-wait`) cannot escape it. No mode of
any file is changed.
Installed as `~/.local/bin/common/ledger-row.py` in `brief-check.py`'s form (the generator's copy and pin); it needs
`ledger.py` beside it wherever it runs.
"""

from __future__ import annotations

import argparse
import errno
import fcntl
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone

# `python3 -I -S` still writes `__pycache__` beside an imported module: `ledger.tsv` is the one file this lever writes.
sys.dont_write_bytecode = True

LEVER = "ledger-row"
HERE = os.path.dirname(os.path.realpath(__file__))

# The write's lock (round 4) is `LOCK_EX` on the ledger's own descriptor, tried non-blocking every LOCK_POLL seconds
# for LOCK_WAIT seconds (`--lock-wait` sets the wait); advisory, so the readers, which take no lock, are unaffected.
LOCK_WAIT = 30.0
LOCK_POLL = 0.1
# The characters no cell and no argument holds: a tab or a line break (the ledger is tab-separated lines) and, since
# U597 round 7, every other control character (`\x00` to `\x1f`, `\x7f`: a NUL in a cell is dropped by bash's `$(...)`
# when a lever captures the row, so the lever would read another text than the file holds), the reader's CONTROL rule.
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))
CONTROL_CHARACTER = re.compile(r"[\x00-\x1f\x7f]")


def control_label(value):
    """How a refusal names the first control character of `value`, or None when it holds none: the three named
    characters by their names, any other as `a control character U+00xx`."""
    for character, label in CONTROL:
        if character in value:
            return label
    found = CONTROL_CHARACTER.search(value)
    if found is None:
        return None
    return f"a control character U+{ord(found.group()):04X}"


def refuse(reason):
    """One stderr line in the levers' words, exit 2; nothing was written."""
    print(f"{LEVER}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def beside(name):
    """The module `<name>.py` beside this file, loaded from that path alone (the lever runs under `python3 -I`, which
    puts no script directory on sys.path); a missing or unreadable file is a refusal naming it (standing order 21),
    read by the open itself and never by a stat whose failure would pass as absence."""
    path = os.path.join(HERE, f"{name}.py")
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    except FileNotFoundError:
        refuse(f"{path}: no {name}.py beside the lever; the row is composed and judged through it alone")
    except OSError as error:
        refuse(f"{path}: cannot read {name}.py beside the lever: {error.strerror}")
    return module


ledger = beside("ledger")

# A unit id, the body's `U<n>` or a fix unit `U<n><letter>` (standing order 24).
UNIT = re.compile(r"^(U[0-9]+)([a-z]?)$")
DIGITS = re.compile(r"^(0|[1-9][0-9]*)$")
# The receipt pr-merge.sh prints: `merged pr=<pr> head=<sha> commit=<40 hex>`, then the end or more words.
MERGE_RECEIPT = re.compile(r"^merged pr=(\S+) head=(\S+) commit=([0-9a-f]{40})(?:$|[\s;,.)])")
# The line audit-carry.py prints, as pr-merge.sh's carried_evidence_re reads it (U180): the digest is a whole word
# before the end or one of the gate's literal separators, space, tab, `;`, `,`, `.` and `)`. The gate's `[[:space:]]`
# runs in the C locale, so the class is ASCII: a non-breaking space is no separator (round 2 finding 5), and a newline
# or a carriage return never reaches here (cell_check).
CARRIED_LINE = re.compile(r"(?:^|[ \t])carried ([0-9a-f]{40}) ([0-9a-f]{40}) ([0-9a-f]{64})(?:$|[ \t;,.)])", re.ASCII)
RECEIPT_LEVERS = ("pr-update-branch.sh", "pr-close.sh", "records-sync.sh")
AUDIT_VERIFIER = "pr-audit.sh"
VERDICT_LINE = re.compile(r"^Verdict: (correct|incorrect)$")
# The two count lines the scored reader writes (U125 round a); `Filed:` is audit-carry.py's `scored` predicate.
FILED_LINE = re.compile(r"^Filed: (0|[1-9][0-9]*)$", re.MULTILINE)
BLOCKING_LINE = re.compile(r"^Blocking: (0|[1-9][0-9]*)$", re.MULTILINE)
CLASS_WORD = re.compile(r"^[A-Za-z0-9_-]+$")
# The findings file under the store: the sweep reader splits the evidence on `;` and reads the first field as the path,
# so the directory name is `[A-Za-z0-9._-]` alone (round 2 finding 3).
SWEEP_FINDINGS = re.compile(r"^sweeps/([A-Za-z0-9._-]+)/findings\.json$")
SWEEP_SEAT = re.compile(r"^\S+$")
# The task id of the coordinator's daily dispatch (U597 round 4), the kit's `daily-sweep-brief.md` template: one per
# UTC day, and the only task a daily row records (round 8: a unit id, which round 4 accepted beside it, is a `sweep`
# row's task, never a daily row's); its day is the UTC day `--swept-at` falls on or the day before it (round 9: the id
# is fixed at dispatch, and a full sweep that crosses midnight finishes under it).
DAILY_TASK = re.compile(r"^daily-([0-9]{4}-[0-9]{2}-[0-9]{2})$")
DAILY_TASK_FORM = "daily-<YYYY-MM-DD>"
# The oldest `--swept-at` the daily kind records (round 6): the window pr-merge.sh reads with (its DAILY_SWEEP_MAX_AGE,
# 86400 seconds); a row dated earlier would be born stale and stand for no head.
SWEPT_AT_MAX_AGE = 86400
# The installed `security-audit` skill (round 7): the manifest's `assets.security-audit-skill` install path, written
# by scripts/update-agent-assets.sh's update_security_audit_skill as `${HOME}/.agents/skills/security-audit`, the one
# place the validators are read from (round 8: `--skill-dir` named any directory, so a passing exit proved nothing of
# the pinned validators). Round 9 (verdict U597-c37800e3 P2 at :654: node reopened each validator by pathname after
# the hash and loaded the schema from the installation directory, so a concurrent skill update could make the writer
# record a pass for bytes outside the checked installation): the two validators and `report-schema.json`, the one
# file `validate-findings.cjs` loads from its own directory (`path.join(__dirname, "report-schema.json")`; both
# validators `require` node's builtins alone besides), are each copied into a private directory of this writer,
# hashed as the copy against the manifest pin `assets.security-audit-skill.validators_sha256.<file>`, and node runs
# the copies, so what is hashed is what runs. VALIDATOR_FILES names the pinned set; VALIDATORS pairs each validator
# with the file it runs over, the findings file the row names and the coverage ledger beside it.
SKILL_DIR = "~/.agents/skills/security-audit"
SKILL_PARTS = (".agents", "skills", "security-audit")
VALIDATORS_KEY = "validators_sha256"
COVERAGE_LEDGER = "coverage-ledger.json"
SCHEMA = "report-schema.json"
VALIDATORS = (("validate-findings.cjs", "findings.json"), ("validate-coverage-ledger.cjs", COVERAGE_LEDGER))
VALIDATOR_FILES = ("validate-findings.cjs", "validate-coverage-ledger.cjs", SCHEMA)
# A sibling a validator loads from its own directory (round 9): a relative `require("./x")` or a `path.join(__dirname,
# "x")`; every such file must be one of VALIDATOR_FILES, pinned and copied beside the validator, else the copy would
# load a file no pin holds (or find none) and the writer refuses by name.
SIBLING_REFERENCE = re.compile(rb"""(?:require\(\s*["']\.{1,2}/([^"']+)["']\s*\)|__dirname\s*,\s*["']([^"']+)["'])""")
PRIVATE_PREFIX = "ledger-row.validators."
# Seconds one validator may run; the skill's own tests finish in well under one.
VALIDATOR_TIMEOUT = 120
# The one directory the validators run from, and the one variable they get: neither the store nor the checkout, and
# none of the caller's `NODE_OPTIONS`, `NODE_PATH` or other environment (the `-I` of a python run, for node).
VALIDATOR_CWD = "/"
# The manifest, read as text by one indentation rule (pr-merge.sh `sweep_pin_probe`, brief-check.py `manifest_levers`):
# a bare `<key>:` line opens a mapping, a line indented no deeper closes it, and the pin is the one `pin: <40 hex>`
# line at the indentation of the `security-audit-skill` asset's first field under the top-level `assets:`.
MANIFEST_PARTS = (".agents", "agent-config.yaml")
MAPPING_KEY = re.compile(r"^(\S+):$")
PIN_LINE = re.compile(r"^pin: ([0-9a-f]{40})$")
# One line of the asset's `validators_sha256:` mapping (round 8): `<file>: <64 hex>`, the file's name as the installed
# file is named.
DIGEST_LINE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*): ([0-9a-f]{64})$")
ASSET_KEYS = ["assets", "security-audit-skill"]


def manifest_lines():
    """The deployed manifest `~/.agents/agent-config.yaml` as (path, lines), the one manifest this writer reads
    (round 9: `--manifest <path>` is gone, since a caller-selected manifest let a row carry the expected skill pin
    while its validators were checked against other digests, and round 8's fall-through to the checkout's copy is
    gone with it, since the deployed writer has no checkout beside it): HOME must be an absolute path, and any
    failure to open or read the file, a missing one included, is a refusal naming it (standing order 21)."""
    home = os.environ.get("HOME", "")
    if not home or not os.path.isabs(home):
        refuse(f"HOME {home!r} is not an absolute path; the manifest ~/{'/'.join(MANIFEST_PARTS)} is read under it")
    manifest = os.path.join(home, *MANIFEST_PARTS)
    try:
        with open(manifest, encoding="utf-8") as handle:
            return manifest, handle.read().splitlines()
    except OSError as error:
        refuse(f"cannot read the manifest {manifest}: {error.strerror}")
    except UnicodeDecodeError as error:
        refuse(f"cannot read the manifest {manifest}: not UTF-8: {error.reason}")


def manifest_asset(lines):
    """The `assets.security-audit-skill` block of the manifest's lines as (pins, digests): every `pin: <40 hex>` line
    at the indentation of the asset's fields, and, under the asset's `validators_sha256:` key, every `<validator>:
    <64 hex>` line at the indentation of that mapping's fields as `{validator: [digest, ...]}` (round 8). Read as
    text by the one indentation rule (no PyYAML under `-S`): a bare `<key>:` line opens a mapping, a line indented no
    deeper closes it; nothing else of YAML is read."""
    keys = []  # the open mapping keys as (indentation, key), outermost first
    asset = None  # the indentation of the `security-audit-skill:` key while its block is open
    fields = None  # the indentation of the asset's fields, fixed by the first
    digests_open = False  # inside the asset's `validators_sha256:` mapping
    digest_fields = None  # the indentation of that mapping's fields, fixed by the first
    pins = []
    digests = {}
    for line in lines:
        text = line.lstrip(" ")
        if not text or text.startswith("#"):
            continue
        indent = len(line) - len(text)
        if asset is not None:
            if indent > asset:
                if fields is None:
                    fields = indent
                if indent == fields:
                    digests_open = text == f"{VALIDATORS_KEY}:"
                    digest_fields = None
                    match = PIN_LINE.match(text)
                    if match:
                        pins.append(match.group(1))
                elif digests_open and indent > fields:
                    if digest_fields is None:
                        digest_fields = indent
                    if indent == digest_fields:
                        match = DIGEST_LINE.match(text)
                        if match:
                            digests.setdefault(match.group(1), []).append(match.group(2))
                continue
            asset = None
            fields = None
            digests_open = False
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if [key for _, key in keys] == ASSET_KEYS:
                asset = indent
    return pins, digests


def manifest_pin(manifest, lines):
    """The one `assets.security-audit-skill.pin` of the manifest's lines, 40 hex, or a refusal naming the file."""
    pins, _ = manifest_asset(lines)
    if len(pins) != 1:
        refuse(
            f"{manifest} holds {len(pins)} assets.security-audit-skill.pin lines of 40 hex, not one; the sweep "
            "verifier's pin word is read from it"
        )
    return pins[0]


def manifest_validator_pins(manifest, lines):
    """The sha256 pin of each file of VALIDATOR_FILES, `assets.security-audit-skill.validators_sha256.<file>` of the
    manifest's lines, exactly one 64-hex line each, as `{file: digest}`, or a refusal naming the file and the key
    (round 8: the installed validator's bytes are held to it before `node` runs it; round 9: the schema too, and the
    copies are what is hashed and run)."""
    _, digests = manifest_asset(lines)
    pins = {}
    for name in VALIDATOR_FILES:
        found = digests.get(name, [])
        if len(found) != 1:
            refuse(
                f"{manifest} holds {len(found)} assets.security-audit-skill.{VALIDATORS_KEY}.{name} lines of 64 hex, "
                "not one; the installed file's copy is compared with it before the validators run, so a manifest "
                "without it earns no PASS"
            )
        pins[name] = found[0]
    return pins


def cell_check(name, value):
    """A cell holds neither a tab, a line break nor any other control character (round 7): the ledger is
    tab-separated lines, and the reader refuses a control character in any cell."""
    label = control_label(value)
    if label is not None:
        refuse(f"the {name} holds {label}; a cell holds neither a tab, a newline nor a control character")


def check_unit(unit):
    if not UNIT.match(unit):
        refuse(f"the unit {unit!r} is not U<n> or U<n><letter>")


def check_head(head, dash=False):
    if dash and head == "-":
        return
    if not ledger.SHA.match(head):
        refuse(f"the head {head!r} is not 40 hex" + (" or '-'" if dash else ""))


def check_pr(pr, dash=False):
    if dash and pr == "-":
        return
    if not ledger.PULL_REQUEST.match(pr):
        refuse(f"the pull request {pr!r} is not a decimal number" + (" or '-'" if dash else ""))


def now():
    """The clock, in UTC under the reader's one form; never an argument."""
    return datetime.now(timezone.utc).strftime(ledger.TS_FORMAT)


def compose(ts, unit, pr, head, verdict, verifier, evidence):
    """One frozen Row of the reader's header; the line number is the reader's to assign."""
    return ledger.Row(ledger.timestamp(ts), unit, pr, head, verdict, verifier, evidence, 0, ts)


def with_note(text, note):
    return text if note is None else f"{text}; {note}"


def merged_row(args):
    """`merged`: verdict `-`, verifier exactly `pr-merge.sh` (rounds-check.py's merge row; the 00:18:19Z lesson)."""
    check_pr(args.pr)
    check_head(args.head)
    match = MERGE_RECEIPT.match(args.receipt)
    if match is None:
        refuse("the receipt is not pr-merge.sh's 'merged pr=<pr> head=<sha> commit=<40 hex>': " + repr(args.receipt))
    if match.group(1) != args.pr:
        refuse(f"the receipt's pr {match.group(1)} is not the argument {args.pr}")
    if match.group(2) not in (args.head, args.head[:8]):
        refuse(f"the receipt's head {match.group(2)} is not the argument {args.head} or its first 8")
    return compose(now(), args.unit, args.pr, args.head, "-", "pr-merge.sh", with_note(args.receipt, args.note))


def carried_row(args):
    """`carried`: the digest lever's line as a whole word before a separator (the 07:04:58Z lesson)."""
    check_pr(args.pr)
    check_head(args.head)
    match = CARRIED_LINE.search(args.line)
    if match is None:
        refuse(
            "the line holds no 'carried <earlier head> <head> <sha256>' as the merge gate reads it (the digest "
            f"followed by the end, whitespace, ';', ',', '.' or ')'): {args.line!r}"
        )
    if match.group(2) != args.head:
        refuse(f"the line carries {match.group(2)}, not the head {args.head}")
    if match.group(1) == args.head:
        refuse(f"the line carries {args.head} from itself; a carried head rests on an earlier audited head")
    verifier = f"audit-carry.py ({args.note})"
    return compose(now(), args.unit, args.pr, args.head, "carried", verifier, with_note(args.line, args.evidence_note))


def sweep_row(args, store):
    """`sweep`: the exact row the AGENTS.md Audit sweep rule defines, the pin word from the manifest."""
    check_head(args.head)
    if not UNIT.match(args.task):
        refuse(f"the task unit {args.task!r} is not U<n> or U<n><letter>")
    if args.pr is not None:
        check_pr(args.pr)
    if not DIGITS.match(args.count):
        refuse(f"the count {args.count!r} is not a decimal number")
    verifier = sweep_verifier(args)
    store_file(store, args.findings, "findings path")
    evidence = (
        f"{args.findings}; pr {'none' if args.pr is None else args.pr}; {args.count} findings; "
        "validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS"
    )
    return compose(now(), args.unit, ledger.SWEEP_PR, args.head, "sweep", verifier, evidence)


def audit_row(args, store):
    """`audit`: the word and the two counts read from the verdict file named by the row's unit and the head's first
    8 (the 12:39:21Z lesson); the class required for incorrect (standing order 39)."""
    check_pr(args.pr)
    check_head(args.head)
    expected = f"verdicts/{args.unit}-{args.head[:8]}.md"
    if args.verdict_file != expected:  # lint-comparisons: allow named-text: the unit and sha8 name the file (12:39:21Z)
        refuse(
            f"the verdict file {args.verdict_file!r} is not {expected!r}: the row's unit and the head's first 8 name it"
        )
    path = store_file(store, expected, "verdict file")
    try:
        text = ledger.read_text(path).replace("\r\n", "\n")
    except ledger.Malformed as error:
        refuse(str(error))
    lines = text.rstrip("\n").split("\n")
    match = VERDICT_LINE.match(lines[-1])
    if match is None:
        refuse(f"the last line of {expected} is {lines[-1]!r}, not 'Verdict: correct' or 'Verdict: incorrect'")
    word = match.group(1)
    filed = FILED_LINE.findall(text)
    blocking = BLOCKING_LINE.findall(text)
    if len(filed) != 1:
        refuse(
            f"{expected} is not a scored verdict: {len(filed)} 'Filed: <n>' lines, not one (audit-carry.py's scored)"
        )
    if len(blocking) != 1:
        refuse(f"{expected} holds {len(blocking)} 'Blocking: <n>' lines, not one")
    if not args.verifier.startswith(AUDIT_VERIFIER):
        refuse(
            f"the verifier {args.verifier!r} does not start with {AUDIT_VERIFIER!r}; an audit row is the audit lever's"
        )
    if word == "incorrect" and args.class_word is None:
        refuse("an incorrect row needs --class <word>, the finding class its evidence starts with (standing order 39)")
    if word == "correct" and args.class_word is not None:
        refuse("--class is for an incorrect row; the verdict file says correct")
    if args.class_word is not None and not CLASS_WORD.match(args.class_word):
        refuse(f"the class {args.class_word!r} is not one word")
    evidence = f"{expected}: Blocking: {blocking[0]}; Filed: {filed[0]}; Verdict: {word}"
    if word == "incorrect":
        evidence = f"class={args.class_word} {evidence}"
    return compose(now(), args.unit, args.pr, args.head, word, args.verifier, evidence)


def pushed_row(args):
    """`pushed`: verifier `coordinator (<how>)`, evidence the what."""
    check_pr(args.pr, dash=True)
    check_head(args.head)
    return compose(now(), args.unit, args.pr, args.head, "pushed", f"coordinator ({args.how})", args.what)


def receipt_row(args):
    """`receipt`: verdict `-`, verifier the lever name alone."""
    check_pr(args.pr)
    check_head(args.head, dash=True)
    if args.lever not in RECEIPT_LEVERS:
        refuse(f"the lever {args.lever!r} is not one of {', '.join(RECEIPT_LEVERS)}")
    return compose(now(), args.unit, args.pr, args.head, "-", args.lever, with_note(args.receipt, args.note))


def sweep_verifier(args):
    """The verifier of a `sweep` or `daily` row: the skill, its pin word from the manifest, the seat, the run and the
    task, after the run, the seat and the findings path are checked (the `sweep` kind's count is its own check; the
    `daily` kind reads its count from the file, round 6)."""
    if not DIGITS.match(args.run):
        refuse(f"the run {args.run!r} is not a decimal number")
    if not SWEEP_SEAT.match(args.seat):
        refuse(f"the seat {args.seat!r} is not one word")
    match = SWEEP_FINDINGS.match(args.findings)
    if match is None or match.group(1) in (".", ".."):
        refuse(
            f"the findings path {args.findings!r} is not sweeps/<dir>/findings.json under the store with <dir> of "
            "[A-Za-z0-9._-] alone (the sweep reader splits the evidence on ';')"
        )
    pin = manifest_pin(*manifest_lines())[:8]
    return (
        f"security-audit-skill {pin} (full audit mode on the srt worker seat {args.seat}, run-{args.run}; "
        f"TASK {args.task})"
    )


def daily_row(args, store):
    """`daily` (U597 round 4): the one row of `daily-sweeps.tsv`, main's head the sweep ran at, the verifier of the
    `sweep` kind, the evidence the daily row's own six fields (round 9; `ledger.parse_daily` requires each): the
    findings file (a regular file under the store, read for the count; round 6), the count, the two validators' PASS
    words earned by running the installed skill's two validators from private copies held to their manifest pins
    (round 7, round 8, round 9) over the findings file and the coverage ledger beside it, the first 8 hex of the two
    validator pins the copies were held to, and the recording time; the ts the sweep's own, `--swept-at` (round 6);
    the task the coordinator's daily id `daily-<YYYY-MM-DD>` alone, its day the UTC day `--swept-at` falls on or the
    day before it (round 8: a unit id is refused naming the grammar; round 9: the id is fixed at dispatch and a sweep
    that crosses midnight keeps it, so another day is refused naming both days)."""
    check_head(args.head)
    match = DAILY_TASK.match(args.task)
    if match is None:
        refuse(
            f"the task {args.task!r} is not {DAILY_TASK_FORM}, the coordinator's daily dispatch id; a daily row records "
            "the day's full sweep of main's head alone, and a unit's sweep is a sweep row of the ledger (the sweep kind)"
        )
    swept_at = check_swept_at(args.swept_at)
    day = swept_at.strftime(ledger.DAY_FORMAT)
    days = (day, (swept_at - timedelta(days=1)).strftime(ledger.DAY_FORMAT))
    if match.group(1) not in days:  # lint-comparisons: allow named-text: the two days the RESULT may fall under
        refuse(
            f"the task {args.task} names neither the UTC day of --swept-at {args.swept_at} ({days[0]}) nor the day "
            f"before it ({days[1]}); the daily id is fixed at dispatch and a sweep that crosses midnight keeps it, so "
            f"daily-{days[0]} or daily-{days[1]} alone records this RESULT"
        )
    verifier = sweep_verifier(args)
    findings_path = store_file(store, args.findings, "findings path")
    count = findings_count(findings_path, args.findings)
    pins = run_validators(args, store, findings_path)
    digests = " ".join(pins[validator][:8] for validator, _ in VALIDATORS)
    evidence = ledger.DAILY_SEPARATOR.join(
        (args.findings, f"{count} findings", *ledger.DAILY_PASSES, f"validators sha256 {digests}", f"recorded {now()}")
    )
    return ledger.DailyRow(swept_at, args.head, verifier, evidence, 0, args.swept_at)


def skill_file(home, name):
    """The installed skill file `~/.agents/skills/security-audit/<name>` as (path, bytes) (round 8): `HOME` must be
    an absolute path; every component below it (`.agents`, `skills`, `security-audit`, the file) is `os.lstat`ed and
    none is a symbolic link; the file is opened `O_RDONLY | O_NOFOLLOW`, its descriptor `fstat`ed a regular file of
    this user, and read whole. Any other outcome is a refusal naming the file: the validator that earns its PASS is
    the installed one, read through real directories alone and never from another place."""
    path = os.path.join(home, *SKILL_PARTS, name)
    if not home or not os.path.isabs(home):
        refuse(f"HOME {home!r} is not an absolute path; the installed skill's validator {path} is read under it")
    current = home
    for part in (*SKILL_PARTS, name):
        current = os.path.join(current, part)
        try:
            status = os.lstat(current)
        except OSError as error:
            refuse(
                f"the validator file {path} is not a regular file of this user under the installed skill "
                f"({current}: {error.strerror}); the daily row states a validator's PASS only after the pinned validator ran"
            )
        if stat.S_ISLNK(status.st_mode):
            refuse(
                f"{current}, a component of the validator file path {path}, is a symbolic link; the installed skill is read "
                "through real directories alone"
            )
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as error:
        refuse(f"cannot open the validator file {path}: {error.strerror}")
    chunks = []
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            refuse(f"the validator file {path} is not a regular file")
        if status.st_uid != os.geteuid():
            refuse(f"the validator file {path} is not this user's (owned by uid {status.st_uid}); it is not run")
        while True:
            chunk = os.read(descriptor, 1 << 16)
            if not chunk:
                break
            chunks.append(chunk)
    except OSError as error:
        refuse(f"cannot read the validator file {path}: {error.strerror}")
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
    return path, b"".join(chunks)


def private_directory():
    """A private directory for the validators' copies (round 9): `tempfile.mkdtemp` under `TMPDIR` (`/tmp` when
    unset or empty, as pr-merge.sh's reader_copies_make chooses it; the directory is named, so tempfile probes no
    candidate of its own), mode 0700 (mkdtemp's own, set again), a directory of this user; a failure is a refusal
    naming the place, and the caller removes the directory on every exit."""
    base = os.environ.get("TMPDIR") or "/tmp"
    try:
        directory = tempfile.mkdtemp(prefix=PRIVATE_PREFIX, dir=base)
        os.chmod(directory, 0o700)
    except OSError as error:
        refuse(
            f"cannot make the private directory for the validators' copies under {base}: {error.strerror}; the "
            "validators run from copies held to their pins alone, so nothing is written"
        )
    return directory


def pinned_copy(home, name, pins, manifest, directory):
    """The installed skill file `name` (skill_file) copied into the private `directory` as a new file of mode 0600,
    the copy read back and hashed, and its sha256 held to the manifest pin `validators_sha256.<name>` (round 9): what
    is hashed is what node runs. A copy that cannot be made, written whole or hashed is a refusal naming the file;
    a differing digest is a refusal naming the file and both digests. Returns (copy, bytes)."""
    path, data = skill_file(home, name)
    copy = os.path.join(directory, name)
    try:
        descriptor = os.open(copy, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            # `os.write` may land fewer bytes than given; the copy is written whole or the write is a failure.
            view = memoryview(data)
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise OSError(errno.EIO, f"a write of {written} bytes with {len(view)} to go")
                view = view[written:]
        finally:
            os.close(descriptor)
        with open(copy, "rb") as handle:
            copied = handle.read()
    except OSError as error:
        refuse(
            f"cannot copy the validator file {path} into {directory}: {error.strerror or error}; the validators run "
            "from copies held to their pins alone, so nothing is written"
        )
    digest = hashlib.sha256(copied).hexdigest()
    if digest != pins[name]:
        refuse(
            f"sha256 {digest} of the validator file {path} (hashed as its copy {copy}) differs from the pin "
            f"{pins[name]} of assets.security-audit-skill.{VALIDATORS_KEY}.{name} in {manifest}; the installed skill is "
            "not the pinned one, so nothing is written"
        )
    return copy, copied


def sibling_check(path, data):
    """Every file the validator at `path` loads from its own directory (SIBLING_REFERENCE over its bytes) is one of
    VALIDATOR_FILES, pinned and copied beside it (round 9); another is a refusal naming it."""
    for match in SIBLING_REFERENCE.finditer(data):
        sibling = (match.group(1) or match.group(2)).decode("utf-8", "replace")
        if sibling not in VALIDATOR_FILES:  # lint-comparisons: allow named-text: the sibling as the validator spells it
            refuse(
                f"{path} loads {sibling!r} from its own directory, a file with no assets.security-audit-skill."
                f"{VALIDATORS_KEY} pin; every file a validator loads beside itself is pinned and copied with it, so "
                "nothing is written"
            )


def run_validators(args, store, findings_path):
    """The installed skill's two validators, run by this writer before it states their PASS (round 7; the round-6 P2
    at daily_row: the statement was the coordinator's word after a JSON-shape check, so a findings set without the
    skill's required fields backed a daily exemption), each held to its pin first (round 8; the round-7 P2 at :489:
    `--skill-dir` took the validators from any directory, so a passing exit established nothing of the pinned
    validators), and since round 9 run from private copies (the round-8 P2 at :654: node reopened the installed path
    after the hash and loaded `report-schema.json` from the installation directory unhashed, so a concurrent skill
    update could make the writer record a pass for bytes outside the checked installation). The manifest's three
    `assets.security-audit-skill.validators_sha256` pins are read (manifest_validator_pins); `node` is the first on
    PATH (`shutil.which`); the coverage ledger is `coverage-ledger.json` beside the findings file, under the store's
    path rule; then, in a private directory of this writer (private_directory, removed on every exit), each file of
    VALIDATOR_FILES is read from the installed skill alone (skill_file), copied, and the copy hashed against its pin
    (pinned_copy), each validator copy is scanned for a sibling it loads that has no pin (sibling_check), and each
    validator then runs as `node <copy> <file>` from VALIDATOR_CWD with the environment reduced to PATH, stdin closed
    and a VALIDATOR_TIMEOUT, its status read: a node that cannot run, a run that expires, or an exit other than 0 is a
    refusal naming the validator, the file and the validator's first stderr line, and nothing is written. Returns
    the pins the copies were held to, `{validator: digest}`, which the row records as `validators sha256 <8> <8>`."""
    manifest, lines = manifest_lines()
    pins = manifest_validator_pins(manifest, lines)
    home = os.environ.get("HOME", "")
    node = shutil.which("node", path=os.environ.get("PATH", ""))
    if node is None:
        refuse(
            "no node on PATH; the skill's validators run under it, and the daily row states a validator's PASS only after it ran"
        )
    directory = args.findings.rsplit("/", 1)[0]
    targets = {
        "findings.json": (findings_path, args.findings),
        COVERAGE_LEDGER: (
            store_file(store, f"{directory}/{COVERAGE_LEDGER}", "coverage ledger path"),
            f"{directory}/{COVERAGE_LEDGER}",
        ),
    }
    private = private_directory()
    try:
        copies = {name: pinned_copy(home, name, pins, manifest, private) for name in VALIDATOR_FILES}
        for validator, _ in VALIDATORS:
            sibling_check(os.path.join(home, *SKILL_PARTS, validator), copies[validator][1])
        for validator, target in VALIDATORS:
            path, relative = targets[target]
            try:
                run = subprocess.run(
                    [node, copies[validator][0], path],
                    cwd=VALIDATOR_CWD,
                    env={"PATH": os.environ.get("PATH", "")},
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    timeout=VALIDATOR_TIMEOUT,
                    check=False,
                )
            except OSError as error:
                refuse(f"cannot run {node} {copies[validator][0]} {relative}: {error.strerror}; nothing is written")
            except subprocess.TimeoutExpired:
                refuse(f"{validator} did not finish within {VALIDATOR_TIMEOUT} seconds on {relative}; nothing written")
            if run.returncode != 0:
                first = run.stderr.decode("utf-8", "replace").splitlines()
                reason = first[0] if first else "no stderr"
                refuse(f"{validator} exited {run.returncode} on {relative}: {reason}; nothing is written")
    finally:
        shutil.rmtree(private, ignore_errors=True)
    return {validator: pins[validator] for validator, _ in VALIDATORS}


def check_swept_at(text):
    """`--swept-at` as a time (round 6): the RESULT message's bus timestamp under the reader's one form
    (`ledger.timestamp`: the shape, two digits in every field, then the calendar), no later than the clock at the
    write (round 7: no future slack here; a sweep's RESULT is never ahead of its recording, and the reader's
    `DAILY_FUTURE_SLACK` of 60 seconds is for rows another host's clock wrote, read on this one) and no earlier than
    the clock minus SWEPT_AT_MAX_AGE (24 hours, the window `pr-merge.sh` reads with: a row dated earlier would be born
    stale and stand for no head). Any other value is a refusal naming it and the clock."""
    at = ledger.timestamp(text)
    if at is None:
        refuse(
            f"--swept-at {text!r} is not {ledger.TS_FORM} (the RESULT message's bus timestamp in UTC, two digits in "
            "every field)"
        )
    clock = ledger.utc_now()
    clock_text = clock.strftime(ledger.TS_FORMAT)
    if at > clock:
        refuse(
            f"--swept-at {text} is in the future: later than the clock {clock_text}; a sweep's RESULT time is never "
            "ahead of its recording, and a row dated ahead would stand longer than its sweep (the reader's 60-second "
            "allowance is for rows written by another host's clock, not for this writer)"
        )
    if at < clock - timedelta(seconds=SWEPT_AT_MAX_AGE):
        refuse(
            f"--swept-at {text} is more than {SWEPT_AT_MAX_AGE} seconds (24 hours) before the clock {clock_text}; the "
            "row would be born stale, outside the window pr-merge.sh reads with, and stand for no head"
        )
    return at


def json_kind(value):
    """A JSON value's kind in the refusals' words."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "a boolean"
    if isinstance(value, (int, float)):
        return "a number"
    if isinstance(value, str):
        return "a string"
    if isinstance(value, list):
        return "a list"
    return "an object"


def findings_count(path, relative):
    """The count of the findings file a daily row names (round 6; the round-5 P2 at daily_row: the writer stated
    `<count> findings` and two validator passes after checking that the file existed, so invalid or truncated JSON
    backed a daily exemption): `path`, already held by store_file's path rule, is opened `O_RDONLY | O_NOFOLLOW`
    (the open itself follows no link at the end), its descriptor `fstat`ed a regular file of this user, read whole,
    decoded as strict UTF-8, parsed as JSON, and held to a list whose every element is an object (the skill's
    findings set); the list's length is the count the evidence states. Any other outcome is a refusal naming the
    file: the writer states no count it did not read."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as error:
        refuse(f"cannot open the findings file {relative}: {error.strerror}")
    chunks = []
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            refuse(f"the findings file {relative} is not a regular file")
        if status.st_uid != os.geteuid():
            refuse(f"the findings file {relative} is not this user's (owned by uid {status.st_uid}); it is not read")
        while True:
            chunk = os.read(descriptor, 1 << 16)
            if not chunk:
                break
            chunks.append(chunk)
    except OSError as error:
        refuse(f"cannot read the findings file {relative}: {error.strerror}")
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
    try:
        text = b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        refuse(f"the findings file {relative} is not UTF-8: {error.reason}")
    try:
        findings = json.loads(text)
    except ValueError as error:
        refuse(f"the findings file {relative} is not JSON: {error}")
    if not isinstance(findings, list):
        refuse(f"the findings file {relative} is not a JSON list of findings but {json_kind(findings)}")
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            refuse(
                f"the findings file {relative} holds {json_kind(finding)} at index {index}, not an object; a findings "
                "set is a list of objects"
            )
    return len(findings)


def refuse_if_audited(read, kind, row):
    """A `pushed` or `receipt` row at a 40-hex head that already has an audit row of the same pull request would
    become the newest row of an audited head and void every later carry from it (the 23:53:08Z lesson)."""
    if row.pr == "-" or not ledger.SHA.match(row.head_sha):
        return
    base, letter = UNIT.match(row.unit).groups()
    units = (row.unit, base) if letter else (row.unit,)
    for unit in units:
        try:
            audit = read.already_audited(unit, row.head_sha, row.pr)
        except ledger.Malformed as error:
            refuse(str(error))
        if audit is not None:
            refuse(
                f"head {row.head_sha} of pull request {row.pr} already has an audit row ({audit.ts_text}, line "
                f"{audit.line}, {audit.verdict}; ledger.already_audited): a {kind} row would become its newest row and "
                "void every later carry from it"
            )


def parser():
    top = argparse.ArgumentParser(prog="ledger-row.py", description=__doc__.splitlines()[0])
    top.add_argument("store", help="the program store directory holding ledger.tsv")
    top.add_argument(
        "--lock-wait",
        type=float,
        default=LOCK_WAIT,
        metavar="SECONDS",
        help=f"seconds to wait for the lock on ledger.tsv before refusing (default {LOCK_WAIT:g}; tests shorten it)",
    )
    kinds = top.add_subparsers(dest="kind", required=True)

    def kind(name, help_text, pr=True, head=True, unit=True):
        sub = kinds.add_parser(name, help=help_text)
        if pr:
            sub.add_argument("--pr", required=True, help="the pull request's decimal number")
        if head:
            sub.add_argument("--head", required=True, help="the head, 40 hex")
        if unit:
            sub.add_argument("--unit", required=True, help="the row's unit, U<n> or U<n><letter>")
        return sub

    def sweep_arguments(sub, task_help):
        sub.add_argument("--seat", required=True, help="the srt worker seat the sweep ran on")
        sub.add_argument("--run", required=True, help="the run number")
        sub.add_argument("--task", required=True, help=task_help)
        sub.add_argument("--findings", required=True, help="sweeps/<dir>/findings.json, a regular file under the store")

    merged = kind("merged", "the merge receipt: verdict -, verifier pr-merge.sh")
    merged.add_argument("--receipt", required=True, help="the line pr-merge.sh printed")
    merged.add_argument("--note", help="appended to the evidence after '; '")
    carried = kind("carried", "the carried head: verdict carried, verifier audit-carry.py (<note>)")
    carried.add_argument("--line", required=True, help="the line audit-carry.py printed")
    carried.add_argument("--note", required=True, help="the verifier's note in parentheses")
    carried.add_argument("--evidence-note", help="appended to the evidence after '; '")
    sweep = kind("sweep", "the security-audit skill's row: pr -, verdict sweep", pr=False)
    sweep_arguments(sweep, "the sweep's own unit, U<n>")
    sweep.add_argument("--count", required=True, help="the findings count")
    sweep.add_argument("--pr", help="the pull request swept; the pr cell stays '-'")
    daily = kind(
        "daily",
        "the daily sweep of main's head: one row of daily-sweeps.tsv, not of the ledger; its ts is --swept-at, its "
        "count is read from the findings file, and the installed skill's validators and report-schema.json "
        "(~/.agents/skills/security-audit, each copied into a private directory and the copy hashed against its "
        "assets.security-audit-skill.validators_sha256 pin of ~/.agents/agent-config.yaml) must pass over the file "
        "and the coverage ledger beside it; the row records the two validator digests",
        pr=False,
        unit=False,
    )
    sweep_arguments(
        daily,
        "the daily dispatch's task id alone, daily-<YYYY-MM-DD> with the UTC day --swept-at falls on or the day before it",
    )
    daily.add_argument(
        "--swept-at",
        required=True,
        metavar="TS",
        help=(
            "the sweep's RESULT timestamp, YYYY-MM-DDTHH:MM:SSZ in UTC, written as the row's ts; refused later than "
            f"the clock or more than {SWEPT_AT_MAX_AGE} seconds (24 hours) before it"
        ),
    )
    audit = kind("audit", "the audit verdict: the word read from the verdict file's last line")
    audit.add_argument("--verdict-file", required=True, help="verdicts/<unit>-<sha8>.md")
    audit.add_argument("--verifier", required=True, help="the verifier text, starting with pr-audit.sh")
    audit.add_argument("--class", dest="class_word", help="the finding class of an incorrect verdict, one word")
    pushed = kind("pushed", "a push: verdict pushed, verifier coordinator (<how>)")
    pushed.add_argument("--how", required=True, help="how the head was pushed")
    pushed.add_argument("--what", required=True, help="what was pushed")
    receipt = kind("receipt", "a lever's receipt: verdict -, verifier the lever name")
    receipt.add_argument("--lever", required=True, help=", ".join(RECEIPT_LEVERS))
    receipt.add_argument("--receipt", required=True, help="the line the lever printed")
    receipt.add_argument("--note", help="appended to the evidence after '; '")
    return top


def daily_absent(path):
    """True when no entry of any kind exists at `path` (`os.lstat` ENOENT alone, so a symlink or another entry at the
    name is present and left to the path rule of store_file); any other failure to look is a refusal naming it
    (standing order 21)."""
    try:
        os.lstat(path)
    except FileNotFoundError:
        return True
    except OSError as error:
        refuse(f"cannot look for the daily sweeps file {path}: {error.strerror}")
    return False


def write_daily_file(store, path, line):
    """The day's first `daily-sweeps.tsv` (U597 round 5): the header and the first row as one byte string into a
    temporary file of the store directory (`tempfile.mkstemp`, `daily-sweeps.tsv.<random>.tmp`, mode 0644 as the
    round-4 file was), one `os.write` compared with the length, `os.fsync`, the close, then `os.replace` onto the
    name, so the file appears whole or not at all. A write that fails or returns short, a fsync, a close or a replace
    that fails removes the temporary file and returns the failure text naming the file (exit 1 is the caller's); the
    store then holds no `daily-sweeps.tsv` and the rerun writes it again (round 4 wrote the header through `O_EXCL`
    first, so a short write left a malformed file no retry repaired). Returns None or the failure text."""
    data = ("\t".join(ledger.DAILY_HEADER) + "\n" + line).encode("utf-8")
    try:
        descriptor, temporary = tempfile.mkstemp(prefix=f"{ledger.DAILY_FILE}.", suffix=".tmp", dir=store)
    except OSError as error:
        return f"cannot make a temporary file in {store} for {path}: {error.strerror}"
    try:
        os.fchmod(descriptor, 0o644)
        written = os.write(descriptor, data)
        if written != len(data):
            raise OSError(errno.EIO, f"short write, {written} of {len(data)} bytes")
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.replace(temporary, path)
    except OSError as error:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        try:
            os.unlink(temporary)
            left = f"the temporary file is removed and no {ledger.DAILY_FILE} exists; the rerun writes it again"
        except OSError as unlink_error:
            left = f"the temporary file {temporary} could not be removed: {unlink_error.strerror}"
        return f"cannot write {path}: {error.strerror or error}; {left}"
    return None


def first_daily_row(args, store, path, row):
    """The day's first daily row (U597 round 5), when no entry exists at `path`: under the ledger's own lock
    (`open_ledger` on `ledger.tsv`, the lock every writer of the store takes, so two first writers serialise and the
    second finds the file and appends under the daily file's lock), the absence looked for again, the row's cells
    checked, the header plus the row parsed by the reader's grammar, then write_daily_file. Returns None when the
    file appeared meanwhile (the caller appends), else (code, text) as write_row returns it."""
    lock = open_ledger(store_file(store, "ledger.tsv", "ledger"), args.lock_wait)
    try:
        if not daily_absent(path):
            return None
        line = daily_line(row)
        try:
            ledger.parse_daily(path, "\t".join(ledger.DAILY_HEADER) + "\n" + line)
        except ledger.Malformed as error:
            refuse(f"the reader refuses the composed row: {error}")
        failure = write_daily_file(store, path, line)
    finally:
        try:
            os.close(lock)
        except OSError:
            pass
    if failure is not None:
        return 1, failure
    return 0, f"appended {row.ts_text} line 2"


def daily_line(row):
    """The daily row's line, its four cells checked for a tab or a line break first."""
    cells = (row.ts_text, row.head_sha, row.verifier, row.evidence)
    for name, value in zip(ledger.DAILY_HEADER, cells):
        cell_check(f"{name} cell", value)
    return "\t".join(cells) + "\n"


def store_file(store, relative, label):
    """The regular file `<store>/<relative>` by the one path rule every read under the store follows (round 2 finding
    2): `store` is already its own realpath; each component below it is `os.lstat`ed and none is a link (a symlinked
    parent directory out of the store is named by its component); the end is a regular file; and the file's realpath
    lies under the store. Any other outcome is a refusal naming the path."""
    current = store
    for part in relative.split("/"):
        current = os.path.join(current, part)
        try:
            status = os.lstat(current)
        except OSError as error:
            refuse(f"the {label} {current} is not a regular file under the store: {error.strerror}")
        if stat.S_ISLNK(status.st_mode):
            refuse(
                f"the {label}'s component {current} is a symbolic link; a file under the store is read through real "
                "directories alone"
            )
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the {label} {current} is not a regular file under the store")
    if not os.path.realpath(current).startswith(store + os.sep):
        refuse(f"the {label} {current} resolves outside the store {store}")
    return current


def argument_rule(argv):
    """The one rule every element of argv passes before argparse runs (round 3 finding 2, round 4 finding 4): the
    element round-trips through strict UTF-8 (Python decodes argv with surrogateescape, so a byte that is not UTF-8
    arrives as a lone surrogate that would fail only at the write) and holds neither a tab, a newline, a carriage
    return nor any other control character (round 7; a check of the parsed strings alone let `--lock-wait`, which
    argparse converts to a float, escape it). The
    refusal names the element's position and the option before it, or the store and the kind for the first two
    positional elements."""
    positional = 0
    for index, value in enumerate(argv):
        if value.startswith("--"):
            where = f"argument {index + 1} (the option {value.split('=', 1)[0]!r})"
        elif index and argv[index - 1].startswith("--"):
            where = f"argument {index + 1} (the value of {argv[index - 1]})"
        else:
            positional += 1
            where = f"argument {index + 1}" + {1: " (the store)", 2: " (the kind)"}.get(positional, "")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as error:
            refuse(f"{where} holds a byte that is not UTF-8 at offset {error.start}: {value!r}")
        label = control_label(value)
        if label is not None:
            refuse(f"{where} holds {label}; a cell holds neither a tab, a newline nor a control character")


def open_ledger(ledger_path, wait):
    """The ledger's own descriptor, `O_RDWR | O_APPEND | O_NOFOLLOW`, locked `LOCK_EX` (round 4): the one descriptor
    the lock, the read and the write go through, released by its close. The lock is tried non-blocking every
    LOCK_POLL seconds for `wait` seconds; a lock not taken by then is a refusal naming the ledger (standing order 21).
    Advisory: `ledger.py` and `pr-merge.sh` open the file without a lock and read it during the hold."""
    try:
        descriptor = os.open(ledger_path, os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW)
    except OSError as error:
        refuse(f"cannot open the ledger {ledger_path} for the write: {error.strerror}")
    deadline = time.monotonic() + wait
    while True:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return descriptor
        except OSError as error:
            if error.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
                refuse(f"cannot lock the ledger {ledger_path}: {error.strerror}")
            if time.monotonic() >= deadline:
                refuse(
                    f"the ledger {ledger_path} is held by another writer after {wait:g} second"
                    f"{'' if wait == 1 else 's'}; the row is not written (--lock-wait sets the wait)"
                )
            time.sleep(LOCK_POLL)


def read_ledger(descriptor, ledger_path):
    """The whole text through the locked descriptor: `os.fstat` for the length n0, `os.pread` from offset 0 looped
    until n0 bytes (a file shorter than n0 under the lock is a refusal), decoded as the reader decodes it (strict
    UTF-8). Every failure is a refusal naming the ledger, exit 2: nothing has been written. Returns (n0, text)."""
    try:
        status = os.fstat(descriptor)
    except OSError as error:
        refuse(f"cannot read the ledger {ledger_path}: fstat: {error.strerror}")
    if not stat.S_ISREG(status.st_mode):
        refuse(f"the ledger {ledger_path} is not a regular file")
    length = status.st_size
    chunks = []
    offset = 0
    while offset < length:
        try:
            chunk = os.pread(descriptor, length - offset, offset)
        except OSError as error:
            refuse(f"cannot read the ledger {ledger_path}: pread at offset {offset}: {error.strerror}")
        if not chunk:
            refuse(f"the ledger {ledger_path} holds {offset} bytes, fewer than its length {length} under the lock")
        chunks.append(chunk)
        offset += len(chunk)
    try:
        return length, b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        refuse(f"{ledger_path}: not UTF-8: {error.reason}")


def append_line(descriptor, ledger_path, length, line):
    """One `os.write` of the line's bytes (O_APPEND puts it at the end), its count compared with the line's length,
    then `os.fsync`. A write that fails or returns short, or a fsync that fails, truncates the file back to `length`
    (`os.ftruncate`): the one recovery, which leaves the old text whole. Returns None, or the failure text naming the
    ledger, the error and the truncate's outcome (exit 1 is the caller's)."""
    data = line.encode("utf-8")
    try:
        # O_APPEND puts the write at the end whatever the offset, but XNU applies RLIMIT_FSIZE to an O_APPEND write at
        # the descriptor's offset, which pread leaves at 0 (Linux applies it at the end); seating the offset at the end
        # first makes a size limit cut the write on both kernels, and a cut write is recovered below.
        os.lseek(descriptor, 0, os.SEEK_END)
        written = os.write(descriptor, data)
    except OSError as error:
        return truncate_back(descriptor, ledger_path, length, f"write: {error.strerror}")
    if written != len(data):
        return truncate_back(descriptor, ledger_path, length, f"short write, {written} of {len(data)} bytes")
    try:
        os.fsync(descriptor)
    except OSError as error:
        return truncate_back(descriptor, ledger_path, length, f"fsync: {error.strerror}")
    return None


def truncate_back(descriptor, ledger_path, length, cause):
    """The recovery of a failed write and its one line: the file truncated to `length`, or the truncate's own failure
    named (`the ledger <path> may hold a partial last line: <error>`)."""
    try:
        os.ftruncate(descriptor, length)
    except OSError as error:
        return (
            f"cannot write {ledger_path}: {cause}; the ledger {ledger_path} may hold a partial last line: "
            f"{error.strerror}"
        )
    return f"cannot write {ledger_path}: {cause}; truncated back to {length} bytes"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    argument_rule(argv)
    args = parser().parse_args(argv)
    if not 0 <= args.lock_wait < math.inf:
        refuse(f"--lock-wait {args.lock_wait!r} is not a non-negative number of seconds")
    daily = args.kind == "daily"
    if not daily:
        check_unit(args.unit)
    store = os.path.realpath(args.store)
    # The record file first (standing order 21): its path by the store's file rule, its descriptor opened and locked
    # before it is read, before the row is composed and before any file of the store is read for it. The daily kind
    # composes and checks its row first, since the row reads nothing from the daily file, so a refusal makes no file;
    # the day's first row makes the file whole (first_daily_row, round 5) and a later one appends; the ledger is
    # never made.
    composed = None
    if daily:
        composed = daily_row(args, store)
        daily_path = os.path.join(store, ledger.DAILY_FILE)
        if daily_absent(daily_path):
            outcome = first_daily_row(args, store, daily_path, composed)
            if outcome is not None:
                return report(*outcome)
        record_path = store_file(store, ledger.DAILY_FILE, "daily sweeps file")
    else:
        record_path = store_file(store, "ledger.tsv", "ledger")
    descriptor = open_ledger(record_path, args.lock_wait)
    try:
        code, text = write_row(args, store, record_path, descriptor, composed)
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
            text = f"the ledger {record_path} was appended ({text}) but its close failed: {error.strerror}"
        else:
            text = f"{text}; the close failed too: {error.strerror}"
        code = 1
    return report(code, text)


def report(code, text):
    """The receipt on stdout (exit 0) or the failure as one stderr line (exit 1); returns `code`."""
    if code == 0:
        print(text)
    else:
        print(f"{LEVER}: {text}", file=sys.stderr)
    return code


def write_row(args, store, ledger_path, descriptor, composed=None):
    """The critical section, under the lock the descriptor holds: the record file read through it (the ledger, or
    `daily-sweeps.tsv` for the `daily` kind, whose row `composed` arrives checked), the row composed and checked, the
    whole re-read through the reader's grammar for that file, the one line appended. Returns (0, the stdout receipt)
    or (1, the failure text)."""
    length, text = read_ledger(descriptor, ledger_path)
    parse = ledger.parse_daily if args.kind == "daily" else ledger.parse_ledger
    try:
        read = parse(ledger_path, text)
    except ledger.Malformed as error:
        refuse(str(error))
    if args.kind == "daily":
        row = composed
        # A findings path an earlier daily row names is a finished run (round 5), and so is a (seat, run) one carries
        # (round 6: the same run's findings copied to another path): recording either again would date a new row
        # and refresh the window without a new sweep.
        for existing in read.rows:
            if existing.sweep_evidence_path == args.findings:  # lint-comparisons: allow named-text: a recorded path
                refuse(
                    f"the findings file {args.findings} is already recorded by the daily sweep row of"
                    f" {existing.ts_text} ({ledger_path}:{existing.line}); a finished run is not re-recorded to"
                    " refresh the window"
                )
            if (existing.seat, existing.run) == (args.seat, args.run):
                refuse(
                    f"run-{args.run} of the seat {args.seat} is already recorded by the daily sweep row of"
                    f" {existing.ts_text} ({ledger_path}:{existing.line}); a finished run is not re-recorded under"
                    " another findings path to refresh the window"
                )
        header = ledger.DAILY_HEADER
        cells = (row.ts_text, row.head_sha, row.verifier, row.evidence)
    else:
        if args.kind == "merged":
            row = merged_row(args)
        elif args.kind == "carried":
            row = carried_row(args)
        elif args.kind == "sweep":
            row = sweep_row(args, store)
        elif args.kind == "audit":
            row = audit_row(args, store)
        elif args.kind == "pushed":
            row = pushed_row(args)
        else:
            row = receipt_row(args)
        if args.kind in ("pushed", "receipt"):
            refuse_if_audited(read, args.kind, row)
        header = ledger.HEADER
        cells = (row.ts_text, row.unit, row.pr, row.head_sha, row.verdict, row.verifier, row.evidence)
    for name, value in zip(header, cells):
        cell_check(f"{name} cell", value)
    line = "\t".join(cells) + "\n"
    lead = "" if text == "" or text.endswith("\n") else "\n"
    try:
        whole = parse(ledger_path, text + lead + line)
    except ledger.Malformed as error:
        refuse(f"the reader refuses the composed row: {error}")
    number = whole.rows[-1].line
    failure = append_line(descriptor, ledger_path, length, lead + line)
    if failure is not None:
        return 1, failure
    return 0, f"appended {row.ts_text} line {number}"


if __name__ == "__main__":
    sys.exit(main())
