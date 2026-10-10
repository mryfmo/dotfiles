---
reviewed_at: 2026-10-10T23:49:29Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 19
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round18.md
files:
  - dotfiles-T128-v0-main-tests-a01@af61f64b6716fc54 (prefix; full hash in the TASK line)
  - dotfiles-T128-v1b-pr-caps-a01@29dd97048b3a9b68
  - dotfiles-T128-v1c-regime-ci-check-a01@9d37d74d178d354b
verdicts:
  dotfiles-T128-v0-main-tests-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
---

# Task-file review round 19: R18-1 across V0, V1b, V1c

Design unchanged at 15daca85; invariants byte-identical; pointers at round 13.

R18-1 applied: V0 adds tests/unit/test_contract_markers.py (named twice, in allowed_files and for the ast cases), V1b adds tests/unit/test_regime_check.py, V1c adds tests/unit/test_validate_task.py. A simulation of V0's step (b0) over all five task files (trigger prefixes, data suffixes excluded, module = test_<name>.py with executable_ stripped and dashes to underscores) finds no declared non-data script without its declared module in V0, V1, V1b, V1c or V2.

The five task files are final at v0 af61f64b, v1 aa5f3be9, v1b 29dd9704, v1c 9d37d74d, v2 9b7828fb.
