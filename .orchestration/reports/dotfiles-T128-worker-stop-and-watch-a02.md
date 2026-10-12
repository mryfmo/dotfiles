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
| 4244248703, 4244272551, 4244248706 | `fixed:1d14eed5` (A7-4) |
| 4244203596, 4244203600, 4244203603, 4244203607, 4244203611, 4244203615 | `fixed:3ba70625` |
| 4244128846, 4244175775 | `not-applicable` (premise rejected) |
| 4244175778 | `fixed:040b32f9` |
| 4244128840, 4244128851, 4244128854, 4244128857, 4244128859 | `fixed:2c8dce27` |
| 4244248694, 4244248710 | `fixed:e924c5df` |
| 4244248692 | the orchestrator's disposition (rows per allowed path) |

A7-1 on this task: no RESULT yet, so 0 heads; the classes since the a02 task copy start empty, because a reset successor never inherits its predecessor's classes. The `--history-only` output before the push is in validation §4. The final head's CI and Bot wait are in the RESULT and the main-checkout copy; a further class-count scope finding is reported, not fixed.

## Bot round 1 on `1d14eed5` and fix round 1

Review 5486194208 (03:02:00Z) raised three P1s on A7 sentences. Its counts were 0 heads, since there is no a02 RESULT yet, and three classes at 1 each, so there was no stop. PONG 675 (`status=question`, a02's first, default hold) reported the classes with proposals. The ACCEPTANCE of 03:03:52Z ordered fix round 1 with the proposed sentences:

| Thread | Class (A7-1) | Fix in this commit |
|---|---|---|
| 4244354410 (P1) | establish the pr | step 7: "Until the RESULT names the PR, the watch reads its number with `gh pr list --head <the task's branch> --json number`." |
| 4244354413 (P1) | count repeated findings | step 15: "Before each fix commit" becomes "After every Bot review round, before deciding whether a fix commit follows", so a round with no fix commit, the third included, still runs the class scan |
| 4244354417 (P1) | define how the | step 7: "A fix round is a push whose predecessor head carries a Codex P0/P1 finding, counted from the PR's commits, the Bot reviews' `commit_id` and the inline comments' `original_commit_id`." |

Both fixtures are regenerated in this commit. The three new tokens fail their test and the pin when removed (validation §6). The docs module runs 45 tests, OK. A further finding on these sentences is reported with its class; fix round 2 is only for a new class.

## Notes

- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `dccaabd2-91e1-4256-9f2c-b934222c3b19` (validation §5).

cost: n/a

## Final head `3a54d340` (main-checkout copy)

- Commits of a02: `1d14eed5` (task copy, A7-4, three fixtures, tokens, evidence) and `3a54d340` (Bot fix round 1, fixtures, tokens, evidence). The three threads of fix round 1 are `fixed:3a54d340`.
- CI: 13 of 13 pass on `3a54d340`; the watcher started once a check run was listed, exited 0, and was joined before the RESULT (validation §7). `1d14eed5`'s watcher also exited 0.
- Bot round 2 on `3a54d340` (review 5486221546, 03:09:23Z) raised one P2, reported and not fixed:
  - `open:4244378809` (P2, bind the first, a new class; Message Contract line 117): a mandatory `head=` does not prove it is the head that produced the first RESULT, and `scripts/regime-counters.sh` accepts any matching prefix. Half of the fix belongs to the task record (a threat-table row for that input binding), and half is an orchestrator acceptance step. Proposal for the contract: "The orchestrator checks it against the PR's head when the first RESULT arrives (`gh pr view <n> --json headRefOid`); a mismatch is answered with a revise, never counted."
- A7-1: no Codex P0/P1 after a first RESULT, since this RESULT is a02's first, so 0 heads. Classes since the a02 copy are at 1 each. `bot_rounds=2`, one fix round.

## Amendment 1 and revise round 1 (TASK and ACCEPTANCE 04:54:52Z; `previous_head=3a54d340`)

The operator chose plan 008 option A, continuing in place. The audit of `3a54d340` was incorrect with four findings; its findings 2 and 4 are the amendment's, and findings 1 and 3 are this revise round's. One commit, `dc7edcc0`, recorded in `revise.yaml` beside the branch report, carries:

- the byte-identical copy of the amended task file (sha256 `1de19e51…`). It adds a sixth threat-table row, the forced removal as the orchestrator's in-process effect with its pre-removal verification and the session's permission mode, and corrects premise 1 to four heads after the park;
- audit finding 1, step 7: "A fix round is a push whose predecessor head carries a Codex badged finding of any priority, counted from the PR's commits, the Bot reviews' `commit_id` and the inline comments' `original_commit_id`." The test token is "…a Codex badged finding of any priority";
- audit finding 3, Message Contract v1, after the `head=` baseline sentence: "When the first RESULT arrives the orchestrator checks its `head=` against the PR's head (`gh pr view <n> --json headRefOid`); a mismatch is answered with `status=revise` and that RESULT's head is not the baseline." The token "a mismatch is answered with `status=revise`" sits in `test_question_pongs_are_in_the_contract`, as the ACCEPTANCE names. This is also thread 4244378809's proposal.

`orchestrator-step-7.md` and `message-contract.md` are regenerated in this commit, a declared change. Both new tokens fail their test and the pin when removed (validation §8). The docs module runs 45 tests, OK. Per the ACCEPTANCE, a Bot P0/P1 on the revise head is an INV-6 head.

## Final head `dc7edcc0` (main-checkout copy, revise round 1)

- Audit findings 1 and 3 are `fixed:dc7edcc0`, and thread 4244378809 with them: the contract sentence it asked for is in.
- CI: 13 of 13 pass on `dc7edcc0`; the watcher started once a check run was listed, exited 0, and was joined before the RESULT (validation §9).
- Bot round on `dc7edcc0` (review 5486694252, 05:03:14Z): five P2s, each a new class. None is P0/P1, so INV-6 heads stay at 0. All five are reported with a proposal, not fixed, since this revise names no further fix round. Two of them follow from this round's own sentences:
  - `open:4244811168` (use the same priority): step 7's any-priority fix round contradicts step 15's fix cap at P0/P1. Proposal: one rule in both playbooks. Either the cap counts badged fixes of any priority, or step 7 counts P0/P1 predecessors and the audit's P2-only gap is left to the cap.
  - `open:4244811164` (exclude a rejected RESULT): a `status=revise` does not remove a stale `head=` from the baseline, because `scripts/regime-counters.sh:110-115` reads `$results[0]` and history is immutable. Proposal: the corrected RESULT carries the baseline (the first RESULT not answered with a head mismatch), in the counter and in the contract sentence. The script is outside `allowed_files`.
  - `open:4244811155` (enforce the removal): the sixth threat row claims the pre-removal checks, but step 7 does not state them. Proposal: step 7 adds the row's checks before any removal (PR number from the task's branch, the identity's worktree against the TASK's `repo=`, fresh counts, evidence preserved).
  - `open:4244811161` (wait for a): a push already in flight when the PING goes out reads as continued pushing. Proposal: removal needs a push whose commit is newer than the PING and that arrives at least one turn after it.
  - `open:4244811170` (track observed head): the PR commits API has no push time. Proposal: "without a push" means the head sha the watch recorded at its previous read is unchanged 45 minutes later.
