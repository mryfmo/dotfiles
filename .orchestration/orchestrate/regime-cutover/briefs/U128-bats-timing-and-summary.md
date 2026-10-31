# U128 Timing and a summary line from the Bats wrapper (plan P-37, research V4-7)

GOAL
The per-test bounds in `scripts/ci/run-bats.py` (DEFAULT_BOUND) and the budget constants in `tests/unit/test_apt_mirror.py` were measured by hand from CI logs, and a stalled test's name and diagnosis stay in the job log where nobody reads them unless the job is red. Bats 1.14.0 (one version everywhere since U127) prints a duration on each result line under `--timing`; the wrapper reads it, names the slowest test of the run, and writes the stall line, the diagnosis and the slowest line to the job summary page when `GITHUB_STEP_SUMMARY` is set. Nothing else changes: the wrapper still signals nothing (U99).

SCOPE
One branch `ci/bats-timing-and-summary` from `origin/main` after U127 lands. May write: `scripts/ci/run-bats.py`, `scripts/run_unit_test.sh` (`run_bats` passes `--timing`), `tests/unit/test_run_bats.py` (new or extended; check `ls tests/unit` for an existing module), `tests/unit/test_apt_mirror.py` (a comment on the budget constants pointing at the timing lines, no value change), `tests/fixtures/` for one recorded `cat` stream.

CHANGE
1. Measure first: one run of `bats --formatter cat --timing` on a two-test file under Bats 1.14.0 is recorded into a fixture, and the exact suffix form of the result line (the vendor documents `--timing` but not the stream's spelling) is pinned by a test on that fixture.
2. `run-bats.py` parses the duration suffix of every result line, keeps the maximum, and prints `slowest: <n> <name> <ms> ms` after the plan line; a result line without the suffix under `--timing` is a malformed stream and the wrapper says so on stderr (exit status unchanged, the suite's status still decides).
3. When `GITHUB_STEP_SUMMARY` names a writable file, the wrapper appends the `not ok ... # timeout` line and the diagnosis block on a stall, and the slowest line on success; a write failure is reported on stderr and changes no exit status (the summary is a convenience, the log is the record).
4. `run_bats` passes `--timing`.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_run_bats tests.unit.test_apt_mirror tests.unit.test_scratch_git` OK: a recorded stream with timing suffixes and a synthetic stall asserts stdout, exit 124 and the summary file content. 2. The lints of the WORKER RULES. 3. One CI run shows the slowest line on the summary page (the coordinator reads it from the run). 4. The PR body's Contract states: the wrapper reads timing from the stream and writes the summary, signals nothing, and its exit status is the suite's or 124; what is left out: no `--jobs` (research section 3.3 item 4).

CLOSURE
parser-module: one reader of the Bats `cat` stream in `run-bats.py`, its line forms pinned by a recorded fixture; no second parser of the stream anywhere.

TRUST
TRUST: the unit trusts Bats 1.14.0's `cat` stream as the one source of test names, results and durations (the fixture records its spelling), and `GITHUB_STEP_SUMMARY` as a file the runner provides; it does not read the job log back and does not time tests itself.

TIMEBOX
60 minutes.

FORBIDDEN
No change to DEFAULT_BOUND or the budget constants' values; no signal to the Bats process; no `--jobs`; no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is made by the coordinator with `worker-worktree.sh`; every command runs with it as cwd. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U128-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U128-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification`, the line `Program-Unit: regime-cutover/U128`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the recorded suffix form, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `handoff/05-remediation-plan.md` row P-37; `handoff/research/03-ci-reliability.md` section 3 and V4-7; U99 (the wrapper's unit).
