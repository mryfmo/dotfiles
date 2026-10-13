---
reviewed_at: 2026-10-13T05:09:36Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a
task: dotfiles-T128-orchestrator-tools-a03-amend-review-a01
round: 1
task_file: dotfiles-T128-orchestrator-tools-a03-amend-review-a01@0a6fb6cc145d32cadf1eef17ac1c4dcbe5352694549445cfa97184d196d259a6
files:
  - dotfiles-T128-orchestrator-tools-a03@ef3b264693a4d8a91b688b06f46d3fb44ec2e90578ad3a18258b69c29b1fcb34
previous: main 1da9594c copy b7348b8a (a03 as written by this seat; byte-equal)
verdicts:
  dotfiles-T128-orchestrator-tools-a03: confirm
---

# Amendment review: dotfiles-T128-orchestrator-tools-a03 amendment 1 (the malformed-identity row), review-seat half, round 1

Both hashes of the 05:08:21Z TASK line recomputed and equal. Read against main's copy (1da9594c, b7348b8a), C-28 and M-20261012-29 (the amend-review question: every behaviour an amendment adds has its row), and the thread as the brief quotes it (gh unreachable from this seat).

Stop condition, each point:

1. Diff against main (numstat 7 added, 1 removed; hunks at 22 to 23, 96, 113 to 116): one row after the two dispatch.sh rows (a line whose task_id= is missing, empty or repeated, or recorded against an acceptance record; thread 4254893065), closed by test_dispatch_refuses_a_line_without_a_task_id; item 2 names that test among the closed-row names with the behaviour (refused before any hash or record work); the Amendment 1 section. Nothing else; reset_of, the copy rows and the a03 evidence directory are unchanged. amend-sweep for the superseded phrases (C1 to C6, C1 to C9, draft PR from, read_at=<timestamp): no leftover.
2. Behaviours this amendment adds or changes (C-28): one, the refusal of a line without a well-formed task_id= before any hash or record work, and its consequence for the record path (such a line is never recorded against a record). Its row is the new one; it touches the bus (a line is not sent) and the acceptance record (nothing is appended), both named in the row's control. No other script or procedure behaviour changes in this amendment; the code change is the worker's revise of the same thread.
3. The closed row's test name appears verbatim in item 2 (and in the Amendment 1 section): three occurrences, as the record row's name does. The wording agrees with the a01 and a04 texts it sits beside (task_file= and 64-hex task_sha256= for a TASK; the dispatch list of the record's JSON block).
4. Checker on a copy named after the task id: OK (C1 to C10); C7b unchanged (one row per allowed_files entry).

## Findings

- P3 0.6 .orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md:93 — item 1's dispatch.sh bullet, the script's contract, still lists the refusals as the second line, the hash mismatch and the TASK without task_file= or task_sha256=; the task_id= refusal is specified only in the row and in item 2's parenthetical. One clause in item 1 ("refuses a line whose task_id= is missing, empty or repeated, before any hash or record work") would put the contract in one place; the test and the row already define it, so this is not blocking, and a03's counters (amendments now 1) make a further amendment the reset, so fold it into the next text change, not a round.
- P3 0.9 .orchestration/tasks/dotfiles-T128-orchestrator-tools-a03-amend-review-a01.md:3 — the review task's own front matter, heading, Output path and RESULT line say -amend-review-a1 while the bus line, the file name and allowed_files say -amend-review-a01; this receipt and the RESULT follow the bus line (task_id …-a01, validation …-a01.md), which is what the Stop gate matches. Align the file's four mentions to a01 before it is committed.

Amendment verdict: dotfiles-T128-orchestrator-tools-a03: confirm
