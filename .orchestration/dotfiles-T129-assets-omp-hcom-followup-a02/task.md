---
format: 2
task_id: dotfiles-T129-assets-omp-hcom-followup-a02
kind: code
security: false
allowed_files:
  - home/dot_local/bin/common/executable_remove-agent-asset
  - tests/unit/test_remove_agent_asset.py
  - scripts/update-agent-assets.sh
  - tests/unit/test_update_agent_assets.py
  - .orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/**
after: [dotfiles-T129-assets-omp-hcom-followup-a01]
threat_table:
  - control: the PR edits scripts/update-agent-assets.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance records (item 1), each with its test named in report.md; the pinned, hash-verified downloads stay the review of what is installed; the audit reads the diff against the rows"
  - control: the PR edits tests/unit/test_update_agent_assets.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row with stub curl, npm and uv on PATH, red before the fix and green after"
  - control: the PR edits home/dot_local/bin/common/executable_remove-agent-asset only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows; the removal runs uv tool uninstall for the named tool only"
  - control: the PR edits tests/unit/test_remove_agent_asset.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row with a stub uv on PATH, red before the fix and green after"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the removal with a stub uv in a temporary home; no live tool environment is touched by a test"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the script runs under bash as today"
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

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-followup-a02 — the assets lineage's second owner task (advisory P2 of PR #398)

Written 2026-10-17 by the orchestrator seat at PR #398's round 1 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a02` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md` (plan 020 step 1.2); it is dispatched after PR #398 merges, to a seat the orchestrator names then.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch (the records are the source: `dotfiles-T129-assets-omp-hcom-followup-a01.md` and, for the re-owned local row, `dotfiles-T130-claude-sandbox-integration-a01.md`; this list is their reading at 2026-10-17T16:4xZ): 4303212235 (class uninstall-leaves-tool-env: `remove-agent-asset` deletes hcom's binary and the retained wheel but not uv's tool environment; the removal runs `uv tool uninstall hcom` for that one tool when uv is present, and reports when it is not); 4303338055 (class install-receipt-repair, `scripts/update-agent-assets.sh`: when `uv tool install` fails after the verified wheel moved into place, the next run skips on the kept wheel without retrying; remove the retained wheel when the install fails, or require that uv's receipt names it before skipping); local:fbbc6d9:1 (class omp-non-npm-entry, `scripts/update-agent-assets.sh`: an existing non-npm omp entry (a mise or manual install) is handled before the npm install, so the managed binary wins without a stale entry shadowing it). Rows added to the records after this text was written are read from them at dispatch.

## Out of scope

Any rule not named by an owned row; the installer (the lineage's PR #388 and #398).

## Check

`uv run python -m unittest tests/unit/test_remove_agent_asset.py tests/unit/test_update_agent_assets.py -v` green and `shellcheck` on both scripts clean, pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 120 changed lines outside `tests/` and `.orchestration/`, 400 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #398 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-assets-omp-hcom-followup-a03` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-assets-omp-hcom-followup-a02.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a02.md
```
