---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: pre_push_checkpoint
---

The hook now compares file URLs to the normalized event path before deciding whether to reload an existing map or open its pane. A map in another repository no longer suppresses opening this event's map or receives its reload. Existing CDP port and target-ID checks, pinning, navigation-away guard, split size, no-merge flag and silent exit behavior are preserved. Only the hook and its existing unit module change; neither allowed prose file has an owned sentence to change.

Owned rows and their tests:
- 4277695198: test_project_map_reload_hook_selects_the_event_map_among_two_repositories. Two distinct map URLs in separate browsers select the correct CDP port and target, including spaces, lexical dot/parent components, Unicode and percent/hash/question/apostrophe filenames.
- audit:73f51ab:1: test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open. An unrelated map with a similar repository prefix causes the event map to open and no agent call.

Both tests failed against the base hook before implementation. All 8 project_map_reload tests, ShellCheck, render-check, Ruff format and source/test whitespace checks pass. Optional Ruff lint reports the same 11 pre-existing findings as origin/main, with no new finding. Optional shfmt requests changes to pre-existing redirection spacing; CI's shfmt scope excludes this hook. Those unrelated style edits are not included.

Branch: fix/project-map-owned-followups. Base: 5fd4fe0c32846f8e5ecbbbd027cb67f0a5be0398. Source changed lines: 11 added + 2 deleted = 13 <= 200. Test additions: 93 <= 1000. Byte-identical task.md SHA-256: 3d87e72644ca0b4f11fd24de768a674fd8fbc6af9f54df7bcffb822ae7e3a27d. The five evidence records and task copy are committed; plan/todo and command logs stay uncommitted. Final commit identifiers, PR, CI and exact-head Bot evidence will be added to report-final.md and validation-final.md after the final push and named in RESULT, preserving a clean tracked tree.

The initial review gate required evidence. Crit status reports no existing review data and no daemon. A separate read-only Codex review found no issues; its resolved JSON approval and receipt are saved as project-map-worker-crit.json and project-map-worker-review-receipt.md. The native worker review gate passes using that receipt; orchestrator integration review, feedback sweep, task-level audit, dispositions and merge remain orchestrator work. No thread is replied to or resolved by this worker.

Tests use stub terminal-browser and agent executables and start no browser/daemon. Live pane fresh/persisted E2E has not been checked by this worker. Path normalization is lexical; symlink identity is not resolved. The existing metadata/racing-write limitation is unchanged. No new executable, dependency, interpreter or settings change.

The old PR375 branch and its untracked evidence remain intact. The graph is stale; targeted rg was used without updating it. No graph-update hook fired, no Plan Mode or Crit server was started. GitHub investigation uses gh first, including the original finding in PR359; no web fallback. AutoSkill and durable memory promotion are not used.

cost: n/a
