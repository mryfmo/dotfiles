---
reviewed_at: 2026-10-11T05:13:39Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-task-review-a02-a01
round: 1
files:
  - dotfiles-T128-process-rules-a02@85e2a1924d93961e011925901e530d8aca4509a137895aea6f581f152b7923aa
verdicts:
  dotfiles-T128-process-rules-a02: "revise: 1 premise 2's command reads the database directly; 2 redesign_source is not a schema key and reset_of is a string"
---

# Task-file review: dotfiles-T128-process-rules-a02 (the reset continuation of PR 318), one round

Stop condition against design v16 at 15957fbc.

1. The three fenced blocks (the SKILL bullet, the AGENTS.md second bullet, the two tests) are byte-identical to the redesign receipt's three blocks (1139, 638 and 929 bytes each), checked programmatically.
2. No contradiction with v16: review tier by INV-1's rule-prose list with kind: docs and no invariant (no map entry), the reset record names message 431 and the receipt hash b95b4eac, the worker and PR continue, a Bot finding on the payload wording is reported rather than fixed (the class the reset closed) and dispositioned by the orchestrator, which the gate permits for a sweep item with a reason.
3. allowed_files complete: the SKILL, AGENTS.md and the docs test module, the three files the receipt names.
4. Premises. Premise 1 (gh) is unverifiable from this seat; its output lists the three threads the reset record names plus the first revise round's ids, consistent with the acceptance record. Premise 3 holds: the receipt hashes to b95b4eacb3b7ef3f8cc8f0da438062e4a794a1e96139268b9cecc6b4df0b40e4 on this seat. Premise 2: holds by history.sh (claude-review-dot-a001 → claude-deep-dot: AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules…): the RESULT is from claude-review-dot-a001, not the author; note that the premise's own command reads the agmsg database with sqlite3 directly, which the agmsg skill forbids, so the command to keep is history.sh dotfiles-conformance "" <limit> filtered by the task id.
5. Items to apply before dispatch, both outside the fenced blocks:
   - R1: replace premise 2's sqlite3 command with the history.sh form and paste that command's raw output.
   - R2: the front matter carries redesign_source (not a key in V1's schema, whose additionalProperties is false) and reset_of as a string where V1's schema declares an array of task ids. Either drop redesign_source here (the reset record already names it) and write reset_of as a one-item list, or add both shapes to the V1 note in plan 006 Phase B beside threat_table; the first is one edit to this file.

Verdict ready once R1 and R2 are applied; neither touches the relayed text.
