# RESULT report: dotfiles-T128-project-map-reload-hook-a01

Implementation commit: `576528758297631ae85ec5ea1e2163594bdc82a0`
Base: `28eec93c9a78e6a56d1f5f60ded675f521edb96f`
Branch: `feat/project-map-reload-hook`

[memory:decision] Claude PostToolUse now runs project-map-reload after the existing formatter for Write/Edit/MultiEdit. The new eleven-line Bash hook reads file_path via jq, requests one terminal-browser action only for /.project-map/index.html, guards the active page's pathname, and silently exits 0 when tools or the browser are unavailable.

## Files

- `home/dot_claude/hooks/executable_project-map-reload.sh`: new executable hook with English shdoc annotations; no event data enters JavaScript or shell execution.
- `home/dot_agents/agent-config.yaml`: one claude.hooks key; no Codex configuration changed.
- `scripts/generate-agent-configs.py`: optional hook rendered after formatter; absent key preserves previous output.
- `home/.chezmoitemplates/claude-settings-managed.json`: regenerated through the renderer.
- `tests/unit/test_generate_agent_configs.py`: two new behavioral tests and existing PostToolUse assertions updated.
- Item 7, `home/dot_agents/skills/project-map/SKILL.md`: the requested Write/Edit-only sentence; its Claude symlink mirror requires no edit.
- `home/dot_config/claude/rules/project-map.md`: the requested automatic-reload sentence.
- Item 8, `scripts/check-agent-runtime.py`: existing check_executable_hook pattern registers deployed-hook parity for doctor.

## Validation and review

The two required tests are `test_project_map_reload_hook_renders_into_post_tool_use` and `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails`. The latter covers Write, Edit, MultiEdit, unrelated paths, missing file_path, browser failure and empty PATH, with exact argv and silent exit assertions. Tests were written first and failed before implementation. All 76 generator tests and 52 runtime tests then passed; render-check, ShellCheck, Ruff formatting and Prettier formatting passed. All outputs are in validation.md.

Source cap: 34 added-plus-deleted lines outside tests/ and .orchestration/, including regenerated settings; limit 200. Test cap: 82 added lines; limit 1000. Amendment 1 confirms the evidence exclusion; task_copy SHA256 is 452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07.

Crit status pointed to a missing review file and comments export confirmed it was unavailable. Independent read-only reviewer /root/hook_review approved the eight source/test paths; its resolved JSON and receipt are saved beside this report. AGENT_REVIEWED=1 with the receipt passed make require-crit-review. No browser Crit session or publication was used.

## Limitations and acceptance work

The real Claude subagent hook dispatch and terminal-browser refresh latency were not exercised in this sandbox. The task assigns the post-merge make update and live project-map-agent verification to the orchestrator/operator. Browser launching, browser selection changes, home installation, local bats runs, dependency additions and merging were skipped.

Project CompactionDB memory add was not executed because the main-checkout state database is outside this worker's writable roots. No memory ID is claimed. Consolidate the two learning.md decisions at acceptance.

Plan Mode was not used; no Crit review server was started. Understand-Anything's graph is stale, so scoped rg was used; no graph update was performed.

cost: n/a
