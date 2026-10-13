---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a01
kind: code
security: false
reset_of: []
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/*
  - tests/unit/test_orchestrator_tools.py
  - scripts/regime-counters.sh
  - tests/unit/test_regime_counters.py
  - .orchestration/dotfiles-T128-orchestrator-tools-a01/**
after: []
threat_table:
  - control: the PR adds scripts/orchestrator/* (dispatch.sh, three-repeat.sh, bus-read.sh), scripts the orchestrator runs on the host against the bus and the learning records
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file"
  - control: the PR edits scripts/regime-counters.sh (its S1 line reads the class slug from the acceptance record's machine-readable block with jq, never a review-title substring)
    disposition: "residual: the diff touches only the S1 line's source and output form (a slug of [a-z0-9-] from the record's ledger; a title is printed only JSON-quoted in its own field); the orchestrator's diff review and the audit read it beside its test; the counting logic is untouched (INV-6)"
  - control: the PR edits tests/unit/test_regime_counters.py (the oracle of the S1 line)
    disposition: "residual: the orchestrator's diff review and the audit read the test beside the script; its fixture record and titles are data the test feeds the script"
  - control: the PR adds tests/unit/test_orchestrator_tools.py, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the tests beside the scripts; the tests run the scripts with stubbed git, gh, make and codex"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance)"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C6 before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: the worker's untrusted claims; acceptance re-checks each against the diff, CI and the test output"
  - control: in-process effects
    disposition: "residual: none: every script under test runs as a subprocess with stubbed binaries on PATH; nothing is imported into the test process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts resolve git (rev-parse --show-toplevel), /usr/bin/grep, shasum, jq, sort, date (coreutils), agmsg-dispatch and the agmsg history.sh or lib/storage.sh from the host as the SKILL's own commands do, and three-repeat.sh runs the repository's contextdb CLI with uv run --no-project (standard library only; no package resolved from the network, PR #329 thread 4250238721); the tests stub every host binary on PATH"
  - control: new or renamed scripts
    disposition: "residual: every new script is under scripts/orchestrator/, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: "the orchestrator's tooling lives in a session scratchpad, hand-typed per use; three recorded mistakes of 2026-10-12 come from that form"
    command: "grep -h '^id:\\|^artifact:' .orchestration/learning/mistakes/M-20261012-11.md .orchestration/learning/mistakes/M-20261012-12.md .orchestration/learning/mistakes/M-20261012-13.md"
    output: |-
      id: M-20261012-11
      artifact: "boundary commit 2026-10-12 (4): the amend chain of 10:55Z in worktree boundary-2026-10-12-4"
      id: M-20261012-12
      artifact: "design-review round 20 and the Phase 1 task-file review, Codex halves (headless codex exec runs of 11:11Z and 11:15Z)"
      id: M-20261012-13
      artifact: "design v19 (dotfiles-T128-regime-v3-a01, round 21): the INV-6 clause appended to INV-4"
  - claim: "the counters' S1 candidate line prints review-title words, not a ledger slug (PR #328 thread 4250028600)"
    command: "git grep -n 'class=' origin/main -- tests/unit/test_regime_counters.py"
    output: "origin/main:tests/unit/test_regime_counters.py:451:            [\"S1: candidate class=reject skipped contract count=3 source=fixture\"],"
  - claim: "the input copies of the scratchpad tools are attached beside this task"
    command: "ls .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/"
    output: |-
      boundary.sh
      codex-review-prompt-example.txt
      design-keydiff.py
      ff-main.sh
      fill_sweep.py
      orch-audit.sh
      orch-gate.sh
      t717-prep.sh
---

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a01 — the three scripts T703's rule text names, and the counters' class slug (plan 007 T718, first slice under plan 012 B; C-20, C-23, C-25)

Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T718, approved with plan 010 D) and re-scoped 2026-10-13 under plan 012 option B. Review tier by INV-1 (`kind: code`; `scripts/orchestrator/` is on no design-tier list; the gate and the audit runner themselves are untouched). Runs before `dotfiles-T128-playbook-rules-a04` merges (plan 012 B: mechanism before rule text, C-21, C-25): the a04 sentences "Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` …" and the counter trigger become true when this PR merges. The other nine scripts of the original scope are `dotfiles-T128-orchestrator-tools-a02`. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C6 pass on this file.

## What to do

1. Create `scripts/orchestrator/` with these three scripts, shdoc comments in English, every path a parameter or derived from `git rev-parse --show-toplevel` (no session scratchpad path, no home directory literal; the agmsg scripts directory defaults to `$HOME/.agents/skills/agmsg/scripts` and is overridable with `AGMSG_SCRIPTS`):
   - `dispatch.sh <team> <from> <to> <pane> <line-file>`: reads a TASK or ACCEPTANCE line from a file, recomputes every `*_sha256=` field from the file each names (`task_file=`, `design=`, `amended_task=`), exits non-zero naming the field on a mismatch, otherwise calls `agmsg-dispatch` (C-20).
   - `three-repeat.sh <class>`: validates the class against `^[a-z0-9-]+$` (exit 2 otherwise), runs `grep -rl` over `.orchestration/learning/mistakes/` for `classes:.*<class>` and the CompactionDB memory search without a shell, and prints the record's `search: <class> -> <sorted basenames or none>` line and the CompactionDB count (C-23; the T703 Bot threads 4249303433, 4249303398).
   - `bus-read.sh <team> [<task id>]`: a complete bus read (`history.sh --limit 1000` or `lib/storage.sh`'s `storage_history`, never the database file) that prints every open TASK without a RESULT and, per task, the minutes since its latest bus event (C-23; threads 4249303413, 4249303426).
2. `tests/unit/test_orchestrator_tools.py`: with stubbed `agmsg-dispatch`, `shasum`, `history.sh` and `uv` on PATH: `test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file` (the exact closed-row name; the stub records no call), the dispatch happy path passes the line byte-identical to the stub, `three-repeat.sh` exits 2 for `Reject skipped contract` and for `a;b` and prints `search: <class> -> <sorted basenames or none>` from a fixture records directory, and `bus-read.sh` lists an open TASK without a RESULT with its minutes since the latest event from a fixture history.
3. `scripts/regime-counters.sh`: the S1 line reads the task's acceptance record `.orchestration/acceptance/<task>.md` when it exists: the machine-readable block between its first two `---` lines is a JSON object (the `dotfiles-T128-gate-evidence-a03` contract as plan 013 A′ amends it; `ledger` is a list of `{id, class}`), read with `jq` only, never with grep or sed over the prose. For every class with three or more ledger rows it prints `S1: class=<slug> count=<n> source=record`, the slug matching `^[a-z0-9-]+$`. Without a record, the Bot-title grouping stays a candidate detector and prints `S1: candidate class=unclassified count=<n> title=<the title as a JSON string from jq> source=<s>`, a field no procedure substitutes into a command (plan 010 D; threads 4249303433, 4250028600). `tests/unit/test_regime_counters.py`: a fixture record with one class at three (the slug line), a title with backticks and `$()` without a record (quoted, `class=unclassified`), and line 451's expectation updated.
4. Keep the two checkers out (T704 owns `ledger-check.py` and `task-consistency-check.py`) and the other nine scripts out (`dotfiles-T128-orchestrator-tools-a02`). Keep the attached inputs untouched; they are evidence of what ran on 2026-10-12.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v` output in the validation file.
- `shellcheck scripts/orchestrator/*.sh` output if shellcheck is on PATH (state it if not).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`); split into two PRs if the caps are exceeded and say so in the RESULT.

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/orchestrator-scripts`, draft PR from `origin/main`. After the merge the orchestrator dispatches only through `dispatch.sh` and searches only through `three-repeat.sh`; PR #328 takes the new base with `gh pr update-branch`.
