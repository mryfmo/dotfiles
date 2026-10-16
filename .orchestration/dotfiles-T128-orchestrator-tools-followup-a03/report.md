# Report: dotfiles-T128-orchestrator-tools-followup-a03

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/dispatch-checker-window`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `b291ba85…`, the TASK's `task_sha256` (validation §1).
- **Commits.** `766c1491`: the change, its tests and the task copy; `aeb4a0fb`: this evidence; `c8e813ea`: the Bot's P1 fix; then this evidence's fix-round update.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## Item 1a: the checker refusal (C-52)

- For an AGMSG-TASK line, after the hash checks and before any read or send, `dispatch.sh` picks the Makefile's `UV_PYYAML` form: `uv run --offline --with pyyaml` when that form imports yaml, else `uv run --with pyyaml`.
- **The brief exemption.** It parses the task file's front matter (the lines between the first two `---` lines) with PyYAML under a `SafeLoader` whose mapping constructor refuses a duplicate key. Only a mapping whose `kind` is the string `review` skips the checker. A parse error, a duplicate key, no closed front matter, no `kind` or any other value runs it.
- **The checker.** `task-consistency-check.py --root <root> <file>` beside the script, as `python -I`. A non-zero exit prints `dispatch: <file> fails the task-consistency check` and the checker's output on stderr, exits 1 and sends nothing.

## Item 1b: the bounded window (C-53)

- Both reads are `history.sh <team> "" <BUS_READ_WINDOW>` (default 200, a positive integer, else usage). `BUS_READ_LIMIT` and the cap refusal are gone.
- **The window file.** `mktemp "${TMPDIR:-/tmp}/dispatch-window.XXXXXX"` (mode 0600), removed by an EXIT trap. The `check` mode writes the pre-send window there: each row's timestamp, sender, recipient and text, never its marker.
- **The alignment.** The `append` mode tries every shift `j` from 0 to `m − 1` and keeps those where the post-send window without its `j` newest rows equals the pre-send window without its `e = n + j − m` oldest (`0 ≤ e < n`). An empty pre-send window takes `j = m`.
- **Outcomes.** Zero or several fits: `does not align uniquely … raise BUS_READ_WINDOW or check the bus`. A unique `j = 0`: `this send added no bus row`. Otherwise the send is the last of the `j` new rows equal to the line, sender and recipient, and none equal: `no new row equals the line`. Every refusal exits 1 with the record unchanged.
- The shdoc header, the `@env BUS_READ_WINDOW` line and the `@exitcode 1` line say so.

## Tests

- `test_dispatch_refuses_a_task_file_failing_the_checker`: the stub checker beside the copied script, a fake `uv` that logs its argv and runs the real `uv` next on PATH. Refused, each with the checker call logged and the C2 line on stderr: `kind: code`, `kind: "code"`, no `kind`, the duplicate key in both orders, and a closed but unparsable front matter with one `kind: review` line. Sent with no checker call: a single `kind: review`. The log's first call is the `UV_PYYAML` probe.
- `test_dispatch_reads_a_bounded_history_window`: the limit argument is 200 on both reads, 50 with `BUS_READ_WINDOW=50`. Recorded once with the right marker: eviction plus collision, same second, and another seat's newer row. Refused with the record unchanged: left the window, no new row, a periodic bus. No `dispatch-window.*` file is left after any case.
- **The module.** 54 tests pass (validation §1). Eight mutants, all killed (validation §2 and §4).
- **Two of the 52 changed.** The cap's removal forced it; the names and edits are in validation §3. The module docstring names its new dependency on a real uv for the checker case.

## Notes

- **The uv form.** The Makefile's `UV_PYYAML` form plus `--no-project`, the Bot's P1 (below): a caller's `pyproject.toml` is never discovered, synced or built.
- **Size.** 105 changed lines outside `tests/` and `.orchestration/` (of 200), 114 added under `tests/` (of 1000), 2 files (validation §4).

## The Bot

- **Code review of `aeb4a0fb`** (review 5545290170): one P1, thread 4292675906, `dispatch.sh:181`, "Isolate uv from the caller's project". `fixed:c8e813ea`: `--no-project` on both uv forms, and the checker test's review brief sent from a directory with an unresolvable `pyproject.toml` (validation §4). The fix round is the PR's one round; the Bot's re-review is asked with `@codex review` on the fix head.
- **Security review of `aeb4a0fb`:** completed, no finding.
- **The PING** of 2026-10-16T21:38:05Z (the host slept overnight) was answered with a PONG, `status=alive`.

## Revise round 2 (`8adf74bb`)

- **The P1.** The Bot's re-review of `57d3577c`, thread 4299651928, `dispatch.sh:182`: `--no-project` keeps a caller's `pyproject.toml` out, but a `.python-version` or virtual environment in the caller's directory still chooses uv's interpreter. The operator's decision D-P1-374 A: one more fix round.
- **The fix.** `fixed:8adf74bb`. Both uv forms run in a subshell that changes to the script's checkout root (`uvr`); the checker is named by the script directory's absolute path.
- **The test.** `test_dispatch_refuses_a_task_file_failing_the_checker` plants a `.python-version` naming an executable in the caller's directory: it never runs, and the fake uv records the root as every call's directory. Mutant M9 (no `cd`) is killed; all nine mutants are killed, and 54 tests pass (validation §6).
- **Size after the round.** 108 changed lines outside `tests/` and `.orchestration/` (of 200), 122 added under `tests/` (of 1000), 2 files.
- **The Bot.** Its re-review is asked with `@codex review` on this round's head.
