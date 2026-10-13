---
format: 2
task_id: dotfiles-T128-gate-evidence-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/require-crit-review.py
  - tests/unit/test_require_crit_review.py
  - tests/fixtures/gate-evidence/*
  - Makefile
  - README.md
  - .orchestration/dotfiles-T128-gate-evidence-followup-a01/**
after: [dotfiles-T128-gate-evidence-a04]
invariants:
  INV-6: "the reset rule's mandatory point is the merge backstop in scripts/require-crit-review.py, with the orchestrator's Stop hook (Claude Stop hook, Codex [hooks].Stop) as the early signal, soft on both runtimes by their documented caps; counts come from history for the hook and the gate (revises = RESULTs for the task_id minus one, threshold 2; amendments = AGMSG-TASKs after the first, threshold 2; AGMSG-PONG status=question, threshold 2) and from GitHub and main-checkout files for the gate and the boundary check only (Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py; an audit implementation or specification finding at P0-P1 on two heads, from .orchestration/validation/<task>-audit-<sha7>.json in the main checkout, each counted only when its sha256 matches its AGMSG-AUDIT record); when a count is reached the gate refuses the merge until a reset record names a redesign task whose design RESULT comes from an identity other than the task's author, or a waiver written by scripts/regime-waive.sh under the INV-1 ask-rule discipline into the state directory outside the sandbox write roots (the only release path besides a redesign; the one-account residual of INV-1 applies); check-regime-boundary.sh reports a closed-unmerged PR whose task has no reset record and a task over any count with neither an accepted acceptance record nor a reset record; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)"
threat_table:
  - control: the PR edits scripts/require-crit-review.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_require_crit_review.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits or adds files under tests/fixtures/gate-evidence/* only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-gate-evidence-followup-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared by the orchestrator at acceptance); the pair's receipts name this file's hash"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C10 and C7b before dispatch and by the orchestrator at acceptance, never by a hand-written parser; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file, so a second front matter or a moved separator fails acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-gate-evidence-followup-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md), which acceptance and the audit read
    disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and the unit-test output, and the audit reads those sources itself"
  - control: "in-process effects: CI imports scripts/require-crit-review.py into the unittest process when it runs tests/unit/test_require_crit_review.py"
    disposition: "residual: the imported module is the declared change itself, reviewed line by line by the orchestrator and the audit from main"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: none: the gate reads the record with the standard library's json module and the correction records with pathlib; the diff adds no host binary call, no uv invocation and no import outside the standard library (C-26's check C11 replays this on the head; thread 4250238721); an undeclared change to a workflow, interpreter or environment file is outside the task and fails at the audit (INV-12)"
  - control: the PR edits Makefile only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits README.md only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: "the ACCEPTANCE_EVIDENCE input: the acceptance record's path, its JSON block (task, head, pr, ledger, searches, audit_findings, optional dispatch) and the ledger's coverage of the swept finding ids, written by the orchestrator and read by the gate"
    disposition: "closed: tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance and tests/unit/test_require_crit_review.py::test_acceptance_record_ledger_must_cover_swept_findings"
  - control: "the AUDIT_EVIDENCE summary (the .last.md file beside the audit receipt: one [P0] to [P3] line per finding, written by the audit runner), which the gate now counts for the ledger coverage"
    disposition: "residual: the gate counts the lines that begin with [P0] to [P3] and reads nothing else of it; the summary is the audit runner's output in the main checkout (INV-5) and is not hash-bound today, so a shortened summary shrinks the required id set: the acceptance record pastes the audit receipt's finding count and the design round compares the two (open residual for T704's ledger-check)"
  - control: new or renamed scripts
    disposition: "residual: none; allowed_files names no new script path, and a new or renamed script outside it is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the lineage's last task file is on origin/main (this task runs after it)"
    command: "git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-gate-evidence-a04.md && echo present"
    output: "present"
  - claim: "the lineage's acceptance record is on origin/main (the owned section is appended to it by the daily boundary after the PR's merge, before this task dispatches)"
    command: "git cat-file -e origin/main:.orchestration/acceptance/dotfiles-T128-gate-evidence-a04.md && echo present"
    output: "present"

---

# AGMSG-TASK dotfiles-T128-gate-evidence-followup-a01 — the residual findings of PR #329 (T702 gate evidence) (the owner task of the T702 gate-evidence lineage; plan 020 step 1, C-32's owner-first pattern)

Written 2026-10-13 13:37Z by the orchestrator seat, pair-reviewed before dispatch. Under plan 020 a P2 finding (Codex Bot, the orchestrator's local review, or the audit) on a head of PR #329 (T702 gate evidence) is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-gate-evidence-followup-a01` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-gate-evidence-a04.md` under the heading `## Owned by dotfiles-T128-gate-evidence-followup-a01`; only P0/P1 findings get the PR's one fix round. This task fixes exactly those rows after the PR merges; it exists on `main` before the findings do, so no boundary commit is needed between a PR's final head and its merge. Review tier by INV-1 (the same files and kind as `dotfiles-T128-gate-evidence-a04`). The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file. Dispatch condition: this task carries `invariants: INV-6` (it edits INV-6's mandatory point), and the design's `implementing_tasks` for INV-6 on `origin/main` lists only `dotfiles-T128-gate-evidence-a01` to `-a04`; this task is dispatchable only after the design amendment of plan 020 step 8 adds its id to that entry (INV-2's set comparison); until then it stays a file on main.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-gate-evidence-followup-a01` in `.orchestration/acceptance/dotfiles-T128-gate-evidence-a04.md` as read from `origin/main` (advisory P2 findings on the lineage's PR heads, each dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-gate-evidence-followup-a01; evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-gate-evidence-followup-a01.md | grep -n 'item 1'` (the gate's full form once PR #329 lands)). That section is this item's whole definition, closed at the lineage's acceptance and landed by the daily boundary after the merge; this task dispatches only after that boundary (the dispatch line names the record's hash); a finding outside the section is not owned here, and a missing or empty section at dispatch makes this task a no-op that report.md states (the section is created at the lineage's acceptance, so it does not exist before that). For each row: the defect the thread or finding names is fixed at root cause in the file it names, with one test per fix in the lineage's test module (and a fixture when the test reads one); the RESULT lists each row with `fixed:<sha>`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name.

## Validation

- The lineage's test command output in the validation file (the module `allowed_files` names), with the new tests named.
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`).

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot's single review (on PR open) is in, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread as advisory. A fresh branch from `origin/main` after the lineage's PR merges, a new PR; the orchestrator runs the local review once on the final head; one fix round at most; a surviving P0/P1 stops the PR.
