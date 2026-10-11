---
reviewed_at: 2026-10-11T07:38:24Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 18
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; none changed in v17 (byte-equal to v16's)
---

# Design review: dotfiles-T128-regime-v3-a01, round 18 (the reset successors' map entries)

Delta judged against v16 at 15957fbc, taken from the boundary branch orchestration/boundary-2026-10-11-2 (commit 48d055ca, whose copy of the design hashes to 15957fbc). A line diff shows two insertions and nothing else: implementing_tasks gains dotfiles-T128-ci-skip-orchestration-a02: [INV-2] after the a01 entry and dotfiles-T128-regime-counters-a02: [INV-6] after the a01 entry. Parsed with PyYAML, invariants, threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to v16's; the map has the two additions, no removal and no changed value.

The entries name the right invariants: each successor's task file carries exactly the invariant id of its entry (ci-skip a02 INV-2, regime-counters a02 INV-6), each sentence is byte-equal to the design's, each reset_of names its a01, and the a01 entries stay, so the -contract-a01 remap (dotfiles-T128-ci-skip-orchestration-contract-a01 resolves to the a01 entry) still lands on a mapped id with the same invariant.

Nothing else a reset successor needs under INV-2 or INV-6: INV-2 compares by task id and the successors are now mapped; INV-6's release is the reset record naming a redesign whose RESULT comes from another identity, which both records have (RESULTs 483 and 502); INV-10 reads reset records on the a01 ids, so the a01s stop being dispatchable and the a02s are already dispatched. Two notes, neither a finding: the boundary branch still carries v16, so it must take v17 before it merges or main stays without the successor entries; and section 8's A3 and A5 bullets (unhashed) still name the a01 ids, cosmetic.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
