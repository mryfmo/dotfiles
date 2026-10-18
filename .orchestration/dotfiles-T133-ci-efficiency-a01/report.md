---
task_id: dotfiles-T133-ci-efficiency-a01
seat: claude-standard-dot-a011
branch: tools/ci-efficiency-a01
base: 99a4a80f (origin/main at the branch point)
code_commit: 414e475b (the test commit 0b7c5b4c, the change 3affaac7; the worker review round: the test commit 20096edf and the fix 414e475b)
pr: 409
task_sha256: 17c1cd7d2d873b38e6c9a1cf5b31ba4b09da6982e91647f1623287e71a43d327 (amendment 1; dispatched at 4440b130…)
---

# Report: dotfiles-T133-ci-efficiency-a01

- Seat: `claude-standard-dot-a011` in `.claude/worktrees/worker-d`.
- Task file: dispatched 2026-10-18T04:22:16Z at `4440b130…`. The seat's question PONG (04:29Z) named an `allowed_files` gap: `tests/unit/test_workflow_security.py` pins the permissions of every workflow file, so a new workflow fails it. Amendment 1 (04:34:47Z, `17c1cd7d…`) added that file for one row, and the task copy is the amended file. The task-consistency check passes, and premises 1 to 4 re-run unchanged (validation §1, §1a and §2).

## Item 0

