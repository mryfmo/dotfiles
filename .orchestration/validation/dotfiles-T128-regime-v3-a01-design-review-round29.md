---
reviewed_at: 2026-10-15T07:38:43Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@a6a19109c194b8e2c36c388f1f05fe55c09652c7c1dc11703eb334e9b78526cb
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
task_file: dotfiles-T128-design-review-a01@2059f40f6eb7d38594d51936f6bf324ac62c5ec8ff868dc63e3312ba97aaeadb
round: 29
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round28.md
previous_design: fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a (v24 as reviewed in round 28; main's copy at 907522c2)
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to main's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 29 (v25: INV-6 recalibrated per plan 020 step 8, two map entries, one history paragraph)

Delta judged against main's copy at fa2c5157 (v24, main 907522c2). A line diff shows three changes: two `implementing_tasks` insertions after the a04 entry, INV-6's sentence replaced, and the v25 history paragraph; nothing else. PyYAML, run by this seat on both copies: of the hashed keys only `invariants` (INV-6) and `implementing_tasks` differ; `threat_model`, `trust_anchors`, `premises`, `supersedes`, `reset_of` and `design_review` are equal to main's. `design-keydiff.py` (origin/main's copy, run in a scratch repository whose HEAD holds v24): `invariants ['INV-6']`, `implementing_tasks ['dotfiles-T128-counters-review-kind-a01', 'dotfiles-T128-gate-evidence-followup-a01']`, the orchestrator's paste. Plan 007's S6 and S7 lines in the main checkout carry the matching clauses (S6: advisory rows excluded from the class counts S1 and S6 read; S7: the asynchronous ask with a default, blocking only for a P0); plan 022 T12 names the amendment; plan 020 step 8 reads "resets only on a failed deterministic check or an unfixed P0/P1".

## INV-6 (rejected: the sentence cannot be enforced by the gate, the counters and the boundary check as they stand)

What stands on origin/main today: `require-crit-review.py` holds no count, threshold or reset logic (a search for counters, threshold, revises, reset and waiver finds nothing; plan 022's decisions panel entry D-S2-364 says the same); `regime-counters.sh` counts every task id with an AGMSG-TASK, prints `S2:` at `threshold=2` (line 60, "changing it is a hashed design change") for revises, amendments, questions and Bot P1 heads, and `S1:` for a ledger class with three rows (171); `check-regime-boundary.sh` reports a counted task over a threshold unless an accepted record with `pr=` or a reset record silences it (199 to 214) and reads `kind` from the task file's front matter (225 to 240). Nothing on origin/main writes or reads a `threshold_dispositions` key (a search over scripts, home and tests finds none; `acceptance-front-matter.py` writes `ledger`, `searches` and `audit_findings`).

Three clauses of the new sentence cannot be built or checked as written:

1. The deterministic-check trigger is circular and unqualified. "A reset is triggered only by a failed deterministic check (the gate's or the task-consistency check's refusal of the acceptance evidence) …" and, later, "when a trigger is reached the gate refuses the merge until a reset record names a redesign task": the gate's own refusal is its own reset cause, so the first refused chain run of any PR needs a redesign or a waiver to merge. Plan 022's log in the main checkout records the #361 chain's run 1 and run 2 as gate refusals of the record (a parenthetical in a `fixed:` row; missing ledger rows), both cured by fixing the record, merged at run 3; under this sentence both were triggers. The P0/P1 clause has the qualifier this clause lacks ("left unfixed after the one fix round") and a machine source (`original_commit_id` through pr-feedback.py; the audit JSON matched to its AGMSG-AUDIT record); a gate refusal is an exit status persisted nowhere the gate or the boundary check reads. A wording slip in the same clause: the task-consistency check refuses a task file (C1 to C10 and C7b on the task copy, at acceptance per every task's metadata row), not acceptance evidence. Ask: "a deterministic check that fails again on the final head after its one correction (the gate's refusal of the acceptance evidence; the task-consistency check's refusal of the task copy), recorded as <the record line the gate and the boundary check read>".
2. "counted toward a reset only when it carries a failed deterministic check or an unfixed P0-P1" names no source for "carries". A revise RESULT in history carries nothing; the v25 history paragraph and plan 022 T14 put the fact in the record's `threshold_dispositions` (T14: "the record block key written by acceptance-front-matter.py"), but that key is in no hashed sentence, has no writer on origin/main, and `acceptance-front-matter.py` is in neither mapped task's files (T14 lists the counters, the boundary check and their tests). Ask: INV-6 names the record key, its row shape (the count, the trigger or none, `evidence=`) and its writer, as it names the sources of the P0/P1 trigger; the map then needs the task that writes it.
3. "advisory rows excluded from that class count": the ledger rows the S1/S6 count reads are `{id, class}` (the a05 record's block; `regime-counters.sh:171`), with nothing that marks a row advisory; the advisory fact lives in the sweep disposition (`not-applicable:advisory P2 owned by …`) and the `## Owned by` prose. Ask: say how an advisory row is recognised (a field on the ledger row, or the disposition prefix in the sweep the counters already read).

Smaller, no verdict weight: "when a trigger is reached" and "a task over any trigger" are count words left from v24 (a trigger fires or is present); "review-brief task ids excluded from every count (a task file with kind: review)" is enforceable as written (the boundary check already reads `kind`) and matches its pr-less rule; "a P2 never counts" is clear; the INV-1 one-account residual clause is unchanged; dropping the numeric thresholds from the sentence is consistent with INV-7 (the change travels as a hashed design change, and T14 moves `threshold=2`).

## The two map entries

- `dotfiles-T128-gate-evidence-followup-a01: [INV-6]`: the file is on origin/main (sha256 prefix `51c983df`, written 2026-10-13); its front matter carries v24's INV-6 sentence, and INV-2 requires a task's invariants byte-for-byte equal to the design's on main, so the task fails INV-2 at its PR once v25 lands unless it is amended. Its item 1 is the owned rows under `## Owned by dotfiles-T128-gate-evidence-followup-a01` in the a04 record as read from origin/main, a section that record does not have today (its headings: integration, two ledgers, audit dispositions), which the item's own text makes a no-op. The entry is a valid mapping; the history paragraph's "the gate's reading of the new rule" is backed by no item of that file. P3: amend the task (the sentence, and an item for the gate's reading) before dispatch, or map the gate's reading to a task that carries it.
- `dotfiles-T128-counters-review-kind-a01: [INV-6]`: no task file yet; plan 022 T14 names it with its files and two test names. P3: the entry precedes the file, as earlier successor entries did; INV-2's comparison binds it once the file exists under that id.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: rejected (clauses 1 to 3 above). INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: revise
