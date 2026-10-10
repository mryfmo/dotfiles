---
reviewed_at: 2026-10-10T23:01:10Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 13
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round12.md
files:
  - dotfiles-T128-v0-main-tests-a01@3bbf8b1d7c666953 (prefix; full hash in the TASK line)
  - dotfiles-T128-v1-task-schema-a01@ff9e66c38e2a78d7
  - dotfiles-T128-v1b-pr-caps-a01@b9195a0632a38c96
  - dotfiles-T128-v1c-regime-ci-check-a01@1a498ec0545094cc
  - dotfiles-T128-v2-audit-schema-and-runner-a01@2a9639aaffcfee74
verdicts:
  dotfiles-T128-v0-main-tests-a01: "ready"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 13: V0 rewritten, the four others as a diff

PyYAML check: each file's invariant equals design v13 byte for byte; all five pointers name the round-13 receipt; the hashes match the TASK.

## V0

R11-1 (git archive HEAD copy with main's tests/unit overlaid, item 1), R11-2 (declared modules from the task's tests/unit entries, every other main module in the undeclared mode, item 1), R11-3 (task.md read with PyYAML; the implementation PR removes the decorator, items 1b and 4), the promotion check 1(c) with its test (b3), and the ROOT premise (34 of 34 modules) are all in these bytes. The undeclared mode runs main's modules as they are against the overlaid copy, so a script with no module of its own is still covered by every other module; the declared mode fails a design-tier task whose module has no contract on main; the promotion check reads the PR's own copy from HEAD, not the overlay, which is the right file. Premise 1 remains unverifiable from this seat (its gh api half); premises 2 and 3 hold (the ROOT count is 34 of 34, re-run in round 11).

## V1, V1b, V1c, V2

Pointer and INV sentence only; ready.
