---
format: 2
task_id: dotfiles-T124-design-receipt-canonical-a01
kind: review
security: false
invariants:
  INV-3: for a security task the gate requires in agmsg history an AGMSG-RESULT receipt= from a non-orchestrator identity preceding the implementing AGMSG-TASK, whose design hash equals the canonical sha256 of the named design task's invariants, threat_model and trust_anchors keys, with the implementing task's invariant ids a subset of the design's and every id accepted
---

# AGMSG-TASK dotfiles-T124-design-receipt-canonical-a01 — the canonical-hash receipt for the accepted T124 design

Drafted 2026-10-10 by the orchestrator seat. Read-only review task on the `review` profile. The T124 design (`.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md`) was accepted in design review round 3 (`…-design-review-round3.md`, reviewer `claude-review-dot-a002`), which hashed the whole file. The validator from T124 wave 1 (PR #313, branch `feat/task-validator`) computes the canonical hash over the front-matter keys `invariants`, `threat_model`, `trust_anchors`, and from now on receipts must carry that hash. You are a different `-review-` identity: confirm that the design you hash is the one round 3 accepted, then write the receipt.

## Steps

1. In `.claude/worktrees/worker-d`: `git fetch origin feat/task-validator` and `git switch -c receipt/canonical --no-track origin/feat/task-validator` (do not modify any tracked file; no PR).
2. Read the design file in the main checkout (`~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md`) and the round-3 receipt. Confirm the prose body is the v3 the round-3 review accepted plus the two sections added afterwards ("Round-3 notes adopted", "v4 addition" on the redesign seat, which the addendum `…-design-review-addendum-redesign-seat.md` records as operator direction) and that the front matter's `invariants` INV-1 to INV-9 restate the body's invariants faithfully (one line each; say if any line narrows or widens the body).
3. Run, from the worktree: `uv run --no-project scripts/validate-task.py ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md --print-design-hash` and paste the output; also run the validator on the design file without the flag and paste its result (a failure about the receipt itself is expected before you write it; anything else is a finding).
4. Write `.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-canonical.md` in the main checkout (through the permission gate, the allowed artifact path): front matter `reviewed_at`, `reviewer: <your identity>`, `profile: review`, `session`, `design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md@<canonical hash>`, `supersedes: …-design-review-round3.md (whole-file hash)`, then `INV-1: accepted` … `INV-9: accepted` (or `rejected: <reason>` if step 2 found a discrepancy), the step-2 confirmation, the step-3 output, and `Design verdict: accept` (or `revise`).
5. `AGMSG-RESULT v1 task_id=dotfiles-T124-design-receipt-canonical-a01 status=ready_for_review verdict=<accept|revise> receipt=<path> design_hash=<canonical hash>` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=6.

Forbidden: editing any tracked file; a PR; anything outside the sandbox except writing the receipt and the dispatch (the `git fetch` of a public branch is in-sandbox).
