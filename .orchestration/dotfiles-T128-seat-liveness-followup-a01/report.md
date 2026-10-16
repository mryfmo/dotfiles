---
task_id: dotfiles-T128-seat-liveness-followup-a01
seat: claude-standard-dot-a002
branch: tools/seat-liveness-followup
base: 1d418126
code_commit: 2fb34e0f
revise_commit: 37ff1475
pr: 377
task_sha256: bd8f2d29b3f88ddb6194d7700f4554fc3680cebc341cfe8171dde47082d90085
---

# Report: dotfiles-T128-seat-liveness-followup-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/seat-liveness-followup` from `origin/main` `1d418126` (boundary (16)). The PR #372 branch stays in the worktree, committed and pushed, until its acceptance.
- Task file: sha256 `bd8f2d29…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 2026-10-16T22:46:03Z. Both premises replay equal (6 and 7, validation §2). No question and no amendment.

## The owned rows and what each changed

Validation §2 prints the owner section from `origin/main`.

| Row | Class | Change in `executable_herdr-agents`, `--stale` mode only |
|---|---|---|
| `audit:d3bc745:1` | stale-no-identity-rows | Before the state loop, an empty `seat_rows` exits 2 with `herdr-agents: no seated identity at <worktree>; nothing retired`. No `delivery.sh`, `leave.sh` or record move follows, and no tab or workspace is closed. The `${seat_rows[@]+…}` guard on the state loop is gone, since the array is non-empty there. |
| `audit:d3bc745:2`, `local:d3bc745:1` | stale-dir-order | After the state loop and before the first `delivery.sh`, each seat's run directory (the directory of `seat_record_path`) is checked without creating anything. If `<run dir>/stale` exists and is not a writable, searchable directory, or the run directory is not writable and searchable (the `-w` and `-x` tests added in revise round 1), it exits 1 with `herdr-agents: <run dir>/stale is not a directory, or <run dir> is not writable; nothing retired`. The `mkdir -p` stays at the move, so a refused run creates no `stale/`. |

The despawn path, and every line outside these two blocks, is unchanged (validation §3).

## Test

`test_remove_worker_stale_prepares_the_archive_before_cleanup_and_refuses_without_identity_rows` uses the module's `seat_remove_fixture` (a standalone workspace `w-b1` listed) and a gone pane. It has four cases. In each, it checks: the exit code; the stderr line; no `delivery`, `leave`, `despawn` or `workspace close` call; the record byte-identical; the workspace list unchanged; and no `retired (stale)` line.
1. `run/stale` is a regular file: exit 1.
2. `run/stale` is a directory with mode `0500` (revise round 1, thread `4300117658`): exit 1, and nothing is moved into it.
3. The fake `identities.sh` prints nothing for the worktree: exit 2.
4. The run directory is `chmod 0500`, with `run/stale` absent: exit 1, and no `stale/` is created. The mode is restored inside the test, because `tearDown`'s `rmtree` runs before `addCleanup` callbacks.

The lineage's tests are unchanged, and all six stale tests pass (validation §4). Mutation check (§5): 5 mutants, each applied alone, all 5 caught; then the six stale tests pass. The mutants drop the no-row refusal, the non-directory test, the run directory's `-w`/`-x` tests, the `stale/` directory's `-w`/`-x` tests, and the whole destination check. The run directory's `-x` test alone has no case of its own: a run directory with write but no search access is not among the task's cases.

## Caps

Validation §6: outside `tests/` and `.orchestration/`, 1 file, 16 added and 1 deleted, so 17 changed lines (cap 200). Under `tests/`, 48 added lines (cap 1000).

## Readings, declared

- **The run directory** is each seat's own record directory, checked for every row. All seats share one `run/` today, so the check repeats the same test.
- **The refusal message** keeps item 1's wording (`<run dir>/stale is not a directory, or <run dir> is not writable`) for the new permission case too, because the revise round asked for nothing else.
- **The full module in this sandbox** has 31 failures, the same set on `origin/main` (validation, the paragraph before §1). CI's `Run Python unit tests` step runs it outside the sandbox (validation §7).
- **ruff check** reports 22 findings on this test module, the same 22 on `origin/main`'s copy, and none is on the new test. CI runs `ruff format --check` on it, which passes; it does not run `ruff check` (validation §7).

## CI and the Bot

- **The Bot** (review `5554579425` on `4fa99329`, 23:07:33Z) left one P2, thread `4300117658`, "Check the existing archive directory's permissions". It was proposed as a C-50 revise round, accepted by the orchestrator at 23:17:24Z, and fixed in `37ff1475` with the new test case.
- **CI on `4fa99329`:** 12 check runs and the CodeRabbit status passed. CI on the final head is in the RESULT; no new Bot wait, per the revise message.

## Not done, or outside scope

- Nothing outside the two files. After the merge the operator runs `make update` (the launcher lives under `home/`).
- Understand-Anything hook: did not fire. plan-mode-used: no.
- cost: n/a (the runtime exposes no session figures to the seat).
