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

`ledger-row.py <store> <kind> ...`, one subcommand per kind; `ts` is now in UTC under the reader's `TS_FORMAT`:
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
  `assets.security-audit-skill.pin` (`~/.agents/agent-config.yaml` when it exists, else the checkout's
  `home/dot_agents/agent-config.yaml` two levels above this file, read as text by `pr-merge.sh`'s `sweep_pin_probe`
  reads it: no PyYAML under `-S`), evidence `<findings>; pr <pr or none>; <count> findings; validate-findings.cjs PASS;
  validate-coverage-ledger.cjs PASS`; the findings path must be a regular file under the store.
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

Two refusals cross rows, before any write (standing order 21): a `pushed` or `receipt` row whose head is 40 hex while
`ledger.already_audited` names an audit row of the same pull request at that head is refused naming that row's ts (the
`merged` kind is exempt: the merge is the last row of a head); and any cell holding a tab, a newline or a carriage
return is refused naming the cell, the store argument included. A store whose ledger does not parse is exit 2 naming
the line. Exit 0 prints one line, `appended <ts> line <n>`; every refusal is exit 2 with one stderr line; a write that
fails is exit 1 naming the file. Round 2 (U222b, verdicts/U222-9187830e.md): every file read under the store
(`ledger.tsv`, the verdict file, the findings file) follows one path rule, its `os.path.realpath` under the realpath of
the store, each component `os.lstat`ed and no link, a regular file at the end; the findings directory name is
`[A-Za-z0-9._-]` alone (the sweep reader splits the evidence on `;`); the deployed manifest is opened, ENOENT alone
falling through to the checkout's and any other failure a refusal naming the file; the carried separator class is the
gate's literal set under `re.ASCII`; and the import of `ledger.py` writes no bytecode (`sys.dont_write_bytecode`).
Round 3 (U222c, verdicts/U222-0fc41a81.md): the read, the check and the write run under one exclusive lock, so two
levers writing at once never lose each other's row, and every argument round-trips through strict UTF-8 before
anything is read (Python decodes argv with surrogateescape). Round 4 (U222d, verdicts/U222-238f0f55.md): the lever
makes no file but the ledger (rounds 2 and 3 each wrote a helper file in the store, a temporary and a lock file, and
the store's own walks refuse a name beginning with `.`). One descriptor, `os.open(ledger, O_RDWR | O_APPEND)`,
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
import importlib.util
import math
import os
import re
import stat
import sys
import time
from datetime import datetime, timezone

# `python3 -I -S` still writes `__pycache__` beside an imported module: `ledger.tsv` is the one file this lever writes.
sys.dont_write_bytecode = True

LEVER = "ledger-row"
HERE = os.path.dirname(os.path.realpath(__file__))

# The write's lock (round 4) is `LOCK_EX` on the ledger's own descriptor, tried non-blocking every LOCK_POLL seconds
# for LOCK_WAIT seconds (`--lock-wait` sets the wait); advisory, so the readers, which take no lock, are unaffected.
LOCK_WAIT = 30.0
LOCK_POLL = 0.1
# The three characters no cell and no argument holds: the ledger is tab-separated lines.
CONTROL = (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return"))


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
# The manifest, read as text by one indentation rule (pr-merge.sh `sweep_pin_probe`, brief-check.py `manifest_levers`):
# a bare `<key>:` line opens a mapping, a line indented no deeper closes it, and the pin is the one `pin: <40 hex>`
# line at the indentation of the `security-audit-skill` asset's first field under the top-level `assets:`.
MAPPING_KEY = re.compile(r"^(\S+):$")
PIN_LINE = re.compile(r"^pin: ([0-9a-f]{40})$")
ASSET_KEYS = ["assets", "security-audit-skill"]


def manifest_lines():
    """The deployed manifest `~/.agents/agent-config.yaml` as (path, lines), else the checkout's
    `home/dot_agents/agent-config.yaml` two levels above this file. Each is opened, never stat-ed first: ENOENT on the
    deployed one alone falls through to the checkout's; any other failure to open or read is a refusal naming the file
    (standing order 21; round 2 finding 4)."""
    home = os.environ.get("HOME", "")
    checkout = os.path.normpath(os.path.join(HERE, "../../home/dot_agents/agent-config.yaml"))
    manifests = [os.path.join(home, ".agents/agent-config.yaml"), checkout] if home else [checkout]
    for manifest in manifests:
        try:
            with open(manifest, encoding="utf-8") as handle:
                return manifest, handle.read().splitlines()
        except FileNotFoundError as error:
            if manifest != checkout:
                continue
            refuse(f"cannot read the manifest {manifest}: {error.strerror}")
        except OSError as error:
            refuse(f"cannot read the manifest {manifest}: {error.strerror}")
        except UnicodeDecodeError as error:
            refuse(f"cannot read the manifest {manifest}: not UTF-8: {error.reason}")


def manifest_pin(manifest, lines):
    """The one `assets.security-audit-skill.pin` of the manifest's lines, 40 hex, or a refusal naming the file."""
    keys = []  # the open mapping keys as (indentation, key), outermost first
    asset = None  # the indentation of the `security-audit-skill:` key while its block is open
    fields = None  # the indentation of the asset's fields, fixed by the first
    pins = []
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
                    match = PIN_LINE.match(text)
                    if match:
                        pins.append(match.group(1))
                continue
            asset = None
            fields = None
        while keys and indent <= keys[-1][0]:
            keys.pop()
        match = MAPPING_KEY.match(text)
        if match and (keys or indent == 0):
            keys.append((indent, match.group(1)))
            if [key for _, key in keys] == ASSET_KEYS:
                asset = indent
    if len(pins) != 1:
        refuse(
            f"{manifest} holds {len(pins)} assets.security-audit-skill.pin lines of 40 hex, not one; the sweep "
            "verifier's pin word is read from it"
        )
    return pins[0]


def cell_check(name, value):
    """A cell holds neither a tab nor a line break: the ledger is tab-separated lines."""
    for character, label in CONTROL:
        if character in value:
            refuse(f"the {name} holds {label}; a cell holds neither a tab nor a newline")


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
    if not DIGITS.match(args.run):
        refuse(f"the run {args.run!r} is not a decimal number")
    if not DIGITS.match(args.count):
        refuse(f"the count {args.count!r} is not a decimal number")
    if not UNIT.match(args.task):
        refuse(f"the task unit {args.task!r} is not U<n> or U<n><letter>")
    if not SWEEP_SEAT.match(args.seat):
        refuse(f"the seat {args.seat!r} is not one word")
    if args.pr is not None:
        check_pr(args.pr)
    match = SWEEP_FINDINGS.match(args.findings)
    if match is None or match.group(1) in (".", ".."):
        refuse(
            f"the findings path {args.findings!r} is not sweeps/<dir>/findings.json under the store with <dir> of "
            "[A-Za-z0-9._-] alone (the sweep reader splits the evidence on ';')"
        )
    store_file(store, args.findings, "findings path")
    pin = manifest_pin(*manifest_lines())[:8]
    verifier = (
        f"security-audit-skill {pin} (full audit mode on the srt worker seat {args.seat}, run-{args.run}; "
        f"TASK {args.task})"
    )
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

    def kind(name, help_text, pr=True, head=True):
        sub = kinds.add_parser(name, help=help_text)
        if pr:
            sub.add_argument("--pr", required=True, help="the pull request's decimal number")
        if head:
            sub.add_argument("--head", required=True, help="the head, 40 hex")
        sub.add_argument("--unit", required=True, help="the row's unit, U<n> or U<n><letter>")
        return sub

    merged = kind("merged", "the merge receipt: verdict -, verifier pr-merge.sh")
    merged.add_argument("--receipt", required=True, help="the line pr-merge.sh printed")
    merged.add_argument("--note", help="appended to the evidence after '; '")
    carried = kind("carried", "the carried head: verdict carried, verifier audit-carry.py (<note>)")
    carried.add_argument("--line", required=True, help="the line audit-carry.py printed")
    carried.add_argument("--note", required=True, help="the verifier's note in parentheses")
    carried.add_argument("--evidence-note", help="appended to the evidence after '; '")
    sweep = kind("sweep", "the security-audit skill's row: pr -, verdict sweep", pr=False)
    sweep.add_argument("--seat", required=True, help="the srt worker seat the sweep ran on")
    sweep.add_argument("--run", required=True, help="the run number")
    sweep.add_argument("--task", required=True, help="the sweep's own unit, U<n>")
    sweep.add_argument("--findings", required=True, help="sweeps/<dir>/findings.json, a regular file under the store")
    sweep.add_argument("--count", required=True, help="the findings count")
    sweep.add_argument("--pr", help="the pull request swept; the pr cell stays '-'")
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
    arrives as a lone surrogate that would fail only at the write) and holds neither a tab, a newline nor a carriage
    return (a check of the parsed strings alone let `--lock-wait`, which argparse converts to a float, escape it). The
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
        for character, label in CONTROL:
            if character in value:
                refuse(f"{where} holds {label}; a cell holds neither a tab nor a newline")


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
    check_unit(args.unit)
    store = os.path.realpath(args.store)
    # The ledger first (standing order 21): its path by the store's file rule, its descriptor opened and locked
    # before it is read, before the row is composed and before any file of the store is read for it.
    ledger_path = store_file(store, "ledger.tsv", "ledger")
    descriptor = open_ledger(ledger_path, args.lock_wait)
    try:
        code, text = write_row(args, store, ledger_path, descriptor)
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
            text = f"the ledger {ledger_path} was appended ({text}) but its close failed: {error.strerror}"
        else:
            text = f"{text}; the close failed too: {error.strerror}"
        code = 1
    if code == 0:
        print(text)
    else:
        print(f"{LEVER}: {text}", file=sys.stderr)
    return code


def write_row(args, store, ledger_path, descriptor):
    """The critical section, under the lock the descriptor holds: the ledger read through it, the row composed and
    checked, the whole re-read, the one line appended. Returns (0, the stdout receipt) or (1, the failure text)."""
    length, text = read_ledger(descriptor, ledger_path)
    try:
        read = ledger.parse_ledger(ledger_path, text)
    except ledger.Malformed as error:
        refuse(str(error))
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
    cells = (row.ts_text, row.unit, row.pr, row.head_sha, row.verdict, row.verifier, row.evidence)
    for name, value in zip(ledger.HEADER, cells):
        cell_check(f"{name} cell", value)
    line = "\t".join(cells) + "\n"
    lead = "" if text == "" or text.endswith("\n") else "\n"
    try:
        whole = ledger.parse_ledger(ledger_path, text + lead + line)
    except ledger.Malformed as error:
        refuse(f"the reader refuses the composed row: {error}")
    number = whole.rows[-1].line
    failure = append_line(descriptor, ledger_path, length, lead + line)
    if failure is not None:
        return 1, failure
    return 0, f"appended {row.ts_text} line {number}"


if __name__ == "__main__":
    sys.exit(main())
