# Orchestration task: Plan 002

## Objective

Implement the second revision of `plans/002-make-review-evidence-non-vacuous.md`
on top of Plan 001. The first attempt proved comments JSON `null` is ambiguous;
the rejected intermediate design attempted false local attestation. Implement
only the final minimal non-empty resolved-comments contract.

## Allowed implementation files

- `scripts/require-crit-review.py`
- `tests/unit/test_require_crit_review.py`
- `AGENTS.md` and `README.md` only for the evidence command and trust-boundary documentation
- `tests/install/common/lifecycle.bats` only if its static documentation assertion must follow the corrected command
- `home/dot_config/codex/AGENTS.md` and `home/dot_config/claude/rules/crit-review.md` for the deployed evidence command and trust-boundary wording

## Forbidden actions

- Do not edit any other implementation file.
- Do not weaken repo-local path, reviewer, explicit-disable, or unresolved-comment checks.
- Do not use browser Crit, push, merge, open a PR, or run Bats locally.
- Do not add raw-review copying, target digests, or authenticity claims.

## Required validations

- Focused review-guard unittest module.
- `make unit-test`.
- Python compile check.
- Isolated negative checks for null/list/unrelated/mismatched evidence.
- Positive non-empty resolved review/line comment fixtures.
- Adversarial null, empty, malformed, unresolved, and agent-as-user fixtures.

## Expected artifacts

- Report: `/Users/mryfmo/Workspace/dotfiles/.orchestration/reports/plan-002.md`
- Validation: `/Users/mryfmo/Workspace/dotfiles/.orchestration/validation/plan-002.md`
- Sandbox: `/Users/mryfmo/Workspace/dotfiles/.orchestration/sandboxes/plan-002.md`
- Learning: `/Users/mryfmo/Workspace/dotfiles/.orchestration/learning/plan-002.md`
- AutoSkill: `/Users/mryfmo/Workspace/dotfiles/.orchestration/autoskill/runs/plan-002.md`

## Completion

- If complete, commit only allowed implementation files.
- If stopped, make no speculative implementation commit and report the exact
  missing Crit fields/output that triggered the STOP condition.
