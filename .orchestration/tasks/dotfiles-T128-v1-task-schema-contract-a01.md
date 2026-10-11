---
format: 2
task_id: dotfiles-T128-v1-task-schema-contract-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - tests/unit/test_validate_task.py
  - tests/unit/test_high_risk_paths.py
invariants:
  INV-1: "every task is a format-2 file whose front matter validates against schemas/task.json (jsonschema + PyYAML, no hand-written parser; every allowed_files entry starts with a literal path segment and a wildcard entry derives the tier of every design-tier path its literal prefix can cover); legacy task ids are grandfathered only for files under .orchestration/tasks/ on main, never for a branch copy; the tier (docs, review, design) is derived from allowed_files by the shared high-risk module, with the regime's own rule prose (home/dot_config/claude/rules/**, the agmsg-orchestration SKILL, AGENTS.md, README) listed in the review tier, and selects the pipeline from process_tiers in agent-config.yaml; every AGMSG-TASK for the task, the first and each amendment, carries task_sha256= of the task file as sent, the worker commits the file byte-identical to .orchestration/<task id>/task.md (first commit, recommitted after each amendment), the CI regime job validates that copy with main's schema and refuses a PR that changes .github/workflows/** unless its task.md is design tier and lists the file, the host gate compares the copy's sha256 with the latest AGMSG-TASK's token in history, and the regime check binds only once the ruleset lists it as required (an operator action named in V1's acceptance record); the orchestrator can add or skip a stage only with an operator waiver written by scripts/regime-waive.sh, a command under a permissions.ask rule in the managed settings with no permgate policy entry, so that only the human's answer to the native prompt runs it (an ask rule prompts even in auto mode; agent-to-agent approval is forbidden); the waiver names the task, the stage and a reason and is written under $XDG_STATE_HOME/regime/waivers/, a directory outside every seat's sandbox write roots, so no sandboxed seat can write it and only a command run outside the sandbox on the human's answer to the native prompt can (the directory is the guard; the ask rule on the named command is the second layer, since a reworded command would still meet the prompt at the sandbox boundary); it is listed by check-regime-boundary.sh and the boundary PR body (V3a owns the script and its ask rule), and is the strongest friction available on a machine where every seat and GitHub action is the operator's own account (operator authentication is a stated residual, not a claim)"
after:
  - dotfiles-T128-v0-main-tests-a01
premises:
  - claim: "a contract PR ships only dormant @contract tests (tests/unit/regime_contract.py from V0), which skip in ordinary CI, so it merges before the implementation and main-tests activates them against the implementation PR"
    command: "grep -n 'REGIME_CONTRACT' .orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md | head -2"
    output: "V0 items 1(b) and 1b: contract = unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')"
---

# AGMSG-TASK dotfiles-T128-v1-task-schema-contract-a01 — contract PR for dotfiles-T128-v1-task-schema-a01 (dormant tests only)

DRAFT; dispatched after V0 merges, before `dotfiles-T128-v1-task-schema-a01`. Design tier (the implementing wave is design tier). Claude seat, `.claude/worktrees/worker-c`, branch `feat/task-schema-contract` from `origin/main`.

Write the test modules the implementing task names (tests/unit/test_validate_task.py tests/unit/test_high_risk_paths.py) with every test decorated `@contract` (from `tests/unit/regime_contract.py`), one test per rule of the implementing task's "What to build" and "Tests" sections, each written so that it fails when its rule is removed; the modules import nothing that does not exist on `main` yet (drive the future script as a subprocess by path and skip with the contract decorator). Nothing else changes. The implementation PR that follows removes the decorators (promotion) as V0's main-tests requires.

Validation: the modules collect under `make unit-test` with every test skipped (`dormant contract`) and run under `REGIME_CONTRACT=1` with every test failing (the script does not exist yet; paste both outputs). First commit: this task file byte-identical to `.orchestration/dotfiles-T128-v1-task-schema-contract-a01/task.md`; evidence beside it. Completion: draft PR within 30 minutes (`test(regime): dormant contract tests for v1-task-schema-a01`), CI, Bot wait, artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=6. Forbidden: any file outside allowed_files; `make update`; thread resolution.
