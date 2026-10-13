# Plan 012: T703 (PR #328) after a further S1 cycle on its a04 head: the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Nothing below is executed until the operator chooses. Every figure is pasted command output of 2026-10-12.
>
> **Drift check (at planning time, 16:12Z)**: `origin/main` `3709a6d8`; PR #328 `OPEN`, head `2276a365` (`mergeStateStatus=BEHIND`), CI 12 of 12 green on it; Bot review `5493270947` on `2276a365` at 16:03:26Z, one new thread (4250028600, P1); worker `claude-standard-dot-a003` RESULT `status=ready_for_review head=2276a365` at 16:04:45Z (bus 779). PR #329 (T702 a03, `claude-standard-dot-a002`): no bus event and no push since the TASK at 15:41:03Z; PING sent 16:10Z (INV-10).

## Status

- **Execution**: DECIDED 2026-10-13 01:05Z: option B (operator, AskUserQuestion). R1 done 01:18Z (a01 re-scoped: dispatch.sh, three-repeat.sh, bus-read.sh, counters slug; a02 drafted; C1 to C10 OK); R2 review pair: round 1 revise (seat 3 findings, Codex 1), round 2 confirm ×2 (seat 01:25:29Z, Codex); R3 boundary PR #334 merged (`480aabc0`); R4 T718 dispatched to a003 01:35:23Z (`t718-dispatch.sh`, hash from the file). R5: T718 a01 RESULT 02:46:54Z (head 5b6d5f24, CI green, three open Bot threads that are task text → amendment 1, review pair in progress); integration after the amendment's worker round; the amendment line went to a003 03:13:58Z (bus 854) after boundary PR #338. a04 (PR #328) held meanwhile.
- **Priority**: P1 (T703 blocks T702's integration order and T718's `after:`)
- **Planned at**: main `3709a6d8`, 2026-10-12 16:12Z

## Situation

