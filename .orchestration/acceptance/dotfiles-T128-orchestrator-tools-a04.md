# Acceptance: dotfiles-T128-orchestrator-tools-a04 (T718 first slice, INV-6 successor of a01 and a03; plan 016 option G′; a02 is the second slice)

- Task file pair-confirmed at `d0a26050132a32ddc8d3b397b31f3a815bdaed1a55867daa4d81551f15e14fd7` (review seat `dotfiles-T128-orchestrator-tools-redesign-a02` rounds 1 to 5, RESULT bus 917; Codex rounds 1, 2 and 4 `revise`, 5 `confirm`, receipts `dotfiles-T128-orchestrator-tools-redesign-a02-codex*.md`). Reset record `dotfiles-T128-orchestrator-tools-a03-design-reset.md` anchored on bus 917. Boundary (10) PR #345 merged 07:59:10Z as `d25c3df8` with a04, a02 (item 6), the reset record, plan 016, M-20261012-33 / C-32.
- Dispatch 2026-10-13 07:59:15Z (bus 919, read 07:59:25Z) to `claude-standard-dot-a003` (worker-c, w5:pA) by `a04-t718-dispatch.sh` after the file matched `origin/main` `d25c3df8`: same branch `tools/orchestrator-scripts`, same PR #336, the worker's head `ba4d4762` and commits stay; delta = the four fixes (bus-read.sh's closing rule and status set, three-repeat.sh's body search and stated memory cap, dispatch.sh's record-destination check and record-block grammar), six tests, the a04 task copy and evidence.
- Integration after its RESULT (`finish-336c.sh <extra.tsv>`): update-branch by ancestry, CI, Bot, the C-32 local review (`local-review.sh`), the sweep with the dispositions (the 20 rows of a03's ledger, the three threads and the local finding as `fixed:<sha>`), one revise round at most, residual P2 owned by a02 item 6 (on main), review receipt, one audit of the final head, gate, `gh pr merge --squash --match-head-commit`, ff, then `integrate-328.sh <squash>` and `integrate-329.sh <T703 squash>`. No boundary while PR #336 is between its update-branch and its merge (`awaiting-merge/336` marker).
- 08:05Z INV-10 baseline: PR #336 head `0d199475`; the worker's last bus event is its read of the TASK (07:59:25Z).
- 08:24:38Z INV-10 check: PR #336 head still `0d199475` (last commit on the branch ba4d4762, 05:19Z); no bus event from a003 since its read of the TASK (07:59:25Z), 25 minutes; no PING yet (the median worker round is 20 to 45 minutes; a PING at 30 minutes of silence without a push).
- 08:41Z INV-10: PR #336 head moved to `5b99a744` (3d131215 merge of origin/main 08:04Z; 05e3292f the a04 fixes 08:30Z; 5b99a744 the a04 task copy and evidence 08:38Z); CI running; the push is the activity, no PING. The C-32 local review runs once on this head now (one sample per head), so its findings reach the worker with the Bot's in the one revise round.
- 08:41:17Z C-32 local review of `5b99a744` (`dotfiles-T128-orchestrator-tools-a04-local-review-5b99a74.md`, 81 s, one sample per head): one P2, `bus-read.sh:60`: a later `AGMSG-ACCEPTANCE status=revise` between unrelated endpoints becomes the opener (`max_by(.i)` over every TASK or revise row), so the original worker's RESULT no longer closes the task; the fix: a revise opens only between the endpoints of the task's latest TASK. Valid against the head (the rule text binds closers, not openers, to the pair). It returns to the worker with the Bot's threads in a04's one revise round (plan 016 G′).

local:5b99a74:1	duplicated-state-machine
- 08:46Z Bot review on `5b99a744` (CI still running): four P2 threads: 4256541708 (`test_orchestrator_tools.py:234`, the unwritable-directory test passes as root: make the denial deterministic), 4256541716 (`dispatch.sh:60`, a NUL byte in the line file is dropped by command substitution: reject it), 4256541723 (`bus-read.sh:52`, the row regex accepts any first token, the grammar allows only `●` and `○`), 4256541725 (`dispatch.sh:126`, a `previous_design_sha256=` reference is treated as an artifact binding: a02 item 4's grammar row, on main, owns it). Under plan 016 G′ the one revise round of a04 carries the local finding and the first three; 4256541725 is `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 4`. Class counts on the lineage after these rows: `input-validation` reaches 5; plan 016 G′ (07:16Z) governs the residual path (no further revise; residual P2 of the revise head owned by a02 item 6), so no new S7 is raised for the same artifact (08:48Z).

4256541708	environment-dependent-test
4256541716	input-validation
4256541723	grammar-not-enforced
4256541725	input-validation
- 08:55:15Z RESULT (bus 920): head `5b99a744` (3d131215 origin/main merged; 05e3292f the four fixes; 5b99a744 the task copy and evidence), CI 13 of 13, Bot review 5500993250 (08:46:05Z, four P2, no P0/P1), `bot_rounds=1`; threads 4255494133, 4255494139, 4255494137 and the local finding on 0d199475 `fixed:05e3292f`; the four new threads reported open and valid for the revise round; tests 16 OK, counters 26 OK, mutants 15 of 15 killed; caps 6 files, 378 lines outside tests, 468 under tests; counters logic unchanged. 08:56:12Z ACCEPTANCE `status=revise` (bus 921 read_at=2026-10-13T08:56:07Z): a04's one revise round carries the local finding (bus-read.sh:60, revise openers bound to the task's endpoints) and all four Bot threads, 4256541725 included (fixed per a02 item 4's grammar row rather than owned: a fix beats an owner; the worker reports seven design-review TASK lines on the bus that dispatch.sh would refuse). INV-6 for a04 after this: `revises=1`; residual P2 of the revise head are owned by a02 item 6.

## Ledger (machine rows id<TAB>class; the lineage a01 → a03 → a04 on PR #336: the 23 rows of a03's record, carried here because ledger-check reads this record alone; a04's own rows are above and below)

4253994697	trusted-checkout
4253994704	threat-row-unit
4254107304	input-validation
4254107312	record-form
4254163604	hash-binding
4254399800	hash-binding
4254399805	agmsg-invocation
4254399807	record-association
4254494989	hash-binding
4254494999	threat-row-missing
4254771284	input-validation
4254771296	record-association
4254771302	hash-binding
4254844587	record-association
4254844595	atomic-write
4254893065	input-validation
4255079204	ledger-shape
4255272793	record-association
4255272797	record-association
4255272803	record-association
4255494133	duplicated-state-machine
4255494137	default-limited-read
4255494139	duplicated-state-machine
- 09:2xZ the operator pasted a003's pane: "API Error: Your computer went to sleep mid-response" after its RESULT, with a recap "I wait for the orchestrator's revise-round message" although the revise ACCEPTANCE (bus 921) was read by its hook at 08:56:07Z: the delivery landed in a turn the sleep cut. PING sent 09:22:59Z (bus 922, read 09:23:05Z) naming bus 921 and the five fixes; the PONG or the push is the next event; the INV-10 silence check would have fired at 09:26Z.
- 09:23:13Z PONG (bus 923): `status=alive revise=1`, the five fixes committed as `e2e67de8` (not yet pushed: revise openers bound to the latest TASK's endpoints, markers ● ○ only, NUL refused exit 2, `previous_<name>_sha256` hex-only, the unwritable-record test root-independent), 16 tests OK, 21 of 21 mutants killed, shellcheck/shfmt/ruff clean; next the evidence files, the push, CI, the Bot wait, the RESULT. The sleep cut the turn after the fixes, before the evidence.
- 09:36:36Z revise RESULT (bus 924): head `3e5cad37` (fix commit `e2e67de8`), CI 13 of 13, Bot review 5501536934 (09:32:57Z, three P2, no P0/P1), `bot_rounds=2`; the five findings of the round `fixed:e2e67de8` with their tests (the local finding by `test_bus_read_ignores_closers_between_other_endpoints`; 4256541708 by `test_dispatch_refuses_an_unwritable_record_before_sending`; 4256541716 by `test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line`; 4256541723 by `test_bus_read_skips_and_counts_malformed_rows`; 4256541725 by `test_dispatch_passes_the_line_byte_identical` and `test_dispatch_refuses_malformed_lines`); 16 tests OK, counters 26 OK, 21 of 21 mutants killed; caps 6 files, 393 outside tests, 485 under tests. The Bot's round on the final head: 4256987062 (bus-read.sh: the limit checked after the shape filter), 4256987076 (the silence clock counts rows between other endpoints), 4256987087 (dispatch.sh: CRLF record prose rewritten as LF): the residual P2 of a04's final head after its one revise round, each `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02 item 6` (a02 on main `d25c3df8`), as the Completion clause and plan 016 G′ define; no further revise (INV-6: `revises=1`).

4256987062	input-validation
4256987076	duplicated-state-machine
4256987087	record-form

local-finding: 5b99a74:1 fixed:e2e67de8 (local review of 5b99a744, bus-read.sh:60: a revise ACCEPTANCE opens only between the endpoints of the task's latest TASK; test_bus_read_ignores_closers_between_other_endpoints)
- 09:4xZ dispositions complete for the final head `3e5cad37`: 30 rows in the sweep table (16 `fixed:` from a01/a03, 3 `fixed:05e3292f`, 5 `fixed:e2e67de8` counting the local finding's line, 4 owned by a02 items 3 and 4, 3 owned by a02 item 6), every id in the ledger and the ledger's ids all in the table; `local-finding: 1 fixed:e2e67de8`. `finish-336c.sh` started: the C-32 local review of 3e5cad37 (one sample), the sweep, the review receipt, one audit, the gate, the merge bound to the head, ff, then `integrate-328.sh`.
- 09:4xZ ACCEPTANCE `status=pending-integration` sent to a003 (C-30's form: the Stop gate wants a line per RESULT before the turn ends, the integration is not done; `accepted` follows the merge; the worker holds at 3e5cad37, no push).
-  C-32 local review of the final head `3e5cad37` (`dotfiles-T128-orchestrator-tools-a04-local-review-3e5cad3.md`, one sample): one P2, `regime-counters.sh:130-132`, malformed ledger rows used before validation: the ledger-shape guard a02 item 3 owns on main (thread 4255079204). The 0d199475 local review (dispatch.sh:187) gets its row and line here too (the audit's finding 3). Audit of 3e5cad37 (`dotfiles-T128-orchestrator-tools-a04-audit-3e5cad3.md`): `Verdict: incorrect`, three P2: (1) `bus-read.sh:56` splits the body on literal spaces while the stop gate tokenizes runs of whitespace (a residual P2 of the final head, owned by a02 item 6 with the three Bot threads of the same head); (2) the revise lacked the pasted counters and the S6 searches; (3) the ledger omitted the 0d199475 local finding. Findings 2 and 3 are addressed below in this record; finding 1 is owned. The gate refused the first pass on exactly these dispositions (`AUDIT_DISPOSITIONS leaves audit findings 1, 2, 3 without a disposition`), as designed; the chain's own verdict match (`*correct)` matching `incorrect`) let it reach the gate and is fixed in the scripts (M-20261012-35 candidate: a glob that matched its negation).

local:0d19947:1	input-validation
local:3e5cad3:1	ledger-shape
audit:3e5cad3:1	input-validation
audit:3e5cad3:2	search-procedure
audit:3e5cad3:3	ledger-completeness

local-finding: 0d19947:1 fixed:05e3292f (local review of 0d199475, dispatch.sh:187: the record destination checked before the send; test_dispatch_refuses_an_unwritable_record_before_sending)
local-finding: 3e5cad3:1 not-applicable:owned by dotfiles-T128-orchestrator-tools-a02 item 3 (the counters trust a ledger block only when every row is an object with a string id and a slug class; thread 4255079204); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md | grep -n 4255079204

audit-finding: 1 not-applicable:owned by dotfiles-T128-orchestrator-tools-a02 item 6 as a residual P2 of a04 final head 3e5cad37 after its one revise round (bus-read.sh:56 tokenizes the row body on runs of whitespace as the stop gate does; the same script and class as the three Bot threads of that head owned by item 6; ledger row audit:3e5cad3:1); evidence=git show origin/main:.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md | grep -n 'item 6'
audit-finding: 2 not-applicable:addressed in this record at 09:51Z: the counters of a04 and a03 and the S6 searches for the four classes at three or more on the lineage (record-association 6, input-validation 6, hash-binding 4, duplicated-state-machine 4) are pasted below; every search returns M-20261012-32 or M-20261012-33, the records of this artifact own cycles (C-31, C-32), and plan 016 G′ (operator, 07:16Z) is the decision taken after them for this artifact: one revise round, residual P2 owned by a02 item 6; evidence=sed -n "/S6 searches for the final head/,/^```$/p" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md
audit-finding: 3 not-applicable:addressed in this record at 09:51Z: the 0d199475 local finding has its ledger row local:0d19947:1 and its line local-finding: 0d19947:1 fixed:05e3292f, and the 3e5cad37 local review its row local:3e5cad3:1 and line; evidence=grep -n "^local" .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a04.md

- S6 searches for the final head (pasted 09:51Z):

```text
$ scripts/regime-counters.sh dotfiles-T128-orchestrator-tools-a04 --pr 336
task=dotfiles-T128-orchestrator-tools-a04 tasks=1 amendments=0 questions=0 results=2 withdrawn=0 revises=1 first_result_head=5b99a7443b255426569724f15822dfb3e248411c bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-13T07:59:15Z..2026-10-13T09:36:36Z (1:37) source=live
detail: pr=336 authors=claude-deep-dot tasks=01a13445-d838-7177-8f19-6e6eddce91bf results=01a13479-1d38-70b4-88ad-4e114050b227,01a1349e-f8a0-7cf8-84e6-b9ca4d605373 questions=- withdrawn=- bot_heads=- source=live
$ scripts/regime-counters.sh dotfiles-T128-orchestrator-tools-a03 --pr 336
task=dotfiles-T128-orchestrator-tools-a03 tasks=2 amendments=1 questions=0 results=2 withdrawn=0 revises=1 first_result_head=c8fb09b00bc3e79fdce2f23617c3e6aadaa55e5e bot_p1_heads_after_result=unknown audits=unknown wall=2026-10-13T04:25:32Z..2026-10-13T05:36:13Z (1:10) source=live
$ class counts over the a04 record's ledger rows (id<TAB>class, lineage a01 → a04, PR #336)
   6 record-association
   6 input-validation
   4 hash-binding
   4 duplicated-state-machine
   2 record-form
   1 trusted-checkout
   1 threat-row-unit
   1 threat-row-missing
   1 ledger-shape
   1 grammar-not-enforced
   1 environment-dependent-test
   1 default-limited-read
   1 atomic-write
   1 agmsg-invocation
$ /usr/bin/grep -rl 'classes:.*duplicated-state-machine' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-33.md
$ /usr/bin/grep -rli -- 'duplicated-state-machine' .orchestration/learning/mistakes/ | wc -l
1
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- duplicated-state-machine | grep -cE '^[0-9a-f]{8}-'
0
$ /usr/bin/grep -rl 'classes:.*hash-binding' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-32.md
$ /usr/bin/grep -rli -- 'hash-binding' .orchestration/learning/mistakes/ | wc -l
1
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- hash-binding | grep -cE '^[0-9a-f]{8}-'
0
$ /usr/bin/grep -rl 'classes:.*input-validation' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-32.md
$ /usr/bin/grep -rli -- 'input-validation' .orchestration/learning/mistakes/ | wc -l
1
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- input-validation | grep -cE '^[0-9a-f]{8}-'
0
$ /usr/bin/grep -rl 'classes:.*record-association' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-32.md
$ /usr/bin/grep -rli -- 'record-association' .orchestration/learning/mistakes/ | wc -l
1
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search --limit 1000 -- record-association | grep -cE '^[0-9a-f]{8}-'
0
```
- 09:5xZ gate passes 1: `AUDIT_DISPOSITIONS leaves audit findings 1, 2, 3 without a disposition` (the lines were not yet written; the chain's verdict match `*correct)` had matched `incorrect`, M-20261012-35); pass 2 after the dispositions: gate rc=0, then GitHub refused the merge: `required_review_thread_resolution` (30 Bot threads open). `resolve-threads.sh 336 336-extra-a04.tsv`: one reply per thread with its disposition, every thread resolved (09:5xZ); the sweep re-run (113 items: the 60 new ones are the replies and their review objects, dispositioned by fill_sweep's orchestrator-reply rule), gate rc=0, **merged 09:56:27Z as `a03c1daa`** (`gh pr merge --squash --match-head-commit 3e5cad37`). Main fast-forwarded to `a03c1daa`; the awaiting-merge marker cleared. ACCEPTANCE `status=accepted` sent to a003 (09:58Z); a02 (the second slice, pair-confirmed a4c929b1…) dispatched to a003 on a fresh branch from origin/main. T703's chain (`integrate-328.sh a03c1daa`) started.
-  residual R1 of the tools lineage (from PR #328 thread 4249414388, raised against T703's rule text and refuted there because the text no longer prescribes a grep): `three-repeat.sh` matches the class as a substring (`^classes:.*<class>`: `scope` also matches `class-count-scope`); the body search of a04 (`grep -rli -- <class>`) has the same property by design. Owner: the tools task after a02 (not yet written; a02 item 6 is defined by this ledger's owned rows only), named here so the next task text carries it.
