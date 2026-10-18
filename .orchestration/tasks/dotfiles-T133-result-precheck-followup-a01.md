---
format: 2
task_id: dotfiles-T133-result-precheck-followup-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/result-precheck.sh
  - tests/unit/test_result_precheck.py
  - .orchestration/dotfiles-T133-result-precheck-followup-a01/**
after: [dotfiles-T133-result-precheck-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/result-precheck.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_result_precheck.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-result-precheck-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the script with fakes on PATH in temporary repositories; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; result-precheck.sh runs under bash with git, make and uv as today"
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

# AGMSG-TASK dotfiles-T133-result-precheck-followup-a01 — the P1-5 lineage's owner task (advisory P2 of PR #411)

Written 2026-10-18 by the orchestrator seat before the F5 acceptance disposition (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-result-precheck-followup-a01` in `.orchestration/acceptance/dotfiles-T133-result-precheck-a01.md` (plan 020 step 1.2); it is dispatched after PR #411 merges, to a seat the orchestrator names then.

## Item 1

Each owned row (the advisory P2 of the local review of a5cb73b4 and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch) gets its fix and one red-then-green test in `tests/unit/test_result_precheck.py`, named in report.md against the row id. Nothing outside the owned rows; `.githooks/*` and `scripts/orchestrator/dispatch.sh` join `allowed_files` only by an amendment naming the row that needs them.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-result-precheck-a01.md` apply as written, with `dotfiles-T133-result-precheck-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-result-precheck-followup-a01/task.md>` in the RESULT.
