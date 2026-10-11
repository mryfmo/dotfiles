---
reviewed_at: 2026-10-10T22:57:40Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@35b48cc3a2f2df31fa75b8a54012ffe62efeedbddb8e875844f461822f8323a1
task: dotfiles-T128-task-review-v1-v2-a01
round: 12
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round11.md
files:
  - dotfiles-T128-v0-main-tests-a01@06fad5f5fe8fa76627bc319d043f265902a3d1b0e40bac7f0a0ff04a04068856
  - dotfiles-T128-v1-task-schema-a01@50df8996864e51e4ac4558923afdfee98a5eb7f0507c117b22858421e411afd9
  - dotfiles-T128-v1b-pr-caps-a01@762f5756f8bf63e55ce05eab8992eca1a025575f3a86ec768ce3ae56d944c855
  - dotfiles-T128-v1c-regime-ci-check-a01@39451055891c0b924a9d94631ddce12322f9d79a179928152f220d9e7e04d566
  - dotfiles-T128-v2-audit-schema-and-runner-a01@6d37fec75ec0d86e4fd88ce0a109a64c7e64e4ea9f2bc447355c2132d2d73922
verdicts:
  dotfiles-T128-v0-main-tests-a01: "revise: R11-1 root resolution, R11-2 module selection, R11-3 PyYAML for task.md (R11-3's decorator removal is in)"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 12: V0's two new sentences, pointers for the rest

PyYAML check: each file's invariant equals design v12 byte for byte; all five pointers name the round-12 receipt; the hashes match the TASK.

- V0: INV-12 v12 verbatim; item 1b and item 4 now say the implementation PR removes the decorator from the contracts it satisfies, and the empty-contract failure follows the invariant. The three round-11 items that remain in these bytes, by the orchestrator's own acceptance note (to land after this result): item 1 still extracts main's tests/unit into <tmp> and runs them there, although every module resolves the repository root from its own path (R11-1: overlay main's tests/unit on a copy or detached worktree of the PR tree and run from there); item 1 still maps a script to tests/unit/test_<stem>.py (R11-2: select declared modules from allowed_files entries under tests/unit/ and run every other main module in the undeclared mode); item 1 still reads allowed_files from task.md without naming PyYAML (R11-3). One diff check after those land.
- V1, V1b, V1c, V2: pointer only; ready.
