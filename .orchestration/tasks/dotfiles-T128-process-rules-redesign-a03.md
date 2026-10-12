---
format: 2
task_id: dotfiles-T128-process-rules-redesign-a03
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-rules-redesign-a03 — the reset redesign of a03 (INV-6: two Bot P1 heads after the RESULT)

Drafted 2026-10-11 22:4xZ by the orchestrator seat. `dotfiles-T128-process-rules-a03` (PR #318, worker `claude-standard-dot-a003`) reached INV-6's Bot threshold during its revise round 1: Codex Bot P1 on two heads after the a03 RESULT `b9a9da7d` (`386f97ff`: 4243516879, fixed in `114d5b91`; `781e6ef8`: 4243537279 and 4243537281). Both of the latter are contradictions between rule sentences the orchestrator's task text wrote and the hashed design: (1) "the orchestrator revises once per pair of results … after at most three revision rounds the design is frozen" freezes an unreviewed hash, against INV-7 (both receipts name the hash that is frozen); (2) "a boundary PR … is never a prerequisite of a dispatch" contradicts INV-2 (the design must be on `main` before the implementing TASK is dispatched), a correction plan 006 already made at 07:25Z but the SKILL sentence did not. The rule's path is a reset; you write the successor. Read-only.

## What to produce

The complete text of `dotfiles-T128-process-rules-a04.md`: the a03 file at sha256 `867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d` (`.orchestration/tasks/dotfiles-T128-process-rules-a03.md`) with exactly these changes:

1. `task_id: dotfiles-T128-process-rules-a04`; `reset_of: [dotfiles-T128-process-rules-a01, dotfiles-T128-process-rules-a02, dotfiles-T128-process-rules-a03]`.
2. A1 item 1 (the design-review protocol): the third revision round is the last; the design is frozen at the hash the pair last accepted, so a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7). State the sentence the SKILL bullet carries and its docs-test token.
3. A1 item 3 (boundary PRs): a boundary PR carries no task draft under review; a design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition. State the sentence and its token (the old token "is never a prerequisite of a dispatch" goes).
4. The a03 revise round's three fixes stay (closed-selector existence at acceptance; the Codex-Bot login filter in step 15; the four pinned sentences), as does everything else of a03; the worker continues from its current head `781e6ef8` on the same branch and PR with one commit for the two sentences and their tokens, after copying this file byte-identical to `.orchestration/dotfiles-T128-process-rules-a04/task.md` (the a01, a02 and a03 directories stay).
5. The "History" paragraph gains a03's reset in one or two sentences.

## Output

`.orchestration/validation/dotfiles-T128-process-rules-redesign-a03.md` with the usual header and the whole a04 file in one non-empty four-backtick block (plain scalars with a colon-space quoted; `wc -l` and a YAML parse before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a03 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a04_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file and asks for the one confirmation (`verdict=accept design_sha256=<hash>`, the reset anchor; the record's `redesign_source` is this task id). max_turns=3. Forbidden: editing tracked files; branches; PRs.
