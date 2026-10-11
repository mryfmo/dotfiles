---
reviewed_at: 2026-10-10T23:47:52Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 18
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round17.md
files:
  - dotfiles-T128-v0-main-tests-a01@ba879b56b6c11518 (prefix; full hash in the TASK line)
  - dotfiles-T128-v1-task-schema-a01@aa5f3be9d0500a2c
  - dotfiles-T128-v2-audit-schema-and-runner-a01@9b7828fb36a9836d
verdicts:
  dotfiles-T128-v0-main-tests-a01: "revise: R18-1 V0's own allowed_files fail its step (b0); R18-2 V1b and V1c fail it too"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 18: Bot findings on boundary head 636e3b5f in V0, V1, V2

Design unchanged at 15daca85; the three invariants byte-identical; pointers at round 13. Bot threads not read from this seat.

## V0: revise

- The per-script convention in step (b0) (tests/unit/test_<name>.py, leading executable_ stripped, extension dropped, dashes to underscores) matches the repository (test_herdr_agents.py, test_permgate.py, test_agmsg_dispatch.py, test_github_release.py all resolve), and "a declared module must exist in HEAD" closes the deletion path. Both are sound.
- R18-1: V0 itself is design tier and declares scripts/main-tests.sh and scripts/lib/contract_markers.py; under its own (b0) the second needs tests/unit/test_contract_markers.py declared, which is not in allowed_files (only test_main_tests.py and regime_contract.py are). On this first PR the job runs the PR's own harness, so V0 fails itself. Add tests/unit/test_contract_markers.py to allowed_files and move the ast cases (b3, b4) there, or fold the helper into main-tests.sh.
- R18-2 (files outside this round, same rule): V1b declares scripts/regime-check.sh and scripts/pr-caps.sh with only tests/unit/test_pr_caps.py, and V1c declares scripts/validate-task.py with only tests/unit/test_regime_check.py; both are design tier, so (b0) fails each. Add tests/unit/test_regime_check.py to V1b's allowed_files and tests/unit/test_validate_task.py to V1c's; extending the tests of a script a task changes is what the rule intends. V2 passes (scripts/audit-head.sh with test_audit_head.py; Makefile is not a script path).
- Test (f) now covers two scripts with one module, a data-only declaration and a deleted declared module; fine.

## V1: ready

tests/unit/test_high_risk_paths.py is added to allowed_files and holds the constants and tier_of cases, so each of V1's scripts has its module under (b0); item 4 says where each test lives.

## V2: ready

The runner now requires the main checkout to be on main with HEAD equal to origin/main after a fetch; reserves a pool slot under a lock for the whole run with one worktree per slot (audit-<slot>-<sha7>) and an exit trap that leaves the identity, removes the worktree and frees the slot on every path; takes the .claude refusal range from the merge base with origin/main so a .claude change that reached main after the branch point does not block the fallback; item 6 adds the admission, trap, HEAD, snapshot-drift, premise-index and lock tests. All consistent with INV-5.
