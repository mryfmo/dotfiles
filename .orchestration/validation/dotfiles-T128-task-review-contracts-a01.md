---
reviewed_at: 2026-10-11T00:08:12Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-contracts-a01
round: 1
files:
  - dotfiles-T128-v1-task-schema-contract-a01@9a934ce8c4113133cde772debb27c5dd9b51124d6b610f6e11bd3728ca895910
  - dotfiles-T128-v2-audit-schema-and-runner-contract-a01@00d622064e8ee14be4185d3db6feed0c9b2fcae0017bc1d239327177cb37533d
  - dotfiles-T128-process-rules-a01@b08061f7124924fe54c88ec122619459a7d0aeb03e59d0184101f79d24e4f398
verdicts:
  dotfiles-T128-v1-task-schema-contract-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-contract-a01: "revise: C-1 an existing module's live tests must stay live"
  dotfiles-T128-process-rules-a01: "revise: P-1 workflow files make it design tier, P-2 invariant and authorization, P-3 premise 1 output, P-4 rule word budget"
---

# Task-file review: the V1 and V2 contract tasks and the process-rules task (one round, frozen stop condition)

Checked against the four points only: no contradiction with the design at 15daca85, premises hold, allowed_files cover the touch points grep finds, one invariant with the contract-id rule.

## dotfiles-T128-v1-task-schema-contract-a01: ready

1. Design: dormant @contract tests only, after V0, before the implementation, promotion left to the implementation PR; INV-1 byte-identical; the id resolves to dotfiles-T128-v1-task-schema-a01's entry. No contradiction. V0's main-tests does not trigger on this PR (no script path changes), so its design-tier checks do not apply to the contract PR itself, which is consistent.
2. Premise holds: V0 items 1(b) and 1b carry the REGIME_CONTRACT decorator.
3. Touch points: both modules are new on main (test_validate_task.py and test_high_risk_paths.py absent), so nothing else is touched; the 1000-line tests cap bounds them.
4. One invariant.
Worker question INV-4 would produce, answered here: the modules must not import scripts/lib/high_risk_paths.py at module level (it does not exist on main yet, and an ImportError is not a skip); the task's "drive the future script as a subprocess by path and skip with the contract decorator" covers it, and the tier_of tests do the import inside the decorated test.

## dotfiles-T128-v2-audit-schema-and-runner-contract-a01: revise

1. Design and 4: as above for INV-5 and the id rule.
2. Premise holds.
3. C-1: tests/unit/test_agmsg_orchestration_docs.py exists on main with 17 live tests (the rule word budgets, the SKILL and AGENTS.md assertions). The task says to write the named modules "with every test decorated @contract", which read literally makes those 17 tests dormant and removes the regime's own prose checks from CI until V2 promotes them. Say: for a module that exists on main, add the new contract tests only (here the HEADLESS_AUDIT form of line 21) and leave existing tests undecorated; test_audit_head.py is new and is all contracts.

## dotfiles-T128-process-rules-a01: revise

1. P-1: allowed_files include .github/workflows/remote.yaml and test.yaml; under the design, .github/workflows/** is design tier (INV-1's workflow-edit refusal, V1's DESIGN_TIER), so this is not a docs task, kind: docs with security: false contradicts the tier the design derives, and V1's validator as specified fails security: false on a design-tier task. remote.yaml (Snippet install, on pull_request, no changes job) is a real CI change. Split: the three prose files stay a docs task; the two workflow skips go to a design-tier task with security: true.
2. P-2: the invariant line is INV-7 with a sentence that is not the design's (INV-2 requires byte-for-byte), and the design's implementing_tasks has no entry for this task, so under the stop condition's fourth point it names no invariant it implements. A docs task may carry no invariant (the schema requires one only when security is true); drop the placeholder. The workflow half, as design tier, needs an authorization the frozen design does not have: an implementing_tasks entry (a hashed-key change, hence a review pair) or an operator waiver under INV-1, written visibly. That is the operator's call, not a wording fix.
3. P-3 (premise 1): the command as written prints 0 on this host (history.sh ... --limit 600 | grep -c 'task_id=…*AGMSG-RESULT'; the token order in a history row is AGMSG-RESULT v1 task_id=…, so the pattern never matches). The real counts from the whole history are 12 Claude RESULTs and 8 Codex RESULTs on the design-review task (20 in all); restate the command and output. Premise 2 is unverifiable from this seat (gh). The claim's substance, no convergence condition, stands and this seat named it at round 9 and round 11.
4. P-4 (touch point): the rule file home/dot_config/claude/rules/agmsg-orchestration.md is at 447 words against the 450-word budget in tests/unit/test_agmsg_orchestration_docs.py:82; "one sentence" exceeds it unless words are removed. Either trim in the same edit or list the test module. The SKILL step-3 edits fall inside the slice that test's routing assertions read (lines 72, 167); the worker must keep the asserted sentences.
Worker question, answered here: step 6 ("the whole-file form was a bootstrap expedient") is consistent with INV-7's last clause and needs no design change.

## Note on the stop condition

The condition itself is the right one and this receipt applies it; the contract tasks pass it, the process-rules task fails it on tier and authorization, which are design points, not implementation detail.
