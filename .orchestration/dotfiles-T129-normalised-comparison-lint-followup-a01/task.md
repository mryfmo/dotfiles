---
format: 2
task_id: dotfiles-T129-normalised-comparison-lint-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/lint-comparisons.py
  - scripts/lint-comparisons-baseline.tsv
  - tests/unit/test_lint_comparisons.py
  - .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/**
after: []
threat_table:
  - control: the PR edits scripts/lint-comparisons.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits scripts/lint-comparisons-baseline.tsv only where a fix removes or adds a hit (item 1)
    disposition: "residual: one content-hashed row per hit on origin/main; the stale-row test fails on a row whose hit is gone, so the baseline follows the fixes and nothing else"
  - control: the PR edits tests/unit/test_lint_comparisons.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after; the audit reads each case against its row"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the lint as a subprocess (python3 -I) on fixture files in a temporary directory and on the checkout, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the lint runs where make unit-test runs, under the repository's python with -I, over the files git ls-files lists under home/, scripts/ and install/"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the three files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T129-normalised-comparison-lint-followup-a01 — the lint lineage's owner task (advisory P2 of PR #387)

Written 2026-10-17 by the orchestrator seat at the acceptance of PR #387's round 2 (C-51: the owner task exists before the first advisory row). It owns the advisory P2 rows recorded under `## Owned by dotfiles-T129-normalised-comparison-lint-followup-a01` in `.orchestration/acceptance/dotfiles-T129-normalised-comparison-lint-a01.md` (plan 020 step 1.2); it is dispatched after PR #387 merges, to a seat the orchestrator names then.

## Goal

Every owned row is fixed in `scripts/lint-comparisons.py` with one refusal fixture per row in `tests/unit/test_lint_comparisons.py`, red before and green after, and the baseline follows (a row whose hit disappears leaves; a hit the sharper rule newly finds in a file no task owns gets a row and a note in the RESULT); no other change.

## Files

1. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T12:3xZ): 4302629300 (`scripts/lint-comparisons.py:69`, class jq-program-location: a single-quoted jq option value before the program is read as the program; locate the program after the options and their arguments); 4302629305 (`:112`, class presence-not-structure: a `def` name inside a string literal on one side satisfies the per-side check; verify an application of the normaliser on each side, not a substring); 4302629307 (`:144`, class presence-not-structure: one `re.escape` accepts every interpolation of an f-string; every interpolated identifier must be escaped). Rows added to the record after this text was written are read from the record at dispatch.
2. The script stays at most 200 lines (D-cap-F2); `--list-rules` and the rule table of the lineage's task are unchanged.

## Out of scope

The baseline rows in files no task owns (their owner tasks are assigned at the lineage's acceptance from the RESULT's per-file list); any rule not named by an owned row; the omp hooks (PR B).

## Check

`uv run python -m unittest tests/unit/test_lint_comparisons.py -v` green and `uv run --no-project python -I scripts/lint-comparisons.py` (exit 0, no output) pasted in the validation file, with `ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines outside `tests/` and `.orchestration/` excluding `scripts/lint-comparisons-baseline.tsv`, and 1000 added lines under `tests/`; the script alone at most 200 lines.

## Completion

One PR from a fresh branch off `origin/main` after PR #387 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with this task's id as the owner of any advisory P2 (`dotfiles-T129-normalised-comparison-lint-followup-a02` is written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/task.md>` in the RESULT.

## Amendment 1 (round 1, 2026-10-18T09:07Z): this task supersedes PR #387 and lands as its own PR against main

PR #387 (the lint, head 7c8e7484) is at INV-6 S2 (revises 2, amendments 2) with a red CI and six Bot threads, so no round runs on it (plan 024 D-024 defaults, section 3 row #387). a008's branch `lint/normalised-comparisons-followup-a01` (445c32dd, code bb60ee84, stacked on 7c8e7484, the re-review round correct) carries the three owned rows fixed; the `gh pr create` that blocked it on 2026-10-17 no longer matches a live ask rule (D-024-13). The task continues as follows, in this order, each gh and git write a single command:
1. `git fetch origin main` and rebase the branch onto `origin/main` (68f8a70a or later; PR #387's commits come along, so the PR's diff against main is the whole F2 change) — a textual conflict is a `status=blocked` PONG, not a hand merge.
2. The CI red of #387: `tests/unit/test_lint_comparisons.py::test_the_tracked_tree_is_clean_against_the_baseline` fails because main gained hits after the baseline (`home/dot_claude/hooks/executable_project-map-reload.sh` and any other file the lint now lists on `origin/main`): run `uv run --no-project python -I scripts/lint-comparisons.py` on the rebased tree, add one content-hashed baseline row per hit in a file no in-flight task owns, and list them per rule and per file in the RESULT (the owner assignment is the orchestrator's); a hit in `scripts/lint-comparisons.py` or the tests is a fix, never a row.
3. The six Bot threads of #387: for each of 4302545078, 4302545082, 4302545085 (the review of 4b843ce9) and 4302629300, 4302629305, 4302629307 (the review of d215e062) the RESULT states `fixed:<sha>` with the commit on this branch (or on #387's) whose fixture closes it, verified by running that fixture; one that is not closed is fixed here with its red-then-green fixture (the owned-rows rule of item 1 widens to these six).
4. `gh pr create --base main --head lint/normalised-comparisons-followup-a01` (one plain command; a draft first, then `gh pr ready`), wait for CI and the automatic review (no `@codex review` comment), then `AGMSG-RESULT` with `pr=<new>`, `supersedes=387`, `task_copy=` and the per-thread dispositions; #387 is closed by the orchestrator when the new PR merges. The Check and caps of this task apply to the diff against `origin/main`, with the script at most 200 lines (D-cap-F2). INV-6 for this task: amendments 1, revises 0; a further amendment or a surviving P0/P1 is a hold and a reset.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-normalised-comparison-lint-followup-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a01.md
```
