---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: final
---


The hook now compares physical absolute paths using one shared canonicalizer for the event and every structurally eligible file-URL tab. It expands a bare home prefix, decodes URL escapes once, resolves relative paths from physical cwd, resolves symlinks and dot/parent segments, and removes trailing separators. The nine-form table selects the existing map tab and issues the original pinned eval without opening another pane. All prior port/target validation, first-match order, split options, fixed navigation guard and silent exit behavior remain in place.

This C59 re-plan D-S1-379-A revision starts at8607a87c71cce2cebfaf0a7747e11de0451fc98e on fix/project-map-owned-followups, PR https://github.com/mryfmo/dotfiles/pull/379; current GitHub base af4f1e997f78119d5994d7d7b1966894d62bbc6a. The approved amendment adds installed PATH-resolved python3 invoked with -I -S, inline stdlib only, no new production script or package. Isolated mode excludes cwd and Python environment injection; the executable retains the existing PATH trust model. The byte-identical amended task SHA256 is 24521a833348cc3c822c262b3e3c2388d89e70d01b86156c6a28290c456ed3d9; the TASK line/hash verification is preserved in validation.md.

Against that GitHub base: hook37 added+4 deleted=41/200 source lines; tests200 added/1000. Only the allowed hook, existing unit module and this task directory change. Neither allowed rule/SKILL prose file has an owned sentence to edit. Eight prior focused test methods are AST-identical; the other two only provision the installed Python executable in PATH fixtures. All ten prior methods retain their assertions.

Owned rows and named regression checks:

- 4277695198: test_project_map_reload_hook_selects_the_event_map_among_two_repositories.
- audit:73f51ab:1: test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open.
- 4300474045: earlier fixed:c0c3ff05f50846d8f880b7ccfb54d0c74630adf4; test_project_map_reload_hook_matches_percent_encoded_tilde remains unchanged and covers literal-percent filenames. The common canonicalizer supersedes the per-form workaround.
- 4300561777 and audit:990b607:1: earlier fixed:02fdf0618be46c9eba11c05cd189846f3e871704; test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd remains unchanged. The common canonicalizer preserves that behavior.
- audit:990b607:3: the prior revision committed the canonical evidence; this revision updates and commits the same nine records.
- audit:8607a87:1: fixed by this revision's publishing commit, named in RESULT-round3; test_project_map_reload_hook_compares_canonical_paths_for_every_path_form has nine subcases: bare home, percent-encoded tab URL, percent-encoded event URL, symlinked cwd, dot/parent segments, each side's trailing slash and each side's symlink path. Seven failed before the fix; all nine now pass.
- audit:8607a87:2: fresh/persisted live E2E is an explicit orchestrator post-merge observation under the accepted re-plan, not a worker-completed check.
- audit:8607a87:3 and earlier count/authorization findings: orchestrator-owned acceptance/counter bookkeeping; the worker neither edits acceptance nor replies to or resolves threads.

All11 focused project_map_reload methods pass (10.279s). ShellCheck, render-check, Ruff format and scoped whitespace checks pass. Independent security review reran the named table and ten additional temporary fixture checks: isolated imports, authority rejection/local authority, invalid encoding/NUL skipping, first match, single decoding and query/fragment identity. No implementation or amended-task consistency findings. The parent read the complete transcript and all four resolved JSON records; validation.md preserves the full review and exact command outputs. The initial auxiliary AST check and reviewer environment fixture needed harness corrections, both documented without product changes.

This committed record is bound to the tested source hashes below. All13 CI checks on previous_head8607a87 passed, which is historical context only. The publishing head, its final-head CI watcher exit/result and Bot re-review are collected after push in RESULT-round3 and raw round3-canonical/ logs. Future external observations and the self-referential publishing hash are not claimed here; this avoids a new untested evidence-only head.

Source SHA256:
- home/dot_claude/hooks/executable_project-map-reload.sh: e5b1ac6aa0f3f595acb00ac63d7c5c75990fb9b5064bc303a15f606a3ed0d0ed
- tests/unit/test_generate_agent_configs.py: ad99c9ea57342d7c202ac6112529e08790d2e920f377b5ad3f986257af5374cf

The canonical task.md/report.md/validation.md/sandbox.md/learning.md/autoskill.md/revise.yaml/project-map-worker-crit.json/project-map-worker-review-receipt.md are committed together. Worklogs and duplicate raw logs are not committed. Crit has no review file/daemon; the explicit AGENTS.md independent read-only fallback and receipt provide local process evidence, not reviewer authentication or the final integration audit.

Live browser behavior remains unverified: the table proves canonical selection/pinned eval issuance/no extra open, and does not execute JavaScript or prove a browser can display an HTML URL with a trailing slash. The original navigation guard is unchanged. Rejected metadata, filesystem races or an inaccessible interpreter can still prevent reload or lead to an open attempt. No local Bats, real process inventory, pane/browser/daemon, Crit web UI, graph update, main write, re-seat, persistent config edit or memory/AutoSkill promotion. PR375/382/383 states are preserved; PR383 ps-width revision is queued after this handoff. Orchestrator owns final feedback sweep, audit, acceptance, post-merge E2E and merge.
