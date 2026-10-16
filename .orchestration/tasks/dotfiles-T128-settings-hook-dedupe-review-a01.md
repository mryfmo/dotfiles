---
format: 2
task_id: dotfiles-T128-settings-hook-dedupe-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-settings-hook-dedupe-review-a01 — confirm the task text `dotfiles-T128-settings-hook-dedupe-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-15 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md` (untracked; its sha256 is the `dedupe_task_sha256` of the TASK line), plan 022 T15: the Claude settings modify script keeps a stale PostToolUse entry beside the managed one because `MANAGED_HOOK_PREDICATES` has no PostToolUse predicate; the task adds the predicate in the shape of the SessionStart one and a test. One round, fixed stop condition; round 2 (2026-10-15 05:20Z) after the review seat's P1 and P2 of round 1 (the set is a constant, case one holds both entries), the Codex half having confirmed round 1.

## Stop condition

1. Item 1 describes the one change correctly against `home/dot_claude/modify_private_settings.json` on `origin/main`: the predicate shape equals `is_managed_session_start_hook`'s, the basename set is a module constant beside `MANAGED_SESSION_START_SCRIPTS` in its shape, `MANAGED_HOOK_PREDICATES` gains the one key, `merge_managed_entries` and `merge_hooks` are unchanged, and the three failure modes (all-managed entry replaced, mixed entry keeps the unmanaged hook in place, no key gets the managed entry) follow from `merge_managed_entries` as written.
2. Item 2's test name appears verbatim in the closed row; its cases (case one holds both entries of the operator's file, case one b the stale entry alone) distinguish the additive branch from the replacing one (case one fails on `origin/main`, where the output would hold two entries) and would fail if a user hook were dropped (case two).
3. The threat table has one row per `allowed_files` entry, the settings-file row as the non-path control, the generic rows verbatim from `.orchestration/templates/task-short.md`, and the new-scripts row saying no new script; no sentence states an unlanded mechanism as present; the Completion clause is plan 020 step 4's (the Bot's single review, one fix round, a surviving P0/P1 to the operator, P2 advisory under the named owner, then `make update` and a restart); the cap sentence reads outside `tests/` and outside `.orchestration/`; `allowed_files` is pairwise-disjoint from every in-flight task (the chain-review follow-up's `scripts/orchestrator/*` and the task-checkers follow-up's checkers and tests name neither of these two files).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-settings-hook-dedupe-a01.md: OK`), the mask check (`masked 0 match(es)`), and its three premises replay from this checkout (`origin/main` fetched): `0`, `1`, `19`.

## Output

`.orchestration/validation/dotfiles-T128-settings-hook-dedupe-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-settings-hook-dedupe-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-settings-hook-dedupe-review-a01 round=1 verdict=confirm|revise dedupe_task_sha256=<sha> validation=<path>`.

Amendment 1 (2026-10-16T01:17:15Z, after dispatch): item 1 recognises a managed hook by the command's program only and item 2 adds the wrapper case, after the audit of PR #369's head bdefcbe4; this review judges the amended items against the managed template's PostToolUse commands and the module on origin/main.

Amendment 2 (2026-10-16T03:21:35Z, after dispatch): item 1 recognises only the exact managed invocation (one part, or an interpreter and one part) and item 2 adds the chained-command case, after the Bot's P1 on PR #369's head 5bcab1f9; this review judges the amended items against the managed template's PostToolUse commands and the module on origin/main.

Amendment 3 (2026-10-16T03:44:09Z, after dispatch): the predicate matches the managed hook path (a plain token ending in `/.claude/hooks/<basename>`) instead of the basename, after the Bot's P1 4290664196 and the worker's residual P1 on head 72d0e66d; item 2 adds cases six to eight; this review judges the amended items against the managed template's PostToolUse commands and the module on origin/main.

Amendment 4 (2026-10-16T04:05:59Z, after dispatch): the predicate compares the token for equality with the two renderings of the managed path for this home (tilde form, absolute form) instead of a path pattern, after the Bot's P1 4290805581 on head e5d0141b; item 2 adds case nine; this review judges the amended items against the managed template's PostToolUse commands and the module on origin/main.

Amendment 5 (2026-10-16T04:18:29Z, after dispatch): item 1 drops the interpreter clause (one `shlex` part equal to a rendering of the managed path; the template never rendered an interpreter form), after the worker's peer finding on amendment 4; item 2 adds case ten.
