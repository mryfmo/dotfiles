---
format: 2
task_id: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 — confirm amendment 2 of `dotfiles-T128-project-map-reload-hook-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 (the TASK line's bus time is the dispatch time) by the orchestrator seat. The Codex Bot's single review of PR #353 (head 2c444b08) raised P1 4267187098: an unselected `terminal-browser action` can drive a freshly launched invisible Chrome instead of the pane's browser (upstream issue 60), so the hook could exit 0 without reloading and leave processes behind; the worker's blocked RESULT (05:52:50Z) confirms it from v0.13.4's `cli/src/action.ts` (the tab listing passes `--cdp`, the final `spawnSync` passes only `--session` and the passthrough, the guardrail rejects a user `--cdp`), so no selector fixes `action`. The reliable form the issue names is `--cdp <port>` on every invocation, which only the bundled agent-browser accepts directly. The task file is not on `main`: the pre-amendment copy is the pair-confirmed amendment-1 version 452a3444, kept as `.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pre-amend2.md`; `git diff --no-index <that copy> <the file>` prints `1 file changed, 48 insertions(+), 9 deletions(-)`. Amended file: `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md`, sha256 `<the amended_task_sha256 of the current round's TASK line>`; the pre-amendment copy is on `main` (`not on main; pre-amendment pair-confirmed copy 452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07`).

## What changed (amendment 2)

1. Item 1: after the path test, the hook reads `terminal-browser ls --all --json`, selects the browser whose `tabs[]` holds a `url` ending with `/.project-map/index.html` (keys `browsers[].cdpPort`, `browsers[].key`, `tabs[].id`, `tabs[].url`, `tabs[].active`, pinned in premise 5 from v0.13.4's `ls.ts` and `instances.ts`), and runs the bundled agent-browser (`${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}`) twice with `--cdp <cdpPort> --session project-map-reload`: `tab <id>`, then `eval 'location.reload()'`; every failure path exits 0; `terminal-browser action` is never used.
2. The hook row and the environment-inputs row (three executables: jq, terminal-browser for `ls`, the agent binary; a loopback CDP port; `TERMINAL_BROWSER_AGENT` as the override terminal-browser itself honours).
3. Item 5's test: the `terminal-browser` stub answers `ls --all --json` with a listing in premise 5's shape (one browser with the map tab, one without); the agent stub named by `TERMINAL_BROWSER_AGENT` records argv; the map case asserts the two calls in order with that browser's port and tab id; the no-map-tab listing, a failing `terminal-browser`, a failing agent, no `file_path` and an empty PATH each exit 0 silently.
4. Premise 1 probes the empty `--json` listing instead of the action form; premises 3 to 6 are new (issue 60's text, `action.ts` lines 96/205/287, the `ls.ts`/`instances.ts` keys, the installed agent-browser 0.38.1 and its `--cdp` connection error on a dead port); the out-of-scope list names `terminal-browser action` in any form and a fix of issue 60.
5. A `## Change of 2026-10-14 (amendment 2 …)` section stating 1 to 4. Amendment 1 stands; nothing else changes.

## Stop condition

1. The diff of the task file against its pre-amendment pair-confirmed copy (`.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pre-amend2.md`, a copy kept in the repository for the reviewers, sha256 452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07; the file is not on `main` yet) contains only what the list above says. Premises 3 to 5 need network (curl to GitHub); a seat without it judges them by the pasted text and says so; premise 6 runs the installed binary.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-project-map-reload-hook-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 verdict=confirm|revise amended_task_sha256=<the amended_task_sha256 of the current round's TASK line> validation=<path>`.

## Round 2 (orchestrator, after the round-1 RESULTs of 05:57Z and 05:58Z)

Round 1: your confirm on 1b9a382d; the Codex half's two P1: terminal-browser's `tabs[].id` is its own numeric id space, not an agent-browser tab ref, so `tab <id>` could fail and the argv stub could not show the map tab switched. Applied: the hook addresses the tab by its CDP `targetId` (`tabs[].targetId` in v0.13.4's `instances.ts`, now in premise 5's grep), which agent-browser accepts as a tab ref ("CDP target ids (from tab list --json) are also accepted as tab refs; unlike t<N> ids they stay stable across daemon restarts", its `tab --help`); a tab with a null `targetId` is skipped (exit 0); item 1, the hook row, the test (`tab <that tab's targetId>`) and the Change section say so. Nothing else changed; input checker `OK`, premises OK x7, counts 7 claims and 18 controls unchanged. Same four stop conditions on the new hash.

## Round 3 (orchestrator, after the round-2 RESULTs of 06:01Z)

The seat confirmed round 2 on the task's current hash; the Codex half's two P1 are about this brief, not the task: the comparison copy lived in the orchestrator's scratchpad, unreadable from the Codex sandbox, and the brief's RESULT example carried round 1's literal hash. Fixed: the pre-amendment copy is now `.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pre-amend2.md` (sha256 452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07), and every amended-hash reference in this brief is the current round's TASK-line token. The task file is unchanged since the seat's round-2 confirm, so round 3 asks the Codex half only; the seat's confirm stands.

## Round 4 (orchestrator, after the Codex round 3 of 06:05Z)

Round 3 (Codex only, the task unchanged): one P3, premise 5's claim omitted `targetId` while its command, its output and item 1 rely on that key. The claim now names it (a CDP targetId, string or null, the ref the hook passes to agent-browser). Nothing else changed: counts 7 claims and 18 controls, input checker `OK`. Because the task's hash moved, round 4 asks both halves again on the new hash; the stop conditions are unchanged.

## Round 5 (orchestrator, after the round-4 RESULTs of 06:08Z)

Round 4: your confirm on a291227a; the Codex half's P1 (the `--session project-map-reload` starts an agent-browser host daemon that idles out after its default hour: a host effect without a row) and P2 (the environment-inputs row called the `TERMINAL_BROWSER_AGENT`-selected binary a pinned tool). Applied: a residual row for the daemon (one per session name, started only when a map tab exists, the user's own CDP connection, idles out, visible in `agent-browser session list`), item 1 names it, and the environment-inputs row states the binary's provenance (the user's own override when set, else the pinned path). Counts 7 claims, 19 controls; input checker `OK`. Same four stop conditions on the new hash.

