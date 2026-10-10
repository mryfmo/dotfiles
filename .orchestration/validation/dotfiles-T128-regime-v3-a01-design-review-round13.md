---
reviewed_at: 2026-10-10T23:01:10Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 13
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round12.md
premises: as in round 11 (13 premises, all hold; none changed in v13)
---

# Design review: dotfiles-T128-regime-v3-a01, round 13 (confirmation of the Codex round-12 clause)

INV-12 (line 57) now also reads: main-tests fails an implementation PR (any task id not ending in -contract-a01) whose declared test module in the PR tree still carries a contract marker. With the two round-11 clauses this closes the contract lifecycle: dormant on main, activated against the implementation, promoted by the implementation, and a leftover marker is a failure rather than a silent skip. The receipt pointer names this round; the five task files carry INV-1, INV-2, INV-5 and INV-12 byte-identical to v13.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
