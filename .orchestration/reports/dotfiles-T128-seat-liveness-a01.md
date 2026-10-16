# Report: dotfiles-T128-seat-liveness-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/seat-liveness`. It was cut with `--no-track` from `origin/main` at `59599783`. The #364 branch `tools/chain-review-scripts-followup` is left as it is for its integration.
- **Task copy.** It is byte-identical to the dispatched file, sha256 `eb50e54f…`, the TASK's `task_sha256`. The file is not yet on `origin/main`, so it is copied from the main checkout. All four premises replay as stated (validation §1).
- **Commits.**
  - `89a55bbd`: the code and the three tests.
  - Then this evidence.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## What changed

### `seat_pane_state <team> <name>`, in both scripts

The function prints `present`, `gone` or `unknown`. It runs the task's lookup in a child bash, with `SKILL_DIR` set:

1. It sources `lib/actas-lock.sh` and `lib/terminal-registry.sh`.
2. It takes the record from `agmsg_spawn_path`, and the pane ref as the first tab-separated field of the record's first line.
3. It reads the terminal with `agmsg_terminal_ref_terminal`, the bare id with `agmsg_terminal_ref_id`, loads the driver with `agmsg_terminal_load`, and prints `terminal_pane_state`.

Any failing step, an empty answer, or an answer other than `present` or `gone` prints `unknown`. The launcher cannot call a repository script, so it carries its own copy, as item 2(a) says.

### `scripts/check-regime-boundary.sh`

- **The lookup row.** For a worktree with a seated identity, the first `<team>\t<name>` row of `identities.sh` decides: claude-code first, then codex.
- **The violation line.** When the state is `gone`, the violation reads `worker seated but its pane is gone at <worktree> (herdr-agents --remove-worker <worktree> --stale)`. Otherwise the existing line stays.
- **The header** names the stale removal.

### `home/dot_local/bin/common/executable_herdr-agents`

