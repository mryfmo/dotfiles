---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-record-ledger-carry-a01"
}
---

# Acceptance record: dotfiles-T133-record-ledger-carry-a01

Plan 024 P1-6 slice 1 (record automation): the chain carries the lineage audit rows and the dispatch lines it checks; ledger-check.py reads the JSON ledger too. Files disjoint from dotfiles-T133-loop-limits-a01. Written after M-20261019-06 (five ledger-gap refusals and three empty dispatch lists on 2026-10-19/20).

- 2026-10-19T21:46:31Z: text authored by the review profile (prompt `p16-slice1-author-prompt.md`, output `redesign/p16-slice1.md`), installed with `$HOME`-relative paths: 227 lines, 5 allowed files, 18 threat rows, 10 premises (proposal 1 caps 250/10 met); checker OK; C-80 round 1 running (security: true).
- 2026-10-19T21:48:17Z: C-80 round 1 (`…-text-security-a26cc07.md`) `Verdict: incorrect`: P1 the dispatch prerequisite covers the trusted parent and interpreter but not the retained callees (orch-audit.sh resolves uv itself and reads the shared git store): the text must require compliant downstream consumers before execution, with a test that they consume the authenticated inputs, or mark the row residual with its owner task; P2 the `closed` containment row names a lineage symlink-escape test that covers neither case aliases, worker-root exclusion nor record/sidecar destination checks; P2 the dispatch sidecar records the current head only, so two audits sharing sha7 and finding number collapse under duplicate-row handling (undercounting S1/S6): per-audit provenance (full head, audit-file sha256) and collision refusal. Design 5.14 stays frozen (D-024-29): all three apply existing items 2, 3, 8 and 9 to this text. Amendment 1 via the review profile (`p16-slice1-r2-prompt.md`, whole text, within 250 lines); C-92 budget 1 of 3.
text-security:a26cc07:1	excluded-command-trusts-sandbox-context
text-security:a26cc07:2	happy-path-closing-test
text-security:a26cc07:3	hash-binding
- 2026-10-19T21:57:08Z: amendment 1 (`redesign/p16-slice1-r2.md`) installed with `$HOME`-relative paths: 249 lines (cap 250), 5 files, 23 threat rows (9 closed with selectors, 14 residual; the orch-audit.sh and ci-rerun.sh callees residual with owners verdict-audit-pool-a04 and ci-efficiency-followup-a04 and a named refusal until their compliance is on main; per-audit provenance and collision refusal in the sidecar); checker OK; C-80 round 2 running (budget 2 of 3 when it returns).
- 2026-10-19T21:59:08Z: C-80 round 2 (`…-text-security-6cbe954.md`) `Verdict: incorrect`: P2 the callee inventory still omits sandbox-scan.sh, local-review.sh and local-advisory.sh (local-review.sh resolves executables itself and diffs against the local `main` ref, a shared-store input); P2 the owner named for orch-audit.sh's hardening (verdict-audit-pool-a04) does not own it (the pool sibling audit-pool-a02 does). Second row of the excluded-command-trusts-sandbox-context family and the second amendment (S2): not a third patch. Re-examination: the slice tied its carry step to chain-integrate.sh, so every retained callee of the chain became its prerequisite, and those callees belong to other tasks sequenced after P1-15; the slice cannot deliver "complete chain execution binding" and must not claim it.
text-security:6cbe954:1	excluded-command-trusts-sandbox-context
text-security:6cbe954:2	missing-owner-task
re-plan: excluded-command-trusts-sandbox-context (rows text-security:a26cc07:1, text-security:6cbe954:1, text-security:6cbe954:2) — specification: the slice depends on no callee of chain-integrate.sh; design: a standalone pre-chain program `scripts/orchestrator/carry-lineage.py` run by the orchestrator under the trusted parent (5.14 items 2, 3, 9) carries the lineage audit rows (prose and JSON) and fills the dispatch list from messages.db with content binding (a TASK line counts only when its task_sha256 equals the dispatched text's sha256; an ACCEPTANCE line only when its head is the record's head or a predecessor head), and ledger-check.py reads the JSON ledger too; chain-integrate.sh is untouched, so the callee rows and their owners leave this text (local-review.sh's base-ref binding goes to the chain-review-scripts owner a07 as an item); implementation: round 3 text by the review profile; verification: tests per program, C-80 round 3 with a fresh budget after this line.
- 2026-10-20T00:04:50Z: C-80 round 2 after the re-plan (`…-text-security-f3bfcc6.md`) `Verdict: correct` (28 threat rows; the item-7 hostile Git environment and configuration tested through the shared helper; chain execution excluded). Text ready: 226 lines, 5 files, after: [dotfiles-T133-trusted-exec-contract-tests-a01]; waits a Codex seat (D-024-25) and the helper's merge.
text-security:f3bfcc6:0	correct

