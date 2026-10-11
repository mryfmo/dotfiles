---
reviewed_at: 2026-10-10T22:12:18Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b5eb917f85d44726a514efbf910d2e0f04c17f07110ef90310fd6b3b13719ceb
task: dotfiles-T128-task-review-v1-v2-a01
round: 4
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round3.md
files:
  - dotfiles-T128-v1c-regime-ci-check-a01@7ec717ca19821b870aee3e1d5e894bc5ea32a20bc11adb6be1119d6ba57edef6
  - dotfiles-T128-v2-audit-schema-and-runner-a01@04d4ea039c2af23211a892f3ccea4d0ddf1aaf5d3e8b5d4e0d401bfc251cecdb
  - dotfiles-T128-v1-task-schema-a01@70a4a7abd656df5b8c0f423062762881fdc00a7908606020c63fa8f412955f35 (unchanged)
  - dotfiles-T128-v1b-pr-caps-a01@121cf591817c6faeec79d8f986d248c463f4e12729de3aaed019436a621b253c (unchanged)
verdicts:
  dotfiles-T128-v1c-regime-ci-check-a01: "revise: R4-1 receipt pointer round 5 (all four files), R4-2 how the test's manifest copy is found"
  dotfiles-T128-v2-audit-schema-and-runner-a01: "revise: R4-1 receipt pointer round 5"
---

# Task-file review round 4: V1c and V2 after the Bot findings on PR 316

PyYAML check: INV-1 in V1c and INV-5 in V2 equal design v5 byte for byte; V1 and V1b hashes unchanged since round 3. Every design_review.receipt in the four files names the round-4 receipt while the design (line 7) now names round 5.

## V1c: revise

- V1c-1 and V1c-2 applied: the process_tiers rule's test lives in tests/unit/test_regime_check.py with a manifest copy (line 49); step (b) states exactly one task.md when anything outside .orchestration/ changes, a second refused, an .orchestration/-only range passing (line 44).
- Bot-driven steps applied: (c) every changed path outside .orchestration/ must match the task.md's allowed_files by fnmatch (line 44), which binds the derived tier to the real diff; audit_budget_usd is named as INV-9's one early field (line 47). Both are consistent with INV-1 and INV-2.
- R4-1: design_review.receipt (line 7) must name .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round5.md; the same one-line change in V1, V1b and V2, since the round-4 receipt's header hash is v4's and the gate compares it with the current design.
- R4-2 (worker question, name it now): item 3 resolves the manifest from the validator's own location, and item 6 tests the rule "in a manifest copy"; say how the copy is reached: the scratch repository carries copies of scripts/validate-task.py, scripts/lib/high_risk_paths.py, schemas/task.json and home/dot_agents/agent-config.yaml so the script-relative path lands on the copy, or item 3 adds a --manifest <path> override used only by tests. Either is fine; one must be written.
- Notes: caps unchanged (seven files, about 220 added lines); routing unchanged; the fnmatch premise lives in V1 and V1c relies on it through V1's module, which is fine since V1c runs after V1.

## V2: revise

- Bot-driven items applied: a reused audit-<sha7> worktree is kept only when its HEAD equals the full sha and its status is clean, otherwise recreated (line 50); the three files are masked before the JSON's sha256 is taken, so history matches the committed bytes (line 50); the fallback runs from inside the detached worktree with --bare when ANTHROPIC_API_KEY is set, else --settings '{"disableAllHooks": true}', managed hooks stated as remaining and harmless there (line 50; matches the headless and hooks pages); the overlap sentence is correct since V1 no longer touches prose (line 39).
- R4-1: receipt pointer as above.
- Note: with the fallback's cwd inside the worktree, --add-dir <worktree> is redundant and the main checkout's .orchestration inputs reach the model only through the prompt text the runner builds; that is what line 50 says ("build the prompt from the main checkout's files"), so no change, but the worker should not also expect to read them with the Read tool.

## V1 and V1b

Unchanged since round 3 (hashes above); they need only R4-1.

Recommendation: from now on, any edit to the design file carries the pointer update in the four task files in the same commit, so one confirmation round covers both.
