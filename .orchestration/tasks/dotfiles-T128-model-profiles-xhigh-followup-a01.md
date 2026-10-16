---
format: 2
task_id: dotfiles-T128-model-profiles-xhigh-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/dot_codex/modify_private_standard.config.toml
  - README.md
  - .orchestration/dotfiles-T128-model-profiles-xhigh-followup-a01/**
after: [dotfiles-T128-model-profiles-xhigh-a01]
threat_table:
  - control: the PR edits home/dot_agents/agent-config.yaml only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits home/dot_codex/modify_private_standard.config.toml only within the owned rows (item 1)
  - control: "the PR edits README.md only within the owned rows (item 1: the three-role constellation paragraph's efforts, the Bot's P2 4289170845 on PR #370)"
    disposition: "residual: the paragraph lines 361 to 366 state the manifest's values after PR #370 (deep Claude xhigh, standard Codex xhigh, review Codex gpt-6.1-sol xhigh); prose, read by the audit against the manifest; no code"
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-model-profiles-xhigh-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-model-profiles-xhigh-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests of the lineage's module import only the standard library and the module under test; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the owned rows name edits to files the lineage landed, run by the same interpreters and seams as the lineage's task states; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the lineage task file is on origin/main at dispatch (absent today: it lands with the next boundary; this task never dispatches before)'
    command: 'git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-model-profiles-xhigh-a01.md && echo present || echo absent'
    output: |-
      absent
  - claim: 'the lineage acceptance record''s Owned-by section is on origin/main at dispatch (absent today: a dispatch before the section would read no rows)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-model-profiles-xhigh-a01.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-model-profiles-xhigh-followup-a01" && echo present || echo absent'
    output: |-
      absent
---

# AGMSG-TASK dotfiles-T128-model-profiles-xhigh-followup-a01 — the advisory findings of PR #370 (plan 007 T717, plan 022 D-model-roles) (the owner task of the dotfiles-T128-model-profiles-xhigh lineage; plan 020 step 1, C-51's owner-first rule)

Written 2026-10-15 by the orchestrator seat before the lineage's integration chain runs (C-51: an advisory P2 disposition is written only when its owner task file exists), pair-reviewed before dispatch. Under plan 020 a P2 finding (the Codex Bot, the orchestrator's local review, the task-level audit or the worker's own report) on a head of PR #370 (plan 007 T717, plan 022 D-model-roles) is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-model-profiles-xhigh-followup-a01` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-model-profiles-xhigh-a01.md` under the heading `## Owned by dotfiles-T128-model-profiles-xhigh-followup-a01`; this task implements those rows after the lineage's PR merges. A small P2 on the PR's own change within the lineage's files is a revise round instead (C-50), never a row here.

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-model-profiles-xhigh-followup-a01` in `.orchestration/acceptance/dotfiles-T128-model-profiles-xhigh-a01.md` as read from `origin/main`; each row's finding text is in the record (the Bot thread, the local review file or the audit receipt the id names). Implement each, with one test per row named in report.md. A missing or empty section at dispatch makes this task a no-op: report `no owned rows` and stop; the orchestrator dispatches only after both premises replay `present`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name.

## Validation

- The lineage's test module green in the validation file, with the new tests named; `shellcheck` or `ruff` as the lineage's task states for its files.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after the lineage's PR merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=1`, stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-model-profiles-xhigh-followup-a02`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-model-profiles-xhigh-followup-a02` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-model-profiles-xhigh-followup-a01/task.md>` and the evidence paths.
