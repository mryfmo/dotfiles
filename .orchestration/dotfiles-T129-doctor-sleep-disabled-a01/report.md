---
task_id: dotfiles-T129-doctor-sleep-disabled-a01
seat: claude-review-dot-a005
branch: doctor/sleep-disabled-a01
base: 59db77bb
test_commit: 825a1664
code_commit: 550ebb14
fixture_commit: 55af5c7d
pr: 394
task_sha256: f7c8ffd8f63c0acd8d329539cd06d70936f83e4219843a449225b60b6789f756
---

# Report: dotfiles-T129-doctor-sleep-disabled-a01

- Seat: `claude-review-dot-a005` in `.claude/worktrees/worker-d`, on a fresh branch `doctor/sleep-disabled-a01` from `origin/main` `59db77bb`; the PR #387 branch (`lint/normalised-comparisons-a01`) stays in the worktree, committed and pushed, for its integration.
- Task file: dispatched 2026-10-17T13:50:58Z at `fae13584…`; Amendment 1 (TASK line 14:14:53Z, `previous_task_sha256=fae13584…`) at `f7c8ffd8…`, copied byte-identical to `task.md`; the task-consistency check passes on it (validation §1a); premise 1 replays `2` (§2a). One question (PONG 14:08:09Z), answered by Amendment 1.

## What changed

- **`scripts/check-sleep.sh`** (new, 35 lines, bash, shdoc header): on `uname -s` = `Darwin` it runs `pmset -g`, reads the `SleepDisabled` line with awk (`$1 == "SleepDisabled"`, so leading spaces and tabs do not matter) and exits 1 with `sleep check: SleepDisabled is <value>; run: sudo pmset -a disablesleep 1` unless the value is `1`; a missing line exits 1 naming it and the same command; a failing `pmset` exits 1 with `sleep check: pmset -g failed: <its output>`; any other OS prints `sleep check: skipped (not macOS)` and exits 0; the passing case prints `sleep check: SleepDisabled is 1`. Failures go to stderr as `check-tools.sh`'s do. It runs nothing but `uname`, `pmset -g` and `awk`, and changes no setting.
- **`Makefile`** (one line): the `doctor` recipe runs `./scripts/check-sleep.sh || tool_status=$$?` right after `./scripts/check-tools.sh`, so its status folds into `tool_status` and the summary's `tools=` the same way (validation §4).
- **`tests/unit/test_check_sleep.py`** (new, 61 lines, stdlib only): `test_check_sleep_fails_unless_sleepdisabled_is_1_on_macos_and_warns_on_linux` runs the script as a subprocess with a stub `uname` and a stub `pmset` first on PATH: `SleepDisabled 1` exits 0; `SleepDisabled 0` exits 1 naming the value and the pmset command; no line exits 1; a failing pmset exits 1 with its message; a Linux `uname` exits 0 with the skipped line, its pmset stub exiting 99 to show it is not consulted. Red before the script existed (commit `825a1664`, five subtest failures on exit 127; validation §3), green after (§3a).

## Amendment 1 (the three make-doctor fixtures; the orchestrator's answer of 14:14:53Z to the 14:08Z question)

CI's four test jobs failed on 550ebb14 on three existing tests of `tests/unit/test_runtime_health.py` (`test_make_doctor_propagates_runtime_drift_after_tool_checks`, `test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing`, `test_make_doctor_passes_repair_variable_to_runtime_check`): each builds a temporary repository from the Makefile, `scripts/check-tools.sh` and a stub runtime check and runs `make doctor` there, so the new recipe line found no `./scripts/check-sleep.sh` (exit 127, `tools=failed`). The file was outside `allowed_files`; the question offered a fixture copy (A) or a Makefile guard (B). Amendment 1 adopted A and refused B (a missing check would pass silently): `tests/unit/test_runtime_health.py` joined `allowed_files` and `55af5c7d` adds one `shutil.copy(ROOT / "scripts/check-sleep.sh", repo / "scripts/check-sleep.sh")` beside the check-tools copy in each fixture, no assertion changed; the three tests are green (validation §8). Their `uname` stub answers `Linux`, so the real script prints the skipped line there. The file is also PR #388's, so `after:` names that task and this PR merges after #388 after a rebase.

## The Check

`uv run python -m unittest tests/unit/test_check_sleep.py -v` OK; `shellcheck -x` and `shfmt -i 4 -sr -d` clean (§3b, §3c); `make doctor` run once on this Mac (§3d): the tools check passed with `sleep check: SleepDisabled is 1` on this machine, the runtime check failed (exit 2 as is) because the sandbox denies the network host mise's version check needs, which is the sandbox and not this change; caps 36 changed lines outside `tests/` and `.orchestration/` (cap 60) and 64 added under `tests/` (cap 200) after Amendment 1 (§5a).

## Readings, declared

- "Warns on Linux" is read as the task's item 1 words it: the skipped line and exit 0, no warning count.
- The failure messages go to stderr; the test reads stdout and stderr together.

## Review, hook, cost

- Worker-side independent review (a fresh read-only subagent given the diff and the task file; the records in `dotfiles-T129-doctor-sleep-disabled-a01-worker-crit.json`, the receipt beside it): one round on 550ebb14, `Verdict: correct`, no P0 to P2, two P3 notes declared (a PATH without `uname` fails open to the skipped line; a theoretical SIGPIPE in the printf-to-awk pipe, unreachable for pmset's output size).
- No Understand-Anything hook prompt fired; no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion, id `e0e7e93d-b586-447d-9f64-8ad3cffd7635` (validation §6); the orchestrator consolidates adopted decisions into the main checkout's store at acceptance.
