---
format: 2
task_id: dotfiles-T128-audit-s1-report-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - AGENTS.md
  - scripts/orchestrator/orch-audit.sh
  - tests/fixtures/regime/audit.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T128-audit-s1-report-a01/**
after: [dotfiles-T128-rules-s1-replan-a01]
threat_table:
  - control: the PR edits AGENTS.md in one place (the Audit section's reporting bullets)
    disposition: "residual: the canonical instruction file of every runtime, a shared source: the operator approved the Codex seat for this change (D-S1-roles); the docs test pins the sentences; the orchestrator's diff review and the task-level audit compare the diff against this row"
  - control: the PR edits scripts/orchestrator/orch-audit.sh in three places (the record's JSON block extracted and validated after the ledger check and before the codex call, the prompt sentence built from it, and the prompt's per-finding format string)
    disposition: "residual: the extraction runs the wrapper's existing interpreter idiom, uv run --no-project python -I (its lines 53 and 57 today), with json on the record text and refuses a missing or malformed block with exit 2 after the ledger check (exit 3) and before any codex call; the classes are slugs validated as the gate validates them and the counts are integers, so no review text reaches the prompt as an instruction; an edit outside these three places is an undeclared change the audit fails"
  - control: the PR adds tests/fixtures/regime/audit.md as the pinned copy of the Audit section
    disposition: "residual: a new fixture (the existing code-review-orchestration fixture pins another section and stays); it changes with the section it pins in the same commit"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py only for the pinned Audit sentences
    disposition: "residual: new tests beside the existing ones, which stay"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only for the two orch-audit cases (the prompt sentence and format string; the malformed-record refusal) and for the record fixture of the one existing test_orch_audit_* test that reaches the extraction with real Python
    disposition: "residual: two new tests beside the four existing test_orch_audit_* tests, which stay with their assertions; the one existing test whose TSV-only record reaches the extraction with real Python (the isolation test) gains a valid JSON block in that fixture and nothing else (the no-fresh-receipt test writes no record and reaches only the stub uv); the tests run the real wrapper through the module's harness with a stub codex on PATH that records its argv, and with a record whose block is malformed"
  - control: in-process effects
    disposition: "residual: the test modules run the wrapper as a subprocess with a stub codex on PATH and read the rule files as text; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the wrapper runs codex, git and uv run --no-project python -I as today, from the trusted main checkout as cwd (its line 47), and the extraction reuses that idiom; a PR checkout as cwd chooses nothing new"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-audit-s1-report-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-audit-s1-report-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the Audit section of AGENTS.md on origin/main does not ask for the class count yet'
    command: 'git show origin/main:AGENTS.md | /usr/bin/grep -c "count on the record"'
    output: |-
      0
  - claim: 'the audit prompt on origin/main carries no ledger classes yet'
    command: 'git show origin/main:scripts/orchestrator/orch-audit.sh | /usr/bin/grep -c "ledger classes"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-audit-s1-report-a01 — the auditor reports the class count and a missing re-plan line (C-59; the operator's correction of 2026-10-17)

Written 2026-10-17 by the orchestrator seat. The auditor is read-only and stops nothing; its report is what the orchestrator's counters and gate consume, so each finding carries its class and its count on the record, and a class at three rows without a re-plan line is itself a finding. AGENTS.md is a shared source; the operator approved the Codex seat for it (D-S1-roles, 「進めること」).

## What to do

1. AGENTS.md, the Audit section, the "Report each finding with" list gains two items: the finding's class slug (`[a-z0-9-]`, the ledger's slug when the record has one for the same finding, else a new one) and its count on the record (the number of ledger rows of that class including this finding); and the "Cover" list gains: a ledger class other than `advisory-p2` at three or more rows without a re-plan line in the record (a body line beginning `re-plan: <class> -> ` whose text holds the four words specification, design, implementation and verification, C-59; a prefix alone is not a re-plan line) is a P2 finding of class `replan-missing`. A new fixture `tests/fixtures/regime/audit.md` pins the Audit section (the existing `code-review-orchestration.md` pins the Code Review Rules and stays); two docs tests, `test_audit_section_reports_class_and_count_per_finding` and `test_audit_section_names_a_missing_re_plan_line_as_a_finding`, each asserting the sentence in AGENTS.md and in the fixture; and the `PINNED_SECTIONS` entry `("audit", ROOT / "AGENTS.md", None, ("## Audit", "\n## "))` in test_agmsg_orchestration_docs.py (its lines 227 to 240), so `test_regime_rule_sections_are_pinned_whole` compares the fixture with the section whole.
2. `scripts/orchestrator/orch-audit.sh`: new work, since today the wrapper delegates the record check to ledger-check.py's TSV parser and extracts nothing from the JSON block: after the ledger check (its `refuse "the ledger is incomplete" 3`) and before the codex call, the wrapper extracts the record's JSON block (the text between the first two `---` lines) with its existing interpreter idiom, `uv run --no-project python -I -c` and json (lines 53 and 57 today), validates it as the gate does (a dict with a ledger list of {id, class} rows; a slug of `[a-z0-9-]`), and adds one prompt sentence `ledger classes: <slug>=<n>, …; re-plan lines: <slug>, …`, a class counted as having a re-plan line only when its body line carries the prefix and the four words, and `ledger classes: none; re-plan lines: none` for an empty ledger (acceptance-front-matter.py writes an empty ledger before the first audit); the prompt's per-finding format string, today `'[P0-P3] confidence dimension file:line rationale'`, becomes `'[P0-P3] confidence dimension class=<slug> count=<n> file:line rationale'` (ledger-check.py's `^\s*(?:[-*+]\s+)?\[P[0-3]\]` still counts the line); the extraction's exit status decides and its stdout is the sentence, taken verbatim (an empty output is an empty sentence, not a refusal): a record whose block is missing or malformed makes the extraction exit non-zero and the wrapper refuse with `orch-audit: the record's JSON block is missing or malformed; refused` and exit 2 (the `refuse` helper's default) before any codex call; two tests in `tests/unit/test_orchestrator_tools.py` beside the four existing `test_orch_audit_*` tests, through the module's real-script harness: `test_orch_audit_prompt_lists_the_ledger_classes`, with a stub codex that records its argv and asserts the sentence and the format string, and `test_orch_audit_refuses_a_malformed_record_block`, asserting exit 2, the line and no codex call. Of the four existing `test_orch_audit_*` tests: `test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules` reaches the extraction with real Python (its `.python-version` shim) and a TSV-only record `4250000001\tother`, so its record fixture gains a valid JSON block (a ledger with that one row), its assertions unchanged, and its sibling `scripts/orchestrator/json.py` must still not be imported, which `python -I` keeps true (cwd and the script directory off `sys.path`), so that test covers the extraction too; `test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt` has no shim and writes no record, so its `uv run` calls go to the module's stub `uv` (records its argv, prints `$CALLS/uv-output`, which that test writes empty, and exits 0), the extraction's stdout is that empty output and the run proceeds with an empty sentence the test does not assert: no change there; `…_refuses_a_gap` stops at the ledger check (exit 3) and `…_differs_from_head` before it: unaffected. The two new tests use the shim as the isolation test does. Nothing else changes.

## Validation

- `uv run python -m unittest tests/unit/test_agmsg_orchestration_docs.py tests/unit/test_orchestrator_tools.py -v` green in the validation file, with the four new tests named; `shellcheck scripts/orchestrator/orch-audit.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after the rules task dotfiles-T128-rules-s1-replan-a01 merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-audit-s1-report-a01-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-audit-s1-report-a01-followup-a01` in this task's acceptance record. The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-audit-s1-report-a01/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T02:29:34Z)

The Codex half's round 1 (P2, P2): the Audit section gets its own fixture `tests/fixtures/regime/audit.md` (the existing code-review-orchestration.md pins the Code Review Rules and stays), named in `allowed_files` with its row; the wrapper's record extraction is stated as new work with its validation and exit-2 path, since today it delegates to ledger-check.py's TSV parser. Nothing else changes from `ea0a7d94`.

## Change (round 3, 2026-10-17T02:38:41Z)

The Codex half's round 3 (P2): the test_chain_glue row named one new test while item 2 requires two (the prompt sentence and the malformed-record refusal); the row now names both. Nothing else changes from `2f8278dd`.

## Change (round 4, 2026-10-17T02:56:52Z)

The review seat's round 1 (a003; P2 ×2, P3 ×4): the two wrapper tests move to `tests/unit/test_orchestrator_tools.py` (the module with the real-script harness and the four `test_orch_audit_*` tests; test_chain_glue.py stubs the wrapper), with its allowed_files entry and row; the prompt's per-finding format string gains `class=<slug> count=<n>`; the refusal line, its exit 2 and its place after the ledger check are named; the extraction uses the wrapper's `uv run --no-project python -I` idiom; item 1 names the `PINNED_SECTIONS` entry; the empty-ledger sentence is stated. Nothing else changes from `8a4bf6e1`.

## Change (round 5, 2026-10-17T03:03:27Z)

The Codex half's round 5 (P2): the two existing `test_orch_audit_*` tests whose TSV-only record reaches the new extraction would hit its exit 2; item 2 and the test module's row now authorise a valid JSON block in those two fixtures, assertions unchanged. Nothing else changes from `34116860`.

## Change (round 6, 2026-10-17T03:12:50Z)

The review seat's round 2 (a003; P2): the round-5 sentence named the no-fresh-receipt test as reaching the extraction with a TSV-only record, while that test writes no record and has no shim, so its `uv run` calls reach the module's stub `uv`; item 2 now states the extraction's contract (exit status decides, stdout verbatim) and each existing test's actual path. Sixth revise of this text, the class being claims about existing code made without the cited line: the `## Cited sources` section below pastes the lines the items rest on and is regenerated before each send. Nothing else changes from `da4d3799`.

## Change (round 7, 2026-10-17T03:16:49Z)

The Codex half's round 7 (P2): the test module's row still said two existing fixtures gain a JSON block while item 2 names one (the isolation test); the row now says one, as item 2 does. Nothing else changes from `006405e6`.

## Cited sources (pasted by the orchestrator, 2026-10-17T03:12:50Z, from the main checkout at b167fe0a)

```
$ sed -n "34,37p;47p;53p;57p" scripts/orchestrator/orch-audit.sh | cut -c1-120
refuse() {
    echo "orch-audit: $1; refused" >&2
    exit "${2:-2}"
}
cd -- "${root}"
uv run --no-project python -I -c 'import json, sys; gaps = [i for i in json.load(open(sys.argv[1]))["items"] if not i.ge
uv run --no-project python -I "${check}" ".orchestration/acceptance/${task}.md" "${v}/${task}-pr-feedback.json" ${lineag
$ /usr/bin/grep -oE "Report each finding as .[^ ]* [^ ]* [^ ]* [^ ]* [^ ]*." scripts/orchestrator/orch-audit.sh
Report each finding as '[P0-P3] confidence dimension file:line rationale' 
$ /usr/bin/grep -nE "P\[0-3\]" scripts/orchestrator/ledger-check.py | cut -c1-120
30:        count = len(re.findall(r"^\s*(?:[-*+]\s+)?\[P[0-3]\]", Path(path).read_text(), re.MULTILINE))
$ /usr/bin/grep -nE "\"ledger\"" scripts/orchestrator/acceptance-front-matter.py | cut -c1-120
78:    ledger = list(record.get("ledger", []))
120:    print("written", path.relative_to(root), "head", head[:7], "pr", block["pr"], "ledger", len(ledger))
$ sed -n "38,41p;1061,1063p;1077p;1114,1116p;1124,1126p;1131,1134p" tests/unit/test_orchestrator_tools.py | cut -c1-120
    # As uv does, a .python-version in the cwd that names an executable runs it.
    "uv": "#!/bin/bash\n"
    + 'pv="$(cat .python-version 2> /dev/null)" && [[ -x ${pv} ]] && exec "${pv}" "$@"\n'
    + RUN.format(name="uv"),
    def test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt(self):
        # a05 item 9: an earlier receipt of the audited head, here and tracked on main (so in the review
        # checkout too), never stands in for a run that wrote no new one.
        (self.calls / "uv-output").write_text("")
    def test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules(self):
        # Round 2 (Bot thread 4279174373, the audit of b84e81f0): the ledger check runs under python -I, so an
        # untracked json.py beside it, which exits 9 when imported, is never imported and the audit passes.
        shim = self.write("python-shim", f'#!/usr/bin/env bash\nshift 3\nexec "{sys.executable}" "$@"\n')
        shim.chmod(0o755)
        self.write(".python-version", f"{shim}\n")
        self.write(".orchestration/acceptance/t-a01.md", "4250000001\tother\n")
        # The run stops later at this fixture's masker call; the ledger check before it has run and passed.
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=3)
        self.assertIn("sweep gaps 0\nledger rows 1; findings 1; gaps 0\n", result.stdout)
$ sed -n "227,229p;236,240p" tests/unit/test_agmsg_orchestration_docs.py | cut -c1-120
    PINNED_SECTIONS = (
        # name, file, outer slice or None, (start, end): the start marker is part of the pinned text.
        ("invariants", SKILL, None, ("## Review and integration invariants", "\n## ")),
            ROOT / "AGENTS.md",
            None,
            ("### Orchestration records and trust-boundary code", "\n## "),
        ),
    )
```

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-audit-s1-report-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-audit-s1-report-a01.md
```

## Change (round 2, 2026-10-17T02:33:34Z)

The Codex half's round 2 (P2 ×3): the orch-audit row authorises the record extraction beside the prompt; `advisory-p2` is excluded from the missing-re-plan finding; a re-plan line needs the four words, not the prefix alone; the pasted checks section added. Nothing else changes from `54eddd5f`.
