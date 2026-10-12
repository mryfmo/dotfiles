---
format: 2
task_id: dotfiles-T128-process-rules-redesign-a06
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-rules-redesign-a06 — the reset redesign of a06 (INV-6: the evidence-records row would be amendment 2; the `bookkeeping` class at four)

Drafted 2026-10-12 01:13Z by the orchestrator seat. `dotfiles-T128-process-rules-a06` (PR #318, worker `claude-standard-dot-a003`, head `f755d714`, CI green, no content change pending) drew Bot P1 4243975211 on its task copy: the `threat_table` has no row for the PR-controlled evidence records under `.orchestration/dotfiles-T128-process-rules-a0*/` (report, validation, sandbox, learning, autoskill, revise.yaml) that acceptance and the audit read. a06 counters: amendments 1, revises 1, Bot P1 heads after the first RESULT 1; the row would be amendment 2, INV-6's threshold, so a06 resets to a07 by this task. It is the fourth finding of the class `bookkeeping` (a task-file field left behind by a change elsewhere): the pre-dispatch check `task-consistency-check.py` covered `tests/` paths only; it now requires a threat-table row naming every `allowed_files` entry (C4) and the design's current receipt (C6), and a07 passes it before dispatch.

## What to produce

The complete text of `dotfiles-T128-process-rules-a07.md`: the a06 file at sha256 `90fb32c26f4b1f70aebf44e7cee898e75dd7e273304def9bfaa2d7dff165f9aa` (`.orchestration/tasks/dotfiles-T128-process-rules-a06.md`) with exactly these changes:

1. `task_id: dotfiles-T128-process-rules-a07`; `reset_of` gains `dotfiles-T128-process-rules-a06`; `allowed_files` names `.orchestration/dotfiles-T128-process-rules-a07/**` in place of the a06 entry; the copies row adds `-a07/task.md` and its residual names the a07 file's hash.
2. `design_review.receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md` (the design's current receipt, as the design file's own front matter names it; round 16 accepted an earlier hash).
3. The SKILL row names its path: `control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md, the rules Claude seats follow once it is applied` (disposition unchanged).
4. A sixth row, after the fixtures row: `control: the branch evidence records under .orchestration/dotfiles-T128-process-rules-a07/ and the a01 to a06 directories (report.md, validation.md, sandbox.md, learning.md, autoskill.md, revise.yaml), which acceptance and the task-level audit read`; `disposition: "residual: they are the worker's untrusted claims; acceptance re-checks each claim against the diff, CI and GitHub, the counters, the sweep and the audit read those sources themselves, and the masked main-checkout copies are acceptance's copy"` (thread 4243975211's remedy, the worker's wording).
5. One sentence in the introduction: "The threat table names every `allowed_files` entry, which bounds what the PR controls (INV-12 fails any other change); `task-consistency-check.py` C1 to C6 pass on this file." The title names a07 and this reset; the "History" paragraph gains a06's reset in one sentence.
6. First commit and Completion: from `f755d714`, copy this file byte-identical to `.orchestration/dotfiles-T128-process-rules-a07/task.md` (the a01 to a06 directories stay), one commit for the copy and the evidence, no content change, CI, Bot wait under the cap, `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-a07 … reset_of=…,dotfiles-T128-process-rules-a06` listing 4243975211 as `fixed:<that sha>` and every earlier thread as before.
7. Nothing else changes. Before sending, run `uv run --no-project --with pyyaml python /private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad/task-consistency-check.py <a scratch copy of the block>` from the repository root (it reads the design file's receipt) and paste its `OK` line in the receipt; a `FAIL` line is fixed before sending.

## Output

`.orchestration/validation/dotfiles-T128-process-rules-redesign-a06.md` with the usual header and the whole a07 file in one non-empty four-backtick block (plain scalars with a colon-space quoted; `wc -l`, a YAML parse and the checker's `OK` before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a06 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a07_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file, runs the checker again and asks for the one confirmation (`verdict=accept design_sha256=<hash>`, the reset anchor; the record's `redesign_source` is this task id). max_turns=3. Forbidden: editing tracked files; branches; PRs.
