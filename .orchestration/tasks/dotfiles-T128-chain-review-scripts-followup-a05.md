---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a05
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/**
after: [dotfiles-T128-chain-review-scripts-followup-a04]
threat_table:
  - control: the PR edits scripts/orchestrator/local-advisory.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits tests/unit/test_chain_review_scripts.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after; the audit reads each case against its row"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-followup-a05/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run local-advisory.sh as a subprocess on fixture files in a temporary directory and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the script runs bash and the main checkout's files as the chain runs it today"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the two files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a05 — the chain-review lineage's next owner task (advisory P2 of PR #386)

Written 2026-10-17 by the orchestrator seat at the integration of PR #386 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a05` in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a04.md` (plan 020 step 1.2); it is dispatched after PR #386 merges, to a seat the orchestrator names then.

## Goal

Every owned row is fixed in `scripts/orchestrator/local-advisory.sh` with one fixture per row in `tests/unit/test_chain_review_scripts.py`, red before and green after; no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T13:0xZ): audit:000c5c6:1 (`scripts/orchestrator/local-advisory.sh:62`, class filename-suffix-parse: the earlier-review guard checks the text after the last `-local-review-`, so `<task>-local-review-notes-local-review-aaaaaa1.md` passes as `aaaaaa1` and a matching finding inherits an unrelated `local:aaaaaa1:1` row; strip the exact task prefix before validating the whole suffix, and test that filename). Rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row; the chain's other scripts.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green pasted in the validation file, with `shellcheck scripts/orchestrator/local-advisory.sh` clean and `git diff --numstat origin/main...HEAD`: at most 200 changed lines outside `tests/` and `.orchestration/`, and 1000 added lines under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #386 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T128-chain-review-scripts-followup-a06` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-chain-review-scripts-followup-a05.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a05.md
```
