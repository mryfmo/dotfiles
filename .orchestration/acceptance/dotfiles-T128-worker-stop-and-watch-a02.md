# Acceptance: dotfiles-T128-worker-stop-and-watch-a02 (plan 006 A7, reset continuation; A6 measured on PR #323)

- **Decision:** parked at 09:32Z (operator, plan 008 decision 2, option D2): PR #323 is a draft at `dc7edcc0`, input for plan 007 T712; not merged.
- pr=323
- **Task:** `af519f0f6b250de6a91fceee8bc480721a8316c01be47b904d577bf0042baa8e`, written by the review seat (`dotfiles-T128-worker-stop-and-watch-redesign-a01`, RESULT 669) as the INV-6 reset successor of a01 (`b0b84598…`): A7-1 to A7-3 unchanged plus A7-4 (threads 4244248703, 4244272551, 4244248706), `tests/fixtures/regime/message-contract.md` in `allowed_files` and the fixture row, a02 bookkeeping, the no-row criterion for 4244248692 in the introduction. `task-consistency-check.py` C1 to C6 `OK` (review seat and orchestrator). Dispatched 02:54Z to `claude-standard-dot-a003`, `.claude/worktrees/worker-f`, branch `docs/worker-stop-and-watch`.
- **A6 clock:** TASK a01 at 01:42Z (history 01:41:55Z); PR #323 draft 01:47:33Z; the clock runs to the merge.
- **Finding-class ledger (moved from the a01 record at 02:54Z; one class per finding; every new finding gets a row before the next acceptance action):**

```text
4244128840	listing-pagination
4244128846	class-count-scope
4244128851	review-text-shell-argument
4244128854	stop-rules-collide
4244128857	evidence-paste-incomplete
4244128859	despawn-dirty-worktree
4244175775	class-count-scope
4244175778	watch-ping-trigger
4244203596	class-count-scope
4244203600	class-count-scope
4244203603	stop-rules-collide
4244203607	watch-ping-trigger
4244203611	class-count-scope
4244203615	class-count-scope
4244248706	result-contract-head
4244248710	watch-audit-source
4244248692	threat-row-outside-paths
4244248694	listing-pagination
4244248703	class-count-scope
4244272551	audit-source-restated
4244354410	watch-pr-number
4244354413	class-scan-timing
4244354417	fix-round-definition
4244378809	result-head-binding
audit:3a54d34:1	fix-round-definition
audit:3a54d34:2	threat-row-outside-paths
audit:3a54d34:3	result-head-binding
audit:3a54d34:4	premise-figure
4244811168	fix-round-definition
4244811164	result-head-binding
4244811155	watch-ping-trigger
4244811161	watch-ping-trigger
4244811170	watch-ping-trigger
```

<!-- audit-input-boundary -->
- **Bot pass 1 on a02's head `1d14eed5` (review 5486194208, 03:0xZ; PONG 675 `status=question`, a02 questions=1): three P1 on the A7 rule sentences, all new classes at one** — 4244354410 (step 7's watch needs the PR number before any message carries it), 4244354413 (the class scan ran only before a fix commit, so a round without a fix could hide the third occurrence), 4244354417 (nothing in step 7 yields the A2 fix-round count). Decision (03:04Z): fix round 1 with the worker's proposed sentences (the PR number from `gh pr list --head <branch>` until the RESULT names it; the scan after every Bot review round; a fix round defined as a push whose predecessor head carries a Codex P0/P1 finding); pre-RESULT, no INV-6 head. A6 note: the two-hour wall from the a01 TASK (01:42Z) ends 03:42Z; with this round, CI, the Bot's pass, the sweep and the audit still ahead, the merge will fall after it by the time those take.
- **Worker commits (checked from the fetched branch):** `1d14eed5` (02:57Z: the a02 task copy at `af519f0f…`; A7-4: badged review bodies P0 to P3 for the class count, the audit-head component "as the counters bullet prescribes", the RESULT line with `head=<full sha>`; three fixtures; tests +20/-3), `3a54d340` (03:06Z, fix round 1: "Until the RESULT names the PR, the watch reads its number with `gh pr list --head <the task's branch> --json number`"; "After every Bot review round, before deciding whether a fix commit follows, the worker lists…"; "A fix round is a push whose predecessor head carries a Codex P0/P1 finding, counted from the PR's commits, the Bot reviews' `commit_id` and the inline comments' `original_commit_id`"; fixtures updated). Diff since `e924c5df` outside `.orchestration`: 5 files, 27 insertions, 9 deletions. CI and the Bot's pass on `3a54d340` pending.
- **RESULT 677 (03:18:33Z, head `3a54d340`):** CI 13 of 13; `bot_rounds=2 fix_rounds=1`; one open P2, 4244378809 (a mandatory `head=` does not prove it is the head that produced the first RESULT; half a threat row, half an orchestrator acceptance check) → `not-applicable` (03:20Z, reply 4244416942): the binding is the orchestrator's acceptance check, performed before every acceptance action (each record pastes `gh pr view` or the fetched branch head beside the RESULT's `head=`; a mismatch is a revise, never counted), and the table's unit is a PR-controlled path; input for B0. All 23 threads of the PR replied (03:19Z to 03:20Z) and resolved; unresolved threads 0.
- **Counters before this acceptance action (03:20Z, `scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a02`, pasted):**
  `task=dotfiles-T128-worker-stop-and-watch-a02 tasks=1 amendments=0 questions=1 results=1 withdrawn=0 revises=0 first_result_head=3a54d340e9078ba3565237f6d73a00d8fc2d75e9 bot_p1_heads_after_result=0 audits=unknown wall=2026-10-12T02:54:30Z..2026-10-12T03:18:33Z (0:24) source=live`
  `detail: pr=323 authors=claude-deep-dot tasks=01a12e08-7a70-73a9-8437-bd8b05332226 results=01a12e1e-7f28-787a-8270-9546f18bd95c questions=01a12e10-3ad0-7b82-8718-e18bb4590029 withdrawn=- bot_heads=- source=live`
  `audits=unknown`: the interim record is the headless audit of this head (`…-a02-audit-3a54d34.md`), pasted below once run. S2: every count under its threshold.
