---
format: 2
task_id: dotfiles-T128-ci-skip-orchestration-contract-a01
superseded_by: dotfiles-T128-ci-skip-orchestration-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - tests/unit/test_workflow_orchestration_skip.py
invariants:
  INV-2: "a PR is mergeable only within the caps the CI regime job enforces from main's workflow (at most 15 changed files outside .orchestration/, 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt, and 1000 added lines under tests/), and its task.md invariants equal the design's as a set of ids and byte-for-byte as sentences (the design read from main, never from the PR; a task id ending in -contract-a01 is compared with its implementing task's entry); the design file must be on main (through a boundary PR) before the implementing TASK is dispatched and the regime job fails closed when the design named by task.md is absent from main; an .orchestration-only PR runs no bootstrap or test matrix and every required check context still reports success (each required workflow decides inside its jobs, as test.yaml's changes job does), so a boundary PR merges in minutes; exceeding a cap is a split, never a finding to disposition (the cap changes the unit of work: T116 +529 and T118 +881 would have been split)"
after:
  - dotfiles-T128-v0-main-tests-a01
premises:
  - claim: "a contract PR ships only dormant @contract tests (tests/unit/regime_contract.py from V0), which skip in ordinary CI, so it merges before the implementation and main-tests activates them against the implementation PR"
    command: "grep -n 'REGIME_CONTRACT' .orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md | head -2"
    output: "V0 items 1(b) and 1b: contract = unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')"
---

# AGMSG-TASK dotfiles-T128-ci-skip-orchestration-contract-a01 — contract PR for A201 (dormant tests only)

Dispatched after V0 merges, before `dotfiles-T128-ci-skip-orchestration-a01`. Design tier. Claude seat, branch `feat/ci-skip-orchestration-contract` from `origin/main`.

Write `tests/unit/test_workflow_orchestration_skip.py` with every test decorated `@contract` (from `tests/unit/regime_contract.py`): the YAML-level rules A201 names (no job-level `if` on a required context's job; step-level `should_run`/`should_test` gates on every heavy step of `public-bootstrap`, `private-bootstrap` and `main-tests`; `changes` true on `push`, `schedule`, `workflow_dispatch`; context names equal the ruleset's seven), each failing on today's workflows under `REGIME_CONTRACT=1` and skipping without it. Nothing else changes.

Validation: the module collects under `make unit-test` with every test skipped (`dormant contract`) and fails under `REGIME_CONTRACT=1` against the current workflows (paste both). First commit: this task file byte-identical to `.orchestration/dotfiles-T128-ci-skip-orchestration-contract-a01/task.md`; evidence beside it. Completion: draft PR within 30 minutes, `gh pr ready` before the Bot wait, CI, Bot wait, artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=6. Forbidden: any other file; `make update`; thread resolution.
