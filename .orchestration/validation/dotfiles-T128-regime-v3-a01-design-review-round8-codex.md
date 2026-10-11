---
reviewed_at: 2026-10-10T22:39:34Z
reviewer: codex-review-dot-h001 (headless)
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@84cec99c360383912134e6d2f5ae0963078c40c3ee0033b2e1017f030d8448d3
round: 8
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round7-codex.md
---

INV-1: accepted

INV-2: rejected: the 500-line cap excludes all additions under `tests/`, so an arbitrarily large test change can still defeat the stated small-review invariant; count test additions toward the total, or impose a separate bounded test-line cap.

INV-3: rejected: checking only that the named test file exists and changed permits a comment-only edit or an unrelated existing selector; require the exact selector to be collected and pass on the revised head, and to fail or be absent on `previous_head`.

INV-4: rejected: requiring premises while having reviewers and auditors re-run only a sample still permits an invented, untested premise to drive implementation; require an explicit per-premise independent disposition, with executable local premises re-run and external premises linked to fetched evidence.

INV-5: rejected: the official headless documentation confirms the quoted `--add-dir` exception, but that means the untrusted PR worktree’s `.claude/skills/` is loaded. The premise says the fallback must refuse such heads, yet INV-5 and V2 do not specify or enforce that refusal. Refuse any audited head changing `.claude/skills/**`, or expose a sanitized data tree that excludes all Claude configuration and instruction files. The input manifest and audit-input boundary otherwise resolve the round-7 acceptance-record finding.

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: rejected: the GitHub commits endpoint’s committer date is embedded in the commit and can be chosen before push, so it does not establish when the first push reached GitHub. Use the draft PR’s server-generated `created_at` as the measurable early-publication event. Dispatchability also ignores task dependencies and stated wave preconditions; compute readiness from prerequisite acceptance/reset state before treating a queued task as dispatchable.

INV-11: accepted

INV-12: rejected: a trusted-root model audit is an independent review but not a deterministic oracle proving that every rule has a fails-when-removed test. A PR can weaken both gate code and its PR-controlled tests while leaving the auditor to detect the mutation probabilistically. Put the invariant contract or mutation cases on `main` before implementation, then run that main-pinned harness against the PR implementation.

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:49 The Claude fallback exposes the audited PR as `--add-dir`; official documentation confirms this loads that directory’s `.claude/skills/`, while the promised refusal for heads changing those files appears only as a premise and has no enforcement point.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56 The independent oracle for gate changes remains a probabilistic model audit rather than a main-pinned deterministic harness exercising the invariants against PR code.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:47 A changed test file does not prove that the named selector exists, executes, or newly detects the issue that caused the revision.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:48 Sampling premises leaves unchecked premises able to reproduce the false-premise loop the invariant is intended to stop.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:54 A commit’s committer date is not a GitHub-observed push timestamp, and the dispatchability predicate treats dependency-blocked tasks as ready work.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:46 Excluding all test additions from the line cap leaves review size unbounded despite the small-PR invariant.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:155 The enforcement map still documents the removed `repro:<id>` path, contradicting INV-3 and section 10.

[P3] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:162 The enforcement map still names `gh pr view`, while INV-10 now specifies the commits endpoint, leaving the implementation contract internally inconsistent.

## Residual

Operator authentication is impossible under the stated one-user and one-GitHub-account constraints. The `permissions.ask` waiver command, absence of a permgate allow path, and visible waiver records are therefore accepted as the strongest achievable friction, not as authenticated attribution.

The round-7 bare-mode P2 is withdrawn: the re-fetched official page contains the quoted `--add-dir` skills exception. That confirmation creates the narrower unresolved trust-boundary finding above because the design does not carry its stated `.claude/skills/**` refusal into an invariant or implementation wave.

Cost data remains based partly on mutable internal transcripts, but INV-9 now binds the sources by path and digest and treats cost only as a warning metric; this is acceptable with the residual that it is reproducible bookkeeping, not tamper-proof accounting.

Skipped: no files were modified and no implementation tests were run. Risk: the design remains unsafe to implement until the rejected invariants are corrected.

Design verdict: reject