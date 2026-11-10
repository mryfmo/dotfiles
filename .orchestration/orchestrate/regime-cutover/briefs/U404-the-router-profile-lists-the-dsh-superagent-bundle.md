# U404 the router profile's package.json lists the dsh-superagent bundle, so the composed tree holds the superagent entries the profile patch configures

GOAL
Table row i3 (`tests/intake-superagent.tsv`, M-26 stage B, the Router under srt) was run on the laptop for the first time on 2026-11-09 (decisions row 2026-11-09T02:24:58Z) and is NG: the launch `hcom-seat router -- --no-open` starts dsh, the three srt probes hold (write-denied, state-write-open, connect-denied), the credential root is mode 700, but no `dsh-superagent is waiting for setup` and no `dsh-superagent ready` line appears in 90 seconds and `$DSH_HOME/router-state` is never made. Measured cause: `dsh --profile router --dump-config` prints `patch: entry "dsh-superagent" not found`, `patch: entry "dsh-superagent-worker-preset" not found` and `patch: entry "dsh-superagent-router-preset" not found`. The rendered `home/dot_dsh/profiles/router/package.json` lists the plugin as a `link:` dependency and its `dsh.profile.bundles` holds `@deepseek-ai/dsh-base` and `@deepseek-ai/dsh-web-app` alone, so the bundle's own layer (`cordis.patch.yml` of the plugin, which inserts the five superagent entries) is never composed, and the profile patch's rows address entries that do not exist. The renderer's docstring (`render_dsh_router_profile`) already says the package carries "the superagent bundle"; the constant did not. Measured on the laptop with the bundle name added to the list: the dump holds the five entries, the profile's stateDir and both presets as `patched by .../cordis.patch.yml`, and no `not found` line.

