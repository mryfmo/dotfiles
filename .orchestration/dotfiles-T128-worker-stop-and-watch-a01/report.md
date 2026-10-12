# Report: dotfiles-T128-worker-stop-and-watch-a01

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`. Branch `docs/worker-stop-and-watch` from `origin/main` `e83e923d` (`git switch -c … --no-track origin/main`). Plan 006 Phase A7.
- Task file sha256 `84d8acde…` checked against the TASK at 01:41:55Z and copied byte-identical in `e596fd88` to `.orchestration/dotfiles-T128-worker-stop-and-watch-a01/task.md`. Content commit `218ac77e`, then this evidence.

## What changed (`218ac77e`, verbatim from the task file)

1. A7-1, Worker Playbook step 15: the task's two bullets sit before "Fix P0/P1 findings, inline or review-body, …":
   - the worker's own stop. Before each fix commit it counts the Codex Bot P0/P1 heads after its first RESULT and the thread title classes, both since its own first commit on the PR. At 2 heads (INV-6) or a class at 3 (S1) it fixes nothing more, sends `AGMSG-PONG v1 … status=blocked note=S1|INV-6;…` and waits for that stop's own release.
   - the `scripts/regime-counters.sh <task id> --history-only` line before each push.
2. A7-2, Orchestrator Playbook step 7: "Track `max_turns`. Use `AGMSG-PING` for liveness if a worker stalls." becomes the watch: from GitHub and history at least every 30 minutes after a TASK, one bounded background wait of at most 30 minutes, a PING after 45 minutes without a push, a PONG or a RESULT, and `herdr-agents --remove-worker <worktree> --force` for a worker that keeps pushing past the cap with its PING unread.
3. Fixtures (a declared change, INV-12): `tests/fixtures/regime/worker-step-15.md` and `tests/fixtures/regime/orchestrator-step-7.md` are regenerated in the same commit with the test's own marker table; `test_regime_rule_sections_are_pinned_whole` is green.
4. Tests: `test_the_worker_stops_itself_on_repeated_findings` (nine tokens in step 15) and `test_the_orchestrator_watches_from_github_and_history` (five tokens in the Orchestrator Playbook). One deviation: the task lists "`status=blocked note=S1|INV-6`" and "`--history-only`" in backticks, but the verbatim prose has them inside longer code spans (`` `AGMSG-PONG v1 … status=blocked note=S1|INV-6;…` `` and `` `scripts/regime-counters.sh <task id> --history-only` ``). The test therefore asserts those two without their outer backticks; a comment in the test says so.

All fourteen tokens fail both the token test and the whole-section pin when removed (validation §3). The docs module runs 44 tests, OK. The premises hold (validation §4), with two notes there: premise 1's read state comes from `history.sh` instead of `sqlite3`, and premise 2's line has moved.

## A7-1 on this PR

This is the first PR on which the worker counts. Before the first push: `task=… results=0 … bot_p1_heads_after_result=skipped … source=live` (validation §5). No fix commit has happened yet; the counts before any fix round are in the main-checkout copy and the RESULT.

## Bot round 1 on `9d001bcb` and fix round 1 (Amendment 1, TASK 02:00:08Z, sha256 `b0b84598…`)

Review 5485951311 (01:52:59Z) raised six threads, all on A7's own sentences. Per the task, a fix round on a rule sentence needs its class reported first. PONG 655 (`status=question`, default hold) reported the A7-1 counts:
- 0 heads after the first RESULT, because none was sent;
- six classes at 1 each;
- so no stop.

The orchestrator ordered fix round 1 with my proposed sentences, except (3) (ACCEPTANCE 02:00:08Z). Amendment 1 adds one threat-table row for review-derived text in notes, and this commit carries its byte-identical copy (validation §7).

| Thread | Class (A7-1) | Fix in this commit |
|---|---|---|
| 4244128840 (P2) | paginate every endpoint | step 7's three list calls get `gh api --paginate`, "all three with `--paginate`" |
| 4244128846 (P2) | include every review | the class count reads "every finding the PR-feedback sweep would list (any reviewer, any priority, inline or review-body…)"; INV-6's head count stays the Codex P0/P1 inline `review_comment` items |
| 4244128851 (P1) | encode review-derived classes | before anything review-derived enters a note, it is reduced: a class name to `[a-z0-9-]`, a thread id to digits, "a Bot title never (only its reduced class)". Step 11's inline `agmsg-dispatch` stays and carries no review text, so there is no `--body-file` clause, as the ACCEPTANCE says |
| 4244128854 (P1) | choose one third-round | when the heads=2 stop and the A2 third round coincide, the worker sends the `AGMSG-RESULT … bot_rounds=3` with the stop's note fields "instead of a blocked PONG, and then waits for the ACCEPTANCE: one handoff" |
| 4244128857 (P2) | preserve the complete | the worker "pastes its complete output (the count line, the `detail:` line and any `S2:` line)" |
| 4244128859 (P2) | quarantine a forced | after `--remove-worker --force`, "the stopped worktree's evidence is preserved and the next seat is created in a clean worktree" |

The two fixtures are regenerated in this commit, a declared change. The six new tokens each fail both their test and the whole-section pin when removed (validation §7). The docs module runs 44 tests, OK. Before the push, `--history-only` prints no `S2:` line (questions 1, amendments 1). Per the ACCEPTANCE, a further finding on these sentences is reported with its class, and fix round 2 is only for a new class.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `8d4a9e78-4caa-4211-91dc-6208369b7100` (validation §6).

cost: n/a
