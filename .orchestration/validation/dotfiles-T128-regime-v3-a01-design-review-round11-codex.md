---
reviewed_at: 2026-10-10T22:51:56Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@07b621d1fe2f0a5616b39b87807df0d08b06243cd6060cdc680f894d2b353eeb
round: 11
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round10-codex.md
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

premise 1: unverifiable — the named dependency call sites are present, but dependency resolution was not rerun in this read-only review.

premise 2: holds — the main-pinned `pull_request_target` architecture and required-status-check use are consistent with the stated GitHub behavior.

premise 3: holds — the stated Codex CLI schema-output and rejected-argument behavior remains consistent with the reviewed interface.

premise 4: holds — the Claude headless, bare-mode, hook, structured-output, and budget behavior is internally consistent.

premise 5: holds — the two-correction reset recommendation supports the proposed mechanical reset threshold.

premise 6: unverifiable — the artifacts support the sequence, but the reported run durations and full elapsed interval were not independently reconstructed.

premise 7: holds — treating both Stop hooks as soft signals and the merge gate as the mandatory backstop is sound.

premise 8: holds — the referenced transcript format contains per-message usage fields.

premise 9: unverifiable — the stated history limits were not rerun because that command requires writable temporary state unavailable to this seat.

premise 10: holds — the default-branch requirement for `workflow_dispatch` supports the proposed bootstrap order.

premise 11: holds — the `--add-dir` skill-loading behavior justifies refusing the Claude fallback for heads changing `.claude/**`.

premise 12: holds — the stated event-policy deadline and explicit allowlisting requirement are correctly carried into the design residual and V1c acceptance action.

## Findings

No findings. The v11 two-mode protocol resolves round 10's blocking cycle: contract PRs can merge while dormant, declared implementation changes activate main's reviewed contracts with `REGIME_CONTRACT=1`, and undeclared script changes remain subject to main's ordinary tests. The V0 task specifies the corresponding harness, required check, contract decorator, and removal-sensitive test cases.

## Residual

Operator authentication remains impossible under the one-user, one-account constraint. The waiver directory and native permission prompt provide enforceable friction and visibility, not authenticated attribution.

The main-pinned gate still depends on the operator installing an applicable Actions event policy before GitHub begins enforcing the stated `pull_request_target` default restriction on 2026-11-02.

Implementation and CI were not executed, and premises requiring writable caches or agmsg-history temporary state were not rerun. No files were modified.

Design verdict: accept