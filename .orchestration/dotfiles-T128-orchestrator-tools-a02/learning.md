# Learning triage: dotfiles-T128-orchestrator-tools-a02

These are candidates only; nothing is promoted.

1. [memory:decision] Check a task's imports against `origin/main` before writing them. a02 told `acceptance-front-matter.py` to import the gate's record validator and `orch-gate.sh` to pass `ACCEPTANCE_EVIDENCE`, but both exist only on PR #329's branch, and the task's `after:` named a04 alone. A `git grep` on `origin/main` for each name a task imports or passes found the gap before any code was written. The question and the split cost one bus round instead of a failed CI.
2. [memory:decision] A lock file inside a directory that a commit sweep lists becomes a committed file. `boundary.sh` commits everything `git status --untracked-files=all -- .orchestration` prints, so `dispatch.sh` locks the record's directory fd instead (`fcntl.flock` works on directory fds on macOS and Linux).
3. [memory:failure] A mutation harness must name the test by its full dotted path, class included. `tests.unit.test_regime_counters.test_x` "killed" four mutants through an unittest load error, not an assertion. Count the `errors=` results and rerun those mutants by hand before reporting them.
4. [memory:failure] The host `bash` is 3.2 here, where `set -u` makes an empty `"${a[@]}"` an unbound-variable error. Use `${a[@]+"${a[@]}"}` for a possibly empty array, and run the tests with the host's `bash` so they catch it.
5. [memory:failure] `uv run --with pyyaml` needs pypi in the seat sandbox even with a warm cache. Run such tests locally with `UV_OFFLINE=1`, which the subprocess inherits, and leave the online path to CI.
