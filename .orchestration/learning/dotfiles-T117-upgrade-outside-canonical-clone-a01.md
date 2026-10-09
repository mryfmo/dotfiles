# Learning: dotfiles-T117-upgrade-outside-canonical-clone-a01

Candidates only; nothing promoted.

1. A guard added to a script's `main()` breaks every test that exercises the state the guard now refuses, and those tests can live outside the task's `allowed_files` (`test_runtime_health.py` ran the upgrade inside the canonical clone). Before dispatch, grep the whole `tests/` tree for the script name and read each fixture that runs it end to end, not only the files that name the changed function.
2. Comparing `$(git rev-parse HEAD)` with `$(git rev-parse origin/main)` passes when neither resolves (both empty). Use `rev-parse -q --verify` and require a non-empty HEAD before comparing. Under `set -e`, `git status --porcelain | grep -v '^??'` kills the assignment on a clean tree; `--untracked-files=no` needs no pipe.
3. A "would this guard run here" check should compare `git rev-parse --show-toplevel` with the script's own root by physical path, so a scratch directory sitting under an unrelated repository never inherits that repository's status.
4. When every passing case of a destructive script is verified through `source script; guard_function`, the check cannot start a real upgrade phase even if the guard is wrong; reserve full-script runs for refusal cases and a PATH without package managers.
