---
format: 2
task_id: dotfiles-T128-orchestrator-tools-a03
kind: code
security: false
reset_of: [dotfiles-T128-orchestrator-tools-a01]
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/*
  - tests/unit/test_orchestrator_tools.py
  - scripts/regime-counters.sh
  - tests/unit/test_regime_counters.py
  - .orchestration/dotfiles-T128-orchestrator-tools-a03/**
after: []
threat_table:
  - control: the PR adds scripts/orchestrator/dispatch.sh, which sends a bus line whose *_sha256 fields it recomputes from the files they name
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file"
  - control: dispatch.sh sends a TASK whose hash field is absent, or a line file with more than one physical line (PR #336 threads 4254163604, 4254107304)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line"
  - control: dispatch.sh sends a line whose task_id= is missing, empty or repeated, or records such a line against an acceptance record (PR #336 thread 4254893065: the malformed-identity path)
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_refuses_a_line_without_a_task_id"
  - control: "dispatch.sh, given an acceptance record path, reads that record's JSON block, reads the bus marker through history.sh, and rewrites the record's dispatch list after the send (a gate input mutated by the orchestrator's tooling; PR #336 thread 4254494999); the controls it keeps: the path is an argument the orchestrator passes, the block is read with object_pairs_hook (a duplicate key refuses), only the dispatch list changes, the file is written whole with sort_keys and indent=2, and the gate of dotfiles-T128-gate-evidence-a04 re-validates the block"
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_dispatch_records_the_sent_line_with_its_read_marker"
  - control: the PR adds scripts/orchestrator/three-repeat.sh, which runs the records search and the CompactionDB CLI from the orchestrator host
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout"
  - control: the PR adds scripts/orchestrator/bus-read.sh, which reads the bus history through the agmsg scripts and prints open TASKs
    disposition: "closed: tests/unit/test_orchestrator_tools.py::test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event"
  - control: the PR edits scripts/regime-counters.sh (its S1 line reads the class slug from the acceptance record's machine-readable block with jq, never a review-title substring)
    disposition: "residual: the diff touches only the S1 line's source and output form (a slug of [a-z0-9-] from the record's ledger; a title is printed only JSON-quoted in its own field); the orchestrator's diff review and the audit read it beside its test; the counting logic is untouched (INV-6)"
  - control: the PR edits tests/unit/test_regime_counters.py (the oracle of the S1 line)
    disposition: "residual: the orchestrator's diff review and the audit read the test beside the script; its fixture record and titles are data the test feeds the script"
  - control: the PR adds tests/unit/test_orchestrator_tools.py, the oracle of its own change
    disposition: "residual: the orchestrator's diff review and the task-level audit from main read the tests beside the scripts; the tests run the scripts with stubbed git, gh, make and codex"
  - control: the task-file copy of a01 on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a01/task.md), kept as history
    disposition: "residual: the copy is byte-identical to the a01 file as dispatched at amendment 1 (its sha256 is in a01's acceptance record); it is not edited under a03"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-orchestrator-tools-a03/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched task file (sha256 in the worker's validation file, compared at acceptance); the reset record names the a03 file's hash and the review seat's verdict=accept on it"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: the branch evidence records under .orchestration/dotfiles-T128-orchestrator-tools-a03/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
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

# AGMSG-TASK dotfiles-T128-orchestrator-tools-a03 (the INV-6 reset of a01, 2026-10-13, after a01 amendment 1 and thread 4254494999; `-a02` is T718's second slice, not a predecessor) — the three scripts T703's rule text names, and the counters' class slug (plan 007 T718, first slice under plan 012 B; C-20, C-23, C-25)

Written 2026-10-13 by the review seat as a01's INV-6 reset (redesign task `dotfiles-T128-orchestrator-tools-redesign-a01`), under the reset record the orchestrator writes for a01 (`.orchestration/acceptance/dotfiles-T128-orchestrator-tools-a01-design-reset.md`, as the gate-evidence lineage names them). The Codex Bot's review of PR #336's amendment-1 head `5ec05d8d` left thread 4254494999 (P1): amendment 1 made `dispatch.sh` read a caller-selected acceptance record, inspect bus output and rewrite the record after the send, while the dispatch rows covered only the hash check and malformed lines; the row is task text, a01 already carried amendment 1 and one question (counters at 04:14Z: `tasks=2 amendments=1 questions=1 results=2 revises=1`), so a second amendment is INV-6's reset. a03 is a01 amendment 1 plus that one threat row, closed by `test_dispatch_records_the_sent_line_with_its_read_marker`, a test the head `5ec05d8d` already carries; nothing else changes. `dotfiles-T128-orchestrator-tools-a02` is T718's second slice (the other nine scripts), not a predecessor of this lineage. The worker's commits (`2dddff84`, `0a5ae302`, `374fc171`, `b80b03ee`, `77e75595`, `5ec05d8d`) stay; the same worker (`claude-standard-dot-a003`) continues on PR #336 under a03.

History (a01). Written 2026-10-12 by the orchestrator seat under plan 007 (Phase 5, T718, approved with plan 010 D) and re-scoped 2026-10-13 under plan 012 option B. Review tier by INV-1 (`kind: code`; `scripts/orchestrator/` is on no design-tier list; the gate and the audit runner themselves are untouched). Runs before `dotfiles-T128-playbook-rules-a04` merges (plan 012 B: mechanism before rule text, C-21, C-25): the a04 sentences "Once plan 007 T718 lands, `scripts/orchestrator/three-repeat.sh <class>` …" and the counter trigger become true when this PR merges. The other nine scripts of the original scope are `dotfiles-T128-orchestrator-tools-a02`. The threat table names every `allowed_files` entry plus the non-path controls; `task-consistency-check.py` C1 to C10 and C7b pass on this file.

## What to do

1. Create `scripts/orchestrator/` with these three scripts, shdoc comments in English, every path a parameter or derived from `git rev-parse --show-toplevel` (no session scratchpad path, no home directory literal; the agmsg scripts directory defaults to `$HOME/.agents/skills/agmsg/scripts` and is overridable with `AGMSG_SCRIPTS`):
   - `dispatch.sh <team> <from> <to> <pane> <line-file> [<acceptance-record>]`: reads exactly one physical line (a TASK, ACCEPTANCE or PING; a second line, blank or not, is refused: thread 4254107304), recomputes every `*_sha256=` field from the file each names (`task_file=`, `design=`, `amended_task=`), exits non-zero naming the field on a mismatch, refuses an `AGMSG-TASK` line without a `task_file=` and a 64-hex `task_sha256=` (thread 4254163604), otherwise calls `agmsg-dispatch`; when an acceptance record path is given it appends, after the send, the string `<the line as sent> read_at=<read_at from the bus through history.sh, or unread>` to the `dispatch` list of the record's JSON block (the object between the record's first two `---` lines, as `dotfiles-T128-gate-evidence-a04` defines it; the key is created when absent, and a record without a block gets one holding only `dispatch`), read and written with the standard library's json (`object_pairs_hook` refusing duplicate keys, `sort_keys`, `indent=2`): the literal `dispatch:` key the a04 rule sentence names (thread 4254107312) (C-20).
   - `three-repeat.sh <class>`: validates the class against `^[a-z0-9-]+$` (exit 2 otherwise), runs `grep -rl` over `.orchestration/learning/mistakes/` for `classes:.*<class>` and the CompactionDB memory search without a shell, both resolved from the script's own checkout (`git -C "$(dirname "$0")" rev-parse --show-toplevel`), never from the caller's working directory, so a PR worktree cannot substitute its own `.claude/hooks/contextdb_cli.py` (thread 4253994697), and prints the record's `search: <class> -> <sorted basenames or none>` line and the CompactionDB count (C-23; the T703 Bot threads 4249303433, 4249303398).
   - `bus-read.sh <team> [<task id>]`: a complete bus read (`history.sh --limit 1000` or `lib/storage.sh`'s `storage_history`, never the database file) that prints every open TASK without a RESULT and, per task, the minutes since its latest bus event (C-23; threads 4249303413, 4249303426).
2. `tests/unit/test_orchestrator_tools.py`: with stubbed `agmsg-dispatch`, `shasum`, `history.sh` and `uv` on PATH: `test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file`, `test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line` and `test_dispatch_refuses_a_line_without_a_task_id` (a missing, empty or repeated `task_id=` is refused before any hash or record work; the exact closed-row names; the stub records no call), the dispatch happy path passes the line byte-identical to the stub, and `test_dispatch_records_the_sent_line_with_its_read_marker` (the closed-row name of the record row) appends the sent line with its read marker to the `dispatch` list of a record's JSON block when a record is given and re-reads the block with the gate's loader, `test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout` (exit 2 for `Reject skipped contract` and `a;b`; the CLI path the stub sees is under the script's checkout, not the test's cwd), `test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event`, `three-repeat.sh` exits 2 for `Reject skipped contract` and for `a;b` and prints `search: <class> -> <sorted basenames or none>` from a fixture records directory, and `bus-read.sh` lists an open TASK without a RESULT with its minutes since the latest event from a fixture history.
3. `scripts/regime-counters.sh`: the S1 line reads the task's acceptance record `.orchestration/acceptance/<task>.md` when it exists: the machine-readable block between its first two `---` lines is a JSON object (the `dotfiles-T128-gate-evidence-a03` contract as plan 013 A′ amends it; `ledger` is a list of `{id, class}`), read with `jq` only, never with grep or sed over the prose. For every class with three or more ledger rows it prints `S1: class=<slug> count=<n> source=record`, the slug matching `^[a-z0-9-]+$`. Without a record, the Bot-title grouping stays a candidate detector and prints `S1: candidate class=unclassified count=<n> title=<the title as a JSON string from jq> source=<s>`, a field no procedure substitutes into a command (plan 010 D; threads 4249303433, 4250028600). `tests/unit/test_regime_counters.py`: a fixture record with one class at three (the slug line), a title with backticks and `$()` without a record (quoted, `class=unclassified`), and line 451's expectation updated.
4. Keep the two checkers out (T704 owns `ledger-check.py` and `task-consistency-check.py`) and the other nine scripts out (`dotfiles-T128-orchestrator-tools-a02`). Keep the attached inputs untouched; they are evidence of what ran on 2026-10-12.

## Validation

- `uv run --no-project python -m unittest tests/unit/test_orchestrator_tools.py -v` output in the validation file.
- `shellcheck scripts/orchestrator/*.sh` output if shellcheck is on PATH (state it if not).
- `git diff --numstat origin/main...HEAD` in the validation file (INV-2 caps: at most 15 changed files outside `.orchestration/`, 500 added lines outside `tests/`, 1000 under `tests/`); split into two PRs if the caps are exceeded and say so in the RESULT.

## Completion

The PR is ready for the orchestrator's integration when CI is green, the Bot wait of Worker Playbook step 15 is done, the validation file carries the outputs above, and the RESULT names every unresolved Bot thread with `fixed:<sha>` or a proposed `not-applicable:<reason>; evidence=<command>`. Branch `tools/orchestrator-scripts`, PR #336 (open since a01, continued from the amendment-1 head `5ec05d8d`; the PR stays open: the worker adds the a03 task copy and evidence under `.orchestration/dotfiles-T128-orchestrator-tools-a03/`, no other change expected). After the merge the orchestrator dispatches only through `dispatch.sh` and searches only through `three-repeat.sh`; PR #328 takes the new base with `gh pr update-branch`.

## History: a01 amendment 1 (orchestrator, 2026-10-13 02:5xZ; a03's base)

The Codex Bot's review of PR #336 (threads 4253994704 on this task's threat row, 4253994697, 4254107304, 4254107312, 4254163604 on the scripts) changes the threat table and items 1 and 2, nothing else: one row per script, each closed by a named test; `dispatch.sh` reads exactly one physical line, refuses a TASK without `task_file=` and `task_sha256=`, and records the sent line with its read marker under the record's JSON block `dispatch` key when given one; `three-repeat.sh` resolves the records directory and the CompactionDB CLI from its own checkout. The worker's commits (`61290da8`, `4843ccb6`, `5b6d5f24`) stay; what they already implement of this counts.

## Amendment 1 (orchestrator, 2026-10-13 05:1xZ)

The Codex Bot's thread 4254893065 on the a03 head `c8fb09b0` (a line without `task_id=` is sent and, with a record, skips the association check; the threat table has no row for that path): one row added for the malformed-identity path, closed by `test_dispatch_refuses_a_line_without_a_task_id`, and that test named in item 2. The code fix is the worker's revise of the same thread; nothing else changes.
