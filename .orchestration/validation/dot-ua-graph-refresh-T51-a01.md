# Validation: dot-ua-graph-refresh-T51-a01 (blocked)

### $ sha256sum task file

```text
0d9b7bcb14ded5dc42737f87e8db9bc9262e13ba81b748177d850c3d437b537e  /home/moriya/Workspace/dotfiles/.orchestration/tasks/dot-ua-graph-refresh-T51-a01.md
```

### $ python3 -c "...len(nodes), len(edges)"   # before

```text
$ python3 -c "...len(nodes), len(edges)"   # before
885 1325
exit=0
```

### $ node /home/moriya/.understand-anything-plugin/skills/understand/prepare-incremental.mjs /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c 72b890157078c583f45d71a61ee6eba0df86afb5

```text
$ node /home/moriya/.understand-anything-plugin/skills/understand/prepare-incremental.mjs /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c 72b890157078c583f45d71a61ee6eba0df86afb5
scan-project: filesScanned=364 filteredByIgnore=1877 complexity=large
[json-parser] Failed to parse JSON: Unexpected token '#', "#!/usr/bin"... is not valid JSON
extract-import-map: filesScanned=364 filesWithImports=13 totalEdges=43
Incremental plan: ARCHITECTURE_UPDATE; analyze=28; delete=0; cosmetic=3; ignored=208; generated=3
exit=0
```

### $ node /home/moriya/.understand-anything-plugin/skills/understand/compute-batches.mjs /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c --changed-files=/home/moriya/Workspace/dotfiles/.claude

```text
$ node /home/moriya/.understand-anything-plugin/skills/understand/compute-batches.mjs /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c --changed-files=/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/changed-files.json
Loaded 364 files (218 code).
Info: compute-batches: merged 249 small batches (258 files) into 11 misc batches — singletons and orphans consolidated
Wrote 12 batches (sizes: max=5, min=1) to /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/batches.json
exit=0
```

### $ python /home/moriya/.understand-anything-plugin/skills/understand/merge-batch-graphs.py /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c

