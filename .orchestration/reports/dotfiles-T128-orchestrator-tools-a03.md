# Report: dotfiles-T128-orchestrator-tools-a03

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, branch `tools/orchestrator-scripts`, PR #336, continued from a01 amendment 1's head `5ec05d8d`. a03 is a01's INV-6 reset (`reset_of: [dotfiles-T128-orchestrator-tools-a01]`) after thread 4254494999.
- Task file sha256 `b7348b8a…` matches the TASK's `task_sha256`. It is copied byte-identical in `a3b71527` to `.orchestration/dotfiles-T128-orchestrator-tools-a03/task.md`. The a01 copy stays at amendment 1 (`91eb1ebe…`, unchanged since `2dddff84`) as the task says (validation §1).

## The delta

a03 is a01 amendment 1 plus one threat row: `dispatch.sh`'s acceptance-record path (it reads the record's JSON block, reads the bus marker through `history.sh`, and rewrites the `dispatch` list after the send), closed by `tests/unit/test_orchestrator_tools.py::test_dispatch_records_the_sent_line_with_its_read_marker`. As the task's Completion expects, the code is unchanged since `5ec05d8d` (§1), and this head adds only the task copy and this evidence.

- All five closed rows name a test present in this head (§2).
- The new row's listed controls are in the code at the lines §3 prints:
  - the record is an argument (`record=${6:-}`);
  - the block is read with `object_pairs_hook=refuse` (a duplicate key refuses);
  - only the `dispatch` list is touched (`setdefault("dispatch", [])`);
  - the file is written whole with `sort_keys=True, indent=2`;
  - the marker is read team-wide through `history.sh <team> "" 100000`.
- Its closing test covers the pre-send refusal of a malformed record, the prose kept byte for byte, the team-wide read, a read and an unread marker, a prose-only record, and only a row this send created being recorded. The record mutants D6 to D9, D12 and D13 each fail it (§5).

## Results

9 tests OK; the counters, boundary and docs modules 77 OK; shfmt (`-i 4 -sr`, the CI form), shellcheck and ruff clean; 27 mutants, 27 failures (§4, §5). Size (§6): 6 files outside `.orchestration/`; added lines outside and under `tests/`: 311 and 316 (caps 500 and 1000).

## Bot threads

The ten threads of the a01 phase stand as a01's report tables them: nine `fixed:` (`e6f2bdc0`, `2dddff84`, `17d3735d`, `0a5ae302` twice, `b80b03ee` three times, `77e75595`). 4254494999 is answered by this task's threat row, `fixed:a3b71527` (the a03 task copy that carries it). The worker resolves no thread.

## Not done, or outside scope

No code change, as the task expects. Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `7a16273b-e91b-450e-abcd-de070e344d08` (§6).

cost: n/a

## Fix round 1 (`9496c734`)

On head `58ecd753` (validation §7), Bot review 5498865497:

| Thread | Finding | Disposition |
|---|---|---|
| 4254771302 (P1, `dispatch.sh:94`) | the field grammar `^([a-z_]+)_sha256=` skipped names with digits (`a02_expected_sha256=`), so such a hash went unchecked | `fixed:9496c734`: any name before `_sha256=` (`^([^=]+)_sha256=`) is checked like the rest; a new case in `test_dispatch_refuses_malformed_lines` (mutant D15) |
| 4254771284 (P2, `three-repeat.sh:40`) | a slug such as `--help` passes `^[a-z0-9-]+$` and reached the CompactionDB CLI as an option | `fixed:9496c734`: `memory search -- <class>`. The real CLI searches `--help` as a query after `--` (§7), and the slug grammar stays the gate's. The closed-row test asserts the argv (mutant T6) |
| 4254771296 (P2, `regime-counters.sh:132`) | a stale or copied record's ledger was trusted without its `task` identity | `fixed:9496c734`: the block counts only when its `task` is the counted task; another task's record falls back to the title detector (mutant R4) |

Results (§7): 9 tests OK; the counters, boundary and docs modules 77 OK; shfmt, shellcheck and ruff clean; 30 mutants, 30 failures. Size: added lines outside and under `tests/`: 313 and 336 (caps 500 and 1000).

## Fix round 2 (`6cd491f5`)

On head `4fc6040f` (validation §8): all `test` jobs passed. Bot review 5498947497 found two P2s and no P1. Both are fixed, because the second guards gate evidence against loss:

| Thread | Finding | Disposition |
|---|---|---|
| 4254844587 (P2, `dispatch.sh:159`) | a record of another task took this line's dispatch | `fixed:6cd491f5`: a record whose `task` is not the line's `task_id` is refused before the send (mutant D16) |
| 4254844595 (P2, `dispatch.sh:173`) | the in-place `write_text` after the send could leave the record truncated | `fixed:6cd491f5`: a temporary file in the record's directory, `fsync`, `os.replace` (mode copied; the temporary file is removed on failure). The record test asserts a new inode and no leftover file (mutant D17) |

Results (§8): 9 tests OK; the counters, boundary and docs modules 77 OK; shfmt, shellcheck and ruff clean; 32 mutants, 32 failures. Size: added lines outside and under `tests/`: 334 and 346 (caps 500 and 1000).

## The final head `c8fb09b0` (main-checkout copy)

- CI: all 12 check runs are `completed success`. The first watcher exited 1 on a GitHub API connection reset, not a check, and the restarted one exited 0 (validation §9).
- Bot: review 5499006240 at 05:00:04Z, with one P2 and no P1. It is the third Codex Bot round under a03 (5498865497 on `58ecd753`, 5498947497 on `4fc6040f`, 5499006240 on `c8fb09b0`), after two fix rounds (`9496c734`, `6cd491f5`), so by Worker Playbook step 15 it is not fixed, and the RESULT carries `bot_rounds=3`:

| Thread | Finding | Proposed handling |
|---|---|---|
| 4254893065 (P2, `dispatch.sh:62`) | a TASK, ACCEPTANCE or PING without `task_id=` passes the prefix check and is sent; with a record, the association check is skipped for it | `open:4254893065`. The finding holds: the SKILL's message contract gives all three a `task_id=`. Proposed fix, about five lines and one test case: refuse a line with no `task_id=`, an empty one, or more than one, before any hash or record work |

All fourteen Codex Bot threads on PR #336, by id (§9): the ten of the a01 phase stand as a01's report tables them (nine `fixed:`, and 4254494999 answered by this task's threat row, `fixed:a3b71527`); 4254771302, 4254771284, 4254771296 `fixed:9496c734`; 4254844587, 4254844595 `fixed:6cd491f5`; 4254893065 `open:4254893065` (third round). The worker resolves no thread.
