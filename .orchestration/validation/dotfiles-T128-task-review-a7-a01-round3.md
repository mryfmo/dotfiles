---
reviewed_at: 2026-10-11T09:02:00Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
task: dotfiles-T128-task-review-a7-a01
round: 3
previous: .orchestration/validation/dotfiles-T128-task-review-a7-a01-round2.md
files:
  - dotfiles-T128-worker-stop-and-watch-a01@755337091075c5ed4b42c14748e7bda87064db4293d1ba338a6b4493dbb8b882
verdicts:
  dotfiles-T128-worker-stop-and-watch-a01: ready
---

# Task-file review: dotfiles-T128-worker-stop-and-watch-a01, round 3 (the task-span clause)

Delta from a779eded (PR 321 at 959ac29d) to 75533709: A7-1 keeps only the comments whose original_commit_id is at or after the task's first commit on the PR (the task.md copy), one new token in A7-3 ("at or after the task's first commit on the PR", present in the clause) and "twelve tokens" in Validation (8 + 4). Nothing else moved; round 2's two items stay applied.

The clause agrees with INV-6 and with scripts/regime-counters.sh: both count heads after the task_id's own first RESULT, which is later than the task's first commit, so for heads the filter changes nothing and a successor inherits none of its predecessor's. For S1 classes it narrows plan 006's artifact from the PR to the task's span of the PR; that is consistent with S1 itself, whose prescribed response is the changed task, so the count restarts with it. Note, not an item: plan 006's S1 line still names "one artifact (design, task file, PR)"; a half-sentence there ("per task on a PR that continues across a reset") would make the plan and the SKILL read the same.

Verdict ready.
