---
format: 2
task_id: dotfiles-T128-seat-liveness-followup-a02
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T128-seat-liveness-followup-a02/**
after: [dotfiles-T128-seat-liveness-followup-a01]
threat_table:
  - control: the PR edits home/dot_local/bin/common/executable_herdr-agents only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_herdr_agents.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: "the seat teardown herdr-agents --remove-worker --stale performs (despawn, delivery off, leave, the workspace close, the archive move under run/stale)"
    disposition: "residual: the lineage's controls (PR #367 and PR #377): no identity row is exit 2 before the state loop; the archive destination is checked after the state loop and before the first delivery.sh, a non-directory or unwritable or unsearchable run/stale is exit 1; covered by tests/unit/test_herdr_agents.py on main; the owned rows change other lines and each carries its own test"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-seat-liveness-followup-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-seat-liveness-followup-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run herdr-agents as a subprocess with stub agmsg scripts and a fake herdr on PATH in a temporary directory, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; herdr-agents runs the agmsg scripts and herdr from PATH as today and reads the manifest and model-profiles.env as data; nothing from a PR head runs; after the merge the operator runs `make update` (the launcher lives under `home/`)"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the two files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the lineage task file is on origin/main at dispatch (present since boundary (16), 1d418126, which carried the a01 task file)'
    command: 'git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a01.md && echo present || echo absent'
    output: |-
      present
  - claim: 'the lineage acceptance record''s Owned-by section is on origin/main at dispatch (absent today: it lands with the boundary after PR #377 merges; a dispatch before the section would read no rows)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-seat-liveness-followup-a02" && echo present || echo absent'
    output: |-
      absent
---

# AGMSG-TASK dotfiles-T128-seat-liveness-followup-a02 — the advisory findings of PR #377 (the owner task of the seat-liveness lineage; plan 020 step 1, C-51's owner-first rule)

Written 2026-10-16 by the orchestrator seat before the lineage's integration chain runs (C-51: an advisory P2 disposition is written only when its owner task file exists), pair-reviewed before dispatch. Under plan 020 step 4 a P2 finding (the Codex Bot, the orchestrator's local review, the task-level audit or the worker's own report) on a head of PR #377 that is not fixed in a C-50 revise round is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-seat-liveness-followup-a02` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md` under the heading `## Owned by dotfiles-T128-seat-liveness-followup-a02`; this task implements those rows after the lineage's PR merges.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-seat-liveness-followup-a02` in `.orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md` as read from `origin/main`; each row's finding text is in the record (the Bot thread, the local review file or the audit receipt the id names). Implement each, with one test per row named in report.md. A missing or empty section at dispatch makes this task a no-op: report `no owned rows` and stop; the orchestrator dispatches only after both premises replay `present`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name (herdr-agents still seats and removes workers as the SKILL describes).

## Validation

- `uv run python -m unittest tests/unit/test_herdr_agents.py -v` green in the validation file, with the new tests named; `shellcheck home/dot_local/bin/common/executable_herdr-agents`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #377 merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more after a P0/P1 fix round), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as fixed in a C-50 round or advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within allowed_files gets C-50's revise round while INV-6's counts allow it, else it is advisory and recorded under the same heading for the lineage's next owner task. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-seat-liveness-followup-a02/task.md>` and the evidence paths. After the merge the operator runs `make update` (the launcher lives under `home/`).
