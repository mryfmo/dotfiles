# Plan 014: T702 (PR #329) amendment-1 head: the Bot's fourth binding finding; the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Nothing below is executed until the operator chooses. Every figure is pasted command output of 2026-10-13 (UTC).
>
> **Drift check (at planning time; the file was written 02:33Z by its mtime, times below from the bus)**: `origin/main` `ce0af5d0` (boundary PR #337); PR #329 head `82e86e50` (`mergeStateStatus=BEHIND`), CI `SUCCESS:12`; Bot review `5498081103` on it at 02:24:39Z with one new P1 (4254092805); worker RESULT (bus, 02:30:11Z): `ci=12-of-12-green … bot_rounds=2 fix_rounds=1(7581d590)+amendment-1(f5f980f9) open:4254092805 … module=86-tests-OK(71-on-main) mutations=19-of-19-caught`. PR #336 (T718 first slice, `claude-standard-dot-a003`) head `61290da8` with failing Unit test jobs; T703's integration, which T702's follows (plan 012 B), is at least 1 h 45 away.

## Status

- **Execution**: DECIDED 2026-10-13 02:3xZ (between the ask at 02:34Z and the withdrawal line at 02:37:48Z, bus 821): option A (operator, AskUserQuestion). R1 done: ACCEPTANCE withdrawn to a002 (bus 821, ack 822), redesign task `dotfiles-T128-gate-evidence-redesign-a03` to the review seat (bus 823, 02:38:32Z). Seat round 1 a04 `b062e46e…` (02:43:13Z, bus 824; accepted 826); Codex round 1 revise (one P2: two checker-range phrases outside the brief) → brief round 2 (items 7 bookkeeping allowed, 8 optional `dispatch` key with unknown-key refusal and a fixture, for T718's dispatch.sh) → seat round 2 a04 `13d2ca487a4e6e73b8c6d37cce050b61dea05e1985f635a21bb5e8ca15c13096` (02:51:30Z, bus 832; checker OK, sweep clean); Codex round 2 confirm (67 s, no findings): the pair agrees on `13d2ca48…`. R4 reset record written (`reset-a03.sh`, anchor bus 832). R3 design v23 round 26: seat accept on `9373f8e8…` (02:56:08Z), Codex revise (P1: a04's coverage omits badged Codex `review` bodies; the sweep data on this host has 1 such body in 242, PR #276) → brief round 3 (item 9: the four badge tokens on Codex `review` bodies join the swept ids; fixture) to the seat 02:57:33Z (bus 841) → a04 round 3 `1f8e7518fb6ef11c41d6ed64f80b931e9e29d1b727327db678941064db884d3e` (03:00:08Z, bus 842; checker OK, sweep clean, the four tokens present; accepted); Codex round 3 revise (P1: the review-body fixture proves only the positive case) → brief round 4 (item 10: an unbadged and a near-match review body excluded, exact swept-id set test) to the seat 03:02:18Z (bus 844) → a04 round 4 `03a5253d1bc78ad928b5b9bc66cbe9ffada6e6090f732acc76c05a532c40001f` (03:03:28Z, bus 845; checker OK, sweep clean; accepted); Codex round 4 confirm (61 s, no findings): the pair agrees on `03a5253d…` after four rounds (bookkeeping scope; the optional `dispatch` key; badged review bodies; their negative cases). Reset record re-anchored on bus 845; design v24: round 27 (seat accept, Codex revise: two history lines still named a04 hashes) → hash-free v24 `fa2c5157…`, round 28 both accept (03:08Z). R5 boundary PR #338 merged (`948d1f38`, squash commit 03:13:30Z; the chain saw it at 03:13:42Z). R6 done: a04 TASK line to a002 03:13:46Z (bus 853), amendment 1 of T718 a01 to a003 03:13:58Z (bus 854). Next: the workers' pushes, CI, Bot; T718 integration first, then PR #328, then PR #329.
- **Priority**: P1 (the gate's trust boundary; INV-6 counters for a03 at `amendments=1 questions=1`: a second amendment is the reset)
- **Planned at**: main `ce0af5d0`, 2026-10-13 02:33Z (file mtime)

## Situation

- Thread 4254092805 (Bot, `scripts/require-crit-review.py:872`): "The S6 check counts only rows supplied by the acceptance record and never verifies that the ledger includes every item from `PR_FEEDBACK_EVIDENCE` or every audit finding. An acceptance record with `ledger: []`, or one that omits enough occurrences of a repeated class to keep its count below three, therefore passes and bypasses the mandatory records-search check … compare ledger IDs against the swept feedback and audit findings before counting classes." The worker: real, and task text (the orchestrator's); its proposal: every Bot-badged sweep item id and every `audit:<sha7>:<n>` must be a ledger id.
- Class at disposition time: `acceptance-record-binding`, the fourth row on the T702 lineage (4248232964 task, 4249544762 head, 4250238714 pr, 4254092805 ledger ↔ swept items), the next row after the third S1 cycle (plan 013): S7 again.
- Counters 02:32:00Z: `task=dotfiles-T128-gate-evidence-a03 tasks=2 amendments=1 questions=1 results=1 withdrawn=0 revises=0 first_result_head=82e86e50… wall=2026-10-12T15:41:03Z..2026-10-13T02:30:11Z (10:49)`.
- S6 search, pasted (02:34Z):

```text
$ /usr/bin/grep -rl 'classes:.*acceptance-record-binding' .orchestration/learning/mistakes/
.orchestration/learning/mistakes/M-20261012-24.md
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search acceptance-record-binding
No matches.
```

  M-24's correction C-26 bound the identity triple and stopped there; it is amended today with the content rule (ledger ids ⊇ badged sweep item ids ∪ `audit:<sha7>:<n>`), and M-20261012-28 records this row.

## Root cause

"Binding" was read as *which record* (task, head, pr) and not also *what the record says*. The gate takes the ledger on trust, and the ledger is written by the same actor the gate is meant to check (INV-6's enforcement row exists for the orchestrator's own bookkeeping, M-15's class). The fix is one set difference the gate computes from the two inputs it already reads.

## Options (today's medians: seat redesign 4 min, design round pair 10 min, boundary 3 min, worker round 25 to 45 min, CI 8.5, Bot 5 to 14, integration 25; T702 merges after T703, at least 1 h 45 away)

| | Option | Rounds | Wall | Risk |
|---|---|---|---|---|
| **A** | **INV-6 reset to a04 by the review seat: a03's text plus one contract sentence ("the gate refuses a record whose `ledger` lacks any Bot-badged item id of `PR_FEEDBACK_EVIDENCE` or any `audit:<sha7>:<n>` of `AUDIT_EVIDENCE`: `S6: ledger lacks <ids>`"), one fixture that omits a row, one test; design v23 map entry (round 26 pair); reset record; boundary; the same worker on PR #329; 4254092805 `fixed:<a04 head>`.** | 1 reset, 1 worker round | about 1 h 15 to 1 h 30 to a Bot-reviewed head, inside the wait for T703: net wall cost about zero | the a04 head's own Bot round; after identity and coverage the gate trusts no record field (format fixed, searches recomputed, audit_findings per numbered finding) |
| E | Accept the a03 head; 4254092805 `not-applicable: owned by a follow-up gate task (ledger coverage) after T702 merges; evidence=<its task file on main>` (the 4248232955 precedent); the follow-up is one worker round on `require-crit-review.py` after #329 merges | 0 now, 1 later | T702 Bot-clean now; the coverage check about 1 h after T702 merges | the merged gate trusts the ledger until the follow-up lands (the window covers T718 a02's and the follow-up's own integrations); the Bot re-raises on the next #329 push and the disposition must hold |
| F | Put the coverage only into T718 a02's record writer (`acceptance-front-matter.py`) and leave the gate | 0 | 0 | the Bot's point stands: a hand-written record still passes; not a disposition |

**Recommendation: A.** The reset fits inside the wait for T703, so it costs no wall time, and it closes the class instead of scheduling it. **Without A: E.**

## Steps after the decision (filled when it arrives)

- A: R1 redesign task `dotfiles-T128-gate-evidence-redesign-a03` to the review seat (a04 = a03 + the coverage sentence, fixture and test; the orchestrator pastes the sentence); R2 Codex half on the same hash; R3 design v23 (map entry `gate-evidence-a04`, round 26 pair); R4 reset record `dotfiles-T128-gate-evidence-a03-design-reset.md`; R5 boundary; R6 dispatch a04 to a002 on PR #329 (`design_sha256`, hash from the file); R7 CI, Bot, then the held integration after T703.
- E: R1 follow-up task file and its review pair; R2 boundary; R3 ACCEPTANCE of the a03 RESULT with the disposition; R4 the held integration after T703; R5 the follow-up after #329 merges.
