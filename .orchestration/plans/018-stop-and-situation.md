# Plan 018: operator stop (2026-10-13 10:36Z): the situation, where the time went, the decision material

> Written 10:46Z on the operator's order ("stop all work; not a log: the situation, organised, and the material for a human to judge"). Every figure is pasted command output of 2026-10-13 unless marked.

## Stopped state (10:46Z)

- Stopped: the landing chain of plan 017 (killed 10:42Z). Before the kill it had merged boundary (11) as PR #347 (`a1d33849`, 10:39:43Z; records only) and sent the a04 amendment TASK (bus 935, 10:40:19Z, unread). Counter-orders sent: PING 936 (a02: stop, commit or stash, no push) and ACCEPTANCE `status=hold` 937 for the amendment TASK. Worker a003's PONG is pending. Worker a002 holds at #329 `21badcd7`. The review seat is idle. No PR is between an update-branch and a merge; no boundary marker is set.
- Main: `a1d33849`. Open PRs of the regime: #328 (T703, head 7771082f), #329 (T702, head 21badcd7). Merged today: #336 (T718 first slice, a03c1daa, 09:56Z), #340 (T702 fixtures, 00943c6a), eleven boundary PRs.

## Phases, tasks, work, verification, completion (plan 007)

| Phase / task | Work | Verification condition | Verified so far | Completion condition | State |
|---|---|---|---|---|---|
| 0 · T700 records and rules | M-1..8, C-1..11, the working rules | records on main; index two-way links | done 2026-10-12 | on main | done |
| 1 · T701 design amendment (B0) | regime-v3 design v20 → v24 | one review pair accepts | round 22 (v20) and 28 (v24) accepted by seat + Codex | receipt on main | done |
| 1 · T702 gate evidence (`gate-evidence-a01 → a04`, PR #329) | `require-crit-review.py` reads the acceptance record's JSON block (identity triple), ledger coverage, fixtures | CI 13/13; task-level audit `correct`; gate; pair-confirmed task text; INV-2 caps | fixtures half merged (#340, 00943c6a: three audits, one revise); main half accepted at 21badcd7 (CI green, Bot 8 rounds / 20 threads dispositioned at acceptance) | merged with `--match-head-commit` after update-branch, Bot, local review, audit, gate | open, held since 05:39Z |
| 1 · T703 playbook rules (`playbook-rules-a01 → a04`, PR #328) | SKILL/AGENTS rule sentences (dispatch evidence, amendment rule, three-repeat, row unit, invariant check, gate command) + token tests | same as above; `kind: docs` | a04 accepted at 2276a365 (CI green) and held for T718 (plan 012 B); update-branch head 7771082f drew P1+2×P2 (Bot) + 1 P2 (local); amendment 1 + owner task pair-confirmed and on main (a1d33849); amendment TASK sent then held | merged after the amendment round (one revise at most), residual P2 owned by `playbook-rules-followup-a01` | open; held by the stop |
| 5 · T718 orchestrator tools, first slice (`orchestrator-tools-a01 → a04`, PR #336) | dispatch.sh, three-repeat.sh, bus-read.sh, the counters' slug line, tests | CI 13/13; audit; gate; pair text; INV-2; INV-6 | merged 09:56:27Z as a03c1daa (one revise round; 30 threads dispositioned and resolved; audit `incorrect` with three P2 dispositioned; local review on each head; mutants 21/21) | merged | done |
| 5 · T718 second slice (`orchestrator-tools-a02`) | nine scripts + items 3, 4, 6 | same | dispatched 09:58Z; split into PR-A (now) and PR-B (after #329) at the worker's question | two PRs merged | held by the stop |
| 2 · T704..T708 detectors permanent | checkers promoted, V1 validator, successor generator, CompactionDB kinds, A7 | — | not started (plan order: after Phase 1) | — | not started |
| 3 · T709..T711 operator decisions | merge queue, permissions `ask` rules, Stop gate anchors | — | T710 patch with the operator | — | waiting |
| 4 · T712, T713 design items | step 15/7 state tables; Bot premise | — | not started | — | not started |
| 5 · T714..T717 make update findings | Homebrew token, AWS CLI, update-bootstrap, Codex profiles | approvals; T717 operator patch | T715/T717 approved; T714/T716 pending; T717+T710 patch with the operator | — | waiting |

Verification content per merged PR (T718 first slice as the example): worker tests (16 + 26 OK), mutants (21/21), CI 13 checks, Codex Bot threads (30) each `fixed:<sha>` or `not-applicable` with evidence, the C-32 local review per head, the task-level audit from main, the gate (`make require-crit-review` with four evidence files), the squash merge bound to the audited head.

## Where the time went (figures)

| Multiplier | Figure (pasted) | Effect |
|---|---|---|
| Codex Bot rounds, one per head including update-branch heads of unchanged code | #336: 13 rounds / 30 threads; #328: 7 / 16; #329: 8 / 20 | each round adds 1–4 findings; two update-branch rounds on #336 and one on #328 added findings on unchanged code; the local review reproduced 0 of 23 Bot threads (a sampler, not an oracle) |
| INV-6 resets to successors | 28 task files across the three lineages (a01 → a04 each, plus redesign and review tasks) | each reset: brief, seat round(s), Codex round(s), reset record, boundary, re-dispatch (30–60 min) |
| Task-text pair reviews | a02: 12 seat + 19 Codex rounds; a04 (tools) redesign: 5 + 5; design review: 25 rounds | the task text (100–150 lines, 20–25 threat rows, grammar tables) became the main reviewed artifact; one finding per round |
| Boundary commits (strict up-to-date ruleset) | 11 today; each forces update-branch + 9 min CI + a Bot round on every open PR | plans 015, 016, 017 are three stops caused by this loop |
| Orchestrator tooling built while in use | 105 scratchpad scripts; 56 Codex headless runs today; bugs M-26 (×6), M-35 | the regime's mechanisms (T718, T704) did not exist when the regime started enforcing them |
| Records | 36 M / 34 C; plans 008–017 | each M/C pair 10–15 min; six S7 asks (one waited 9 h) |
| Bus | today: 48 TASK, 46 RESULT, 35 ACCEPTANCE, 20 PONG, 7 PING | per merged PR: ~40 lines |
| Merge mechanics learned late | thread resolution required by the ruleset; the sweep re-run after replies; the gate's dispositions grammar | one hour on #336 after the audit |
| Wall per merged change | PR #336: created 01:55Z, merged 09:56Z (8 h) for 6 code/test files; #328 and #329 open since 2026-10-12 12:xxZ | ≈ 100× the authoring time |

Root cause in one sentence: every change passes through an unbounded number of adversarial sampling rounds (the Bot per head, the pair per text revision, the audit per head), each finding breeds a record, an amendment or a successor, the tooling that should make this cheap is itself under construction, and the orchestrator answered each loop with more process (plans 012 to 017) instead of less.

## Material for the operator's decision

| | Option | What stops / starts | Cost to close Phase 1 (T702, T703 merged) | Risk |
|---|---|---|---|---|
| **B** | **Cut the multipliers, finish Phase 1 with the owner-first structure already on main.** (1) P2 findings of the Bot or the local review on an accepted PR's later heads are recorded and owned (followup tasks: `playbook-rules-followup-a01` exists; one for #329 to add), never a fix round; only P0/P1 get the one round (#328's P1 is in the amendment already confirmed); (2) no boundary until Phase 1 closes (records batched); (3) task-text reviews: seat and Codex in parallel, two rounds total, the rest becomes follow-up items; (4) **operator levers**: set the ruleset's strict up-to-date off and the Codex Bot to on-request for the rest of Phase 1 (the two largest multipliers), restore both at Phase 2; (5) no new M/C for process slips until the retrospective. | #328 ≈ 1.5 h (amendment round, Bot, audit, merge), #329 ≈ 1 h, a02 PR-A ≈ 1 h → Phase 1 in ≈ 3.5 h | residual P2 accumulate in the follow-up tasks (bounded, listed); the levers weaken two guards for the duration |
| A | Continue as designed (G″ on #328, then #329, then a02) with every multiplier in place | ≈ 4–6 h at today's rates | more stops of the plan 015/016/017 kind; INV-6's P1-heads threshold on #328 is at 1 of 2 |
| C | Stop here; retrospective before anything else: write Phase 1's cost table and redesign the regime's cost model (the local review as the single pre-merge review, the Bot advisory, one text round, resets only on P0/P1, one boundary per day), resume tomorrow | 0 today; Phase 1 closes after the redesign | #328 and #329 stay open another day; a02 PR-A idle |
| D | Hand the two PRs to the operator: a human look, then merge #328 and #329 as they stand; a02 continues solo under the lighter rules of B | ≈ 30 min of the operator's time | the regime's evidence chain for these two PRs stays as it is (audits of earlier heads) |

Recommendation: **B now, then C's retrospective as Phase 1's closing item before Phase 2.** Without B: C.

Operator-only items in B: the ruleset's `strict_required_status_checks_policy` (GitHub settings) and the Codex Bot's automatic review setting; both are app or repository settings outside the seats. Everything else in B is the orchestrator's.

## Staged completion (operator's correction 10:50Z: "everything at once is why it never finishes; aim for staged completion")

Rules for every stage: one PR at a time, nothing else dispatched until it is merged; a P2 on a later head of an accepted PR is recorded and owned, never a round (only a P0/P1 gets the one round); no task-text review (the texts are confirmed); one boundary at the end of each stage, none inside it; the local review once per head; the stage is done only when the thing is merged and exercised once on main.

| Stage | Deliverable (one PR) | Done when (verifiable) | Leaves out | Time |
|---|---|---|---|---|
| 1 | PR #328, T703 rules text with amendment 1 (four sentences + token tests; the worker's one round) | merged; `grep -c "20 minutes" home/dot_agents/skills/agmsg-orchestration/SKILL.md` on main ≥ 1; the token tests green in CI on main | residual P2 of its last head → `playbook-rules-followup-a01` (on main) | ≈ 1.5 h |
| 2 | a02 PR-A (seven scripts + items 3, 4, 6; the worker is mid-way, branch `tools/orchestrator-scripts-2`) | merged under the current gate; `scripts/orchestrator/boundary.sh --help` runs from main | PR-B's two gate-coupled scripts | ≈ 1.5 h |
| 3 | PR #329, T702 gate evidence (the gate reads the acceptance record's JSON block) | merged; `make require-crit-review` on main exercised once on a fixture record | residual P2 → a follow-up task written at stage start (same pattern as stage 1) | ≈ 1 h |
| 4 | a02 PR-B (acceptance-front-matter.py + orch-gate.sh + tests; on the new gate) | merged; one real acceptance record written by the script and read by the gate | — | ≈ 1.5 h |
| 5 | Phase 1 retrospective + the regime's cost rules (plan 019): one mechanism per stage from here on, Bot advisory on later heads, one text round, resets only on P0/P1, one boundary per stage | plan accepted by the operator | Phase 2 starts only after it | ≈ 1 h of writing |

Each stage ends in something merged and in use; the operator may stop after any stage. Optional operator levers that shorten every stage (not required): the ruleset's strict up-to-date flag off and the Codex Bot on-request during stages 1 to 4 (no re-review of unchanged code after each boundary).
