---
reviewed_at: 2026-10-10T22:57:40Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@35b48cc3a2f2df31fa75b8a54012ffe62efeedbddb8e875844f461822f8323a1
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 12
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round11.md
premises: as in round 11 (13 premises, all hold; none changed in v12)
---

# Design review: dotfiles-T128-regime-v3-a01, round 12 (confirmation of the two INV-12 clauses)

INV-12 (line 57) now reads: the implementation PR promotes its contracts by removing the decorator in its own tree, main-tests judging it against main's dormant copy so nothing stays dormant after the wave lands; and main-tests fails a design-tier implementation PR whose declared script has no dormant contract on main, an empty contract being no pass. Both round-11 clauses are applied as asked. The receipt pointer names this round. The five task files carry INV-1, INV-2, INV-5 and INV-12 byte-identical to v12.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

This Claude-side review closes at 35b48cc3; the Codex round-12 confirmation is the second receipt INV-7 requires.

Design verdict: accept
