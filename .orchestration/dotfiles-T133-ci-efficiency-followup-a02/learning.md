---
task_id: dotfiles-T133-ci-efficiency-followup-a02
seat: claude-standard-dot-a011
---

# Learning: dotfiles-T133-ci-efficiency-followup-a02

1. A helper that calls `uv run` without `--python` and `--no-config` takes its interpreter from wherever it is run. ci-rerun.sh had the same interpreter-selection defect that verdict.sh's item 6 fixed. Mechanism: the pinning block is now the shape of three orchestrator scripts: tools resolved under `env -i` from `/`, PATH made of links then `/usr/bin:/bin`, python3 started by its own resolved path (item 3), and `uv run --no-config --no-project --python <that path>` under `env -i`. The next script that runs Python should start from it, and its test should plant a working, marker-writing interpreter through `.python-version`, `.venv`, `UV_PYTHON` and `VIRTUAL_ENV`.
2. Pinning tools changes which binaries a test's PATH stubs can reach. A real `mise which gh` would have bypassed the stub `gh`. Mechanism: setUp plants a failing fake `mise`, so resolution falls back to PATH, and every tool the tests stub (gh, and the uutils-style mkdir) is in the pinned set.
3. A symlink to an interpreter is not the interpreter. CPython looks for `pyvenv.cfg` beside, and one directory above, the path it was started by, without resolving links. A pinned-tools directory under a shared TMPDIR therefore hands the interpreter's standard library to whoever writes `${TMPDIR}/pyvenv.cfg`. Mechanism: python3 is resolved but never linked, and is always started by its own path. `test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path` logs `$0` of every start. The same link pattern exists in PR #410's `verdict.sh` (withdrawn), and the RESULT names it for the redesign `dotfiles-T133-verdict-audit-pool-a03`.
4. A clean local ShellCheck is not CI's ShellCheck. The seat's 0.11.0 did not flag a one-line `A && B && C || { … }`, but the ubuntu-24.04 runner's version did, as SC2015, and the push failed. Mechanism: write a refusal with several conditions as `if ! { A && B && C; }; then … fi`, which neither version flags, and read the runner's ShellCheck output before reporting a lint result as CI's.
