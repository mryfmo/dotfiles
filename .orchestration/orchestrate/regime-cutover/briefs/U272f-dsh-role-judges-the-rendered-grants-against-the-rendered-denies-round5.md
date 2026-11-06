# U272f round 5 of U272: every rendered grant is judged against every rendered deny, nothing else is the boundary

GOAL
The round-4 audit of PR 697 (U272e, head d1ffd919; `verdicts/U272e-d1ffd919.md`) found one P1 of the same class as round 3: the refusal judged three inputs (`DSH_HOME`, the scratch cwd, the state slot) against the denies, and the profile root `~/.omp/profiles/dsh`, which the role also renders into `allowWrite`, was not among them; a profile directory linked to `~/.aws` was granted write. The mechanism-change row of 2026-11-06T15:2xZ removes the input list. From this round the refusal reads the role's rendered settings as its only source: every path of the final `allowWrite` and `allowRead` lists, resolved physically and compared by (device, inode) identity where the path exists, against every path of the final `denyRead` and `denyWrite` lists; a grant that equals, contains or lies inside a deny refuses the launch by name before any directory is made, except the two tagged structural rows the omp roles need (the own slot re-opened under the seats-root deny, the project files under the cwd), which stay tagged where they are rendered and are judged by their tag. Two P2 also close: when the slot removal fails under a signal, `set -e` ends the handler before the signal status is restored (the launch exits 1 with a slot left, instead of the signal's status with the slot named); the new `physical_each` batched reader has no failure-injection test.

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at d1ffd91939e4d069b01d0e4d467c12eff971a944 in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `scripts/orchestrator/hcom-seat` and the deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical), the pin rows by regeneration, `tests/unit/test_hcom_seat.py` (only the failure-injection test for `physical_each`), `tests/unit/test_hcom_seat_dsh.py`, `docs/deepseek-harness.md` (one sentence), `../U272-design.md` (the rule), and the body `../U272-pr-body.md` (a Round 5 section, the Contract's refusal sentence, the threat rows). Not: the omp roles' rendered settings (byte-identical to d1ffd919, the comparison test extended).

CONTEXT
Read the verdict whole, round 4's refusal function and its three call sites, the settings rendering (where `allowWrite` and `allowRead` are assembled for the dsh role, including the profile root and the pinned tool directory), the tags round 4 added, the signal handler and the slot removal, and `physical_each` with the existing `test_every_batched_producer_fails_closed`. The rule's input is the rendered arrays (or the written settings file read back); the function that judges them replaces the three call sites with one call after rendering and before any mkdir.

DATA SHAPE
One judge over two tables: grants (each row: path, kind allowRead or allowWrite, tag or none) and denies (each row: path, kind); every path physical; the judge returns the first (grant, deny) pair that overlaps and is not exempted by a tag; the launch refuses naming both paths. The signal handler runs the cleanup under `set +e` (or in a function whose status is read), then restores the signal status; a slot that remains is named and the exit is 2 whatever the signal. `physical_each` gets the same failure-injection coverage as `physical_paths` (a failed batch, an empty batch, a short batch each refuse).

CHANGE
1. The judge and its one call site, the three input checks removed; the handler; the test coverage; the design file and docs sentence.
2. Tests: `~/.omp/profiles/dsh` as a link to a denied directory refuses before mkdir (recorder: no mkdir); a grant row added to the fixture under any deny refuses (a parametrised test over each deny path of the fixture); `DSH_HOME` on `~/.aws` and `~/.omp/agent` still refuse (round 4's cases); SIGTERM with a read-only `.state` exits 2 naming the slot (not 1); `physical_each` failure injection; the omp roles byte-identical to d1ffd919; the existing tests stay.
3. Measurement on this host (scratch `DSH_HOME` and a scratch `HOME` under `/tmp` as U272 did): a profile root linked to a scratch `.aws` is refused by name and the scratch seats root stays empty; `--version` prints `0.2.1-rc.5`; SIGTERM with a read-only scratch `.state` exits 2 with the slot named; paste.
4. The body's Round 5 section quoting the three findings with each one's change and test; the Contract's refusal sentence states the rule's source (the rendered grants against the rendered denies) and the two tagged exemptions; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `make render-check` exit 0.
4. The CHANGE 3 measurements pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs the audit at the new head.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the rendered settings as the role's one boundary statement and judges its grants against its denies; it changes no omp role's rendered settings, reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the omp roles' rendered settings; no new input list for the refusal; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.aws`, `~/.local/state/omp-seats` or `~/Workspace`; no `/v1/messages` request; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272f/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272f-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U272f-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Model the Domain: the rendered tables are the boundary; Subtract Before You Add: the input list goes).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the rule in one line, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 36, 44, 46); the mechanism-change row of 2026-11-06T15:2xZ; `verdicts/U272e-d1ffd919.md`; `briefs/U272-hcom-seat-dsh-role.md`; `../U272-design.md`.