## Round 6 (orchestrator, after the Codex round 5 of 06:11Z)

Round 5's Codex P2: the environment-inputs row still read as if all three executables were installed tools and the agent binary bundled. Rewritten in full: jq (mise) and terminal-browser (the asset manifest) on the user's PATH, and an agent-browser binary whose path is `TERMINAL_BROWSER_AGENT` when the user's environment sets it (an executable of the user's own choosing, the override terminal-browser honours and the tests use) and otherwise the pinned installer's bundled one; the hook row says "the bundled one unless the user's TERMINAL_BROWSER_AGENT overrides it". Counts 7 claims, 19 controls; input checker `OK`. Same four stop conditions on the new hash; your round-5 RESULT on the previous hash is superseded.

## Round 7 (orchestrator, after the seat's round-5 PONG of 06:13Z)

The seat is right: the round-5 and round-6 TASK lines carried texts without the daemon row. The round-5 edit script had failed on its own count assertion before writing, and the dispatch that followed was not gated on it, so round 5 went out on the round-4 hash and round 6 added only the environment-row rewrite (recorded as M-20261014-04). The daemon row and item 1's daemon sentence are now in the file: 19 controls (verified by count before this line was sent), the environment-inputs row as round 6 described, input checker `OK`. Round 7 is the first line whose hash carries everything the Round 5 and Round 6 sections describe; every earlier RESULT or PONG of this review on another hash is superseded. Same four stop conditions.

## Round 8 (orchestrator, after the round-7 RESULTs of 06:17Z)

Round 7: your confirm on 91de52fd; the Codex half's P2: the test did not exercise a failure of the second `eval` call or a missing agent binary. Applied by construction: item 1 now lists the failure paths once, (a) to (j), each ending in exit 0 with empty output, and item 5's test has one case per path plus the two success cases, with (i) and (j) asserting that no agent call follows the failing one. Counts 7 claims, 19 controls (checked in the shell before this line); input checker `OK`. Same four stop conditions on the new hash.
