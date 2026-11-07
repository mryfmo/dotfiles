# U330 pr-merge.sh requires the Unit test checks by name, so a head whose pull_request workflows never ran cannot merge

GOAL
On 2026-11-07 PR 708's head 792604f9 conflicted with main, GitHub ran none of its `pull_request` workflows (Unit test, Agent assets, Apply check, Docs build, Snippet install), and `gh pr checks` listed three passing checks: `regime` (a `pull_request_target` workflow), GitGuardian and CodeRabbit (skipping). `pr-merge.sh`'s CI gate (`scripts/orchestrator/pr-merge.sh:906-927` at 668ba887: at least one check, every bucket `pass` or `skipping`) would have merged that head with no test leg run (decisions row 2026-11-07T01:45:00Z). The gate must know which checks a merge needs and refuse when one is missing, not only when one is red.

SCOPE
A new branch `fix/pr-merge-requires-the-test-checks-by-name` from `origin/main` 668ba887; the tree is `/tmp/dotfiles-wt/U330`. May write: `scripts/orchestrator/pr-merge.sh` and its byte-identical copy `home/dot_local/bin/common/executable_pr-merge.sh`, `tests/unit/test_pr_levers.py` (or the module that tests pr-merge.sh today; read it first), `scripts/orchestrator/README.md` (the pr-merge.sh paragraph, one sentence), the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (by `uv run --with pyyaml python scripts/generate-agent-configs.py` only), and the body `../U330-pr-body.md`. Not: any other lever, the workflows, the ruleset.

CONTEXT
Read `pr-merge.sh` whole, its header (the CI paragraph at lines 71 to 76) and the gate at lines 906 to 927; read how the lever's tests fake `gh` (a recorded `gh` on PATH answering `pr checks` with a tab-separated listing) and how refusals are asserted. The required contexts of the main ruleset today (measured 2026-11-07T03:34Z by `gh api repos/mryfmo/dotfiles/rulesets/24397953`): `public-bootstrap (macos-15, client)`, `public-bootstrap (ubuntu-24.04, client)`, `public-bootstrap (ubuntu-24.04, server)`, `regime`, `test (macos-15, client)`, `test (ubuntu-24.04, client)`, `test (ubuntu-24.04, server)`, `validate`. The lever may not call the rulesets API at merge time without a reason (one more `gh` read per merge, and a ruleset the operator edits is not the program's record); the list lives in the lever as a constant the operator's ruleset is compared against by a test, or is read from the ruleset once per run: choose, and say why in the header.

DATA SHAPE
`REQUIRED_CHECKS`, one bash array of the check names a merge needs (the eight contexts above, as GitHub names them, exact strings). The gate's judgement is a set comparison: every required name must appear in the `gh pr checks` listing with bucket `pass` (a `skipping` bucket satisfies only a check that is not required), and every listed check must be `pass` or `skipping` as today. The refusal names the missing checks (`CI has no result for: test (ubuntu-24.04, client), ...`) separately from the red ones. A `tests/unit` test holds the array equal to the ruleset's required contexts recorded in the test (a fixture copied from the 03:34Z measurement), so a drift between the lever and the ruleset fails CI, not a merge.

CHANGE
1. Add `REQUIRED_CHECKS` to the lever with a header sentence naming its source and the reason it is a constant; extend the gate: after the red check, compute the required names absent from the listing (or present with bucket other than `pass`) and refuse naming them. 2. Tests: a listing of `regime`, GitGuardian and CodeRabbit alone refuses naming the eight missing checks (the PR 708 case); a listing with every required check `pass` plus extras merges as today; a required check `skipping` refuses naming it; a required check `pending` refuses as today; the array equals the recorded ruleset contexts. 3. The README paragraph gains one sentence on the named-check rule. 4. `cmp`; the generator; `make render-check`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/orchestrator/pr-merge.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 5. Commit `fix(levers): pr-merge.sh requires the Unit test and bootstrap checks by name (regime-cutover U330)` with the trailer. 6. The body: `## Summary`, `## Contract` (TRUST line), `## Threat table` (`row | risk | status | evidence`, one row per changed path, the two pin files in rows of their own, every closed row naming a selector, a row for the drift between the constant and the ruleset), `## Verification` with every ACCEPTANCE line pasted; `Program-Unit: regime-cutover/U330` once and the `Generated with [Claude Code]` footer.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest <the lever's test module> -v` OK (count pasted; the new tests named). 2. The PR-708-case test fails against the 668ba887 lever (a scratch copy of `git show 668ba887:scripts/orchestrator/pr-merge.sh`) and passes on the head (outputs pasted). 3. `cmp` 0; `make render-check` 0; validate-agent-assets 0. 4. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 5. `gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context'` run by the coordinator after the head is reported equals the array (the worker pastes the array; the coordinator pastes the API read).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts `gh pr checks` as the record of CI results and the ruleset's required contexts as the operator's list of what a merge needs; it adds a comparison, removes nothing, and merges nothing itself.

TIMEBOX
45 minutes.

FORBIDDEN
No `gh` call that writes; no change to the workflows or the ruleset; no network beyond the lever's own `gh` reads in tests (which are faked); no push; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u330/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U330`.
- Progress line at `../U330-progress.txt`; final report to `../U330-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat origin/main HEAD`, the ACCEPTANCE lines with their outputs, the array as written, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 32, 34, 44, 46); `decisions.tsv` row 2026-11-07T01:45:00Z (ci-gap) and 2026-11-07T03:35:00Z (the ruleset's rules); the pr-merge.sh header.
