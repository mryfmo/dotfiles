---
format: 2
task_id: dotfiles-T130-claude-sandbox-integration-followup-a01
kind: code
security: false
allowed_files:
  - README.md
  - .orchestration/dotfiles-T130-claude-sandbox-integration-followup-a01/**
after: [dotfiles-T130-claude-sandbox-integration-a01]
threat_table:
  - control: the PR edits README.md only within the owned rows (item 1)
    disposition: "residual: prose; the edits are exactly the owned rows of the lineage's acceptance record (item 1); the orchestrator's diff review and the task-level audit from main compare the diff against the rows and against the rendered settings the text describes"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T130-claude-sandbox-integration-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T130-claude-sandbox-integration-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: a text change; no script, test or setting runs differently"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the README's prettier and markdown checks run in the existing workflow"
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

# AGMSG-TASK dotfiles-T130-claude-sandbox-integration-followup-a01 — the sandbox-integration lineage's owner task (advisory P2 of PR #392)

Written 2026-10-17 by the orchestrator seat at the review of PR #392's final head (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T130-claude-sandbox-integration-followup-a01` in `.orchestration/acceptance/dotfiles-T130-claude-sandbox-integration-a01.md` (plan 020 step 1.2); it is dispatched after PR #392 merges and the operator's `make update`, to a seat the orchestrator names then.

## Goal

Every owned row is fixed; for a text row the README says what the rendered settings do, sentence by sentence, no more; no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T13:2xZ): 4302795772 (`README.md:464-480`, class stale-security-docs: the sandbox security paragraphs still describe the pre-#392 Claude sandbox; rewrite them from the rendered settings of each OS: the Mach allowlist, the per-OS excluded commands, the ask rules, the env map, the domains). Rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any setting change (the lineage's PR #392 and its own follow-ups own them); any README section the owned rows do not name.

## Check

`make validate-agent-assets` (exit 0) and `npx prettier --check README.md` (or the repository's formatter target) pasted in the validation file, with `git diff --numstat origin/main...HEAD`: README.md only outside `.orchestration/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #392 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T130-claude-sandbox-integration-followup-a02` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T130-claude-sandbox-integration-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T130-claude-sandbox-integration-followup-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T130-claude-sandbox-integration-followup-a01.md
```
