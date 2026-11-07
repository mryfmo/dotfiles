# U317c round 3 of U317: main merged into PR 711 and the superagent store's temporary directory named plainly

GOAL
PR 711 (U317, M-26 stage A: the dsh-superagent asset, the GitHub Source in observe mode, the Router profile) has stood at 9cb6a2fb since 2026-11-07T00:37Z, held for U321 (the router role of hcom-seat), which merged as 0249e534 (PR 715). GitHub now reports the branch CONFLICTING with main, and its Unit test run 42319806884 fails all four test legs on one test: `test_sandbox_portability.SandboxPortabilityTest.test_tracked_scripts_pass_both_guards` reports `scripts/update-agent-assets.sh:2376: tmp: "TMPDIR=${DSH_SUPERAGENT_STORE}/tmp" ...` (and the same at `:2505`, the mkdir). The guard's contract (the module docstring, lines 7 to 17) refuses a shell word holding a literal `/tmp` path unless the word expands TMPDIR, and a refused odd form is fixed by writing it the plain way, never by teaching the guard a spelling. The U322 branch (PR 718, `build_under_srt`) spells the same directory `${store_real}/tmpdir` (its line 1994). This round merges main into the branch and renames the store's temporary directory so the guard passes, nothing else.

SCOPE
The same branch `feat/dsh-superagent-asset-observe` and PR 711; the tree is `/tmp/dotfiles-wt/U317` at 9cb6a2fb (clean). May write: the merge of main (`git merge --no-ff 0249e534b482a7b07c24daac6ab83bf7cc0fa361`, already fetched into the tree as FETCH_HEAD; resolve every conflict keeping both sides' intent, main's text where the two edit the same lines for the same reason), the two `${DSH_SUPERAGENT_STORE}/tmp` words of `scripts/update-agent-assets.sh` (renamed to `${DSH_SUPERAGENT_STORE}/tmpdir`), any test of `tests/unit/test_update_agent_assets.py` that asserts the old spelling, and the body `../U317c-pr-body.md` (the round-2 body `/tmp/dotfiles-wt/U317b-pr-body.final.md` plus a `## Round 3` paragraph). Not: any behaviour beyond the rename; no change to the portability guard or its `ALLOWED_TMP` table.

CONTEXT
Seven files changed on both sides since the base 2b2415f6: `docs/deepseek-harness.md` (main added the router paragraph, U321; then the install paragraph, U322, at PR 718's merge head if it lands first; keep every paragraph), `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (regenerate with `scripts/generate-agent-configs.py` after the merge rather than hand-merging the generated file), `scripts/update-agent-assets.sh` (main's `build_under_srt` from U322 may or may not be on main yet; the branch's `update_dsh_superagent` and `dsh_superagent_srt_settings` stay), `tests/unit/test_asset_manifest.py`, `tests/unit/test_network_bounds.py`, `tests/unit/test_update_agent_assets.py` (both sides add test groups; keep both). After the merge, `git diff --name-only 0249e534 HEAD` must list only the branch's own files.

DATA SHAPE
One merge commit and one fix commit on the branch. The fix is two shell words, `${DSH_SUPERAGENT_STORE}/tmpdir`, where `${DSH_SUPERAGENT_STORE}/tmp` stood (the env line of the srt run and the mkdir), with the matching test expectation.

CHANGE
1. `git merge --no-ff --no-commit 0249e534b482a7b07c24daac6ab83bf7cc0fa361`; resolve; regenerate the generated outputs if either side touched the manifest; commit the merge unsigned (`Merge main 0249e534 into feat/dsh-superagent-asset-observe (regime-cutover U317c)`). 2. Rename the two words; adjust the test that pins the old spelling if one exists. 3. `uv run --with pyyaml python -m unittest tests.unit.test_sandbox_portability tests.unit.test_update_agent_assets tests.unit.test_asset_manifest tests.unit.test_network_bounds tests.unit.test_runtime_health tests.unit.test_generate_agent_configs tests.unit.test_dsh_profile tests.unit.test_intake_observe -v` OK. 4. `uv run ruff format --check`; `scripts/lint-comparisons.py --changed`; `shellcheck -x scripts/update-agent-assets.sh`; `shfmt -d scripts/update-agent-assets.sh`. 5. Commit `fix(dsh): the superagent store's temporary directory is tmpdir, the plain spelling the portability guard reads (regime-cutover U317c)` with the trailer. 6. The body: the round-2 body plus `## Round 3` (the hold for U321, the merge, the guard hit and the rename); `Program-Unit: regime-cutover/U317` once and the footer.

ACCEPTANCE
1. The eight test modules OK (counts pasted; `test_tracked_scripts_pass_both_guards` named as passing). 2. `git diff --name-only 0249e534b482a7b07c24daac6ab83bf7cc0fa361 HEAD` lists only the branch's files (pasted). 3. `git diff --stat <merge commit> HEAD` shows the rename alone (pasted). 4. ruff 0; lint-comparisons 0; shellcheck 0; shfmt 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; CI on the pushed head and the round-3 audit are the coordinator's.

CLOSURE
remove

TRUST
TRUST: the unit trusts the portability guard as the repository's rule for temporary paths and fixes the spelling, not the guard; the merge changes no behaviour of either side.

TIMEBOX
40 minutes.

FORBIDDEN
No change to the guard; no `ALLOWED_TMP` row; no rebase; no network beyond nothing (main is already fetched); no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u317c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U317`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U317c-progress.txt`; final report to `../U317c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Each commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, the merge commit and head shas (40 hex), the conflicts and how each was resolved (one line each), the ACCEPTANCE lines. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 18, 21, 24, 27, 29, 34, 44, 46); the U317 and U317b briefs; `tests/unit/test_sandbox_portability.py` lines 1 to 60 (the rule).
