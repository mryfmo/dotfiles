# U127 One Bats for hosts and CI (plan P-33, research V4-6)

GOAL
Hosts run Bats 1.14.0 from the reviewed pin in `home/dot_mise/config.toml` (`[tools."http:bats"]`, version 1.14.0, sha256 pinned), while CI installs whatever the image's package manager has: `apt-get install -y bats` in `.github/workflows/test.yaml` (1.10.0 on ubuntu-24.04, 1.13.0 on ubuntu-26.04) and `brew install bats-core` in `test.yaml` and `macos.yaml` (1.14.0 today, unpinned). Bats 1.14.0 made `run` honour `set -e`, a documented breaking change (research 03-ci-reliability.md section 3), so a test can pass under 1.10.0 in CI and fail on a host or the reverse, the ShellCheck skew of U97 again. U97 closed that class for ShellCheck and shfmt with `scripts/ci/install-pinned-lint-tools.sh` and `scripts/ci/pinned-tool-version.sh` reading the one pin; this unit adds Bats to that set, so every CI row and every host runs the same Bats and the version is checked before a suite runs.

SCOPE
One branch `ci/one-bats-for-hosts-and-ci` from `origin/main`. May write: `.github/workflows/test.yaml` (the apt and brew install lines lose `bats` and `bats-core`; the "Put the pinned ShellCheck and shfmt on PATH" step gains Bats), `.github/workflows/macos.yaml` and `.github/workflows/ubuntu.yaml` (the files-test jobs take Bats from the pin the same way; the dead commented install block in `ubuntu.yaml` is removed), `scripts/ci/install-pinned-lint-tools.sh` and `scripts/ci/pinned-tool-version.sh` (accept `bats` as a third tool), `scripts/run_unit_test.sh` (`run_bats` refuses any other Bats version through `pinned-tool-version.sh` before it runs; the rationale comment drops the 1.10.0 clause), `tests/unit/test_pinned_lint_tools.py`, `tests/unit/test_apt_mirror.py` only if an assertion names the install lines, and any `.bats` test that fails under 1.14.0 because `run` now honours `set -e` (fixed in the test, never by relaxing the pin).

CHANGE
1. `install-pinned-lint-tools.sh` installs `http:bats` 1.14.0 from the mise pin beside ShellCheck and shfmt; `pinned-tool-version.sh` accepts `bats` with the prefix `Bats ` and compares `bats --version` with the pin's version by value. Tests in `test_pinned_lint_tools.py` for the third tool (installed, wrong version refused, absent refused, the version line's shape).
2. `test.yaml`: the step that puts the pinned ShellCheck and shfmt on PATH puts Bats there too, before the unit tests; `bats` and `bats-core` leave the apt and brew install lines. `macos.yaml` and `ubuntu.yaml` files-test jobs install the pinned Bats the same way (they already run mise-action with `install: true`); the `brew install bats-core` line and the commented block go.
3. `run_bats` in `scripts/run_unit_test.sh` runs `pinned-tool-version.sh ... bats` first and refuses with its message when the version differs (standing order 21: the read's status decides; a check that cannot run refuses).
4. Every `Run unit test` and `Test file existence` log prints `Bats 1.14.0` (the version line printed by `run_bats` before the suite).

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_pinned_lint_tools tests.unit.test_apt_mirror tests.unit.test_scratch_git` OK. 2. The lints of the WORKER RULES; `scripts/ci/masked-dirname-check.sh`, ShellCheck 0.11.0 and `shfmt -i 4 -sr -d` on the touched shell files; the workflow files pass `tests.unit.test_regime_workflow` and the existing workflow tests. 3. CI on the PR head: the four test jobs and the files-test jobs print `Bats 1.14.0` and pass (a failure under 1.14.0 is the skew made visible and is fixed in the same unit, in the test). 4. The PR body's Contract states: one Bats version on every CI row and host, read from one pin, checked before every suite; what is left out: hosts without mise keep the pin's instructions (`run_unit_test.sh` rationale, bats-core #1020).

CLOSURE
allowlist: the pinned-tool set is one closed list (`shellcheck`, `shfmt`, `bats`) read from one manifest by one installer and one version check; no second spelling of a version anywhere in CI.

TRUST
TRUST: the unit trusts `home/dot_mise/config.toml` as the one reviewed pin (version and sha256) and mise's http backend to fetch and verify it; it trusts `bats --version` as the installed version's report and does not read package-manager metadata; it trusts the U97 installer pattern as the form.

TIMEBOX
90 minutes.

FORBIDDEN
No pin relaxation (1.14.0 stays); no `--jobs` for Bats (research section 3.3 item 4); no change to `scripts/ci/run-bats.py` (P-37 owns it); no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is made by the coordinator with `worker-worktree.sh`; every command runs with it as cwd. Never `git stash`. No `/tmp` literal in tracked files. No local Bats run as evidence of CI (CI is the full-suite evidence); a local `bats --version` after the installer is fine.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U127-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U127-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification`, the line `Program-Unit: regime-cutover/U127`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, deviations, anything not verified. Under 20 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `handoff/05-remediation-plan.md` row P-33; `handoff/research/03-ci-reliability.md` section 3 and V4-6; the U97 unit (units.tsv) for the pattern.
