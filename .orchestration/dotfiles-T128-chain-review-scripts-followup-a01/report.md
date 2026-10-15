# Report: dotfiles-T128-chain-review-scripts-followup-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/chain-review-scripts-followup`. It was cut with `--no-track` from `origin/main` at `f0faa33a`, after PR #361 merged. The earlier branches are left as they are.
- **Task copy.** It is byte-identical to the dispatched file, sha256 `1d11eb07…`, the TASK's `task_sha256`.
  - **Not `origin/main`'s copy.** `origin/main`'s copy hashes to `0b10249e…`, the pair-confirmed text the TASK note names.
  - **The difference** is amendment 1: decision A's P1 as the first row, and the resolver in the environment row. The orchestrator's record for this task names the amended hash and its second review round (validation §1).
- **Commits.**
  - `5880df9b`: the fixes and their tests.
  - Then this evidence.
- **The PING.** I answered the orchestrator's state PING of 04:43:51Z with a PONG.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## The owned rows

The section on `origin/main` holds eight rows (validation §2). They name six defects, all in `local-review.sh` except the traversal, which `local-advisory.sh` shares. Each has its own test:

| # | Row | Class | What it names | Disposition | Test |
|--:|---|---|---|---|---|
| 1 | `4270918132` | stale-review-file-on-error | Bot, PR #357, local-review.sh:61: a failed review still writes a reusable `findings: 0` file | `fixed:5880df9b` | `test_local_review_writes_no_file_when_the_review_binary_fails` |
| 2 | `4270918140` | reuse-keyed-by-sha7 | Bot, PR #357, local-review.sh:28: a file is reused by the seven-character prefix without its full head | `fixed:5880df9b` | `test_local_review_reuses_only_a_file_that_records_this_head` |
| 3 | `local:b6ce4ff:1` | stale-review-file-on-error | the same as row 1 (rated P1 there) | `fixed:5880df9b` | as row 1 |
| 4 | `local:b6ce4ff:2` | reuse-keyed-by-sha7 | the same as row 2 | `fixed:5880df9b` | as row 2 |
| 5 | `audit:b6ce4ff:1` | review-binary-shim | P1, operator decision A: `command -v codex` can return a mise shim that picks its binary from the PR worktree | `fixed:5880df9b` | `test_local_review_resolves_codex_through_mise_and_refuses_a_shim` |
| 6 | `audit:b6ce4ff:2` | task-arg-traversal | local-review.sh:27 and local-advisory.sh:24: a `/` in the task argument writes outside the directory | `fixed:5880df9b` | `test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory` |
| 7 | `audit:b6ce4ff:3` | sed-path-interpolation | local-review.sh:62: the worktree path is interpolated into a sed program | `fixed:5880df9b` | `test_local_review_strips_a_worktree_path_holding_sed_syntax_literally` |
| 8 | `audit:b6ce4ff:4` | test-order-unproven | the test proved the resolution in the root, not before the checkout | `fixed:5880df9b` | `test_local_review_resolves_the_review_binary_before_the_checkout` |

## The fixes (`5880df9b`)

- **The resolver (rows 5 and 8).** With `CODEX_BIN` unset, local-review.sh resolves codex in this order:
  1. `env -i PATH="$PATH" HOME="$HOME" mise which codex` in the trusted root, before the head's checkout;
  2. else `command -v codex`.

  A relative answer is anchored to the root as before. Any path under a `shims` directory is refused with exit 2.
  - **`CODEX_BIN`** stays the test seam and is resolved with `command -v`, as before.
  - **The form** is orch-gate.sh's for gh.
  - **Where it lives.** It is in local-review.sh itself, not a separate file. `allowed_files` admits no new script, and local-advisory.sh and sandbox-scan.sh run no binary but git and coreutils, so local-review.sh is the only caller.
  - **The tests.**
    - **The shim test.** A mise stub answering a `shims` path is refused, and the review worktree does not move. A stub answering an installed path runs that binary, not the one on PATH. mise is called as `which codex` with the caller's `MISE_CONFIG_FILE` gone.
    - **The ordering test.** The mise stub records the review worktree's HEAD at its call, which is `main`, not the head.
- **No file on a failed review (rows 1 and 3).** A non-zero exit of the review binary prints `local-review: codex exited <n>; no review file written (transcript <tmp>)` and exits 4. The next run reviews again. The header documents exit 4.
- **Reuse by the full head (rows 2 and 4).** An existing review file is reused only when its `head:` line is the requested head. A file that records another head with the same prefix is refused with exit 2, and nothing runs.
- **Checked arguments (row 6).** Both scripts refuse, with exit 2 and a usage line, a task id outside `[A-Za-z0-9][A-Za-z0-9._-]*` or a head that is not 40 hex characters. Both values name the files they read and write.
  - **Why the head too.** The row names the task argument. The head is checked as well because its seven characters are part of the same paths.
  - **Already the documented form.** Both headers already document the head as 40 hex characters, and the chain passes `git rev-parse` output.
