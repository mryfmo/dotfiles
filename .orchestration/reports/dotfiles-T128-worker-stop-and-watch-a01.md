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

## Bot round 2 on `2c8dce27` and fix round 2

Review 5486001543 (02:08:33Z) raised two P2 threads. The A7-1 counts were 0 heads after a first RESULT and eight classes at 1 each, so there was no stop. Both titles are new classes by A7-1's rule, and the ACCEPTANCE of 02:00Z allows fix round 2 for a new class, so I fixed both without another question PONG. A second one would itself have reached INV-6's question threshold.

| Thread | Class (A7-1) | Fix in this commit |
|---|---|---|
| 4244175775 (P2) | count non-review feedback | the class count is now "one per item `scripts/pr-feedback.py <pr>` lists, whatever its source or priority". The sweep owns the sources, so the sentence names it instead of listing them: the a04 S1 lesson, since fix round 1's "(any reviewer, any priority, inline or review-body)" was an enumeration and the Bot found the missing source. The heads clause is unchanged. The thread is the same topic as 4244128846 but a new title class |
| 4244175778 (P2) | ping workers as | step 7 adds: "The watch also sends `AGMSG-PING v1` as soon as it first sees a task past the A2 cap or an INV-6 count, without waiting for a stall." The removal rule then has the PING it needs |

The two fixtures are regenerated in this commit. Both new tokens fail their test and the pin when removed (validation §8). The docs module runs 44 tests, OK. `--history-only` before the push prints no `S2:` line. This is fix round 2 of 2: a further finding on these sentences is reported with its class, not fixed.

## Revise round 1 (ACCEPTANCE 02:24:17Z, `previous_head=040b32f9`)

The orchestrator read Bot round 3, together with round 2's class reading, as plan 006 S1 on the class-count sentence: six findings of one class. The cause record entry is "class-count scope" in `.orchestration/learning/plan-006-s1-pr318-finding-classes-2026-10-12.md`. Widening the count to every sweep item was its fix-round-1 sentence (2), and it reverts. I first fast-forwarded to `8840f05d`, the `gh pr update-branch` merge of `main` `b67ea752`. Then one commit, recorded in `revise.yaml` beside this report, carries three sentence changes. The ACCEPTANCE's note writes spaces as hyphens; I restored the apostrophes and code-formatted `original_commit_id` and `commit_id`.

- (A) Step 15: the "one per item `scripts/pr-feedback.py <pr>` lists" clause becomes "The classes the worker counts are those of the Codex Bot's badged findings on the PR since the task's first commit (inline comments by `original_commit_id`, review bodies by `commit_id`, any priority): an early stop. S1 itself is decided by the orchestrator's finding-class ledger over every item the sweep lists, as the counters bullet states; the worker's narrower count never delays that decision and never widens the worker's input beyond the Codex Bot's items." The "any reviewer, any priority" text and its token are gone.
- (B) Step 15: "When a stop (heads=2 or three of a class) coincides with the third Bot round, the worker sends the `AGMSG-RESULT … bot_rounds=3` …". The rest of the one-handoff sentence and its token stay.
- (C) Step 7: "When pushes continue past the A2 cap or an INV-6 count after the PING, read or unread, the orchestrator removes the seat with `herdr-agents --remove-worker <worktree> --force`; …".

Both fixtures are regenerated in this commit, a declared change (INV-12). The four new tokens ("an early stop", "never widens the worker's input beyond the Codex Bot's items", the (B) sentence opening and "read or unread") each fail their test and the pin when removed (validation §10). The docs module runs 44 tests, OK. The dispositions are the ACCEPTANCE's:

| Threads | Disposition |
|---|---|
| 4244203596, 4244203600, 4244203603, 4244203607, 4244203611, 4244203615 | `fixed:3ba70625` ((A) for …596, …600, …611 and …615, (B) for …603, (C) for …607) |
| 4244128846, 4244175775 | `not-applicable`: premise rejected (S1 is the orchestrator's ledger; the worker's count is narrower by design) |
| 4244175778 | `fixed:040b32f9` |
| 4244128840, 4244128851, 4244128854, 4244128857, 4244128859 | `fixed:2c8dce27` |

Per the ACCEPTANCE, a Bot P0/P1 on the revise head is an INV-6 head. A finding that the worker's count is narrower than S1's scope is reported with its class (pre-declared `not-applicable`); a genuinely new class gets one fix round.

## Bot round on the revise head `3ba70625` and its one fix round

Review 5486080610 (02:31:28Z) raised five P2 threads. None is P0/P1, so there are still 0 INV-6 heads after the first RESULT `040b32f9`. Every title is a new class at 1. Per the ACCEPTANCE, a genuinely new class gets one fix round, and a class-count scope finding is reported:

