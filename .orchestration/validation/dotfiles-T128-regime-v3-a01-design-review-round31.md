---
reviewed_at: 2026-10-15T08:09:48Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@bb0dc151f8ed95e0c10c1cae97d730cef014474b6be3a6221d0df06fd98a6fdd
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@0fb788767ce66014b036e95f76d0f9ed66306cd3e601935c9ef89cd76054f48d
round: 31
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round30.md
previous_design: 94d246c1690d1c08fd93fb4b3404e6be76d2dacc2b35ac2ce4a89a9087dcd401 (v26 as reviewed in round 30); main's copy fa2c5157 (v24, at 907522c2)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 31 (v27: the threshold number back, the det-check trigger on gate-written entries, the advisory badge; the third and last pair)

Delta judged against main's copy at fa2c5157 (v24, main 907522c2) and against v26. A line diff against v26 shows three changes: INV-4's sentence, INV-6's sentence, the v27 history paragraph; the map is v26's. PyYAML, run by this seat on v24 and v27: of the hashed keys only `invariants` (INV-4, INV-6) and `implementing_tasks` (the three entries) differ; `threat_model`, `trust_anchors`, `premises`, `supersedes`, `reset_of` and `design_review` are equal to main's. `design-keydiff.py` (origin/main's copy, in a scratch repository whose HEAD holds v24): `invariants ['INV-4', 'INV-6']`, `implementing_tasks ['dotfiles-T128-counters-review-kind-a01', 'dotfiles-T128-gate-evidence-followup-a01', 'dotfiles-T128-gate-reset-trigger-a01']`, the orchestrator's paste. Plan 007's S6 cites v27 and names the badge; S7 is the v26 sentence and cites v26, which is accurate. Plan 022's T14 reads as the raw-counts-plus-rows model; T16 names `acceptance-front-matter.py`, `require-crit-review.py`, the two test modules and the gate fixtures, with the `gate_refusals` writer and the row checks.

## What round 30 asked, and v27

- This seat's clause (no threshold number): answered. INV-6 reads "two: the second revise, the second amendment, the second question; a P0 or P1 on two heads; scripts/regime-counters.sh's constant"; INV-4 reads "a count that reaches two (the second amendment or the second question)"; the counters' `threshold=2` has its design anchor again and a change of it is a hashed design change (INV-7).
- The Codex half's three: the det-check trigger now rests on `gate_refusals` entries `{check, head, at}` the gate appends itself, two of them naming one check on two heads (a correction of the record alone never moves the head, so the #361 chain's two refusals on one head are trigger none, which is right); the p0p1 trigger is bound to the Bot and audit sources and the gate refuses a row whose id is in neither; an advisory row needs a P2 or P3 badge besides the prefix, so a mislabelled P0 or P1 stays in the S6 class count. Each has a named writer and reader in T14 or T16, except the point below.

## INV-6 (rejected, one clause: where the gate's entries live)

The sentence says the det-check trigger "holds only when the record's gate_refusals entries, appended by scripts/require-crit-review.py itself on every refusal ({check, head, at}, never written by the orchestrator), name the same check on two heads", and the gate "refuses a det-check row with fewer than two matching gate_refusals entries". Against the scripts on origin/main and T16 as plan 022 states it, no entry can ever persist:

- `scripts/orchestrator/orch-gate.sh` sets the record as the relative path `.orchestration/acceptance/<task>.md` (line 50), copies every evidence file, the record among them, into the review worktree at the gated head (77 to 80), enters that worktree and runs the gate with `ACCEPTANCE_EVIDENCE` as that relative path under `env -i` (84 to 89), so the gate reads and could write only the copy; the EXIT trap then runs `git clean -fdq -- .orchestration` in the review worktree (63 to 64), and the next run refuses a review worktree that is not clean (62). An entry the gate appends is deleted before the run ends; two entries never meet; every det-check row is refused as "fewer than two", so the trigger the sentence defines is dead, and the orchestrator cannot even record a true one.
- T16's files are `acceptance-front-matter.py`, `require-crit-review.py`, `tests/unit/test_orchestrator_tools.py`, `tests/unit/test_require_crit_review.py` and the gate fixtures; `orch-gate.sh` is in neither T16 nor T14, so neither mapped task can carry the entries across runs.
- The record block's allowlist (`require-crit-review.py:785`, `RECORD_KEYS`) refuses an unknown key today, so both new keys enter it in T16, the same file as the row writer and the entry writer; that ordering is consistent, and `acceptance-front-matter.py`'s `{**record}` rewrite keeps keys it does not own.

Ask, one clause and one plan line: INV-6 says where the entries live and how they get there, one of (a) the wrapper passes the main checkout's record to the gate by its absolute path, so the gate appends to the record itself; or (b) the wrapper merges the gate's `gate_refusals` entries from the copy into the main checkout's record before its trap runs; and T16's files gain `scripts/orchestrator/orch-gate.sh` (its tests are already in T16's module). Nothing else in INV-6 is rejected; INV-4 is accepted.

Smaller, worker input on accept: the Bot's badge is the image form `![P2 Badge](…)` (the sweep bodies; `fill_sweep.py:32`'s regex), not a literal `[P2]`, so T14's recogniser must use that form or every Bot advisory row stays in the class count; a `none` row's `evidence=` has no stated content since v26's "names the command whose pasted output shows it" went, so the gate should at least require it non-empty, as it does for a not-applicable disposition; "two heads" as the proxy for "failed again after its one correction" counts two refusals of one check that straddle a `gh pr update-branch` with no correction between them, a design choice to state or accept; the gate does not run the task-consistency check, so `<check>` can only name a gate check, consistent with v27 dropping that mention; the map entries are v26's (the two files unwritten, the gate-evidence-followup amendment pending), as noted in round 30.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: rejected (the gate_refusals clause above). INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: revise
