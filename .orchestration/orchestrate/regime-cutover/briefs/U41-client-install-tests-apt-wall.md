# U41 The docs-PR wall is the apt installs inside the client Bats suite — brief

GOAL
A docs-and-skills PR's wall time is bound by the "Run unit test" Bats step of the `test (ubuntu-24.04, client)` cell (U39 measured 210 s, about 180 s of real `apt-get install` runs inside `tests/install/ubuntu/client`). After this unit that step costs what the shell logic costs, and the real installs run only where a real install is the thing under test. The measurement comes first: which cases need a real install, which only check the command the installer builds.

SCOPE
One branch `ci/client-install-tests-apt-wall` from `origin/main` (4f7b55f9 or later, U39 in it). May write: `tests/install/ubuntu/client/*.bats` and their helpers under `tests/install/` (stubs for `apt-get`/`dpkg` where a case checks the built command, a shared `install_real_packages` marker for the cases that keep installing), `.github/workflows/test.yaml` only for an apt archive cache step (`actions/cache` on `/var/cache/apt/archives` keyed by the client package list) if the measurement shows real installs must stay, `tests/unit/test_ci_workflows.py` for that step's pin, `README.md` one paragraph in the CI section. Nothing else; no change to the installers themselves.

CONTEXT (measured by U39, PR #493 self-check issuecomment-6383233202 and ADDENDUM 2 run 40088677832 after the merge)
- `test (ubuntu-24.04, client)` after U39: Bats "Run unit test" step 210 s, of which `PACKAGES for misc` 65 s, `misc` 57 s, `ghostty` 22 s, `docker` 20 s are apt installs on the runner; the Python shards run in 161 s on macOS and less on Ubuntu; the bun step 29 s.
- `tests/install/ubuntu/client/` cases call the installers under test with the real `apt-get`; a case that asserts the installed package set must install; a case that asserts the command line, the repository file or the key path does not.
- The cache route: GitHub's `actions/cache` restores `/var/cache/apt/archives/*.deb` in about 10 s for a few hundred MB; `apt-get install` then unpacks without downloading (the unpack still costs; measure).

ACCEPTANCE
1. A table in the PR body, one row per client case that runs apt today: seconds today (from the run log), what it asserts, and the disposition (`stub`: the command is asserted against a recorded `apt-get` invocation; `real`: it stays, with why), pasted from a run of the suite with `BATS_...` timing or `time` per file.
2. The `real` rows run against a cached apt archive if the sum of their seconds stays above 60 s after the stubs; otherwise no workflow change (say which, with the number).
3. CI on the PR head: the Bats step of the client cell measured before and after (seconds pasted from both runs' step logs), the same test names present in both logs (no case silently dropped: `grep -c '^ok'` equal or explained), every stubbed case still fails when its installer builds a wrong command (one mutation per stubbed file, pasted).
4. PR body `Program-Unit: regime-cutover/U41`, the threat table (the stubs must not mask an installer that stops installing: name the case that still proves a real install per installer group), the footer; pre-RESULT five-point self-check; orchestrator verdict (a test-only change with the measured step times as the evidence), audit seat only if the workflow changes.

TIMEBOX
3 hours. If the measurement shows that fewer than 30 s can be saved, stop after ACCEPTANCE 1 and report the table as the result.

FORBIDDEN
No `continue-on-error`, no skipping cases by name, no change to `install/**`, no local Bats runs reported as evidence (AGENTS.md: the Bats results of record are the CI jobs; local runs are for your own iteration only and are not pasted); no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line at push time (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).
