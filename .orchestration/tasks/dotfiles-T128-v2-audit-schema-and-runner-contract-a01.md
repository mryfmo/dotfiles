---
format: 2
task_id: dotfiles-T128-v2-audit-schema-and-runner-contract-a01
superseded_by: dotfiles-T128-v2-audit-schema-and-runner-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round15.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - tests/unit/test_audit_head.py
  - tests/unit/test_agmsg_orchestration_docs.py
invariants:
  INV-5: "the task-level audit is a headless read-only run whose instruction root is the trusted main checkout and whose schema is main's schemas/audit.json: codex exec --output-schema <main>/schemas/audit.json -C <main> with the detached worktree at the head added as a read-only data directory (--add-dir), so the audited PR controls neither the schema nor the AGENTS.md the auditor reads; the fallback claude -p --json-schema from the same root with --add-dir <worktree>, --bare when an API key is set and otherwise with project and user hooks disabled, and refused with exit 2 blocked when the head changes any file under .claude/ (bare mode loads skills from an --add-dir directory's .claude/skills/), leaving such a head to the codex path), with at most one valid audit per head (a stale input manifest invalidates an audit and a new audit of the same head replaces it), pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file and amendments, the acceptance record as it stands when present (its text above the line <!-- audit-input-boundary --> is the pre-audit part; dispositions of this audit's findings are appended below it), the head's pr-feedback JSON and the previous round's audit JSON; the audit JSON carries an input manifest (path to sha256 of every input as read, computed by the runner, which overwrites any model-supplied value) and the gate recomputes the manifest at gate time, so a pre-audit input edited after the audit makes the audit stale and a new audit is required; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
after:
  - dotfiles-T128-v0-main-tests-a01
premises:
  - claim: "a contract PR ships only dormant @contract tests (tests/unit/regime_contract.py from V0), which skip in ordinary CI, so it merges before the implementation and main-tests activates them against the implementation PR"
    command: "grep -n 'REGIME_CONTRACT' .orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md | head -2"
    output: "V0 items 1(b) and 1b: contract = unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')"
---

# AGMSG-TASK dotfiles-T128-v2-audit-schema-and-runner-contract-a01 — contract PR for dotfiles-T128-v2-audit-schema-and-runner-a01 (dormant tests only)

DRAFT; dispatched after V0 merges, before `dotfiles-T128-v2-audit-schema-and-runner-a01`. Design tier (the implementing wave is design tier). Claude seat, `.claude/worktrees/worker-f`, branch `feat/audit-runner-contract` from `origin/main`.

Write the new module the implementing task names (`tests/unit/test_audit_head.py`) with every test decorated `@contract`; in the existing `tests/unit/test_agmsg_orchestration_docs.py` keep its 17 live tests untouched and add only the dormant `@contract` test for the new `HEADLESS_AUDIT` form (from `tests/unit/regime_contract.py`), one test per rule of the implementing task's "What to build" and "Tests" sections, each written so that it fails when its rule is removed; the modules import nothing that does not exist on `main` yet (drive the future script as a subprocess by path and skip with the contract decorator). Nothing else changes. The implementation PR that follows removes the decorators (promotion) as V0's main-tests requires.

Validation: the new module collects under `make unit-test` with every test skipped (`dormant contract`) and the existing module's 17 tests still pass live and run under `REGIME_CONTRACT=1` with every test failing (the script does not exist yet; paste both outputs). First commit: this task file byte-identical to `.orchestration/dotfiles-T128-v2-audit-schema-and-runner-contract-a01/task.md`; evidence beside it. Completion: draft PR within 30 minutes (`test(regime): dormant contract tests for v2-audit-schema-and-runner-a01`), CI, Bot wait, artifacts, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=6. Forbidden: any file outside allowed_files; `make update`; thread resolution.
