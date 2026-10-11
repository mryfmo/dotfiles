---
reviewed_at: 2026-10-10T23:17:50Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 15
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round14.md
files:
  - dotfiles-T128-v0-main-tests-a01@8cc88e110d3c4872 (prefix; full hash in the TASK line)
  - dotfiles-T128-v2-audit-schema-and-runner-a01@4e7cc503339de724
verdicts:
  dotfiles-T128-v0-main-tests-a01: "ready"
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 15: R14-1 and the V2 notes

Design unchanged at 15daca85; both invariants byte-identical; pointers at round 13, which is right while the design does not move.

- V0, R14-1 applied: item 1(b) takes the tier from the task.md's stamped tier: key, which V1 later validates against the derived tier, and treats a missing stamp as design, so V0 needs neither high_risk_paths.py nor --print-tier before V1 exists. The helper scripts/lib/contract_markers.py the Round-15 section allows is named in V0 (2 mentions), so the ast walk has a home outside the shell script.
- V2 notes applied: the premises keys are stated as JSON object keys, the strings "1".."N" (item 2, line 53); the "under 120 lines" figure is gone, leaving the PR cap as the bound.
