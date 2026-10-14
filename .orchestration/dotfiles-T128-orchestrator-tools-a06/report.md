# Report: dotfiles-T128-orchestrator-tools-a06

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on PR #350's branch `tools/orchestrator-scripts-3`, continuing from `a06c874e`. That head and every commit before it stay (validation §1).
- **Task copy.** The task file's sha256 `b10dfb47…` matches the TASK's `task_sha256`. It is copied byte-identical to `.orchestration/dotfiles-T128-orchestrator-tools-a06/task.md`. The a05 task copy (`6b238e5a…`) and the a05 evidence records are not edited.
- **The delta.** Item 10 with its test (`dd2f3af1`), this task copy, and this evidence. a05's items 1 to 9 and amendment 1 stand as implemented at `a06c874e`.

## Item 10 (`dd2f3af1`): the gate's execution environment by construction

The task-level audit of `a06c874e` found one P1 at `orch-gate.sh:69`. The wrapper kept the orchestrator's environment, `PYTHONPATH` among it. The gate then starts the feedback collector as `[sys.executable, collector, …]`, without `-I`, with the review worktree as its cwd. An inherited `PYTHONPATH=.` would therefore load a `sitecustomize.py` the PR commits.

- **The fix.** `orch-gate.sh` now runs the gate as `env -i PATH="${PATH}" HOME="${HOME}" AUDIT_EVIDENCE=… ACCEPTANCE_EVIDENCE=… PR_FEEDBACK_EVIDENCE=… REVIEW_EVIDENCE=… AGENT_REVIEWED=1 PYTHONSAFEPATH=1 "${python}" -I -P <root>/scripts/require-crit-review.py --base origin/main`. It still runs inside the subshell whose cwd is the review worktree.
  - `${python}` is the interpreter that `uv python find` resolved in this checkout before the review worktree was entered (amendment 1, unchanged).
  - The amendment-1 line `unset AUDIT_DISPOSITIONS CRIT_REVIEW CRIT_REVIEWED` (thread 4265190267) is removed. The environment is built, not filtered.
  - The shdoc header and the inline comment say the same.
- **The allowlist** is item 10's list: the eight `*_ENV` names of `scripts/require-crit-review.py`, of which the wrapper supplies five and withholds three, plus `PATH`, `HOME` and `PYTHONSAFEPATH=1`.
- **The children.** The gate's children inherit this environment: the collector (`sys.executable`, now the pinned interpreter, with `PYTHONSAFEPATH=1` and no `PYTHONPATH`) and `gh` and `git`.
- **gh still authenticates.** Run in this worktree under `env -i PATH HOME NO_COLOR=1`, the gate's first `gh` call returns `mryfmo/dotfiles` with rc 0 (validation §2). `NO_COLOR` is set by the gate itself.
- **Test: `test_orch_gate_runs_the_gate_under_an_explicit_environment`.**
  - Setup: the test environment holds `PYTHONPATH=.`, `PYTHONSTARTUP`, `PYTHONHOME`, `CRIT_REVIEW=off` and `CRIT_REVIEWED=1`.
  - It checks that the gate stub records exactly the allowlist's names, plus the three its own bash exports (`PWD`, `SHLVL`, `_`; validation §2).
  - It checks that `PATH` and `HOME` hold the caller's values and `PYTHONSAFEPATH` and `AGENT_REVIEWED` hold `1`.
  - It checks that the argv starts `-I -P`.
  - It compares names only, so a failure prints no value.
- **Test-module changes.** Because `env -i` drops `CALLS`, `gate()` writes the gate stub with the calls directory in its text. The inputs test's argv check gains `-P`.
- **Why the stub is bash.** Under `env -i` this macOS Python adds `LC_CTYPE` and `__CF_USER_TEXT_ENCODING` to its own `os.environ` (validation §2), so a Python stub could not report what it was given.
- **Mutation proofs.** Validation §4 lists 5 mutants, all killed:
  - E1, the a05 code;
  - E2, without `PYTHONSAFEPATH`;
  - E3, without `-P`;
  - E4, without `HOME`;
  - E5, one inherited name passed through.
- **Size.** INV-2: 3 files outside `.orchestration`, 201 added lines outside tests and 222 under tests (validation §3).

### Notes for the orchestrator

- **`-P` needs Python 3.11 or later.** The interpreter `uv python find` names here is 3.15. An older one would refuse `-P` and the gate would fail, so the wrapper fails closed.
- **No `TMPDIR`.** `TMPDIR` is outside the allowlist, so the gate's `tempfile` uses Python's default `/tmp`. That is writable for the unsandboxed run the gate needs for `gh`.
- **The collector fallback** at `require-crit-review.py:604-608` is a06's residual row: the gate lineage owns it, and under orch-gate.sh the base is in this repository's object store. It is unchanged here.
