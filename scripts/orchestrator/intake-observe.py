#!/usr/bin/env -S python3 -I
"""Append the dsh-superagent Router's ladder Decisions to a decisions.tsv as rows (regime-cutover U317, the M-18
ladder's observe rung; U465, the accept rung and the refusals, table rows i6 and i7).

`intake-observe.py [--kind would-accept|accept|refusal|all] <orchestrator.sqlite> <decisions.tsv>` reads the Router's
store read-only and appends one row per ladder Decision newer than the last row it wrote, then prints a count: the
would-accept rows appended by default (the count rows i2 and i6 read), else the rows of the kind the one flag names,
or every row with `all`. The rows appended are the same whatever the flag. The Decision kinds, each an allowlist of
its own and nothing else a row:

- would-accept: the record observe mode leaves in place of an accept (upstream docs/002-authorization.md, "Accept
  mode and rules"): `src/policy.ts:57` returns `{ kind: 'ignore', audit: { ..., would_accept: true, proposal },
  reason: { code: 'observed', ... } }` for a positive assessment of an inferred candidate outside `auto`. The row is
  `ts \\t intake-observe \\t <source>-source would-accept: <thread label> trigger=<ids> rules=<rule ids> \\t <reason
  text> \\t <decision id> \\t -`. A Decision is this kind when its `kind` is `ignore`, its `audit.would_accept` is
  `true` and one of its reasons carries the code `observed`.
- accept: `kind: 'accept'` (`src/policy.ts:59`, recorded by `src/core/evals.ts:313` with the reason, the rule ids
  the matches named, the audit and the ticket it started). The row is `<source>-source accept: <thread label>
  trigger=<ids> rules=<rule ids>[ ticket=<ticket id>] \\t <reason text> \\t <decision id> \\t -`; the rule ids are the
  Decision's `rules`, else the `rule_id`s of `audit.matches`.
- refusal: an ignore Decision whose reasons carry a gate refusal code with the refused trigger's id
  (`src/core/evals.ts:97-103`, one Decision per batch, one reason per refused trigger): `not_a_member` (the sender is
  not on the Source's allowed list, `src/policy.ts:210`) or `not_human` (a bot, CI or the agent itself,
  `src/policy.ts:173-175`). One row per such reason: `<source>-source refusal <code>: <thread label> login=<login>
  \\t <reason text> \\t <decision id> \\t -`, the login the `actor.id` of the trigger row the reason names (the
  `trigger` table, `src/app/store.ts:72`; `unknown` when that row is gone). The gate's other codes
  (`admission_ignored`, `no_mention`) and every other ignore (`noRuleMatched`, `directionUnsettled`, a stop, a
  policy change) are not rows.

`<source>` is the Decision's own Source, read from its `threadKey` (`<source>:<id>`, `src/core/model.ts`: `github:12`,
`discord:guild/42`), so a Decision of another Source is recorded under its own word and never as GitHub's (U465d,
verdict U465-e6a9a84f P2 `:240`); a key without the `<source>:` prefix is recorded as `unknown`, never guessed.
The Store saves a Decision as JSON in the `value` column of the `decision` table (`src/app/store.ts:76`, `CREATE
TABLE IF NOT EXISTS decision (id TEXT PRIMARY KEY, thread TEXT NOT NULL, value TEXT NOT NULL)`; the save at `:245`).
The thread label is the Thread's `meta.label` when its Source set one, else the thread key; the reason text is the
Decision's reasons rendered as `src/core/reasons.ts` renders them (`Observe mode: would accept ({text})`, `{text}` for
`said`, the bare code with its `<trigger id>: ` prefix for a code without a template); tabs and newlines inside any
field become spaces.

"Newer" is the Decision's `at` after the `at` of the Decision the last `intake-observe` row names (the row's fifth
column), and a Decision already named by a row is never written twice; when the named Decision is no longer in the
store, every ladder Decision not yet named is written. The three kinds share the one cursor, so a table the observe
rung alone wrote carries on from its last row.

The database path must be a regular file that is not a symlink (a Router that keeps its store elsewhere is read
nowhere else), and it is opened read-only (`mode=ro`); the decisions.tsv path must be absent or a regular file that
is not a symlink, and the rows are appended in one write after every Decision has been read. A table this lever
creates starts with the store's header, `ts\\tphase\\tdecision\\twhy\\tevidence\\tresult`, the one `rounds-check.py`
reads (round 2: a created table without it was rejected there). Exit 0 with the count on stdout; exit 2 with one
line on stderr and nothing appended for usage (a kind outside the four included), a refused path, a store that
cannot be read (a store without the `trigger` table included), a `value` that is not the JSON object the schema
promises, a table that cannot be read (round 2: that read escaped the refusal handler as a traceback), or a row that
cannot be appended.

Before anything else the file hashes itself against its `claude.levers.sha256.intake-observe.py` pin in the
manifest beside it (the deployed `~/.agents/agent-config.yaml` for the copy under the physical `~/.local/bin/common`,
else the checkout's `home/dot_agents/agent-config.yaml` two levels up) and refuses to run (exit 2, nothing on
stdout) when the digest differs, in the form `brief-check.py` uses (round 2: an altered installed copy appended a
row); `python3 -I` ignores the script directory and the PYTHON* variables, so no planted module answers first.
"""

