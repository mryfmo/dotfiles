# U4 omp config render (W2a / B-1) — brief

GOAL
Finish the omp configuration rendering so that `make update` (chezmoi apply) writes `~/.omp/agent/config.yml` `modelRoles.default` per profile from the manifest, with the two new provider ids, and the asset validator accepts them. Start from the open draft PR #406 (branch `tools/omp-config-render`, head 2e978db7) and bring it to mergeable.

SCOPE
Exclusive worktree on branch `tools/omp-config-render` (check it out from `origin/tools/omp-config-render`; do not rebase; merge `origin/main` into it if needed). May write: `home/.chezmoitemplates/omp-config-managed.yml`, `home/dot_omp/agent/modify_config.yml`, `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py` (the `omp:` model regex only), `home/dot_agents/agent-config.yaml` (only the `model_profiles.*.omp` lines and comments next to them), `home/dot_agents/README.md` (the omp section only), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_omp_config_merge.py`, `tests/unit/test_validate_agent_assets*.py`. May read anything. Nothing else; U6 owns `home/dot_agents/omp/policies/**`, U2 owns `assets.*` entries.

CONTEXT
- Functional spec: `.orchestration/tasks/dotfiles-T129-omp-config-render-a01.md` (166 lines) in the main checkout at `~/Workspace/dotfiles/.orchestration/tasks/`. Take its functional content (render targets, `omp: { model: "<provider>/<model id>" }` per profile, the modify script replacing only `modelRoles.default`, `make render-check`), not its regime ceremony (caps, Checks blocks, PING/PONG, allowed_files counts).
- Provider mapping (operator decisions D-024-129/130/131, plan 025 v14 §1): profiles `deep`, `review`, `standard` → `claude-bridge/<claude model id>`; `audit`, `audit-r2`, `security` → `openai-siwc/<openai model id>`. Fallback routes stay expressible: `anthropic/<id>` and `openai-codex/<id>`. Validator regex: `^(openai-codex|openai-siwc|anthropic|claude-bridge)/[A-Za-z0-9._-]+$`. Model ids come from each profile's existing `claude.model` / `codex.model` values in `home/dot_agents/agent-config.yaml` (e.g. `claude-fable-5-1`, `claude-opus-5-5`, `gpt-6.1-sol`, `gpt-6-astra`); the bridge lists models by pi-ai catalog id, so use the bare id after the provider prefix.
- omp 18.11.3 facts: `~/.omp/agent/config.yml` holds `modelRoles` (README of the installed package `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/README.md`); profiles live under `~/.omp/profiles/<name>/agent/` (upstream `docs/extension-loading.md`); confirm the `modelRoles` schema in the installed `src/config/` before writing the template and cite `file:line` in the PR description.
- Measured facts to respect: `.orchestration/validation/025-v13-facts-20261023.md` and `.orchestration/validation/025-pilot-facts.md` (both in the main checkout).

ACCEPTANCE
1. `uv run --no-project scripts/generate-agent-configs.py` renders the managed template deterministically from the manifest (paste the diff of the rendered output against the committed one being empty).
2. The modify script replaces only `modelRoles.default` and preserves every other key of an existing `config.yml` (unit test with a fixture containing unrelated keys; paste the test output).
3. `scripts/validate-agent-assets.py` accepts the four provider prefixes and rejects `foo/bar` (tests).
4. Existing unit tests pass: `uv run --no-project -m pytest tests/unit -q` (paste the summary line). Do not run bats.
5. PR #406 updated (push to its branch), description rewritten in English to the current content, `isDraft` cleared to ready for review. CI must be green; fix root causes.

VERIFY
`uv run --no-project -m pytest tests/unit -q`; `make render-check` if the target exists (read the Makefile first; paste); `git diff --stat origin/main...HEAD`. Network: `api.github.com` and `github.com` for `gh` and `git push`; nothing else.

TIMEBOX
75 minutes.

FORBIDDEN
No edits outside SCOPE; no changes to the `assets:` section; no rebase or force-push; no bats; no merge.

REPORT
≤ 200 words: branch, head sha, PR link and state, test summary lines, the modelRoles schema citation, deviations, follow-ups.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
