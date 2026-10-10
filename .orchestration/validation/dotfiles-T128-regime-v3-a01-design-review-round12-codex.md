---
reviewed_at: 2026-10-10T22:56:28Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@35b48cc3a2f2df31fa75b8a54012ffe62efeedbddb8e875844f461822f8323a1
round: 12
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round11-codex.md
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

INV-12: rejected: the no-contract clause is mechanically carried through V0 steps 1(b), 3(b2), and 4, but removal of the contract decorator is specified only as an implementation/Worker-Playbook obligation. No check fails when an implementation PR leaves a satisfied contract decorated, despite INV-12 requiring every rule to have a test that fails when the rule is removed.

The two clauses introduce one new enforcement gap: the “nothing stays dormant” outcome is asserted but not checked. The design-tier no-contract clause introduces no new gap; `main-tests` explicitly fails it and V0 includes the corresponding negative test.

## Findings

P1, high confidence — `.orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md:33`: require a deterministic check, with a removal-sensitive test, that fails an implementation PR when the contracts it satisfies remain decorated. Documentation in steps 1b and 4 does not enforce promotion into ordinary tests.

## Residual

Operator authentication and the forthcoming `pull_request_target` policy remain the previously accepted residuals. Implementation and CI were not executed; this was a read-only design confirmation and no files were modified.

Design verdict: revise