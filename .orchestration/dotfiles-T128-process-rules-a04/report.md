# Report: dotfiles-T128-process-rules-a04

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `docs/regime-pattern`, PR #318, from `781e6ef8`. Third reset continuation of PR #318 (`reset_of: [dotfiles-T128-process-rules-a01, -a02, -a03]`). a03 was reset under INV-6's Bot threshold during its revise round 1, with P1 on two heads after its RESULT `b9a9da7d`: `386f97ff` and `781e6ef8`.
- Task file sha256 `842deee2…` checked against TASK 22:41:04Z and copied byte-identical in `379fa107` to `.orchestration/dotfiles-T128-process-rules-a04/task.md`; the a01 to a03 directories stay as history. Content commit `28d728c5`, then this evidence.

## Carried over (on the branch before this task)

Items 1 to 5, the a02 revise round's five checks, the three Bot P2 fixes of `21c160c8`, a03's `798fa098` and `7524e001`, and the a03 revise round's three fixes (`386f97ff`) plus its fix round (`114d5b91`), all unchanged.

## Items 6 and 7 (`28d728c5`, verbatim from the task file)

6. Thread 4243537279: the design-review bullet now reads "The third revision round is the last: the design is frozen at the hash the pair last accepted, a revision after the third pair is not made, and any later change to a hashed key is a new pair (INV-7); …". In `test_design_review_runs_in_paired_rounds_with_a_cap`, the token "After at most three revision rounds the design is frozen" is replaced by "frozen at the hash the pair last accepted", and "any later change to a hashed key is a new pair (INV-7)" is added.
7. Thread 4243537281: the boundary bullet now reads "It carries no task draft under review. A design not yet on `main` lands through a merged boundary PR before its implementing TASK is dispatched (INV-2), and any merged boundary that carries the design meets that precondition." `test_a_boundary_pr_never_gates_a_dispatch` is renamed `test_a_design_lands_on_main_before_its_task`; it asserts both new tokens and `assertNotIn("is never a prerequisite of a dispatch", …)`. The old token is gone from the test and from the prose.

One edit the task did not name: item 7 rewords "meets the design-on-main precondition" to "meets that precondition", and a02's `test_pattern_rules_pin_their_safeguards` pinned the old wording. That test now pins the reworded clause, "any merged boundary that carries the design meets that precondition"; without the change the verbatim replacement fails it.

Each new token fails its test when removed, and each old sentence pasted back fails too: 5 of 5 (validation §3). The docs module runs 41 tests, OK. The premises hold (validation §4).

## Bot threads

| Thread | Head | Disposition |
|---|---|---|
| 4243537279 | `781e6ef8` | `fixed:28d728c5` (item 6) |
| 4243537281 | `781e6ef8` | `fixed:28d728c5` (item 7) |
| 4243516879 | `386f97ff` | `fixed:114d5b91` (the hand count of review-body findings beside the counter script) |
| 4243516880 | `386f97ff` | `fixed:114d5b91` (the no-checks race of the CI watcher) |
| 4243537278 | `781e6ef8` | `fixed:2a3f52e9` (Amendment 1, item 8) |

The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report. The worker resolves no thread.

## Amendment 1 (TASK 22:55:53Z, sha256 `6ef9ae95…`)

- The hold PING of 22:54:55Z asked for no a04 RESULT until this amendment; my first a04 RESULT went out at 22:57:06Z anyway, because I did not re-read the inbox between the recheck and the dispatch. It listed 4243537278 as open. PONG `status=ok` reported the crossing; this RESULT supersedes it.
- `16c2e3d4` re-copies the amended task file byte-identical. `2a3f52e9` is item 8, verbatim (thread 4243537278: the hashed INV-6 counts Bot heads from `original_commit_id` on `review_comment` items only). The counters bullet now says the script's inline count "is INV-6's whole head count", and the hand list of P0/P1 review bodies serves "S1's finding classes and the worker's fix-round cap only, never as INV-6 heads". The review-body clause reads "which S1 and the fix-round cap count, INV-6 does not, and history does not hold". `test_counters_add_review_body_findings` asserts the new sentence and the absence of both replaced phrases; the token "P0/P1-badged Bot review bodies grouped by `commit_id`" stays.
- The three proofs fail their test: the new sentence removed, the old sentence pasted back, and the old INV-6 clause pasted back (validation §7). The perl harness could not carry the sentences' `/` and apostrophes, so `scratchpad/mutate_a04_am1.py` makes the same replacements in Python on the same `git archive` copy. The docs module runs 41 tests, OK.
- No Bot P0/P1 round was open on `cc9fc785` to fold in (its round had no findings).

## Notes

- Nothing here touches the threat-table rule's payload wording.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `172a34d7-e9a7-4556-9874-cf55f2c7314d` (validation §5).

cost: n/a
