# Acceptance: dotfiles-T128-process-rules-a03 (second reset continuation of PR #318; plan 006 Phase A: A1, A2, A4)

- **Decision:** superseded at 22:42Z by a04 (INV-6 reset: Bot P1 on two heads after the a03 RESULT `b9a9da7d`; record `dotfiles-T128-process-rules-a03-design-reset.md`); the PR continues under a04 and, after plan 006 S1 at 23:08Z, a05.
- pr=318
- **Worker:** `claude-standard-dot-a003`, `.claude/worktrees/worker-f`, branch `docs/regime-pattern`. a03 TASK 472 at 06:54:59Z (task file `867ea4ca…`, written by the review seat as the reset redesign of a02, anchored by RESULT 476), read 06:58:52Z; RESULT at 07:27:23Z on `b9a9da7d`: commits `798fa098` (Codex-seat push clause), `f4d45983` (a03 task.md), `c4300f47` (evidence), `7524e001` (Bot fix round 1: `gh pr ready` only while a draft), `b9a9da7d` (evidence); carried over from a02: items 1 to 5, the revise round's five checks (`108b43bd`, `052eea4c`), the three Bot P2s (`21c160c8`), the a02 amendment-1 copy (`e8d20aae`). CI 14 of 14, watcher joined. `bot_rounds=2`, one fix round; the final head drew no review (👍 07:19:56Z).
- **Threads (replied and resolved by the orchestrator at 07:29Z, 1 kept open):** 4240566259 `fixed:f4d45983` (the a03 four-row threat table), 4240566263/66/68 `fixed:21c160c8`, 4240598179 `fixed:798fa098`, 4240646079 `fixed:7524e001`, 4240646082 `not-applicable` (a `closed` selector's existence is checked on the PR tree by V1's schema and by the task-file reviewer until then; the shape class the reset closed), 4240598178 `not-applicable` (ordering: PR #320 merges first, then this PR updates its base; the thread stays open until that has happened).
- **Orchestrator review:** `…-a03-crit.json` and `…-a03-review-receipt.md` at `b9a9da7d`: approved subject to the merge order.
- **Counters by hand (07:28Z, `history.sh --limit 1000` to a file, 494 rows):** a03: tasks=1 amendments=0 questions=0 results=1 revises=0; Bot P0/P1 heads after a03's first RESULT head `b9a9da7d`: 0. (a02 closed with tasks 2, amendments 1, questions 3, results 1; its revise ACCEPTANCEs 451 and 457 count as one round.) No threshold; no S1 class under a03.
- **Three metrics for PR #318 so far (a01 + a02 + a03):** revision rounds 2 (a01 revise 1; a02 revise 1), resets 2, Bot rounds 3 + 3 + 2, one redesign RESULT per reset plus two anchor confirmations; wall TASK 419 at 04:16Z to the a03 RESULT at 07:27Z = 3 h 11 min (merge pending); cost `n/a` from the worker; seats: one standard worker, the review seat for 8 RESULTs, one Codex headless pair round, two audits so far.
- **Exemption declared:** acceptance and evidence-sync bookkeeping; agmsg control plane.

<!-- audit-input-boundary -->

## After the merges of #320 and #319 (21:45Z to 22:06Z)

- Thread 4240598178 (the in-job decision sentence) resolved at 21:45Z: PR #320 merged at 21:44Z, so the sentence is true on the merged tree. `gh pr update-branch` twice: `6e47afa7` (onto `0e522059`) and `b7ae2d54` (onto `52575497`, after A3 merged); the final head's diff from `main` outside `.orchestration` is byte-identical to the PR's own diff. CI on `b7ae2d54` in progress at 22:06Z.
- **Counters by the merged script (A1 item 5, the literal form, 22:04Z):**

  ```
  $ scripts/regime-counters.sh dotfiles-T128-process-rules-a03 --pr 318
  task=dotfiles-T128-process-rules-a03 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=b9a9da7d406fd6f210537c63369b8257dd1f954f bot_p1_heads_after_result=0 audits=unknown wall=2026-10-11T06:54:59Z..2026-10-11T07:27:23Z (0:32) source=live
  (a01: results=2 revises=1 bot_p1_heads_after_result=6; a02: tasks=2 amendments=1 questions=3 results=1 bot_p1_heads_after_result=2: both reset and anchored)
  $ scripts/check-regime-boundary.sh --report   (INV-6 lines on main 52575497)
  regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
  regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
  regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
  regime-boundary: dotfiles-T128-v0-main-tests-a01 S2: bot_p1_heads 6 >= 2 source=live
  ```

  No threshold under a03; the four lines are the true states the plan names.
- Orchestrator review at `b7ae2d54`: `…-a03-crit.json` record a03-review-2; receipt at the final head.

## Final audit of `b7ae2d54` (headless, `…-process-rules-a03-audit-b7ae2d5.md`, verdict `incorrect`, four findings) and revise round 1

- Finding 1 (P2, SKILL threat-table bullet: the by-hand task-file review cannot verify that a `closed:` selector's test exists before implementation): real; the bullet now says the selector names a test present in the PR tree at acceptance and in the schema's validation of the PR, and the task-file review checks the selector's form only. Revise round 1, check `test_closed_selector_existence_is_checked_at_acceptance`.
- Finding 2 (P2, step 15's `@codex review` trigger matches any `Bot`, so a CodeRabbit review ends the wait without a Codex review; the same point as Bot thread 4243369347 on `6e47afa7`): real; the listings select `.user.login == "chatgpt-codex-connector[bot]"`. Revise round 1, check `test_the_bot_wait_filters_the_codex_bot`.
- Finding 3 (P2, four sentences unpinned: the S1/S2 decision sentence and the three shape rules): real; tokens added. Revise round 1, check `test_shape_rules_and_the_decision_sentence_are_pinned`.
- Finding 4 (P2, the sweep JSON the audit received had 90 empty dispositions): the orchestrator's fill aborted on the new thread 4243369347 (unhandled id) and left the file unwritten; the sweep is re-run and filled on the revised head before the next audit, with the new thread dispositioned `fixed:<revise sha>`.
- INV-1, INV-2 and INV-6 hold per the auditor (review-tier routing, the three task-copy hashes, design `4520b8f0…` on `main`, the caps: 3 files, 19 non-test and 202 test additions; a03 has no reached threshold). INV-12 marked violated for finding 3 (rule removals undetected) until the tokens land.
- Revise ACCEPTANCE sent 22:2xZ (`previous_head=b7ae2d54`, three `check=` selectors). a03 counters after this round: results 2, revises 1, one below INV-6's threshold; the next head gets the sweep, the audit and the gate.

## Close of a03 (22:36Z to 22:42Z): INV-6 reached during revise round 1

- The revise commit `386f97ff` drew Bot P1 4243516879 (+ P2 4243516880), fixed in `114d5b91`; the next head `781e6ef8` drew P1 4243537279 (the design-review freeze rule froze an unreviewed hash, against INV-7) and P1 4243537281 (a boundary PR "never a prerequisite of a dispatch", against INV-2; plan 006 had corrected the rule at 07:25Z, the SKILL sentence had not). Two Bot P1 heads after the a03 RESULT `b9a9da7d`: INV-6's threshold. PONG 567 (`status=question`, a03 questions=1) asked fix round 2, reset or disposition; the rule's path is a reset (`…-a03-design-reset.md`): the two findings are the orchestrator's specification errors, the third reset of this PR for the same cause class.
- Successor a04 (`842deee2…`, written by the review seat as `dotfiles-T128-process-rules-redesign-a03`, RESULT 570): a03 plus items 6 and 7 (the two sentences and their tokens; the old boundary token asserted absent); dispatched to `claude-standard-dot-a003` at 22:42Z from head `781e6ef8`. a03 closed `status=superseded`.
