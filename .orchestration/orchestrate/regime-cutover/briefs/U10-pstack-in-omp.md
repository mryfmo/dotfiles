# U10 pstack skills visible inside omp seats (plan item G / H9) — brief

GOAL
Make omp 18.11.3 list and load the pstack skills already linked under `~/.agents/skills/<name>` (the pstack asset, pinned sparse clone at `~/.local/share/pstack/repo`) inside every seat profile, through omp's own skills discovery configuration rendered from the manifest, and prove it with a dry run that shows the skill names in omp's skill list.

SCOPE
Exclusive worktree on a new branch `feat/omp-pstack-skills` from `origin/main` (main ≥ 34e216e9). May write: the omp config render path that U4 landed (`home/.chezmoitemplates/omp-config-managed.yml`, `home/dot_omp/private_agent/modify_private_config.yml`, `scripts/generate-agent-configs.py`) ONLY for the new skills-discovery key(s); `home/dot_agents/agent-config.yaml` ONLY for a new `omp:`-section key naming the skills directories (not `assets:`, not `model_profiles`); `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_omp_config_merge.py` (the merge must now replace the new key as well as `modelRoles.default` and still preserve unrelated keys); `docs/omp-skills.md`. Nothing else.

CONTEXT (read first)
- Functional spec: `~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-pstack-asset-a01.md` lines 79-95 (omp reads `~/.agents/skills` only after the skills provider is enabled; the task calls it `enabledProviders`, confirm the real key) and plan 023 §G/H9 (`~/Workspace/dotfiles/.orchestration/plans/023-omp-hcom-migration.md` lines 52-54). Drop the regime ceremony.
- omp 18.11.3 source: `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/src/extensibility/skills.ts`, `src/discovery/**` (skills discovery, `~/.agents/skills`, `.agents/skills`, provider toggles), `src/config/settings.ts` (the settings keys), and the upstream docs `https://raw.githubusercontent.com/can1357/oh-my-pi/main/docs/skills.md` plus any `docs/*discovery*` / `docs/skills/*.md` the index lists (`~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/dist/docs-index.generated.txt`). Cite `file:line` for the key you set and for the directory omp scans.
- The U4 render: `scripts/generate-agent-configs.py` renders `home/.chezmoitemplates/omp-config-managed.yml` from the manifest; the private modify script merges `modelRoles.default` into the live `~/.omp/agent/config.yml` under uv with PyYAML (read both before adding the second key; keep the merge's "replace only our keys" contract and its idempotence test).
- Measured facts to respect: `~/Workspace/dotfiles/.orchestration/validation/025-pilot-facts.md` (#G1..#G1-3: the session path `omp -e … --no-session -p …` is the instrument that shows what a seat loads; `omp models` is not).

ACCEPTANCE
1. The manifest gains one `omp:` key for the skills directories (default `~/.agents/skills`), the generator renders it, the modify script merges it (test: a config with unrelated keys keeps them; second apply is a no-op; `make render-check` up to date). Paste the test summary.
2. Dry run under a scratch HOME (wrapper script exporting `HOME=$TMPDIR/u10-home`; link two real pstack skill directories from `~/.local/share/pstack/repo/skills/` or `~/.agents/skills/` into the scratch `~/.agents/skills/`): with the rendered config present, omp's skill listing (find the command or the `--mode json` startup event that lists skills; cite it) names those skills; without the key it does not. Paste both.
3. `docs/omp-skills.md`: the key, the directory, the pin of the pstack asset (`~/.local/share/pstack/repo`, commit from `home/dot_agents/agent-config.yaml` if present, else the receipt `~/.local/state/pstack/skills.links`), and how a seat's SKILL (e.g. `hcom-worker`) and pstack skills coexist.
4. PR open with `Program-Unit: regime-cutover/U10`, title `feat(omp): render omp's skills directories so pstack skills load in every seat (U10)`, English body per STANDING 14, CI green.

VERIFY
`uv run --no-project -p ">=3.11" --with pytest --with pyyaml -m pytest tests/unit/test_generate_agent_configs.py tests/unit/test_omp_config_merge.py -q`; `make render-check`; the two dry runs. Network: `raw.githubusercontent.com` (docs), `api.github.com`, `github.com`. Push over `https://github.com:443/mryfmo/dotfiles.git` with a gh-token askpass if SSH is refused.

TIMEBOX
60 minutes.

FORBIDDEN
No `assets:` or `model_profiles` edits, no real `~/.omp`, no edits outside SCOPE, no merge, no rebase.

REPORT
≤ 150 words: branch, head sha, PR link, CI state, the key and its citation, the dry-run lines, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (19 lines) before any command.
