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

The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report. The worker resolves no thread.

## Notes

- Nothing here touches the threat-table rule's payload wording.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `172a34d7-e9a7-4556-9874-cf55f2c7314d` (validation §5).

cost: n/a

## Final head `cc9fc785` (main-checkout copy)

- Commits: `379fa107` (task copy), `28d728c5` (items 6 and 7), `cc9fc785` (evidence), pushed together at 22:44:40Z.
- CI: 13 of 13 pass on `cc9fc785` (PR 320's merge removed the `changes` check); the watcher started once a check run was listed, exited 0, and was joined before the RESULT (validation §6).
- Bot: one round on `cc9fc785`. The code review completed at 22:46:20Z with no review object and no comment, 👍 at 22:46:23Z. `bot_rounds=1`, no fix round.
- A thread the task does not list: 4243537278 (P1, on `781e6ef8`, SKILL.md:72), raised in the same review as 4243537279 and 4243537281. It says the counters bullet counts review-body findings toward INV-6 ("…which INV-6 and S1 count…"), while canonical INV-6 counts "from original_commit_id on review_comment items recorded by pr-feedback.py" (`git show origin/main:.orchestration/tasks/dotfiles-T128-regime-v3-a01.md`, line 55). That is right: the sentence contradicts the hashed design, the same class as items 6 and 7. Thread 4243516879 asked for the opposite, and `114d5b91` added the hand count of review bodies. I did not change the sentence; it is left open for your disposition. Proposed wording: "…P0/P1-badged Bot review bodies grouped by `commit_id`, which S1 and the fix rounds count (INV-6's head count reads inline `review_comment` items only, as pr-feedback.py records them) and history does not hold", and in `114d5b91`'s sentence, "counts … review bodies … for S1".
