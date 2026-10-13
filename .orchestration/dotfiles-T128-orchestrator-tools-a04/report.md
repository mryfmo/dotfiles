# Report: dotfiles-T128-orchestrator-tools-a04

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts`, PR #336. a04 is a03's INV-6 reset (`reset_of: [dotfiles-T128-orchestrator-tools-a01, dotfiles-T128-orchestrator-tools-a03]`). It covers Bot review 5499708109 of `0d199475` and the orchestrator's local review of the same head.
- Task file sha256 `d0a26050…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-a04/task.md` in this head. The a01 and a03 copies are unchanged since `ba4d4762` (validation §1).
- Base: a fast-forward to the remote head `0d199475`, whose scripts and tests are byte-identical to `ba4d4762`, then `origin/main` (`d25c3df8`) merged in `3d131215`. The four fixes and six tests are one commit, `05e3292f`.

## The four fixes

| Thread | Finding | Disposition |
|---|---|---|
| 4255494133 (P2, `bus-read.sh:51`) | any member's RESULT or closing ACCEPTANCE with the task id closed the task | `fixed:05e3292f`. The open rule is now the stop gate's worker-seat branch (`scripts/agent-stop-gate.sh:283-297`). A task's latest opener (TASK, or ACCEPTANCE `status=revise`, X to Y) stays open until one of these comes later: a RESULT or a PONG `status=blocked` from Y to X, or an ACCEPTANCE from X to Y with any status but `revise`. Test: `test_bus_read_ignores_closers_between_other_endpoints` (mutants M3a, M3b) |
| 4255494139 (P2, `bus-read.sh:51`) | the closing-status whitelist omitted `closed-historical` | `fixed:05e3292f`. There is no whitelist: an absent status, `closed-historical`, `hold` and any other status close, and `revise` reopens. Test: `test_bus_read_closes_a_task_on_any_non_revise_acceptance` (M4, which restores the old whitelist) |
| 4255494137 (P2, `three-repeat.sh:41`) | `memory search` without `--limit` returns 30 rows at most, which were printed as the total | `fixed:05e3292f`. The search asks for `memory search --limit 1000 -- <class>` and prints `compactiondb: <class> -> >=1000 matches (capped)` when the count reaches the limit. A `search-body:` line (`/usr/bin/grep -rli`) is printed beside the unchanged `search:` line. Test: `test_three_repeat_prints_body_matches_and_states_a_capped_memory_count` (M6, M7, M8) |
| local review of `0d199475` (P2, `dispatch.sh:187`) | with a record that cannot be written, `agmsg-dispatch` sent first and `mkstemp` failed after | `fixed:05e3292f`. Before the send, the record must be an existing regular file, writable, in a writable directory. Otherwise the script prints `dispatch: the record <path> cannot be written`, exits 1 and sends nothing. Test: `test_dispatch_refuses_an_unwritable_record_before_sending` (M1: without the check, the stub is called) |

The other two tests the task names:

- `test_dispatch_refuses_a_malformed_record_block_before_sending` is table-driven: a block that is not an object, malformed JSON, a duplicate key, and a `dispatch` that is not a list. Each exits 1 with its message, and the stub is not called. Malformed JSON used to exit with a traceback; it now prints `the block is not valid JSON: …` (M2). The duplicate-key case that `test_dispatch_records_the_sent_line_with_its_read_marker` carried moved into this table.
- `test_bus_read_skips_and_counts_malformed_rows` covers one row of each rejected form around one open task. The forms are: a line not in row shape, another kind, no `v1`, `task_id=` missing, empty or repeated, `status=` repeated, and an unparsable `<at>`. Each of those rows would close the task if it counted. The task stays listed with `skipped=8`, and an empty history prints `skipped=0` (M5a to M5g).

## Choices the task left open

- three-repeat.sh prints its lines in this order: `search:`, `search-body:`, `compactiondb:`. A failed grep exits 1 after the lines of the searches before it, as the exit-code comment says.
- bus-read.sh:
  - It prints one `open:` line per task, as before. The task's latest opener between any two members sets X and Y, so a later `revise` from a third member resets the pair, as the task's rule reads.
  - `last_event` is still the task's latest counted row.
  - The limit check still counts the rows in row shape.
  - `skipped=` counts every non-empty line that is not a counted row, so the live read (validation §6) skips 45. By a one-off classification of the same history: 40 AGMSG-PING rows, 4 rows of other kinds (two `ctrl:despawn`, one AGMSG-NOTE, one body starting `T121`) and 1 row with a repeated `status=`.
  - Empty lines are not counted, so an empty history is not one skipped row.
- dispatch.sh refuses a missing record before the send, where a03 created a block in it. Since the record now always exists, the `record.exists()` branches in the recorder are gone.
- `scripts/regime-counters.sh` and its test are unchanged (item 3: "a04 adds no counters behaviour"). The ledger-row validation is `dotfiles-T128-orchestrator-tools-a02`'s.

## Results

- `test_orchestrator_tools.py`: 16 tests OK. `test_regime_counters`: 26 OK.
- shellcheck 0.11.0, shfmt 3.14.1 (`-i 4 -sr`, run from `$TMPDIR`; see sandbox) and ruff 0.17.0 are clean.
- Mutation proofs: 15 mutants, 15 failures, every file restored (validation §3, §5).
- The full discover in the sandbox fails only in eight modules this task does not touch, where the sandbox denies what the test needs (§4).
- Size (§3): 6 files outside `.orchestration/`; added lines outside and under `tests/`: 378 and 468 (caps 500 and 1000).

## Bot threads

The threads of a01 and a03 stand as their reports table them. The four findings above are `fixed:05e3292f`. The worker resolves no thread. The CI and the Bot on the pushed head are in the RESULT and in the main-checkout copy of this report.

## Not done, or outside scope

Nothing the task names is left undone. Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` in the main checkout printed `02822e62-4e86-4360-a142-3ccd2d6fc359`.

cost: n/a
