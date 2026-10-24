# U42 An unpinned `latest` npm tool turned `main` red; pin the statusline tools — brief

GOAL
`main` CI is green again and cannot turn red from an upstream npm release the repository never chose: the statusline tools that the CI smoke test executes are pinned to versions that exist and run on both runner platforms, the pin lives in the manifest-of-record (`home/dot_mise/config.toml`), and the smoke test's failure message names the pin to bump. Every open PR inherits the fix through its next `origin/main` merge.

SCOPE
One branch `fix/pin-statusline-npm-tools` from `origin/main` (50cde130 or later). May write: `home/dot_mise/config.toml` (the `npm:ccusage` and `npm:ccstatusline` lines, versions pinned; every other `latest` npm line only if the same smoke test executes it), `tests/unit/test_statusline_tools.py` (pin the version strings and the failure message), `.github/workflows/test.yaml` "Smoke-test statusline tools without network" step only if the message needs the pin name, `README.md` one sentence where the statusline tools are documented. Nothing else; no change to the statusline scripts themselves.

CONTEXT (measured 2026-10-24T10:5xZ)
- `main` run 40087404553 ("Unit test" workflow on 50cde130, the U37 merge) failed in all four `test` jobs at the step "Smoke-test statusline tools without network" (`.github/workflows/test.yaml:253-265` on `origin/main`): `~/.local/share/mise/installs/npm-ccusage/latest/bin/ccusage --version failed with 1: ccusage native binary is not available for linux-x64. Reinstall ccusage so optional native dependencies …` (job 120853039189). The PR CI at 2babd4b7 had passed 14/14 about 15 minutes earlier, so the breakage arrived with an upstream release between the two runs, not with the diff.
- `home/dot_mise/config.toml:29-36` installs `npm:ccusage = "latest"`, `npm:ccstatusline = "latest"` and six other npm tools at `latest`; mise's npm backend installs without the optional native dependencies the new ccusage release requires on linux-x64 (the message says so).
- `tests/unit/test_statusline_tools.py` is the unit test of the statusline tools; the CI smoke step installs the two tools into `${RUNNER_TEMP}/statusline-mise` and runs `--version` through `mise which`.
- Three program PRs are open or about to be (U27 #495, U39 #493, U36) and each runs the same step, so the red spreads to every PR until the pin lands.

ACCEPTANCE
1. `npm:ccusage` and `npm:ccstatusline` pinned to exact versions that install and answer `--version` on ubuntu-24.04 and macos-14 (measure: the previous green run 40086677434 or the PR 2babd4b7 runs resolved which versions; `mise ls-remote npm:ccusage` or the npm registry's version list, read-only, gives the candidate; paste the chosen versions and why).
2. The smoke step's failure message, when a tool fails, names the `home/dot_mise/config.toml` pin to bump (one printf before the existing exit); `tests/unit/test_statusline_tools.py` pins the two version strings so a silent drift back to `latest` fails a test.
3. CI green on the PR head including the four `test` jobs; `make validate-agent-assets` and `make render-check` unchanged.
4. PR body `Program-Unit: regime-cutover/U42`, the measured cause (job 120853039189 excerpt), no threat table needed (a version pin; say so), the footer; pre-RESULT five-point self-check; orchestrator's own verdict (the green `test` jobs are the evidence) and merge first, before any other open PR, so they can merge `origin/main` and pass.

TIMEBOX
45 minutes.

FORBIDDEN
No `continue-on-error`, no skip of the smoke step, no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line at push time (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).

ADDENDUM (orchestrator-sari, 2026-10-24T11:0xZ, worker question bus row 5176)
1. SCOPE edge granted: `tests/unit/test_supply_chain_policy.py` (`test_mise_tools_track_latest_behind_the_cooldown`, lines 354-390 on `origin/main`) keeps a closed `held` dict of pinned mise tools and fails on any pin outside it; add exactly `npm:ccusage` and `npm:ccstatusline` to that dict, nothing else in the file. The same test requires a one-line `# ` reason comment directly above each pinned line in `home/dot_mise/config.toml`; write the measured cause there.
2. Cause as measured by the worker: ccusage 20.0.38 (published 2026-10-21T10:49:51Z) cleared the 72h `minimum_release_age` cooldown at 2026-10-24T10:49Z, between the green PR run at 2babd4b7 and the main run on 50cde130; mise's npm backend installs it without the optional native binary it needs on linux-x64. 20.0.39 clears the cooldown about 17:22Z the same day, so waiting is no fix. Pins accepted: ccusage 20.0.37, ccstatusline 2.2.32, the versions run 40086677434 ran green on every runner.
