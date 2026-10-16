# Report: dotfiles-T128-orchestrator-tools-followup-a03

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/dispatch-checker-window`, cut with `--no-track` from `origin/main` at `1d418126`. The earlier branches are left as they are.
- **Task copy.** Byte-identical to the dispatched main-checkout file, sha256 `b291ba85…`, the TASK's `task_sha256` (validation §1).
- **Commits.** `766c1491`: the change, its tests and the task copy; then this evidence.
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
- **The module.** 54 tests pass (validation §1). Seven mutants, all killed (validation §2).
- **Two of the 52 changed.** The cap's removal forced it; the names and edits are in validation §3. The module docstring names its new dependency on a real uv for the checker case.

## Notes

- **The uv form.** It is the Makefile's form without `--no-project`, as the task names it three times. The repository has no root `pyproject.toml`; a caller standing in a directory with its own project would make uv consider that project, which the task's form accepts.
- **Size.** 104 changed lines outside `tests/` and `.orchestration/` (of 200), 107 added under `tests/` (of 1000), 2 files.
