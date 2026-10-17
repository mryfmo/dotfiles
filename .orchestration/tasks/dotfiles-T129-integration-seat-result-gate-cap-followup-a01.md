---
format: 2
task_id: dotfiles-T129-integration-seat-result-gate-cap-followup-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/integrate-seat.sh
  - scripts/orchestrator/result-precheck.sh
  - tests/unit/test_integration_seat.py
  - .orchestration/dotfiles-T129-integration-seat-result-gate-cap-followup-a01/**
after: [dotfiles-T129-integration-seat-result-gate-cap-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/integrate-seat.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits scripts/orchestrator/result-precheck.sh only within the owned rows (item 1)
    disposition: "residual: as above; the precheck never accepts a RESULT the lineage's rules refuse"
  - control: the PR edits tests/unit/test_integration_seat.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: "the inputs of the two scripts as a trust boundary (PR-controlled content: review bodies, comments, check runs; the RESULT line's fields)"
    disposition: "residual: the lineage's rows; a fix reads one more source (review bodies) through the same gh reads and the same badge grammar"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-integration-seat-result-gate-cap-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-integration-seat-result-gate-cap-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts as subprocesses with stub gh and stub scripts on PATH in a temporary repository; nothing touches a live PR"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run bash, git, gh and jq as the lineage's do"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T129-integration-seat-result-gate-cap-followup-a01 — the F4 lineage's owner task (advisory P2 of PR #393)

Written 2026-10-17 by the orchestrator seat at PR #393's second Bot review (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-integration-seat-result-gate-cap-followup-a01` in `.orchestration/acceptance/dotfiles-T129-integration-seat-result-gate-cap-a01.md` (plan 020 step 1.2); it is dispatched after PR #393 merges, to a seat the orchestrator names then.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T14:2xZ): 4302959629 (class review-body-findings: precheck (g) reads the Bot's inline comments only; a review-body finding with a P0 to P3 badge, which Worker Playbook step 15 lists beside the inline threads, is not seen; read the reviews of the head and treat a badge in a review body as a finding). Rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row.

## Check

`uv run python -m unittest tests/unit/test_integration_seat.py -v` green and `shellcheck` on the two scripts clean, pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 120 changed lines outside `tests/` and `.orchestration/`, 400 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #393 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-integration-seat-result-gate-cap-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-integration-seat-result-gate-cap-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
