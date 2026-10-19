---
format: 2
task_id: dotfiles-T133-regime-ci-followup-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/regime-ci.py
  - .github/workflows/regime.yml
  - tests/unit/test_regime_ci.py
  - tests/unit/test_workflow_security.py
  - .orchestration/dotfiles-T133-regime-ci-followup-a01/**
after: [dotfiles-T133-regime-ci-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/regime-ci.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits .github/workflows/regime.yml only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_regime_ci.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_workflow_security.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-regime-ci-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts with fakes on PATH in temporary directories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; regime.yml runs regime-ci.py under uv run --no-project --with pyyaml python -I from the base commit"
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

# AGMSG-TASK dotfiles-T133-regime-ci-followup-a01 — the P1-11 lineage's owner task (advisory P2 of PR #418)

Written 2026-10-18 by the orchestrator seat before the first advisory disposition of PR #418 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-regime-ci-followup-a01` in `.orchestration/acceptance/dotfiles-T133-regime-ci-a02.md` (plan 020 step 1.2; the a01 record holds the S1 class table); it is dispatched after PR #418 merges, to a seat the orchestrator names.

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of PR #418's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the records at dispatch) gets its fix and one red-then-green test in `tests/unit/test_regime_ci.py` or `tests/unit/test_workflow_security.py`, named in report.md against the row id. Nothing outside the owned rows; `scripts/orchestrator/task-consistency-check.py` joins `allowed_files` only by an amendment that names the row needing them.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-regime-ci-a02.md` apply as written, with `dotfiles-T133-regime-ci-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-regime-ci-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T01:3xZ dispatch 1 (the owner task of P1-11; the a02 record Owned by section holds 3 rows: audit:f7d2c48:3 stale-pr-description, audit:7fad835:1 threat-row-selector, audit:7fad835:2 evidence-head-mismatch)
task=dotfiles-T133-regime-ci-followup-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live; task-consistency-check: OK; C-78: no in-flight task names regime-ci.py, regime.yml, test_regime_ci.py or test_workflow_security.py
```
