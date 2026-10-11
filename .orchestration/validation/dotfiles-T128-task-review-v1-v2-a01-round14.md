---
reviewed_at: 2026-10-10T23:15:37Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 14
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round13.md
files:
  - dotfiles-T128-v0-main-tests-a01@bb61c8103725ab7d (prefix; full hash in the TASK line)
  - dotfiles-T128-v2-audit-schema-and-runner-a01@fed31de7c48362af
verdicts:
  dotfiles-T128-v0-main-tests-a01: "revise: R14-1 tier source before V1 exists"
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 14: Bot findings on boundary head 8be11e65 folded into V0 and V2

Design unchanged at 15daca85; both files carry their invariant byte-identical and point at the round-13 receipt, which is right while the design does not move. The Bot threads were not read from this seat; the edits are judged on their mechanics.

## V0: revise

- Applied: the promotion check detects the decorator with Python's ast under the three alias forms and the inline skipUnless (item 1(c)); test (b4) covers them; (b2) and (b3) are in. The ast walk is stdlib, not a hand-written parser.
- R14-1 (a worker question INV-4 says to name now): item 1(b) fails "when the task.md is design tier", and test (b2) contrasts a design-tier task with a review-tier one, but V0 lands before V1, so neither scripts/lib/high_risk_paths.py nor validate-task.py --print-tier exists when main-tests first runs. Say where V0 takes the tier from: the task.md's optional stamped tier: key (the schema V1 later adds keeps it and requires it to equal the derived tier), with a missing stamp treated as design tier for this rule (fail closed), or state that V0's no-contract failure applies to every task until V1 lands and V1c switches it to --print-tier. One sentence in item 1(b) and the matching fixture in (b2).
- Notes: the inline-skipUnless form can be written other ways (a helper, unittest.skip with a message); the ast check covers the named forms and the design-tier audit covers the rest, which item 1(c) could say in six words. The script's "under 100 lines" with an embedded Python ast snippet is tight; the PR cap is the real bound.

## V2: ready

- Applied: inputs are snapshotted and hashed before the model runs, recomputed from the live files after, and a difference fails the run (item 2), which is stronger than the round-8 overwrite rule; the premises map must carry exactly the keys 1..N from the task file; join, send and leave of pooled runs are serialized by a mkdir lock with a trap.
- Notes: JSON object keys are strings, so the 1..N comparison is over the strings "1".."N"; say so to spare a question. The runner's "under 120 lines" is no longer realistic with snapshot, manifest, lock, premise check, three outputs and the fallback; keep the PR cap as the bound and drop the line figure or raise it.
