# U210 every test of the Ubuntu client misc installer runs with a fake `snap` first on PATH, so the unit-test leg never reaches the snap store

GOAL
CI's `test (ubuntu-24.04, client)` and `test (ubuntu-26.04, client)` legs timed out (exit 124 of the step) on PR 666 at 445a2d22 on 2026-11-05: the process tree the runner printed at the kill shows `bats-exec-test ... tests/install/ubuntu/client/...` running `bash ./install/ubuntu/client/misc.sh` running `sudo timeout --kill-after=30 600 snap install chromium` for nine minutes, the real snap client against the real store, whose latency that day also failed the `public-bootstrap (ubuntu-24.04, client)` leg four times. The tests of `tests/install/ubuntu/client/misc.bats` that exercise `install_chromium` use `fake_snap` (`:90-111`), but the tests that run the script's `main` or the script as a program (the `install_misc` tests with the recorded `apt-get`, `:1-88`, among them the mutant test at `:74-88`) run `install_chromium` too, with whatever `snap` the runner has: on an Ubuntu runner the real one. A unit test that reaches a third-party store is a fixture leak, and its cost is the whole leg when the store is slow. After this head every test of that file (and of any other file under `tests/install/ubuntu/client/` that runs the misc script's `main`) has a fake `snap` first on PATH that records its call and succeeds at once, the recorded call is asserted where `main` runs (so the fake is proven to be the one reached), and no test can reach `snap` on the host.

SCOPE
A new branch `test/misc-bats-fake-snap` from `origin/main` ba051b0d. May write: `tests/install/ubuntu/client/misc.bats`, `tests/install/helpers/*` only if a shared helper is the right place for the fake (say which), any other `tests/install/ubuntu/client/*.bats` that runs `install/ubuntu/client/misc.sh` as a program. Nothing else; `install/ubuntu/client/misc.sh` is not yours.

CONTEXT
Measured 2026-11-05. `misc.bats:59-65` runs `install_chromium` with `PATH=${BATS_TEST_TMPDIR}` (no snap: the no-op case); `:90-111` `fake_snap` writes `${BATS_TEST_TMPDIR}/bin/snap` logging to `SNAP_CALLS` and `run_install_chromium` puts that bin first on PATH; `:113-137` the three install_chromium tests use them; the `install_misc` tests before `:59` (the `apt_record` helper fakes `apt-get`, `load "../../helpers/apt_record"`) run the script's `main` (`misc.sh:83-86`: `install_misc` then `install_chromium`) with the host's PATH after the recorded apt, so `command -v snap` finds the runner's snap and `sudo timeout ... snap install chromium` runs for real (`misc.sh:61-66`; `sudo` is passwordless on the runner). CI's log of the timed-out step (run 42068892022, job 127390927595) shows the tree. The repository's test policy forbids workers from running bats locally; CI is the proof, and today it is blocked by the same store, so this unit's own CI may wait for the store to recover.

CHANGE
1. One fixture for the whole file: a `setup` (or the apt helper's setup, if that is where `PATH` is already built) that writes a fake `snap` into `${BATS_TEST_TMPDIR}/bin` (log the argv to `${BATS_TEST_TMPDIR}/snap_calls`, exit 0) and puts that bin first on PATH for every test; `fake_snap` becomes the per-test override of the fake's behaviour (exit code, hang) on the same path, so the three `install_chromium` tests change only in where the fake comes from.
2. Every test that runs `main` or the script as a program asserts afterwards that `snap_calls` holds exactly one `snap install chromium` line (the fake was the snap reached), and the no-op test keeps its empty PATH.
3. A guard against the leak returning: one test runs `main` with a `snap` fake that exits 99 on `install` and asserts the recorded call and the status the script returns, so a future test that forgets the fake is visible by the fake's absence in `snap_calls`.
4. The PR body (`../U210-pr-body.md`): Summary (the leak and the day's timeout), Contract (no test of the file can reach `snap` on the host; the fake records every call), a Threat table with four columns `row | risk | status | evidence` and one row per changed path plus an `orchestrator effect` row (the unit-test legs stop depending on the snap store), Verification with the ACCEPTANCE lines, the footer `Program-Unit: regime-cutover/U210`.

ACCEPTANCE
1. `grep -c 'snap' tests/install/ubuntu/client/misc.bats` printed before and after (paste both). 2. `shellcheck -x` is not run on `.bats`; `bash -n` cannot parse bats; so: `grep -n 'fake_snap\|snap_calls\|PATH=' tests/install/ubuntu/client/misc.bats` pasted whole, and a reading of each `@test` that names which snap it reaches (paste the list: test name, snap reached). 3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0 (it reads shell files; `.bats` may be skipped, say so). 4. `git diff --stat origin/main` names SCOPE files alone.

VERIFY
CI's `test (ubuntu-24.04, client)` leg is the proof (the bats run there); the coordinator reads it. The worker pastes the ACCEPTANCE lines into the body's Verification section.

CLOSURE
remove

TRUST
TRUST: the unit trusts the bats harness's PATH handling and `${BATS_TEST_TMPDIR}` as the per-test isolation, and `misc.sh` as it is; it changes no installer, removes the unit tests' reach to the snap store, and reads no network.

TIMEBOX
30 minutes.

FORBIDDEN
No change to `install/ubuntu/client/misc.sh`; no local bats run; no network read; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/U210`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the coordinator names in your task.
- Progress line beside your tree (`../U210-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U210-pr-body.md`) per CHANGE 4.
- Comments explain a non-obvious why only, no phase narration. Tests assert behaviour the user observes.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 33); `AGENTS.md` Test Policy and Audit sections; gates.md G-28.
