---
reviewed_at: 2026-10-12T15:33:44Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 25
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round24.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 25 (v22: the gate-evidence a03 map entry)

Delta judged against main's copy at 9c9d42cb (v21, main e0e2fe62). A line diff shows one insertion in the front matter, dotfiles-T128-gate-evidence-a03: [INV-6] after the a02 entry, and the v22 history paragraph; nothing else. PyYAML: invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to main's; implementing_tasks adds that one entry, removes nothing, changes nothing.

The entry names the right invariant: the a03 task file (686806a1, written by this seat as dotfiles-T128-gate-evidence-redesign-a02) carries exactly INV-6, byte-equal to the design's sentence, and its reset_of names a01 and a02, whose entries stay as parked history, as the earlier successors' do. This closes the design note the redesign receipt and the a03 introduction carry: a03's INV-2 map lookup holds on main once this lands.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
