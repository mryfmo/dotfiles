---
id: M-20261019-03
artifact: "dotfiles-T133-permission-guard-gate-a04: after the security review of 911f5202 reported two P1 of the class the a03 review had already reported three of (decision-not-bound-to-execution), the orchestrator drafted revise 1 for the two instances (updatedInput rewrites) instead of stopping at S1 and re-planning; the operator's question of 2026-10-19T02:1xZ exposed it before the send"
classes: [replan-not-patch, s1-overrun]
found_at: "2026-10-19T02:1xZ (the operator)"
detector: "the operator, not the counter: regime-counters.sh counts rows per task record, and the class spans the a03 and a04 records"
count_at_detection: "five findings of one class, a sixth (the local review) minutes later; one deadline missed"
corrections: [C-59, C-80, C-81]
status: open
recorded_at: "2026-10-19T02:2xZ"
---

# M-20261019-03

- **Evidence:** `.orchestration/validation/dotfiles-T133-permission-guard-gate-a03-security-31d6c32.md` (3 P1), `…-a04-security-911f520.md` (2 P1), `…-a04-local-review-911f520.md` (1 P1); the revise draft `$TMPDIR/revise-p114-a04-draft.txt` (never sent); the report of 02:1xZ that announced the revise.
- **Detection and why not earlier:** the class table is kept per record; the counter's S1 reads one record's ledger; the a04 record held 0 rows of the class when the review landed because security findings are filed in validation, not the ledger, until disposition.
- **Root cause:** security-review findings do not enter the ledger as rows at the moment they are reported, so the S1 counter never sees them; and the orchestrator treated "a reviewer named a fix" as "a round is the answer" (M-20261017-04's pattern).
- **Should have been:** at the a04 review (instances 4 and 5) the orchestrator writes the class table across the lineage's records, stops, and re-plans at the tier the class points to (design).
- **Corrections:** C-80 (new): the security-profile review of a `security: true` task text and threat table runs before dispatch, and its findings count toward the class table; C-81 (new): a security review's `[P0-P1]` findings are written to the record's ledger as `security:<sha7>:n` rows with their class at the moment the review lands, and `regime-counters.sh --lineage` counts classes across the lineage's records (P1-12 owner, with C16).