- (a) T132 was finished first on its own branch. A worker review of T132 found a P1 (uv colours its tool list under herdr's `FORCE_COLOR`/`CLICOLOR_FORCE`), fixed in `7eb9438f`/`09414805`. T132's records were committed (`6121555d`) and pushed, and `gh pr ready 405` and `gh pr ready 402` were run at 04:37:04Z. T132's RESULT followed #405's CI and Bot wait. All 13 checks passed on `6121555d`. The Codex summary comment 6245716789 reports the code and security review completed with no findings, and no threads. The RESULT went out as message 2102.
- (b) Measured before any change: `measure.md`. Over the last 30 completed pull-request runs, test.yaml has a median wall time of 557 s, and remote.yaml 615 s. The longest queues are on macOS: 487 s for test, 591 s for public-bootstrap, and 516 s for private-bootstrap, whose median run is 12 s because it only decides and skips. Q4: no cache for test.yaml, because no fetch or install step reaches 60 s. In remote.yaml the only qualifying step is the bootstrap under test, 474 to 575 s, so the cache key and the caveats are named for a follow-up and nothing is cached here. Flakes: the window holds two failures. One is real (PR #400's own test errors). The other is a Snap Store assertion timeout (HTTP 408) in `public-bootstrap (ubuntu-24.04, client)`, whose rerun passed; its log line is pasted. No Homebrew tap warning appears in the measured failures.

## What changed

1. **Concurrency (Q1)**: `test.yaml`, `remote.yaml` and `agent-assets.yml` each gain the task's block, top-level, in block style. The group is `${{ github.workflow }}-` followed by `pr-<number>` on a pull request, or `main-<sha>` otherwise. `cancel-in-progress` is true only on a pull request. A newer PR head cancels its older run; every main push runs to completion under its own commit's group. A schedule or dispatch run is never grouped with a PR.
2. **Private bootstrap (Q2)**: the `private-bootstrap` job moves from `remote.yaml` to the new `.github/workflows/private-bootstrap.yaml` (`name: Private bootstrap`; `on:` push to main, the same `0 0 * * 5` schedule and `workflow_dispatch`; `permissions: contents: read`). The job text is byte for byte except the decide and skip edits of item 3, which keep its decide script identical to public-bootstrap's (validation §5). It is not a required check, and `remote.yaml` keeps `public-bootstrap` as its only job.
3. **In-job skips (Q3)**:
   - **Bootstrap decide step** (identical in both files): on a pull request it runs only when the diff is empty or touches `setup.sh`, `install/`, `home/`, `scripts/lib/`, `scripts/update-agent-assets.sh`, `scripts/gh-auth.sh`, `tests/install/` or one of the two workflow files. Push, schedule and dispatch still run. The skip step is renamed "Skip the bootstrap when no bootstrap path changed".
   - **test.yaml decide step**: it keeps today's relevance rule (`skip_reason=unrelated`). It additionally sets `should_test=false` with `skip_reason=os-independent on macos-14` only when `OS` is `macos-14`, the event is a pull request, and every relevant path matches the OS-independent pattern. The skip step prints the reason through `env`.
   - No job gains an `if` or `needs`, and every heavy step keeps its decision as its only condition.
4. **Flakes (item 4)**: `.github/flakes.yaml` holds one signature, `snapcraft-assertion-timeout`. `scripts/orchestrator/ci-rerun.sh <run-id>` (bash, shdoc, `set -euo pipefail`, jq) works as follows:
   - It refuses a run already listed in `.orchestration/validation/ci-reruns.tsv` (exit 4) before any `gh` call.
   - It reads the run with `gh run view --json jobs,status,conclusion,headSha,event` and each failed job's `--log-failed` output, and matches each job against the signatures, reading them through PyYAML with the repository's `uv run --offline … || uv run …` pattern.
   - It runs `gh run rerun <id> --failed` once, and only when every failed job matches. It then appends one TSV row per job (exit 0).
   - Any unmatched job prints `real failure: <job>` and exits 3 with no rerun. A run with no failed job exits 2.
5. **Tests**:
   - In `test_workflow_orchestration_skip.py`, the module reads the new file (`PRIVATE`), the existing tests read private-bootstrap from it, and `pull_request_head` creates parent directories.
   - New in that module: `test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run`, `test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script`, `test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed` and `test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise`, which also checks that a push to main keeps macOS.
   - `test_ci_rerun.py::test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature`, with a stub `gh`.
   - `test_workflow_security.py` gains the `EXPECTED_PERMISSIONS` row (amendment 1).

## The Check

- `uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security tests.unit.test_ci_rerun -v`: 27 tests green at the head (validation §4). Red on `0b7c5b4c` (6 failures and 7 errors: the four new workflow tests, the moved job's reads and the missing script) and on `20096edf` (the exit-code test: `1 != 4`, `1 != 2`).
- `make unit-test` (validation §4a): 1181 tests, run with the validation-only `mktemp` shim at `3affaac7`. The fix round after it touches only `ci-rerun.sh`, one test module and three comments. It reported 254 failures and errors, in six modules this change does not touch. All six fail identically on untouched `origin/main`: `test_require_crit_review` 136, `test_herdr_agents` 82, `test_ua_symbol_coverage` 19, `test_runtime_health` 8 (the same tests), `test_gh_auth` 5 and `test_agent_stop_gate` 4. The cause, shown for the `git commit` failures, is this machine's global `commit.gpgsign=true` with SSH signing: the sandbox denies `~/.ssh/id_ed25519*`, so every fixture commit that does not disable signing fails with "Couldn't load public key". The stop-gate tests see the gate's own `Terminated: 15` line on stderr. CI is the authority.
- `shellcheck` and `shfmt -i 4 -sr -d` (3.14.1) on `ci-rerun.sh` are clean, and so is CI's own shfmt form. `ruff format --check` is clean on the three test modules. `ruff check` is clean on the two new or extended modules; `test_workflow_security.py` keeps an I001 that already exists at `99a4a80f` (§6a), and amendment 1 limits that file to one line. `make format` exits non-zero as on `origin/main` (Declared). `make render-check` passes (validation §6 and §7).
- Caps (validation §8): 149 changed lines outside `tests/`, `.orchestration/` and the moved job (235 if the 86 lines the move removed from `remote.yaml` count too; cap 250). `private-bootstrap.yaml` is counted separately at 101 added lines. `tests/` has 232 (cap 350).
- After the push (validation §10): no `Private bootstrap` run on the pull request. Item 1 worked live: the push of `414e475b` cancelled the in-progress `Snippet install` run of `3affaac7`. The seven required contexts reported on `414e475b`, as §10 shows.

## Declared

- The bootstrap path filter is the task's pattern as written. Of what the bootstrap depends on, it misses the root `.chezmoiroot` and `vendor/` (`scripts/update-agent-assets.sh` resolves its source root through `vendor/compactiondb`). A PR changing only those skips the bootstrap, and main's push catches it. The pattern is not widened beyond the task's text; the orchestrator decides.
- The existing test `test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff` keeps its name and cases, which still pass under the wider rule. Its name now describes only part of the rule, and the new test covers the rest.
- `ci-rerun.sh` reads YAML through `uv run … --with pyyaml`, the repository's established way for shell scripts to parse YAML (`check-regime-boundary.sh`); jq alone cannot read YAML.
- `make format` exits non-zero on `origin/main` as on this branch. Its whole-tree shfmt step flags 12 files, ten `.orchestration/tasks/*-input/` records plus `home/dot_claude/hooks/executable_project-map-reload.sh` and `tests/install/macos/common/brew.bats`, all unchanged from `origin/main`. CI's own shfmt step (`install/**/*.sh`, `scripts/**/*.sh`, pinned 3.14.1) is clean, and ruff and prettier are clean (validation §6).

- The OS-independent pattern (item 3) is the task's text. Its `.*\.md$` arm also matches Markdown under `home/` and `install/`, so a PR whose only `home/` change is Markdown skips macOS. A `home/` shell file keeps it, as the test asserts.
- `ci-rerun.sh` fetches the fields the task names (`status`, `event`) but does not refuse a run that is not complete or not the PR's current head (worker review P3). Rerunning a superseded head's run would re-enter the PR's concurrency group. The orchestrator runs the script on the current head's failed run.

## Review, hook, cost

- Worker-side independent review: one round on `3affaac7` by a fresh read-only subagent returned `Verdict: incorrect`:
  - P2, fixed: gh's own exit codes (4 needs authentication, 2 cancelled) passed through `set -e` as the script's "already rerun" and "usage" codes. Fixed in `20096edf` (red) and `414e475b`; every gh and jq call and the signature read now end in `|| exit 1`.
  - P2, declared: the bootstrap pattern (the task's text) misses `vendor/` and `.chezmoiroot`, which the bootstrap reads. A PR changing only those skips the bootstrap, and main's push catches it.
  - P3, declared: the OS-independent pattern's `.*\.md$` also matches Markdown under `home/` and `install/`, which is in tension with the task's "a home change keeps macOS".
  - P3, declared: `ci-rerun.sh` does not require a completed run of the PR's current head. A rerun of a superseded head's run re-enters `pr-<N>` and could cancel the newest run, and `--failed` also reruns cancelled or timed-out jobs that no signature checked.
  - P3, fixed in `414e475b`: the concurrency comment's wording.
  - Files: `dotfiles-T133-ci-efficiency-a01-worker-crit.json` and receipt `dotfiles-T133-ci-efficiency-a01-worker-review-receipt.md`. This fix round is the one worker-side round. The orchestrator's task-level audit and `security`-profile review remain the authority (`security: true`).
- No Understand-Anything hook prompt fired, and no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
