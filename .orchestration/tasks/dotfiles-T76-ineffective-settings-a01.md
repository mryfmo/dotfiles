# AGMSG-TASK dotfiles-T76-ineffective-settings-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T76). Dispatch after T71 (`scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`) has merged; the two scripts are shared with it, everything else is disjoint from in-flight tasks.

## Objective

Principle 9: configuration that has no effect is deleted, not carried.

1. **`enabledPlugins: {}`** (`home/dot_agents/agent-config.yaml:277`, generator `render_claude_settings` ~468, rendered `home/.chezmoitemplates/claude-settings-managed.json:132`): remove the manifest key, the generator line and therefore the rendered key. Plugins are installed by the managed asset lifecycle (`make update`), not by this empty map.
2. **Six disabled MCP servers** (`agent-config.yaml:308-430`: `context7`, `filesystem_dotfiles`, `github`, `time`, `sequential_thinking`, `playwright`, every one `enabled: false` on both agents): reduce to `mcp_servers: {}`. Rendered outputs follow: no `[mcp_servers.*]` table in `home/.chezmoitemplates/codex-config-managed.toml`, and `home/dot_claude/private_mcp.json.tmpl` renders `{"mcpServers": {}}`.
   - `scripts/validate-agent-assets.py` `validate_claude_mcp_config` (~457-462) currently fails on an empty map (`not servers`); make it accept `{}` (still a dict) and keep the per-server checks for any future entry. `validate_mcp_parity` (~720-729) and the manifest loop (~688-709) already handle empty maps; confirm with the tests rather than by reading.
   - `DEPRECATED_MCP_PACKAGES` stays (it guards future entries).
3. **gwq `[claude]` queue** (`home/dot_config/gwq/config.toml:1-15`, including `[claude.execution]`, `[claude.queue]`, `[claude.worktree]`): delete; keep `[finder]`. Nothing in this repository reads the queue directory (`grep -rn 'gwq/claude' home scripts tests` → confirm empty before deleting).
4. **Tests:** `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_codex_config_merge.py` and `tests/unit/test_claude_settings_merge.py` where they pin `enabledPlugins`, the six server names or the `must define mcpServers` failure; add one case that an empty `mcp_servers` renders an empty Codex table set and `{"mcpServers": {}}` and validates.

Forbidden: `alwaysThinkingEnabled`, `allowUnixSockets`, Codex `hooks.state`, `permissions`, `sandbox`, `model_profiles`, hooks of either agent; any file under `home/` other than the three named above and the two rendered templates.

[memory:decision] dotfiles-T76 (operator 2026-10-03): the empty `enabledPlugins` map, the six never-enabled MCP server definitions (context7, filesystem_dotfiles, github, time, sequential_thinking, playwright) and the gwq `[claude]` queue are deleted; MCP servers are added back only when one is enabled for a target agent.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/ineffective-settings origin/main` (the commit that merged T71 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/codex-config-managed.toml`, `home/dot_claude/private_mcp.json.tmpl`, `home/dot_config/gwq/config.toml`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_codex_config_merge.py`, `tests/unit/test_claude_settings_merge.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T76-ineffective-settings-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -n "enabledPlugins" home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json scripts/generate-agent-configs.py ; echo "rc=$?"
grep -c "^\[mcp_servers\." home/.chezmoitemplates/codex-config-managed.toml
grep -c "enabled = false" home/.chezmoitemplates/codex-config-managed.toml
grep -rn 'gwq/claude' home scripts tests ; echo "rc=$?"
make render-check
make validate-agent-assets
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Live acceptance (operator, after merge and `make update`): `gwq list --json | jq length` runs; `make doctor` exits 0; `jq '.mcpServers|length' ~/.claude/private_mcp.json` → 0.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; close your crit server if Plan Mode opened one; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.