```text
$ python /home/moriya/.understand-anything-plugin/skills/understand/merge-batch-graphs.py /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c
Found 14 batch files (13 logical batches, 1 multi-part):
  batch-existing.json: 742 nodes, 1036 edges
  batch-6.json: 2 nodes, 31 edges
  batch-7.json: 1 nodes, 10 edges
  batch-8.json: 2 nodes, 7 edges
  batch-10.json: 4 nodes, 9 edges
  batch-19.json: 1 nodes, 0 edges
  batch-22.json: 3 nodes, 17 edges
  batch-23.json: 8 nodes, 7 edges
  batch-25.json: 1 nodes, 10 edges
  batch-26.json: 51 nodes, 81 edges
  batch-27-part-1.json: 34 nodes, 40 edges
  batch-27-part-2.json: 35 nodes, 41 edges
  batch-29.json: 17 nodes, 31 edges
  batch-30.json: 8 nodes, 16 edges

Input: 909 nodes, 1336 edges

Fixed (3 corrections):
     3 × tested_by edges dropped (orphan endpoint or test↔test / prod↔prod pair)

Tested-by linker:
     0 × tested_by edges produced (path-convention supplement, production → test)
     5 × production nodes tagged "tested"

Output: 909 nodes, 1333 edges

Imports edge recovery:
  Recovered 43 `imports` edges from importMap (364 entries scanned)

Written to /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c/.ua/intermediate/assembled-graph.json (821 KB)
Incremental symbol validation:
  "Makefile": nodes 1 -> 1; symbols 0 -> 0
  "README.md": nodes 1 -> 1; symbols 0 -> 0
  "home/.chezmoitemplates/claude-settings-managed.json": nodes 1 -> 1; symbols 0 -> 0
  "home/.chezmoitemplates/codex-config-managed.toml": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_agents/agent-config.yaml": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_agents/skills/agmsg-orchestration/SKILL.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_claude/modify_private_settings.json": nodes 8 -> 8; symbols 7 -> 7
    unknown: "function:home/dot_claude/modify_private_settings.json:load_json_object" ("load_json_object") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:is_managed_permission_hook" ("is_managed_permission_hook") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:is_managed_session_start_hook" ("is_managed_session_start_hook") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:merge_managed_entries" ("merge_managed_entries") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:merge_hooks" ("merge_hooks") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:merge_settings" ("merge_settings") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_claude/modify_private_settings.json:main" ("main") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "home/dot_codex/modify_private_audit.config.toml": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_codex/modify_private_security.config.toml": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_config/claude/rules/agmsg-orchestration.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_config/claude/rules/model-selection.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_config/claude/rules/pr-integration.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_config/claude/rules/understand-anything.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_config/codex/AGENTS.md": nodes 1 -> 1; symbols 0 -> 0
  "home/dot_local/bin/common/executable_agmsg-dispatch": nodes 2 -> 2; symbols 1 -> 1
    unknown: "function:home/dot_local/bin/common/executable_agmsg-dispatch:wait_for_read" ("wait_for_read") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "home/dot_local/bin/common/executable_herdr-agents": nodes 35 -> 42; symbols 34 -> 41
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:resolve_worker_profile" ("resolve_worker_profile") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:resolve_worker_kind" ("resolve_worker_kind") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:resolve_worker_worktree" ("resolve_worker_worktree") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:ensure_worker_worktree" ("ensure_worker_worktree") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:ensure_worker_identity" ("ensure_worker_identity") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:ensure_worker_delivery" ("ensure_worker_delivery") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:write_spawn_options" ("write_spawn_options") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:despawn_worker_seat" ("despawn_worker_seat") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:repo_worktree_path" ("repo_worktree_path") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:worker_seat_applies" ("worker_seat_applies") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:prepare_worker_seat" ("prepare_worker_seat") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:seat_pane_shell" ("seat_pane_shell") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:agent_name_for_workspace" ("agent_name_for_workspace") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:wait_for_shell_prompt" ("wait_for_shell_prompt") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:split_agent_pane" ("split_agent_pane") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:wait_for_agent_ready" ("wait_for_agent_ready") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:wait_for_agent_name_release" ("wait_for_agent_name_release") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:start_agent_in_pane" ("start_agent_in_pane") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:start_claude_in_pane" ("start_claude_in_pane") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:start_worker_agent" ("start_worker_agent") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:load_seat_labels" ("load_seat_labels") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:normalize_seat_labels" ("normalize_seat_labels") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:find_managed_workspaces" ("find_managed_workspaces") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:single_managed_workspace" ("single_managed_workspace") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:live_worker_pane_id" ("live_worker_pane_id") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:restart_worker_in_pane" ("restart_worker_in_pane") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:panes_on_pane_tab" ("panes_on_pane_tab") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:attach_panes_are_unambiguous" ("attach_panes_are_unambiguous") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:repair_attach_pane_order" ("repair_attach_pane_order") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:repair_attach_pane_ratio" ("repair_attach_pane_ratio") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:require_distinct_worker_identity" ("require_distinct_worker_identity") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:bootstrap_agmsg" ("bootstrap_agmsg") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:remove_shadowing_node_global" ("remove_shadowing_node_global") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
    unknown: "function:home/dot_local/bin/common/executable_herdr-agents:audit_pane_id" ("audit_pane_id") — Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed
  "home/dot_local/bin/common/executable_ua-symbol-coverage": nodes 0 -> 7; symbols 0 -> 6
  "scripts/check-agent-runtime.py": nodes 18 -> 20; symbols 17 -> 19
  "scripts/check-regime-boundary.sh": nodes 0 -> 1; symbols 0 -> 0
  "scripts/require-crit-review.py": nodes 12 -> 14; symbols 11 -> 13
  "scripts/validate-agent-assets.py": nodes 34 -> 35; symbols 33 -> 34
  "tests/unit/test_check_agent_runtime.py": nodes 2 -> 2; symbols 1 -> 1
  "tests/unit/test_generate_agent_configs.py": nodes 4 -> 4; symbols 3 -> 3
  "tests/unit/test_herdr_agents.py": nodes 2 -> 2; symbols 1 -> 1
  "tests/unit/test_pr_feedback.py": nodes 6 -> 6; symbols 5 -> 5
  "tests/unit/test_require_crit_review.py": nodes 3 -> 3; symbols 2 -> 2
  "tests/unit/test_ua_symbol_coverage.py": nodes 0 -> 4; symbols 0 -> 3
  "tests/unit/test_validate_agent_assets.py": nodes 4 -> 4; symbols 3 -> 3
Symbol validation blocked publication; baseline not advanced
exit=1
```

