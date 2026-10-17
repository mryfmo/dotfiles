---
format: 2
task_id: dotfiles-T130-sandbox-portability-followup-a01
kind: code
security: false
allowed_files:
  - scripts/check-statusline-tools.py
  - tests/unit/test_sandbox_portability.py
  - .orchestration/dotfiles-T130-sandbox-portability-followup-a01/**
after: [dotfiles-T130-sandbox-portability-a01]
threat_table:
  - control: the PR edits scripts/check-statusline-tools.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits tests/unit/test_sandbox_portability.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after; the guards never widen to refuse less than they do on the lineage's head"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T130-sandbox-portability-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T130-sandbox-portability-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests read git ls-files and the checkout and write fixtures into a temporary directory; nothing else runs"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the tests run under make unit-test as today"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T130-sandbox-portability-followup-a01 — the portability lineage's owner task (advisory P3 and later P2 of PR #395)

Written 2026-10-17 by the orchestrator seat at PR #395's round 1 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T130-sandbox-portability-followup-a01` in `.orchestration/acceptance/dotfiles-T130-sandbox-portability-a01.md` (plan 020 step 1.2); it is dispatched after PR #395 merges, to a seat the orchestrator names then, only if rows exist.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T15:3xZ): the worker review's six declared P3 of round 1 (among them: `.sh.tmpl` scripts sit outside both guards; an `export TMPDIR=/tmp` line is accepted), each a row at the sweep with its class; rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row; the CompactionDB store relocation (D-portability-store, an upstream design task).

## Check

`uv run python -m unittest tests/unit/test_sandbox_portability.py -v` green pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 40 changed lines outside `tests/` and `.orchestration/`, 200 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #395 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T130-sandbox-portability-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T130-sandbox-portability-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
