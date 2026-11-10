# U343n round 11 of U343 (test-only): the reaper test's two teardown budgets are the grace plus a slack the test measures on the same machine, so the slow macOS runner gets its own margin and this host's claim stays

GOAL
PR 720's head 3e25e940 has a correct audit (verdicts/U343m-3e25e940.md), a 0-finding sweep (run-69) and every CI check green but `test (macos-15, client)`, which failed twice on one line (attempts 1 and 2 of run 42802615459): `tests/unit/test_acp_broker.py::test_a_a_term_ignoring_worker_is_ended_by_the_reaper_and_holds_neither_the_slot_nor_the_record`, `AssertionError: the slot's removal did not happen within 7 s` at `:848` (`self.wait_for(..., seconds=GRACE + 2)`). The runner ran the module in 760 s and 573 s against about 150 s on this host, where the test passes; the three Ubuntu runners pass it. The reaper (acp-broker `connection_reaper`, `:1549-1566`) sends TERM, polls `kill -0` fifty times with `/bin/sleep 0.1` between (the grace of `reaper_grace=5` seconds is counted in iterations, each a fork, so on a slow machine it runs over five seconds), then KILLs, appends the exit line, removes the slot (`slot_remove`, an `rm -rf` of the worker's clone) and writes the record through the Python helper; the test's two seconds of slack after the grace cover the fork overrun and that teardown, which the macOS runner does not finish in time. The claim under test is the one the U343g brief fixed on this host: within the grace plus two seconds, the slot is gone and the record complete. This round keeps that claim where it was measured and gives a slower machine a slack it measures itself: the time the same test's connection setup (`held_connection`: the broker's clone, canary, omp start, record line and one echoed line, the same kinds of work as the teardown) took on that machine, never less than two seconds. The lever is not changed: a grace that runs a little long on a slow machine gives the worker more time, not less, and is documented at `:1506`.

SCOPE
The worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j` on branch `fix/acp-broker-round8` at 3e25e940cdf3617066912cd73f5986668f54fa2a (one new commit on top). May write: `tests/unit/test_acp_broker.py`, the one test named above and, if a helper is the cleanest form, one small helper beside `wait_for`. Non-goals: every lever, copy, pin and generated output (no lever changes); every other test; the PR body (the coordinator keeps it).

CONTEXT
`tests/unit/test_acp_broker.py:47` (`GRACE = 5`), `:525-530` (`wait_for`), `:536-544` (`held_connection`), `:831-871` (the test; the three budget sites are `:848` the slot's removal wait, `:850` the elapsed assertion after `recv_all`, `:866` the broker's end under `stop_broker` after a second held connection at `:859`). `GRACE` is used at those three lines alone. The reaper's loop: acp-broker `:1551-1564`; its documentation `:1505-1508`.

DATA SHAPE
One number per connection, `slack = max(2.0, setup_seconds)`, where `setup_seconds` is the wall time of the `held_connection` call that opened the connection whose teardown is measured; the budget of each teardown is `GRACE + slack` of its own connection (the first connection's slack for `:848` and `:850`, the second's for `:866`). The assertion messages print the measured elapsed time and the budget, so a failure names both numbers.

CHANGE
1. In the test, time each of the two `held_connection` calls (`time.monotonic()` around them) and derive `slack = max(2.0, setup)` for each; use `GRACE + slack` at `:848` (the `seconds=` of `wait_for`), `:850` and `:866` (the elapsed assertions), with messages of the form `f"the slot went in {elapsed:.1f} s, budget {GRACE + slack:.1f} s (setup took {setup:.1f} s)"`. Extend the docstring's "within the grace plus two seconds" to say the slack is two seconds or the connection's own setup time on the same machine, whichever is longer, and why (the macOS runner's two failures at 7 s with the module four to five times slower than this host; the reaper's grace is counted in forked sleeps, `acp-broker:1506`). 2. Measure on this host and paste: run the one test three times (`uv run --with pyyaml python -m unittest tests.unit.test_acp_broker.AcpBrokerTest.test_a_a_term_ignoring_worker_is_ended_by_the_reaper_and_holds_neither_the_slot_nor_the_record -v`), with a temporary print (removed before the commit) or the assertion messages' numbers read from a deliberately failing budget on a scratch copy, of `setup` and `elapsed` for both connections; the report states the three pairs. 3. `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker -v` OK; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `make render-check` exit 0. 4. Commit unsigned: `test(acp-broker): the reaper test's teardown budgets are the grace plus a slack the test measures on the same machine (its connection setup, at least two seconds), after two failures of the fixed seven seconds on the macos-15 runner (regime-cutover U343n, round 11)` ending with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker.AcpBrokerTest.test_a_a_term_ignoring_worker_is_ended_by_the_reaper_and_holds_neither_the_slot_nor_the_record -v` OK at the head on this host, pasted, with the three measured `(setup, elapsed)` pairs for the first connection and for the second (CHANGE 2) and one sentence saying whether `slack` was 2.0 on this host (expected: yes, setup under two seconds; if not, say what it was). 2. `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker -v` OK at the head, the `Ran N tests` and `OK` lines pasted. 3. `git diff --stat 3e25e940 HEAD` shows one file, pasted; `grep -n 'GRACE' tests/unit/test_acp_broker.py` pasted (the three sites use `GRACE + slack`; no other `GRACE + 2` remains). 4. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0 and `make render-check` exit 0, pasted.

VERIFY
ACCEPTANCE pasted into the report; the coordinator fetches the head by path, pushes it onto `feat/acp-broker-lever`, and CI (the macOS runner is the proof this host cannot give), the sweep and the audit under `--cyber-program daybreak_blue` run at it; then `pr-merge.sh`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the connection's own setup on the same machine as the measure of that machine's speed for the same kinds of work (process spawns, git, the file system), the two-second floor as the claim this host measured in U343g, and the macOS runner's CI result as the proof the budget fits there; it changes no lever and reads no store.

TIMEBOX
40 minutes.

FORBIDDEN
No change outside the one test (and one helper beside `wait_for` if used); no change to `GRACE`'s value; no lever change; no rebase; no `git stash`; no push; no `gh` call; no network; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u343n/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at the committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U343j`. Your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U343n-progress.txt` after each CHANGE step; final report to `/tmp/dotfiles-wt/U343n-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the head (40 hex), the ACCEPTANCE lines with the measured pairs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 44, 46, 49); decisions rows 2026-11-10T11:59:12Z and 12:37:46Z (the two macOS failures and the judgement); `verdicts/U343m-3e25e940.md`.
