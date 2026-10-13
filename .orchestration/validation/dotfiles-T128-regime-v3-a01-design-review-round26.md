---
reviewed_at: 2026-10-13T02:56:08Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@9373f8e8a3f2f19549e3028f089f7b4c433e8ffdfbec71c1f9ed1c4046896c92
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@cff76d4224fea364c3aade2cb782c7d5dcc14262bd55a2e41d8a86dbf4c0d725
round: 26
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round25.md
previous_design: 20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a (v22, main ce0af5d0)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 26 (v23: the gate-evidence a04 map entry)

Delta judged against main's copy at 20d0937b (v22, main ce0af5d0). A line diff shows one insertion in the front matter, dotfiles-T128-gate-evidence-a04: [INV-6] after the a03 entry, and the v23 history paragraph; nothing else. PyYAML, run by this seat: of the front-matter keys only implementing_tasks differs; it adds that one entry, removes nothing and changes nothing; invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to main's. The orchestrator's pasted keydiff (implementing_tasks ['dotfiles-T128-gate-evidence-a04']) matches.

The entry names the right invariant: the a04 task file (13d2ca48, written by this seat as dotfiles-T128-gate-evidence-redesign-a03 round 2, accepted by the orchestrator, the Codex half pending) carries exactly INV-6, byte-equal to the design's sentence, and its reset_of names a01, a02 and a03, whose entries stay as parked history, as the earlier successors' do. The history line states the reset's reason (the fourth binding row; plan 014 option A: the ledger covers every swept Codex finding id and every audit finding) and the a04 hash, which is the file's. This closes the design note the redesign receipt and the a04 introduction carry: a04's INV-2 map lookup holds on main once this lands.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
