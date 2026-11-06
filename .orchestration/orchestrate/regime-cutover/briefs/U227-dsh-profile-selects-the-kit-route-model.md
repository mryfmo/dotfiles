# U227 the kit's DeepSeek harness profile selects its own route and model

GOAL
M-21 measured on 2026-11-06 (decisions rows of phase `M-21`, 03:50:31Z) that the kit profile boots under srt and composes with the ollama-cloud route under `llm-pi-ai`, but the base bundle's `agent-default-model` row still reads `provider: deepseek-official, model: deepseek-flash`, so the one headless turn ended with `dsh: NO_ADAPTER: no adapter registered for provider "deepseek-official"`. The kit patch disables the official adapters and adds a route without ever pointing the agent at it. This unit makes the profile renderer emit the `agent-default-model` row for the kit's route and model, read from the manifest, so a turn on the thak profile reaches ollama-cloud.

SCOPE
A new branch `feat/dsh-profile-default-model` from `origin/main` c4195463 (your tree is positioned on it). May write: `scripts/generate-agent-configs.py` (`render_dsh_profile_patch` only), `tests/unit/test_dsh_profile.py`, the rendered `home/dot_dsh/profiles/thak/cordis.patch.yml` (regenerated, never edited by hand), `home/dot_agents/agent-config.yaml` only if a new key is needed (see CHANGE 1), and the body file `../U227-pr-body.md` beside your tree. Not: the updater, the asset entry, `hcom-seat`, any other renderer.

CONTEXT
Measured 2026-11-06 at c4195463. `render_dsh_profile_patch` (`scripts/generate-agent-configs.py:2231-2296`) emits the rows session-log-deepseek, llm-deepseek, llm-deepseek-account, bash-sandbox, llm-pi-ai (one provider per `DSH_ROUTES` entry with the sorted dsh models of `model_profiles.*.dsh`) and the hooks-claude-code insert. `model_profiles.<tier>.dsh` entries (`home/dot_agents/agent-config.yaml:555-601`) name `model` and `route`; `standard` is `deepseek-v4.1-flash:1017` on `ollama-cloud`, `deep`, `review`, `security` and `audit` are `deepseek-v4-pro:0813` on `ollama-cloud`. The composed tree at the pinned tag shows the base bundle row `- id: agent-default-model` / `name: '@deepseek-ai/dsh-agent-default-model'` with `provider` and `model` under its config. The provider key the agent row must name is the one `llm-pi-ai` registers for the route; read `packages/llm/llm-pi-ai` (or its README) and `packages/agent/agent-default-model` (or wherever the base bundle keeps them; `pnpm` layout under the installed tree `~/.dsh/dsh/current/packages/`, read-only, and the tag's source on GitHub are both acceptable sources) at `dsh-v0.2.1-rc.5` to confirm whether the provider id equals the providers map key (`ollama-cloud`) or carries a prefix, and cite the file and line in the PR body. `tests/unit/test_dsh_profile.py` reads the rendered patch as text, splits it into top-level `- id:` blocks (`rows()`), and compares the llm-pi-ai models and the hooks insert with the manifest; it refuses a `dsh-bash-sandbox` mention.

CHANGE
1. The default model. Read it from the manifest with no new key if `interactive_profile` or an existing field gives the tier; otherwise add one key `dsh_default_profile: standard` beside `interactive_profile` (`agent-config.yaml:602`) and read `model_profiles[<that tier>].dsh`. Record in the PR body which form you took and why (the coordinator's default is the `standard` tier; the Router preset of a later unit sets its own model and does not use this row).
2. Renderer: emit, after the llm-pi-ai block and before the insert, the row
   `- id: agent-default-model` / `  config:` / `    provider: <provider id of the route>` / `    model: <the tier's dsh model>`, with the provider id in the form CHANGE's reading established. Fail (`fail(...)`) when the tier names no dsh entry or its route is not in `DSH_ROUTES`.
3. Regenerate: `uv run --with pyyaml scripts/generate-agent-configs.py` so `home/dot_dsh/profiles/thak/cordis.patch.yml` carries the row; `make render-check` clean.
4. Tests in `test_dsh_profile.py`: the patch has exactly one `agent-default-model` block; its `model` equals the manifest tier's dsh model and its `provider` the route's provider id; the model it names is among the llm-pi-ai models of the same route; a manifest fixture whose default tier lacks `dsh` makes the renderer fail with a message naming the tier (use the fixture loader the file already imports).
5. The body `../U227-pr-body.md`: Summary (the measured refusal, the missing row, the fix), Contract (guarantee: a thak turn selects a model the kit's route serves; leaves out: the Router preset's model, the API key's placement on hosts, the srt settings for dsh; `TRUST:` sentence as below), a Threat table `row | risk | status | evidence` with rows for the renderer, the regenerated patch and the test plus an `orchestrator effect` row, each `closed` with the ACCEPTANCE command, and `Program-Unit: regime-cutover/U227`.

ACCEPTANCE
1. `grep -n -A3 '^- id: agent-default-model' home/dot_dsh/profiles/thak/cordis.patch.yml` prints the block with `provider:` and `model: deepseek-v4.1-flash:1017` (or the model of the tier CHANGE 1 chose, named in the body).
2. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0, no diff.
3. `uv run python -m unittest tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs tests.unit.test_scratch_git` OK (paste the count), the new tests named in the paste.
4. `make validate-agent-assets` exit 0.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
6. The PR body cites the upstream file and line that fixes the provider id form.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. The live proof (one headless turn on `dsh --profile thak` under srt with the route's key exported) is the coordinator's step after the merge and the key's placement, recorded in the store as the M-21 task 06 rerun.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the manifest's model_profiles as the single source of models and routes and the pinned tag's plugin configuration keys as read from its source; it changes one renderer function and its test, reads no network at test time, and does not place any API key or change any sandbox setting.

TIMEBOX
45 minutes.

FORBIDDEN
No hand edit of the rendered patch; no change to the updater, the asset entry or `hcom-seat`; no API key anywhere; no local bats; no network read beyond the two upstream source files named in CONTEXT; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your TASK; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line beside your tree (`../U227-progress.txt`) every ten minutes at most; if that path is not writable from your seat, write it under your tree's `.state` directory the TASK names and say so in the RESULT.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U227-pr-body.md`, or under `.state` as above) per CHANGE 5.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, the provider-id source line, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35, 37); `AGENTS.md` (Comment Policy, Test Policy, Audit); the decisions rows of phase `M-21` dated 2026-11-06T03:50:31Z.
