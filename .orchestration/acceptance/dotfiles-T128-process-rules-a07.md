# Acceptance: dotfiles-T128-process-rules-a07 (sixth continuation of PR #318; plan 006 Phase A: A1, A2, A4)

- **Decision:** accepted at 01:40Z on head `92634b25` (audit `correct`, no findings; sweep 148 of 148 dispositioned; ledger 49 of 49); gate and merge below.
- pr=318
- **Task:** `d5d499cead2297a8357b243d46172f8fea7cb929b4e4a62addb71633f3babb6a`, written by the review seat (`dotfiles-T128-process-rules-redesign-a06`, RESULT 643) as the INV-6 reset successor of a06: a06 (`90fb32c2…`, items 1 to 10) plus the sixth threat-table row (the branch evidence records, the worker's wording on thread 4243975211), the SKILL row naming its path, `design_review.receipt` round 18, a07 bookkeeping, and the sentence that the table names every `allowed_files` entry. `task-consistency-check.py` C1 to C6: `OK` (review seat and orchestrator). Dispatched 01:18Z to `claude-standard-dot-a003`, `.claude/worktrees/worker-f`, branch `docs/regime-pattern`.
- **Reset lineage:** a01 → a02 → a03 → a04 → a05 → a06 → a07: six resets (a01 INV-6 and S1 together; a02 INV-6 amendments; a03 INV-6 Bot heads; a04 plan S1; a05 INV-6 questions; a06 INV-6 amendments; the `bookkeeping` S1 caused no reset of its own); records `…-a0{1,2,3,4,5,6}-design-reset.md`; cause records under `.orchestration/learning/` (`plan-006-s1-process-rules-counters-bullet-2026-10-11.md`, `plan-006-s1-pr318-finding-classes-2026-10-12.md`).
- **Finding-class ledger:** below (47 rows at 01:19Z, moved from the a06 record); every new finding on this PR gets a row before the next acceptance action; the pre-audit check reads this record.
- **Exemption declared:** acceptance and evidence-sync bookkeeping; agmsg control plane.


## Finding-class ledger of PR #318 (moved from the a06 record at 01:19Z; the a05 and a06 records keep the audit narratives; 49 rows: the 45 the ledger check derives plus 4243885108, 4243923211, 4243923214 and 4243975211, Bot findings newer than the last sweep)

### Finding-class ledger (one class per finding, by content; `audit:<sha7>:<n>` = the n-th `[P` line of that audit's `.last.md`)

```text
4240250137	tool-not-on-main
4240250141	step15-wait
4240269216	scope
4240269218	third-round-outcome
4240269219	unpinned
4240269222	sources
4240290382	third-round-outcome
4240290387	grammar
4240290391	step15-wait
4240321113	scope
4240334094	scope
4240334098	unpinned
4240348412	sources
4240348414	third-round-outcome
4240382519	sources
4240566259	threat-table-missing
4240566263	unpinned
4240566266	step15-wait
4240566268	unpinned
4240598178	tool-not-on-main
4240598179	sandbox
4240646079	step15-wait
4240646082	grammar
4243369347	step15-wait
4243516879	sources
4243516880	step15-wait
4243537278	sources
4243537279	freeze
4243537281	boundary
4243631335	sources
4243732324	freeze
4243732326	scope
4243732330	contract
4243885108	bookkeeping
4243923211	bookkeeping
4243923214	bookkeeping
4243975211	bookkeeping
audit:27ea99b:1	scope
audit:27ea99b:2	tool-not-on-main
audit:27ea99b:3	unpinned
audit:27ea99b:4	evidence
audit:27ea99b:5	sandbox
audit:b7ae2d5:1	grammar
audit:b7ae2d5:2	step15-wait
audit:b7ae2d5:3	unpinned
audit:b7ae2d5:4	evidence
audit:4af8939:1	evidence
audit:4af8939:2	unpinned
audit:4af8939:3	evidence
```

### Classes at three or more (plan 006 S1), with status (nine classes; `bookkeeping` is the ninth, added 00:55Z and 01:10Z)

- `unpinned` (7: 4240269219, 4240334098, 4240566263, 4240566268, audit 27ea99b:3, b7ae2d5:3, 4af8939:2): S1 open at this audit → changed task: a05 item 10 (sections pinned whole). Cause: token tests pin the clauses their author chose; every new sentence brings an unpinned clause and the auditor's mutation test finds it.
- `step15-wait` (7: 4240250141, 4240290391, 4240566266, 4240646079, 4243369347, 4243516880, audit b7ae2d5:2): S1 was reached at the third (4240566266, 06:44Z) and not recognized; every finding was fixed in a worker fix round (last `114d5b91`); none open. Cause: Worker Playbook step 15 is an imperative procedure (timer start, CI watcher, draft/ready, review filter, retry) written clause by clause, and each Bot pass found the next edge. Changed plan step: step 15 is pinned whole by item 10; A7 (the next change to step 15) updates that fixture, and a further finding of this class on A7's PR stops A7 for a re-specification of step 15 as one state machine (Phase B input).
- `scope` (5: 4240269216, 4240321113, 4240334094, 4243732326, audit 27ea99b:1): S1 reached at the third (4240334094, 05:03Z), not recognized; fixed in rounds (last `1fdebcb0`); none open. Cause: the threat-table review protocol is restated in three places (two AGENTS bullets, the SKILL threat-table bullet). Changed plan step: the AGENTS subsection is pinned whole by item 10; V1 (the schema) becomes the single owner of the shape and the AGENTS bullets shrink to one review sentence and a pointer when V1 lands (plan Phase 3 note).
- `evidence` (4: audit 27ea99b:4, b7ae2d5:4, 4af8939:1, 4af8939:3): S1 on the orchestrator's own acceptance evidence → changed plan step: the ledger check and the zero-gap fill gate `orch-audit.sh` from now on (interim record until V2b's gate reads the JSON).
- `sources` (6: 4240269222, 4240348412, 4240382519, 4243516879, 4243537278, 4243631335): S1 recognized at the sixth (23:08Z); reset to a05 by the review seat; closed by `dfdee38b`. (The earlier records listed 4240250137 in this class; by content it is `tool-not-on-main`, and 4240269222 belongs here.)
- `third-round-outcome` (3: 4240269218, 4240290382, 4240348414): S1 reached at the third (05:09Z), not recognized; closed when a03 defined the outcome (`open:<id>` is a sweep item, step 10.1; `c31b8327`). Cause: A2's cap created a state with no defined outcome.
- `tool-not-on-main` (3: 4240250137, 4240598178, audit 27ea99b:2): S1 reached at the third (05:4xZ), not recognized; closed by the INV-2 correction (07:25Z) and the merge order (A5 `0e522059`, A3 `52575497`); the a05 bullet names no tool fallback. Changed plan step (Phase 0): a rule that requires a tool is dispatched after the tool is on `main`.
- `grammar` (3: 4240290387, 4240646082, audit b7ae2d5:1): S1 recognized at a01's reset (a01 → a02 by the review seat, the disposition grammar left to the schema); the third fixed by `386f97ff`; closed.
- Under three: `freeze` 2 (4243537279, 4243732324; a third stops the sentence), `sandbox` 2 (4240598179, audit 27ea99b:5), `boundary` 1, `contract` 1, `threat-table-missing` 1.
- **Amendment 1 (00:19Z, a05 → `5b17e7bda1c3cd38de247260b3a557ae110509931f56ce1daacb579f7b2259db`):** item 10 (five golden section fixtures under `tests/fixtures/regime/` and `test_regime_rule_sections_are_pinned_whole`; `allowed_files` gains the fixtures; Validation items 1 to 10; Completion's revise-round sentence); the `unpinned` class's changed task under plan S1. Scoped Codex round on item 10 and the review seat's re-anchor (round 5) requested 00:19Z; the revise ACCEPTANCE (`previous_head=4af89390`, `check=tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_regime_rule_sections_are_pinned_whole`) and the amendment TASK follow their accept. Expected counters after the round: a05 amendments 1, revises 1, questions 1.
- **Scoped Codex round on item 10 (`…-a05-taskfile-review-codex-round4.md`, 00:23Z): `revise`, two findings, both applied verbatim as a05 amendment 1 v2 (`d2bc02ccee035fea58aba8c6e49fadc7a75d7b6bfca5f1c192b02a23319099de`):** P1 (the branch task-copy directory was absent from `allowed_files`, as in every a0N file before it) → `.orchestration/dotfiles-T128-process-rules-a05/**` added; P2 (two fixture boundaries underspecified) → step 15 ends at the next `## ` heading (the playbook's last step; "## Codex seat worklogs" at line 210 of the SKILL at `4af89390`) and the AGENTS subsection runs to the end of the file (its last section, from line 75). No further Codex round: the remedies are the review's own text. The reset record and the review seat's anchor (round 6) follow this hash.
- **Review seat round 6 (00:22:54Z) on `d2bc02cc…`: `revise`, one item introduced by the P2 remedy ("likewise" for step 7 now pointed at step 15's boundary):** applied verbatim (step 7 runs from its numbered line to `8. `, the Orchestrator Playbook sliced first because the Worker Playbook has a step 7 too); a05 is now `71ca5df01db48361a5c6ea140faebeede70fa0fb41f00f78d280bd9ba13024fe`; round 7 anchors it.
- **Dispatch of the revise round (00:25Z):** amendment TASK (`71ca5df0…`, anchored by RESULT 614) and `AGMSG-ACCEPTANCE status=revise round=1 previous_head=4af89390… check=tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_regime_rule_sections_are_pinned_whole` sent to `claude-standard-dot-a003`.

<!-- audit-input-boundary -->
- **RESULT 651 (01:31:15Z, head `92634b25`):** one commit (the a07 copy at `d5d499ce…` and evidence; checked from the branch: no change outside `.orchestration`; SKILL and AGENTS.md unchanged since `4af89390`; the only tree change since the audited head is item 10's `07b2160b`, 6 files, 125 insertions under `tests/`); CI 13 of 13; the Bot's pass on `92634b25` completed 01:22:27Z with no comment; `bot_rounds=1 fix_rounds=0`; no open thread. Replies posted 01:32Z on the four task-record threads (4243885108 `fixed:3a4ebdbb`, 4243923211 and 4243923214 `fixed:f755d714`, 4243975211 `fixed:92634b25`) and the four threads resolved; every thread of the PR is now answered and resolved.
- **Counters before this acceptance action (01:32Z, `scripts/regime-counters.sh dotfiles-T128-process-rules-a07`, pasted):**
  `task=dotfiles-T128-process-rules-a07 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=92634b25e11eb1f097513ea0ae9d379d084981c2 bot_p1_heads_after_result=0 audits=unknown wall=2026-10-12T01:17:57Z..2026-10-12T01:31:15Z (0:13) source=live`
  `detail: pr=318 authors=claude-deep-dot tasks=01a12db0-1588-74d8-8407-dad5fea85bd4 results=01a12dbc-42b8-72c3-8eb1-04a93623bad2 questions=- withdrawn=- bot_heads=- source=live`
  `audits=unknown`: INV-6's audit source has no entry (V2 not landed); the interim record is the headless audit of this head, `…-a07-audit-92634b2.md`, pasted below once it has run, beside the predecessor audit of `4af89390` (three findings, all dispositioned in the a05 record). S2: every count at zero.
- **Sweep (last step after the replies, 01:32Z, `scripts/pr-feedback.py 318 --json .orchestration/validation/dotfiles-T128-process-rules-a07-pr-feedback.json`, head `92634b2`):** 148 items, every one dispositioned (36 `fixed:`, 112 `not-applicable:`; dispositions taken from the latest backticked reply in each thread, the orchestrator's own replies and the review objects marked as non-findings). Pre-audit check (pasted): `sweep gaps 0`, `ledger rows 49; findings 49; gaps 0` (every Bot top-level finding of the sweep and every `[P` line of the a02, a03 and a05 audits has a class row). Audit of `92634b25` started 01:33Z from the clean review worktree (`orch-audit.sh`, output `…-a07-audit-92634b2.md`).

## Audit of `92634b25` (01:33Z to 01:40Z, `…-a07-audit-92634b2.md`, verdict `correct`)

- audit-finding: none (approval: "no remaining findings"; the four clause removals fail the fixture test; the 49-row ledger matches the 37 Bot findings and 12 prior audit findings; every `allowed_files` entry has threat-table coverage; live GitHub feedback matches the sweep; final-head CI passed; INV-1, 2, 3, 5, 6, 7, 8, 12 hold). The first `correct` audit of a Phase A head.
- **Interim audit record for INV-6's `audits` component:** the audits of this PR's lineage are `27ea99b2` (a02, `incorrect`, 5 findings), `b7ae2d54` (a03, `incorrect`, 4), `4af89390` (a05, `incorrect`, 3) and `92634b25` (a07, `correct`, 0); P0/P1 implementation or specification findings after a07's first RESULT head: none (the one P1 of `4af89390` was an orchestration finding on a predecessor's head). S2 by this reading: no audit threshold reached.
- **Decision:** accepted at 01:40Z on head `92634b25` (the final head). Gate and merge follow.
- **Independent review evidence:** `.orchestration/validation/dotfiles-T128-process-rules-a07-crit.json` (one resolved record: the orchestrator's read of `git diff origin/main..92634b25`, 8 files, 416 insertions, 7 deletions outside `.orchestration`) and `…-a07-review-receipt.md` (`review_surface: crit-data`, head `92634b25…`, 01:39:42Z).
- **Gate (01:40:18Z, `orch-gate.sh dotfiles-T128-process-rules-a07 92634b25… 318` from the review worktree checked out at the head, after cleaning the audit's 15 copied record files out of it; pasted):**
  `PR feedback evidence accepted: .orchestration/validation/dotfiles-T128-process-rules-a07-pr-feedback.json`
  `Audit evidence accepted: .orchestration/validation/dotfiles-T128-process-rules-a07-audit-92634b2.md`
  `Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.`
  `gate rc=0`
- **Merge (01:40:38Z):** `gh pr merge 318 --squash --match-head-commit 92634b25e11eb1f097513ea0ae9d379d084981c2` → `main` `e83e923d`; `git diff origin/main 92634b25 -- . ':!.orchestration'` empty (the merged tree equals the audited head outside the records). A1, A2 and A4 are on `main`. Worker `claude-standard-dot-a003` accepted 01:41Z and re-tasked with A7 on a fresh branch from `e83e923d`.
- **A6 figures for this PR (for the plan's self-verification row; the wall is the whole PR, five resets included):** task a01 dispatched 2026-10-11T04:16:13Z (history), merged 2026-10-12 01:40:38Z; 48 commits; 18 Codex review passes with findings on 18 distinct heads (`gh api …/pulls/318/reviews`, bodies containing "Codex Review"); Bot P0/P1 heads after each task's first RESULT: a01 and a02 reset before a RESULT-relative count applied, a03 2 (reset), a04 2 (the successor's heads), a05 1, a06 1, a07 0; audits 4 (`27ea99b2` incorrect, `b7ae2d54` incorrect, `4af89390` incorrect, `92634b25` correct); resets 6 (INV-6 on a01, a02, a03, a05, a06; S1 on a01 and a04); rounds per task under the A2 cap throughout (fix rounds ≤ 1 per head). The ≤ 2 h wall is not met by this PR; it is measured again on A7's PR, the first dispatched with the consistency check and the whole-section fixtures in place.
