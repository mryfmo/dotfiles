---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: final
---

The hook selects this event's map using its normalized file URL. For relative paths it now obtains the physical working directory with Bash `pwd -P`, matching Node's resolution when the repository is reached through a symlink. An existing physical map tab is reloaded instead of opening a duplicate pane. The URL-side tilde fix from c0c3ff05 is retained. CDP port/target checks, pinning, navigation guard, split options and silent exit behavior remain covered by the existing cases.

Branch: fix/project-map-owned-followups; PR: https://github.com/mryfmo/dotfiles/pull/379. This revision starts at 990b607fb286155737f5ee9078d2f572f1624837, whose GitHub base is b167fe0a76a2e77d262f9f556c69ba6b9f118bbe. The original dispatch base5fd4fe0 is historical. Against the current PR base the source changes12 added+2 deleted=14/200 lines and tests add143/1000 lines; no new executable or dependency. Only the hook, its existing test module and this task's artifacts change. Neither allowed rule/SKILL prose file has an owned sentence to edit.

Owned rows and regressions:
- 4277695198: test_project_map_reload_hook_selects_the_event_map_among_two_repositories.
- audit:73f51ab:1: test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open.
- 4300474045: fixed:c0c3ff05f50846d8f880b7ccfb54d0c74630adf4; test_project_map_reload_hook_matches_percent_encoded_tilde preserves upper/lower tilde escapes, raw tilde and literal percent filenames.
- 4300561777 and audit:990b607:1: fixed by this revision's publishing commit, identified in RESULT-round2; test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd fails on the previous logical PWD argument (it records an unwanted open) and passes with pwd-P.
- audit:990b607:3: fixed by that same publishing commit: these canonical report/validation records are current and the review JSON/receipt are committed beside them. The prior untracked report-final.md/validation-final.md are historical supplements, no longer the canonical final evidence.
- audit:990b607:2: orchestrator-owned acceptance/count correction C-56 explicitly authorizes this second C-50 revision; the previous advisory/no-second-round statements are superseded. The worker does not edit acceptance records or reply to/resolve threads.

All10 project_map_reload tests pass (6.003s), including both original owned rows, the tilde regression and the physical-cwd regression. ShellCheck, render-check, Ruff format and source/test whitespace checks pass. The test runs real Bash and jq with stub terminal-browser/agent executables; it starts no pane or browser. The initial formatter check requested only wrapping of the new fixture; formatting was applied and the final check passes. An incidental zsh read-only variable error occurred after the expected-red test had written its log; the saved test output shows the actual duplicate-open failure.

This final record is bound to the tested source hashes below and the publishing commit that includes it. All13 CI checks on previous_head990b607 passed; those do not validate the new revision. The new publishing head, its final-head CI watcher result and Bot re-review are collected after push and named in RESULT-round2 with raw logs under round2-physical/. Committing future external observations or the self-referential publishing hash here would create another untested head; this phase boundary is explicit.

Source SHA-256:
- home/dot_claude/hooks/executable_project-map-reload.sh: 35a69558dd93f27e1e416387a5fec7b28134ebb1d21f4018f70893b146d6dd3d
- tests/unit/test_generate_agent_configs.py: 220858e58acf322715a861791d3b269abb7fcb29b86ba232447d70909ab1c299

Task copy SHA-256:3d87e72644ca0b4f11fd24de768a674fd8fbc6af9f54df7bcffb822ae7e3a27d. task.md/report.md/validation.md/sandbox.md/learning.md/autoskill.md/revise.yaml/project-map-worker-crit.json/project-map-worker-review-receipt.md are committed together; plan/todo and raw duplicate logs are not committed.

Crit reports no existing review file and no running daemon. The AGENTS.md fallback uses an independent read-only Codex review of this incremental source/test diff, with its complete transcript in validation.md and resolved approval in project-map-worker-crit.json. The receipt and passing worker review gate are local process evidence; integration feedback sweep, final audit, acceptance, thread dispositions and merge remain with the orchestrator.

Path normalization remains lexical beyond resolving the working-directory prefix; arbitrary symlinked event-file components are not canonicalized. Existing rejected-metadata/racing-write behavior can still open a pane. Live fresh/persisted pane E2E is unverified. No local Bats, real process probes, browser/daemon, Crit server, Plan Mode, graph update, persistent config edit, AutoSkill or memory promotion. The stale graph was queried, then targeted rg used; no graph hook fired. PR375, PR382 and PR383 branches/evidence are preserved. Per-command sandbox-safe HTTPS push and unsigned commit are used without escalation.

cost: n/a
