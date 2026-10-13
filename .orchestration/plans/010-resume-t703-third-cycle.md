# Plan 010: T703 (PR #328) after its third S1 cycle: the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Nothing below is executed until the operator chooses. Every figure is pasted command output of 2026-10-12.
>
> **Drift check (at planning time, 14:54Z)**: `origin/main` `e0e2fe62`; PR #328 `OPEN`, head `e12872cd` (the orchestrator's `update-branch` over the worker's `fe34f7db`), CI running; Bot review 5492353166 on `fe34f7db`: 4249303413 P1, 4249303433 P1, 4249303398 P2, 4249303426 P2 open; worker `claude-standard-dot-a003` holds (ACCEPTANCE `under_review`); T702 (PR #329, head `4e2266aa` after `update-branch`) continues.

## Status

- **Execution**: DECIDED 15:19Z: option D (operator, AskUserQuestion); T718 approved as the owner of three-repeat.sh, dispatch.sh and bus-read.sh (default with D). Steps: R1 a03 withdrawn (INV-6 pre-empted), R2 redesign task to the review seat (a04), R3 reset record, R4 boundary PR, R5 a04 dispatched on PR #328, R6 update-branch, CI, sweep, audit, gate.
- **Priority**: P1
- **Planned at**: main `e0e2fe62`, 2026-10-12 14:54Z

## Situation

- Four Bot rounds on PR #328 (`9b2c02a1`, `375bae0f`, `c4e0bb72`, `fe34f7db`), each on items 1 or 3 of the task (the dispatch-evidence sentences and the three-repeat procedure); the other items (2, 4, 5, 6, 7) drew no finding after the first round. Counters for a03 at 14:54Z: `task=dotfiles-T128-playbook-rules-a03 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=fe34f7db0311fd5503104abe1a4b8ddec509c54`.
- S1 cycles on the artifact: `search-procedure` (13:24Z), `unlanded-mechanism-stated-as-present` (14:01Z, S7 → plan 009 A), and now a fourth `search-procedure` row (4249303433) with three sibling findings on the same two items (M-20261012-21). Third cycle: S7 again.

## Problems and open issues

1. 4249303433 (P1): the class slug comes from `regime-counters.sh:146-147` as an unfiltered review-title substring and the procedure substitutes it into a quoted grep and an unquoted memory search: review text reaches the orchestrator's shell. Real, and a security finding.
2. 4249303413 (P1): "the bus line `history.sh <team>` prints" is a default-limited read (LIMIT 20, `history.sh:9`); the sentence needs a complete read.
3. 4249303426 (P2): "no bus event from its seat since" never resets after one early PONG; the clock must count from the latest bus event for that task.
4. 4249303398 (P2): a correction can be landed for one mechanism and pending for another (C-2); "landed/pending" is per mechanism.
5. Any fix is task text → amendment 1 of a03 (budget exists: amendments 0, revises 0) or a reset; but the pattern says the next round finds the next operational gap in the same prose.

## Root cause

Operational procedure in rule prose (M-20261012-21, C-23). The operator's first direction was mechanical rules; items 1 and 3 state commands, limits and grammars in SKILL sentences the Bot reviews as text, and each round found the next one. Items 2, 4, 5, 6, 7 are obligations and have been stable since the first round.

## Options (today's medians: seat redesign 4 min, boundary 2 min, worker round 30 min, CI 8.5, Bot 4.7, integration 25)

| | Option | Rounds | Wall to a mergeable head | Risk |
|---|---|---|---|---|
| **D** | **Reset to a04 that keeps items 2, 4, 5, 6, 7 and reduces items 1 and 3 to the obligation plus the script that performs it with its landing condition** ("…recorded under a `dispatch:` key as the bus line `dispatch.sh` reads once T718 lands; until then a complete `history.sh --limit 1000` read"; "…the next acceptance action is the records search `three-repeat.sh <class>` once T718 lands; until then the orchestrator runs the two commands with a slug validated against `[a-z0-9-]` and pastes the template line"); T718's scope gains `three-repeat.sh` and the counters' slug output (recommended) | 1 reset, 1 worker round | about 50 min, then 25 min integration | low: the four findings become script requirements with tests; the Bot reviews code next |
| A | Amendment 1 of a03 with the four fixes written into the prose | 1 worker round | about 35 min, then 25 min | a fifth round on the same prose is the pattern; one more finding of the class is a fourth cycle |
| C | Reset to a04 without items 1 and 3 (ship 2, 4, 5, 6, 7 now; items 1 and 3 land as T718's scripts and their one-sentence SKILL pointers) | 1 reset, 1 worker round | about 45 min, then 25 min | the plan holds the two rules until T718 (it already binds the orchestrator); smallest SKILL diff |
| E | Hold T703 until T718 lands and restate items 1 and 3 then | 0 now | T718 is pending approval and hours of work | the open PR idles with four threads; items 2, 4, 5, 6, 7 wait for no reason |

**Recommendation:** D. It ships what is stable, keeps the two rules visible with their mechanism named, and moves every operational detail where a reviewer can test it. **The options without the recommendation:** D reset to a04 with obligation-plus-script sentences; A amend the prose; C reset to a04 without items 1 and 3; E hold until T718.

## Decision for the operator

- **Question:** which option; and does T718 (the orchestrator tools, pending approval) now become approved as the owner of these two scripts (default with D or C: yes)?
- **Default if no answer arrives:** none; S7 waits for the operator.
- **Answer:** D, 15:19Z.