SCOPE
A new branch `fix/router-profile-bundles-dsh-superagent` from origin/main 57e5345a1; the tree is the worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U404` (clean, made by worker-worktree.sh). May write: `scripts/generate-agent-configs.py` (the one constant `DSH_ROUTER_BUNDLES` and the comment above it), `tests/unit/test_dsh_profile.py` (the router package test), the generated `home/dot_dsh/profiles/router/package.json` through `scripts/generate-agent-configs.py` (never by hand), and the PR body `/tmp/dotfiles-wt/U404-pr-body.md`. Non-goals: the profile patch's preset rows (they restate the bundle's presets with the sandbox row off, by design, generate-agent-configs.py:180-186), `home/dot_dsh/profiles/router/cordis.patch.yml`, `hcom-seat`, `router-settings-apply`, the updater, the manifest, the thak profile, and every other test module.

CONTEXT
`scripts/generate-agent-configs.py` at 57e5345a1: line 191 `DSH_ROUTER_BUNDLES = ("@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app")`; line 189 `DSH_SUPERAGENT_PLUGIN = "dsh-superagent"`; lines 2619-2686 `render_dsh_router_profile` (line 2641 writes the bundles list, line 2642 the link dependencies). `tests/unit/test_dsh_profile.py`: class `DshRouterProfileTest` from line 221; `test_the_package_links_the_bundle_and_the_gateway_over_the_web_profiles_bundles` at lines 319-331 pins the two-name bundle list at line 323. dsh composes a profile as "bundle layers in `dsh.profile.bundles` order, the profile's own `cordis.patch.yml`, then overlays" (`apps/cli/lib/profile-boot-*.js`, the PROFILE_ROOT_CONFIG text); upstream installs the plugin with `dsh plugin --profile superagent add "link:$PWD"` (`docs/006-deployment.md` line 80), whose result is the bundle both in `dependencies` and in `bundles`. The plugin's `package.json` declares `dsh.bundle.patch ./cordis.patch.yml`, whose first entry is `- insert:` of `dsh-superagent`, `dsh-superagent-github`, `dsh-superagent-feishu` (disabled), `dsh-superagent-worker-preset` and `dsh-superagent-router-preset`. The U317 brief's step 6 named a stage A dump-config measurement of the router profile; no row of decisions.tsv or ledger.tsv records it, so the composed router tree was never read before 2026-11-09.

DATA SHAPE
One tuple constant of bundle package names, in composition order: `("@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app", "dsh-superagent")`; the third name equals `DSH_SUPERAGENT_PLUGIN`, so the bundle and the `link:` dependency share one spelling. The rendered `package.json` `dsh.profile.bundles` is that list.

CHANGE
1. Test first, red at 57e5345a1: in `tests/unit/test_dsh_profile.py`, `test_the_package_links_the_bundle_and_the_gateway_over_the_web_profiles_bundles` expects `{"manifestVersion": 1, "profile": {"bundles": ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app", "dsh-superagent"]}}`, and asserts that the third bundle name is a key of the package's `dependencies` (the bundle the profile composes is the one the updater installs). Paste the red line.
2. `scripts/generate-agent-configs.py`: `DSH_ROUTER_BUNDLES = ("@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app", DSH_SUPERAGENT_PLUGIN)` (move the constant below line 189 if the name must be defined first), and one sentence in the comment block above it saying the bundle is listed so dsh composes its insert layer before the profile patch (`dsh plugin add` writes both the dependency and the bundle; this renderer writes both too).
3. Regenerate: `python3 scripts/generate-agent-configs.py` (the kit's form, see the Makefile's render target); `home/dot_dsh/profiles/router/package.json` changes by the one list entry and nothing else changes in the tree (`git status --porcelain` names the three files alone).
4. Body at `/tmp/dotfiles-wt/U404-pr-body.md`: Summary (the i3 measurement and the cause, four sentences), Contract (the bundle list), Threat table (one row per changed path: the generator, the test module, the rendered package.json; one effect row: the Router now loads the superagent bundle inside srt, with the controls that bound it named: the dsh and router rows' deny lists in hcom-seat, the state root under DSH_HOME, the credential root read grant), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U404` once at the end.

ACCEPTANCE
1. The test's red line at 57e5345a1 (`/tmp/u404/red.txt`) and its green line at the head, pasted. 2. `python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (the three lint checks: shfmt, ruff format, prettier) exits 0 and `make render-check` exits 0, pasted. 4. `git diff --stat 57e5345a1 HEAD` pasted; only `scripts/generate-agent-configs.py`, `tests/unit/test_dsh_profile.py` and `home/dot_dsh/profiles/router/package.json` in it. 5. `python3 -I -c` reading the rendered package.json prints `["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-web-app", "dsh-superagent"]` for `dsh.profile.bundles`, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request with the body, and the one audit, the sweep and CI follow (standing order 49). After the merge and `make deploy-kit`, the coordinator runs `dsh --profile router --dump-config` on the laptop (no `not found` line, the five entries present) and table row i3 by its command cell through run-host-rows.py; i3's OK is the unit's goal check (standing order 42).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts dsh's composition order as its documentation states it (bundle layers in `dsh.profile.bundles` order, then the profile patch), the plugin's own `cordis.patch.yml` as the bundle layer, and the generator's render as the one writer of the profile's package.json; it reads no dsh output in its tests (the composed tree is read by the coordinator on the laptop after deploy, VERIFY) and changes no row of the profile patch.

TIMEBOX
25 minutes.

FORBIDDEN
No edit of `home/dot_dsh/profiles/router/package.json` by hand (the generator writes it); no change to `cordis.patch.yml` of any profile; no change to any lever under `scripts/orchestrator/`; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u404/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U404`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U404-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U404-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the test with its red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 42, 44, 46, 49); the U317 brief (`briefs/U317-dsh-superagent-asset-github-source-observe-router-under-the-dsh-role.md`) step 6; `handoff/09-plan-fastest-build-then-tests-2026-11-07.md` section 4 (one NG row is one fix unit, the row's command and expected are its acceptance); the decisions rows 2026-11-09T02:24:58Z (the i3 measurement) and this unit's reservation.
