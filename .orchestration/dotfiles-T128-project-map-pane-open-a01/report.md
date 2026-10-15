# RESULT report: dotfiles-T128-project-map-pane-open-a01

Branch: feat/project-map-pane-open
Base: 727180dbc33f50b8934c2f2ed229d1c6a744ce0d (after e3006da7)
Task-copy SHA256: a2c1196e1f0ba873543683f49e89f2d27629d92c2edb3e076e099efc5d81842f

[memory:decision] When the map Write/Edit event has a cleanly parsed listing but no selected map tab, the hook now calls terminal-browser open with the quoted event path, --split right --size0.5 --no-merge, then exits0 regardless of open success. Existing reload calls, manifest, renderer, managed settings and runtime checker are unchanged. Parsing/listing failures still exit without opening.

## Files and tests

The four source/test files are home/dot_claude/hooks/executable_project-map-reload.sh (one branch plus shdoc description), tests/unit/test_generate_agent_configs.py (new test and nine empty-selection expectations), home/dot_config/claude/rules/project-map.md (one sentence) and home/dot_agents/skills/project-map/SKILL.md (one sentence; Claude mirror follows its source).

The new test is test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map. It was written first and failed on the old hook. It verifies exact argv including a spaced path, open failure with discarded stdout/stderr, existing-map reload without open, empty browsers and malformed JSON without open. All three focused project_map_reload tests pass. ShellCheck, render-check, Ruff/Prettier formatting and source diff-check pass; outputs are in validation.md. Source change cap:14 added-plus-deleted lines outside tests/ and .orchestration/ (limit200). Test additions:104 (limit1000).

Crit data was absent; the independent read-only review found no new issues in the four scoped paths and its resolved JSON plus receipt are saved beside this report. No browser Crit session or Plan Mode was used.

## Limits and effects

This change makes the first map write open a separate right pane using half the width when no map is selected. A rejected map port/target or racing writes may open a duplicate pane; the task explicitly accepts this and the shdoc shortcut comment records it. Existing tab-fallback and target-id concerns remain owned by dotfiles-T128-project-map-reload-hook-followup-a01 and are outside this task. No new advisory finding is claimed at local review.

Tests use stubs; live pane placement, real Claude hook dispatch and browser startup timing were not checked. No real browser was launched, home installed state changed, dependency added, local bats run or PR merged by this worker. CompactionDB consolidation is left to the orchestrator because its main-checkout state database is outside writable roots; no memory ID is claimed. The existing knowledge graph is stale; no update was performed.

cost: n/a
