---
reviewed_at: 2026-10-12T11:49:16Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@ed51f1d465dd3ed1a71bd5cf3c38ada99dfde89bed43fe479a7da6f77fcc3770
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 22
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to v18's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 22 (v20: the round-20 INV-6 clause, in INV-6)

Delta judged against 7f007ec4 (round 20's input) two ways. Reconstruction: removing from v20 the clause "; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)" and the v19 and v20 history paragraphs yields a file whose sha256 is 7f007ec41c9b0dedded66c964ba8e858d1d604e40b10a0ab278966f7eb2a2ae6, so nothing else differs, byte for byte. PyYAML against main's copy (4520b8f0): threat_model, trust_anchors, premises, supersedes, reset_of and design_review equal; the changed invariants are INV-2, INV-6 and INV-12, the first and last as round 20 accepted them; INV-4 equals main's text; INV-6 equals main's INV-6 plus the clause, byte-equal to the round-20 proposal, and the clause occurs once across all invariants; implementing_tasks adds dotfiles-T128-v0-main-tests-a02: [INV-12] and dotfiles-T128-gate-evidence-a01: [INV-6], nothing removed or changed.

The gate-evidence entry now maps to a sentence that states both refusals, which is what round 20 asked. Round 21 was withdrawn before it reached this seat; this receipt covers v20 only.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted (back to its v18 text). INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
