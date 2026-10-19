---
task_id: dotfiles-T133-ci-efficiency-followup-a01
seat: claude-standard-dot-a011
branch: tools/ci-efficiency-followup-a01
base: 3e41e36a (origin/main, PR #409's merge)
code_commit: 4da0c7be (row audit:4fe2438:2: 11ca625b red, c3460269 fix; row audit:4fe2438:1: 05714d84 red, 4da0c7be fix)
task_sha256: b2088fe0b8ddd2e9edc0c8275ed179d073bcdcffaf408afcd9dd6d9fe40d02d9 (amendment 1; dispatched at 650c0610…)
---

# Report: dotfiles-T133-ci-efficiency-followup-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`. The branch `tools/ci-efficiency-followup-a01` was created with `--no-track` from `origin/main` `3e41e36a`, after a single-command `git fetch origin`. PR #410's branch and the seat's local `verdict-audit-pool-a02-a011` were left untouched.
- Task file: dispatched at `650c0610…`. My question PONG (20:36:35Z) asked for `private-bootstrap.yaml`, and amendment 1 (20:37:50Z, `b2088fe0…`) added it for row `audit:4fe2438:1` only. The copy at `.orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md` is the amended text, byte-identical (validation §1).
- The owned rows are the two under `## Owned by dotfiles-T133-ci-efficiency-followup-a01` in `.orchestration/acceptance/dotfiles-T133-ci-efficiency-a02.md`: `audit:4fe2438:1` (`path-filter-quoting`, the same finding as `local:4fe2438:1`) and `audit:4fe2438:2` (`relevance-filter-incomplete`, the same finding as `local:4fe2438:2`). The record's two Bot P2 rows, 4305896433 and 4305896435, are already `fixed:99b07d2b`. Item 1 lists `local:27613c0:1` to `:3` as examples; PR #409's a02 items 7 to 9 fixed them (superseded heads, the production-registry test, timed-out jobs), and the a02 record does not list them as owned. This PR changes nothing for them.

## Row audit:4fe2438:2: the flake registry in test.yaml's relevance filter

- Fix (`c3460269`): the relevance pattern of `test.yaml`'s unit-test decision gains `\.github/flakes\.yaml$`, and its comment says why: `test_ci_rerun.py` validates the file. Before the fix, a pull request that changed only the registry skipped the unit tests (`should_test=false`, `skip_reason=unrelated`), so the production-registry test never checked it.
- Test (`11ca625b`): `tests/unit/test_workflow_orchestration_skip.py::DecisionTest::test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff`. It is red on `11ca625b`, where `test.yaml` is unchanged (validation §3), and green at the head.

## Row audit:4fe2438:1: NUL-delimited paths in the bootstrap path gate

- The defect: even with `core.quotePath=false`, Git quotes a path that holds a double quote, a backslash or a control character. A changed `home/a"b` printed as `"home/a\"b"`, missed `^(…|home/|…)`, and the pull request skipped `public-bootstrap`. `private-bootstrap` never runs on a pull request; its decide step changes only to stay equal to `remote.yaml`'s.
- Fix (`4da0c7be`, `remote.yaml` and, under amendment 1, `private-bootstrap.yaml` line for line): `git diff -z --no-renames --name-only <range>` writes the raw, NUL-delimited list to `${RUNNER_TEMP}/changed-paths`, and `grep -zEq` matches it with the same pattern.
  - An empty list (`[ ! -s … ]`) still runs the bootstrap.
  - A failing `git diff` still fails the step under `set -euo pipefail`; there is no pipe.
  - Push, schedule and workflow_dispatch still exit with `should_run=true` before any diff.
  - BSD grep on the macOS runner supports `-z` with per-record anchors (checked locally: `grep (BSD grep, GNU compatible) 2.6.0-FreeBSD`).
- The two decide steps stay byte-identical (validation §4), so `test_both_bootstrap_jobs_decide_with_the_same_script` and `test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script` stay green unchanged.
- Test (`05714d84`): `tests/unit/test_workflow_orchestration_skip.py::DecisionTest::test_the_bootstrap_decision_reads_paths_that_git_quotes`.
  - A `home/` name holding a double quote, a backslash, a tab or a newline must run the bootstrap; a quoted `.orchestration/` name must still skip.
  - It is red on `05714d84` for the four quoted names (the workflows unchanged; validation §3), and green at the head.
  - The shared `run_decision` fixture now runs each decision in a temporary directory that it also exports as `RUNNER_TEMP`; the GitHub output file lives there too. No other test's expectations changed.

## Observations outside the owned rows (advisory, for dotfiles-T133-ci-efficiency-followup-a02)

`test.yaml`'s unit-test decision still reads `git -c core.quotePath=false diff --name-only` output line by line. A quoted name there can miss the relevance pattern and skip the unit tests, the same class as row `audit:4fe2438:1`. No owned row covers it, so this PR leaves it alone. It is named here and in the RESULT for the orchestrator to record. The worker review adds a second, older one: the gate's `grep` sits in an `if`, so a `grep` error (exit 2) reads as "no match" and skips the bootstrap instead of failing the step. That predates this PR, and the PR leaves it as it was.

## The Check

Validation sections are cited as §. Everything ran at `4da0c7be` plus the draft records (`5df527dd`), inside the sandbox.

- `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v`: 35 tests pass at the head (§3). Each row's test is red on its red commit (§3): the registry test on `11ca625b` (`should_test=false`, `skip_reason=unrelated`), and the four quoted-name subtests on `05714d84` (`should_run=false`), while the `.orchestration/` control passes there.
- The two bootstrap decide steps are byte-identical at the head, and the `remote.yaml` and `private-bootstrap.yaml` diffs are the same hunk (§4).
- `shellcheck` on `ci-rerun.sh`: clean. `shfmt -d`: the repository form `shfmt -i 4 -sr -d` is clean. A bare `shfmt -d` asks for tabs on every tracked script (`.editorconfig` has `indent_size` without `indent_style`). `ci-rerun.sh` is unchanged by this PR. `ruff format --check` on the test module: clean. actionlint is not installed here (§5).
- `make format`: exit 2 (§6). Its whole-tree shfmt step flags 12 files, all unchanged from `3e41e36a`. ruff and prettier, run as the Makefile writes them, are clean.
- `make unit-test` (§7):
  - Plain run: 1209 tests, 194 failures and 111 errors. Fixture commits fail on the sandbox's SSH signing.
  - Neutralized (`GIT_CONFIG_GLOBAL=/dev/null` and the `mktemp` shim): 1209 tests at the head, 1207 at the base `3e41e36a`.
  - Both runs have the same 44 failures and 10 errors, in `test_agent_stop_gate` (4), `test_gh_auth` (5), `test_herdr_agents` (37) and `test_runtime_health` (8). No test fails at the head that does not fail at the base.
  - These are inherited failures, not passing results.
- Caps (§8): 31 changed lines outside `tests/` and `.orchestration/` (cap 250), and 32 under `tests/` (cap 350). The task sets no moved-job count.
- After the push: `gh run list --branch tools/ci-efficiency-followup-a01 --json name,event,conclusion`, the seven required contexts, whether a `private-bootstrap` run happened on the PR, and the Bot window all go in the RESULT, because a record cannot hold its own commit's CI.

## Changed files

`.github/workflows/test.yaml`, `.github/workflows/remote.yaml`, `.github/workflows/private-bootstrap.yaml` (amendment 1), `tests/unit/test_workflow_orchestration_skip.py`, and `.orchestration/dotfiles-T133-ci-efficiency-followup-a01/**`. `scripts/orchestrator/ci-rerun.sh` and `tests/unit/test_ci_rerun.py` are unchanged.

## Evidence, review, cost

- Evidence in `.orchestration/dotfiles-T133-ci-efficiency-followup-a01/`: `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `dotfiles-T133-ci-efficiency-followup-a01-worker-crit.json` and `dotfiles-T133-ci-efficiency-followup-a01-worker-review-receipt.md`.
- Worker-side independent review: one round on `4da0c7be`. Verdict `correct`, with no P0, P1 or P2. Of its three P3, two are advisory and outside the owned rows: the `test.yaml` quoting, and the gate's `grep` exit 2 read as no match, which predates this PR. The third, a wording error in this report, is corrected. No code fix round followed. Files: `dotfiles-T133-ci-efficiency-followup-a01-worker-crit.json` and `dotfiles-T133-ci-efficiency-followup-a01-worker-review-receipt.md`.
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
