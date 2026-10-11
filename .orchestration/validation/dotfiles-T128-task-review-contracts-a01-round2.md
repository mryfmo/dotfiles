---
reviewed_at: 2026-10-11T00:16:13Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-contracts-a01
round: 2
previous: .orchestration/validation/dotfiles-T128-task-review-contracts-a01.md
files:
  - dotfiles-T128-v2-audit-schema-and-runner-contract-a01@327e8653c354b1ce (prefix; full hash in the TASK line)
  - dotfiles-T128-process-rules-a01@7a2bc9ecc57e17b5
verdicts:
  dotfiles-T128-v2-audit-schema-and-runner-contract-a01: ready
  dotfiles-T128-process-rules-a01: "revise: P-2b a docs task with no map entry carries no invariant, P-3 output 20 not 21"
---

# Task-file review round 2: V2-contract and process-rules after round 1

Design unchanged at 15daca85.

## V2-contract: ready

C-1 applied: the new test_audit_head.py is all contracts; the existing test_agmsg_orchestration_docs.py keeps its 17 live tests untouched and gains only the dormant contract for the new HEADLESS_AUDIT form; validation requires the 17 to still pass live. INV-5 byte-identical.

## process-rules: revise

- P-1 applied: allowed_files are the SKILL and AGENTS.md; the workflow half is recorded as deferred to the next design amendment with no waiver (item 5). P-4 applied: the rule file is not edited, item 4 moved to the SKILL, and the docs test is named in validation.
- P-2b: the task still carries INV-7, now verbatim, but the design's implementing_tasks has no entry for dotfiles-T128-process-rules-a01. INV-2 compares the task.md's invariant ids with the map entry for its id as a set; with no entry the set is empty, so an empty invariants map passes and a map naming INV-7 fails closed. The task implements no invariant (its own line 27 says so), it is docs tier with security: false, and the schema requires an invariant only when security is true. Remove the invariants key. The stop condition's fourth point then reads: a task names the invariant it implements, or none when the map has none for it.
- Premise 1's corrected command prints 20 on this host, not 21 (by sender: 12 Claude, 8 Codex); restate the output to what the command prints.
