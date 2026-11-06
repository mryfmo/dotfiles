#!/usr/bin/env -S python3 -I
"""Append the dsh-superagent Router's would-accept Decisions to a decisions.tsv as rows (regime-cutover U317, the M-18
ladder's observe rung).

`intake-observe.py <orchestrator.sqlite> <decisions.tsv>` reads the Router's store read-only and appends one row per
would-accept Decision newer than the last row it wrote, then prints the count of rows appended. A would-accept
Decision is the record observe mode leaves in place of an accept (upstream docs/002-authorization.md, "Accept mode
and rules"): `src/policy.ts:57` returns `{ kind: 'ignore', audit: { ..., would_accept: true, proposal }, reason: {
code: 'observed', ... } }` for a positive assessment of an inferred candidate outside `auto`, and the Store saves the
Decision as JSON in the `value` column of the `decision` table (`src/app/store.ts:76`, `CREATE TABLE IF NOT EXISTS
decision (id TEXT PRIMARY KEY, thread TEXT NOT NULL, value TEXT NOT NULL)`; the save at `:245`). The row shape is
`ts \\t intake-observe \\t github-source would-accept: <thread label> trigger=<ids> rules=<rule ids> \\t <reason text>
\\t <decision id> \\t -`: the thread label is the Thread's `meta.label` when its Source set one, else the thread key;
the reason text is the Decision's reasons rendered as `src/core/reasons.ts` renders them (`Observe mode: would accept
({text})`); tabs and newlines inside any field become spaces.

The closing form is an allowlist: a Decision is written only when its `kind` is `ignore`, its `audit.would_accept` is
`true` and one of its reasons carries the code `observed`; every other Decision, whatever else it says, is not this
lever's to record. "Newer" is the Decision's `at` after the `at` of the Decision the last `intake-observe` row names
(the row's fifth column), and a Decision already named by a row is never written twice; when the named Decision is
no longer in the store, every would-accept Decision not yet named is written.

The database path must be a regular file that is not a symlink (a Router that keeps its store elsewhere is read
nowhere else), and it is opened read-only (`mode=ro`); the decisions.tsv path must be absent or a regular file that
is not a symlink, and the rows are appended in one write after every Decision has been read. Exit 0 with the count
on stdout; exit 2 with one line on stderr and nothing appended for usage, a refused path, a store that cannot be
read, a `value` that is not the JSON object the schema promises, or a row that cannot be appended.
"""

import datetime
import json
import os
import sqlite3
import sys
import urllib.parse

LEVER = "intake-observe"
WOULD_ACCEPT_CODE = "observed"
REASON_TEMPLATES = {
    "observed": "Observe mode: would accept ({text})",
    "directionUnsettled": (
        "Implementation intent or target direction is not established, or a product/design decision is still required"
    ),
    "noRuleMatched": "No enabled admission rule matched",
}


def refuse(message: str) -> int:
    print(f"{LEVER}: {message}", file=sys.stderr)
    return 2


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


def would_accept(decision: dict) -> bool:
    """The allowlist: an ignore Decision marked would_accept whose reasons carry the observe code (src/policy.ts:57)."""
    if decision.get("kind") != "ignore":
        return False
    audit = decision.get("audit")
    if not isinstance(audit, dict) or audit.get("would_accept") is not True:
        return False
    reasons = decision.get("reason")
    items = reasons if isinstance(reasons, list) else [reasons]
    return any(isinstance(reason, dict) and reason.get("code") == WOULD_ACCEPT_CODE for reason in items)


def written_rows(path: str) -> list[list[str]]:
    """The `intake-observe` rows already in the table, each as its fields."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as handle:
        return [line.rstrip("\n").split("\t") for line in handle if line.split("\t")[1:2] == [LEVER]]


def read_decisions(database: str) -> tuple[dict[str, dict], dict[str, dict]]:
    """Every Decision by id and every Thread by key, read from the store read-only."""
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
        return decisions, threads
    finally:
        connection.close()


def thread_label(decision: dict, threads: dict[str, dict]) -> str:
    key = str(decision.get("threadKey", ""))
    thread = threads.get(key, {})
    meta = thread.get("meta") if isinstance(thread.get("meta"), dict) else {}
    label = meta.get("label")
    return str(label) if isinstance(label, str) and label else key


def new_rows(decisions: dict[str, dict], threads: dict[str, dict], written: list[list[str]], now: str) -> list[str]:
    named = {row[4] for row in written if len(row) > 4}
    since = ""
    if written:
        last = written[-1][4] if len(written[-1]) > 4 else ""
        since = str(decisions.get(last, {}).get("at", ""))
    rows = []
    for decision_id, decision in decisions.items():
        if decision_id in named or not would_accept(decision):
            continue
        if since and str(decision.get("at", "")) <= since:
            continue
        triggers = decision.get("triggerIds") if isinstance(decision.get("triggerIds"), list) else []
        audit = decision["audit"]
        matches = audit.get("matches") if isinstance(audit.get("matches"), list) else []
        rules = [str(match.get("rule_id")) for match in matches if isinstance(match, dict) and match.get("rule_id")]
        rows.append(
            "\t".join(
                [
                    now,
                    LEVER,
                    flat(
                        f"github-source would-accept: {thread_label(decision, threads)} "
                        f"trigger={','.join(str(item) for item in triggers)} rules={','.join(rules)}"
                    ),
                    flat(reason_text(decision.get("reason"))),
                    flat(decision_id),
                    "-",
                ]
            )
        )
    return rows


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        return refuse("usage: intake-observe.py <orchestrator.sqlite> <decisions.tsv>")
    database, table = argv[1], argv[2]
    for path, what, allow_absent in ((database, "the store", False), (table, "the decisions table", True)):
        reason = regular_file(path, what, allow_absent=allow_absent)
        if reason:
            return refuse(reason)
    try:
        decisions, threads = read_decisions(database)
    except (sqlite3.Error, ValueError, json.JSONDecodeError) as error:
        return refuse(f"the store {database} could not be read: {error}")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = new_rows(decisions, threads, written_rows(table), now)
    if rows:
        try:
            with open(table, "a", encoding="utf-8", newline="") as handle:
                handle.write("".join(row + "\n" for row in rows))
        except OSError as error:
            return refuse(f"the decisions table {table} could not be appended: {error}")
    print(len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
