---
reviewed_at: 2026-10-10T22:12:18Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b5eb917f85d44726a514efbf910d2e0f04c17f07110ef90310fd6b3b13719ceb
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 5
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 5 (confirmation of the INV-3 form change)

Diff check of v5 against the Round-5 section: INV-3 (line 47) now admits check=<tests/<file>::<name> | repro:<id>>; the ci:<job> form is gone; a repro carries its command and pasted output in revise.yaml; the CI regime job verifies the test selector by existence and diff against the previous RESULT head and the repro by a non-empty command and output; the host gate requires the same id in the validation file. The receipt pointer names this round (line 7). V3c (line 170) and V2b still match the split of CI step and gate line. Dropping ci:<job> is right: a new CI job is a .github/workflows/** change, design tier under INV-1 and never a one-round fix, and it had no "fails on the previous head" meaning; the test selector and the repro both do.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Note: the task files V1, V1c, V1b and V2 still name the round-4 receipt, whose header hash is v4's whole-file sha256; V4's gate (and INV-7's whole-file form for pre-V4 receipts) compares the receipt against the current design, so every design change needs the implementing task files' design_review.receipt moved in the same edit. The task-review round-4 receipt carries this as its one item.

Design verdict: accept