import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys
import urllib.parse

LEVER = "intake-observe"
LEVER_SCRIPT = "intake-observe.py"
USAGE = "usage: intake-observe.py [--kind would-accept|accept|refusal|all] <orchestrator.sqlite> <decisions.tsv>"
WOULD_ACCEPT_CODE = "observed"
# The gate's refusal codes this lever records (src/policy.ts:173, :175, :210; U465, table row i7): the sender is not
# on the Source's allowed list, or is no human (a bot, CI, the agent itself). The gate's other two codes
# (admission_ignored, no_mention) and every other ignore are not rows: the allowlist is these two words.
REFUSAL_CODES = ("not_a_member", "not_human")
# The Source word of a Decision's threadKey (`<source>:<id>`), the grammar of an upstream Source id (U465d); a key
# outside it is recorded under `unknown`.
SOURCE_WORD = re.compile(r"[a-z0-9][a-z0-9_-]*")
WOULD_ACCEPT, ACCEPT, REFUSAL, ALL = "would-accept", "accept", "refusal", "all"
KINDS = (WOULD_ACCEPT, ACCEPT, REFUSAL, ALL)
# rounds-check.py DECISIONS_HEADER, joined by tabs: the first line of a table this lever creates.
DECISIONS_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult"
# The levers block of the manifest, read as text by indentation alone, never parsed as YAML (brief-check.py's reader):
# a mapping key is a bare `<key>:` line; a pin is `<name>: <64 hex>` at the one indentation the first pin fixes.
MAPPING_KEY = re.compile(r"^(\S+):$")
LEVER_PIN = re.compile(r"^(\S+): ([0-9a-f]{64})$")
LEVERS_KEYS = ("claude", "levers", "sha256")
# src/core/reasons.ts REASONS, the templates of the codes a ladder row can carry; a code outside them renders as itself.
REASON_TEMPLATES = {
    "said": "{text}",
    "observed": "Observe mode: would accept ({text})",
    "directionUnsettled": (
        "Implementation intent or target direction is not established, or a product/design decision is still required"
    ),
    "noRuleMatched": "No enabled admission rule matched",
    "senderNotMember": "The sender is not on the Source's list",
}


def refuse(message: str) -> int:
    print(f"{LEVER}: {message}", file=sys.stderr)
    return 2


def refuse_to_run(reason: str) -> None:
    """The self-check's refusal, in the shell levers' words on stderr: exit 2 and nothing was read or written."""
    print(f"{LEVER_SCRIPT}: refused: {reason}", file=sys.stderr)
    sys.exit(2)


