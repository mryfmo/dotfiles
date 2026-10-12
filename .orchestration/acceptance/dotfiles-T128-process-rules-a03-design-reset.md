---
format: 2
reset_of: dotfiles-T128-process-rules-a03
redesign_task: dotfiles-T128-process-rules-a04
design_sha256: 6ef9ae9572ecd90876ed7b706c4d2d739b082d39adec4b531ccef0789e410fa6
redesign_source: dotfiles-T128-process-rules-redesign-a03
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 on PR 318 under a03: Codex Bot P1 on two heads after the a03 RESULT b9a9da7d (386f97ff: 4243516879, fixed in 114d5b91; 781e6ef8: 4243537279 and 4243537281), the latter two being contradictions between the orchestrator's rule sentences and the hashed design (the design-review freeze rule against INV-7; the boundary-PR sentence against INV-2)"
---

# Design reset: dotfiles-T128-process-rules-a03 (PR #318), 2026-10-11

- **What stops:** task id a03's specification. The branch, PR #318, the worker and the content continue under `dotfiles-T128-process-rules-a04` (a03 plus the two sentence corrections and their tokens; the revise round's three fixes kept).
- **Why a reset:** the two P1s are specification errors of the orchestrator's (two A1 sentences contradicting INV-7 and INV-2), the third reset of this PR for the same cause class (the orchestrator writing rule text without checking it against the hashed design); INV-6's count leaves no further round.
- **Redesign:** `dotfiles-T128-process-rules-redesign-a03` on the review seat produces the whole a04 file; the orchestrator writes it byte-identical from the receipt and the review seat confirms its hash (`verdict=accept design_sha256=<hash>` under this record's `redesign_source`), the anchor the boundary probe reads.
- **Counts carried:** a03 at the reset: tasks 1, amendments 0, questions 1 (PONG 567), results 1, revises 1 (ACCEPTANCE at 22:2xZ), Bot P0/P1 heads after the RESULT 2.
- **Waiver:** none.
- **Anchor:** redesign RESULT 570 (`claude-review-dot-a001`, 22:40:07Z, receipt `457aa876…`, `a04_expected_sha256=842deee2…`, matched on disk); the review seat's `verdict=accept design_sha256=842deee2…` under task id `dotfiles-T128-process-rules-redesign-a03` is the anchor (RESULT 574 at 22:41:42Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a03 round=2 status=ready_for_review verdict=accept design_sha256=842deee29dab4594ba077b56fc5d7769936617fcaa50fb2b4ebc947361626950 receipt=none`).

## Amendment 1 of a04 (22:50Z): the third P1 of the same Bot round

Bot review 5485324335 on `781e6ef8` carried three P1 threads, not two: 4243537278 (SKILL.md:72 counts P0/P1 Bot review bodies toward INV-6; the hashed INV-6, design line 55, counts Bot heads from `original_commit_id` on `review_comment` items only, and plan 006 A7's task says the same) beside 4243537279 and 4243537281. PONG 567 listed two; the redesign task named those two; the a04 file (`842deee2…`) and its anchor RESULT 574 covered those two. The orchestrator added item 8 (the two sentence replacements and their test tokens) to a04 as amendment 1; the file is now `6ef9ae9572ecd90876ed7b706c4d2d739b082d39adec4b531ccef0789e410fa6`, the hash above, and the review seat re-anchored it under `dotfiles-T128-process-rules-redesign-a03` round 3, RESULT 577 at 22:51:47Z (`AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a03 round=3 status=ready_for_review verdict=accept design_sha256=6ef9ae9572ecd90876ed7b706c4d2d739b082d39adec4b531ccef0789e410fa6 receipt=none`), before the amendment TASK went to the worker at 22:56Z; RESULT 574 (`842deee2…`) is the superseded anchor. a04 counters after this: amendments=1 (threshold 2).

Root cause of the omission: the orchestrator built the redesign task's thread list from PONG 567 (the worker's two ids) instead of listing the Bot's comments on `781e6ef8` from GitHub (`gh api --paginate repos/mryfmo/dotfiles/pulls/318/comments`, filter `original_commit_id`), against the run-not-recall rule; what caught it, five minutes after the a04 dispatch, was that GitHub listing, which is plan 006 A7's orchestrator-watch step at an action boundary. Finding class of 4243537278, 4243537279 and 4243537281: one class, "a SKILL sentence restates a hashed invariant and drifts from it" (INV-6, INV-7, INV-2); a04 carries it as S1 count 1 on the a04 artifact (the a03 artifact's count ended with the reset).