### $ python3 (summary of .ua/intermediate/incremental-symbol-report.json + presence of old IDs in assembled-graph.json)

```text
$ python3 (summary of .ua/intermediate/incremental-symbol-report.json + presence of old IDs in assembled-graph.json)
ok: False | unresolvedFiles: ['home/dot_claude/modify_private_settings.json', 'home/dot_local/bin/common/executable_agmsg-dispatch', 'home/dot_local/bin/common/executable_herdr-agents'] | errors: []
home/dot_claude/modify_private_settings.json: beforeSymbols=7 afterSymbols=7 missing=7 oldIdsPresentInCandidate=7/7 statuses=[('unknown', 'Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed')]
  missing ids: load_json_object, is_managed_permission_hook, is_managed_session_start_hook, merge_managed_entries, merge_hooks, merge_settings, main
home/dot_local/bin/common/executable_agmsg-dispatch: beforeSymbols=1 afterSymbols=1 missing=1 oldIdsPresentInCandidate=1/1 statuses=[('unknown', 'Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed')]
  missing ids: wait_for_read
home/dot_local/bin/common/executable_herdr-agents: beforeSymbols=34 afterSymbols=41 missing=34 oldIdsPresentInCandidate=34/34 statuses=[('unknown', 'Old symbol cannot be mapped uniquely, or source parsing is unavailable/failed')]
  missing ids: resolve_worker_profile, resolve_worker_kind, resolve_worker_worktree, ensure_worker_worktree, ensure_worker_identity, ensure_worker_delivery, write_spawn_options, despawn_worker_seat, repo_worktree_path, worker_seat_applies, prepare_worker_seat, seat_pane_shell, agent_name_for_workspace, wait_for_shell_prompt, split_agent_pane, wait_for_agent_ready, wait_for_agent_name_release, start_agent_in_pane, start_claude_in_pane, start_worker_agent, load_seat_labels, normalize_seat_labels, find_managed_workspaces, single_managed_workspace, live_worker_pane_id, restart_worker_in_pane, panes_on_pane_tab, attach_panes_are_unambiguous, repair_attach_pane_order, repair_attach_pane_ratio, require_distinct_worker_identity, bootstrap_agmsg, remove_shadowing_node_global, audit_pane_id
```

### $ git status --short .ua

```text
exit=0
```

### $ make validate-agent-assets  # main checkout

```text
uv run --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/acceptance/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/autoskill/runs/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/learning/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/reports/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/sandboxes/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/tasks/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-5952ab8.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-5952ab8.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-e334af5.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-audit-e334af5.md.last.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-crit-comments.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-codex-worktree-git-writable-T50-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles: .orchestration/validation/dot-ua-graph-refresh-T51-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/autoskill/runs/dot-pr-gate-trust-boundary-T40-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/learning/dot-pr-gate-trust-boundary-T40-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/reports/dot-pr-gate-trust-boundary-T40-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/sandboxes/dot-pr-gate-trust-boundary-T40-a01.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-receipt.md
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01-review.json
WARN: regime-boundary: untracked .orchestration file in /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec: .orchestration/validation/dot-pr-gate-trust-boundary-T40-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-sec (herdr-agents --remove-worker)
agent asset validation ok
exit=0
```