def lever_self_check() -> None:
    """Refuse to run unless this file's sha256 equals its pin in the manifest beside it (regime-cutover U31; U317b).

    The physical directory of this file decides the manifest: the deployed `~/.agents/agent-config.yaml` when the
    directory is the physical `~/.local/bin/common`, else the checkout's `home/dot_agents/agent-config.yaml` two
    levels up; an unset or unresolvable HOME means the checkout manifest. The pin is the block's `intake-observe.py`
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
        refuse_to_run(f"manifest unreadable: {manifest}")
    try:
        with open(manifest, "rb") as handle:
            lines = handle.read().decode("utf-8", "replace").splitlines()
    except OSError:
        refuse_to_run(f"cannot read {manifest}")
    pins = [digest for name, digest in manifest_levers(lines, manifest) if name == LEVER_SCRIPT]
    if len(pins) != 1:
        refuse_to_run(f"no single sha256 pin for {LEVER_SCRIPT} in {manifest}")
    try:
        with open(self_path, "rb") as handle:
            digest = hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        refuse_to_run(f"cannot hash {self_path}")
    if digest != pins[0]:
        refuse_to_run(f"sha256 {digest} of {self_path} differs from the pin in {manifest}")


def manifest_levers(lines: list[str], manifest: str) -> tuple[tuple[str, str], ...]:
    """The `(name, sha256)` pins under the manifest's `claude.levers.sha256` mapping, in file order (brief-check.py,
    U136): the mapping keys are walked by indentation, so `levers:` counts only under the top-level `claude:` and
    `sha256:` only under that `levers:`; inside the block, blank and comment lines are skipped, the entries share the
    indentation of the first pin, and the list ends at the first line indented less. An entry that is not
    `<name>: <64 hex>` is a refusal naming the line; no entry at all is the missing-block refusal."""
    pins: list[tuple[str, str]] = []
    keys: list[tuple[int, str]] = []  # the open mapping keys as (indentation, key), outermost first
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
                refuse_to_run(f"line {number} of {manifest} is not a `<name>: <sha256>` pin under claude.levers.sha256")
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
        refuse_to_run(f"no claude.levers.sha256 block in {manifest}")
    return tuple(pins)


def regular_file(path: str, what: str, *, allow_absent: bool) -> str | None:
    """None when `path` is a regular file that is not a symlink (or absent, when allowed); else the refusal text."""
    if os.path.islink(path):
        return f"{what} {path} is a symlink; the lever reads and writes only a regular file there"
    if not os.path.lexists(path):
        return None if allow_absent else f"{what} {path} does not exist"
    if not os.path.isfile(path):
        return f"{what} {path} is not a regular file"
    return None


def flat(text: object) -> str:
    """One TSV field: a string with every tab, carriage return and newline replaced by a space."""
    return str(text).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def reason_text(reasons: object) -> str:
    """The Decision's reasons as `reasonText` of src/core/reasons.ts renders them, joined by `; `."""
    items = reasons if isinstance(reasons, list) else [reasons] if reasons else []
    parts = []
    for reason in items:
        if not isinstance(reason, dict):
            continue
        code = str(reason.get("code", ""))
        values = reason.get("values") if isinstance(reason.get("values"), dict) else {}
        text = REASON_TEMPLATES.get(code, code)
        for name, value in values.items():
            text = text.replace("{" + str(name) + "}", str(value))
        trigger = reason.get("triggerId")
        parts.append(f"{trigger}: {text}" if trigger else text)
    return "; ".join(parts)


def reasons_of(decision: dict) -> list[dict]:
    """The Decision's reasons as a list of the dict reasons it carries (`reason` is one Reason or a list of them)."""
    reasons = decision.get("reason")
    items = reasons if isinstance(reasons, list) else [reasons]
    return [reason for reason in items if isinstance(reason, dict)]