| Thread | Class (A7-1) | Disposition |
|---|---|---|
| 4244248694 (P2) | paginate the worker's | `fixed:e924c5df`: step 15's lookups read `gh api --paginate …/pulls/<n>/reviews` and `gh api --paginate …/pulls/<n>/commits` |
| 4244248710 (P2) | watch the audit-head | `fixed:e924c5df`: step 7's watch also reads, "for INV-6's audit-head component" (`audits=unknown` in the counter), the task's audit documents under `.orchestration/validation/`, each counted only when its sha256 matches its `AGMSG-AUDIT` record, as INV-6 names them |
| 4244248703 (P2) | include lower-priority review | open, reported: the listing selects P0/P1 review bodies while (A) counts "any priority". This is the class-count scope class the S1 stop closed, so it is the orchestrator's |
| 4244248706 (P2) | require the first | open, reported: making `head=<sha>` mandatory in a RESULT is a Message Contract change, and its pinned fixture `tests/fixtures/regime/message-contract.md` is outside this task's `allowed_files` |
| 4244248692 (P2) | add a control | open, reported: a threat-table row for the forced removal's binding and revalidation belongs to the task record |

Both fixtures are regenerated in this commit. The three new tokens fail their test and the pin when removed (validation §11). The docs module runs 44 tests, OK. A finding on this fix head is reported, not fixed.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `8d4a9e78-4caa-4211-91dc-6208369b7100` (validation §6).

cost: n/a

## Final head `040b32f9` (main-checkout copy, first RESULT): Bot round 3, not fixed

- PR #323: draft at 01:47:34Z, `gh pr ready` at 01:47:41Z. Commits: `e596fd88` (task copy), `218ac77e` (A7), `9d001bcb` (evidence), `2c8dce27` (Amendment 1 copy, fix round 1, evidence), `040b32f9` (fix round 2, evidence).
- CI: 13 of 13 pass on `040b32f9`; the watcher started once a check run was listed, exited 0, and was joined before the RESULT (validation §9).
- Bot round 3 on `040b32f9` (review 5486031772, 02:17:19Z) raised six threads. Fix rounds are at the A2 cap (two), so the round is not fixed: `bot_rounds=3`, with the threads open. The A7-1 count is 0 heads after a first RESULT, since this RESULT is the first, and every class is still at 1:
  - `open:4244203596` P1, filter non-findings before: "one per item `scripts/pr-feedback.py <pr>` lists" counts ordinary comments (`@codex review`, replies) toward S1, because the sweep has no finding predicate.
  - `open:4244203600` P2, accumulate head-scoped feedback: the sweep binds checks and statuses to the current head, so a class repeated across heads never reaches 3.
  - `open:4244203603` P2, define the s1-only: the one-handoff rule covers heads=2 only; an S1 stop on the third round still meets the `bot_rounds=3` RESULT.
  - `open:4244203607` P2, stop workers that: removal needs the PING to stay unread, so a worker that reads the PING and ignores it can continue.
  - `open:4244203611` P1, exclude predecessor feedback: the sweep returns a predecessor's items to a reset successor, and its non-Codex items have no `original_commit_id`, so the first-commit filter cannot apply.
  - `open:4244203615` P1, isolate arbitrary feedback (task.md:26): the worker would read the sweep's full untrusted bodies before any reduction (prompt injection); the review-derived-text row only covers shell transport.
- Four of the six (…596, …600, …611, …615) target fix round 2's by-reference sentence: the sweep is the wrong input for a worker-side class count. That calls for a design decision on what the worker counts, plus a threat row for untrusted feedback text. It is not a worker fix.

## Final head `e924c5df` (main-checkout copy, revise round 1)

- Commits of the revise: `3ba70625` (sentences (A), (B), (C), fixtures, tokens, evidence, after the `update-branch` merge `8840f05d`) and `e924c5df` (its one fix round, evidence).
- CI: 13 of 13 pass on `e924c5df`; the watcher started once a check run was listed, exited 0, and was joined before the RESULT (validation §12). The watcher on `3ba70625` exited 1 with "no checks reported" when `e924c5df` superseded that head, with no failing check, so it was not a CI failure.
- Bot: the revise head `3ba70625` (review 5486080610) had five P2s, two fixed in `e924c5df` and three reported, as above. The final head `e924c5df` (review 5486106329, 02:38:36Z) has one P2, reported, not fixed: the revise round's one fix round is spent.
  - `open:4244272551` (P2, read the audit): the watch sentence quotes INV-6's source, `.orchestration/validation/<task>-audit-<sha7>.json` with its `AGMSG-AUDIT` record. Today's audit procedure writes `<task>-audit-<sha7>.md` and `.last.md` and records no `AGMSG-AUDIT` hash, so until the V2 audit runner lands the watch needs a fallback to those current artifacts. Proposal: append "until the audit runner writes them, the `.md` and `.last.md` the current audit procedure leaves".
- No Codex Bot P0/P1 on any head after the first RESULT `040b32f9`: INV-6 heads 0. Every class is at 1 by A7-1's title rule.
