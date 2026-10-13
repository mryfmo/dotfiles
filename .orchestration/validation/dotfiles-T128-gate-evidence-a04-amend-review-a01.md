---
reviewed_at: 2026-10-13T03:33:51Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a
task: dotfiles-T128-gate-evidence-a04-amend-review-a01
round: 1
task_file: dotfiles-T128-gate-evidence-a04-amend-review-a01@d1854d6ee5d9c9da2f7e4a31428852357794f6c30d48822a2472ef79b0f4bdbd
files:
  - dotfiles-T128-gate-evidence-a04@be659392a6300bc0fff0ba3c421660352938762d6fccb259075f1c430ae8b3d8
previous: main 948d1f38 copy 03a5253d (a04 as written by this seat, redesign round 4)
verdicts:
  dotfiles-T128-gate-evidence-a04: confirm
---

# Amendment review: dotfiles-T128-gate-evidence-a04 amendment 1 (the dispatch entry's read marker), review-seat half, round 1

Both hashes of the 03:32:46Z TASK line recomputed and equal. Read against main's copy (948d1f38, 03a5253d, byte-equal to this seat's redesign round-4 file), T718 a01 amendment 1 on main (dotfiles-T128-orchestrator-tools-a01.md item 1), the a04 rule sentence (SKILL step 6: the bus line with its read marker) and the agmsg skill's rule (scripts only, never the database).

Stop condition, each point:

1. Diff against main (numstat 5 added, 1 removed; hunks at 93 and 111 to 114): item 2's dispatch key now reads "each a sent bus line followed by ` read_at=<marker>`, the marker being what scripts/orchestrator/dispatch.sh records from the agmsg scripts: `read` or `unread` as history.sh prints it, never a database read", and the Amendment 1 section. Nothing else; reset_of, the copy rows and the a04 directory are unchanged. amend-sweep for read_at=<timestamp finds no leftover.
2. The wording matches what dispatch.sh will write: T718 a01 amendment 1's item 1 appends "<the line as sent> read_at=<read_at from the bus through history.sh, or unread>", history.sh exposes the read marker (the ●/○ the worker's question of 03:15Z named) and no timestamp, so the value is the marker; the rule sentence asks for "the bus line with its read marker", which this is. The gate still validates the list only as strings, so the change touches no check.
3. Checker on a copy named after the task id: OK (C1 to C10); C7b unchanged (one row per allowed_files entry).

Note, not a finding: a01's phrase "read_at from the bus through history.sh" can be read as a timestamp while a04 says read or unread; the two agree once history.sh's output is known, and a01 cannot be re-worded without its amendment 2 (INV-6's reset), so a04 carrying the precise form is the right place for it. The worker reads both.

## Findings

None.

Amendment verdict: dotfiles-T128-gate-evidence-a04: confirm
