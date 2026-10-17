---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: final
---

The hook uses one physical-path canonicalizer for the event and every eligible file-URL tab: bare home expansion, one-pass URL decoding, physical cwd, symlinks, dot/parent segments and trailing separators. The selected URL is bound to that successful canonical identity check. The reload guard then checks that the pinned tab still has that URL, using its browser-serialized href; it no longer repeats a suffix comparison that rejects trailing separators. jq encodes the selected URL as a JSON string before it enters JavaScript. Existing port/target filters, first match, pinning, right-half split, original open argument and silent exit behavior remain.

PR https://github.com/mryfmo/dotfiles/pull/379, branch fix/project-map-owned-followups; round3 began at8607a87c71cce2cebfaf0a7747e11de0451fc98e under C59 re-plan D-S1-379-A. The first round3 publishing checkpoint ba0bf3548b17ec0ad0837a518e338611066daf63 received P2 4301859324: trailing-slash matching selected the tab but the old suffix guard did not reload it. At07:16:28Z the orchestrator explicitly authorized this guard correction within the same round3, not another round. The pair-confirmed runtime amendment remains byte-identical task SHA256 24521a833348cc3c822c262b3e3c2388d89e70d01b86156c6a28290c456ed3d9: installed PATH-resolved python3 -I -S -c, inline stdlib only, no new production script/package.

Against GitHub base af4f1e997f78119d5994d7d7b1966894d62bbc6a, source40 added+5 deleted=45/200; tests237 added/1000. Only the allowed hook, existing unit module and nine canonical task records change. Rule/SKILL prose has no owned sentence to edit. Seven original focused methods remain AST-identical, including all four original path regressions. The two static command expectations and navigation-guard method now exercise the authorized guard; prior Python fixture provisioning remains.

Owned rows and checks:

- 4277695198: test_project_map_reload_hook_selects_the_event_map_among_two_repositories.
- audit:73f51ab:1: test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open.
- 4300474045: earlier fixed:c0c3ff05f50846d8f880b7ccfb54d0c74630adf4; unchanged test_project_map_reload_hook_matches_percent_encoded_tilde includes literal-percent controls.
- 4300561777 and audit:990b607:1: earlier fixed:02fdf0618be46c9eba11c05cd189846f3e871704; unchanged test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd.
- audit:990b607:3: earlier fixed:02fdf0618be46c9eba11c05cd189846f3e871704 by committed current evidence; this revision commits the updated same nine records.
- audit:8607a87:1 and 4301859324: fixed by the final publishing commit named in RESULT-round3. test_project_map_reload_hook_compares_canonical_paths_for_every_path_form covers nine path forms plus a quoted/U2028 URL query. Each executes the exact emitted JavaScript with Node URL/location fixtures and asserts one reload and no injected global. Before the guard fix, the trailing-slash row reports actual0/expected1; after, all ten rows pass. The named test_project_map_reload_hook_guards_against_a_tab_navigating_away executes the guard for the selected map (reload1), an unsaved form (0) and another repository map (0).
- audit:8607a87:2: fresh/persisted live E2E remains the explicit orchestrator post-merge observation; Node fixtures are not live browser E2E.
- audit:8607a87:3 and earlier count/authorization items: orchestrator-owned acceptance/counter bookkeeping. Worker does not edit acceptance or reply to/resolve threads.

All11 focused project_map_reload methods pass in10.776s. ShellCheck, render-check, Ruff format and scoped whitespace pass. Ruff requested only quote style on two expected-script f-strings; formatting preserves the complete module AST from that passing run. Independent read-only security review approved this incremental hook/test diff againstba0bf354 with no findings; its complete focused transcript is preserved in validation.md. The parent read it and all five resolved review records. The previous canonicalizer/runtime review remains historical support, and its claimed checks are preserved in the labeled appendix.

The current report is bound to these tested source SHA256 values:
- home/dot_claude/hooks/executable_project-map-reload.sh: a3a2dcf0b0c13ce264a6f062309469e72744a2a8a14fc9b925a1b5c87b69154d
- tests/unit/test_generate_agent_configs.py: e4297f6a8e6f6e8c6eeeff83015ab9e64adf2b5914f77940716347c09cd3190b

Task SHA256 24521a833348cc3c822c262b3e3c2388d89e70d01b86156c6a28290c456ed3d9. task.md/report.md/validation.md/sandbox.md/learning.md/autoskill.md/revise.yaml/project-map-worker-crit.json/project-map-worker-review-receipt.md are committed together; worklogs and duplicate raw observer logs are not. This committed phase covers local validation and independent review. The final publishing head, its fresh CI watcher result and Bot re-review are collected after push in RESULT-round3 and round3-guard/ raw logs. Earlier8607a87 CI and ba0bf354 Bot observations are historical, not validation of this corrected head; the ba0 review explicitly had P2 4301859324.

Live fresh/persisted pane behavior remains unverified; the Node harness executes JavaScript with emulated URL/location, not a browser or file load. The guard safely skips a tab whose full href changes after selection, even if its new URL has an equivalent filesystem path; a later write can reselect it. Filesystem/metadata races and unavailable tools remain existing operational limits. No local Bats, real process inventory, browser/pane/daemon, Crit web UI, graph update, re-seat, main write, persistent configuration or memory/AutoSkill promotion. PR383 ps-width correction and then PR375 evidence-only revision are queued. Orchestrator owns final feedback sweep, audit, acceptance, post-merge E2E and merge.
