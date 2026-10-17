---
format: 2
task_id: dotfiles-T128-seat-liveness-followup-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - tests/unit/test_herdr_agents.py
  - .orchestration/dotfiles-T128-seat-liveness-followup-a01/**
after: [dotfiles-T128-seat-liveness-a01]
threat_table:
  - control: the PR edits home/dot_local/bin/common/executable_herdr-agents only within the owned rows (item 1), the two failure edges of the --stale path PR #367 landed (the archive destination checked before any cleanup; no identity row refuses and closes nothing)
    disposition: "closed: tests/unit/test_herdr_agents.py::test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows"
  - control: the PR edits tests/unit/test_herdr_agents.py (one new test beside the lineage's, which stay as they are; the module's seat fakes answer as in PR #367's tests)
    disposition: "residual: the fakes record and answer, nothing else; the audit reads the cases against item 1"
  - control: "the --stale path's side effects (delivery off, leave, the record moved, the standalone workspace closed): each happens only after the archive destination was checked (an existing non-directory `run/stale`, or a run directory that is not writable, refuses) and at least one identity row was read and found gone"
    disposition: "residual: a non-directory archive destination or an unwritable run directory refuses before any cleanup; no identity row refuses before any cleanup and closes no workspace; the closed row's three cases cover a non-directory destination, an unwritable run directory and no identity row, and each asserts the record untouched and the workspace still listed; the despawn path and the lineage's tests are unchanged"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-seat-liveness-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-seat-liveness-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the test module runs the launcher as a bash subprocess with HOME set to a temporary tree holding the fake agmsg scripts and a fake herdr, and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the launcher runs bash, git, mkdir, mv and the agmsg scripts under HOME/.agents/skills/agmsg/scripts by that fixed path, as today; the tests' seam is HOME; a PR checkout as cwd chooses nothing"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the owned rows are in the lineage record''s owner section on origin/main at dispatch (present since boundary (16), PR #373 merged as 1d418126 on 2026-10-16)'
    command: 'git show origin/main:.orchestration/acceptance/dotfiles-T128-seat-liveness-a01.md 2>/dev/null | /usr/bin/grep -c "^audit:d3bc745:" || true'
    output: |-
      6
  - claim: 'the launcher on origin/main carries PR #367''s --stale path (present since the merge of 2026-10-15 08:28Z)'
    command: 'git show origin/main:home/dot_local/bin/common/executable_herdr-agents | /usr/bin/grep -c -e "--stale" || true'
    output: |-
      7
---

# AGMSG-TASK dotfiles-T128-seat-liveness-followup-a01 — the two failure edges of the launcher's `--stale` path (the owner task of the seat-liveness lineage; the audit of PR #367's d3bc745 and its local review)

Written 2026-10-15 by the orchestrator seat (the bus time of its TASK line is the dispatch time), pair-reviewed before dispatch; dispatched only after PR #367 merges and boundary (16) puts the rows on `origin/main` (both premises then read `1` or more). The audit of PR #367's round-2 head d3bc745 and the chain's local review of it left two P2 on the new `--stale` path of `herdr-agents --remove-worker`: (1) when `identities.sh` enumerates no row (an enumeration failure), `seat_rows` is empty, the leader and pane-state checks are skipped, and `--stale` still closes the matching standalone worker workspace with exit 0 (line 1975) without establishing `gone`; (2) the archive destination `run/stale/` is prepared after `leave.sh` removed the identity (lines 1964-1966), so when it cannot be created, or is a regular file, the identity is gone while the placement record stays under `spawn.*`, undiscoverable through identities; the remedy checks the destination before any cleanup and leaves the `mkdir -p` at the move, so the lineage's own test (no `stale/` after a failed `leave.sh`) stands. The rows are `audit:d3bc745:1` (class `stale-no-identity-rows`), `audit:d3bc745:2` and `local:d3bc745:1` (class `stale-dir-order`, one defect) under `## Owned by dotfiles-T128-seat-liveness-followup-a01` in `.orchestration/acceptance/dotfiles-T128-seat-liveness-a01.md`. A third revise round on PR #367 would have reached INV-6's revise threshold (two), so under plan 020 step 4 the rows came here.

## What to do

1. The owned rows, in `--stale` mode only (the despawn path unchanged): (a) when the identity enumeration yields no row for the worktree, refuse (stderr `herdr-agents: no seated identity at <worktree>; nothing retired`, exit 2) and close no workspace or tab, before the state loop; (b) after the state loop and before the first `delivery.sh` call, check the archive destination without creating it (every seat that reaches this point has a placement record: `seat_pane_state` answers `unknown` without a readable one and the state loop already refused): refuse (stderr `herdr-agents: <run dir>/stale is not a directory, or <run dir> is not writable; nothing retired`, exit 1) when `<run dir>/stale` exists and is not a directory, or when the run directory is not writable; the `mkdir -p` stays at the move, so a refused run creates nothing. Failure modes stated: both refusals happen before `delivery.sh`, `leave.sh`, the record move and any `herdr` call, and a refusal leaves no `stale/` behind (the lineage's test that asserts its absence after a failed `leave.sh` stands).
2. One test, `test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows`, in the module's style: case one, `run/stale` pre-created as a regular file: exit 1, the stderr line, no `delivery`, `leave`, `despawn` or `workspace close` call (the identity and workspace lookups precede the refusal, as in the lineage's first stale test), the record byte-identical and the workspace still listed; case two, the fake `identities.sh` printing nothing for the worktree: exit 2, the stderr line, no `delivery`, `leave`, `despawn` or `workspace close` call, the record byte-identical and the workspace still listed; case three, the run directory made read-only (`chmod 0500`, restored by the test's cleanup) with `run/stale` absent: exit 1, the stderr line, no such call, the record byte-identical, the workspace still listed and no `stale/` created; the lineage's tests stay as they are.
3. Nothing else changes: no file outside the two, no behaviour the rows do not name.

## Validation

- `uv run python -m unittest tests/unit/test_herdr_agents.py -v` in the validation file, with the new test named; `shellcheck home/dot_local/bin/common/executable_herdr-agents`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after PR #367 merged as 2c9b10e9 and boundary (16), PR #373 merged as 1d418126). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-seat-liveness-followup-a02`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-seat-liveness-followup-a02` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names per row, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-seat-liveness-followup-a01/task.md>` and the evidence paths. After the merge the operator runs `make update` (the launcher lives under `home/`).

## Change (round 2, 2026-10-15 09:5xZ)

The review seat's round 1 (P2, four P3) and the Codex half's (P2, P3): the archive destination is checked, not created, before the first cleanup call (so the lineage's test asserting no `stale/` after a failed `leave.sh` stands); the check sits after the no-row refusal and the state loop and applies to a seat with a placement record; both test cases assert the record byte-identical and the workspace still listed and name the four calls; premise 2 regenerated (the path is on origin/main since PR #367's merge, count 7); the record's row class aligned.

## Change (round 3, 2026-10-15 10:0xZ)

The Codex half's round 2 (two P2; the review seat confirmed round 2): the record-less sentence is gone (the state check already refuses a seat without a readable record, so every seat reaching the destination check has one); a third test case exercises the unwritable-run-directory refusal.

## Change (premises, 2026-10-16T06:27:52Z, before dispatch)

Boundary (16) (PR #373, merged as 1d418126 on 2026-10-16) landed the owner section on `origin/main`, so the premise that waited for it now records the post-boundary output that `presend.sh` replays at dispatch; its claim says so. Nothing else changes from the pair-confirmed hash `1b64dca6`; re-confirmed Codex first (C-54).

## Change (Completion, 2026-10-16T08:44:50Z, before dispatch)

The review seat's round on the premise change (P2, P3): the Completion clause still had the single-review form written before T13's amendment 6 (no `open:<thread id>`, no `bot_rounds=2`, "every P2 as advisory", the pre-C-51 owner wording). It is now the task template's clause of 2026-10-16 (`.orchestration/templates/task-short.md`, Completion): the Bot's review at PR open and once more on `@codex review` after a P0/P1 fix round, a surviving P0/P1 listed as `open:<thread id>` with `bot_rounds=2`, the C-50 revise round for a small in-scope P2, every other P2 advisory and owned by `dotfiles-T128-seat-liveness-followup-a02` (written when the first advisory P2 appears, C-51) under `## Owned by dotfiles-T128-seat-liveness-followup-a02` in this task's acceptance record. Nothing else changes from `23d3ed55`; re-confirmed Codex first (C-54). The Codex half's round 5 (2026-10-16T09:00:01Z): the replacement had dropped the lineage's post-merge `make update` sentence (the brief's stop condition 3); restored verbatim from the clause on origin/main.

