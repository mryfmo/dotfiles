# U406 the router profile keeps dsh's bash-sandbox on, so the permission presets and the superagent activate under srt

GOAL
Table row i3 (`tests/intake-superagent.tsv`, M-26 stage B) stays NG after U404 (PR 743): with the superagent bundle composed, dsh reports `3 entries did not activate`: `dsh-superagent` pending on the service `permissionPresets`, `permission` (@deepseek-ai/dsh-permission-presets) pending on the service `shell`, `dsh-superagent-github` pending on `orchestrator`. The kit's router patch disables the only confining shell provider upstream ships, `bash-sandbox`, at the base row and inside the two restated presets (generate-agent-configs.py:180-186: the presets are restated whole only to turn that row off), under the 2026-11-06 decision that srt, not bash-sandbox, is the seat's boundary. Measured on the laptop 2026-11-09 (decisions row 03:52:16Z): with `bash-local` as the provider, permission-presets refuses (`the mounted bash executor does not confine (no sandboxMode)`); with the three `disabled: true` rows removed every plugin activates and the Router makes `$DSH_HOME/router-state/orchestrator.sqlite`. So for the router profile alone the decision reverses: bash-sandbox stays on and runs inside srt (two boundaries), and the presets are no longer restated.

SCOPE
A new branch `fix/router-profile-bash-sandbox-on` from origin/main 57e5345a1; the tree is the worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U406` (clean, made by worker-worktree.sh). May write: `scripts/generate-agent-configs.py` (the function `render_dsh_router_profile`, the function `dsh_superagent_presets` and its helpers if they become unused, and the comment block at lines 180-186), `tests/unit/test_dsh_profile.py` (the `DshRouterProfileTest` class), the generated `home/dot_dsh/profiles/router/cordis.patch.yml` through the generator (never by hand), `scripts/orchestrator/README.md` only if it names the restated presets, and the PR body `/tmp/dotfiles-wt/U406-pr-body.md`. Non-goals: the thak profile and its `bash-sandbox disabled: true` row (its turn needs no shell; d15 stands), `home/dot_dsh/profiles/router/package.json` and the bundles constant (U404, PR 743), `hcom-seat`, `router-settings-apply`, the updater, the manifest.

CONTEXT
`scripts/generate-agent-configs.py` at 57e5345a1: lines 180-186 (the comment that explains the restated presets), line 2508 `def dsh_superagent_presets()`, line 2439 `def patch_block`, lines 2619-2686 `render_dsh_router_profile` (lines 2665-2666 render `- id: bash-sandbox` / `  disabled: true`; lines 2679-2680 render the two presets through `dsh_superagent_presets()`). `tests/unit/test_dsh_profile.py`: `DshRouterProfileTest` from line 221; `test_the_presets_restate_the_archives_rows_with_the_sandbox_off` at lines 333-371 pins the restated presets and their `disabled: true` sandbox rows; the `sandbox_rows` helper at line 202. The plugin's own bundle layer (`~/.dsh/plugins/dsh-superagent/cordis.patch.yml`, not in this repository) inserts `dsh-superagent-worker-preset` and `dsh-superagent-router-preset` with `bash-sandbox` disabled on win32 alone, so once the kit stops restating them the composed tree carries upstream's presets as shipped. The base bundle's `bash-sandbox` row (`packages/bundle/base/cordis.patch.yml:249-253`) is `disabled: !!js process.platform === 'win32'` with `timeoutMs: 60000`; dropping the kit's row leaves that. `permission-presets` (`packages/interaction/permission-presets/lib/index.js:177`) refuses an executor without `sandboxMode`.

DATA SHAPE
The router patch is a list of entry rows keyed by id; after this unit it holds the thak-form rows (session log off, the DeepSeek API, account, web-search and web-API rows disabled, the default model on the gateway provider), the webserver row, the superagent `stateDir` row, and the gateway insert. No `bash-sandbox` row and no preset row of any kind.

CHANGE
1. Tests first, red at 57e5345a1, in `DshRouterProfileTest`: (a) the patch holds no row with id `bash-sandbox` and the text `dsh-bash-sandbox` appears nowhere in it (the inverse of d15's thak assertion, with the reason in the test's docstring: upstream's permission presets need a confining executor, srt is the outer boundary); (b) the patch holds no `dsh-superagent-worker-preset` or `dsh-superagent-router-preset` row (upstream's bundle layer supplies them); (c) the rows that remain are exactly the DATA SHAPE list, in order. Remove `test_the_presets_restate_the_archives_rows_with_the_sandbox_off` and the `sandbox_rows` helper if nothing else uses it. Paste the red lines.
2. `render_dsh_router_profile`: drop the two `bash-sandbox` lines and the presets loop; rewrite the comment block at lines 180-186 to say why the router keeps the sandbox on (two sentences: the presets require a confining executor, srt stays the outer boundary) and drop the sentences about restating presets. Remove `dsh_superagent_presets` and any helper only it used, when no other caller remains (`grep -n dsh_superagent_presets scripts tests` names them).
3. Regenerate (`make render-check` form); `home/dot_dsh/profiles/router/cordis.patch.yml` loses the bash-sandbox row and the two preset blocks and nothing else changes in the tree.
4. Body at `/tmp/dotfiles-wt/U406-pr-body.md`: Summary (the measurement and the reversal for the router alone, five sentences), Contract (the DATA SHAPE), Threat table (one row per changed path; one effect row: the Router's shell commands now run under dsh's bash-sandbox inside srt, bounded by hcom-seat's router row denies, the state root and the credential root grant; one residual row: a bash-sandbox command inside srt on macOS was not executed by this unit, the observe-mode Router runs none, and the first real command is measured by the i2 row), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U406` once at the end.