- **Sweep (last step after the replies, 03:21Z, `scripts/pr-feedback.py 323 --json .orchestration/validation/dotfiles-T128-worker-stop-and-watch-a02-pr-feedback.json`, head `3a54d34`):** 85 items, every one dispositioned (20 `fixed:`, 65 `not-applicable:`; from the latest backticked reply in each thread). Pre-audit check (pasted): `sweep gaps 0`, `ledger rows 24; findings 24; gaps 0`. Independent review evidence: `…-a02-crit.json` (one resolved record: the orchestrator's read of `git diff origin/main..3a54d340`, 5 files, 77 insertions, 4 deletions outside `.orchestration`) and `…-a02-review-receipt.md` (03:21:49Z). Audit of `3a54d340` started 03:23Z (the helper's first attempt at 03:21Z exited on an empty lineage glob, fixed).

## Audit of `3a54d340` (03:23Z to 03:31Z, `…-a02-audit-3a54d34.md`, verdict `incorrect`, four findings)

- audit-finding: 1 (P2, SKILL:165: the watcher's fix-round definition counts only pushes after P0/P1 findings while the worker's `fix_rounds` and the A2 cap count a fix after any badged finding; this PR's `2c8dce27 → 040b32f9` followed P2s) → fixed in the revise round: "a fix round is a push whose predecessor head carries a Codex badged finding of any priority".
- audit-finding: 2 (P2, the `not-applicable` on 4244248692 was wrong on two facts: the threat-table rule names orchestrator-controlled in-process effects explicitly, and the forced removal is not behind a human-only gate in this configuration) → fixed by a02 amendment 1: a threat-table row for the forced removal with a verification control (the PR number re-read from the task's branch, the identity's worktree compared with the TASK's `repo=`, the counts re-derived from a fresh listing before any removal; the stopped worktree's evidence preserved; the removal logged in the record); the thread gets a corrected reply.
- audit-finding: 3 (P2, the `not-applicable` on 4244378809 claimed a mismatched RESULT head is "never counted", but `scripts/regime-counters.sh` takes the first RESULT as the baseline permanently) → fixed in the revise round for the contract part (the sentence the thread proposed: the orchestrator checks `head=` against the PR head when the first RESULT arrives; a mismatch is answered with a revise) and recorded as a plan item for the script part (the baseline is the first RESULT whose head the orchestrator confirmed; revise-answered heads are excluded), named in plan 006 Phase 0 and B0; the thread gets a corrected reply.
- audit-finding: 4 (P3, premise 1 of the task record says six reviewed heads after 03:09Z while its own timestamps show four) → fixed by a02 amendment 1 (the figure corrected from the premise's own evidence).
- **Class rows:** the first three findings join existing classes (`fix-round-definition` 2, `threat-row-outside-paths` 2, `result-head-binding` 2); the fourth is `premise-figure` 1. None at three.
- **Counters after this round (expected):** a02 amendments 1 (the row and the premise), revises 1 (the two sentences), questions 1; one more of anything is a reset.
- **A6:** the two-hour wall (01:42Z to 03:42Z) is missed by this round; recorded as not met, with the cause (the orchestrator's two wrong dispositions and the fix-round definition).

## Resumption under plan 008 (operator's choice: option A, continue in place; 2026-10-12 04:5xZ)

- **S7 report and decision:** plan 008 (`.orchestration/plans/008-resume-a7-pr323.md`) presented options A to D; the operator chose A. Plan 007 S5 satisfied first: the four audit findings are instances of M-20261012-1 (fix-round definition, C-8), M-20261012-3 (the two evidence-less dispositions, C-5), M-20261012-4 (the premise figure, C-3) and M-20261012-8 (the forced-removal row, C-11), recorded under `.orchestration/learning/{mistakes,corrections}/` with `index.yaml` (M and C records, every M linked, every C with a mechanism or plan row; 10 M and 11 C after the second S1 cycle and the V0 re-expression).
- **R2 (amendment 1):** the sixth threat-table row (forced removal as the orchestrator's in-process effect, pre-removal verification, the real permission mode stated) and premise 1 corrected to its own output (four heads after 03:09Z); `task-consistency-check.py` C1 to C6 `OK`; the reset record's `design_sha256` moves to the new hash and the review seat re-anchors (round 3).
- **R3 (revise round 1):** two sentences (the fix-round definition at any priority; the contract's first-RESULT head check with a mismatch answered by `status=revise`), fixtures `orchestrator-step-7.md` and `message-contract.md`, `check=` the watch test, the contract test and the whole-section test; dispatched together with the amendment after the anchor.
- **Expected counters after R3's RESULT:** amendments 1, revises 1, questions 1; S7 applies if any further counted finding appears.
- **R2 landed as text (04:54Z):** a02 amendment 1 is `1de19e51b9e23edff9bfc21a64e92a6755ddf247d12c3cf98456bb7629e3878e` (the review seat's round 3 corrected the introduction's 4244248692 sentence, round 4 anchored; `task-consistency-check.py` `OK`). Amendment TASK and the revise-round-1 ACCEPTANCE (`previous_head=3a54d340…`, three `check=` selectors) dispatched to `claude-standard-dot-a003` at 04:54Z; one worker commit expected (task copy, two sentences, two fixtures, tokens).
- **RESULT 688 (05:08:22Z, revise round 1 + amendment 1, head `dc7edcc0`):** one commit (task copy `1de19e51…`, the two sentences, `orchestrator-step-7.md` and `message-contract.md`, tokens, evidence); CI 13 of 13; audit findings 1 and 3 `fixed:dc7edcc0`; the Bot's pass on `dc7edcc0`: five P2, no P0/P1 (INV-6 heads 0): 4244811168 (step 7's any-priority fix round contradicts step 15's P0/P1 fix cap: one rule in both playbooks), 4244811164 (`regime-counters.sh` reads `results[0]`, so a revise does not drop a stale `head=`; script outside `allowed_files`), 4244811155 (step 7 should state the sixth row's pre-removal checks), 4244811161 (a push in flight at the PING reads as continued pushing), 4244811170 (the commits API has no push time; "without a push" undefined). Counters: amendments 1, revises 1, questions 1, heads 0; any text fix is a second revise or amendment (reset).
- **Plan 007 S7 (second S1 cycle on this task):** ledger classes now at three or more: `fix-round-definition` 3 (4244354417, audit 3a54d34:1, 4244811168), `result-head-binding` 3 (4244378809, audit 3a54d34:3, 4244811164), `watch-ping-trigger` 5 (4244175778, 4244203607, 4244811155, 4244811161, 4244811170), after `class-count-scope` 7 earlier. The orchestrator stops: no dispatch, amendment, reset or disposition; the report and options are plan 008 "Decision 2". Worker held at 05:09Z.
- **Decision (operator, plan 008 decision 2, option D2; executed 09:32Z):** PR #323 parked as a draft at `dc7edcc0` as input for plan 007 T712 (step 7 and step 15 as state and transition tables, one Phase B task on a new branch). Corrected, evidence-bearing replies posted on 4244248692 (4246521761) and 4244378809 (4246521974); the five P2 threads of the last pass stay open on purpose as T712's rows; a park comment on the PR names the decision. Worker released (`status=superseded`, stays seated idle). a02 counters at the park: amendments 1, revises 1, questions 1, INV-6 heads 0; no reset.
- **A6 on this PR (final, not met):** TASK a01 01:41:55Z to the park 09:32Z (the operator's halt 03:3xZ to 04:4xZ and the decision wait 05:10Z to 09:3xZ included; the working wall to the last Bot pass was about 3 h 27 min); Bot passes 8 (`9d001bcb`, `2c8dce27`, `040b32f9`, `3ba70625`, `e924c5df`, `1d14eed5`, `3a54d340`, `dc7edcc0`); INV-6 heads after the first RESULT 0 on a01 and a02; resets 1; S1 cycles 2; audits 1 (`incorrect`, four findings, two of them the orchestrator's). Criterion "rounds ≤ 2, heads ≤ 2, wall ≤ 2 h, audit correct": heads met, the rest not; the measurement moves to the T712 PR (plan 007 C-8).
