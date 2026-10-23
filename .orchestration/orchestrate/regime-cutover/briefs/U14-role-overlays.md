# U14 per-role omp overlays rendered from the manifest — brief

GOAL
Close the gap U10 measured: a named profile (`omp --profile <role>`) reads `~/.omp/profiles/<role>/agent/config.yml` (pi-utils `src/dirs.ts:312-315`), so the default-profile render of `modelRoles.default` (U4) and `skills.customDirectories` (U10) never reaches a seat. Render one overlay per role, `~/.agents/omp/profiles/<role>.yml`, from the manifest, so the seat launcher (U7) passes it as a second `--config` and every seat gets its model route and skills directories without per-profile hand edits.

SCOPE
Exclusive worktree on a new branch `feat/omp-role-overlays` from `origin/main` (main ≥ a6a409ba). May write: `home/dot_agents/agent-config.yaml` (ONLY a new `omp.roles` mapping, e.g. `orchestrator: deep`, `worker: standard`, `audit: audit`, `review: review`, `security: security`; nothing else), `scripts/generate-agent-configs.py` (render the overlays), the generated files `home/dot_agents/omp/profiles/{orchestrator,worker,audit,review,security}.yml` (committed output, checked by `make render-check`), `scripts/validate-agent-assets.py` only if the new key needs a schema line, `tests/unit/test_generate_agent_configs.py`, `docs/omp-skills.md` (one section) or `docs/omp-role-overlays.md`. Nothing else: `home/dot_agents/omp/policies/**` (U6) and the launcher (U7) are other units' files.

CONTEXT (read first)
- U10's report and PR #465 (merged a6a409ba): key `skills.customDirectories` (`src/extensibility/settings.ts:65-69`, consumed `src/extensibility/skills.ts:471-480`), manifest key `omp.skills_directories`, `~` must be expanded to the absolute home because omp resolves relative entries against cwd (`src/cli/skill-list.ts:58-64`); the generator and the modify script show the current render path (`scripts/generate-agent-configs.py`, `home/.chezmoitemplates/omp-config-managed.yml`, `home/dot_omp/private_agent/modify_private_config.yml`).
- U4's render: `model_profiles.<profile>.omp.model` holds `<provider>/<model id>` per profile (`claude-bridge/…` for deep, review, standard, express; `openai-siwc/…` for audit, audit-r2, security); the validator regex admits `openai-codex|openai-siwc|anthropic|claude-bridge`.
- omp overlays: `--config <file>` is repeatable and strict ("Config overlay not found" / "must be a YAML mapping", U6 report); the overlay is a plain config.yml-shaped mapping, so `modelRoles: {default: …}` and `skills: {customDirectories: […]}` are valid top-level keys (cite `src/config/settings.ts` for both).
- chezmoi renders `home/dot_agents/omp/profiles/*.yml` to `~/.agents/omp/profiles/*.yml` as plain files (no template needed when the generator writes the absolute home? No: the home path differs per machine, so render the skills directory with the chezmoi template function for the home directory, or keep `~` in the committed file and let the launcher expand; pick the form that keeps `make render-check` deterministic on every machine and say which, with the citation for how omp treats `~` in `skills.customDirectories` and in `modelRoles`).
- Conventions: tests via `uv run --no-project -p ">=3.11" --with pytest --with pyyaml -m pytest …`; English docs; shortcut comments where you take one.

ACCEPTANCE
1. `make render-check` up to date after generation; the five overlay files exist with `modelRoles.default` from the mapped profile and `skills.customDirectories` from `omp.skills_directories` (paste one file).
2. Tests: generator renders the overlays from a fixture manifest; a missing role mapping fails loudly; the overlay set equals the `omp.roles` keys (paste the summary).
3. Dry run under a scratch HOME (wrapper script): `omp --profile u14test --config <rendered worker overlay> --no-extensions skill list --json` lists the skills from the configured directory and `omp --profile u14test --config <overlay> config get modelRoles --json` (or the equivalent read-back U6 used) shows the role's model (paste both; cite the commands).
4. PR open with `Program-Unit: regime-cutover/U14`, title `feat(omp): render per-role omp overlays (model route and skills directories) for the seats (U14)`, English body per STANDING 14, CI green.

VERIFY
Commands above. Network: `api.github.com`, `github.com` only. Push over `https://github.com:443/mryfmo/dotfiles.git` with a gh-token askpass if SSH is refused.

TIMEBOX
45 minutes.

FORBIDDEN
No `assets:` edits, no policy file edits, no launcher edits, no real `~/.omp`, no merge, no rebase.

REPORT
≤ 150 words: branch, head sha, PR link, CI state, the overlay form chosen and its citations, the dry-run lines, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (19 lines) before any command.
