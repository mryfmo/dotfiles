---
format: 2
task_id: dotfiles-T128-chain-github-scripts-followup-a02
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/resolve-threads.sh
  - tests/unit/test_chain_github_scripts.py
  - .orchestration/dotfiles-T128-chain-github-scripts-followup-a02/**
after: [dotfiles-T128-chain-github-scripts-followup-a01]
threat_table:
  - control: the PR edits scripts/orchestrator/resolve-threads.sh only within the owned row (item 1), refusing before any GitHub call a disposition, from the TSV or from the sweep JSON, that the reply template cannot carry losslessly (a backtick), with one clause in its shdoc description and @exitcode 2 line
    disposition: "closed: tests/unit/test_chain_github_scripts.py::test_resolve_threads_refuses_a_disposition_the_reply_cannot_carry"
  - control: the PR edits tests/unit/test_chain_github_scripts.py (one new test beside the lineage's, which stay as they are; the stub gh records every call and the test asserts none is made on a refusal, for a TSV disposition and for a sweep-JSON one; run_script gains a keyword that also returns stderr, the existing calls unchanged)
    disposition: "residual: the stub records and answers, nothing else; the audit reads the case against item 1"
  - control: "the PR review threads on GitHub and the sweep JSON fill_sweep.py reads back from the replies: a disposition that fill_sweep.py would truncate (a backtick: the reader's code span ends at it; a newline is read back whole, so it is not refused), whichever of the two sources it comes from, never reaches a reply, so the evidence saved from a reply is never shorter than the disposition the orchestrator wrote"
    disposition: "residual: the refusal exits before any gh call and names the id, so the orchestrator rewrites the disposition (evidence commands quote without backticks); the closed row's cases cover a TSV backtick and a sweep-JSON backtick, and the unchanged lineage tests cover the posting path"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-chain-github-scripts-followup-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run resolve-threads.sh as a subprocess with a stub gh first on PATH in a temporary directory and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; resolve-threads.sh runs gh, jq and the coreutils by name from PATH as today (the test seam is PATH with the stub gh); it reads the dispositions TSV and the sweep JSON by the two paths its caller passes, with no path check of its own (as today): the orchestrator passes files of its own checkout, and the chain never passes a PR checkout's path"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the owned row is in the lineage record''s owner section on origin/main at dispatch (present since boundary (16), PR #373 merged as 1d418126 on 2026-10-16: the row was added on 2026-10-15 after the audit of e9404a6)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md 2>/dev/null | /usr/bin/grep -c "^audit:e9404a6:1	disposition-backtick-truncation" || true'
    output: |-
      1
  - claim: 'the five other rows of the section are closed by PR #360 and marked so in the record on origin/main at dispatch (the fixed lines were added on 2026-10-15 and landed with boundary (16), PR #373)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md 2>/dev/null | /usr/bin/grep -c "fixed in PR #360" || true'
    output: |-
      5
  - claim: 'resolve-threads.sh on origin/main backticks the disposition in both reply sentences and refuses nothing about its content'
    command: 'git show origin/main:scripts/orchestrator/resolve-threads.sh | /usr/bin/grep -c "cannot carry it losslessly"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-chain-github-scripts-followup-a02 — resolve-threads.sh refuses a disposition the reply template cannot carry losslessly (the second owner task of the chain-github-scripts lineage; plan 020 step 1; the audit of e9404a6, PR #360)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch; dispatched after boundary (16) (PR #373, merged as 1d418126 on 2026-10-16) put the row and the five `fixed in PR #360` lines on `origin/main` (both premises read `1` and `5`, the outputs recorded above). The audit of PR #360's head e9404a6 (finding 1, P2, `resolve-threads.sh:57`): the reply template wraps the disposition in backticks, the form `fill_sweep.py`'s reader takes back from the thread; a disposition that itself holds a backtick (an evidence command such as ``rg 'uses `example`' README.md``) is cut at the embedded backtick when read back, `fill_sweep.py` reports `filled 1 gaps 0`, and the saved evidence is shorter than what the orchestrator wrote. The row is `audit:e9404a6:1` (class `disposition-backtick-truncation`) under `## Owned by dotfiles-T128-chain-github-scripts-followup-a01` in `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md`; the five rows above it are closed by PR #360 and carry a `fixed in PR #360` line each.

## What to do

1. The owned row: `resolve-threads.sh` scans the two local sources before any `gh` call (the thread set is known only after the first query, so the scan reads every TSV first column and every sweep JSON item whose url ends in `_r<id>`, and a disposition for an id outside this run's unresolved threads refuses too, fail closed): every disposition of the TSV and every `disposition` of such a sweep item; it refuses the run (exit 2, stderr `resolve-threads: disposition for <id> holds a backtick; the reply cannot carry it losslessly`) when one holds a backtick; nothing is posted or resolved for any thread of that run. The shdoc header's description and its `@exitcode 2` line each gain one clause naming the refusal (item 3 does not forbid the header edit). The reply template, the resolve mutation and the summary line stay as PR #360 left them. A newline is not refused: a TSV row cannot hold one (one record per line) and the landed reader reads a sweep-sourced newline back whole. Failure mode stated: clean sources behave as today; one bad disposition changes nothing on GitHub (fail closed).
2. One test, `test_resolve_threads_refuses_a_disposition_the_reply_cannot_carry`, in the module's style (the stub `gh` first on PATH recording every call), with two cases: a TSV whose second row's disposition holds a backtick; and a TSV without a row for the thread with a sweep JSON whose item's disposition holds a backtick: each exits 2, the stderr line names the id, and the stub recorded no call; `run_script` gains a keyword argument that also returns stderr (its existing calls unchanged), or the test runs `subprocess.run` directly; the lineage's tests stay as they are.
3. Nothing else changes: no file outside the two, no behaviour the row does not name.

## Validation

- `uv run python -m unittest tests/unit/test_chain_github_scripts.py -v` in the validation file, with the new test named; `shellcheck scripts/orchestrator/resolve-threads.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after boundary (16), PR #373 merged as 1d418126). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-chain-github-scripts-followup-a03`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-chain-github-scripts-followup-a03` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-github-scripts-followup-a02/task.md>` and the evidence paths.

## Change (round 2, 2026-10-15 07:2xZ)

The Codex half's round 1 (P1): the refusal covered the TSV dispositions only while resolve-threads.sh also posts dispositions read from the sweep JSON (the `-` form); item 1, item 2 (a third case) and the first and third threat rows now cover both sources (the TSV row, else the sweep JSON item).

## Change (round 3, 2026-10-15 07:3xZ)

The review seat's rounds 1 and 2 (P2, three P3): the newline leaves the refusal (a TSV row cannot hold one; the reader reads a sweep-sourced newline back whole), only the backtick is refused; the scan reads the two local sources' ids before the first query and refuses an unknown id too; the shdoc description and `@exitcode 2` line gain a clause; `run_script` gains a stderr-returning keyword. The Codex half confirmed round 2.

## Change (round 4, 2026-10-15 07:5xZ)

The Codex half's round 3 (P2): the environment row had claimed the script never reads a PR checkout's files as if the script checked its paths; it reads the two paths its caller passes with no check of its own, and the row now says so (the orchestrator passes its own checkout's files). The review seat confirmed round 3.

## Change (premises, 2026-10-16T06:25:31Z, before dispatch)

Boundary (16) (PR #373, merged as 1d418126) landed the lineage record's owned row and the five `fixed in PR #360` lines on `origin/main`, so premises 1 and 2 now record the post-boundary outputs (1 and 5) that `presend.sh` replays at dispatch; their claims say so. Nothing else changes from the pair-confirmed hash `5d3b78db`; re-confirmed Codex first (C-54). The Codex half's round 5 (2026-10-16T08:26:10Z): the introduction had still called the recorded outputs pre-boundary values; it now names the boundary and the recorded values.

## Change (Completion, 2026-10-16T08:44:50Z, before dispatch)

The review seat's round on the premise change (P2, P3): the Completion clause still had the single-review form written before T13's amendment 6 (no `open:<thread id>`, no `bot_rounds=2`, "every P2 as advisory", the pre-C-51 owner wording). It is now the task template's clause of 2026-10-16 (`.orchestration/templates/task-short.md`, Completion): the Bot's review at PR open and once more on `@codex review` after a P0/P1 fix round, a surviving P0/P1 listed as `open:<thread id>` with `bot_rounds=2`, the C-50 revise round for a small in-scope P2, every other P2 advisory and owned by `dotfiles-T128-chain-github-scripts-followup-a03` (written when the first advisory P2 appears, C-51) under `## Owned by dotfiles-T128-chain-github-scripts-followup-a03` in this task's acceptance record. Nothing else changes from `8ce7462f`; re-confirmed Codex first (C-54).

