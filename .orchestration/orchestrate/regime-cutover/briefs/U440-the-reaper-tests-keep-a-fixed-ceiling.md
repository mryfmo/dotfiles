# U440 the acp-broker reaper tests assert the behavior with a ceiling that does not depend on the runner's load

GOAL
End the flake of `tests/unit/test_acp_broker.py` on the macos-15 runner: `test_a_a_term_ignoring_worker_is_ended_by_the_reaper_and_holds_neither_the_slot_nor_the_record` failed PR 720 twice on 2026-11-10 (`did not happen within 7 s`, then the U343n calibrated slack) and PR 757 at 5ba30064 on 2026-11-11 (`the slot's removal did not happen within 9.07 s`; the module ran 920 s on the runner against about 150 s on this host). The tests keep every behavioral assertion (the slot goes, the record completes with `status=2 push=skipped`, the TERM-ignoring worker is dead, one exit line, the broker ends by its signal, the records go) and stop asserting a wall-clock bound derived from the setup time.

CONTEXT (measured)
- The reaper's grace is counted in forked `/bin/sleep 0.1` iterations (`scripts/orchestrator/acp-broker` line 1727: `for ((n = 0; n < reaper_grace * 10; n++))`), so on a loaded machine the grace stretches well past 5 s; the test's budget `GRACE + slack` with `slack = max(2.0, setup)` (lines 864, 888, 1303) assumes the setup's wall time predicts the iteration cost. Two fixes (the 2 s slack, then the calibrated slack) shared that premise and both failed the same gate (Attack the Premise). The premise is dropped: no bound derived from setup.
- Same pattern at lines 1303 to 1312 and 1326 (the second reaper test) and 1367 to 1368 (`GRACE + 2`, `GRACE + 2 + 30`).
- What the tests must still prove: the reaper does not hang (a TERM-ignoring worker is ended and the slot removed in bounded time) and the records are complete. A generous fixed ceiling proves "bounded" on any runner; the design value of the grace (5 s) is the lever's, not the test's, claim.
- The elastic grace itself (a KILL later than designed under load, never earlier) is a lever defect of its own, filed as U441 (planned: the grace counted by the wall clock in acp-broker). Not this unit.
- Standing order 49: fix the defect through the test, no review round.

DATA SHAPE
A ceiling is one module constant, `REAPER_CEILING` (seconds, a generous fixed value such as 60, the `wait_for` default), used by every reaper-timing wait and bound in the module; the `slack`/`setup` derivation is deleted. Asserting "within the ceiling" states the behavior (bounded) and the message prints the measured elapsed time for the record.

CHANGE
1. Red first: at 5b99f2c3 the tests pass on this host (they fail only on the loaded runner), so the red run is not a failing test but a demonstration: paste the three current budget lines (`GRACE + slack` sites) with `git grep -n 'GRACE + slack' -- tests/unit/test_acp_broker.py` as the before state.
2. `tests/unit/test_acp_broker.py`: add `REAPER_CEILING = 60` beside `GRACE`; in the three tests replace each `wait_for(..., seconds=GRACE + slack)` and `GRACE + 2` wait with `seconds=REAPER_CEILING`; replace each `assertLessEqual(elapsed, GRACE + slack, ...)` and the `GRACE + 2 + 30` bound with `assertLessEqual(elapsed, REAPER_CEILING, f"... in {elapsed:.1f} s, ceiling {REAPER_CEILING} s")`; delete the `setup_started`, `setup` and `slack` lines that no longer feed anything; rewrite the docstrings' slack paragraphs to say why the ceiling is fixed (two sentences at most, naming the runner measurement and U441 for the lever's grace). Keep every other assertion.
3. Run `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker -v` to a file; paste `Ran N tests` and `OK`. Lints: `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `python3 -I scripts/lint-comparisons.py tests/unit/test_acp_broker.py` exit 0 if the tool accepts the path (else say so).
4. Body draft `/tmp/dotfiles-wt/U440-pr-body.md`: Summary, Contract (what the tests still prove; what they no longer claim), Threat table with the one changed path (`| row | risk | status | evidence |`: the risk is a reaper that hangs and a test that no longer notices; closed by the ceiling and the behavioral assertions), Verification (the pastes), last line `Program-Unit: regime-cutover/U440`.
5. Commit unsigned: `test(acp-broker): the reaper tests keep a fixed ceiling, not a budget derived from the runner's setup time (regime-cutover U440)` with the footer `Program-Unit: regime-cutover/U440`.

ACCEPTANCE
1. `git grep -n 'GRACE + slack\|GRACE + 2' -- tests/unit/test_acp_broker.py` prints nothing at the new head; `git grep -n 'REAPER_CEILING'` prints the constant and its uses.
2. `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker -v`: `Ran N tests`, `OK` at the new head (N equal to the count at 5b99f2c3), pasted.
3. ruff format --check exit 0, pasted.
4. Tree clean; one commit on 5b99f2c3.

VERIFY
ACCEPTANCE pasted into the report; the coordinator pushes, audits, sweeps, runs CI (the macos-15 leg is the proof), merges, then moves PR 757 onto the new main.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the reaper's behavior as the merged lever implements it and the module's existing fixtures; it changes one test module, no lever, no grant.

TIMEBOX
40 minutes.

FORBIDDEN
No change outside `tests/unit/test_acp_broker.py`; no lever change; no rebase, amend or stash; no push; no `gh` call; no network; no pipe `|` in any bash command (standing order 46: outputs under `/tmp/u440/`); a progress line at `/tmp/dotfiles-wt/U440-progress.txt` within five minutes and at least every 10 minutes after.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at the committed head in the tree `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U440`. Your final line is the Task return.
- Final report to `/tmp/dotfiles-wt/U440-report.txt`; the body draft to `/tmp/dotfiles-wt/U440-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the head (40 hex), the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 44, 46, 49); decisions 2026-11-10T11:59:12Z, 2026-11-10T12:37:46Z and 2026-11-11T02:15:12Z (the flake's three failures); `tests/unit/test_acp_broker.py:842-903`, `:1295-1330`, `:1360-1370`; `scripts/orchestrator/acp-broker:1720-1735`.
