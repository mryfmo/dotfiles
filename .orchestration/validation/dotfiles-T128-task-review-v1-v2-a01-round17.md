---
reviewed_at: 2026-10-10T23:33:05Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 17
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round16.md
files:
  - dotfiles-T128-v0-main-tests-a01@94ef3320252fce53 (prefix; full hash in the TASK line)
verdicts:
  dotfiles-T128-v0-main-tests-a01: ready
---

# Task-file review round 17: R16-1 in V0

Design unchanged at 15daca85; INV-12 byte-identical; pointer at round 13.

R16-1 applied: step (b0) (line 36) fails a design-tier task.md only when allowed_files declares at least one script path that is not a data file (*.txt, *.json, *.md, *.yaml named as data) and no tests/unit/*.py module, with the message "design task declares scripts but no contract module"; test (f) matches. V1's own task (three script paths, one data file, one module) now passes it, as do V1c, V1b and V2.

V0 is ready; the five task files are final at v0 94ef3320, v1 e5474a80, v1b b30aa981, v1c 39451055, v2 4e7cc503.
