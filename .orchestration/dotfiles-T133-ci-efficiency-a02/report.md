---
task_id: dotfiles-T133-ci-efficiency-a02
seat: claude-standard-dot-a011
reset_of: dotfiles-T133-ci-efficiency-a01
branch: tools/ci-efficiency-a01
pr: 409
base: 99a4a80f (origin/main)
previous_head: 6b2ff08f0b09d719eb3786fd032ce16786002257 (a02's first RESULT; the revise round 1 of 08:03:45Z, amendment 1)
code_commit: 2ac65e3b (the test commit 1bb5d946 and the fix fa66ad4d; the worker review round: 72fcb93b and 492e7e28; the orchestrator's revise round 1: eb4a0c34 and 3bd08848, then the canary's race: b9b8a5b2 and 2ac65e3b)
task_sha256: 684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98 (amendment 1; dispatched at 0695769b…)
---

# Report: dotfiles-T133-ci-efficiency-a02

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`, on PR #409's branch `tools/ci-efficiency-a01` at a01's head `27613c0c`.
- Task file: dispatched 2026-10-18T06:58:17Z at `0695769b…`, copied byte-identical to `.orchestration/dotfiles-T133-ci-efficiency-a02/task.md`. The task-consistency check passes (validation §1 and §1a), and the four a01 premises re-run unchanged against `origin/main` (§2). The a01 copy stays: its removal is the orchestrator's reset bookkeeping, outside this task's `allowed_files`.
- Inherited, not repeated: a01's item 0 (the parked PRs) and its measurement. `measure.md` is a01's record under a header that names its source and date (2026-10-18T04:2xZ). Everything in `validation.md` ran for a02.

## The five P2 of the a01 audit, each red against 27613c0c and green at the head

1. **Item 7: superseded heads** (`ci-rerun.sh`).
   - A `pull_request` run must belong to exactly one pull request: `gh api repos/{owner}/{repo}/actions/runs/<id> --jq '[.pull_requests[].number|tostring]|join(" ")'` must print one number. That pull request's current head (`gh pr view <n> --json headRefOid`) must be the run's `headSha`.
   - The check runs before the logs are read and again after the reservation, right before the rerun.
   - Missing or ambiguous association (a fork's run has an empty `pull_requests`), a missing SHA or an unreadable response exits 1. A mismatch prints `superseded: run <id> …` and exits 3. Neither calls `gh run rerun`. A refusal by the second check leaves the reservation in place.
   - Test `test_ci_rerun_refuses_a_superseded_pull_request_head` covers: current, superseded, a head that advances during the log reads, no pull request (a fork), two pull requests, an unreadable head, a push run (no comparison) and a run still in progress.
2. **Item 8: timed-out and cancelled jobs.**
   - Jobs concluded `failure`, `timed_out` and `cancelled` all need a matching signature.
   - A failed job's log comes from `--log-failed`; a timed-out or cancelled job's whole `--log` is read. An empty log matches nothing.
   - Matched timeout and cancellation jobs get their own ledger rows.
   - Test `test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs` covers, for each conclusion: mixed with a matched failure, alone, and matched. It also has a missing log against a catch-all signature, which is red when the guard is removed (§13).
3. **Item 9: the production registry.** Test `test_the_production_flake_registry_matches_its_samples_and_no_real_failure` loads the checked-in `.github/flakes.yaml` through the script's own loader (PyYAML under `uv`) and checks each signature with `grep -E`, the script's engine:
   - the ids equal the measured samples;
   - both expressions compile and match no empty line;
   - each matches its own measured job and log line;
   - its `log_regex` matches neither measured real failure: run 39079197825's `test_validate_agent_assets` ERROR and a plain assertion failure.
   - Red on an invalid `(` and on a broad `.*` registry mutation, green restored (§5).
4. **Item 10: Markdown on macOS** (`test.yaml`). The OS-independent arm is `[^/]+\.md$`, so only root-level Markdown lets a pull request skip `macos-14`. The macOS test gains `home/dot_claude/skills/x/SKILL.md` and `install/common/README.md` (`should_test=true`), and root `README.md` plus `docs/` still skip, while Ubuntu and main-push cases still run.
5. **Item 11: per-run reservations.**
   - The checkout-wide `ci-reruns.lock` is gone. After classification and the first head check, an atomic `mkdir .orchestration/validation/ci-reruns.lock.d/<run-id>` reserves the run, before the ledger rows and the rerun request. It stays after success, failure or interruption.
   - An existing reservation or TSV row exits 4 before any `gh` call. A losing concurrent `mkdir` exits 4. A `mkdir` that fails for another reason exits 1.
   - Tests: `test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs` covers two concurrent calls for one run (exactly one 0 and one 4, one rerun), overlapping calls for two runs (both rerun), and an abandoned reservation with no TSV row (exit 4 for that run only). `test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice` now asserts that the stub `gh` saw the reservation directory and both rows when the rerun request arrived.

Red: on `1bb5d946` (= `27613c0c` plus the tests, no fix) the Check's command gives 16 failures (§4, `unittest exit status: 1`). Green: 32 tests at the head (§4).

## The worker review round (one round, on fa66ad4d)

- **P2, fixed** in `72fcb93b`/`492e7e28`: `ci-rerun.sh` did not require a completed run. A run in progress has jobs that are not final: GitHub refuses the rerun and the reservation is spent, or `--failed` reruns jobs that ended after the snapshot without a signature. A run whose `status` is not `completed` now exits 2 before any reservation.
- **P3, fixed**: the missing-log case and its guard test; the registry test feeds `"\n"`, as the script's here-string does, instead of zero lines; the stub runs the script's own `--jq` on a `pull_requests` payload; the `.github/flakes.yaml` header; a non-EEXIST `mkdir` failure exits 1. **P3, declared**: a broadened `job: '.*'` still passes the registry test (the log expression must still match on its own).
- **P2, spec level, proposed to the orchestrator (no code change)**:
  - Both matrices keep the default `fail-fast: true`, so one failing job cancels its siblings, and item 8 requires a signature for every cancelled job.
  - The measured flake run 39046848147 attempt 1 has `public-bootstrap (macos-14, client)` and `public-bootstrap (ubuntu-24.04, server)` cancelled beside the failed job, so the helper exits 3 on the very run that justifies the only signature.
  - The remedy is a spec decision: `fail-fast: false` in `test.yaml` and `remote.yaml` (both in `allowed_files`; failing PRs would then run every matrix job to completion), or a rule for cancellations a sibling's failure caused.

## Revise round 1 (amendment 1, ACCEPTANCE revise of 08:03:45Z, previous_head 6b2ff08f)

The orchestrator decided the spec-level P2 this seat proposed in its 07:58Z RESULT:

- **The change:** the `test` matrix in `test.yaml` and the `public-bootstrap` and moved `private-bootstrap` matrices set `strategy.fail-fast: false`, with a two-line comment above each `strategy:` that says why. Every matrix job now reports its own conclusion, so a required context is never cancelled by a sibling, and a cancellation `ci-rerun.sh` meets still needs its own signature.
- **Test:** `tests/unit/test_workflow_orchestration_skip.py::test_the_matrices_do_not_fail_fast` reads the three strategy blocks. It is red on `eb4a0c34`, which is `6b2ff08f` plus the test, for all three jobs, and green at `3bd08848`.
- **Records:** the task copy is amendment 1's text (`68425731…`), and `revise.yaml` carries `previous_head` and the selector. The Check's command passes 33 tests, and `make unit-test` and `make format` ran again at `3bd08848` (validation §4, §11 and §12).
- **Caps:** 216 changed lines outside `tests/`, `.orchestration/` and the moved job (302 with the 86 lines the move removed from `remote.yaml`; cap 330). `private-bootstrap.yaml` counted separately: 104 added lines. `tests/`: 435 (cap 500).

## The ubuntu-26.04 canary's race (found in revise round 1, fixed before the RESULT)

The first push of revise round 1 (`c2da7960`) passed every required context. The non-required canary `test (ubuntu-26.04, client)` (run 39111755140, job 117629185615) failed `test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs` with `[0, 4] != [0, 0]`: both of two concurrent calls for one run reran it.

- **Root cause:** uutils' `mkdir` ignored `EEXIST` on a non-recursive creation until uutils commit `bf423f388d` (2026-08-28, "mkdir: do not ignore EEXIST on non-recursive creation", fixing uutils/coreutils#13970). Ubuntu 26.04 ships an older uutils, so there the `mkdir` binary returns 0 for a directory another call has just created. GNU `mkdir` (ubuntu-24.04) and macOS refuse it, which is why those jobs passed. Item 11's reservation was therefore not exclusive on that platform.
- **Red** in `b9b8a5b2`: the same test gains a case with a fake `mkdir` that behaves the same way, first on `PATH`. That makes the race deterministic on any platform: `[0, 4] != [0, 0]` on this Mac.
- **Fixed** in `2ac65e3b`: the reservation is claimed by the `mkdir(2)` system call itself, through `python3`'s `os.mkdir`. `FileExistsError` exits 4 and any other failure exits 1. It stays an atomic mkdir of the per-run directory, independent of the `mkdir` binary.
- **Check:** the 33 tests are green (validation §4 and §16).

## Item 12: evidence counts

- My a01 RESULT's "CI 13/13" is withdrawn: it counted `gh pr checks` rows, which mix check runs and commit statuses.
- For `27613c0c` the orchestrator's saved feedback JSON (`.orchestration/validation/dotfiles-T133-ci-efficiency-a01-pr-feedback.json` in the main checkout) holds 9 check runs in `checks` and 1 commit status (an item with `source: status`). The 7 required contexts all succeeded (§10, against `REQUIRED_CONTEXTS` of `test_workflow_orchestration_skip.py`).
- For a02's final head, the check-run and commit-status counts come from that head's feedback after the push and are stated in the RESULT, separately from the 7 required contexts.

## The Check

- `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v`: 33 tests, green at `2ac65e3b` (§4); 32 at `492e7e28` before the revise round.
- `make unit-test` (§11, complete output, at `2ac65e3b`): 1188 tests, `rc=2`, with 38 failures and 10 errors (the same at `3bd08848`, and at `492e7e28` with 1187 tests). The run sets `GIT_CONFIG_GLOBAL=/dev/null` and puts the `mktemp` shim first on `PATH` to neutralize the sandbox's signing and `mktemp` limits. The 48 failing tests sit in `test_agent_stop_gate` (4), `test_gh_auth` (5), `test_herdr_agents` (31) and `test_runtime_health` (8), none touched by this PR. The same 48 fail on `origin/main` `99a4a80f` under the same settings, so they are reported as pre-existing failures, never as passing.
- `make format` (§12, complete output, at `2ac65e3b`): `rc=2`. Its whole-tree shfmt step flags 12 files, all unchanged from `origin/main`. ruff and prettier are clean.
- `shellcheck scripts/orchestrator/ci-rerun.sh` is clean. `shfmt -d`: the repository form `shfmt -i 4 -sr -d` is clean. A bare `shfmt -d` asks for tabs on this file and on every tracked script, because `.editorconfig` sets `indent_size = 4` with no `indent_style`; `make format` and CI pass `-i 4 -sr` (§6).
- Caps (§8, at `2ac65e3b`): 223 changed lines outside `tests/`, `.orchestration/` and the moved job (309 if the 86 lines the move removed from `remote.yaml` count too; cap 330). `private-bootstrap.yaml`, the extracted job, counted separately: 104 added lines. `tests/`: 445 (cap 500).
- After the push: `gh run list --branch tools/ci-efficiency-a01 --json name,event,conclusion,headSha`, `gh pr checks 409 --required` and the final head's feedback counts go in the RESULT, because a record cannot hold its own commit's CI.

## Changed files

`.github/workflows/test.yaml`, `.github/workflows/remote.yaml`, `.github/workflows/private-bootstrap.yaml` (the extracted workflow), `.github/workflows/agent-assets.yml`, `.github/flakes.yaml`, `scripts/orchestrator/ci-rerun.sh` (the new script), `tests/unit/test_workflow_orchestration_skip.py`, `tests/unit/test_ci_rerun.py` and `tests/unit/test_workflow_security.py`. In the first a02 round: `test.yaml`, `flakes.yaml`, `ci-rerun.sh` and the two test modules. In revise round 1: `test.yaml`, `remote.yaml`, `private-bootstrap.yaml` and `test_workflow_orchestration_skip.py`.

## Review, hook, cost

- Worker-side independent review: one round, as above. Files: `dotfiles-T133-ci-efficiency-a02-worker-crit.json` and receipt `dotfiles-T133-ci-efficiency-a02-worker-review-receipt.md`.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion, id `4a84814c-b3fe-43fc-ba6f-f0ed64dd4e34` (validation §14).