- **A literal strip (row 7).** The worktree prefix is now removed with `prefix="$W/"; final=${final//"$prefix"/}`, which applies no regex.
  - **The variable is needed.** A quoted `"$W/"` written inline in the expansion is mis-parsed by `/bin/bash` 3.2, which leaves `"//b.txt`. The test caught it.
- **The existing test changed in two places only:**
  - **A mise stub.** It now puts a failing mise stub on PATH, so its `command -v` path still applies and no host codex can run.
  - **The stale-file subtest.** Its subtest "no finding exits 0, also when the binary fails" asserted the stale file. It is now "no finding exits 0", and the failing binary has its own test.

## Proofs and size

- **Tests.**
  - `test_chain_review_scripts.py`: 9 tests OK, the 3 of `origin/main` and 6 new.
  - `test_chain_github_scripts`, `test_orchestrator_tools` and `test_orch_gate_path`: 54 OK.
- **Linters.** shellcheck, shfmt, ruff check and ruff format are clean (validation §4).
- **Mutation proofs.** 11 mutants, all killed (validation §5). C10 and C11 are `origin/main`'s two scripts.
- **Caps.** 75 changed lines outside `tests/` and `.orchestration/` (of 200), 113 added under `tests/` (of 1000), 3 files (validation §6).
- **The repository validator** passes on `5880df9b` (validation §7).

## Threat table

| Row | Where it is bounded |
|---|---|
| local-review.sh, local-advisory.sh | exactly the eight rows, each with its test and its mutants |
| sandbox-scan.sh | unchanged; no owned row names it |
| tests/unit/test_chain_review_scripts.py | six new tests, the helper `review_head` and the stub `mise`, and the existing test's two changes above |
| the review worktree | the guard is unchanged; the review worktree no longer moves on a shim refusal, because the refusal comes before the checkout |
| environment inputs | local-review.sh adds `env` and `mise` (the resolver the row names); everything else is as row 11 lists |
| the task copy | byte-identical to the dispatched file, `1d11eb07…` |
| new or renamed scripts | none |

## Notes for the orchestrator

- **local-review.sh has a new exit code, 4,** for a failed review binary. A chain that treated a non-zero exit as findings should read 4 as "no sample".
- **Both scripts now refuse a short or symbolic head.** Callers pass `git rev-parse` output, as the usage examples do.
- **The Understand-Anything stale-graph hook** did not fire. plan-mode-used: no.

## CompactionDB

The main-checkout `memory add` runs after CI. Its command and output go into the main-checkout copy of this report.

- [memory:decision] local-review.sh resolves codex like orch-gate.sh resolves gh: `mise which` under `env -i` in the trusted root before the checkout, a shims path refused. A failed review writes no file (exit 4). A review file is reused only when its `head:` is the full requested head. The task id and the head are path-checked in local-review.sh and local-advisory.sh.
- [memory:failure] `/bin/bash` 3.2 mis-parses a quoted pattern written inline in `${var//"$x/"/}`. Put the literal in a variable and write `${var//"$p"/}`.

## Revise round 2 (`35f76e7d`)

- **The finding.** The audit's P1 on `c45f9b5` (local-review.sh:86): the binary `mise which` answers can be a launcher whose first line is an env shebang for node, so the interpreter was still found on PATH at exec time, in the PR worktree. The binary was pinned, its interpreter was not, a gap of row `audit:b6ce4ff:1`.
- **The fix.** After the binary is resolved and before the checkout, local-review.sh reads its first line. For `#!/usr/bin/env NAME`, or `env -S NAME …`, it resolves NAME exactly as the binary is resolved (`mise which` under `env -i` in the root, else `command -v`, a shims path refused with exit 2), and runs the interpreter with the binary as its first argument, then the review arguments. Any other first line runs the binary as before. The resolution is one function, `resolve`, used for both; the header's binary sentence says so.
- **The test.** `test_local_review_pins_the_review_binary_interpreter`, the revise's check, with its two cases (validation §8). Three mutants of the round are killed: no interpreter step, the interpreter resolved after the checkout, and no `-S` form.
- **Size after the round.** 95 changed lines outside `tests/` and `.orchestration/` (of 200), 145 added under `tests/` (of 1000), 3 files.
- **No new Bot wait**, as the revise says.

## Bot and CI

The PR opens after this evidence commit. The CI result and the Bot's review go into the main-checkout copy and the RESULT.
