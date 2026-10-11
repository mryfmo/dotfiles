---
format: 2
task_id: dotfiles-T128-regime-counters-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-regime-counters-redesign-a01 — the reset redesign of A3 (INV-6: the second round)

Drafted 2026-10-11 06:5xZ by the orchestrator seat. `dotfiles-T128-regime-counters-a01` (PR #319, worker `claude-standard-dot-a004`) has two RESULTs (the first at `324652e0`, amendment 1's at `72764f05`), so revises=1 and amendments=1 under INV-6; the audit of `72764f05` (`.orchestration/validation/dotfiles-T128-regime-counters-a01-audit-72764f0.md.last.md`) found two P1s and one P2, and any further round reaches a threshold. The rule's path is a reset: you write the successor task; this is read-only.

## What to produce

The complete text of `dotfiles-T128-regime-counters-a02.md`: the a01 file at sha256 `d9a44b7eece0871217fb5a7871ad3088a92fd27b3668bc1de88ccf35506151c1` (`.orchestration/tasks/dotfiles-T128-regime-counters-a01.md`) with exactly these changes:

1. `task_id: dotfiles-T128-regime-counters-a02`; add `reset_of: [dotfiles-T128-regime-counters-a01]` after `after: []`.
2. Threat table: row 5 ("a worker sends extra RESULTs or PONGs") gains the clause that a status or verdict is read from the first `status=`/`verdict=` token, never from free text (`has()` anywhere in the body is the audit's P1), with a test whose PONG note mentions `status=question` and whose RESULT note mentions `verdict=accept`; a new row "a reset record names an unrelated, already accepted design" → `closed:` the redesign task file's own `reset_of` list must name the task being reset, else the record anchors nothing; test with an unrelated accepted design.
3. A new row "the PR's fixtures count against INV-2's 1000-line test cap" → `closed:` `tests/fixtures/regime-counters/*` hold only the rows and fields the tests read (PR 313: the P0/P1 top-level comments and the commits; message TSVs cut to the task's rows), so `git diff --numstat origin/main -- tests/` adds at most 1000 lines; test: none (the acceptance measures it); state the current figures (697 + 1038).
4. "What to build" items 1 and 2 and the Validation list updated to match (first-token reads; the `reset_of` binding in the boundary probe; the fixture budget in the validation, pasted from `git diff --numstat`).
5. A "History" paragraph: a01's amendment 1 (PR-less anchor; premises corrected to the fixtures' figures) and this reset (audit P1s: token matching, reset binding; P2: the test-line cap), two or three sentences; the worker's first commit of a02 copies the file byte-identical to `.orchestration/dotfiles-T128-regime-counters-a02/task.md` (the a01 directory stays as history), same branch `feat/regime-counters` and PR #319 from head `72764f05`.

## Output

`.orchestration/validation/dotfiles-T128-regime-counters-redesign-a01.md` with the usual header and the whole a02 file in one four-backtick block (verify the block is non-empty with `wc -l` before sending), then `AGMSG-RESULT v1 task_id=dotfiles-T128-regime-counters-redesign-a01 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256> a02_expected_sha256=<sha256 of the block plus a trailing newline>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the file and asks for the one confirmation (`verdict=accept design_sha256=<hash>`). max_turns=3. Forbidden: editing tracked files; branches; PRs.
