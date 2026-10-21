---
format: 2
task_id: dotfiles-T129-assets-omp-hcom-followup-a01
kind: code
security: false
allowed_files:
  - scripts/update-agent-assets.sh
  - scripts/lib/installer-pins.sh
  - scripts/check-tools.sh
  - tests/unit/test_update_agent_assets.py
  - tests/unit/test_asset_manifest.py
  - tests/unit/test_runtime_health.py
  - tests/install/common/check_tools.bats
  - .orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: the PR edits scripts/update-agent-assets.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows; the pinned, hash-verified downloads stay the review of what is installed"
  - control: the PR edits scripts/lib/installer-pins.sh only within the owned rows (item 1)
    disposition: "residual: as above; a pin changes only with its hash"
  - control: the PR edits scripts/check-tools.sh only within the owned rows (item 1)
    disposition: "residual: as above"
  - control: the PR edits tests/unit/test_update_agent_assets.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_asset_manifest.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_runtime_health.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/install/common/check_tools.bats only within the owned rows (item 1)
    disposition: "residual: Bats runs in CI only; one case per owned row"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the updater with stub curl, npm and uv on PATH in a temporary directory; no real install; the operator's make update is the live run"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under bash as today"
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

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-followup-a01 — the assets lineage's owner task (advisory P2 of PR #388)

Written 2026-10-17 by the orchestrator seat at PR #388's integration chain (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a01` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-a01.md` (plan 020 step 1.2); it is dispatched after PR #388 merges and the operator's `make update`, to a seat the orchestrator names then.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T14:3xZ): local:b49da6d:1 (`scripts/update-agent-assets.sh:989`, class install-receipt-artifact: the hcom wheel that uv's installation receipt references is removed after the install, so a later `uv tool` operation that re-reads the receipt finds no file; keep the verified wheel where the receipt points, or install from a path that persists). Rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row; a change of pin or hash.

## Check

`uv run python -m unittest tests/unit/test_update_agent_assets.py tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py -v` green and `shellcheck` on the edited scripts clean, pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 120 changed lines outside `tests/` and `.orchestration/`, 400 under `tests/`.

## Completion

One PR; the branch starts now from PR #388's head (b49da6dd or its successor; the files are shared) and rebases onto `origin/main` after #388 merges, no PR opening before that rebase (the monitor's 23:45 JST correction: the seat does not wait for the merge). The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-assets-omp-hcom-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-assets-omp-hcom-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-assets-omp-hcom-followup-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a01.md
```
