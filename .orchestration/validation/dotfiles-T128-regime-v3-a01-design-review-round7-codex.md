---
reviewed_at: 2026-10-10T22:34:30Z
reviewer: codex-review-dot-h001
profile: review
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@40476474ad9aec1f36f14927a43a8f98d0187eb5d7092b422b635fbdff70142a
round: 7
---

INV-1: rejected: an operator waiver is only named in an orchestrator-authored acceptance record, so the orchestrator can fabricate permission to skip stages; require an operator-authenticated agmsg or GitHub event and bind its immutable identifier in the gate.
INV-2: accepted
INV-3: rejected: the `repro:<id>` path verifies only that PR-controlled command and output strings are non-empty, so any revision passes without adding a deterministic check; execute a main-approved reproducer in CI or remove this alternative.
INV-4: rejected: premises and pasted outputs are entirely orchestrator-authored and never independently executed or history-anchored, so false premises still pass; verify commands in a trusted runner and bind results to the task hash before dispatch.
INV-5: rejected: the audit is said to consume an acceptance record before stage 4 creates it, and no hash binds the complete audit input set; create and anchor an immutable pre-acceptance disposition draft before audit, then prohibit material changes without re-audit.
INV-6: rejected: `DESIGN_RESET_WAIVED_BY` and the reset record do not authenticate operator consent, allowing the orchestrator to release its own reset; require an operator-authored agmsg or GitHub event whose actor and immutable id the gate verifies.
INV-7: accepted
INV-8: accepted
INV-9: rejected: `accept-task.py` writes orchestrator-controlled cost claims from local transcripts without an immutable source binding, while transcript format is explicitly internal and per-message usage is unverified; anchor raw runtime JSON/session identifiers before acceptance and recompute the totals.
INV-10: rejected: `gh pr view` cannot establish the time of the first pushed commit, and “idle while a dispatchable task exists” has no mechanical definition or trusted dispatchability source; use immutable GitHub commit timestamps and define dispatchability as a computable history state.
INV-11: accepted
INV-12: rejected: `make unit-test` runs from the PR-controlled `pull_request` workflow and PR-controlled tests, while the proposed main-pinned job checks schemas, caps, and evidence shape rather than independently exercising every invariant; run invariant tests and their trusted harness from the base branch against PR data.

## Findings

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:45 The stage-skipping waiver is authenticated only by an orchestrator-authored acceptance record, so INV-1 can be bypassed by the actor it constrains.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:47 A fabricated non-empty `repro` command and output satisfy INV-3 without introducing any executable fact.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:48 The orchestrator can invent premise output, leaving T119’s false-premise amendment loop open before dispatch.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:49 The audit input includes an acceptance record that stage 4 has not yet produced, and later edits to that record do not invalidate the audit.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:50 The orchestrator can set `DESIGN_RESET_WAIVED_BY` and author the supporting record, defeating the mandatory reset backstop.

[P1] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:56 INV-12 relies on tests and a `pull_request` workflow the PR controls, so a malicious PR can weaken the oracle that judges its enforcement code.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:53 Cost totals are copied into orchestrator-controlled evidence without a trusted runtime-output digest, permitting arbitrary understatement.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:54 GitHub PR metadata does not identify the first push time, and “dispatchable” is subjective, making both timing rules gameable.

[P2] .orchestration/tasks/dotfiles-T128-regime-v3-a01.md:88 The premise that Claude bare mode loads skills from `--add-dir` contradicts the cited factsheet, which says `--bare` skips skills; fallback policy must distinguish bare from non-bare execution.

## Residual

T118’s long revise loop can still pass through fabricated `repro` evidence, and its oversized review burden can move into excluded tests or orchestration evidence.

T119’s false-premise cycle remains possible because premise commands are recorded but not independently executed; the orchestrator can also waive the resulting reset.

T124’s trust-boundary bypass pattern remains possible because PR-controlled invariant tests can approve weakened enforcement, while unauthenticated waiver and cost records preserve the same self-certification problem.

Design verdict: reject