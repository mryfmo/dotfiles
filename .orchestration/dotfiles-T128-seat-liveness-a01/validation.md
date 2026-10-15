---
task_id: dotfiles-T128-seat-liveness-a01
seat: claude-standard-dot-a003
commit: 89a55bbd
---

# Validation: dotfiles-T128-seat-liveness-a01

## 1. The Check's outputs

The task copy's hash, the four premises (1, 0, 189 and 9, as the task states), the base, the two test modules, shellcheck and shfmt on the two scripts, and the size:

```text
$ shasum -a 256 .orchestration/dotfiles-T128-seat-liveness-a01/task.md
eb50e54f2427d9acc5fd9f0f1fb1e6f934828cf5c47c8530e5cca1da065ae9c9  .orchestration/dotfiles-T128-seat-liveness-a01/task.md
$ the four premises
1
0
189
9
$ git merge-base HEAD origin/main
59599783

$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false UV_OFFLINE=1 uv run --no-project python -m unittest -v tests/unit/test_check_regime_boundary.py tests/unit/test_herdr_agents.py  # the new tests, the summary, the failing names
(rc=1)
test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal ... ok
test_attach_names_stale_seats ... ok
test_remove_worker_stale_retires_a_seat_whose_pane_is_gone ... ok
Ran 201 tests in 234.267s
FAILED (failures=28, errors=3)
failing here: 31

$ the same command on origin/main in a scratch worktree (git worktree add --detach; removed after), then diff of the failing names
FAILED
Ran 198 tests in 238.406s
identical failure sets (31 names)

$ shellcheck scripts/check-regime-boundary.sh home/dot_local/bin/common/executable_herdr-agents; shfmt -d (the same two)
(rc=0)
$ ruff format --check (the two test modules)
2 files already formatted

$ git diff --numstat origin/main...HEAD -- . ':!.orchestration'
112	14	home/dot_local/bin/common/executable_herdr-agents
34	2	scripts/check-regime-boundary.sh
41	0	tests/unit/test_check_regime_boundary.py
99	0	tests/unit/test_herdr_agents.py
files: 4; changed lines outside tests/ and .orchestration/: 162; added under tests/: 140
```

**The three new tests pass.** The modules run all 201 tests: the 198 existing plus the three new ones.

**The 31 failures are the environment's.** In this seat's sandbox, 28 tests fail and 3 error, all in `test_herdr_agents.py`'s `--add-worker` and seat-claim groups. The same command on `origin/main`, in a scratch worktree, fails the identical 31 names out of its 198. So this seat's sandbox fails them, not this change. CI runs both modules on GitHub.

**Commit signing is off for this run.** The tests make commits, and commit signing from the global git configuration fails in this sandbox: `git commit` exits 128 there. The runs set `commit.gpgsign=false` through git's environment configuration, which is what CI's unsigned runner amounts to.

## 2. Mutation proofs

Each mutant is applied to the working file, its test runs (with the same git environment), and the file is restored byte for byte:

```text
S1 boundary: every state reads unknown -> test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal: killed (FAILED (failures=1))
S2 boundary: unknown counts as gone -> test_a_seated_worker_whose_pane_is_gone_names_the_stale_removal: killed (FAILED (failures=1))
S3 launcher: no seat_stale= lines -> test_attach_names_stale_seats: killed (FAILED (failures=1))
S4 launcher: seat_stale= also for a skipped claim -> test_attach_names_stale_seats: killed (FAILED (failures=1))
S5 launcher: --stale skips the state check -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S6 launcher: the record is not moved -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S7 launcher: --stale still despawns -> test_remove_worker_stale_retires_a_seat_whose_pane_is_gone: killed (FAILED (failures=1))
S8 launcher: unknown counts as gone -> test_attach_names_stale_seats: killed (FAILED (failures=1))
mutants 8/8 killed; tree restored
```

A first run had S4 and S8 survive: the attach test then had no `unknown` case and no skipped-claim case. Both cases were added before the commit, and the run above is the final one.

## 3. The repository validator

```text
$ UV_OFFLINE=1 uv run --no-project --with pyyaml scripts/validate-agent-assets.py 2>&1 | tail -1  # on 89a55bbd, before the commit
agent asset validation ok
(rc=0)
```
