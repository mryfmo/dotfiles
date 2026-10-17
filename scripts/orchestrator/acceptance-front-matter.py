"""acceptance-front-matter.py <task> <sweep-json> <pr-worktree> [--ledger <tsv>] [--audit-dispositions <tsv>]

Write or update the JSON block of `.orchestration/acceptance/<task>.md` in this checkout (plan 007 T718, a05 item 1;
plan 013 A′, C-24, C-26): the object between the record's first two `---` lines that the gate reads. `head` is
`git -C <pr-worktree> rev-parse HEAD` and must equal the sweep JSON's `head_sha`; `pr` is the sweep JSON's own `pr`.
`ledger` keeps every row the record has and adds each `--ledger` row (`id<TAB>class`) whose id is new; a row whose
id is present is printed as kept-ledger-row. `searches` is recomputed by the gate's rule: each class with three or
more rows, with the sorted basenames of the mistake records naming it. `audit_findings` come from
`--audit-dispositions` (`n<TAB>reason<TAB>evidence`), required when the audit summary orch-audit.sh writes beside
its receipt (`.orchestration/validation/<task>-audit-<sha7>.md.last.md`) ends in `Verdict: incorrect`, refused
otherwise; the record is written before the audit (the audit reads it) and again after an incorrect one. A record
that starts with a `---` block is read with the gate module's reader (duplicate keys refused) and keeps its text
after the block and its `dispatch` list; a prose record gets the block prepended. `replans`, the C-59 re-plans
(`{<class slug>: {specification, design, implementation, verification}}`, each a non-empty string), is kept as found
and written `{}` when absent; another shape exits 2 naming the key. The gate module's field checks run on the new
block, and any refusal exits 1 before anything is written.
"""

import argparse
import collections
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


def refuse(message):
    sys.exit(f"acceptance-front-matter: {message}; nothing written")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def rows(path, width):
    """The `width`-field rows of a TSV file, blank and `#` lines skipped."""
    lines = Path(path).read_text().splitlines() if path else []
    found = [line.split("\t") for line in lines if line.strip() and not line.startswith("#")]
    for fields in found:
        if len(fields) != width:
            refuse(f"{path}: a row needs {width} tab-separated fields: {fields!r}")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task")
    parser.add_argument("sweep")
    parser.add_argument("pr_worktree")
    parser.add_argument("--ledger")
    parser.add_argument("--audit-dispositions")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.task):
        parser.error(f"not a task id: {args.task!r}")
    root = Path(git("-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"))
    spec = importlib.util.spec_from_file_location("require_crit_review", root / "scripts/require-crit-review.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    try:
        sweep = json.loads(Path(args.sweep).read_text(), object_pairs_hook=gate.refuse_duplicate_keys)
    except ValueError as error:
        refuse(f"{args.sweep}: {error}")
    head = git("-C", args.pr_worktree, "rev-parse", "HEAD")
    if sweep.get("head_sha") != head:
        refuse(f"the sweep was collected for head {sweep.get('head_sha')!r}, not {args.pr_worktree}'s HEAD {head}")

    path = root / ".orchestration/acceptance" / f"{args.task}.md"
    text = path.read_text() if path.is_file() else ""
    record, rest = {}, text
    if text.split("\n")[0] == "---":
        record, error = gate.read_acceptance_record(path)
        if error:
            refuse(error)
        lines = text.split("\n")
        rest = "\n".join(lines[lines.index("---", 1) + 1 :])
    replans, parts = record.get("replans", {}), ", ".join(gate.REPLAN_KEYS)
    if not isinstance(replans, dict):
        parser.error(f"replans must be {{<class slug>: {{{parts}}}}}; nothing written")
    for cls, entry in replans.items():
        if not gate.CLASS_SLUG.fullmatch(cls) or not gate.replan_complete(entry) or set(entry) != set(gate.REPLAN_KEYS):
            parser.error(f"replans.{cls} must be {{{parts}}}, each a non-empty string; nothing written")

    ledger = list(record.get("ledger", []))
    present = {str(row.get("id")) for row in ledger if isinstance(row, dict)}
    for row_id, cls in rows(args.ledger, 2):
        if row_id in present:
            print("kept-ledger-row", row_id)
        else:
            ledger.append({"id": row_id, "class": cls})
            present.add(row_id)

    summary = root / f".orchestration/validation/{args.task}-audit-{head[:7]}.md.last.md"
    audit = summary.read_text() if summary.is_file() else ""
    # The gate's verdict rule: the summary's last non-blank line.
    last = [line for line in audit.splitlines() if line.strip()][-1:]
    verdict = (match := gate.AUDIT_VERDICT.fullmatch(last[0]) if last else None) and match.group(1)
    incorrect = verdict == "incorrect"
    if incorrect != (args.audit_dispositions is not None):
        refuse(
            f"--audit-dispositions is {'required' if incorrect else 'refused'}: {summary.name} {verdict or 'missing'}"
        )
    findings = [
        {"n": n, "reason": reason, "evidence": evidence} for n, reason, evidence in rows(args.audit_dispositions, 3)
    ]

    classes = collections.Counter(
        row["class"] for row in ledger if isinstance(row, dict) and isinstance(row.get("class"), str)
    )
    searches = []
    for cls in sorted(c for c, count in classes.items() if count >= gate.S6_CLASS_LIMIT):
        found = gate.mistake_records(root, cls)
        if isinstance(found, str):
            refuse(found)
        searches.append({"class": cls, "records": sorted(found)})

    block = {**record, "format": gate.RECORD_FORMAT, "task": args.task, "head": head, "pr": sweep.get("pr")}
    block.update(ledger=ledger, searches=searches, audit_findings=findings, replans=replans)
    errors = gate.record_field_errors(block, args.task, head, sweep.get("pr"))
    if not errors and incorrect:
        errors = gate.audit_findings_errors(block, len(gate.AUDIT_FINDING.findall(audit)))
    if errors:
        refuse("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + json.dumps(block, indent=2, sort_keys=True, ensure_ascii=False) + "\n---\n" + rest)
    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))


if __name__ == "__main__":
    main()
