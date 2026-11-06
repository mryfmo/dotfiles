# U227b the kit's DSH profile points the agent at the login route: the omp-gateway plugin row, the default model row, the install link

GOAL
U227 (PR 675, held) made the profile renderer emit `agent-default-model` for the Ollama Cloud route; the operator withdrew every API-key route on 2026-11-06 (frame row 05:46:33Z), U238 chose the login route through `omp auth-gateway stdio`, and U240 built the DSH adapter plugin at `home/dot_dsh/plugins/omp-gateway/` (PR 679; U240b is moving the system text into the first user turn in parallel; the plugin's package name is `dsh-omp-gateway`). U240's loading mechanism (its body, "Loading mechanism"): a profile loads an out-of-tree plugin through a `link:` dependency in the profile's `package.json`, the `node_modules/dsh-omp-gateway` symlink, and a bare-name `insert` row in `cordis.patch.yml`. This round makes the kit profile `thak` carry those rows and the default model, removes the Ollama provider rows, and gives the updater the link step, so a `dsh --profile thak` turn on this host reaches Claude through the operator's login once PR 679 lands.

SCOPE
A new branch `feat/dsh-profile-login-route` from `origin/main` b49be338 (your tree is `/tmp/dotfiles-wt/U227b`). May write: `scripts/generate-agent-configs.py` (`render_dsh_profile_patch`, `DSH_ROUTES`, `DSH_MODEL_RE`, the `model_profiles.*.dsh` validation), `home/dot_agents/agent-config.yaml` (the six `model_profiles.<tier>.dsh` rows and the `assets.deepseek-harness.note` sentence that names the route), the rendered `home/dot_dsh/profiles/thak/cordis.patch.yml` and `home/dot_dsh/profiles/thak/package.json` (regenerated, never edited by hand), `scripts/update-agent-assets.sh` (`update_deepseek_harness` only: the link step), `tests/unit/test_dsh_profile.py`, `tests/unit/test_update_agent_assets.py`, `tests/unit/test_dsh_hook_coverage.py` only if the hooks row moves, and the body `../U227b-pr-body.md`. Not: the plugin directory (U240's), `hcom-seat`, the srt settings (U251), the PRD.

CONTEXT
Measured at b49be338. `render_dsh_profile_patch` (`scripts/generate-agent-configs.py:2231-2296`) emits the rows `session-log-deepseek`, `llm-deepseek`, `llm-deepseek-account`, `bash-sandbox`, one `llm-pi-ai` provider per `DSH_ROUTES` entry (`:164`, `("ollama-cloud",)`, rendered at `:2272-2281` with `displayName: Ollama Cloud`, `baseURL: https://ollama.com/v1`, `apiKeyEnv: OLLAMA_API_KEY`) and the `hooks-claude-code` insert with `configPath` `~/.claude/settings.json` (`:170`). `DSH_MODEL_RE` (`:167`) admits an Ollama id; `model_profiles.<tier>.dsh` rows (`home/dot_agents/agent-config.yaml:555-601`) name `model` and `route: ollama-cloud`. The U227 brief (`briefs/U227-dsh-profile-selects-the-kit-route-model.md`) measured the composed tree's `agent-default-model` row (`provider`, `model` under its config) and is the reference for how the row is addressed. The plugin's config rows (`home/dot_dsh/plugins/omp-gateway/config.mjs` on branch `feat/dsh-omp-gateway-adapter`, readable at `/tmp/dotfiles-wt/U240`): `command` (default `omp`), `args` (default `["auth-gateway","stdio"]`), `env`, `cwd`, `providers` (default `["claude-bridge"]`), `models`, `maxTokens`, `readyTimeoutMs`. `dsh plugin add link:` fails on this host (`ENOEXEC` on the mise pnpm shim, U240 body), so the updater writes the symlink itself. The updater's install transaction and its tests: `scripts/update-agent-assets.sh#update_deepseek_harness`, `tests/unit/test_update_agent_assets.py` (U178 to U178d, U226). The bridge serves model ids `claude-bridge/<claude model>`; the kit's omp profiles name `claude-bridge/claude-haiku-5-5`, `claude-bridge/claude-opus-5-5`, `claude-bridge/claude-fable-5-1` (`agent-config.yaml:554-577`).

DATA SHAPE
The manifest stays the single source. `DSH_ROUTES = ("omp-gateway",)`; a `model_profiles.<tier>.dsh` row is `{ model: <claude model id without provider prefix>, route: omp-gateway }`, validated by a `DSH_MODEL_RE` that admits the bridge's model ids (`claude-` followed by the launcher-safe form; read PROFILE_VALUE_RE) and no Ollama tag form. The renderer emits, in place of the `llm-pi-ai` provider rows: one `insert` row `{ id: omp-gateway, name: dsh-omp-gateway, config: { command: omp, args: [auth-gateway, stdio], providers: [claude-bridge], models: <sorted distinct dsh models, each prefixed claude-bridge/> } }` and one `{ id: agent-default-model, config: { provider: claude-bridge, model: <the interactive_profile tier's dsh model, agent-config.yaml:602> } }`; the profile `package.json` gains `"dsh-omp-gateway": "link:../../plugins/omp-gateway"` beside the hooks dependency. The updater's link step: after the profile files are in place and before the receipt, `ln -sfn ../../../plugins/omp-gateway <DSH_HOME>/profiles/thak/node_modules/dsh-omp-gateway` (relative target so a moved `DSH_HOME` keeps working; `mkdir -p` the `node_modules` directory; refuse when the plugin directory is absent or not a directory), idempotent, recorded in the receipt.

CHANGE
1. Manifest: the six `dsh` rows become `{ model: claude-haiku-5-5, route: omp-gateway }` for `standard`, `{ model: claude-opus-5-5, route: omp-gateway }` for `review`, `deep`, `security`, `audit`, and `claude-haiku-5-5` for the cheapest tier if one exists (mirror the omp rows of each tier, `:554-577`); the asset note sentence that names the Ollama route is rewritten to name the login route and the plugin link.
2. Generator: `DSH_ROUTES`, `DSH_MODEL_RE`, the validation message, `render_dsh_profile_patch` per DATA SHAPE; the Ollama provider lines and their comment go. Run the generator; commit the rendered files.
3. Updater: the link step per DATA SHAPE with its refusals; the dry-run and the already-installed paths behave as the transaction's rules say (read U178d's body in `gh`-free form: the brief `briefs/U178d-dsh-updater-input-table-round4.md`).
4. Tests: `test_dsh_profile.py` asserts the two rows, the package.json dependency, the absence of `apiKeyEnv`, `ollama`, `OLLAMA` in the rendered files, and the validator's refusal of an Ollama-form model id; `test_update_agent_assets.py` covers the link step (created, idempotent on rerun, refused when the plugin directory is missing, relative target), with the fake tools the module already has.
5. Composition proof in a scratch `DSH_HOME` under `/tmp`: copy the rendered profile there, link `node_modules/dsh-omp-gateway` to `/tmp/dotfiles-wt/U240~/plugins/omp-gateway`, and run `~/.dsh/bin/dsh --profile thak --dump-config` (the hooks plugin may be absent in the scratch; if the dump refuses for that reason alone, disable that one row through a `--patch` overlay and say so); paste the `omp-gateway` and `agent-default-model` entries of the composed tree. Then one headless turn with a `--patch` overlay that sets `command` to `node` and `args` to the stub gateway (`/tmp/dotfiles-wt/U240~/plugins/omp-gateway/stub-gateway.mjs`): paste the `pong`.
6. The body `../U227b-pr-body.md`: Summary, Contract (guarantee: the rendered thak profile names no API key and no Ollama route, points the agent at provider `claude-bridge` through the `dsh-omp-gateway` row, and the updater links the plugin into the profile idempotently; leaves out: the plugin itself (PR 679), the srt profile (U251), the real-login turn (the coordinator's item in `tests/dsh-login-route.tsv`)), Threat table (the link target and its refusals, the command and args rows as configuration, the manifest as the one source), Verification (ACCEPTANCE pasted), and a line that this PR merges after PR 679.

ACCEPTANCE
1. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 with no diff.
2. `make validate-agent-assets` exit 0, no ERROR line.
3. `grep -rn -iE 'ollama|apiKeyEnv|OLLAMA' home/dot_dsh/profiles/thak/ home/dot_agents/agent-config.yaml scripts/generate-agent-configs.py` prints nothing except the manifest note's withdrawal sentence if you keep one (say so).
4. `uv run python -m unittest tests.unit.test_dsh_profile tests.unit.test_update_agent_assets tests.unit.test_dsh_hook_coverage tests.unit.test_scratch_git` OK (paste the count; the new tests named).
5. The composition dump's two entries and the stub `pong` pasted (CHANGE 5).
6. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0, `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0, `make shellcheck` exit 0, `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The real-login turn on the thak profile is the coordinator's row in `tests/dsh-login-route.tsv` once PR 679 and this PR are both in.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the manifest's `model_profiles` as the one source of the model ids, U240's measured loading mechanism and the plugin's config rows at its branch head, and the updater's existing transaction as the place of the link step; it reads no credential, sends no model request, and does not decide the srt profile or the plugin's code.

TIMEBOX
75 minutes.

FORBIDDEN
No API key, `apiKeyEnv` or Ollama row anywhere; no edit of the plugin directory; no `/v1/messages` request to the real omp; no write under `~/.dsh`, `~/.omp`, `~/.agents` or `~/Workspace`; no edit of `hcom-seat`; no local bats; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 54)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U227b` and the coordinator fetches it by path.
- Progress line beside your tree (`../U227b-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Subtract Before You Add: the Ollama rows go before the new rows come).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45); `AGENTS.md`; `briefs/U227-dsh-profile-selects-the-kit-route-model.md` (round 1, held); `briefs/U240-dsh-adapter-over-omp-stdio-gateway-prototype.md`; the `decisions.tsv` rows of 2026-11-06 05:46:33Z (frame), 05:56:15Z (U238 design) and the M-21 rows.
