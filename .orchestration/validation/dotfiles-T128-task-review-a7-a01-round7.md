---
reviewed_at: 2026-10-11T09:38:24Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
task: dotfiles-T128-task-review-a7-a01
round: 7
previous: .orchestration/validation/dotfiles-T128-task-review-a7-a01-round6.md
files:
  - dotfiles-T128-worker-stop-and-watch-a01@23417dde375545598e7e3516f1448fbd3ef130853ce4a09e0fdcf17b264b1ecf
verdicts:
  dotfiles-T128-worker-stop-and-watch-a01: ready
---

# Task-file review: dotfiles-T128-worker-stop-and-watch-a01, round 7 (the watch sees the heads)

Delta from 60f782e2 (PR 321 at 15ed1553, before A7 was withdrawn from that PR) to 23417dde: A7-2's watch also lists the PR's top-level review comments (pulls/<n>/comments) and, once A3 is on main, names scripts/regime-counters.sh <task id> --pr <n> for the same counts in one line, "so an INV-6 head count crossed by a worker that ignores its PING is seen from the inline P0/P1 threads"; one new token in the Orchestrator Playbook test; "fourteen tokens". Nothing else moved.

The sentence agrees with INV-6 (heads from inline review_comment items, which is what pulls/<n>/comments lists) and with the script's rule; it reads state and leaves completion to the RESULT, as the cadence sentence still says; the stop that follows (PING unread, pushing past an INV-6 count) was already there and now has its evidence source. The new token is in step 7's text, where the section-scoped test reads it; its other occurrence is in the Worker section and does not interfere. All five Orchestrator Playbook tokens and the nine step-15 tokens resolve. Rounds 2 to 6 stay applied.

Verdict ready.
