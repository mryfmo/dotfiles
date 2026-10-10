---
reviewed_at: 2026-10-10T10:50:00Z
reviewer: claude-review-dot-a004
profile: review
session: 26619e82-a3a8-46c0-a37f-8eef8ba593d0
design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md@503eea51458b61048ef37272c8a8e9fad9672facc90d52810d159d7503c0bd66
design_hash_kind: canonical sha256 of invariants, threat_model and trust_anchors (scripts/validate-task.py at PR #313 head 2d2ae688); whole-file sha256 c7acfe2b24d7f4bc396b60ea9ed7b5db4d4b759c0bf95df2d3dd6c75c33735c7
task: dotfiles-T126-design-review-a01
round: 3
previous: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round2.md
---

# Design review round 3: T126 regime v2 (v3 of the document)

Scope as tasked: the validator at the current `feat/task-validator` head on the file as written at 10:42:31Z, each round-2 item confirmed as applied, and a diff of v3 against v2 to confirm nothing else changed.

## Validator output (verbatim, worker-d worktree at 2d2ae688, before this receipt existed)

```
$ uv run --no-project scripts/validate-task.py ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md --print-design-hash
~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T126-regime-v2-a01.md: design_review.receipt: '.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round3.md' is not a file inside the main checkout ~/Workspace/dotfiles
503eea51458b61048ef37272c8a8e9fad9672facc90d52810d159d7503c0bd66
rc=1
```

The one failure is this receipt not yet existing; the id failure of round 2 is gone (`V1`–`V12` occur nowhere in the file; `INV-1`–`INV-12` occur 45 times), the tier derives as `design`, `security: true`, and the canonical hash is the value in this receipt's `design:` line. With this file in place at the named path, the validator's three receipt checks (hash suffix, one `-aNNN` non-orchestrator `reviewer:`, one `Design verdict: accept` line) are satisfied by construction; the orchestrator's re-run after this RESULT is the confirmation.

## Diff v3 against v2 (ids and quoting normalised)

Exactly five changes: `design_review.receipt` now names this file; INV-5 gains "the gate refuses not_applicable for any id listed in the task file's invariants, which are applicable by construction"; INV-12's gaming-path list gains "an invariant map with not_applicable for a task invariant"; the Review record gains the round-2 paragraph (ids per design, the docs-tier exemption for the tests-first check in W5, `AGMSG-PONG v1 status=question` entering the contract in W3); ids `V-n` → `INV-n` throughout. No other key or body text changed.

## Invariants

INV-1: accepted. The file now passes the id rule; the remaining validator failure is the receipt's absence, which this file ends. Ids per design is the right reading: an implementing task names one design in `design_review.design`, and the subset check runs against that design's ids, so T124's `INV-1..9` (waves W1, W2) and this file's `INV-1..12` (W3 onward) do not collide.
INV-2: accepted.
INV-3: accepted. The docs-tier exemption is recorded for W5.
INV-4: accepted.
INV-5: accepted. The `not_applicable` clause closes the round-2 dodge.
INV-6: accepted. The `status=question` contract entry is recorded for W3.
INV-7: accepted.
INV-8: accepted.
INV-9: accepted.
INV-10: accepted.
INV-11: accepted.
INV-12: accepted. The new gaming path is named.

## Carried notes (not conditions)

- Round-1 F3 stands as recorded: the (d) redefinition was decided in a document the orchestrator authored while PR #313 was open; the PR #313 acceptance record names it and these receipts.
- The remaining open decision (where the automatic audit runs) is the operator's; the document lists both options' dependencies and a recommendation.
- INV-2 binds the receipt file's sha256 in history from W5 on; this receipt's sha256 is in its RESULT line so the record exists from the first canonical receipt.

Design verdict: accept
