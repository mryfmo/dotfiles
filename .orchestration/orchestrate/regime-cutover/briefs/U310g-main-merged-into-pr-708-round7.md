# U310g round 7 of U310: main 49f3c33c merged into PR 708, both sides' behaviour kept

GOAL
PR 708 (U310, the dsh role provisions its omp profile with the bridge route) stands at b2ba1204 (round 6, U310f, pushed 2026-11-07T06:38Z) and GitHub reports it CONFLICTING with main. Main gained U321 (0249e534, the `router` role of hcom-seat: a third role row, `allowLocalBinding: true` for that role alone, the state root `$DSH_HOME/router-state` held physical and resolved once, the passthrough refusing `--profile`) and U322 (49f3c33c, `build_under_srt` in the updater, the docs install paragraph). Both sides edit hcom-seat (both copies), `tests/unit/test_hcom_seat_dsh.py`, the manifest's pin lines, the generated outputs and `docs/deepseek-harness.md`. This round is the merge alone: no new behaviour, no finding fixed, every test of both sides kept and green.

SCOPE
The same branch `feat/dsh-role-profile-route` and PR 708; the tree is `/tmp/dotfiles-wt/U310` at b2ba1204 (clean); main's head 49f3c33c3fe0322474a671a598765aa2f1397259 is already fetched there (FETCH_HEAD). May write: the merge of main and its conflict resolutions in the six overlapping files (`home/dot_local/bin/common/executable_hcom-seat`, `scripts/orchestrator/hcom-seat`, `tests/unit/test_hcom_seat_dsh.py`, `home/dot_agents/agent-config.yaml`, `scripts/generated-agent-outputs.json`, `docs/deepseek-harness.md`), and the body `../U310g-pr-body.md` (the round-6 body `/tmp/dotfiles-wt/U310f-pr-body.final.md` plus a `## Round 7` paragraph naming the merge and each resolution in one line). Not: any file outside the merge; no behaviour change on either side.

CONTEXT
hcom-seat: U321's router role adds rows and a `state_root_hold` among the pre-launch checks; U310's profile provision adds `profile_config_hold`, `helper_copy_make`, `helper_path_check` and the one `"${profile_config_cmd[@]}"` run (hcom-seat:1113 at b2ba1204). Both touch the dsh row's settings and launch sequence. Keep U321's text where the two edit the same lines for the router role, and U310's where they edit the profile provision; where both add a check among the pre-launch checks, keep both in the order the comments state (the hold of the state root and the hold of the helper are independent). The pins: `home/dot_agents/agent-config.yaml` `claude.levers.sha256.hcom-seat` and `.profile-config-place.py` must equal `shasum -a 256` of the merged sources, refreshed by `uv run --with pyyaml scripts/generate-agent-configs.py` (never by hand), which also rewrites `scripts/generated-agent-outputs.json`. The two copies of hcom-seat are byte-identical (cmp). `docs/deepseek-harness.md`: keep every paragraph (main's router and install paragraphs, the branch's profile paragraph). The test module: both sides add test classes; keep both; a test that asserts a settings byte sequence may need the union of both roles' rows.

DATA SHAPE
One merge commit on the branch whose three-dot diff against main equals b2ba1204's intent and nothing else: `git diff --name-only 49f3c33c HEAD` lists only the branch's own files.

CHANGE
1. `git merge --no-ff --no-commit 49f3c33c3fe0322474a671a598765aa2f1397259`; resolve as CONTEXT says; `uv run --with pyyaml scripts/generate-agent-configs.py`; `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat`; commit the merge unsigned (`Merge main 49f3c33c into feat/dsh-role-profile-route (regime-cutover U310g)`). 2. `uv run --with pyyaml python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat tests.unit.test_profile_config_place tests.unit.test_generate_agent_configs tests.unit.test_pr_levers -v` OK (the router tests of U321 and the profile tests of U310 both present and passing). 3. `make render-check`; `uv run --no-project scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/orchestrator/hcom-seat`; `uv run ruff format --check`; `scripts/lint-comparisons.py --changed`. 4. The body: the round-6 body plus `## Round 7`; `Program-Unit: regime-cutover/U310` once and the footer; under 65536 bytes.

ACCEPTANCE
1. `git diff --name-only 49f3c33c3fe0322474a671a598765aa2f1397259 HEAD` (pasted) lists only the branch's files. 2. The five test modules OK with counts pasted, and the names of one router test and one profile test that passed. 3. cmp 0; render-check 0; validate 0; shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 4. The pins equal `shasum -a 256` of the two sources (pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the audit at the merge head, the sweep and CI are the coordinator's.

CLOSURE
remove

TRUST
TRUST: the unit changes no behaviour; it trusts both sides' tests as the proof that each side's behaviour survived the merge.

TIMEBOX
45 minutes.

FORBIDDEN
No behaviour change; no pin edited by hand; no rebase; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u310g/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U310`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U310g-progress.txt`; final report to `../U310g-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, the merge head sha (40 hex), each conflict and its resolution in one line, the ACCEPTANCE lines. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 18, 21, 24, 27, 29, 34, 44, 46); the U310f and U321d briefs; `docs/orchestrator/README.md` "The dsh role" and "The router role".
