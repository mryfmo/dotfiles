# Report: dotfiles-T76-ineffective-settings-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/ineffective-settings` from `origin/main` 2ad504e3. Earlier branches are untouched.
- **task_rev:** `sha256:36e87971…ba85`, matched in the main checkout.
- **PR:** #257, https://github.com/mryfmo/dotfiles/pull/257. One commit, `526dd18b`, which is the final head.
- **Final head state:** CI green (13 pass), branch up to date, `mergeable_state` `blocked` only by the unresolved bot thread below.
- **Status:** ready_for_review.

## 1. What changed

1. **`enabledPlugins: {}`:** removed from the manifest (with its three-line comment), from the `render_claude_settings` line, and so from the rendered `claude-settings-managed.json`.
   - Safety: `modify_private_settings.json` (unchanged) keeps any key present only in the current file (`merge_settings`, lines 156-157), so a user's runtime `enabledPlugins` survives.
   - `test_runtime_enabled_plugins_survive_a_managed_file_without_the_key` pins that.
   - The validator's guard against a non-empty managed `enabledPlugins` (`validate_claude_settings`) stays and is now trivially satisfied.
2. **Six MCP servers:** `mcp_servers: {}`, with a one-line comment that servers return only when one is enabled. The generator rewrote both templates:
   - the Codex template has no `[mcp_servers.*]` table and no `enabled = false` (both counts 0);
   - `private_mcp.json.tmpl` renders `{"mcpServers": {}}`.
   - `validate_claude_mcp_config` now requires `mcpServers` to be a mapping and accepts an empty one. A missing key or a list fails with "must define mcpServers as a mapping", and the per-server checks are kept.
   - `validate_mcp_parity` passes on empty maps (tested), and `DEPRECATED_MCP_PACKAGES` stays.
3. **gwq:** `[claude]`, `[claude.execution]`, `[claude.queue]` and `[claude.worktree]` are deleted; `[finder]` onward is kept. Before deleting, `grep -rn 'gwq/claude' home scripts tests` found only the config file's own two lines. After, rc=1.
4. **Tests:**
   - `test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map` (generator);
   - `test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping` (validator; includes parity);
   - the merge test above.
   - The generator fixture drops `enabledPlugins`.
   - The first two fail against the `origin/main` scripts, and the merge test passes there, because it pins an existing guarantee.
   - The fixtures in `test_codex_config_merge.py` and `test_claude_settings_merge.py` still use `filesystem_dotfiles`, `github` and `enabledPlugins` as generic merge input. They exercise the merge scripts, not the manifest, so they stay unchanged; all 161 tests in the four named suites pass.
   - `make unit-test` passes with 788 tests.

## 2. Codex bot thread 4177937781: proposed `not-applicable` in round 0, `fixed:f2db43f9` in revise round 1 (see below)

"Purge retired Codex MCP tables during migration." The finding is correct about the mechanism. `modify_private_config.toml` `merge_config` (lines 159-160) appends every current table missing from the new managed baseline. A simulated apply merges the new baseline into the `origin/main` baseline as the current file (verbatim in the validation file). All six `[mcp_servers.*]` tables remain in `~/.codex/config.toml`, each still `enabled = false`.

They are inert, not "locally enabled". While they were managed, every apply replaced each table wholesale with the baseline chunk (`enabled = false`), so the last applied state of all six is disabled. A purge needs a retired-table list in `home/dot_codex/modify_private_config.toml`, which the task forbids ("any file under home/ other than the three named above and the two rendered templates").

Proposed follow-up, for the orchestrator to decide:
- add a one-time retired-table list (the six names) to the Codex merge script; or
- have the operator delete the six disabled tables from `~/.codex/config.toml` during the live acceptance.

The Claude side needs neither, because `private_mcp.json.tmpl` is a full template that `make update` rewrites.

## 3. Codex bot

| Head | Result |
|---|---|
| `526dd18b` (final) | Review at 13:51:13Z with the single P2 above; no 👍. |

I did not reply to or resolve any thread.

## Revise round 1 (task_rev `sha256:ec678510…1592`): purge of the retired tables

- **Commits:** `f2db43f9` (the fix) and `f805ee3a` (`gh pr update-branch`, main 04bce61b). The final head is `f805ee3a`.
- **`home/dot_codex/modify_private_config.toml`:**
  - Module constants `RETIRED_MCP_SERVERS` (the six names, with a one-line T76 comment), `RETIRED_MCP_TABLES` (`mcp_servers.<name>`) and `DISABLED` (an `enabled = false` assignment line, trailing comment allowed).
  - `merge_config` drops a current-only chunk only when its table name is a retired `mcp_servers.<name>` and its body sets `enabled = false`, which was the last managed state of all six. A re-enabled retired table is kept like any other current-only table.
  - The table name must carry the `mcp_servers.` prefix; my first draft matched a bare `[github]` too, and I fixed it before committing. No new helpers.
