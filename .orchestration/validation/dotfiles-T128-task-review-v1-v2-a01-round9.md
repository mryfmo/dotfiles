---
reviewed_at: 2026-10-10T22:46:42Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@015e32530307a3fe65b8f9a328a85ce99a8beda72602f790c6822d17ad34cb30
task: dotfiles-T128-task-review-v1-v2-a01
round: 9
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round8.md
files:
  - dotfiles-T128-v1-task-schema-a01@62fa300dd5325e14ea254ee08f5a4a592d33763cc333b28ea9f83211b9a25027
  - dotfiles-T128-v1b-pr-caps-a01@b1a37d2fd2336d1c153ed0e27642ef07599ee0e9f0edc5563770355c970faeb2
  - dotfiles-T128-v1c-regime-ci-check-a01@e03be9dee6587a533b26a6da135f842f3fa86f9533ebc1ac8b152e2288b3921f
  - dotfiles-T128-v2-audit-schema-and-runner-a01@41d35ff3a6581e04166aab87c0b89cdfb66a7799c2a2088b71356208999ccda0
verdicts:
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 9: the four files after design v9

PyYAML check: each file's invariant equals design v9 byte for byte; all four pointers name the round-9 receipt; the hashes match the TASK.

- V1: the schema gains after (prerequisite task ids) beside supersedes and reset_of (line 44). Ready.
- V1b: pr-caps.sh prints a third figure tests_added with its own cap of 1000 and a breach line (line 31). Ready.
- V1c: pointer only. Ready.
- V2: the fallback runs only when git diff --quiet origin/main <head> -- .claude holds, else exit 2 blocked (line 53); the schema gains the premises map, one entry per premise (line 52). Ready. Note: the test case at line 57 names .claude/skills/ while the runner refuses any .claude/ change; make the test's fixture touch .claude/ outside skills too, so it pins the wider rule. The round-8 item (the runner computes inputs and overwrites a model-supplied value) is slated for v10 and is not in these bytes.

All four will move again with v10 (INV-1 and INV-5 sentences, pointers).
