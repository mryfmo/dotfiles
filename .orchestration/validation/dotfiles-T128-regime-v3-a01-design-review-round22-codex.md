reviewed_at: (headless run 11:47Z; receipt saved by the orchestrator)
reviewed_at: 2026-10-12T11:49:21Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@ed51f1d465dd3ed1a71bd5cf3c38ada99dfde89bed43fe479a7da6f77fcc3770  
round: 22  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round21-codex.md

INV-6: accepted

## Findings

None.

PyYAML confirms that v20 differs from reconstructed v18 only at `invariants.INV-6`; `threat_model`, `trust_anchors`, every other invariant, `implementing_tasks`, and `premises` are unchanged. The reconstruction independently matches v18 SHA-256 `7f007ec41c9b0dedded66c964ba8e858d1d604e40b10a0ab278966f7eb2a2ae6`. Against `HEAD`, the changed hashed keys exactly match the stated set.

The proposed clause occurs once, byte-equal to the round-20 proposal, at `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:57`. INV-4 is restored to v18. The clause truthfully states both refusals specified by `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:62-64`, and both are enforceable in `scripts/require-crit-review.py`, INV-6’s mandatory merge backstop.

Skipped: implementation and tests were not run; this was a read-only design review, and no receipt file was written.

Design verdict: accept