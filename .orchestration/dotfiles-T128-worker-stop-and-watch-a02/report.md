# Report: dotfiles-T128-worker-stop-and-watch-a02

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`, branch `docs/worker-stop-and-watch`, PR #323, from `e924c5df`. Reset successor of `dotfiles-T128-worker-stop-and-watch-a01` under INV-6: a second revise RESULT would have made revises 2 (reset record `.orchestration/acceptance/dotfiles-T128-worker-stop-and-watch-a01-design-reset.md`).
- Task file sha256 `af519f0f…` checked against the TASK at 02:54:30Z and copied byte-identical to `.orchestration/dotfiles-T128-worker-stop-and-watch-a02/task.md`. One commit carries the copy, the three text changes, the three fixtures, the tokens and this evidence.

## A7-4 (verbatim from the task file)

1. Thread 4244248703, step 15's listing: review bodies that "carries a badge, P0 to P3", "counted toward the classes at any priority and toward the fix cap at P0 or P1, never INV-6's heads". The class count therefore reads every badged Codex finding since the task's first commit, inline or review-body. The fix cap and the INV-6 heads stay P0/P1, and the heads stay inline `review_comment` items.
2. Thread 4244272551, step 7: the audit-head clause becomes "INV-6's audit-head component read as the counters bullet prescribes (…)". It names no file format.
3. Thread 4244248706, Message Contract v1: the RESULT line carries `head=<full sha>`, and a new sentence follows the block: "`head=<full sha>` is mandatory: the first RESULT's head is INV-6's baseline, the sha the counters read."

Three fixtures are updated in this commit, a declared change (INV-12): `tests/fixtures/regime/worker-step-15.md`, `orchestrator-step-7.md` and `message-contract.md`. The token changes:
- `test_the_worker_stops_itself_on_repeated_findings` replaces the fix-cap token and adds "carries a badge, P0 to P3";
- `test_the_orchestrator_watches_from_github_and_history` adds "read as the counters bullet prescribes" and drops the replaced clause's token;
- the new `test_result_head_is_in_the_contract` asserts "head=<full sha>" and "the first RESULT's head is INV-6's baseline" in the Message Contract section.

Each new token fails its test and the whole-section pin when removed (validation §3). The docs module runs 45 tests, OK.

## Threads

| Threads | Disposition |
|---|---|
| 4244248703, 4244272551, 4244248706 | `fixed:` this commit (A7-4) |
| 4244203596, 4244203600, 4244203603, 4244203607, 4244203611, 4244203615 | `fixed:3ba70625` |
| 4244128846, 4244175775 | `not-applicable` (premise rejected) |
| 4244175778 | `fixed:040b32f9` |
| 4244128840, 4244128851, 4244128854, 4244128857, 4244128859 | `fixed:2c8dce27` |
| 4244248694, 4244248710 | `fixed:e924c5df` |
| 4244248692 | the orchestrator's disposition (rows per allowed path) |

A7-1 on this task: no RESULT yet, so 0 heads; the classes since the a02 task copy start empty, because a reset successor never inherits its predecessor's classes. The `--history-only` output before the push is in validation §4. The final head's CI and Bot wait are in the RESULT and the main-checkout copy; a further class-count scope finding is reported, not fixed.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `dccaabd2-91e1-4256-9f2c-b934222c3b19` (validation §5).

cost: n/a