- **Test:** `test_retired_disabled_mcp_servers_are_purged_and_enabled_ones_kept`. Five disabled retired tables disappear, a re-enabled `context7` and an unknown `private_server` (disabled) survive, and the output parses as TOML. It fails against `526dd18b`'s merge script, and all 12 merge tests pass.
- **Live-shape check:** merging the new baseline into the `2ad504e3` baseline, which is what a machine holds after applying the parent revision, now leaves no `[mcp_servers.*]` table. Before the fix all six remained.
- **Thread 4177937781:** now `fixed:f2db43f9`. Per the revise note, I posted no reply; the orchestrator replies and resolves it.
- **New Codex P2 4178090831 on `f805ee3a`** ("Preserve customized disabled MCP entries"): proposed `not-applicable`.
  - The purge rule (retired name plus `enabled = false`) is exactly the revise spec.
  - A customized table under a retired name could not survive under the old regime. While the six were managed, every apply emitted the managed chunk and skipped the current chunk of the same name (`merge_config`), so any local edit was overwritten wholesale. A disabled custom table under one of these names could exist only if someone created it after their last apply of the parent revision; being disabled, it has no effect.
  - Matching the prior managed fields would need the rendered old baseline (its `filesystem_dotfiles` args hold `{ .chezmoi.sourceDir }`) for a case the old regime already excluded. I left it to the orchestrator.
- **Codex bot:** review at 14:38:08Z on `f805ee3a` with that single P2; no 👍.
- **Checks:** `make render-check`, `make validate-agent-assets` and `make unit-test` (791 OK) pass on `f805ee3a`. CI, branch and bot state are in the validation file.

## Revise round 2 (task_rev `sha256:500dd7c7…bd92`): child tables and parsed enablement

- **Commit:** `26a882ac`, the final head. `main` had not moved, so no update-branch was needed.
1. **P1, orphaned child tables:** `merge_config` first computes `purged`, the current-only retired parents whose parsed `enabled` is false. It then drops each purged parent and every current-only `mcp_servers.<retired>.*` child. A kept parent keeps its children.
2. **P2, enablement by parsing:**
   - `retired_and_disabled()` reads `tomllib.loads(chunk)["mcp_servers"][name].get("enabled") is False`. A chunk that fails to parse is kept.
   - `tomllib` is imported guardedly: these merge scripts run under any `python3` (no floor is set anywhere), so on Python < 3.11 nothing is purged rather than `chezmoi apply` failing.
   - The `DISABLED` regex and the `re` import are removed.
3. **Tests:** the round-1 case now also covers:
   - a disabled retired `github` with a `[mcp_servers.github.env]` child, which disappears with the child;
   - a re-enabled `context7` whose own body holds the text `enabled = false` inside a multi-line string, which is kept;
   - its `env` child, which is kept;
   - an unknown disabled `private_server`, which is kept.
   - Against the `f805ee3a` script it fails (`github` survives through its orphaned child).
   - A direct check (verbatim in the validation file) shows both findings on `f805ee3a` and neither on the new script.
   - All 12 merge tests pass.
4. **Live shape:** the new baseline merged into the `2ad504e3` baseline still leaves no `[mcp_servers.*]` table.

Checks on `26a882ac`: `make render-check`, `make validate-agent-assets` and `make unit-test` (791 OK). CI and bot state are in the validation file.

**Codex bot on `26a882ac`:** 👍 at 14:59:13Z with no new comment. The orchestrator replies on the round-1 threads.

## CompactionDB

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T76 (operator 2026-10-03): the empty `enabledPlugins` map, the six never-enabled MCP server definitions (context7, filesystem_dotfiles, github, time, sequential_thinking, playwright) and the gwq `[claude]` queue are deleted; MCP servers are added back only when one is enabled for a target agent.'
ebdd360d-0bea-450e-a842-23f0313655aa
[exit 0]
```

[memory:decision] dotfiles-T76 (operator 2026-10-03): the empty `enabledPlugins` map, the six never-enabled MCP server definitions (context7, filesystem_dotfiles, github, time, sequential_thinking, playwright) and the gwq `[claude]` queue are deleted; MCP servers are added back only when one is enabled for a target agent.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T76-ineffective-settings-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T76-ineffective-settings-a01.md`
- learning: `.orchestration/learning/dotfiles-T76-ineffective-settings-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T76-ineffective-settings-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
