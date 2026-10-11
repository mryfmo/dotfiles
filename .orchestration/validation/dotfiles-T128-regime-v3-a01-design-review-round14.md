---
reviewed_at: 2026-10-11T02:43:34Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@58b95ba4e39ad2e422fa2cf80e218c76880f4847dd0510ce5e7aef5b2e8f6355
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 14
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11 (re-run or re-fetched there; none changed in v14)
---

# Design review: dotfiles-T128-regime-v3-a01, round 14 (plan 006 A102: INV-12 nonce runner, INV-2 CI skip)

Read: v14's INV-2 and INV-12, the map entry dotfiles-T128-ci-skip-orchestration-a01: [INV-2], plan 006 (A102, A201, A301), V0's current task text for the runner (hash bbb3dc53, not the dispatched f16cbd9c), the five bootstrap and test workflows' triggers, and the count of unit modules that import scripts in-process (7 of 34 use importlib). The Codex review of this hash runs in parallel; one revision follows the pair.

INV-2: accepted. An .orchestration-only PR running no bootstrap or test matrix, with the required checks reporting success from the changes job, is the CI half round 1 of the contracts review asked to authorize properly, and the map entry does that. Note for A201: remote.yaml, macos.yaml and ubuntu.yaml all run on pull_request and none has a changes job today; the implementing task must cover every workflow whose job the ruleset lists as required, not only remote.yaml and test.yaml, and the ruleset's list is not readable from this seat.

INV-12: rejected on one clause. The nonce runner is sound as far as it goes: a nonce read from an inherited pipe and closed before any test loads, never in the environment or argv, written back with the counts to a harness-chosen path, means a planted module cannot write an accepted result on its own. The residual sentence is incomplete, though: the nonce authenticates the writer of the result, not the counts in it. PR code that main's tests import in-process (7 modules do) can patch unittest's result machinery (TestResult.addFailure, TestCase.run) at import time, and the genuine runner then writes genuine-nonce JSON with forged counts; no frame introspection is needed. Right: "the remaining forgery paths, frame introspection for the nonce and in-process patching of unittest's result collection by adversarial PR code, are the trusted-root audit's to catch and are stated in every acceptance record of a design-tier PR". Optional cheap hardening for V0, not for the sentence: the runner keeps references to the unittest classes it will use before importing any test and refuses when they differ afterwards, which closes the import-time patch and leaves only patches made during a test's own execution.

INV-1, INV-3, INV-4, INV-5, INV-6, INV-7, INV-8, INV-9, INV-10, INV-11: accepted; INV-1 and INV-5 verified byte-identical through the task files, the others stated unchanged by the Round-14 section and not byte-diffed against v13.

## Consequences for the task files

- V0 is in flight (PR 317, revise round 1); its task file already carries the runner text and its hash moved from the dispatched f16cbd9c to bbb3dc53, so the change reaches the worker as AGMSG-TASK amendment=1 with the new task_sha256 (INV-1), the first of the two INV-6 allows; V0's INV-12 sentence must be v14's at that point.
- V1b carries INV-2 v13 and is not yet dispatched; update its sentence before dispatch. Every other task file moves its pointer to this round once both receipts accept, as A102 says.
- A premise for the in-process import (the importlib count) would ground the new INV-12 clause; add it with the grep.

Design verdict: revise