- **`--remove-worker <worktree> [--force] [--stale]`.** `--stale` is parsed beside `--force`, refused outside remove-worker, and documented in `usage()` and the shdoc header.
- **The remove block** collects every identity row of the worktree (type, team, name) first.
  - **The orchestrator-identity check** (`leader`) runs over the rows before either path, as before. The dirty-worktree refusal stays before it.
  - **With `--stale`,** every row's state is read before anything changes. Any state but `gone` prints `herdr-agents: <name> at <worktree> is <state>, not gone; use --remove-worker without --stale.` and exits 2.
  - **When every row is gone,** each row skips the despawn and runs `delivery.sh set off <type> <worktree>`, then `leave.sh <team> <name>`.
    - **The record** (`agmsg_spawn_path`'s path) is moved to `<run directory>/stale/<basename>.<%Y%m%dT%H%M%SZ>`.
    - **Then** the tab is closed best-effort, and the launcher prints `Herdr agents worker retired (stale): <name> (<worktree>)`.
  - **Without `--stale`,** the path runs as before.
- **`claim_seat_and_print_directive`.** When the claim was not skipped, it prints the `seat_stale=` lines after the claim line and before the directive.
  - **Which worktrees.** Each linked worktree of the main checkout under `.claude/worktrees/` that holds an identity of either type, and whose first row's state is `gone`.
  - **The path printed** is relative to the main checkout.

## Tests

- **`test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal`** (boundary module, the 10th test).
  - **The setup.** A linked worktree `.claude/worktrees/b1` is added. The fakes `identities.sh`, `lib/actas-lock.sh` and `lib/terminal-registry.sh` live under the test's HOME, and `terminal_pane_state` prints a state file (`unknown` exits 10).
  - **The cases.** `gone`, `present` and `unknown`. Each asserts the full list of violation lines about that worktree: the stale line for `gone`, and the despawn line for the other two.
- **`test_attach_names_stale_seats`** (launcher module).
  - **The setup.** Fake libraries are appended to the module's orchestrator seat fakes. The `identities.sh` fake is path-aware, and a linked worktree `b1` holds `claude-standard-dot-a007`.
  - **The state cases.** `gone` gives the claim line, then `seat_stale=.claude/worktrees/b1`. `present` and `unknown` give the claim line only.
  - **The skipped claim.** A worker pane's SessionStart (claim skipped) gives `seat_claim=skipped reason=not-orchestrator-pane` only, even for a gone seat. The `unknown` and skipped cases were added after mutants S8 and S4 survived the first proof run (validation §2).
- **`test_remove_worker_stale_retires_a_seat_whose_pane_is_gone`** (launcher module).
  - **State `present`.** Exit 2 with the message. The whole calls list is the seven lookups (two `workspace list`, five `identities`), with no `delivery`, `leave` or `despawn` call, and the record is untouched.
  - **State `gone`.** Exit 0 with the retired line. The whole calls list is the same lookups, then `delivery set off claude-code <worktree>` and `leave dotfiles claude-standard-dot-a007`, with no `despawn`. The record is gone, and exactly one `stale/spawn.dotfiles__claude-standard-dot-a007.<timestamp>` exists.

## Proofs and size

- **Tests.** The two modules run 201 tests, and all three new ones pass.
  - **The local failures.** Locally, 31 existing tests fail, the identical set that fails on `origin/main` in this sandbox (validation §1). CI is the judge of the full modules.
  - **Commit signing.** The local runs set `commit.gpgsign=false` through git's environment.
- **Linters.** shellcheck, shfmt and ruff format are clean on the changed files.
- **ruff check on the launcher test module** reports the same 22 findings as `origin/main`'s copy of it, all pre-existing. None is in the added code.
- **Mutation proofs.** 8 mutants, all killed (validation §2).
- **Caps.** 162 changed lines outside `tests/` and `.orchestration/` (of 200), 140 added under `tests/` (of 1000), 4 files.

## Threat table

| Row | Where it is bounded |
|---|---|
| check-regime-boundary.sh | `test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal`; S1, S2 |
| test_check_regime_boundary.py | one new test; the nine are unchanged |
| executable_herdr-agents | `test_remove_worker_stale_retires_a_seat_whose_pane_is_gone`, `test_attach_names_stale_seats`; S3 to S8 |
| test_herdr_agents.py | two new tests and the helper `write_pane_state_fakes`; the 189 are unchanged |
| the placement record | retired only on an explicit `--stale` with every row `gone`; moved under `stale/`, never deleted; `present` and `unknown` change nothing |
| environment inputs | the child bash sources the two upstream libraries with `SKILL_DIR`, which run herdr and sqlite3 from PATH, as despawn.sh does |
| new or renamed scripts | none |

## Notes for the orchestrator

- **After the merge,** the operator runs `make update` to install the launcher.
- **The `unknown` state never retires anything.** An unreachable herdr, or a missing record or library, keeps the despawn path. So `--stale` is refused there.
- **The Understand-Anything stale-graph hook** did not fire. plan-mode-used: no.

## CompactionDB

The main-checkout `memory add` runs after CI. Its command and output go into the main-checkout copy of this report.

- [memory:decision] A seated worker's liveness is its pane state from upstream's chain: `agmsg_spawn_path`, the record's first field, `agmsg_terminal_ref_terminal`/`_id`, `agmsg_terminal_load`, then `terminal_pane_state`, giving present, gone or unknown. `herdr-agents --remove-worker <wt> --stale` retires only gone seats and moves the record under `run/stale/`. `check-regime-boundary.sh` names that command, and `--attach` prints `seat_stale=`.
- [memory:failure] In this Claude worker sandbox, `git commit` in tests exits 128 because of global commit signing, and 31 tests of `test_herdr_agents.py` fail on `origin/main` too. Compare the failure set against a baseline worktree before reading local failures as regressions.

## Revise round 2 (`3cc248cb`)

- **The P2** of the audit of `cb9ea17` (executable_herdr-agents:1950). On the `--stale` path a failed `leave.sh` or `delivery.sh` was suppressed, and the record still moved. The retirement reported success while an identity remained with no record, and a retry then read `unknown`.
- **The fix.** On the `--stale` path, `delivery.sh set off` and `leave.sh` run before the record is touched. Either failure prints the step on stderr, keeps the record, and exits 1. The despawn path is unchanged.
- **The test.** `test_remove_worker_stale_keeps_the_record_when_cleanup_fails`, the revise's check. Its mutant, the suppression restored, is killed (validation §4).
- **The P3** (validation.md:33). The baseline comparison is now pasted in full in validation §4: the command, the 31 failing names on the branch, the 31 on `origin/main` `907522c2`, and their empty diff.
- **Size after the round.** 167 changed lines outside `tests/` and `.orchestration/` (of 200), 169 added under `tests/` (of 1000), 4 files.

## Bot and CI

- **CI.** Every check passes on `ee929382`, the four unit-test jobs included (validation §4). The 31 local failures are the sandbox's only.
- **The Bot.** Both its code review and its security review completed with no comment and a 👍 reaction. There is no thread and no fix round.

## Main-checkout copy: the memory add

```text
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T128-seat-liveness-a01 (PR #367, head ee929382, plan 022 T6, M-20261015-01): a seated worker whose Herdr pane is gone is told from a live one by seat_pane_state (agmsg_spawn_path record, first field, agmsg_terminal_ref_terminal/_id, agmsg_terminal_load, terminal_pane_state: present, gone or unknown for any failing step). check-regime-boundary.sh names herdr-agents --remove-worker <wt> --stale for a gone seat; herdr-agents --attach prints seat_stale=<wt> after an unskipped claim; --remove-worker --stale reads every row state first, refuses anything but gone with exit 2, else skips the despawn, turns delivery off, leaves, and moves the placement record to run/stale/<basename>.<UTC>. Locally 31 test_herdr_agents tests fail in the worker sandbox, identical on origin/main; CI green.'
1c390546-19bb-4e55-868f-d4281e75d515
rc=0
```

## Round 2: CI on `d3bc745c`, the final head

Every check passes on `d3bc745c`, the four unit-test jobs included (validation §5). `mergeStateStatus` is `CLEAN`. No Bot wait, as the revise says.
