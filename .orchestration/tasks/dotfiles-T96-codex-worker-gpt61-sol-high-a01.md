# AGMSG-TASK dotfiles-T96-codex-worker-gpt61-sol-high-a01 (role constellation: worker gpt-6.1-sol high, auditor gpt-6-astra high)

Drafted 2026-10-04 by the orchestrator seat from the operator's instruction (final wording): 「指示役 fable-5.1 high、監査役 gpt-6 astra high、作業役 gpt-6.1 sol high / opus-5.5 high」. Queued for the next free Claude seat (a model profile is not a sandbox or permission source; the manifest `model_profiles` block, its rendered Codex profile file and the model-selection rule are the whole scope).

## Objective

The role constellation the operator fixed: orchestrator = Claude `claude-fable-5-1` high (profile `deep`, already so), auditor = Codex `gpt-6-astra` high (profile `audit`), worker = Codex `gpt-6.1-sol` high and Claude `claude-opus-5-5` high (profile `standard`; the Claude side is already so).

1. `home/dot_agents/agent-config.yaml`: `model_profiles.standard.codex` → `model: gpt-6.1-sol`, `model_reasoning_effort: high` (today `gpt-5.6-terra` / `medium`); `model_profiles.audit.codex` → `model: gpt-6-astra`, `model_reasoning_effort: high` (today `gpt-6.1-sol` / `xhigh`). `deep.claude` (fable-5.1 high) and `standard.claude` (opus-5.5 high) already match and stay. Every other profile stays as is. `scripts/validate-agent-assets.py` pins the audit profile (~74 and ~678-684): update that pin to `gpt-6-astra` / `high` in the same commit.
2. Regenerate the rendered outputs with `make render-check`: the `standard` and `audit` Codex profile sources under `home/dot_codex/`, `home/dot_agents/model-profiles.env`, and any Claude settings fragment that embeds a profile.
3. `home/dot_config/claude/rules/model-selection.md` line 3: the role constellation reads `orchestrator=\`deep\` (fable-5.1 high, advisor fable), worker=\`standard\` (Claude opus-5.5 high; Codex gpt-6.1-sol high), auditor=\`audit\` (Codex gpt-6-astra high, read-only sandbox)`; state which Codex models need API-key auth on which seat (the ChatGPT-login account rejects `gpt-6.1-sol`, so the worker seat needs it; verify whether `gpt-6-astra` does and record the answer). Mirror the sentence in `home/dot_config/codex/AGENTS.md` if it lists the constellation.
4. Tests that pin `gpt-5.6-terra`/`medium` for `standard` or `gpt-6.1-sol`/`xhigh` for `audit` (`tests/unit/test_generate_agent_configs.py:44,446,478,550-551,599,629`, `tests/unit/test_validate_agent_assets.py:185`, `tests/unit/test_runtime_health.py` if it checks the audit profile) follow.

Forbidden: any other profile; permissions, sandbox, hooks; launchers; the audit lane's `--sandbox read-only` and prompt.

[memory:decision] dotfiles-T96 (operator 2026-10-04): the role constellation is orchestrator fable-5.1 high (`deep`), auditor Codex gpt-6-astra high (`audit`), worker Codex gpt-6.1-sol high and Claude opus-5.5 high (`standard`); the Codex worker seat needs API-key auth for gpt-6.1-sol.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/codex-worker-gpt61-sol origin/main` (6de95167 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the `standard.codex` and `audit.codex` mappings), the rendered Codex profile sources for `standard` and `audit`, `scripts/validate-agent-assets.py` (the audit profile pin only), `home/dot_agents/model-profiles.env`, `home/.chezmoitemplates/*` only where `make render-check` regenerates them, `home/dot_config/claude/rules/model-selection.md` (line 3), `home/dot_config/codex/AGENTS.md` (constellation sentence, if present), `tests/unit/**` files that pin the old value
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T96-codex-worker-gpt61-sol-high-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
grep -n 'model\|reasoning' home/dot_codex/modify_private_standard.config.toml home/dot_codex/modify_private_audit.config.toml | head
grep -rn 'gpt-5.6-terra\|gpt-6.1-sol\|gpt-6-astra' home/dot_agents/agent-config.yaml home/dot_codex scripts tests
make validate-agent-assets
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if a Crit plan review ran.
3. Artifacts at the exact expected paths; validation with verbatim commands and raw output, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T96` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=20.

## Dispatch

- 2026-10-04 (queued for the first free Claude seat once PR #253 (T69) has merged, because both edit `home/dot_config/claude/rules/model-selection.md` line 3). Branch from the commit that merged #253 or later. Routing: model profiles are not an execution-boundary source, so a Claude seat is fine.
- 2026-10-04 23:00Z: also wait for T76 (`chore/ineffective-settings`, a005, dispatched 13:44Z) to merge, because both edit `home/dot_agents/agent-config.yaml`, `scripts/validate-agent-assets.py` and `tests/unit/test_generate_agent_configs.py`; parallel tasks need pairwise-disjoint allowed_files (T88). Branch from the commit that merged T76 or later.
- 2026-10-05 00:25Z dispatched to `claude-standard-dot-a006` (worker-d, wY:p2): T69 merged as 04bce61b, T76 as 40993f20. Branch from `origin/main` 40993f20 or later with `git switch -c <branch> --no-track origin/main`. Note T76 reshaped `agent-config.yaml` (no `mcp_servers` entries, no `enabledPlugins`) and `scripts/validate-agent-assets.py`; re-read the current line numbers before editing. The operator still has to supply Codex API-key auth for the gpt-6.1-sol worker seat; this task only changes the rendered profiles and pins.

### PONG decision (orchestrator, 2026-10-05 00:30Z) — README sentence allowed

- Allowed files gain `README.md`, limited to the auditor sentence at lines 289-290 (and any other line that states the audit profile's model or auth; `grep -n 'gpt-6.1-sol\|API-key auth' README.md`). Rewrite it to the new constellation (auditor `audit` = Codex gpt-6-astra high, read-only sandbox; worker `standard.codex` = gpt-6.1-sol high). Same class of change, same PR.
- The auth clause: state only what the live probe proved. Paste the `codex --profile security exec …` probe (command and output) in the validation file; if gpt-6-astra answered under the ChatGPT login, drop the "requires Codex API-key auth" clause from README and from `model-selection.md` line 3; if the new worker model gpt-6.1-sol was not probed, say so in the report rather than asserting its auth path.
- `ADH_PROFILE` (~74): correct, leave it (T79 removes it).

### PONG decision 2 (orchestrator, 2026-10-05 00:35Z) — memory text

Approved. Record the `[memory:decision]` with its last clause replaced by: "both Codex models answered under the ChatGPT login (probe 2026-10-05: `codex --profile audit exec` gpt-6.1-sol OK, `--profile security` gpt-6-astra OK), so neither seat needs Codex API-key auth; the 2026-10-01 rejection no longer reproduces." Paste both probe commands and outputs in the validation file. The task file's original clause is superseded by this decision.
