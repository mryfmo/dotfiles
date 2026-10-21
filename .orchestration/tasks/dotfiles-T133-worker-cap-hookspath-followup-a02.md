---
format: 2
task_id: dotfiles-T133-worker-cap-hookspath-followup-a02
kind: code
security: true
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a02/**
after: [dotfiles-T133-worker-cap-hookspath-followup-a01]
threat_table:
  - control: the PR edits home/dot_local/bin/common/executable_herdr-agents only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_herdr_agents.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-worker-cap-hookspath-followup-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the launcher against temporary repositories with fake agmsg scripts and a fake herdr on PATH; nothing live changes before the operator's make update"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the launcher runs under the host's bash as today"
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

# AGMSG-TASK dotfiles-T133-worker-cap-hookspath-followup-a02 — the P1-7 lineage's owner task (advisory P2 of PR #422)

Written 2026-10-18 by the orchestrator seat before the P1-7 acceptance disposition (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T133-worker-cap-hookspath-followup-a02` in `.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md` (plan 020 step 1.2); it is dispatched after PR #408 merges, to a seat the orchestrator names then.

## Item 1

Each owned row (any advisory P2 of the local review, the task-level audit or the security review of PR #422's final head, and any Bot P2 the orchestrator records under `## Owned by dotfiles-T133-worker-cap-hookspath-followup-a02` in `.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md`; rows are read from the record at dispatch) gets its fix and one red-then-green test in `tests/unit/test_herdr_agents.py`, named in report.md against the row id. Nothing outside the owned rows. Written 2026-10-19T00:0xZ by the orchestrator seat before PR #422's first advisory disposition (C-51). This task runs on a Codex seat.

Each owned row (the Bot P2 4305808095 was first recorded here; the task-level audit of c96697ae showed the defect is the lock path, not `is_main_checkout`, so that row moves to the reset task dotfiles-T133-worker-cap-hookspath-a02 and this task starts with no row; rows the orchestrator adds later are read from the record) gets its fix and one red-then-green test in `tests/unit/test_herdr_agents.py`, named in report.md against the row id. Nothing outside the owned rows.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md` apply as written, with `dotfiles-T133-worker-cap-hookspath-followup-a03` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-cap-hookspath-followup-a02/task.md>` in the RESULT.
