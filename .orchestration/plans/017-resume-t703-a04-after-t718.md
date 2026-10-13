# Plan 017: T703 a04 (PR #328) after T718's first slice landed: the Bot's round on the update-branch head, the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Every figure is pasted command output of 2026-10-13 (UTC). Prepared before the ask (ask-blocks-hold-first): the amendment and the owner task are drafted, checked and under pair review; nothing is dispatched to the worker, no boundary runs, no disposition is sent until the operator chooses.
>
> **Drift check (10:21Z)**: `origin/main` `a03c1daa` (T718 first slice merged 09:56:27Z); PR #328 head `7771082f` (the orchestrator's update-branch of the accepted `2276a365`, 09:58:25Z), CI 13 green, Bot review 5501887212 (10:03:30Z) with three new threads, the C-32 local review with one; PR #329 (T702, `21badcd7`) waits; a02 (T718 second slice) is with a003 as PR-A (its two gate-coupled scripts wait for #329); the review seat holds the pair review of the drafts; the bus is quiet otherwise.

## Status

- **Execution**: DECIDED 2026-10-13 10:30Z: option G″ (operator, AskUserQuestion). R1 done 10:35Z: the pair confirms a04 amendment 1 at c5dbc2c3… and the owner task at cb32794d… (seat rounds 1 revise, 2 confirm, bus 933; Codex rounds 1 revise, 2 confirm) → R2 boundary (11) running (land-t703-amend.sh) → R3 the amendment line to a003 → R4 the round, the local review, one revise at most, dispositions, resolution, sweep, audit, gate, merge → `integrate-329.sh`.
- **Priority**: P1 (T703 and T702 close plan 007 Phase 1; a02 PR-B waits on #329)
- **Planned at**: main `a03c1daa`, 2026-10-13 10:21Z

## Situation

- The accepted a04 head `2276a365` (2026-10-12 16:04Z) was held for T718 (plan 012 B). After T718 landed, the update-branch head `7771082f` drew: 4257278283 (P1, SKILL.md:69: the task-file review's invariant check compares ids only; the design, INV-2 line 56, requires "byte-for-byte as sentences"), 4257278271 (P2, SKILL.md:164: "thirty minutes" where INV-10 line 64 says "not idle for 20 minutes"; 30 is the first-push deadline), 4257278276 (P2, SKILL.md:71: one wildcard row can cover several trust-boundary scripts), and the local review's 7771082:1 (P2, SKILL.md:164: `--limit 1000` is not a complete read; the merged script refuses a read at its limit). All four sentences are dictated by the a04 task text (items 1, 4, 5), so a fix is an amendment plus a revise round.
- INV-6 for a04: `tasks=1 amendments=0 questions=0 results=1 revises=0` (pasted in the record): one amendment and one revise are available before a reset. With GitHub (10:33Z): `bot_p1_heads_after_result=1` (7771082f; the first RESULT head 2276a365 is excluded by INV-6's "after the first RESULT"): a P1 on one more head of this PR reaches INV-6's threshold of two and the gate refuses the merge until a reset record exists. G″'s amendment head is that one head; the round answers the P1 at its root (the design's words) so the Bot's next round has no P1 to raise.
- The lineage ledger (a01 → a04 on PR #328, 17 rows): `search-procedure` 6, `design-mismatch` 3 (4247933561 and the two new threads), `wall-clock` 2, `unlanded-mechanism-stated-as-present` 2, `threat-row-unit` 2, `default-limited-read` 2. A second class at three on the artifact: S7 by plan 007's letter, after plans 009, 010 and 012 on the same lineage. S6 searches pasted in the record: `design-mismatch` has no record; `threat-row-unit` → M-20261012-14 (and -29 in prose); `default-limited-read` → M-20261012-33 (M-21 in prose).
- The same structure as plan 016 on PR #336: an accepted PR's update-branch head draws new findings; the owner of residual findings does not exist on main.

## Root cause

The a04 text was reviewed against the design's ids and map entry, not against its sentences (the Bot's P1 names the gap in the rule and the gap applies to how a04 itself was reviewed: "thirty minutes" and "complete read" went in against INV-10's and T718's words). The verification stage lacked the by-hand sentence comparison the amendment now requires; C-32's local review and the owner-first structure were not in place when a04 was accepted.

## Options (medians: pair review 5 to 15 min, boundary 3, worker round 20 to 45, CI 9, Bot 5 to 14, local review 2, audit + gate + merge 15)

| | Option | Rounds | Wall to #328 merged | Risk |
|---|---|---|---|---|
| **G″** | **The plan 016 G′ pattern on this PR.** Amendment 1 of a04 (the four sentences, against the design's words) and the owner task `dotfiles-T128-playbook-rules-followup-a01` (its one item = the residual rows of a04's final head) pair-confirmed; boundary (11) lands both (and today's records); the amendment line to a003 (it pauses a02 PR-A, does the round on `regime/playbook-rules`, returns); Bot round + local review on the new head; one revise at most; residual P2 owned by the follow-up task (on main); audit, gate, merge. | 1 amendment, 1 worker round, ≤ 1 revise | about 1 h 30 to 2 h | the follow-up task inherits a bounded residual; a02 PR-A pauses for the round |
| H | Merge `7771082f` now with the four findings owned by the follow-up task (no amendment, no round): dispositions `not-applicable: owned by …followup-a01` after boundary (11) lands the owner | 0 now; the follow-up's round later | about 40 min (boundary, update-branch, CI, Bot round, audit, gate, merge) | main carries a P1 gap in the review rule until the follow-up lands; the Bot's next round on the update-branch head can add findings again (the loop of plan 015 B) |
| R | INV-6 reset of a04 to a05 by the review seat with the four fixes as items | 1 reset, 1 worker round | about 2 h | a05 is the fifth file of the lineage; the same Bot behaviour on its head; the owner question remains |

**Recommendation: G″.** It is the pattern the operator chose for the sibling artifact three hours ago, INV-6 leaves exactly the amendment and the revise it needs, and the P1 gap is fixed on the same PR instead of landing on main. **Without G″: H.**

One assumption the operator may overrule: the follow-up task is the owner of the residual findings (a small docs task on the same files, after a04). The alternative is to leave residual rules findings to plan 007 Phase 2 (T704's checkers) without a file on main; the default is the file.

## Steps after the decision (filled when it arrives)

- G″: R1 the pair confirms both files (running); R2 boundary (11); R3 the amendment line to a003; R4 the worker's RESULT → local review → Bot → one revise if needed → dispositions (residual owned) → thread resolution → sweep → audit → gate → merge → `integrate-329.sh <T703 squash>`.
- H: R1 the owner task alone pair-confirmed; R2 boundary (11); R3 update-branch, CI, Bot, dispositions, audit, gate, merge.
- R: R1 redesign brief to the seat; R2 Codex half; R3 reset record; R4 boundary; R5 the a05 line.
