---
reviewed_at: 2026-10-12T13:10:22Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@9c9d42cb00c52457e8e7df37bf5276d42978d3466768286cd30b326fb8fdc0e2
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 24
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 24 (v21: the gate-evidence a02 map entry)

Delta judged against main's copy at 7a067b19 (the round-22 pointer copy). A line diff shows one insertion in the front matter, dotfiles-T128-gate-evidence-a02: [INV-6] after the a01 entry, and the v21 history paragraph; nothing else. PyYAML: invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to main's; implementing_tasks adds that one entry, removes nothing, changes nothing.

The entry names the right invariant: the a02 task file (930f570b, written by this seat as dotfiles-T128-gate-evidence-redesign-a01) carries exactly INV-6, byte-equal to the design's sentence, and its reset_of names a01, whose entry stays as parked history as the V0 and round-18 successors' do. The sibling successor dotfiles-T128-playbook-rules-a02 carries no invariants key and needs no entry (kind docs, review tier). This closes the consequence the redesign receipt named: a02's INV-2 map lookup now holds on main once this lands.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
