---
reviewed_at: 2026-10-10T11:00:00Z
reviewer: claude-review-dot-a004
profile: review
session: 26619e82-a3a8-46c0-a37f-8eef8ba593d0
design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md@1e3b9d12b6526a6b56059e09974a1eb9b1f234af80483b4f32e90e95328626e5
task: dotfiles-T124-design-receipt-canonical-a01
round: 4 (canonical re-issue of the round-3 accept of task dotfiles-T126-design-review-a01)
previous: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round3.md (canonical hash 503eea51458b61048ef37272c8a8e9fad9672facc90d52810d159d7503c0bd66 over three keys)
validator: scripts/validate-task.py at origin/feat/task-validator 4f9627ac (PR #313), DESIGN_HASH_KEYS = invariants, threat_model, trust_anchors, implementing_tasks; run from .claude/worktrees/worker-d
---

# Canonical-hash receipt for the accepted T126 design (round 4: implementing_tasks joins the hash)

INV-1: accepted
INV-2: accepted
INV-3: accepted
INV-4: accepted
INV-5: accepted
INV-6: accepted
INV-7: accepted
INV-8: accepted
INV-9: accepted
INV-10: accepted
INV-11: accepted
INV-12: accepted

## Scope of this round

No new review questions, as tasked. This receipt restates the round-3 accept under the validator's four-key hash and confirms that the three keys round 3 hashed are unchanged.

- `implementing_tasks` is the new hashed key; its value is the three-item list `dotfiles-T124-wave3b-audit-grammar-a01`, `dotfiles-T126-w2b-herdr-audit-delegation-a01`, `dotfiles-T126-w3-headless-design-review-a01`, which the validator's own parser reads as that list.
- The round-3 serialization recomputed on the current file (compact JSON, sorted keys, over `invariants`, `threat_model`, `trust_anchors`, parsed with the validator's `parse_front_matter`) gives `503eea51458b61048ef37272c8a8e9fad9672facc90d52810d159d7503c0bd66`, the round-3 value: byte-identical hashed keys, so the round-3 verdicts stand.
- Whole-file sha256 at this review: `e84ae70f5938beed0b3fd045fd9b9c4a32163fb937c91ab2a69517aaf3327128`.

## Validator output (verbatim, before this receipt existed)

```
$ uv run --no-project scripts/validate-task.py ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md --print-design-hash
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md: design_review.receipt: its `design:` does not end in the design's canonical hash 1e3b9d12b6526a6b56059e09974a1eb9b1f234af80483b4f32e90e95328626e5 (re-review the design after any change to its keys)
1e3b9d12b6526a6b56059e09974a1eb9b1f234af80483b4f32e90e95328626e5
rc=1
```

The one failure is the round-3 receipt's three-key hash. `design_review.receipt` still names the round-3 file; the orchestrator points it at this file, after which the hash suffix, reviewer and verdict checks pass.

Design verdict: accept
