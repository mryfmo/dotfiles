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

## Dispatch

- 2026-10-04 22:50Z to `claude-standard-dot-a005` (worker-c, wT:p2) after its T72 acceptance (PR #256 merged as 2ad504e3; T71 merged as 65915b93). Branch from `origin/main` 2ad504e3 or later; keep the earlier branches untouched. Note that T72 (merged) added `assets.chezmoi-bootstrap` and the `setup.sh` scan to `scripts/validate-agent-assets.py`; T96 (queued, model_profiles only) and this task touch `agent-config.yaml` in disjoint sections.

## Revise round 1 (orchestrator, 2026-10-04 23:45Z) — Codex P2 4177937781 is a real convergence gap

The deletions on 526dd18b are accepted as they stand. The Bot finding stands too: `modify_private_config.toml` `merge_config` keeps every current-only table, so the six retired `[mcp_servers.*]` tables stay in `~/.codex/config.toml` on every machine that applied the parent revision (the orchestrator confirmed all six at lines 33-75 of its live file). Principle 9 says dead configuration is deleted, not carried, and the operator must not hand-edit two hosts, so purge them in the merge script:

1. **Allowed files gain** `home/dot_codex/modify_private_config.toml` and `tests/unit/test_codex_config_merge.py` (routing: a Codex-only rendering source, so a Claude seat may edit it).
2. In `modify_private_config.toml`, add a module constant `RETIRED_MCP_SERVERS = ("context7", "filesystem_dotfiles", "github", "time", "sequential_thinking", "playwright")` with a one-line comment naming T76, and in `merge_config` drop a current-only chunk whose table name is `mcp_servers.<retired>` **and** whose body contains an `enabled = false` assignment (the last managed state of all six); a table the operator re-enabled or re-added with `enabled = true` is kept as any other current-only table. Follow the existing stale-removal precedent (`test_managed_permgate_replaces_stale_private_ccgate_hook`); keep the diff to the constant plus the filter, no new helpers unless `split_chunks` already exposes what you need.
3. Tests: one case where the six disabled retired tables disappear while a seventh unknown table and a retired name with `enabled = true` survive; the existing cases stay green.
4. `make render-check`, `make validate-agent-assets`, `make unit-test` (verbatim), then `gh pr update-branch 257` (main is 04bce61b after T69) and CI on the new head; Bot wait per SKILL; reply nothing on the thread (the orchestrator replies `fixed:<sha>` and resolves it). One commit for the fix, then RESULT.

## Revise round 2 (orchestrator, 2026-10-05 00:00Z) — task-level audit of f805ee3a is `incorrect` (2), both reproduced by the auditor

1. **P1, orphaned sub-tables.** Purging `[mcp_servers.<retired>]` leaves its child tables (`[mcp_servers.<retired>.env]`, `.http_headers`, …) behind, and Codex then fails with `invalid transport`. When the parent chunk is dropped, drop every current-only chunk whose name starts with `mcp_servers.<retired>.` as well (and only then; a kept parent keeps its children).
2. **P2, enablement by parsing, not regex.** `DISABLED.search(chunk)` also matches `enabled = false` inside a string value (for example an `env` entry). Decide with the parsed field instead: `tomllib.loads(chunk)` on the parent chunk and read `["mcp_servers"][name].get("enabled")`; treat a chunk that fails to parse as *kept* (never purge what you cannot read). Remove the `DISABLED` regex and the `re` import if nothing else uses them.
3. Tests: extend the round-1 case (or add one) so a retired disabled parent **with** an `.env` child disappears together with the child, a retired parent with `enabled = true` and an `env` string containing the text `enabled = false` is kept, and a kept parent keeps its child.
4. `make unit-test`, `make render-check`, `make validate-agent-assets` (verbatim), one commit, `gh pr update-branch 257` only if `main` moved, CI, Bot wait per SKILL, RESULT. Orchestrator replies on any new thread.
