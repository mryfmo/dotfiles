---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a03
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/**
after: [dotfiles-T128-chain-review-scripts-followup-a02]
threat_table:
  - control: the PR edits scripts/orchestrator/local-advisory.sh in two places, the refusal of an absent owner task file with the evidence that hashes the file (item 1a) and the class of a repeated finding (item 1b)
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file"
  - control: "the class of a repeated finding (item 1b): a finding whose path:line token matches an earlier local review's finding takes that finding's class from the record"
    disposition: "closed: tests/unit/test_chain_review_scripts.py::test_local_advisory_classes_a_repeat_by_the_earlier_row"
  - control: the PR edits tests/unit/test_chain_review_scripts.py (two new tests beside the three and the ones the a02 owner task adds, which stay as they are; the temporary repository holds the local review files, the record and the owner task file the case writes)
    disposition: "residual: the fixtures are files the case writes; the audit reads each case against items 1a and 1b"
  - control: "the acceptance record and the owner task file (.orchestration/acceptance/<task>.md, .orchestration/tasks/<owner>.md in the checkout the script runs from): the script appends rows and lines to the record and reads the owner file's existence and sha256"
    disposition: "residual: the record is appended only, each row and line once (as today); the owner file is read, never written; a missing owner file is exit 2 before any row is written"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
  - control: in-process effects
    disposition: "residual: the test module imports only the standard library and runs the script as a bash subprocess with real git in a temporary repository; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; local-advisory.sh runs git rev-parse, grep, sed, cut, tr, head, sort and now shasum from PATH, as the lineage's scripts do; the tests' seam is the temporary repository as cwd; a PR checkout as cwd chooses nothing new, since the script already resolves the record and the review file from the repository root it runs in"
premises:
  - claim: 'local-advisory.sh on origin/main writes an advisory row without checking that the owner task file exists'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"'
    output: |-
      0
  - claim: 'local-advisory.sh on origin/main names git show origin/main as the row evidence, replayable only after the boundary'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"'
    output: |-
      1
  - claim: 'local-advisory.sh on origin/main gives every row the class advisory-p2'
    command: 'git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"'
    output: |-
      2
  - claim: 'the chain-review test module on origin/main holds fourteen tests after the a01 and a02 owner PRs (#364 merged as fdef3ceb, #376 merged as f7847616) landed theirs; this task adds its own beside them'
    command: 'git show origin/main:tests/unit/test_chain_review_scripts.py | /usr/bin/grep -c "def test_"'
    output: |-
      14
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a03 — local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the record's earlier row (corrections C-51 (2) and C-50 (3); the chain-review-scripts lineage's next owner task; a Claude seat)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch. Two corrections name this task as the landing of their tool half. C-51 (M-20261015-03): the chain wrote advisory rows whose owner task existed only as a name, with an evidence command (`git show origin/main:.orchestration/tasks/<owner>.md …`) that replays only after a boundary, and two audits raised it. C-50 (M-20261015-02): the class table gives every local advisory row the generic class `advisory-p2`, so a defect found again on a later head is never counted as a repeat of the same class and the three-rows rule cannot fire on it.

## Change (round 2, 2026-10-15T22:08:38Z)

The review seat's round 1 (confirm on `0d82d7c4`, five P3 taken as text fixes since the task waits for the a02 owner task): the owner check sits after the no-findings exit and before the heading; both refusals exit 2 with distinct messages; the token grammar ignores backticks and allows a line range, and the earlier number is the loop's; the scope (local review files and `local:` rows only) is stated against C-50's wider sentence; a repeat row's line names its provenance.

## Change (round 3, 2026-10-15T22:11:13Z)

The Codex half's round 2 (on `5bd7e601`): P3 the absent-owner case now asserts the record byte-identical to its pre-run content; P3 the repeat test adds a line-range token and two matching earlier heads with different classes, the later head's class winning.

## Goal

After the merge, `local-advisory.sh` writes no row whose owner task file is absent, its evidence command hashes that file in the checkout it runs from, and a finding repeated from an earlier head of the task takes the class the record gave the earlier finding.

## Files

1. `scripts/orchestrator/local-advisory.sh`: (a) after the script's existing exit 0 for a review without findings and before it writes the `## Owned by <owner>` heading, `.orchestration/tasks/<owner>.md` must exist in the repository root the script runs from, else it prints `write the owner task <owner> first` and exits 2 as well (the missing review file keeps its exit 2; the two messages tell them apart and the `@exitcode 2` line names both), so a refused run leaves the record untouched and a review without findings needs no owner file; the `evidence=` tail of each `local-finding:` line becomes `shasum -a 256 .orchestration/tasks/<owner>.md` with the file's sha256 at the time of writing appended as `(<sha256>)`, so the line replays in the orchestrator's checkout before the boundary; (b) each finding's token, the first run of path characters, `:` and digits with an optional `-<digits>` range in the finding's line (backticks around it ignored, so `` `a.sh:1` `` and `resolve-threads.sh:48-52` both count), is compared with the findings of the task's earlier local review files (`.orchestration/validation/<task>-local-review-*.md` other than the current head's), each numbered as this script's own loop numbers them (`sort -u` order, P0 and P1 lines included); when an earlier finding has the same token and the record holds a row `local:<sha7'>:<n'><TAB><class>` for it with a class other than `advisory-p2`, the new row takes that class, the latest matching head's row winning when two earlier files match with different classes, and its `local-finding:` line's parenthesis gains `repeat of local:<sha7'>:<n'>` so the provenance is on the line; otherwise `advisory-p2`, as today. The scope is the local review files and the `local:` rows only: a repeat first classed by a Bot thread's row or an `audit:` row keeps `advisory-p2`, since those rows carry no `path:line` token (C-50's wider sentence is applied here to the one source that has tokens). Nothing else changes (the P0/P1 stop, the heading, the once-only writes).
2. `tests/unit/test_chain_review_scripts.py`: two new tests in the module's style (the temporary repository, the script as a subprocess): `test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file` (no owner file: exit 2, `write the owner task` on stdout or stderr, and the record byte-identical to what the case wrote before the run, so no heading and no row appeared; with the owner file: exit 0, the `local-finding:` line's evidence names `shasum -a 256 .orchestration/tasks/<owner>.md` and the file's actual sha256) and `test_local_advisory_classes_a_repeat_by_the_earlier_row` (two earlier review files: the older with a finding at `scripts/x.sh:12` whose record row carries the class `quoting`, the newer with the same token whose row carries `env-s-quoting`, and the older also with a finding at `scripts/y.sh:3-5` whose row carries `range-case`; a current review file with a P2 at `` `scripts/x.sh:12` `` in backticks, one at `scripts/y.sh:3-5` and one at another token: the new rows are `env-s-quoting` (the later head's class wins), `range-case` (the line-range token matches) and `advisory-p2` respectively, and the first two rows' `local-finding:` lines hold `repeat of local:<sha7'>:<n'>` naming the matched head and number; a review without findings and no owner file: exit 0 and no heading written).

## Out of scope

`local-review.sh` and `sandbox-scan.sh` (the a02 owner task's and the lineage's); the chain scripts that call this one (T7's `chain-integrate.sh`); the record's class table beyond the rows this script writes.

## Check

`uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` green (the module's tests and the two new ones), pasted in the validation file with `shellcheck scripts/orchestrator/local-advisory.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #376, the a02 owner task's PR, merged as f7847616 on 2026-10-17). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-chain-review-scripts-followup-a04`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md>` and the evidence paths.

## Owned row (2026-10-16T05:53:07Z)

`audit:40f3be4:2` (advisory P2 of PR #364's final head): `test_local_advisory_matches_the_owner_heading_literally` has no fixture that fails under an anchored regex match, so the literal match of the owner heading (df92b402) is not isolated; add the heading `tXfollowup-a01` against the owner id `t.followup-a01` and assert it does not match (the test module is in allowed_files).

## Change (premises, 2026-10-17T00:26:15Z, before dispatch)

PRs #364 (fdef3ceb) and #376 (f7847616) landed the a01 and a02 owner tasks' tests, so premise 4 records the module's fourteen tests and the Completion clause names the a02 PR's merge; the owned row `audit:40f3be4:2` (the heading-test fixture) was added on 2026-10-16 after the pair-confirmed hash `d6b2108b`. Nothing else changes from `33e1c301`; re-confirmed Codex first (C-54).

## Change (Completion, 2026-10-17T00:29:55Z, before dispatch)

The Codex half's re-confirm (P3): the Completion clause still read `bot_rounds=1`; it is now the task template's clause of 2026-10-16 (`open:<thread id>` with `bot_rounds=2`, the C-50 revise round, every other P2 advisory and owned by `dotfiles-T128-chain-review-scripts-followup-a04` under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in this task's acceptance record). Nothing else changes from `fd1f800a`.

