# Plan 015: T718 first slice (a03, PR #336) after its second S1 cycle: the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Nothing below is executed until the operator chooses. Every figure is pasted command output of 2026-10-13 (UTC).
>
> **Drift check (06:1xZ)**: `origin/main` `0a071318` (boundary PR #343; the fixtures PR #340 merged before it as `00943c6a`); PR #336 head `e16c5219` (the orchestrator's update-branch of the accepted `ba4d4762`), CI 12 of 12 (chain log), Bot review on it at 06:07:30Z with three new P2 threads; PR #328 (T703) and #329 (T702) held, both waiting for this merge.

## Status

- **Execution**: DECIDED 2026-10-13 06:1xZ: option B (operator, AskUserQuestion). R1 done: a02 item 4 (dispatch.sh's three fixes, the line's grammar table with its table-driven test, the closed binary list) pair-confirmed at `3817bb70…` after seat rounds 9 to 11 and Codex rounds 13 to 17 (06:25Z); R2 boundary (9) running, then `finish-336.sh`: the twenty #336 dispositions, the audit of e16c5219, gate, merge; R3 `integrate-328.sh <squash>` then `integrate-329.sh <T703 squash>`.
- **Priority**: P1 (T703 and T702 integrate after this merge; a02's dispatch follows it)
- **Planned at**: main `0a071318`, 2026-10-13 06:1xZ

## Situation

- a03's accepted head `ba4d4762` carried 17 Codex threads (16 fixed, 1 owned by a02); the ledger assigned `record-association` to three of them (4254399807, 4254771296, 4254844587), the artifact's first S1 cycle (searches pasted 05:5xZ; M-20261012-32 / C-31 recorded: an input-grammar table for every parsed input).
- The update-branch head `e16c5219` drew three more P2 threads on `dispatch.sh`'s record path: 4255272793 ("Bash tokenization accepts exactly one non-empty task ID, but `line.split(" ")` does not find it … the record identity check is therefore skipped"), 4255272797 ("both append subprocesses can read the same pre-update JSON … whichever replacement runs last silently discards the other dispatch evidence"), 4255272803 ("when the team already has at least 100,000 messages … line 182 then reports that no row was added"). Class `record-association` at 6: the second S1 cycle → S7.
- INV-6 counters for a03 (from its RESULTs): `amendments=1 revises=1`; a code fix is the second revise, INV-6's reset to a successor written by the review seat.
- The workers: a003 holds at ba4d4762 (accepted 05:36:59Z); a002 holds at 21badcd7 (accepted 05:39Z); the review seat is free. Chains for #328 and #329 are staged and wait on this merge.

## Root cause

`dispatch.sh` became a bus-protocol validator plus a record writer (209 lines) specified by behaviours, not by an input grammar; each Bot round enumerates another cell of the missing table (tokenization, concurrency, a capped history). C-31 (06:00Z) names the fix for the next tasks; it has not yet shaped this one.

## Options (today's medians: seat redesign 4 min, review pair 5 min, boundary 3 min, worker round 20 to 45 min, CI 9, Bot 5 to 14; the critical path is this merge → T703 → T702)

| | Option | Rounds | Wall to #336 merged | Risk |
|---|---|---|---|---|
| **B** | **Merge the accepted head as it stands; the three threads are `not-applicable: owned by dotfiles-T128-orchestrator-tools-a02` as new items of the second slice (the recorder tokenizes like the validator, a per-record lock around the read-modify-write, a capped history refused before the send), each with its input-grammar row per C-31; a02 dispatches right after this merge.** | 0 now; a02's round later | about 15 min (sweep, audit, gate, merge) | main carries three known P2 edges of an orchestrator-only tool (tabs in a line, concurrent dispatches, a 100,000-row history) for the one or two hours until a02 lands; the Bot reviews the fixes there |
| A | INV-6 reset to a04 by the review seat: a03 plus the three fixes as items with the grammar table; same worker, same PR; then CI, a Bot round, sweep, audit, gate | 1 reset, 1 worker round | about 1 h 15 (4 + 5 + 3 + 25 + 9 + 10 + 15) plus the Bot's next round on dispatch.sh | the pattern of this PR: 20 threads on one script, one to three per round; another round likely |
| C | Reset to a04 that drops the record writing from `dispatch.sh` (the path of 7 of the 20 threads) and leaves it to a02 | 1 reset, 1 worker round | about 1 h | the a04 rule's `dispatch:` key stays unfulfilled until a02; the T703 text already names the landing condition, so no text change there |

**Recommendation: B.** The three edges are real but small for a tool only the orchestrator runs, the fixes belong with the grammar table C-31 prescribes, a02 is the next dispatch anyway, and every other open task waits on this merge. **Without B: A.**

## Steps after the decision (filled when it arrives)

- B: R1 a02 gains three items and the grammar rows (re-confirmed by the pair on the new hash; its dispatch follows this merge and a boundary); R2 dispositions in the #336 sweep (`not-applicable: owned by …a02 item N; evidence=git show origin/main:…`), audit of `e16c5219`, gate, merge; R3 `integrate-328.sh <squash>`, then `integrate-329.sh <T703 squash>`.
- A or C: R1 redesign brief to the seat; R2 Codex half; R3 reset record; R4 boundary; R5 a04 line to a003; R6 its RESULT and the chain.
