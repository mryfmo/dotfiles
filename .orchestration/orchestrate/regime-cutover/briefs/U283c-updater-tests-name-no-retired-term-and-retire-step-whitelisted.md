# U283c round 3 of U283: the updater tests name no retired term, and the understand-anything retirement is a single step

GOAL
PR 701's round-2 head (fa969db6) fails CI's Ubuntu test legs in `test_lint_retired_terms.RepositoryTest.test_the_repository_names_no_retired_term_outside_the_allow_list`: the new tests in `tests/unit/test_update_agent_assets.py` name the retired term `agmsg` at line 4797 (`"retire_agmsg_shim"` in the whitelist assertion) and line 4976 (a fixture manifest step `update_agmsg`). The retired-terms lint (`scripts/lint-retired-terms.py` and its list) forbids the word outside its allow list, so the tests must assert the whitelist by another member and use a neutral fixture step name. Second, the first host judgment (U288, row `g13`) found the understand-anything Claude Code plugin still installed and enabled on the laptop because its retirement step (`retire_understand_anything`, `scripts/update-agent-assets.sh:2498`) runs only under the updater's full `main`; the single-step whitelist U283 built does not name it, so the coordinator cannot close that deploy gap. This round adds the step to the whitelist under the same fail-closed contract.

SCOPE
The existing branch `fix/updater-single-function-fails-closed` at fa969db6b9ba7d5d0b8fe26171760e51634765a2 in `/tmp/dotfiles-wt/U283` (the PR is 701). May write: `tests/unit/test_update_agent_assets.py` (the two lines and whatever the whitelist test needs), `scripts/update-agent-assets.sh` (the whitelist row and the usage line only), and the body `../U283-pr-body.md` (a Round 3 section). Not: any updater function body, the manifest, the retired-terms list or its allow list.

DATA SHAPE
The whitelist assertion names members that are not retired terms (`update_deepseek_harness`, `update_omp`, `prune_retired_manifest_steps`, `retire_understand_anything`); the fixture manifest step is `update_fixture_step`. The whitelist gains `retire_understand_anything`; the single-step exit rule already covers every whitelisted name.

CHANGE
1. The two test lines; the whitelist row and usage line; a test that `retire_understand_anything` dispatches as a single step and exits non-zero when the function records a failure (recorder fake), as the other whitelisted steps are tested.
2. `uv run python -m unittest tests.unit.test_lint_retired_terms` OK (the repository test passes in your tree).
3. The body's Round 3 section: the CI failure quoted, the two changes, ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets tests.unit.test_lint_retired_terms` OK (paste the count; the new test named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `grep -c agmsg tests/unit/test_update_agent_assets.py` prints 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's test legs on the PR are the coordinator's evidence; after the merge the coordinator runs `scripts/update-agent-assets.sh retire_understand_anything` for the g13 row.

CLOSURE
remove

TRUST
TRUST: the unit trusts the retired-terms lint as the rule and the single-step exit rule as the contract; it renames two test literals and adds one whitelist row, runs no function on this host, reads no credential and opens no network.

TIMEBOX
20 minutes.

FORBIDDEN
No run of any `update_*` or `retire_*` function on this host; no change to the retired-terms list or allow list; no change to any function body; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u283c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U283` and the coordinator fetches it by path.
- Progress line at `../U283c-progress.txt`; final report to `../U283c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol).

REPORT
Status, head sha (40 hex), files changed, the ACCEPTANCE result lines, deviations. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); CI run 42229858138 job 127932676138; `tests/ng-u288.md` g13; `briefs/U283-*.md`.
