---
reviewed_at: 2026-10-11T02:45:05Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@3572107047ffd67012ac494d6d3ca4bb4100bd564e9ea1b78f3942f2c39435ca
round: 15
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round14-codex.md
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

The residual is now stated honestly. The nonce authenticates that the pinned runner reached the reporting path, but does not authenticate the reported counts. Pinning the `unittest` result and runner classes before test imports narrows trivial replacement paths without claiming process isolation; PR-controlled in-process code can still mutate result collection or recover the nonce through shared-process introspection.

## Findings

None.

INV-2 now covers every required check context while preserving the safe job-internal skip model for `.orchestration`-only PRs. INV-12 no longer overstates the nonce’s guarantee and explicitly carries the unresolved in-process forgery risk into trusted-root audit and design-tier acceptance records.

## Residual

A malicious PR module executing inside the trusted test process can still tamper with result collection—even with pinned class references—and can potentially recover the genuine nonce from process memory or frames. The trusted-root audit is therefore a model-backed detection control, not cryptographic prevention. Eliminating this residual requires process isolation and would replace the proposed in-process oracle.

Implementation and live CI were not executed; no files were modified. Existing operator-authentication and `pull_request_target` policy residuals remain unchanged.

Design verdict: accept