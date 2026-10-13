---
reviewed_at: 2026-10-13T03:06:15Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@e1ad741f35ed9057d2cf6ccc38374525ac52f593b682a41c83fcce8180edb6e9
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@682ec66b87a5b82dae26bc4153c4342f4c1ea7fe9db6c93fdeebb232e9de7245
round: 27
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round26.md
previous_design: 9373f8e8a3f2f19549e3028f089f7b4c433e8ffdfbec71c1f9ed1c4046896c92 (v23, round 26); main's copy 20d0937b (v22, ce0af5d0)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 27 (v24: the gate-evidence a04 map entry, the a04 hash moved out of the design)

Delta judged against main's copy at 20d0937b (v22, main ce0af5d0). A line diff shows one insertion in the front matter, dotfiles-T128-gate-evidence-a04: [INV-6] after the a03 entry, and the v23 and v24 history paragraphs; nothing else. PyYAML, run by this seat: of the front-matter keys only implementing_tasks differs, adding that one entry, removing and changing nothing; invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to main's. The orchestrator's pasted keydiff (implementing_tasks ['dotfiles-T128-gate-evidence-a04']) matches, and the map is identical to v23's.

The entry names the right invariant: the current a04 file (03a5253d, redesign round 4, Codex round-4 confirm on it) carries exactly INV-6, byte-equal to the design's sentence, and its reset_of names a01, a02 and a03, whose entries stay as parked history. The v24 line's decision is sound: the a04 hash lives in the reset record, not in the design, so a later a04 round does not move the design hash and force another design round; the v23 line keeps the hash it named as history, which the v24 line explains.

Note, not a finding (P3, text): the v24 line calls 03a5253d "a04 round 3"; 03a5253d is the round-4 file (round 3 was 1f8e7518, before the negative review-body cases). The design binds no a04 hash after v24, so nothing depends on the label; correct it at the next history line.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
