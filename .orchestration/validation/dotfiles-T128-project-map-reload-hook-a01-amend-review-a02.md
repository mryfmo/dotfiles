---
reviewed_at: 2026-10-14T06:22Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02
round: 8
task_file: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02.md@6bc144e68b559c122e2225177e41911d1df885ed127c1ec998d68ba040392e56
amended_task: .orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md@a7c4d65b4ce3a79f54f08a8dec80e65586c6fbe3e53e4196f4aa8dde3d085530 (untracked; previous_amended_task_sha256 452a3444, the amendment-1 text; round 7 (91de52fd) and the earlier rounds superseded)
previous_receipt: 25381709af5c74496ae9da794d8829b433b5abdc77c66bcac9c4d0929dd3475a (round 7, confirm on 91de52fd with three P3; superseded by this file at the same path)
diff_base: .orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-pre-amend2.md (452a3444) for the whole amendment, and this seat's round-7 copy (91de52fd) for what round 8 changed
consistency_check: "dotfiles-T128-project-map-reload-hook-a01.md: OK (checker fdab23e0 on a copy named by the task id, run from the main checkout)"
counts: 7 claims, 19 controls, 2 closed, as the brief states
amend_sweep: "no leftover of: exactly one command / under 40 lines / exactly two names / action exit / several browsers / non-map active tab / action -- eval / tab <id> / every other path; one hit for tabs[].id at line 127 (P3, since round 2)"
premises: seven, byte-identical to round 4 (each replayed EQUAL in rounds 1, 2 or 4)
verdict: confirm
---

# Amendment review: dotfiles-T128-project-map-reload-hook-a01 (the project-map reload hook), amendment 2, round 8

Both hashes of the 06:21:41Z TASK line recomputed and equal. Against the round-7 text the diff is two hunks: item 1's failure paths listed once, (a) to (j), each ending in exit 0 with empty stdout and stderr (line 127), and item 5's test with two success cases and one case per path, (i) and (j) asserting that no agent call follows the failing one (line 131). Nothing else differs. The Codex half's round-7 P2 (no case for a failing second `eval` or a missing agent binary) is answered by (h) and (j).

## Stop conditions, round 8

1. The two hunks are the brief's Round 8 and nothing more.
2. Unchanged from round 7: every behaviour and host effect has its row; the hook row's "exits 0 on every path, no browser, no map tab and a failing command included" is now spelled out by item 1's list, and the closing test exercises each path.
3. Both closed rows' tests appear once in the table and once in item 5. The ten paths cover the hook's branches in order (event, path, jq, terminal-browser, listing empty, no map tab, null targetId, agent binary, first call, second call); the stub "can be told to fail on a given call" is what (i) and (j) need.
4. Checker OK on a7c4d65b; sweep as before (one hit, P3). No `reset_of`; the task-copy row and the evidence directory are unchanged. Counts 7 claims, 19 controls; "(a) to (j)" is ten paths and item 5 says one case each plus two success cases; the only times are bus times.

## Findings

- P3 (high) `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md:127`, :131 — path (d) folds two branches into one letter, "`terminal-browser` missing, or `ls` failing", and item 5 gives one case per letter, so one of the two goes untested (round 7's text had both: a stub exiting 1 and an empty PATH). Split (d), or say the case covers both (an absent binary and a stub exiting 1 with stderr text).
- P3 (high) `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md:106` — from round 7: premise 6's probe starts a `probe` session daemon on every replay; `--idle-timeout 1s` on the probe, or one clause in the claim.
- P3 (high) `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md:127` — from round 2: the superseded key `tabs[].id` survives in item 1's negative clause.
- P3 (high) `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01-amend-review-a02.md:10` — the brief's last sentence still says the pre-amendment copy "is on `main`" and then quotes "not on main; …" (brief only).

Approval of the task text: as in round 7, with the failure paths enumerated once and tested one by one.

Amendment verdict: dotfiles-T128-project-map-reload-hook-a01: confirm
