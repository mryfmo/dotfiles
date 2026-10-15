---
format: 2
task_id: dotfiles-T128-chain-github-scripts-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/resolve-threads.sh
  - scripts/orchestrator/pr-cost.sh
  - tests/unit/test_chain_github_scripts.py
  - .orchestration/dotfiles-T128-chain-github-scripts-followup-a01/**
after: [dotfiles-T128-chain-github-scripts-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/resolve-threads.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits scripts/orchestrator/pr-cost.sh only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: the PR edits tests/unit/test_chain_github_scripts.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against those rows; an edit outside them is an undeclared change the audit fails"
  - control: "the GitHub writes (reply comments and thread resolutions on the PR, with the orchestrator's gh credentials): the body of a reply is built only from the disposition table row or the sweep JSON's disposition field, both orchestrator-authored, in the two fixed sentences; --dry-run writes nothing"
    disposition: "residual: covered on main by the lineage's test tests/unit/test_chain_github_scripts.py::test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows (one reply and one resolution per thread with a row, the missing row left open with exit 3, dry-run writing nothing); the first owned row, 4270684630, changes exactly this path (the resolve mutation's response is checked before the thread counts as resolved), so the owner PR's row edit carries its own test in that module and the audit reads this row for it"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-github-scripts-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-github-scripts-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the two scripts as subprocesses with the stub gh first on PATH and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run gh, jq, awk and uv run --no-project python, each resolved on the orchestrator's PATH (the tests put the stub gh first); the repository name mryfmo/dotfiles stays literal as in the inputs; nothing the PR under integration contains chooses any of them"
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
    command: 'git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md && echo present || echo absent'
    output: |-
      present
  - claim: 'the lineage acceptance record''s Owned-by section is on origin/main at dispatch (absent today: the section exists in the orchestrator''s checkout since the lineage''s RESULT of 12:32Z and lands with the boundary after PR #356 merges, before this task dispatches; a record on origin/main without the section is still absent here, so a dispatch before the section would read no rows)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-chain-github-scripts-followup-a01" && echo present || echo absent'
    output: |-
      present
---

# AGMSG-TASK dotfiles-T128-chain-github-scripts-followup-a01 — the residual findings of the GitHub-side chain scripts PR (#356) (the owner task of the chain-github-scripts lineage; plan 020 step 1, C-32's owner-first pattern)

Written 2026-10-14 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Under plan 020 a P2 finding (Codex Bot, the orchestrator's local review, the audit, or the worker's own report) on a head of PR #356 is advisory: it is dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-chain-github-scripts-followup-a01` and recorded as a row of `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md` under the heading `## Owned by dotfiles-T128-chain-github-scripts-followup-a01`; this task implements exactly those rows after the lineage's PR merges. Its first row is `4270684630`, in the owner section since 12:34Z today, written when the lineage's RESULT arrived (the Bot's P2 on resolve-threads.sh line 65: the resolve mutation's `isResolved` value is discarded, so a successful response carrying `false` still counts the thread resolved and the closed-row test checks only the request; the remedy the row names is to require the selected value to equal `true` before reporting success, with the test checking the response).

## What to do

1. The owned rows: the `<id>\t<class>` rows under the heading `## Owned by dotfiles-T128-chain-github-scripts-followup-a01` in `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md` as read from `origin/main` (advisory P2 findings on the lineage's PR heads, each dispositioned on the PR as `not-applicable:advisory P2 owned by dotfiles-T128-chain-github-scripts-followup-a01`, filed as a `local-finding:` or `audit-finding:` line naming this owner, or named in the lineage RESULT's report as advisory); each row's finding text is in the record (the Bot thread, the local review file, the audit receipt or the report the id names). Implement each, with one test per row named in report.md. A missing or empty section at dispatch makes this task a no-op: report `no owned rows` and stop; the orchestrator dispatches only after both premises replay `present`.
2. Nothing else changes: no file outside the owned rows' files, no behaviour the rows do not name, no change to what a script does beyond the row's text.

## Validation

- `uv run python -m unittest tests/unit/test_chain_github_scripts.py -v` in the validation file, with the new tests named; `shellcheck` on the changed scripts.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

A fresh branch from `origin/main` after PR #356 merges, one new PR. The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's single review (on PR open) is in, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 as advisory; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot reviews once, at PR open; its P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round stops the PR and goes to the operator as a decision; a P2 on this PR is advisory and recorded under the same heading in `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md` for the lineage's next owner task. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-github-scripts-followup-a01/task.md>` and the evidence paths.

## Change (round 2, 2026-10-14 12:40Z)

The seat's round 1: P2 the GitHub-writes row cited "the first closed row", which this file has none of; it now names the lineage's test on main as the cover and the first owned row as the edit of that path, with its own test in the owner PR. P3 the first-row sentence and premise 2's claim spoke of a future write; both now say the section exists since the lineage's RESULT.
