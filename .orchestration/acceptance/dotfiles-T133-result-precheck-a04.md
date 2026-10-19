---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-result-precheck-a04 round=1 reset_of=dotfiles-T133-result-precheck-a03 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-result-precheck-a04.md task_sha256=ce5f7d06ba3f7b8efe55861eb264052528b691e25b3121300071e8b2b984a15a deadline=none done_signal=AGMSG-RESULT note=a009:the-reset-of-a03-after-the-security-review(eight-hardening-items)"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 411,
  "searches": [],
  "task": "dotfiles-T133-result-precheck-a04"
}
---

# Acceptance record: dotfiles-T133-result-precheck-a04

Plan 024 P1-5, the reset of `dotfiles-T133-result-precheck-a03` after its security-profile review (two P1: a masking failure prints the raw captured text; evidence writes follow repository-controlled symlinks) with the security P2, the audit P2 of ddf262d and the `--premises-sha` wiring of dispatch.sh as eight hardening items. Redesigned by a review-profile context (`.agents/worklog/orchestrator-glue/redesign/p15-a04.md`, prompt `p15-a04-redesign-prompt.md`); seat a009 (worker-c, Claude) continues PR #411 on `tools/result-precheck-a01` from ddf262d, ahead of its `dotfiles-T133-audit-pool-a01`. Owner of advisory P2: `dotfiles-T133-result-precheck-followup-a01` (its rows absorbed here).

- 2026-10-19T00:4xZ: `task-consistency-check.py … : OK`, home-path scan 0 matches, dispatched to a009 (the line above; the full note is in the bus history). In-flight file check (C-78): result-precheck.sh, dispatch.sh, the two githooks and test_result_precheck.py appear in no other in-flight task.
- 2026-10-19T01:20:05Z: a009 `status=blocked`: hardening item 8 (dispatch.sh passes `--premises-sha` to the checker) conflicts with `tests/unit/test_orchestrator_tools.py`, outside allowed_files but in the Check: `test_dispatch_refuses_a_task_file_failing_the_checker` (line 470) and `test_dispatch_resolves_its_root_without_inherited_git_variables` (line 587) assert the exact substring `task-consistency-check.py --root <root> <task-file>`, and the stub checker reads the task file as `sys.argv[-1]`; no argument order satisfies both (7 failures either way). Everything else is implemented at 838fc9e9 (local; the eight hardening tests red on ddf262d, green there); caps at 599/600 tests and 480/480 source. a009 also reports: main's checker before PR #417 rejects `--premises-sha`, so #417 must merge before #411 or every TASK dispatch is refused.
- decision: amendment 1 (INV-6 amendments 0 → 1): `tests/unit/test_orchestrator_tools.py` joins allowed_files for the two expected argv strings and the stub's argument reading only; the argv order is `--root <root> --premises-sha <sha> <task-file>` (the file stays last); caps measured by the worker's paste (C-79): tests 600 → 640, source 480 → 500. C-78: PR #423 (audit-inherit follow-up a02, pending integration) also lists that test file; #423 merges before #411, and #411 takes the new base by update-branch (a conflict there is a rebase by a009, not a round). Integration order: #417 before #411 (the live checker gains `--premises-sha` first); recorded in the progress table.
- 2026-10-19T01:29:4xZ: amendment 1 dispatched to a009 (wJ:p2) as a TASK line with the new text (task sha256 e52afb63…, previous ce5f7d06…; `task-consistency-check`: OK; counters before the send pasted in the text: tasks=1 amendments=0 questions=0 results=0; INV-6 now amendments 1). The threat row for the joined file names `test_dispatch_refuses_a_task_file_failing_the_checker`.
- 2026-10-19T03:31:54Z: RESULT round 1 (amendment 1) from a009: PR #411 head f461d6072332598f7edb4cc8d1fbe944935f763a (precheck head 9f6ec7c9, precheck sha 2b921eb1…), continued from ddf262de on 740772ef, branch `tools/result-precheck-a01`; `task_copy=e52afb63…` (amendment 1's sha); CI 10/11 (the optional regime check fails on the stale base, the P1-11 defect). `status=pending-integration` sent 03:3xZ; the integration order #417 → #415 → #424 → #425 → #410 → #411 stands (the checker that accepts `--premises-sha` lands first).
