---
reviewed_at: 2026-10-11T04:04:48Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 16
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; none changed in v16
---

# Design review: dotfiles-T128-regime-v3-a01, round 16 (plan 006 Phase A: the A3 map entry)

Delta only, as asked. The hashed change is the map entry dotfiles-T128-regime-counters-a01: [INV-6] (line 17) with the A3 bullet before V3a (line 181): scripts/regime-counters.sh computes every INV-6 count and prints the thresholds reached, check-regime-boundary.sh reports a reached threshold with no reset record or waiver, the orchestrator runs it before every acceptance action, and V3a wires the script into the hook and the gate.

- Consistent with INV-6's enforcement point: the mandatory point stays the merge backstop in require-crit-review.py and the early signal stays the Stop hook; A3 supplies the computation both call and gives the boundary check its report earlier than V3a lands. Two notes for the A3 task, not the sentence: the hook may only use history counts inside its 3 s budget (INV-6), so the script needs a history-only mode the hook calls, with the GitHub and audit-JSON counts reserved for the gate and the boundary check; and the bullet says "from history and GitHub" while INV-6 also counts audit heads from the main checkout's audit JSONs whose sha256 matches their AGMSG-AUDIT record, which the script must read the same way (and history through the storage facade or with a limit, premise 9).
- Consistent with INV-7: a map change, reviewed by the pair on one hash, as the protocol now runs. Consistent with the trust anchors: the counts' sources are history, GitHub and sha-anchored audit JSONs, never a file the orchestrator can author freely.
- No other wave's scope changes: V3a keeps the hook and gate wiring. Prose outside the hash to align without a new review: the INV-6 enforcement row names regime-counters.sh (0) and the V3a bullet names it (0); where either is 0, V3a still reads as computing the counts itself, which is now A3's job.
- INV-1 to INV-12 and the 13 premises are unchanged against round 15 (INV-1, INV-2 and INV-5 verified byte-identical through the task files; the others not byte-diffed and stated unchanged). The design's own design_review.receipt (line 7) still names round 15; the ci-skip task already names round 16, so move the design's pointer once the pair accepts.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: accept
