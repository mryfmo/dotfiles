---
{
  "format": 1,
  "task": "dotfiles-T128-project-map-pane-open-a01-followup-a01",
  "head": "2842c345f56113594f3feb298fb0a731baacee3b",
  "pr": 379,
  "ledger": [],
  "searches": [],
  "audit_findings": []
}
---

# Acceptance record: dotfiles-T128-project-map-pane-open-a01-followup-a01 (the residual findings of PR #359: the map tab matched to the event before the pane is declared present; plan 020 step 1; the owner task of the pane-open lineage; Codex seat)

- 2026-10-15T00:3xZ record created before the first dispatch (Orchestrator Playbook step 6). The task text was written when the Bot's first advisory P2 on PR #359 (thread comment 4277695198, head 73f51ab2) appeared, as the lineage task's Completion requires; its paired one-round review (brief `dotfiles-T128-project-map-pane-open-a01-followup-review-a01`) goes to the review seat and the Codex half; its two premises read `origin/main` and replay `absent` until the boundary that lands the lineage task file and the record's owner section; the dispatch follows that boundary, the hook follow-up's merge (the same four files, INV-10) and a one-round refresh of the premise outputs, to `codex-standard-dot-a004` (Claude-boundary files).
- 2026-10-15T00:34Z pair-confirmed on `ace9aebd46d6c440d90a41dd501cbe3fa6108c44ea1a39e5340196b39560b738` (one round): the Codex half's receipt `validation/dotfiles-T128-project-map-pane-open-a01-followup-review-a01-codex-r1.md` (`confirm`, no finding) and the review seat's `AGMSG-RESULT … round=1 verdict=confirm owner_task_sha256=ace9aebd…` at 00:34:23Z; ACCEPTANCE accepted to the seat. Premise 1 reads `present` (the lineage task file landed with boundary (15)); premise 2 reads `absent` until the boundary that lands the lineage record's owner section (one row today, `4277695198`, plus the audit row `audit:73f51ab:1`); the pre-boundary copy is kept under the orchestrator's glue directory for the refresh round. Dispatch order: after PR #359 merges, after the hook follow-up (the same four files) merges, after that boundary and the one-round premise refresh; to `codex-standard-dot-a004`.

re-plan: path-form-normalisation -> specification: the hook compares every tab URL and map path in one canonical form, the file URL that pathToFileURL(realpath) yields (home expanded, physical cwd, no trailing slash, percent-encoding as Node encodes it); design: one normaliser function on both sides of every comparison, no string form compared directly (plan 023 PR F2 lints the forms); implementation: the four fixes of rounds 2 and 3 (c0c3ff05, 02fdf061, 40d18027, e234a05b) route each input through that normaliser; verification: one test per form (encoded tilde, logical cwd, bare tilde, trailing slash, encoded separator) asserting identity of the normalised values, not absence of a mismatch. Written 2026-10-17T10:08Z by the orchestrator (D-S1-379, default A); the six path-form rows above are this one class.

## Ledger rows (id<TAB>class; read by the block writer)

Written 2026-10-17T10:25Z by the orchestrator (the chain 3 and 4 refusals of 2026-10-17 10:0xZ: the block writer reads tab rows, not the block): the four Bot threads of PR #379 and the six findings of the audits of 990b607 and 8607a87, six of them one class, which the re-plan line above covers.

4300474045	path-form-normalisation
4300561777	path-form-normalisation
4301859324	path-form-normalisation
4301888204	path-form-normalisation
audit:990b607:1	path-form-normalisation
audit:990b607:2	record-counting
audit:990b607:3	evidence-checkpoint
audit:8607a87:1	path-form-normalisation
audit:8607a87:2	live-verification
audit:8607a87:3	record-counting
