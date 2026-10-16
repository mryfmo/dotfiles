---
reviewed_at: 2026-10-15T07:55:03Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@94d246c1690d1c08fd93fb4b3404e6be76d2dacc2b35ac2ce4a89a9087dcd401
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@4b43dffd1ab4f0fd31a7ccb828f5aa9a85e3aabacc19f177c697d0a48cc4f160
round: 30
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round29.md
previous_design: a6a19109c194b8e2c36c388f1f05fe55c09652c7c1dc11703eb334e9b78526cb (v25 as reviewed in round 29); main's copy fa2c5157 (v24, at 907522c2)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 30 (v26: INV-6's trigger qualified and recorded, INV-4 aligned, a third map entry, S7 one sentence)

Delta judged against main's copy at fa2c5157 (v24, main 907522c2) and against v25. A line diff against v25 shows four changes: one `implementing_tasks` insertion, INV-4's sentence, INV-6's sentence, the v26 history paragraph; nothing else. PyYAML, run by this seat on v24 and v26: of the hashed keys only `invariants` (INV-4, INV-6) and `implementing_tasks` (three entries) differ; `threat_model`, `trust_anchors`, `premises`, `supersedes`, `reset_of` and `design_review` are equal to main's. `design-keydiff.py` (origin/main's copy, in a scratch repository whose HEAD holds v24): `invariants ['INV-4', 'INV-6']`, `implementing_tasks ['dotfiles-T128-counters-review-kind-a01', 'dotfiles-T128-gate-evidence-followup-a01', 'dotfiles-T128-gate-reset-trigger-a01']`, the orchestrator's paste. Plan 007's S7 in the main checkout is one sentence again (the decisions panel, the default at the next boundary, blocking only for a P0); S6 keeps its advisory clause; plan 022 holds T16 (`acceptance-front-matter.py`, `require-crit-review.py`, the two test modules, the gate fixtures; the row writer and the gate's reading) and T14 aligned with v26 (the counters as today plus the review exclusion; the boundary check reads the rows).

## What round 29 asked, and v26

- Clause 1 (the circular, unqualified trigger): answered. The trigger is `det-check:<check>`, "a deterministic check that failed again on the final head after its one correction", the gate's refusal of the acceptance evidence or the task-consistency check's refusal of the task copy, and it exists only as a `threshold_dispositions` row; the gate refuses on a row whose trigger is not none, not on its own exit status. The #361 chain's two cured refusals are trigger none under this text.
- Clause 2 ("carries" without a source): answered. The row `{count, n, trigger, evidence}` in the record's block, written by `scripts/orchestrator/acceptance-front-matter.py` from the orchestrator's TSV, `evidence=` naming the command; the gate refuses a reached count with no row; the boundary check reports a reached count with no row and a trigger row with neither reset nor waiver. T16 maps the writer and the gate's reading; T14 maps the boundary check's reading. Every file the sentence names has a mapped task.
- Clause 3 (the advisory marker): answered. A row is advisory when the sweep disposition of its id or the record's `local-finding:` or `audit-finding:` line begins `not-applicable:advisory`; both are files the counters can read.
- INV-4's last clause now says amendments and questions are INV-6's counts, dispositioned in the same row, withdrawal only by a trigger row: consistent with INV-6.
- The map: `gate-evidence-followup-a01` stays mapped with its INV-6 sentence to be amended before dispatch (INV-2), as the round-29 P3 asked; `counters-review-kind-a01` and `gate-reset-trigger-a01` are plan 022's T14 and T16.

## INV-6 and INV-4 (rejected together, one clause)

The sentences no longer say what a count's threshold is. v24 said it three times ("threshold 2" for revises, amendments and questions) and INV-4 said "the second amendment or the second question"; v26's INV-6 reads "a count that reaches its threshold is dispositioned …", "the gate also refuses a merge whose record has a reached count with no row", and INV-4 reads "a reached count is dispositioned …", with no number anywhere in the hashed keys ("two heads" survives only for the Bot and audit sources). `scripts/regime-counters.sh` lines 59 to 60 carry `threshold=2` as "INV-6's constant for every count; changing it is a hashed design change (INV-7)": with the number gone from INV-6, the constant has no design anchor, the gate's "reached count" (T16) and the boundary check's (T14) are left to the implementer, and a later change of the number would no longer be a hashed design change. Ask, one clause in INV-6 where "reaches its threshold" first appears: "its threshold (two: the second revise, the second amendment, the second question; a P0 or P1 on two heads; `scripts/regime-counters.sh`'s constant)", and in INV-4 "a count that reaches two" or "a reached count (two)". Nothing else in either sentence is rejected.

Smaller, no verdict weight: INV-6's "(review-brief task ids excluded from every count)" repeats the clause before it; plan 007's S6 still cites "design v25" for the advisory exclusion, whose recognition rule is v26's (plan text, not a hashed key); the `counters-review-kind-a01` and `gate-reset-trigger-a01` files do not exist yet (plan 022 T14 and T16 name them), so INV-2's comparison binds them only once written; `gate-evidence-followup-a01`'s owned section in the a04 record is still absent on origin/main, so that task is a no-op until rows exist, which is not this round's question.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: rejected (the threshold number, with INV-6). INV-5: accepted. INV-6: rejected (the threshold number). INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: revise
