---
reviewed_at: 2026-10-11T04:04:38Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
round: 16
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15-codex.md
---

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: rejected: splitting count/report into A3 and mandatory Stop-hook/merge-gate wiring into V3a preserves the enforcement point, but A3’s threat table does not protect boundary reporting from orchestrator-controlled acceptance, reset, or waiver artifacts; require validation of those release artifacts, with tests proving forged records cannot suppress a reached threshold.

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

The two-line removal reproduces round 15’s accepted whole-file SHA-256 exactly, confirming that INV-1 through INV-12 and all premises are otherwise unchanged. The new implementing-task entry assigns only INV-6 to A3 and does not transfer or expand another wave’s scope. A3 computes and reports; V3a retains the mandatory Stop-hook and merge-gate enforcement and therefore remains consistent with INV-7 and the trust anchors.

## Findings

A3: The closed “orchestrator edits `.orchestration` files” row tests only that a forged acceptance record does not change a count. It cannot close the actual control path: `check-regime-boundary.sh` suppresses reporting when the orchestrator creates an accepted acceptance record, any `<id>-reset.md`, or a `DESIGN_RESET_WAIVED_BY=` line. The test must prove that forged or semantically invalid release artifacts do not suppress a reached threshold; reset identity/redesign validity and waiver provenance must be validated through their trusted anchors.

A3: No row covers the PR’s control of `scripts/regime-counters.sh`, its tests, and its fixtures. A malicious implementation can undercount or falsely label fixture-derived output as `source=live`, while PR-authored tests still pass. Add a row binding the behavior to main’s dormant contract tests and trusted-root audit, including a test that fails for undercounting and forged source attribution.

## Residual

A3 is only a counting and boundary-reporting layer; it is not the mandatory enforcement point. Until V3a lands, Stop-hook signaling and merge refusal remain absent, audit counts intentionally remain `unknown`, and the orchestrator’s manual audit-class count is not mechanically authenticated.

Implementation, live GitHub behavior, and tests were not executed; no files were modified.

Design verdict: revise