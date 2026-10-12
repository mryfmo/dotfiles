---
task_id: dotfiles-T128-process-rules-a06
status: reset
redesign_task: dotfiles-T128-process-rules-a07
design_sha256: d5d499cead2297a8357b243d46172f8fea7cb929b4e4a62addb71633f3babb6a
redesign_source: dotfiles-T128-process-rules-redesign-a06
reason: INV-6-amendments
---

# Reset record: dotfiles-T128-process-rules-a06 → a07 (INV-6, 2026-10-12 01:12Z)

- **Trigger:** Bot P1 4243975211 on `f755d714` (no threat row for the branch evidence records) is a task-record change; added, it is amendment 2 of a06 (counters at 01:12Z: amendments 1, revises 1, Bot P1 heads after the first RESULT 1). Fourth finding of the `bookkeeping` class (S1 declared at the third, 00:55Z); the changed step's check was too narrow (`tests/` paths only) and is generalized (C4 every `allowed_files` entry, C6 the design's current receipt).
- **Redesign:** `dotfiles-T128-process-rules-redesign-a06` on the review seat (01:13Z): a07 = a06 (`90fb32c2…`) + the evidence-records row (the worker's wording), the SKILL row naming its path, `design_review.receipt` round 18, a07 bookkeeping (`reset_of`, `allowed_files`, the copies row), one intro sentence (the table names every `allowed_files` entry), History, First commit and Completion from `f755d714`; the review seat runs the checker on the block before sending.
- **Worker:** `claude-standard-dot-a003` holds at `f755d714` (ACCEPTANCE `under_review`, 01:12Z).
- **Anchor:** RESULT 649 at 01:18:23Z: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a06 round=2 status=ready_for_review verdict=accept design_sha256=d5d499cead2297a8357b243d46172f8fea7cb929b4e4a62addb71633f3babb6a receipt=none`.
