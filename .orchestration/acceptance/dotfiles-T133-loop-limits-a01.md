---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-loop-limits-a01"
}
---

# Acceptance record: dotfiles-T133-loop-limits-a01

Mechanism task (proposal 2 of 2026-10-19 20:2x JST; M-20261019-05): the loop limits that ran as manual procedure become tools: regime-counters.sh counts text reviews and S1 per family (C-87, C-93), acceptance-front-matter.py refuses a class outside the vocabulary (C-93), dispatch.sh refuses a revise line without selectors (C-91) and a fourth text review without a newer re-plan line (C-92), task-consumers.py enumerates the consumers of a rendered form (C-89). Sibling of plan 024 P1-6 (which keeps --from-result and --next). Text designed by the review-profile context with probed premises (`.agents/worklog/orchestrator-glue/redesign/loop-limits-a01.md`, prompt `p16-a01-design-prompt.md`); security: true; after: []; a Codex seat (D-024-25) when one frees (a012 after P1-12, or a010 after P1-15).

- 2026-10-19T11:42Z: design installed (237 lines, 8 allowed_files; the vocabulary file removed from allowed_files per C2: the orchestrator owns its content); checker OK; C-80 first review started.
- 2026-10-19T11:46:31Z: C-80 first review (newest `…-text-security-*.md`): `Verdict: incorrect`: P1 the uv launch omits `--isolated`; P1 an agmsg hardening "prerequisite" claimed as authentication of the installed dispatch chain; P2 the text required edits to the vocabulary file, which C2 keeps out of allowed_files (the family keys are the orchestrator's record). Round 2 by the review-profile context with all findings (prompt `loop-limits-a01r2-redesign-prompt.md`).
text-security:loop-limits-r1:1	interpreter-isolation
text-security:loop-limits-r1:2	installation-binding
text-security:loop-limits-r1:3	record-in-allowed-files
- 2026-10-19T11:53Z: round-2 text (`loop-limits-a01r2.md`, 235 lines, 8 allowed_files) installed: `--isolated` on every uv launch, no agmsg prerequisite claim (the installed agmsg route stays the owner's residual), the vocabulary read only (family keys are the orchestrator's record; a class without one is its own family); checker OK; C-80 round 2 started.
- 2026-10-19T11:56:50Z: C-80 second review (newest `…-text-security-*.md`): `Verdict: incorrect` on three P2: the review launcher (orchestrator glue, outside the repository) bypasses the dispatch guard; the message task_id is not bound to the file front matter and hash; the re-plan freshness renews no budget. Decision: round 3 (the last under C-92) by the review-profile context (prompt `loop-limits-a01r3-redesign-prompt.md`): the launcher moves into the repository under the same budget rule, task_id/sha binding at dispatch, the budget counted from the newest re-plan line.
text-security:loop-limits-r2:1	guard-bypass-launcher
text-security:loop-limits-r2:2	message-file-binding
text-security:loop-limits-r2:3	budget-renewal
- 2026-10-19T12:06Z: round-3 text (`loop-limits-a01r3.md`, 249 lines, 10 allowed_files) installed: the review launcher moves into the repository under the same budget rule, dispatch.sh binds the message task_id and sha to the file, the budget counts verdicts newer than the newest re-plan line and renews with each re-plan; checker OK; C-80 round 3 (the last under C-92) started.
- 2026-10-19T12:09:14Z: C-80 third review (newest `…-text-security-*.md`): `Verdict: incorrect` on one P2: the review launcher moved into the repository needs an absolute Codex binding, which no provider supplies (the resolver resolves Python only) and a PATH-selected fake codex in the test contradicts the binding rule. Third incorrect verdict: C-92 applies, no fourth delta round.
re-plan: review-launcher-binding (rows text-security:loop-limits-r2:1, text-security:loop-limits-r3:1) — specification: the text pulled the review launcher (a Codex-executing program) into a task about counters and refusals, so it inherited the executable-binding family; design: the budget rule lives in one repository helper (`scripts/orchestrator/review_budget.py`: verdict files newer than the newest re-plan line, three per budget) that dispatch.sh calls and that the orchestrator glue launcher calls before starting Codex, while the launcher itself and its Codex binding stay with the executable-binding family (trusted-entrypoint-binding-a01 names it as a later consumer); implementation: the round-4 text drops scripts/orchestrator/text-security-review.sh and its test from allowed_files, adds the helper and its test, and keeps the other items; verification: the helper's four budget tests plus a dispatch.sh refusal test; the glue launcher is edited by the orchestrator (glue exemption) to call the helper once it merges.
text-security:loop-limits-r3:1	executable-binding
- 2026-10-19T12:16Z: re-planned text (`loop-limits-a01r4.md`, 247 lines, 10 allowed_files: review_budget.py + its test in, the launcher out) installed; checker OK; C-80 round 4 (first after the re-plan) started.
