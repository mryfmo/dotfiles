---
reviewed_at: 2026-10-11T09:12:51Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
task: dotfiles-T128-task-review-a7-a01
round: 4
previous: .orchestration/validation/dotfiles-T128-task-review-a7-a01-round3.md
files:
  - dotfiles-T128-worker-stop-and-watch-a01@838684ddb069441bef1ae3885f12806a180f52e729fef8f2a431e89d067e109a
verdicts:
  dotfiles-T128-worker-stop-and-watch-a01: "revise: 1 review-body findings cannot enter the INV-6 head count the gate does not share"
---

# Task-file review: dotfiles-T128-worker-stop-and-watch-a01, round 4 (review bodies)

Delta from 75533709 (PR 321 at 4ce664fc) to 838684dd: A7-1 also lists every Codex Bot review body with a P0 or P1 badge (pulls/<n>/reviews, attributed to the review's commit_id, "counted like an inline finding"), one new token, "thirteen tokens". Nothing else moved.

R4-1 (revise). INV-6's hashed sentence counts "Codex Bot P0 or P1 on two heads after the first RESULT, from original_commit_id on review_comment items recorded by pr-feedback.py", and scripts/regime-counters.sh on PR 319's head counts exactly that (its header: the distinct original_commit_id of Codex Bot review comments with a P0 or P1 badge). A review body is not a review_comment item and has no original_commit_id. With this clause the worker's INV-6 head count is a superset of the gate's: a worker reaches heads=2 on one inline head plus one review-body head, sends status=blocked note=INV-6, and A7-1 then allows no release but a reset record or the operator's waiver, while the merge gate would not refuse that PR at all. That is an INV-6 stop INV-6 never asked for, released only by a reset. Fix, either form: (a) review-body P0/P1 findings count toward the A2 fix cap and the S1 title classes (the title line is the body's first line) but not toward INV-6's heads, which stay the script's rule, and the token becomes "counted toward the fix cap and the classes, never INV-6's heads"; or (b) INV-6's sentence gains review bodies first (a hashed change, a round-20 pair, and the script follows), and only then does A7 count them as heads. The Bot's P2 is answered by (a) today.

Verdict revise with R4-1; round 2 and round 3 items stay applied.
