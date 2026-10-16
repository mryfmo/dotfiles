# RESULT report: dotfiles-T128-settings-hook-dedupe-a01 amendment 1

Status: published PR https://github.com/mryfmo/dotfiles/pull/369 . The earlier network-blocked publication state is historical and superseded.
Branch: fix/managed-post-tool-use-dedupe
GitHub base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Revise previous_head: bdefcbe402ecda1cd7376c2796ac8cc48777b38e
Task-copy SHA256: 99fb3dc7f244c31f58eb9f24f0b0fd9b58c8a5eac71f91027af8a47ee3771225
Exact final revision head and remote CI/Bot outcomes are recorded in amend1/report.md and amend1/validation.md supplied with RESULT; this committed report describes the implementation, not a self-referential commit hash.

[memory:decision] PostToolUse joins MANAGED_HOOK_PREDICATES and reuses managed-entry replacement to remove stale formatter-only entries. Recognition now checks the command program only: after shlex.split, the first token, or the second after python3/python/bash/sh, must have a basename in MANAGED_POST_TOOL_USE_SCRIPTS. An argument naming a managed script never makes a user wrapper managed. Dict/string, malformed quoting and empty/interpreter-only command guards preserve unmanaged hooks. Shared merge_managed_entries/merge_hooks and SessionStart any-token recognition remain unchanged.

Only home/dot_claude/modify_private_settings.json and tests/unit/test_claude_settings_merge.py change outside task evidence. Source14 added lines of200 changed, tests42 added lines of1000. One new method, test_managed_post_tool_use_replaces_stale_format_only_entry, keeps the original cases and adds the wrapper case, all four recognized interpreters and empty/interpreter-only preservation. The wrapper case failed on auditedbdefcbe4 before the predicate correction; all20 tests pass after it, the nineteen pre-existing tests unchanged. render-check, native test formatting and source/test whitespace checks pass. Review/evidence and final publication results accompany RESULT.

The PR was published from80f59cd6, then advanced by the orchestrator's base-merge tobdefcbe4; all bdefcbe4 checks were green on entry to this revise round. The audit's P2 argument-matching specification flaw is corrected by this revision; its P3 stale publication report is corrected by this committed report. The orchestrator owns the separate INV-6 count finding/disposition D-S2-369. Neither initial network-blocked records nor earlier any-token limitations describe the amended predicate/current publication state.

Limits: recognition remains basename-based for the program; unrelated same-named programs still classify as managed. Only the four specified interpreters in the immediate first position are recognized; env launchers and interpreter options are outside the task. No command from settings is executed by the predicate. Tests execute only the modifier on temporary managed/current settings. Installed settings, renderer/template, manifest, PermissionRequest, SessionStart, hook executables, dependency and policy files unchanged. No installed apply/restart, local bats, Plan Mode, browser Crit, graph update or merge. Main-checkout CompactionDB consolidation is orchestrator-owned. After integration, apply dotfiles and restart Claude Code.

cost: n/a
