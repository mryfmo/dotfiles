---
reviewed_at: 2026-10-10T23:00:35Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
round: 13
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round12-codex.md
---

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

V0 as written mechanically enforces every main-tests clause of INV-12. In particular, step 1(c) inspects the PR-tree copy of each declared test module, rejects contract markers on task ids not ending in `-contract-a01`, and test (b3) is removal-sensitive while confirming the contract-PR exception. The PR-tree archive plus main-test overlay preserves module-relative `ROOT` resolution; module selection comes from `tests/unit/*.py` entries in the PyYAML-parsed task; the existing no-contract, undeclared-change, deletion, and no-script-change cases remain specified. INV-12’s broader per-invariant tests and audit conformance clauses are mechanically distributed to their implementing waves rather than implemented by V0 alone.

## Findings

None. The round-12 enforcement gap is closed by V0 steps 1(c), 3(b3), and 4.

## Residual

Operator authentication and the forthcoming `pull_request_target` policy remain the previously accepted residuals. Implementation and CI were not executed; this was a read-only design confirmation, and no files were modified.

Design verdict: accept