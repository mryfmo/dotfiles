# Acceptance: dotfiles-T128-task-review-phase1-a01 (one task-file review round over T702, T703, T715; review seat + Codex headless)

- kind: review; pr: none; cost: n/a
- task_file: `.orchestration/tasks/dotfiles-T128-task-review-phase1-a01.md` sha256 `973872460fd26a65…` (full hash in the TASK line)
- reviewed (both halves on the same files): gate-evidence `cba77a8d…`, playbook-rules `15ae4da2…`, aws-cli-macos `6000f026…`; design v18 `7f007ec4…`
- dispatch (C-12 form; `history.sh dotfiles-conformance`, ○ = read): `○ [2026-10-12T11:40:38Z] claude-deep-dot → claude-review-dot-a001: AGMSG-TASK v1 task_id=dotfiles-T128-task-review-phase1-a01 …`; `○ [2026-10-12T11:45:40Z] claude-review-dot-a001 → claude-deep-dot: AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase1-a01 status=ready_for_review verdicts=…:revise,…:revise,…:revise receipt=… receipt_sha256=5cc69df9…`; `○ [2026-10-12T11:47:10Z] claude-deep-dot → claude-review-dot-a001: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-task-review-phase1-a01 status=accepted …`
- receipts: seat `.orchestration/validation/dotfiles-T128-task-review-phase1-a01.md` (sha256 verified `5cc69df9…`, 11:46Z); Codex `.orchestration/validation/dotfiles-T128-task-review-phase1-a01-codex.md` (11:42Z, after the 11:15Z run hung on stdin, M-20261012-12)
- counters (`scripts/regime-counters.sh dotfiles-T128-task-review-phase1-a01 --history-only`, 11:51Z):

```text
task=dotfiles-T128-task-review-phase1-a01 tasks=1 amendments=0 questions=0 results=1 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=skipped audits=unknown wall=2026-10-12T11:40:38Z..2026-10-12T11:45:40Z (0:05) source=live
detail: pr=none authors=claude-deep-dot tasks=01a12fea-2af0-79ff-8bea-f54ed19343c1 results=01a12fee-c6a0-76ec-8c6a-4db22db1e640 questions=- withdrawn=- bot_heads=- source=live
```

- decision: both halves `revise` on all three; one revision applied 11:51Z (new hashes: gate-evidence `86431d3e…`, playbook-rules `391eeeac…`, aws-cli-macos `fdc66955…`, before the metadata-row quoting fix; final hashes in the TASK lines); no second round (the SKILL's one-round rule); dispatch after the boundary PR that carries design v20 (INV-2).

## Findings and dispositions

| # | source | prio | file:line (pre-revision) | class | disposition |
|---|---|---|---|---|---|
| S-T702-1 | seat | P1 | gate-evidence:16 | invariants-block-missing | applied: `invariants:` carries INV-6's v20 sentence byte for byte (copied from the design line) |
| S-T702-2 / C-T702-2 | seat, codex | P2 / P1 | gate-evidence:64,10 | gate-input-touch-points | applied: `ACCEPTANCE_EVIDENCE` stays required in PR mode; `Makefile` and `README.md` join allowed_files with rows; item 2 names the recipe list, the comment and README 427/1101; existing PR-mode tests gain the variable; the SKILL step 10.4 sentence moves to T703 item 6 |
| C-T702-3 | codex | P2 | gate-evidence:45 | premise-command-portability | applied: premise 3 uses awk; output re-pasted from the run of 11:4xZ |
| C-T702-1 / C-T703-1 / C-T715-1 | codex | P1 | *:8 | receipt-pointer | applied: `design_review.receipt` = round 22 (the design's pointer moved at 11:51Z; C6 re-run before dispatch) |
| S-T703-1 | seat | P2 | playbook-rules:64 | oracle-token-stale | applied: item 5 names the line-278 token |
| S-T703-2 | seat | P2 | playbook-rules:66 | gate-input-touch-points | applied: item 6 (step 10.4 gains `ACCEPTANCE_EVIDENCE`); items renumbered |
| C-T703-2 / C-T715-2 | codex | P2 | playbook-rules:30, aws-cli:27 | threat-row-unit | applied: the combined non-path rows split one per control in all three files (13, 12, 13 rows) |
| S-T715-1 | seat | P2 | aws-cli:45 | premise-output-not-as-printed | applied: premise 2 re-run 11:4xZ and pasted as printed (7 lines, ascending) |
| S-T715-2 | seat | P3 | aws-cli:69 | premise-missing | applied: premise 4 (gpg formula at line 21 keeps gpgv) and the item 1 sentence |
| C-T715-1 | codex | P1 | aws-cli:64 | plan-task-contradiction | applied: plan 007 T715 row corrected (manifest untouched, no `aws update`), task unchanged on that point |
| C-T715-1b | codex | P1 | aws-cli:15 | wrong-test-file | applied: `brew.bats` dropped; the existing assertion at test_aws_cli_acquisition.py 636–637 is the one to change |

## Ledger (class counts)

invariants-block-missing 1; gate-input-touch-points 2; premise-command-portability 1; receipt-pointer 1 (one finding repeated per file); oracle-token-stale 1; threat-row-unit 2; premise-output-not-as-printed 1; premise-missing 1; plan-task-contradiction 1; wrong-test-file 1. Highest 2: S1 not reached. Own mistakes surfaced: a premise output pasted out of order (run-not-recall), a plan row contradicting its task, a test file named without reading it; all three are the "recalled, not run" class already under M-20261012-10/C-12 and M-20261012-13/C-15 (the author's own check before the request).
