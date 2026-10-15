---
reviewed_at: 2026-10-14T05:22Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-project-map-reload-hook-review-a01
round: 3
task_file: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-review-a01.md@007ecd2a0ac3038c6f690d066ac80b0b7e2fb79596a408ff4812b432a5d6c1a2
hook_task: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md@cc6ac23f3e87015f139dc4037963671cfdad188913be10193192759b876b2a67 (untracked; previous_hook_task_sha256 607ec1fb, this seat's round-2 copy; round-1 hash 2918dfcd, both superseded)
previous_receipt: dd727042ef0e5d7ed083e9373772dc4525e56f349c034ab331cbd86debee3a32 (round 2, revise on 607ec1fb with one P2 and two P3, all answered here; superseded by this file at the same path)
sources: the round-1 and round-2 sources; terminal-browser v0.13.4's `action --help` ("With no selectors it targets the browser in this terminal tab and that browser's active tab") and `ls --help` ("Lists the browsers running in this terminal tab")
consistency_check: "dotfiles-T128-project-map-reload-hook-a01.md: OK (checker fdab23e0 on a copy named by the task id, run from the main checkout)"
premises: three, byte-identical to round 1, where each replayed EQUAL (premise 1 from the user's environment outside the sandbox); the round-2 premise 4 is removed
verdict: confirm
---

# Task-file review: dotfiles-T128-project-map-reload-hook-a01 (the project-map pane reloads through a PostToolUse hook), round 3

Both hashes of the 05:21:39Z TASK line recomputed and equal; the previous hash equals this seat's round-2 copy. The diff against that copy is exactly the brief's Round 3: row one describes the single selector-less command and its guard (line 21), premise 4 is gone (the former lines 75 to 84), item 1 runs exactly one command, `terminal-browser action -- eval 'location.pathname.endsWith("/.project-map/index.html") && location.reload()'`, with every failure mode ending in exit 0 (line 91), item 5's test names that single call, the Edit case and the three failure modes with empty stdout and stderr (line 95), out of scope names a browser in another terminal tab and says where the operator's split lives (line 102). Nothing else differs. The round-2 P2 (the test contradicted item 1) and both P3 (a caller-dependent premise; undocumented tab fields) are answered by removing the listing: the test now names the one call item 1 makes, and no premise or filter depends on a tab shape. No finding remains.

## Stop conditions, round 3

1. Nothing contradicts the renderer, the rendered settings, the routing rule or plan 021 step 7. Premises 1 to 3 are the round-1 text (EQUAL then). The design's premise is terminal-browser's own help text, pasted in round 2's derivation 2 and the brief's Round 3: a selector-less action targets the browser in the caller's terminal tab and its active tab; the hook's process is the orchestrator's Claude session, whose tab is the one the operator split the map pane from (round-2 derivation 1 showed `self` as the caller's own tab and pane), so the call reaches that pane by construction and the eval's guard leaves any other page alone.
2. Touch points unchanged since round 2: nine entries covering items 1 to 8 and the evidence directory; disjoint from T704's and the gate wrapper task's files.
3. The two closed rows name `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails` and `test_project_map_reload_hook_renders_into_post_tool_use`, each once in the table and once in item 5; the first now closes row one as written (one call with the script, the Edit case, nothing on other paths, exit 0 with empty output on no `file_path`, a failing stub with stderr text, and an empty PATH), the second the renderer's risk. The hook's threat is stated right (two names and their provenance; no browser, several browsers, a non-map active tab and a failing action all swallowed). The Completion matches plan 020 rows 1, 2 and 4.
4. Checker OK on cc6ac23f (header). Count words agree: "exactly one command", "two test names", "under 40 lines", "items 7 and 8", "three" failure modes; the only times are bus times. Caps by construction.

## Findings

None. Approval: the mechanism now rests on a documented property of the one tool it calls, the test item describes the call item 1 makes, every added behaviour has its row, and the premises are reproducible from any seat.

## Derivations

1. A map opened as a file URL has `location.pathname` equal to the file path, so the guard's suffix test holds for the operator's `terminal-browser open ~/Workspace/dotfiles/.project-map/index.html`.
2. A browser in the orchestrator's tab whose active tab is not the map is left alone by design (the brief says so); the map in a background tab is therefore not reloaded until it is active. Out of scope as the task now states, not a finding.

Task-file verdict: dotfiles-T128-project-map-reload-hook-a01: confirm
