---
format: 2
reset_of: dotfiles-T128-process-rules-a01
redesign_task: dotfiles-T128-process-rules-a03
design_sha256: 867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
redesign_task_reviews: "two one-round task-file reviews by claude-review-dot-a001 (05:13Z the relay, 05:19Z items 4 and 5); the anchor the boundary probe reads is that identity's AGMSG-RESULT verdict=accept design_sha256=0a31acb4… (round 3 confirmation); dispatched 05:21Z"
redesign_source: dotfiles-T128-process-rules-redesign-a02
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
redesign_result: "agmsg message 431 (claude-review-dot-a001 → claude-deep-dot, 2026-10-11T05:10:11Z), receipt .orchestration/validation/dotfiles-T128-process-rules-redesign-a01.md sha256 b95b4eacb3b7ef3f8cc8f0da438062e4a794a1e96139268b9cecc6b4df0b40e4"
reason: "plan 006 S1 and design INV-6 on PR 318: the same finding class three times (a disposition grammar stated in prose accepts a vacuous payload: threads 4240290387 on 9a46c3c4, 4240321113 on ac3794f9, 4240334094 on 6635030f) and Codex Bot P1 on two heads after the first RESULT 9a46c3c4"
---

# Design reset: dotfiles-T128-process-rules-a01 (PR #318), 2026-10-11

- **What stops:** the threat-table rule text of `dotfiles-T128-process-rules-a01` as written on PR #318 (`home/dot_agents/skills/agmsg-orchestration/SKILL.md`, "Review and integration invariants", the `threat_table` bullet, and its fix-by-fix descendants). The PR, branch and worker continue: the reset replaces the rule's specification, not the task's other content (A1 items 1, 2, 3, 5; A2; A4 are untouched by the findings).
- **Why a reset and not a third fix:** three Bot rounds found three vacuous payloads the prose regex admitted (empty, `residual: none`, `out-of-scope: none`); the next round would find the fourth. The specification was wrong: prose cannot close a grammar. The operator's rule (2026-10-10/11) and plan 006 S1 forbid continuing finding by finding.
- **Redesign:** written by the review seat under `dotfiles-T128-process-rules-redesign-a01`: the prose names the three disposition forms and what each carries, states the three shape rules V1's `schemas/task.json` implements, and leaves substance to the task-file reviewer, the Bot and the auditor. Its RESULT (identity `claude-review-dot-a001`, not the author) is the anchor INV-6 names; the redesign text is relayed verbatim as `dotfiles-T128-process-rules-a02` to the same worker on the same PR, whose first commit copies that task file to `.orchestration/dotfiles-T128-process-rules-a02/task.md`.
- **Counts carried into the acceptance record of the reset task:** PR #318 Bot-reviewed heads before the reset: `f7c229ff`, `ddadd5c9`, `9a46c3c4`, `ac3794f9`, `6635030f`, `aeb6c5ad` (Bot P1 on three heads after the first RESULT); revises 1; amendments 0; questions 0. The third round on `aeb6c5ad` left two P1 threads of other classes (4240348412 history limit, 4240348414 open-thread integration outcome); a02 folds them in with one check each.
- **Waiver:** none (`DESIGN_RESET_WAIVED_BY` absent).
- **Anchor moved (2026-10-11 07:43Z, Bot P1 4240720572 on boundary PR #321):** a02 was amended (its file moved from `0a31acb4…` to `b6500dbf…`, accepted by no foreign RESULT) and then reset itself; the surviving redesign of a01's rule is a03 (`867ea4ca…`, `reset_of: [a01, a02]`, accepted by `claude-review-dot-a001` in RESULT 476 `verdict=accept design_sha256=867ea4ca…`), so this record's `redesign_task` and `design_sha256` now name a03. The chain a01 → a02 → a03 is in `…-a02-design-reset.md`.
- **redesign_source corrected (09:15Z, review seat round 8 note):** the surviving redesign a03 was produced and accepted (RESULT 476, `verdict=accept design_sha256=867ea4ca…`) under task id `dotfiles-T128-process-rules-redesign-a02`; the probe binds the accepting RESULT's task_id to this field, so it names redesign-a02 (redesign-a01 produced the a02 text that was itself reset).