ACCEPTANCE
1. The red lines of tests (a) to (c) at 57e5345a1 (`/tmp/u406/red.txt`) and their green lines at the head, pasted; the removed test named. 2. `python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (the three lint checks: shfmt, ruff format, prettier, as the Makefile lint target runs them) exit 0 and `make render-check` exit 0, pasted. 4. `git diff --stat 57e5345a1 HEAD` pasted; only `scripts/generate-agent-configs.py`, `tests/unit/test_dsh_profile.py`, `home/dot_dsh/profiles/router/cordis.patch.yml` and, if it named the presets, `scripts/orchestrator/README.md` in it. 5. `grep -c bash-sandbox home/dot_dsh/profiles/router/cordis.patch.yml` prints 0 and `grep -c 'preset' home/dot_dsh/profiles/router/cordis.patch.yml` prints 0, pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request with the body, and the one audit, the sweep and CI follow (standing order 49). After U404 and this unit merge and `make deploy-kit`: `dsh --profile router --dump-config` prints no `not found` line and `bash-sandbox` enabled off win32; table row i3 by its command cell through run-host-rows.py; i3's OK is the goal check (standing order 42).

CLOSURE
remove

TRUST
TRUST: the unit trusts upstream's bundle layer for the two presets and the base bundle for the bash-sandbox row, dsh's composition order as documented, and the generator's render as the one writer of the profile patch; it reads no dsh output in its tests (the composed tree and the row are read by the coordinator on the laptop after deploy), changes no row of the thak profile, and executes no command through bash-sandbox.

TIMEBOX
30 minutes.

FORBIDDEN
No hand edit of `home/dot_dsh/profiles/router/cordis.patch.yml` (the generator writes it); no change to `package.json` of any profile or to `DSH_ROUTER_BUNDLES` (U404's); no change to the thak profile; no change to any lever under `scripts/orchestrator/`; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u406/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U406`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U406-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U406-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 33, 34, 42, 44, 46, 49); the U404 brief; the decisions rows 2026-11-06T16:45:37Z (srt is the boundary, the thak decision) and 2026-11-09T03:52:16Z (the two prototypes); `handoff/09-plan-fastest-build-then-tests-2026-11-07.md` section 4.
