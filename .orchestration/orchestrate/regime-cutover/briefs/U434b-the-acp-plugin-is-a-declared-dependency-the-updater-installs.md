# U434b round 2 of U434 (PR 757, M-22 Part B, table row s21): the Router profile's ACP plugin is a declared dependency the updater installs, the Contract states the reach of the repoint, and the threat table carries a row per control

GOAL
Fix the two blocking findings and the two P2 findings of verdicts/U434-8c3cfec2.md (the round-1 audit of PR 757 at 8c3cfec25f49a3f5e63501e8c20631cf37806205) on the same branch `feat/router-profile-acp-subagent` in the tree `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U345` (the U434 worker's tree, head 8c3cfec25f49a3f5e63501e8c20631cf37806205, clean), as new commits on top of the head (no amend, no rebase). After this round a fresh deploy of the kit resolves `@deepseek-ai/dsh-subagent-acp` from the deployed Router profile without a hand-made link, the pull request body says what the repoint reaches and what it does not, and every control of the change has its own threat-table row.

CONTEXT (measured by the coordinator and the round-1 worker; read the verdict first)
- Finding P1 [f8 s6] cordis.patch.yml:49: the `subagent-acp` insert names `@deepseek-ai/dsh-subagent-acp`, but the rendered `home/dot_dsh/profiles/router/package.json` declares only `dsh-superagent` (link:../../plugins/dsh-superagent) and `dsh-omp-gateway` (link:../../plugins/omp-gateway), so the deployed profile cannot resolve the package: dsh boots, serves and prints `dsh: warning: 1 entry did not activate`. The package exists built in the pinned dsh tree at `~/.dsh/dsh/current/packages/subagent/subagent-acp` (package.json present; the round-1 real run linked it by hand, the U313 deviation). The generator renders the package.json in `render_dsh_router_profile` (scripts/generate-agent-configs.py; the constants `DSH_SUPERAGENT_LINK`, `DSH_GATEWAY_LINK` at :184 and :205 and the `"dependencies"` dict). The installer is `update_dsh_superagent` in `scripts/update-agent-assets.sh`: it runs `pnpm install` in `${DSH_HOME}/profiles/router` under srt, and in its already-installed branch (lines [2817]) reruns the profile install only when `node_modules/dsh-superagent` is absent, so a new dependency row would never be installed on a host where dsh-superagent is already present.
- Finding P1 [f5 s8] cordis.patch.yml:31: the web-app bundle leaves the top-level `tool-subagent` row disabled and the superagent presets carry nested `tool-subagent` rows with `provider: spawn`, so the kit's repoint reaches the Router's base agent (the round-1 real run's ACP session) and not the Executor Sessions the presets spawn. U406 (PR 744) removed restated preset rows from the kit (a restated preset row broke activation), so a preset-level row is not this round's change. This round states the reach in the body and files the gap as a residual row owned by U437 (planned: the superagent presets' subagent provider, a design unit with a prototype).
- Finding P2 [f10 s4] test_generate_agent_configs.py:2570: the threat table's ACP-activation row cites a rendered-text test that cannot see the missing package. The row needs a test of the dependency (below) and the coordinator's deployed-surface measurement named as evidence.
- Finding P2 [f10 s3] generate-agent-configs.py:2562: the threat table lacks a row for the `permission: allow` control and a row for the Router worker-routing effect (what the repoint changes for a Router turn), with the deployment gaps owned by name.
- Standing order 49: fix the defect, prove it by a test, no review round beyond this.

DATA SHAPE
The Router profile's dependency table: name -> link spelling, one row per plugin the patch inserts. Add one row: `@deepseek-ai/dsh-subagent-acp` -> `link:../../dsh/current/packages/subagent/subagent-acp` (the path from `${DSH_HOME}/profiles/router` to the pinned tree's package through the `dsh/current` link, the same `link:` form as the two rows that exist). The installer's rerun condition becomes a function of that table: the profile install reruns when any dependency name of the rendered package.json has no entry under `node_modules/`, read from the deployed `package.json` (never a hard-coded name), so the kit's next dependency needs no installer edit (Model the Domain).

CHANGE
1. Red tests first, each named for the behavior: (a) in `tests/unit/test_generate_agent_configs.py` beside the U434 test: the rendered router package.json declares `@deepseek-ai/dsh-subagent-acp` with the link spelling above, the thak profile declares no such row, and the insert's package name equals the dependency's name (one source of the name: a constant such as `DSH_SUBAGENT_ACP_PLUGIN`/`DSH_SUBAGENT_ACP_LINK` beside the gateway constants); (b) in tests/unit/test_update_agent_assets.py: with dsh-superagent already installed and `node_modules/dsh-superagent` present but `node_modules/@deepseek-ai/dsh-subagent-acp` absent, the already-installed branch runs the profile install; with every dependency present it does not; the names come from the deployed package.json (inject a package.json with a third made-up dependency and assert the install runs for it). Run them red at 8c3cfec2 and paste the red lines.
2. The generator: the constants and the dependency row; the thak profile unchanged. Regenerate (`uv run --with pyyaml python scripts/generate-agent-configs.py`), then `make render-check`, `make validate-agent-assets`, both `cmp` of the lever copies.
3. `scripts/update-agent-assets.sh` `update_dsh_superagent`: the already-installed branch's rerun condition reads the dependency names of `${DSH_HOME}/profiles/router/package.json` (a `python3 -I -S -c` or `node -e` one-liner reading `dependencies` keys, its exit status read, a failed read a refusal naming the file, never an assumption) and reruns the profile install when any name has no `node_modules/<name>` entry; the fresh-install branch is unchanged (it runs the install anyway). Keep the hosts check and the canary before the install as they stand. shdoc comment updated. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` and `scripts/lint-comparisons.py scripts/update-agent-assets.sh` exit 0.
4. Green: the new tests plus `tests.unit.test_generate_agent_configs tests.unit.test_dsh_profile tests.unit.test_scratch_git` and the updater module, pasted.
5. Body draft to `/tmp/dotfiles-wt/U434b-pr-body.md`, rewriting `/tmp/dotfiles-wt/U434-pr-body.md` whole (keep its Summary facts; the file is the round-1 body): a `## Round 2` section naming each finding and what changed; the Contract states the reach (the repoint reaches the Router's base agent; the superagent presets' nested `tool-subagent` rows keep `provider: spawn` until U437, named as a residual); the threat table in the `| row | risk | status | evidence |` form with one row per changed path plus the non-path controls: the `permission: allow` control (risk, closed-by, evidence), the worker-routing effect (what a Router subagent turn does now: `omp acp` worker in a sibling sandbox, evidence the round-1 real run lines and the test (b) of round 1), the dependency row (evidence test (a) and the coordinator's deployed measurement `node -e "require.resolve('@deepseek-ai/dsh-subagent-acp')"` from `~/.dsh/profiles/router` after `make update`, to be pasted by the coordinator, marked `pending deploy` by you), and the residual row for the preset gap (`residual: U437`). The last line stays `Program-Unit: regime-cutover/U434`.
6. Commit unsigned on top of 8c3cfec2 with the message `fix(router): the ACP plugin is a declared dependency the updater installs; the threat table and contract name every control (regime-cutover U434b, round 2 of U434)` and the footer line `Program-Unit: regime-cutover/U434`.

ACCEPTANCE
1. Tests (a) and (b) red at 8c3cfec2 and green at the new head, pasted lines.
2. `uv run --with pyyaml python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_dsh_profile tests.unit.test_scratch_git <updater module>` OK at the new head, the `Ran N tests` and `OK` lines pasted.
3. `make render-check`, `make validate-agent-assets`, shfmt, ruff format --check, prettier --check, `lint-comparisons.py` on the two shell levers, both `cmp`: each exit 0, pasted.
4. The rendered `home/dot_dsh/profiles/router/package.json` holds the three dependencies, and `git grep -n '@deepseek-ai/dsh-subagent-acp' -- home scripts` lists the patch, the package.json, the generator and the tests.
5. The tree is clean at the new head; `git log --oneline 8c3cfec2..HEAD` shows the one commit.

VERIFY
ACCEPTANCE pasted into the report; the coordinator fetches the head by path, pushes, runs the round-2 audit, the sweep and CI, merges, deploys by `make update` in the chezmoi clone (the updater's real path, so the dependency installs), measures the resolve and the dsh boot line, relaunches the Router and judges row s21.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the pinned dsh tree's built `packages/subagent/subagent-acp` as the package, the updater's srt-bound `pnpm install` as the install path, and the round-1 real run as the proof of the route; it adds one dependency row and one data-driven rerun condition, changes no grant and reads no store.

TIMEBOX
90 minutes.

FORBIDDEN
No change to acp-broker, acp-seat, hcom-seat, the relay or the record helper; no preset row in the router patch; no new grant in any settings row; no pin typed by hand; no edit of `~/.dsh`; no rebase, no amend, no `git stash`; no push; no `gh` call; no network; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u434b/`, then read it); a progress line at `/tmp/dotfiles-wt/U434b-progress.txt` within five minutes of starting and at least every 10 minutes after, before and after every long run (a silent worker is stopped and replaced).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at the committed head in the tree. Your final line is the Task return.
- Final report to `/tmp/dotfiles-wt/U434b-report.txt`; the body draft to `/tmp/dotfiles-wt/U434b-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the head (40 hex), the ACCEPTANCE lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 44, 46, 49); verdicts/U434-8c3cfec2.md; briefs/U434-the-router-profile-drives-omp-acp-through-the-broker.md; /tmp/dotfiles-wt/U345-report.txt (the round-1 report); decisions 2026-11-09T06:58:42Z (U406, no preset row).
