---
format: 2
task_id: dotfiles-T128-task-checkers-a01-amend-review-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-checkers-a01-amend-review-a02 — confirm amendment 2 of `dotfiles-T128-task-checkers-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 (the TASK line's bus time is the dispatch time) by the orchestrator seat. The Codex Bot's single review of PR #352 (head 63433cf1; the worker's question, PONG 05:08:02Z) raised four P1: 4266930617 (`ledger-check.py:21`: a top-level `review` body with a P0 to P3 badge is a finding the gate's `swept_finding_ids()` counts and the check ignored), 4266930623 (`ledger-check.py:25`: a Markdown-bulleted `- [P1]` audit line counts zero while the gate's `AUDIT_FINDING` accepts bullets), 4266930635 (`task-consistency-check.py:69`: C4's substring search lets `scripts/foo.py.bak` cover `scripts/foo.py`), 4266930643 (the checker's one `closed` row cites one test for C1 to C10). The worker reports all four hold, that the first three change what a check means (which the task text froze) and that the three fixes pass the 200-line practice cap. Plan 020 step 4 gives a P1 one fix round before the RESULT; this amendment opens exactly that scope. The task file is not on `main`: the pre-amendment copy is the pair-confirmed amendment-1 version cd00812f, kept beside this brief; `git diff --no-index <that copy> <the file>` prints `1 file changed, 15 insertions(+), 6 deletions(-)`. Amended file: `.orchestration/tasks/dotfiles-T128-task-checkers-a01.md`, sha256 `c5ea9a543a80d766803d4a0b5bd877f4b977b9a548c53a1b327ff3a8c90cd20d`; the pre-amendment copy is on `main` (`not on main; pre-amendment pair-confirmed copy cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d`).

## What changed (amendment 2)

1. Item 1: C4 names an `allowed_files` entry only at a path boundary (the entry followed by the end, a space, a slash, a quote, a parenthesis, a comma or a glob character).
2. Item 2: ledger-check counts a badged `review`/`issue_comment` body as the gate's `swept_finding_ids()` keys it, and an audit line by the gate's `AUDIT_FINDING` regex (an optional bullet and whitespace before `[P0]` to `[P3]`).
3. The checker's closed row is two rows: the ten-file test and `test_task_consistency_check_reaches_every_other_check` (thread 4266930643).
4. Item 4: the ten-file table becomes the replay of the amended checker (the worker pastes it; premise 1 stays as the pre-amendment replay); a new case `test_ledger_check_counts_what_the_gate_counts`; the a05 triple's `36` is unchanged (no badged body, no bulleted line in those fixtures).
5. Out of scope: "a change to what any check means beyond the three alignments of amendment 2"; the Check: the 200-line practice cap yields to the three fixes within INV-2's 500, the RESULT states the count.
6. A `## Change of 2026-10-14 (amendment 2 …)` section stating 1 to 5. Amendment 1 stands; nothing else changes.

## Stop condition

1. The diff of the task file against its pre-amendment pair-confirmed copy (the orchestrator's scratchpad `t704-before-amend2.md`, sha256 cd00812f4a3cd64d841d5a96c7720e33be904e9cabb2cf70d31ccad8580b6a2d; the file is not on `main` yet) contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-task-checkers-a01-amend-review-a02.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-task-checkers-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-checkers-a01-amend-review-a02 verdict=confirm|revise amended_task_sha256=c5ea9a543a80d766803d4a0b5bd877f4b977b9a548c53a1b327ff3a8c90cd20d validation=<path>`.

## Round 2 (orchestrator, after the round-1 RESULTs of 05:18Z and 05:21Z)

Round 1: the Codex half's P1 (the new row claimed the pass path with one test) and your two P2 and three P3. All applied: `issue_comment` is gone from item 2, which now names the Codex Bot's badged `review` keyed `pullrequestreview-<id>` (require-crit-review.py:858-865); each alignment has its own closed row and test (the ledger-check alignments → `test_ledger_check_counts_what_the_gate_counts`; C4's boundary → a new case `test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary`; the pass path → its own row); row one of the checker is scoped to the checks the ten reach (C2, C3, C4, C6, C7); item 4 asks the worker to list, beside the paste, each file whose set differs from premise 1 with the causing row text and entry; this brief's "on main" slip is fixed. Input checker `OK`, premises OK x5. Same four stop conditions on the new hash (`amended_task_sha256` of the round-2 TASK line).

## Round 3 (orchestrator, after the round-2 RESULTs of 05:25Z and 05:26Z)

Round 2: your confirm on b10113f2; the Codex half's P1 (the Change section's summary still said `issue_comment` and "two rows") and P2 (the C4 case covered four boundaries of the seven item 1 names). Both applied: the summary names the Codex Bot's badged `review` keyed `pullrequestreview-<id>` and the four checker rows plus the ledger-check alignment row; the C4 case covers the end of the control text, a slash, a parenthesis, a space, a quote, a comma and a glob character, one case each. Nothing else changed; input checker `OK`, premises OK x5. Same four stop conditions on the new hash.

## Round 4 (orchestrator, after the round-3 RESULTs of 05:28Z and 05:29Z)

Round 3: your confirm on a223b108; the Codex half's P1: the superseded term still stood in item 2's parenthesis ("… items are not counted there"), so `amend-sweep.sh` for that term failed stop condition 4. Removed (the parenthesis now says the gate counts no other item source there); `amend-sweep.sh` prints `no leftover`. Nothing else changed; input checker `OK`, premises OK x5. Same four stop conditions on the new hash.