- Counters at 16:07:36Z: `task=dotfiles-T128-playbook-rules-a04 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=2276a365cba9f104cadd7cd82f3fb0bfec7dac21 bot_p1_heads_after_result=0 audits=unknown wall=2026-10-12T15:40:52Z..2026-10-12T16:04:45Z (0:23) source=live`. INV-6 allows a04 one amendment or one revise; the second is a reset to a05.
- The new thread, 4250028600 (P1, `SKILL.md:74`, 16:03:26Z): "`scripts/regime-counters.sh:145-147` emits the first three title words verbatim (the existing unit test expects `class=reject skipped contract`), while this rule requires the triggered class to be a `[a-z0-9-]` slug assigned during disposition. When that counter path reaches three, 'search for that class' therefore supplies a non-slug with no defined mapping to the ledger class". Verified: `git grep -n 'class=' origin/main -- tests/unit/test_regime_counters.py` → `451: ["S1: candidate class=reject skipped contract count=3 source=fixture"]`.
- Class at disposition time: `search-procedure` (the search's input is review-title text), also `unlanded-mechanism-stated-as-present` (the slug output is T718 item 3, added by the orchestrator at 16:00Z, after the a04 dispatch). The a03 acceptance record already states "`search-procedure` on the T703 lineage: 4 (a fourth row after the first S1 cycle) → … another S1 cycle, the third on the artifact → plan 007 S7 (plan 010)". This is the next row after that cycle: S7 again, the fourth stop on T703 (plans 008 wording, 009, 010, 012).
- S6 search, pasted (16:08Z):

```text
$ /usr/bin/grep -rl 'classes:.*search-procedure' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-16.md
.orchestration/learning/mistakes/M-20261012-20.md
.orchestration/learning/mistakes/M-20261012-15.md
.orchestration/learning/mistakes/M-20261012-21.md
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search search-procedure
No matches.
```

  Matching corrections: C-17, C-18, C-22, C-23 (all `pending`; C-23's mechanism is T718's `three-repeat.sh`, and T718 is ordered `after: [dotfiles-T128-playbook-rules-a04]`). None of them covers a rule sentence whose two trigger paths disagree on the class format; recorded as M-20261012-23 / C-25 (16:12Z).
- Replay of the proposed checker C10 (C-25) on the a04 task file: `FAIL C10 rule sentence names scripts/regime-counters.sh beside the literal [a-z0-9-], which neither the script nor tests/unit/test_regime_counters.py carries on origin/main`. C9 had skipped the sentence because it contains "Once plan 007 T718 lands" for another script.
- The worker's head is otherwise complete: docs module 47 OK, 20 of 20 mutants fail, the four a03 threads `fixed:beee078a`, size within caps (its report).

## Root cause

Rule text ahead of its mechanism, the pattern plan 007's dependency rationale and C-21 name: T718 (the scripts that items 1 and 3 cite) is ordered after T703, so every a0N head describes behaviour the tree does not have, and each review finds the next place where prose and tree disagree. Four heads, four findings on items 1 and 3 (4247933574 a01, 4248319926 a02, 4249303433 a03, 4250028600 a04). The landing-condition form (plan 010 D) covered `three-repeat.sh` but not the counter line's output, and no check compared the sentence's claim with the script's test.

## Options (today's medians: seat redesign 4 min, boundary 2 min, worker round 30 to 45 min, code round 45 to 60, CI 8.5, Bot 4.7 to 14, integration 25)

| | Option | Rounds | Wall to T703 merged | Risk |
|---|---|---|---|---|
| **B** | **Mechanism first: re-scope T718 to the scripts items 1 and 3 name (`regime-counters.sh` slug line and its test, `three-repeat.sh`, `bus-read.sh`, `dispatch.sh`); the other seven scripts move to a follow-up `orchestrator-tools-a02`. T718 goes to `claude-standard-dot-a003` now on a fresh branch (PR #328's branch stays in its worktree). a04's text is unchanged: its "Once plan 007 T718 lands" clauses become true, the counter prints the ledger slug, and 4250028600 is `fixed:<T718 squash sha>` after `gh pr update-branch 328`.** | T718: 1 review pair + 1 code round; a04: 0 | about 1 h 40 to 2 h 05 for T718, then 35 to 40 min for PR #328 (update-branch, Bot, sweep, audit, gate, merge): about 2 h 15 to 2 h 45 | T718's own Bot findings (code with tests, a different class); PR #329 (T702) waits behind T703 for the 4248232955 order, so T702 merges after about 2 h 45 even if its head is ready earlier |
| C | Amendment 1 of a04: drop the counter path from the sentence ("When a finding class reaches three on one artifact (the record's ledger), …"); the counters' S1 line stays an INV-6 detector for the orchestrator, not a rule trigger | 1 worker round | 60 to 85 min | the second amendment or revise resets a04 (INV-6); items 1 and 3 still describe T718's scripts under landing conditions, the pattern that produced four findings in four heads |
| A | Amendment 1 of a04: add a landing clause for the counter path ("until T718 prints the ledger slug, an S1 candidate line is read against the ledger and the ledger's slug is searched") | 1 worker round | 60 to 85 min | as C, plus one more unlanded-mechanism sentence for the Bot to test |
| D | Accept 2276a365 with 4250028600 `not-applicable` | 0 | 40 min | not available: the finding is substantive and no refutation exists (bot-ci-findings rule) |

**Recommendation: B.** It is plan 007's own order (mechanism before rule text), the only option that removes the class instead of patching its next instance, and T718 is work the plan needs anyway. **Without B: C** (one amendment, the smallest text, no new mechanism claim).

## Steps after the decision (filled when it arrives)

- B: R1 re-scope `dotfiles-T128-orchestrator-tools-a01` (items, allowed_files, threat rows; C1 to C10), draft `-a02` for the remainder; R2 task-file review pair (seat + Codex headless, same hash); R3 boundary PR (this plan, M-23, C-25, T718 files); R4 dispatch T718 to a003 on branch `tools/orchestrator-scripts`; R5 T718 integration; R6 `gh pr update-branch 328`, Bot, sweep with 4250028600 `fixed:<T718 squash>`, audit, acceptance record, gate, merge; R7 T702 integration.
- C or A: R1 amendment 1 text, hashed, confirmed by the review seat; R2 dispatch to a003; R3 integration as planned. A further finding on items 1 or 3 is INV-6's count: reset to a05 and S7.
