---
reviewed_at: 2026-10-14T05:31Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check in parallel)
profile: review
session: 2089b04f
task: dotfiles-T128-task-checkers-a01-amend-review-a02
round: 4
task_file: .orchestration/tasks/dotfiles-T128-task-checkers-a01-amend-review-a02.md@819bda2758509df6073df1dd19f4e66495f10366383a486c1b8de2d05e25e24b
amended_task: .orchestration/tasks/dotfiles-T128-task-checkers-a01.md@a309b3944b2dec9be6117499a98d7cc4bd7bd0026706f99525df1221fd226efb (untracked; previous_amended_task_sha256 cd00812f, the amendment-1 text; rounds 1 to 3 (c5ea9a54, b10113f2, a223b108) superseded)
previous_receipt: 81f292ac05238d19e6d7b08fbdd50db871e6f9d18f977fff1d5a44414525fe01 (round 3, confirm on a223b108; superseded by this file at the same path)
diff_base: this seat's amendment-1 copy (cd00812f) for the whole amendment, and its round-3 copy (a223b108) for what round 4 changed
diffstat: "1 file changed, 23 insertions(+), 7 deletions(-) against the amendment-1 copy"
consistency_check: "dotfiles-T128-task-checkers-a01.md: OK (checker fdab23e0 on a copy named by the task id, run from the main checkout)"
amend_sweep: "no leftover of: check means, fixing / equals premise 1, exactly / unchanged in meaning\. / input unchanged in meaning (ledger / two rows / issue_comment"
sources: origin/main 28eec93c (scripts/require-crit-review.py lines 43 to 44, 50, 854 to 868), the round-1 sources
verdict: confirm
---

# Amendment review: dotfiles-T128-task-checkers-a01 (plan 007 T704), amendment 2, round 4

Both hashes of the 05:30:46Z TASK line recomputed and equal; the previous hash equals this seat's amendment-1 copy. Against the round-3 text the diff is one hunk, item 2's parenthesis (line 118): "`issue_comment` items are not counted there" becomes "the gate counts no other item source there", which is what require-crit-review.py:858–865 does (review comments by id, badged reviews by `pullrequestreview-<id>`, nothing else). Nothing else differs; against the amendment-1 copy the diff is the amendment-2 list plus the round-2 to round-4 changes. The superseded term no longer appears anywhere in the file, so stop condition 4's sweep passes as pasted.

## Stop conditions, round 4

1. The one hunk is the brief's Round 4 and nothing more.
2. Unchanged from round 3: every changed behaviour has its own closed row and test.
3. Nine closed rows, each test named once in the table and once in item 4; item 2 and the Change section agree with the gate on main.
4. Checker OK on a309b394; sweep clean for every superseded term of the amendment (header); no `reset_of`, no copy rows; the task-copy row, the evidence directory and the five premises unchanged. Count words unchanged ("four rows", "seven" boundaries, "two alignments", "four P1", "36"); the only times are bus times.

## Findings

- P3 (high) `.orchestration/tasks/dotfiles-T128-task-checkers-a01-amend-review-a02.md:10` — still "the pre-amendment copy is on `main` (`not on main; …`)" and the round-1 diffstat "15 insertions(+), 6 deletions(-)" (now 23 and 7). Brief only, since round 1.

Approval of the task text: as in round 3, with the last superseded term gone.

Amendment verdict: dotfiles-T128-task-checkers-a01: confirm
