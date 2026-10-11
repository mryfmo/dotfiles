---
reviewed_at: 2026-10-11T08:06:08Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
task: dotfiles-T128-task-review-a7-a01
round: 2
previous: .orchestration/validation/dotfiles-T128-task-review-a7-a01.md
files:
  - dotfiles-T128-worker-stop-and-watch-a01@ed9d316e970f1a272100a6b2bb6c22cb8f9f49633f3b3edffff2f7450f49b7f1
verdicts:
  dotfiles-T128-worker-stop-and-watch-a01: "revise: 1 the S1 release must be plan 006's S1 steps, not a disposition or a row; 2 heads=, classes= and threads= after note= are new PONG fields"
---

# Task-file review: dotfiles-T128-worker-stop-and-watch-a01, round 2 (the two sentences changed after the Bot's P1s on PR 321)

Delta judged from the boundary branch (73387b9a at e63b4ac7 to ed9d316e at d779df17): A7-1's count source and release sentences, two new tokens in A7-3 and "ten tokens" in Validation; nothing else moved.

1. Count source: accepted. "Every top-level Codex Bot review comment of the PR ... and the PR's commits ... original_commit_id of chatgpt-codex-connector[bot] comments whose title carries a P0 or P1 badge, in the PR's commit order, after its first RESULT's head" is INV-6's source (review_comment items by original_commit_id) and the rule scripts/regime-counters.sh states in its header on PR 319's head (distinct original_commit_id of Codex Bot review comments with a P0 or P1 badge, counted for commits after the first RESULT's head). The S1 class rule is A3's. All ten tokens are present in their sections.
2. INV-6 release: accepted. "A reset record naming a redesign by another context or the operator's waiver, never a disposition" is INV-6's sentence.
3. R2-1 (revise): the S1 release contradicts plan 006. A7-1 says "after an S1 stop the orchestrator's ACCEPTANCE decides (a reset, a disposition or a threat-table row)". Plan 006's S1 rule says: stop the artifact, switch the orchestrator to xhigh, re-examine the plan phase that produced it, record the cause under .orchestration/learning/, and "resume only with a changed task or a changed plan step. Never a fourth round of the same thing." A disposition or a threat-table row of the third same-class finding is the fourth round the rule forbids. Replace the parenthesis with: the orchestrator's ACCEPTANCE releases it only after plan 006's S1 steps (the xhigh re-examination and the learning record) with a changed task (amendment or reset) or a changed plan step, never a disposition of the finding.
4. R2-2 (revise): the PONG line "status=blocked note=S1|INV-6 heads=<n> classes=<class:count,...> threads=<ids>" claims "no new field", but heads=, classes= and threads= follow note= as fields of their own (the contract's note=<short-note>; every note in this team's history is one token). Either fold them into the note (note=S1|INV-6;heads=<n>;classes=<class:count,...>;threads=<ids>) or add the three fields to the Liveness line in the same PR, and keep the claim true either way. The pinned token "status=blocked note=S1|INV-6" survives both.

Verdict revise with R2-1 and R2-2; neither touches a hashed sentence, the premises or allowed_files.
