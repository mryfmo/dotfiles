# U343d: the broker test's real dsh launch places the profile overlay hcom-seat requires since U310

GOAL
After main 6ad1be23 was merged into PR 720's branch (the merge commit at the tree's HEAD in `/tmp/dotfiles-wt/U343`), the merged tree runs 415 tests with one failure: `tests/unit/test_acp_broker.py::AcpBrokerTest::test_the_worker_settings_are_the_dsh_row_but_the_named_rows` (line 764) starts a real `hcom-seat dsh` in a scratch HOME to take the dsh row's settings as the reference, and main's hcom-seat (U310, PR 708) now refuses that launch: `hcom-seat: profile config overlay absent or a symbolic link: <scratch home>/.agents/omp/profiles/dsh.yml`. The fixture predates the requirement. `tests/unit/test_hcom_seat_dsh.py` on main already builds that overlay for its own launches (search `placed_overlay`, `dsh.yml`, `.agents/omp/profiles` in that module); the broker test takes the same helper or the same file so the reference launch runs as main's lever expects. No lever changes.

SCOPE
The same branch `feat/acp-broker-lever` and PR 720; the tree is `/tmp/dotfiles-wt/U343` at the merge commit (clean). May write: `tests/unit/test_acp_broker.py` (the fixture of the reference launch: the overlay file in the scratch HOME in the form test_hcom_seat_dsh.py uses, imported from that module if it exposes it, else the same bytes), and the body `../U343-pr-body.md` (one sentence under `## Round 2` naming the merge and this fixture). Not: hcom-seat, acp-broker, acp-seat, any behaviour.

DATA SHAPE
One scratch-HOME file the reference launch needs, written by the fixture before the launch, equal to what test_hcom_seat_dsh.py writes for its launches.

CHANGE
1. Run the one test to see the refusal (red). 2. The fixture. 3. `uv run --with pyyaml python -m unittest tests.unit.test_acp_broker tests.unit.test_hcom_seat_dsh -v` OK. 4. `uv run ruff format --check tests/unit/test_acp_broker.py`; `scripts/lint-comparisons.py --changed`. 5. Commit `test(acp): the broker test's reference dsh launch places the profile overlay hcom-seat requires since U310 (regime-cutover U343d)` with the trailer. 6. The body sentence.

ACCEPTANCE
1. The test's red line at the merge commit and its green line at the head. 2. The two modules OK with counts. 3. ruff 0; lint-comparisons 0. 4. `git diff --stat <merge commit> HEAD` shows the one test module.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts test_hcom_seat_dsh.py's overlay fixture as the shape main's lever expects; it changes a test fixture and nothing a user runs.

TIMEBOX
15 minutes.

FORBIDDEN
No lever change; no behaviour change; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u343d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U343`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U343d-progress.txt`; final report to `../U343d-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the red and green lines, the ACCEPTANCE lines. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U343c brief; `tests/unit/test_hcom_seat_dsh.py` (the overlay fixture).
