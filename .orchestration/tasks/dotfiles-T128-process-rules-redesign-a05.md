---
format: 2
task_id: dotfiles-T128-process-rules-redesign-a05
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-rules-redesign-a05 — the reset redesign of a05 (INV-6: questions 2; the second amendment would be the threat-table row the Bot found missing)

Drafted 2026-10-12 00:36Z by the orchestrator seat. `dotfiles-T128-process-rules-a05` (PR #318, worker `claude-standard-dot-a003`, head `be0afe7e`, the revise-round commit for item 10 already pushed) reached INV-6: two `AGMSG-PONG status=question` (603 and 621), and the Bot's P1 4243885108 on `be0afe7e` (the a05 `threat_table` has no row for `tests/fixtures/regime/*.md`, the expected half of the whole-section oracle item 10 introduced) would be amendment 2. The missing row is the orchestrator's omission when writing item 10 (A7's text got the same row at 00:27Z; a05's did not). The rule's path is a reset by another context: this task.

## What to produce

The complete text of `dotfiles-T128-process-rules-a06.md`: the a05 file at sha256 `71ca5df01db48361a5c6ea140faebeede70fa0fb41f00f78d280bd9ba13024fe` (`.orchestration/tasks/dotfiles-T128-process-rules-a05.md`) with exactly these changes:

1. `task_id: dotfiles-T128-process-rules-a06`; `reset_of` gains `dotfiles-T128-process-rules-a05`.
2. A fifth `threat_table` row, after the test-module row: `control: the PR edits tests/fixtures/regime/*.md, the expected values of test_regime_rule_sections_are_pinned_whole, so a rule and its fixture can change together`; `disposition: "residual: a fixture diff is the declared change itself (the test's message requires listing it in the RESULT, INV-12); the orchestrator's diff review and the task-level audit from main read each fixture diff beside the prose diff, and main keeps the previous fixture to compare against"` (the Bot's own remedy on thread 4243885108, quoted a colon-space safe).
3. The title and introduction name a06 and this reset; the "History" paragraph gains a05's reset in one sentence (INV-6 questions, the missing oracle row).
4. First commit and Completion: from `be0afe7e` (item 10's fixtures and test are on the branch), copy this file byte-identical to `.orchestration/dotfiles-T128-process-rules-a06/task.md` (the a01 to a05 directories stay), one commit for the copy and the evidence, CI, Bot wait under the cap, `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-a06 … reset_of=…,dotfiles-T128-process-rules-a05` listing thread 4243885108 as `fixed:<that sha>` and every earlier thread as before.
5. Nothing else changes (items 1 to 10, the other rows, Validation).

## Output

`.orchestration/validation/dotfiles-T128-process-rules-redesign-a05.md` with the usual header and the whole a06 file in one non-empty four-backtick block (plain scalars with a colon-space quoted; `wc -l` and a YAML parse before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a05 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a06_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file and asks for the one confirmation (`verdict=accept design_sha256=<hash>`, the reset anchor; the record's `redesign_source` is this task id). max_turns=3. Forbidden: editing tracked files; branches; PRs.
