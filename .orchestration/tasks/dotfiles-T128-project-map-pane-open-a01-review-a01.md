---
format: 2
task_id: dotfiles-T128-project-map-pane-open-a01-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-project-map-pane-open-a01-review-a01 — confirm the task text `dotfiles-T128-project-map-pane-open-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-14 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md` (untracked; its sha256 is the `pane_task_sha256` of the TASK line), a step-7 short-form task for the operator's direction of 14:1xZ: the map pane opens itself at the first map write (the merged hook of PR #353, 6a2473f3, only reloads an existing tab and exits 0 silently when none shows the map). It edits the hook in one branch, adds one test beside the two hook tests, and one sentence each in the rule and the SKILL. Sources: the merged hook (`git show origin/main:home/dot_claude/hooks/executable_project-map-reload.sh`), the lineage task `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md` (amendment 2: the rows this file keeps verbatim, the daemon row among them), `terminal-browser open --help`, plan 020 step 4, the hook follow-up `dotfiles-T128-project-map-reload-hook-followup-a01` (shares the files; runs after this task). One round, fixed stop condition.

## Stop condition

1. Nothing contradicts the merged hook's behaviour (the new branch is the only change, at the point where the hook exits because no selection was made; a listing that fails to parse still exits 0 without opening) or step 7's form (one mechanism, one test, two one-sentence prose edits, no renderer or manifest change); the two premises hold (re-run the commands and compare).
2. `allowed_files` covers every touch point the items name and nothing else; nothing is in flight on these files (the hook follow-up is dispatched only after this task merges and boundary (15)): confirm by listing the in-flight tasks.
3. The closed row's test name appears verbatim in item 2 and its four cases close the row's risk (exactly one open call with the event's path and the fixed split arguments when no browser shows the map; no open when the map tab exists; exit 0 and empty output when the open fails; the empty browsers list opens); the environment-inputs row states what terminal-browser open touches (the pane of the Claude session that wrote the map) and that the event's path is the only variable argument; the Completion clause matches plan 020 step 4.
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-project-map-pane-open-a01.md: OK`), the brief check (premises OK, mask clean, 15 controls, 2 claims) and `validate-agent-assets.py --mask-secrets` changes nothing in it; the caps hold by construction.

## Output

`.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-review-a01.md`: the usual header with both sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-project-map-pane-open-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-pane-open-a01-review-a01 round=1 verdict=confirm|revise pane_task_sha256=<sha> validation=<path>`.

## Round 2 (amendment 1 of the reviewed task; plan 022 P0.5)

Round 1 (the review seat, 2026-10-14T14:22:07Z, `.orchestration/validation/dotfiles-T128-project-map-pane-open-a01-review-a01.md`) returned `revise` with four findings; the Codex half did not run (the session ended). The orchestrator applied all four on 2026-10-14T23:2xZ; round 2 reviews the amended file (its sha256 is the TASK line's `pane_task_sha256`) under the same four stop conditions, and this section states what changed:

1. Finding 1 (P1, item 2 and the test row): the merged test `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails` is no longer said to stay as it is; its nine empty-selection cases now expect the one `open … --split right --size 0.5 --no-merge` call in `browser_calls`, and the listed-tab cases keep `["ls --all --json"]`; the threat row for the test module says the same.
2. Finding 2 (P2, item 1 and row 17): item 1 states that the empty selection includes a map tab the jq filter rejects, that the branch then opens a second pane, that this task accepts that consequence, and that the stricter filter stays the hook follow-up's `target-id-validation` row.
3. Finding 3 (P3, items 1 and 3, row 38): `--no-merge` is passed (the installed `terminal-browser open --help` documents it; premise 2 now counts it: `3`), and item 3 says the pane is its own, never a tab merged into a neighbouring terminal-browser.
4. Finding 4 (P3, item 1): item 1 states that `terminal-browser open` returns when the browser is ready, so a second hook run in the same second finds the tab, and that otherwise the second open is accepted the same way as the filter case.

Nothing else in the file changed. The Codex half runs on this round for the first time, with the same brief and the amended file.
