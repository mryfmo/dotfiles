---
format: 2
task_id: dotfiles-T128-gate-evidence-a01
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/require-crit-review.py
  - tests/unit/test_require_crit_review.py
  - tests/fixtures/gate-evidence/*
  - Makefile
  - README.md
  - .orchestration/dotfiles-T128-gate-evidence-a01/**
after: []
invariants:
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
threat_table:
  - control: the PR edits scripts/require-crit-review.py, the merge backstop (INV-6's mandatory point) that the orchestrator runs on the host from the main checkout after the merge
    disposition: "residual: the script is design tier (the design's enforcement row INV-6 and waves V2b/V3a name it); the orchestrator's diff review and the task-level audit from main read every changed line, the unit tests of this PR cover both the refusals and the acceptances named below, and the script runs on the host only from main after the merge, never from the PR tree in CI"
  - control: the PR edits tests/unit/test_require_crit_review.py, the module that is the oracle for its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the test diff beside the script diff; a deleted or weakened test is a conformance finding (INV-12)"
  - control: the PR adds tests/fixtures/gate-evidence/* (two pr-feedback JSON files and two acceptance records), data the tests read
    disposition: "residual: fixtures are data read by the declared test module only; each fixture is listed in the RESULT with the test that reads it, and the audit compares the wrong-disposition fixtures with the two real dispositions of 2026-10-12 they reproduce"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-gate-evidence-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-gate-evidence-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md), which acceptance and the audit read
    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the unit-test output, and the audit reads those sources itself"
  - control: "in-process effects: CI imports scripts/require-crit-review.py into the unittest process when it runs tests/unit/test_require_crit_review.py"
    disposition: "residual: the imported module is the declared change itself, reviewed line by line by the orchestrator and the audit from main"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none in allowed_files; an undeclared change to a workflow, interpreter or environment file is outside the task and fails at the audit (INV-12)"
  - control: the PR edits Makefile (the require-crit-review recipe's explicit variable list and its comment, lines 205 to 211)
    disposition: "residual: the diff adds one variable name to the recipe and one to the comment; the orchestrator's diff review and the audit read the two lines; no other target changes"
  - control: the PR edits README.md (the two lines that name the gate's inputs, 427 and 1101 on main)
    disposition: "residual: prose that names the new input beside the existing ones; reviewed in the diff; no other README section changes"
  - control: new or renamed scripts
    disposition: "residual: none; allowed_files names no new script path, and a new or renamed script outside it is an undeclared change the audit fails"
  - control: orchestrator effects on this PR (merge, update-branch, forced worker removal)
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate; update-branch re-runs CI, the sweep and the audit on the new head; no forced removal is planned"
premises:
  - claim: "the gate's disposition grammar accepts not-applicable:<reason> with no evidence clause and checks only a 20-character minimum for failure-level items"
    command: "sed -n '26,27p' scripts/require-crit-review.py"
    output: |-
      PR_FEEDBACK_DISPOSITION = re.compile(r"(?:fixed:(?P<commit>[0-9a-f]{7,40})|not-applicable:(?P<reason>.*\S.*))", re.S)
      FAILURE_REASON_MIN_CHARS = 20
  - claim: "the two wrong dispositions of 2026-10-12 (refuted by the audit of 3a54d340) are the ledger rows 4244248692 and 4244378809 of the A7 a02 acceptance record; their first replies cited a setting and a script line that the record did not paste"
    command: "grep -n -E '^4244248692|^4244378809' .orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a02.md"
    output: |-
      26:4244248692	threat-row-outside-paths
      33:4244378809	result-head-binding
  - claim: "an acceptance record's ledger is tab-separated rows of <thread id or audit:<sha7>:<n>> and <class>, one per swept or audited finding"
    command: "awk -F'\\t' 'NF==2 && ($1 ~ /^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/ || $1 ~ /^audit:/) {print NR\": \"$0}' .orchestration/acceptance/dotfiles-T128-process-rules-a07.md | head -3"
    output: |-
      16: 4240250137	tool-not-on-main
      17: 4240250141	step15-wait
      18: 4240269216	scope
---

# AGMSG-TASK dotfiles-T128-gate-evidence-a01 — the gate requires `evidence=` on every `not-applicable` and refuses an acceptance action after a third repeat without the pasted search (plan 007 T702, S6)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 1, T702) and plan 006 (regime v3 design, INV-6). Design tier: `scripts/require-crit-review.py` is INV-6's mandatory point; the design's `implementing_tasks` entry for this id is `[INV-6]` (design v20, plan 006 B0), and the front matter carries INV-6's sentence byte for byte (INV-2). One PR, one invariant. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## Why (the mistakes this closes: M-20261012-3, C-5)

On 2026-10-12 two `not-applicable` dispositions written from memory ("human-only permission gate" where the managed settings say `defaultMode: auto` and `ask: []`; "never counted" where `regime-counters.sh:114` uses the first RESULT as the baseline) passed the gate and reached the auditor, who refuted both. The gate's grammar (premise 1) cannot tell a reason from a recollection. Plan 007 Phase 0 now requires `; evidence=<command>` on every `not-applicable`, and S6 requires the pasted record search once a finding class reaches three on one artifact. This task makes both mechanical.

## What to do

1. In `scripts/require-crit-review.py`, extend `PR_FEEDBACK_DISPOSITION` so a `not-applicable` disposition is `not-applicable:<reason>; evidence=<command>` with a non-empty `<reason>` and a non-empty `<command>` (the `fixed:<commit>` form is unchanged). Apply the same rule to every `audit-finding:` line read through `AUDIT_DISPOSITIONS`. Error text names the missing clause: `needs a disposition fixed:<commit> or not-applicable:<reason>; evidence=<command>`.
2. Add `ACCEPTANCE_EVIDENCE=<acceptance record>` as a required input whenever `BASE` is set (PR mode), beside `PR_FEEDBACK_EVIDENCE`; reuse the existing path check (`orchestration_path_error`) for it. Name it where the inputs are named: the `require-crit-review` recipe's explicit variable list and its comment in `Makefile` (lines 205 to 211), and the two README lines that list the gate's inputs (427 and 1101 on main); the SKILL's step 10.4 sentence is `dotfiles-T128-playbook-rules-a01`'s. The module's existing PR-mode tests that set `BASE` gain the variable (with a passing record fixture) so they keep passing. Read its ledger: every line matching `^\S+\t\S+$` whose first field is a thread id (10 or more digits) or `audit:<sha7>:<n>` is one row of `<id>\t<class>`. For each class with three or more rows, the record must contain a line beginning with `search:` that names that class slug and both commands, `contextdb_cli.py memory search` and `grep -rl`; otherwise the gate refuses with `S6: class <slug> at <n> without a pasted search`. A record with no class at three passes.
3. Unit tests in `tests/unit/test_require_crit_review.py`, with fixtures under `tests/fixtures/gate-evidence/`: `pr-feedback-wrong.json` (two items carrying the dispositions of premise 2 as they were first written, without evidence; refused with the new error text), `pr-feedback-right.json` (the same two items with `; evidence=<command>`; accepted), `acceptance-s6-missing.md` (a ledger with one class at three rows and no `search:` line; refused with the S6 text) and `acceptance-s6-present.md` (the same ledger with the `search:` line; accepted). Keep the four fixtures under 60 lines together; the test count for the module grows by at least four.
4. `make require-crit-review` on a records-only tree (no `BASE`) is unchanged; state the command and its output in the validation file.
5. Nothing else changes: not the gate's other checks, not the SKILL (`dotfiles-T128-playbook-rules-a01` owns the rule text and the step 10.4 sentence), not the scratchpad tools the orchestrator uses to fill dispositions (T718).

## Validation

- `uv run --no-project python -m unittest tests/unit/test_require_crit_review.py -v` output in the validation file, with the four new tests named.
- The fixture files listed in the RESULT with the test that reads each.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 15 changed files outside `.orchestration/`, at most 500 added lines outside `tests/`, at most 1000 under `tests/` (INV-2).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>` (this task's own grammar). Branch `regime/gate-evidence`, draft PR from `origin/main`, `kind: code`.
