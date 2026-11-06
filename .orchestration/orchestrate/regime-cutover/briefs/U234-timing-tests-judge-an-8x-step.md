# U234 the two linear-time tests of the secret scanner judge an 8x size step with interleaved runs, so runner jitter cannot reach the bound

GOAL
`tests/unit/test_validate_agent_assets.py` holds two complexity tests, `test_a_generic_rule_scans_a_padded_line_in_linear_time` (`:2773`) and `test_the_report_of_many_findings_in_one_file_is_linear_in_the_findings` (`:2909`). Each judges a 4x size step (8,000 to 32,000) against a growth bound of 12 and a 20 s hang cap. The bound has failed on healthy linear code four times on GitHub's shared runners (the rows of 2026-11-03T09:41:48Z and 2026-11-06T04:55:18Z; the last at 13.4x per 4x step after 920 s of a loaded shard run), each costing a CI cycle, an empty commit and a carried row. The distance between linear (4x) and the bound (12x) is three, and a load burst on the larger size alone crosses it. This unit widens the judged step to 8x (8,000 to 64,000), where linear is 8x and quadratic is 64x, sets the bound to 24 (three times linear, less than half of quadratic), and interleaves the sizes across the repetitions so a burst hits both sizes alike. The tests keep failing a quadratic scan and stop failing a slow runner.

SCOPE
A new branch `test/timing-tests-judge-an-8x-step` from `origin/main` at the head the TASK names (your tree is positioned on it). May write: `tests/unit/test_validate_agent_assets.py` (the two tests and their docstrings) and the body file `/tmp/claude/U234/U234-pr-body.md`. Nothing else: no scanner code, no other test.

CONTEXT
Read both tests whole (`:2773-2850`, `:2909-2974`). The padded-line test runs three sizes (2,000, 8,000, 32,000) for two padding kinds and three forms, least of five per size, judges the 8,000-to-32,000 step and caps each run at 20 s; the report test runs two counts (8,000, 32,000), least of five, judges the step and caps at 20 s. Both docstrings record the measured history (rounds 7 to 10, U165, the 2026-11-04 runs) and the reason the bound is a growth ratio and the cap a hang detector. Measured on this host and the runners in those docstrings: linear steps 3.8x to 4.1x locally, up to 9.2x on runners for a 4x step at 32,000; a 128,000-character run took 2.5 s on a runner against 0.2 s locally, so a 64,000 run fits the 20 s cap with a wide margin.

CHANGE
1. Padded-line test: sizes (2,000, 8,000, 64,000); judged step (8,000, 64,000); `growth_bound = 24`; the five repetitions run the sizes interleaved (for each repetition, every size once, in order), and the least per size is judged; the hang cap stays 20 s; the correctness assertions stay per size.
2. Report test: counts (8,000, 64,000); `growth_bound = 24`; repetitions interleaved the same way; the hang cap stays; the per-count assertions stay (the count of findings and the first and last line).
3. Docstrings: one added paragraph each, in the existing voice, recording this change and its reason (the four runner failures, the 8x step, the bound at three times linear and under half of quadratic, interleaving), with the dates and run ids from the rows named in GOAL.
4. Measure before you commit and paste into the body: both tests run five times on your seat (`uv run python -m unittest tests.unit.test_validate_agent_assets -k linear -v`), the per-run growth ratios printed by adding them to the assertion messages (they already are), so the body shows the linear ratios at the new step.
5. The body: Summary (the flake record, the change), Contract (guarantee: a quadratic scan at these sizes still fails both tests, a linear scan on a runner three times slower on the larger size still passes; leaves out: the scanner code, every other test; `TRUST:` sentence as below), a Threat table `row | risk | status | evidence` with one row for the test file, one for the non-path control (the bound and the step), and an `orchestrator effect` row, each `closed`, and `Program-Unit: regime-cutover/U234`.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_validate_agent_assets -k linear -v` OK, five runs, the ratios pasted.
2. A negative check pasted: in a scratch copy of the test module (under `$TMPDIR`), temporarily replace the judged scan of the padded-line test with a quadratic stand-in (for example `text.count` inside a loop over the line's characters) and show the step assertion fails with a ratio above 24; the scratch copy is not committed.
3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0; `make format` leaves no diff.
4. `git diff --stat origin/main` names `tests/unit/test_validate_agent_assets.py` alone.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section; CI on the head runs the module on every cell.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the scanner as it stands on origin/main and the measured linear ratios in the tests' own docstrings; it changes the judged sizes, the bound and the repetition order of two tests, no production code, and reads no network.

TIMEBOX
30 minutes.

FORBIDDEN
No change to `scripts/validate-agent-assets.py` or any other file; no removal of the hang cap or the correctness assertions; no `skip`; no local bats; no network read; no push; no `gh` call; no mention of any private design directory; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 46 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U234/U234-progress.txt` every ten minutes at most.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body at `/tmp/claude/U234/U234-pr-body.md` per CHANGE 5.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), `git diff --stat origin/main`, the ACCEPTANCE result lines with the ratios, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 27, 29, 34, 35, 41, 42); `AGENTS.md` (Test Policy, Comment Policy); the decisions rows of 2026-11-03T09:41:48Z and 2026-11-06T04:55:18Z.
