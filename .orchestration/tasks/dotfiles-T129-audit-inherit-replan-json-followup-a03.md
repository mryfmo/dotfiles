---
format: 2
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a03
kind: code
security: true
allowed_files:
  - scripts/orchestrator/chain-integrate.sh
  - scripts/require-crit-review.py
  - scripts/regime-counters.sh
  - scripts/orchestrator/acceptance-front-matter.py
  - scripts/orchestrator/ledger-check.py
  - tests/unit/test_chain_glue.py
  - tests/unit/test_require_crit_review.py
  - tests/unit/test_regime_counters.py
  - tests/unit/test_orchestrator_tools.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a03/**
after: [dotfiles-T129-audit-inherit-replan-json-followup-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/chain-integrate.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits scripts/require-crit-review.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits scripts/regime-counters.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits scripts/orchestrator/acceptance-front-matter.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits scripts/orchestrator/ledger-check.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_chain_glue.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_require_crit_review.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_regime_counters.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_task_checkers.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a03/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a03/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts with fakes on PATH in temporary repositories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under bash and uv run --no-project python -I as today"
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

# AGMSG-TASK dotfiles-T129-audit-inherit-replan-json-followup-a03 — the F1 lineage's owner task (advisory P2 of PR #423)

Written 2026-10-19 by the orchestrator seat before the first advisory disposition of PR #423 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a03` in `.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a02.md` (plan 020 step 1.2); it is dispatched after PR #423 merges, to a seat the orchestrator names.

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of PR #423's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch) gets its fix and one red-then-green test in the test module beside the fixed script, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a02.md` apply as written, with `dotfiles-T129-audit-inherit-replan-json-followup-a04` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a03/task.md>` in the RESULT.
