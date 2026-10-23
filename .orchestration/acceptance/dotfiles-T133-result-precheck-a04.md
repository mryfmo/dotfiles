---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-result-precheck-a04 round=1 reset_of=dotfiles-T133-result-precheck-a03 repo=~/Workspace/dotfiles/.claude/worktrees/worker-c task_file=.orchestration/tasks/dotfiles-T133-result-precheck-a04.md task_sha256=ce5f7d06ba3f7b8efe55861eb264052528b691e25b3121300071e8b2b984a15a deadline=none done_signal=AGMSG-RESULT note=a009:the-reset-of-a03-after-the-security-review(eight-hardening-items)"
  ],
  "format": 1,
  "head": null,
  "ledger": [
    {
      "class": "precheck-head-binding",
      "id": "audit:bccb2de:1"
    },
    {
      "class": "baseline-unchecked",
      "id": "audit:bccb2de:2"
    },
    {
      "class": "substring-selection",
      "id": "audit:bccb2de:3"
    },
    {
      "class": "fail-open-on-error",
      "id": "audit:bccb2de:4"
    },
    {
      "class": "records-form",
      "id": "audit:bccb2de:5"
    },
    {
      "class": "path-traversal",
      "id": "audit:ddf262d:1"
    },
    {
      "class": "mask-on-error",
      "id": "audit:ddf262d:2"
    },
    {
      "class": "precheck-head-binding",
      "id": "audit:ddf262d:3"
    }
  ],
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
- 2026-10-19T11:45:54Z: the #411 chain update-branched the PR onto main 51ba5801 (f461d607 → 15380731) and refused: a required check failed on the new head (`test (ubuntu-24.04, server)`); the job log is being read (flake or a check that landed on main after the RESULT → D-024-24 rebase repair).
- 2026-10-19T11:5xZ: all four required unit jobs fail on the update-branch head 15380731 at "Run Python unit tests" (the job logs are not retrievable from this host through gh today; the worker reads them inside its sandbox). D-024-24 rebase-repair-1 sent to a009 (worker-c, the seat of this lineage): identify the failing tests, repair within allowed_files if a check landed on main after f461d607 (the lint of #415 is the likely cause), else report blocked; sequenced with its a04 owner task.
- 2026-10-19T12:03Z: main 51ba5801 is green (Unit test run 39236457264 success), so the four failing unit jobs on 15380731 come from the PR's files under a check that landed on main after its RESULT (the comparison lint of #415); the rebase repair with a009 stands.
- 2026-10-19T12:23:50Z: a009 RESULT rebase-repair-1: head 3838d0c6 (code head d3eb4249) on 51ba5801; the only failing test of 1288 was tests/unit/test_lint_comparisons.py::test_the_changed_files_are_clean_against_the_baseline on result-precheck.sh:127 (R1, the #415 lint that landed after f461d607): confined form normalised; baseline untouched; lint 97/97, shellcheck and shfmt clean. CI then chain, security review (security: true), gate.
- 2026-10-19T12:4xZ: lineage audit rows carried into this ledger for the chain's precheck (8).
audit:bccb2de:1	precheck-head-binding
audit:bccb2de:2	baseline-unchecked
audit:bccb2de:3	substring-selection
audit:bccb2de:4	fail-open-on-error
audit:bccb2de:5	records-form
audit:ddf262d:1	path-traversal
audit:ddf262d:2	mask-on-error
audit:ddf262d:3	precheck-head-binding

## Owned by dotfiles-T133-result-precheck-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:3838d0c:2	advisory-p2
local-finding: 3838d0c:2 not-applicable:advisory P2 owned by dotfiles-T133-result-precheck-followup-a01 (- [P2] Align the merge exemption with the regime CI verifier — scripts/orchestrator/dispatch.sh:230-231); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T133-result-precheck-followup-a01.md (b66f9b41fc936c7712f307b94c89e964af942fb6967ad8c7cbf9b792b58fb3d9)
- 2026-10-19T12:47:08Z: the #411 chain on the repaired head 3838d0c6: local review one P1 (dispatch.sh:337 sends `--premises-sha` before the checker on main supports it: the consumer lands with P1-12 a03, PR #417) and two advisory P2 recorded under the owner. Judgment: a sequencing finding, not a code defect: the a04 wiring is correct once #417 merges; this chain ran early for parallelism. Decision: #411 waits for #417, then update-branch and re-chain; no worker round.
local:3838d0c:1	sequencing-dependency

## Update-branch head 94fa6465 (2026-10-21T09:34Z)

- PR #411 update-branched after the pins merge (main 4eafd890): required checks green, non-required `regime` red. Clean reproduction in the review worktree at 4eafd890 (`regime-ci.py --base 4eafd890 --head 94fa6465`, exit 1, 33 lines): (1) `precheck: precheck.json head d3eb4249 differs from the head outside .orchestration/dotfiles-T133-result-precheck-a04/` (the update-branch merge brought main's changes, so the committed precheck no longer covers the head); (2) 32 `allowed-files` refusals for `.orchestration/dotfiles-T133-result-precheck-a01/` and `-a02/` artifacts the branch carries from the lineage, which the a04 text did not declare in `retained_predecessor_directories`. The regime verifier (clean reproduction) is the evidence; the job log itself is unreadable from the sandbox (gh's run-log cache write is denied).
- D-024-61 (recommended default executed): amendment 1 of the a04 text adds `retained_predecessor_directories` (a01/, a02/, a03/) and the rule that the worker re-runs the precheck after every update-branch in a records-only round; the amended bytes need C-80 (security: true), then reach main in records boundary 28, then a records-only round updates the task copy and `precheck.json` on the branch (another Claude seat may run it, since a009 is on pre-send a03), then regime rerun, chain, security review, gate, merge. The S2 rows of the a03 security review are dispositioned in the a03 record (rows 1,2,4 carried by a04; rows 3,5 owned by followup-a01).

