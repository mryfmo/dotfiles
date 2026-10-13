---
reviewed_at: 2026-10-13T03:08:23Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@828b410a66a0bf993ffab1f7a9987180f9eaa54c29ddd2a57995dafdf8f9c731
round: 28
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round27.md
previous_design: e1ad741f35ed9057d2cf6ccc38374525ac52f593b682a41c83fcce8180edb6e9 (v24 as reviewed in round 27); main's copy 20d0937b (v22, ce0af5d0)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 28 (v24 history lines without any a04 hash)

Delta judged against main's copy at 20d0937b (v22, main ce0af5d0). A line diff shows one insertion in the front matter, dotfiles-T128-gate-evidence-a04: [INV-6] after the a03 entry, and the v23 and v24 history paragraphs; nothing else. PyYAML, run by this seat: of the front-matter keys only implementing_tasks differs, adding that one entry, removing and changing nothing; invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to main's. The orchestrator's pasted keydiff (implementing_tasks ['dotfiles-T128-gate-evidence-a04']) matches; the map is identical to v23's and v24's as reviewed in rounds 26 and 27.

Since round 27: the v23 line no longer carries the a04 hash it named (it points to the reset record dotfiles-T128-gate-evidence-a03-design-reset.md), the v24 line no longer carries the prefix and now says "a04 round 4 after round 3" (the label my round-27 note asked to correct), and grep for the four a04 hashes (b062e46e, 13d2ca48, 1f8e7518, 03a5253d) finds none in the design, so the reset record is the sole anchor and later a04 rounds do not move the design. Neither history line has reached main, so the rewrite is of uncommitted text.

The entry names the right invariant: the current a04 file (03a5253d, redesign round 4) carries exactly INV-6, byte-equal to the design's sentence, and its reset_of names a01, a02 and a03, whose entries stay as parked history.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
