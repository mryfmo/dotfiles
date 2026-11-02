# U133 rounds-check counts a unit's rounds per pull request

GOAL
Standing order 36 caps the audit rounds of one change: three audit rows without a mechanism-change row, or two `incorrect` rows of one class after the latest one, refuse the next audit. `scripts/orchestrator/rounds-check.py` counts those rows per unit. The records unit U20 is one unit with a new pull request per sync, so three `correct` syncs read as three rounds of one change: sync 16 (U126 cap, 2026-10-31T04:51Z) and sync 20 (U20 cap, 2026-10-31T10:25Z) were refused with no `incorrect` row at all, each costing a superseded PR and a mechanism-change row that changed no mechanism (decisions rows of those timestamps). The rule's premise is one pull request per change, so the count moves to the pair (unit, pull request); mechanism rows stay per unit.

SCOPE
One branch `feat/rounds-check-per-pull-request` from `origin/main`. May write: `scripts/orchestrator/rounds-check.py`, `tests/unit/test_rounds_check.py`, `scripts/orchestrator/README.md` (the rounds-check paragraph and row), `AGENTS.md` (the one clause of the round-cap bullet, line 72, that says when the count starts), `home/dot_agents/agent-config.yaml` (the pin, by the generator), `scripts/generated-agent-outputs.json` (by the generator), and `home/dot_local/bin/common/executable_rounds-check.py` if the generator produces one.

CHANGE
1. (Round 2, after Codex thread 4437730129 on PR 623 showed that a per-pull-request key lets a unit reset its count by opening a new pull request.) The counted audit rows for a unit are the unit's rows after its latest merge row (a ledger row whose `verifier` is `pr-merge.sh`), across every pull request; a merge ends a change, a new pull request does not. Rows before that merge row are read for shape and counted for nothing, as rows before `RULE_EFFECTIVE` are today. The mechanism rows stay the unit's; the strikes count `incorrect` rows of one class after the latest mechanism row and after the latest merge row. `--pr <n>` and `--all` keep their shapes; a unit's line names the merge row it counts from (`U20 allowed: 1 audit rows (0 incorrect) since the merge of 2026-11-01T22:26:11Z, ...`) or `since the start`.
2. The docstring, the README paragraph, the `ROW_TO_WRITE` hint and the one clause of `AGENTS.md` line 72 say the same thing: a unit's rounds are counted since its last merge, because a merge ends a change and a new pull request does not.
3. Tests, behaviour only: a unit with three `correct` rows each followed by its merge row is allowed on a fourth (the records unit); a unit with two audit rows on pull request 1, no merge, then two on pull request 2 is refused on the fourth without a mechanism row (the Codex scenario); three audit rows on one pull request are refused; two `incorrect` rows of one class after the mechanism row refuse whether on one pull request or two; a merge row resets both the cap and the strikes; rows with `pr` `-` and merge rows themselves are never audit rows; `--all` prints one line per unit and refuses when any is refused. Rewrite the round-1 pair tests to this rule and say so in the body.
4. Red proof: on a `git archive` of `origin/main`, the store as of this head with the U20 mechanism row of 2026-10-31T10:25:42Z removed refuses U20 (three correct syncs read as three rounds); this head allows it (each sync's merge row ended its change). A second red proof on this head's own scratch fixture: the Codex scenario is refused here and was allowed by round 1 (`git archive` of 5e067c2d).

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_rounds_check tests.unit.test_filed_findings tests.unit.test_regime_ci` OK (paste the Ran line). 2. `uv run --no-config --no-project python -I scripts/orchestrator/rounds-check.py --all .orchestration/orchestrate/regime-cutover` exit 0 on the checkout's store. 3. ruff format check; `scripts/lint-comparisons.py --changed` exit 0; the generator check up to date. 4. The PR body's Contract states the counting key, what stays per unit, and what is left out: no change to the cap or the strike count, no exemption of any unit.

CLOSURE
allowlist: one counting key, (unit, pull request), spelled in one function; no unit is exempt and no number changes.

TRUST
TRUST: the unit trusts the ledger's `pr` column as the identity of a change and the body's `Program-Unit:` line as the unit; it does not read GitHub and trusts the coordinator to write one pull request per change.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `ROUND_CAP`, `STRIKES`, `RULE_EFFECTIVE` or the class vocabulary; no exemption list; no `gh` call; no edit to the live store or to any file outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U133-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U133-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines and the red proof), the line `Program-Unit: regime-cutover/U133`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing order 36); decisions rows mechanism-change of 2026-10-31T04:51:47Z (U126) and 2026-10-31T10:25:42Z (U20); the follow-up candidates row of 2026-10-31T12:21:10Z.
