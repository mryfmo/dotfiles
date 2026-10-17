---
format: 2
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/chain-integrate.sh
  - scripts/require-crit-review.py
  - scripts/regime-counters.sh
  - scripts/orchestrator/acceptance-front-matter.py
  - tests/unit/test_chain_glue.py
  - tests/unit/test_require_crit_review.py
  - tests/unit/test_regime_counters.py
  - tests/unit/test_orchestrator_tools.py
  - .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/**
after: [dotfiles-T129-audit-inherit-replan-json-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/chain-integrate.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits scripts/require-crit-review.py only within the owned rows (item 1)
    disposition: "residual: the gate is a trust boundary; an owned row's fix never widens what the gate accepts without a test that refuses the wider form; the audit reads each case"
  - control: the PR edits scripts/regime-counters.sh only within the owned rows (item 1)
    disposition: "residual: as above; the audit reads each case"
  - control: the PR edits scripts/orchestrator/acceptance-front-matter.py only within the owned rows (item 1)
    disposition: "residual: as above; the writer's exact-key rule is never weakened"
  - control: the PR edits tests/unit/test_chain_glue.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_require_crit_review.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_regime_counters.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts as subprocesses on fixtures in a temporary directory with stub gh and real git in a temporary repository; nothing touches a live PR"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under the repository's python and bash as today"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T129-audit-inherit-replan-json-followup-a01 — the F1 lineage's owner task (advisory P2 of PR #390)

Written 2026-10-17 by the orchestrator seat before PR #390's integration chain (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a01` in `.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-a01.md` (plan 020 step 1.2); it is dispatched after PR #390 merges, to a seat the orchestrator names then, only if rows exist.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch: none at the time of writing (PR #390's two Bot findings were fixed in its rounds); rows added by the audit or a later review are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row.

## Check

`uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v` green pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 200 changed lines outside `tests/` and `.orchestration/`, 1000 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #390 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-audit-inherit-replan-json-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```
