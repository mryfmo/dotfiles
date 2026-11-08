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
fails is exit 1 naming the file. Round 2 (U222b, verdicts/U222-9187830e.md): the write is atomic, the whole text plus
the new line written to `<store>/.ledger.tsv.<pid>.tmp`, fsynced and renamed over `ledger.tsv` by `os.replace`, the
temporary removed on any failure, so a write that fails leaves the old file whole; every file read under the store
(`ledger.tsv`, the verdict file, the findings file) follows one path rule, its `os.path.realpath` under the realpath of
the store, each component `os.lstat`ed and no link, a regular file at the end; the findings directory name is
`[A-Za-z0-9._-]` alone (the sweep reader splits the evidence on `;`); the deployed manifest is opened, ENOENT alone
falling through to the checkout's and any other failure a refusal naming the file; the carried separator class is the
gate's literal set under `re.ASCII`; and the import of `ledger.py` writes no bytecode (`sys.dont_write_bytecode`).
Installed as `~/.local/bin/common/ledger-row.py` in `brief-check.py`'s form (the generator's copy and pin); it needs
`ledger.py` beside it wherever it runs.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import stat
import sys
from datetime import datetime, timezone

# `python3 -I -S` still writes `__pycache__` beside an imported module: `ledger.tsv` is the one file this lever writes.
sys.dont_write_bytecode = True

LEVER = "ledger-row"
HERE = os.path.dirname(os.path.realpath(__file__))


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
    for character, label in (("\t", "a tab"), ("\n", "a newline"), ("\r", "a carriage return")):
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


def write_whole(store, ledger_path, text):
    """The whole text to `<store>/.ledger.tsv.<pid>.tmp`, fsynced and renamed over `ledger.tsv` by `os.replace`, the
    one atomic whole-file replace the operating system offers: a write that fails (a size limit, a full disk) leaves
    the old file whole and no temporary (round 2 finding 1). The old file's mode is kept. Returns None, or the failure
    text naming the file."""
    temporary = os.path.join(store, f".ledger.tsv.{os.getpid()}.tmp")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except OSError as error:
        return f"cannot write {ledger_path}: cannot create {temporary}: {error.strerror}"
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fchmod(handle.fileno(), stat.S_IMODE(os.stat(ledger_path).st_mode))
            os.fsync(handle.fileno())
        os.replace(temporary, ledger_path)
    except OSError as error:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        return f"cannot write {ledger_path} ({temporary} removed): {error.strerror}"
    return None


def main(argv=None):
    args = parser().parse_args(argv)
    for name, value in sorted(vars(args).items()):
        if isinstance(value, str):
            cell_check(name.replace("_", "-") if name != "class_word" else "class", value)
    check_unit(args.unit)
    store = os.path.realpath(args.store)
    # The ledger first (standing order 21): a store that does not parse is a refusal naming the line, before the
    # row is composed and before any file of the store is read for it.
    ledger_path = store_file(store, "ledger.tsv", "ledger")
    try:
        text = ledger.read_text(ledger_path)
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
    failure = write_whole(store, ledger_path, text + lead + line)
    if failure is not None:
        print(f"{LEVER}: {failure}", file=sys.stderr)
        return 1
    print(f"appended {row.ts_text} line {number}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
