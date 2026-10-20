---
format: 2
task_id: dotfiles-T129-assets-omp-hcom-followup-a06
kind: code
security: false
allowed_files:
  - scripts/update-agent-assets.sh
  - tests/unit/test_update_agent_assets.py
  - .orchestration/dotfiles-T129-assets-omp-hcom-followup-a06/**
after: [dotfiles-T129-assets-omp-hcom-followup-a05]
threat_table:
  - control: the PR edits scripts/update-agent-assets.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the task-level audit from main compares the diff against the rows"
  - control: the PR edits tests/unit/test_update_agent_assets.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-assets-omp-hcom-followup-a06/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-assets-omp-hcom-followup-a06/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the owned scripts on fixtures in temporary homes; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the owned scripts run as today"
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

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-followup-a06 — the assets lineage's fifth owner task (advisory P2 of PR #430)

Written 2026-10-20 by the orchestrator seat before the first advisory disposition of PR #430 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a06` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a05.md` (plan 020 step 1.2); it is dispatched after PR #430 merges, to a seat the orchestrator names.

## Item 1

Each owned row (any advisory P2 of the local review or the task-level audit of PR #430's final head, and any Bot P2 the orchestrator records under this owner; rows are read from the record at dispatch) gets its fix and one red-then-green test in `tests/unit/test_update_agent_assets.py`, named in report.md against the row id. Nothing outside the owned rows; any other file joins `allowed_files` only by an amendment that names the row needing it.

## Check and Completion

The Check and Completion clauses of `.orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a05.md` apply as written, with `dotfiles-T129-assets-omp-hcom-followup-a06` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-assets-omp-hcom-followup-a06/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
dispatch to claude-standard-dot-a009, 2026-10-19T20:1xZ; task-consistency-check.py: OK; security: false (no C-80); D-024-25 order: owner rows of a merged lineage, files disjoint from every in-flight task
task=dotfiles-T129-assets-omp-hcom-followup-a06 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=none..none (-) source=live
detail: pr=none authors=- tasks=- results=- questions=- withdrawn=- bot_heads=- source=live
```