def would_accept(decision: dict) -> bool:
    """The allowlist: an ignore Decision marked would_accept whose reasons carry the observe code (src/policy.ts:57)."""
    if decision.get("kind") != "ignore":
        return False
    audit = decision.get("audit")
    if not isinstance(audit, dict) or audit.get("would_accept") is not True:
        return False
    return any(reason.get("code") == WOULD_ACCEPT_CODE for reason in reasons_of(decision))


def refusals(decision: dict) -> list[dict]:
    """The gate refusals among an ignore Decision's reasons (src/core/evals.ts:97: `{code, triggerId}` per refused
    trigger), those whose code is one of REFUSAL_CODES; empty for every other Decision."""
    if decision.get("kind") != "ignore":
        return []
    return [reason for reason in reasons_of(decision) if reason.get("code") in REFUSAL_CODES]


def row_kind(decision: dict) -> str | None:
    """The ladder row a Decision is: `accept` by its kind (src/core/evals.ts:313), `would-accept` by the observe
    allowlist, `refusal` by a gate refusal code among its reasons; None for every other Decision."""
    if decision.get("kind") == "accept":
        return ACCEPT
    if would_accept(decision):
        return WOULD_ACCEPT
    if refusals(decision):
        return REFUSAL
    return None


def written_rows(path: str) -> list[list[str]]:
    """The `intake-observe` rows already in the table, each as its fields."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as handle:
        return [line.rstrip("\n").split("\t") for line in handle if line.split("\t")[1:2] == [LEVER]]


def read_decisions(database: str) -> tuple[dict[str, dict], dict[str, dict], dict[str, str]]:
    """Every Decision by id, every Thread by key and every trigger's actor id (the sender's login) by trigger id, read
    from the store read-only."""
    uri = "file:" + urllib.parse.quote(os.path.abspath(database)) + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    try:
        decisions: dict[str, dict] = {}
        for row_id, value in connection.execute("SELECT id, value FROM decision ORDER BY rowid"):
            decision = json.loads(value)
            if not isinstance(decision, dict):
                raise ValueError(f"decision {row_id} holds no JSON object in its value column")
            decisions[str(row_id)] = decision
        threads: dict[str, dict] = {}
        for key, value in connection.execute("SELECT key, value FROM thread"):
            thread = json.loads(value)
            if isinstance(thread, dict):
                threads[str(key)] = thread
        logins: dict[str, str] = {}
        for trigger_id, value in connection.execute("SELECT id, value FROM trigger"):
            trigger = json.loads(value)
            actor = trigger.get("actor") if isinstance(trigger, dict) and isinstance(trigger.get("actor"), dict) else {}
            if isinstance(actor.get("id"), str) and actor["id"]:
                logins[str(trigger_id)] = actor["id"]
        return decisions, threads, logins
    finally:
        connection.close()


def source_word(decision: dict) -> str:
    """The Source a Decision belongs to, read from its `threadKey` (`<source>:<id>`, src/core/model.ts: `github:12`,
    `discord:guild/42`; U465d, verdict U465-e6a9a84f P2 `:240`: every row said github-source, so another Source's
    accept was recorded as GitHub's): the word before the first colon when it is `[a-z0-9][a-z0-9_-]*`, else
    `unknown`, never a guess."""
    word, separator, _ = str(decision.get("threadKey", "")).partition(":")
    return word if separator and SOURCE_WORD.fullmatch(word) else "unknown"


def thread_label(decision: dict, threads: dict[str, dict]) -> str:
    key = str(decision.get("threadKey", ""))
    thread = threads.get(key, {})
    meta = thread.get("meta") if isinstance(thread.get("meta"), dict) else {}
    label = meta.get("label")
    return str(label) if isinstance(label, str) and label else key


def ladder_rows(
    decision_id: str, decision: dict, threads: dict[str, dict], logins: dict[str, str], now: str
) -> list[tuple[str, str]]:
    """The (kind, row) pairs one Decision yields: one row for a would-accept or an accept, one per gate refusal among
    a refusal Decision's reasons, none for any other Decision."""
    kind = row_kind(decision)
    if kind is None:
        return []
    label = thread_label(decision, threads)
    source = source_word(decision)

    def row(text: str, why: str) -> str:
        return "\t".join([now, LEVER, flat(text), flat(why), flat(decision_id), "-"])

    if kind == REFUSAL:
        return [
            (
                REFUSAL,
                row(
                    f"{source}-source refusal {reason['code']}: {label} "
                    f"login={logins.get(str(reason.get('triggerId', '')), 'unknown')}",
                    reason_text(reason),
                ),
            )
            for reason in refusals(decision)
        ]
    triggers = decision.get("triggerIds") if isinstance(decision.get("triggerIds"), list) else []
    audit = decision.get("audit") if isinstance(decision.get("audit"), dict) else {}
    matches = audit.get("matches") if isinstance(audit.get("matches"), list) else []
    rules = (
        [str(rule) for rule in decision["rules"]]
        if isinstance(decision.get("rules"), list)
        else [str(match.get("rule_id")) for match in matches if isinstance(match, dict) and match.get("rule_id")]
    )
    text = f"{source}-source {kind}: {label} trigger={','.join(str(item) for item in triggers)} rules={','.join(rules)}"
    if kind == ACCEPT and decision.get("ticketId"):
        text += f" ticket={decision['ticketId']}"
    return [(kind, row(text, reason_text(decision.get("reason"))))]


def new_rows(
    decisions: dict[str, dict], threads: dict[str, dict], logins: dict[str, str], written: list[list[str]], now: str
) -> list[tuple[str, str]]:
    """The (kind, row) pairs of every ladder Decision newer than the last row's and not yet named by a row."""
    named = {row[4] for row in written if len(row) > 4}
    since = ""
    if written:
        last = written[-1][4] if len(written[-1]) > 4 else ""
        since = str(decisions.get(last, {}).get("at", ""))
    rows: list[tuple[str, str]] = []
    for decision_id, decision in decisions.items():
        if decision_id in named:
            continue
        if since and str(decision.get("at", "")) <= since:
            continue
        rows.extend(ladder_rows(decision_id, decision, threads, logins, now))
    return rows


def parse_argv(argv: list[str]) -> tuple[str, str, str] | None:
    """The kind counted, the store path and the table path; None for anything else (the usage refusal)."""
    kind, rest = WOULD_ACCEPT, argv[1:]
    if rest and rest[0].startswith("--kind"):
        if rest[0] == "--kind":
            if len(rest) < 2:
                return None
            kind, rest = rest[1], rest[2:]
        elif rest[0].startswith("--kind="):
            kind, rest = rest[0][len("--kind=") :], rest[1:]
        else:
            return None
    if kind not in KINDS or len(rest) != 2:
        return None
    return kind, rest[0], rest[1]


def main(argv: list[str]) -> int:
    parsed = parse_argv(argv)
    if parsed is None:
        return refuse(USAGE)
    counted, database, table = parsed
    for path, what, allow_absent in ((database, "the store", False), (table, "the decisions table", True)):
        reason = regular_file(path, what, allow_absent=allow_absent)
        if reason:
            return refuse(reason)
    try:
        decisions, threads, logins = read_decisions(database)
    except (sqlite3.Error, ValueError, json.JSONDecodeError) as error:
        return refuse(f"the store {database} could not be read: {error}")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        written = written_rows(table)
    except (OSError, UnicodeDecodeError) as error:
        return refuse(f"the decisions table {table} could not be read: {error}")
    rows = new_rows(decisions, threads, logins, written, now)
    if rows:
        header = "" if os.path.lexists(table) else DECISIONS_HEADER + "\n"
        try:
            with open(table, "a", encoding="utf-8", newline="") as handle:
                handle.write(header + "".join(row + "\n" for _, row in rows))
        except OSError as error:
            return refuse(f"the decisions table {table} could not be appended: {error}")
    print(sum(1 for kind, _ in rows if counted == ALL or kind == counted))
    return 0


if __name__ == "__main__":
    lever_self_check()
    sys.exit(main(sys.argv))
