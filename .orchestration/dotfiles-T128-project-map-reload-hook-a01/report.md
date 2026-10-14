# RESULT report: dotfiles-T128-project-map-reload-hook-a01, amendment 2

PR: https://github.com/mryfmo/dotfiles/pull/353
Branch: feat/project-map-reload-hook
Base: 28eec93c9a78e6a56d1f5f60ded675f521edb96f
Task-copy SHA256: a7c4d65b4ce3a79f54f08a8dec80e65586c6fbe3e53e4196f4aa8dde3d085530

[memory:decision] The hook discovers the map browser through terminal-browser ls --all --json, validates its loopback port and CDP target token, and passes --cdp and the fixed project-map-reload session on both direct agent-browser calls: tab <targetId>, then eval location.reload(). It does not call the affected terminal-browser action wrapper. TERMINAL_BROWSER_AGENT is the existing upstream override used as the test seam; the default is the installed bundled binary.

## Files

The eight source/test paths are home/dot_claude/hooks/executable_project-map-reload.sh (new27-line executable with English shdoc annotations), home/dot_agents/agent-config.yaml (one Claude hook key), scripts/generate-agent-configs.py (optional hook after formatter), home/.chezmoitemplates/claude-settings-managed.json (generated), tests/unit/test_generate_agent_configs.py (two named tests and updated assertions), home/dot_config/claude/rules/project-map.md (automatic reload sentence), item7 home/dot_agents/skills/project-map/SKILL.md (Write/Edit-only sentence; no Claude mirror edit), and item8 scripts/check-agent-runtime.py (deployed executable parity).

## Tests and caps

The required tests are test_project_map_reload_hook_renders_into_post_tool_use and test_project_map_reload_hook_acts_only_on_the_map_and_never_fails. Revised tests first failed against the old action call, then all76 generator tests passed. The hook test covers Write, Edit and MultiEdit success, exact stable-target argv, each failure (a)-(j), invalid ports and an option-like target. The tab failure permits one agent call only; the eval failure permits two, with no extra calls. Missing tools, browsers, map tabs and target ids remain silent exit0. ShellCheck, render-check, Ruff formatting and source diff-check pass. The52 runtime tests passed before amendment2; that runtime checker block is unchanged. Full outputs are in validation.md.

The current source cap is50 changed lines outside tests/ and .orchestration/ including generated settings (limit200); test additions are160 (limit1000). CI on the original head2c444b08 passed every check. CI on the fix head is checked after push; the final local report and validation capture those observations without moving the pushed head.

## Findings

P1 Bot comment4267187098, threadPRRT_kwDOSMyAV86sLZvx: fixed by this one fix round. The final RESULT and local final report identify the actual fix commit. The direct calls carry CDP on every invocation and select the map by CDP targetId, closing the root cause documented in upstream issue60 and pinned v0.13.4 action.ts.

P2 (independent review, high confidence), hook line26: if the selected map tab closes between tab selection and eval, agent-browser can fall back to another tab and reload it, potentially discarding unsaved input. The bundled tab --help lines16-22 are pasted in validation.md. It is NOT fixed here. Orchestrator PING2026-10-14T06:38:37Z expressly directs no amendment3, the exact amendment2 argv, no code change for this advisory, and ownership by dotfiles-T128-project-map-reload-hook-followup-a01. That follow-up task is to be written and landed by the next boundary before integration, per this task's P2 clause. No not-applicable claim is made for P2; acceptance and integration decisions remain with the orchestrator.

Crit data remains absent. Independent review and the acknowledged P2 disposition are saved in worker-crit.json and the worker receipt. The local resolved record for P2 records workflow disposition only, not that the code risk is fixed. No browser Crit server was started; Plan Mode was not used.

## Remaining checks and effects

Live Claude subagent dispatch and real browser reload latency are untested here and remain for the post-install check named by the task. The production hook may start or reuse one host daemon for the fixed project-map-reload session; its default idle timeout is one hour, per the amended threat table. Tests use a stub and start no daemon. Browser launching, dependency changes, home installation, local bats and merging were not performed. Project CompactionDB consolidation remains with the orchestrator because the main state database is outside this sandbox's writable roots. No memory ID is claimed.

cost: n/a
