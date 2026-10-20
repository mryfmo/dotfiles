---
{
  "audit_findings": [
    {
      "evidence": ".orchestration/validation/dotfiles-T133-regime-ci-followup-a01-audit-380e7f4.md.last.md; .orchestration/dotfiles-T133-regime-ci-followup-a01/validation.md:123; report.md:68; .orchestration/acceptance/dotfiles-T133-regime-ci-a02.md row audit:7fad835:2",
      "n": "1",
      "reason": "advisory P2 (orchestration, no code change): the a01 task text inherited the a02 Check clause verbatim, including the 'bootstrap on the final head' wording that the a02 record's owned row audit:7fad835:2 reworded to the code head with an evidence-only commit; the worker followed the reworded rule (validation.md:123 bootstraps the code head b65dd4c2, report.md:68 says so), so the evidence is right and the dispatched text is stale; owned by dotfiles-T133-regime-ci-followup-a02, whose Check clause states the reworded rule explicitly (owner task present before this row, C-51)"
    }
  ],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T133-regime-ci-followup-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-d task_file=.orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md task_sha256=65d4b24a390674b303e7dcad6a305be7584ebf49e5f3776f2560dd9ffc14a0a1 deadline=none done_signal=AGMSG-RESULT note=a011:owner-task-of-P1-11(PR-418-merged-0e496ce7;the-3-rows-are-in-the-Owned-by-section-of-.orchestration/acceptance/dotfiles-T133-regime-ci-a02.md);fresh-branch-from-origin/main;for-the-stale-pr-description-row-write-the-new-title-and-body-to-.orchestration/dotfiles-T133-regime-ci-followup-a01/pr-body.md-and-the-orchestrator-applies-them-at-acceptance(no-gh-pr-edit-from-the-seat);the-two-text-rows-are-realized-in-this-task-s-own-threat-table,Check-wording-and-validation,never-by-editing-the-a02-copy;your-#424-is-pending-integration-and-needs-nothing-from-you"
  ],
  "format": 1,
  "head": "380e7f4d048097ce3bddc76194f24dbc01be7f42",
  "ledger": [
    {
      "class": "threat-row-stale",
      "id": "4310261909"
    },
    {
      "class": "evidence-head-mismatch",
      "id": "audit:380e7f4:1"
    }
  ],
  "pr": 425,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T133-regime-ci-followup-a01"
}
---

# Acceptance: dotfiles-T133-regime-ci-followup-a01 (plan 024 P1-11 owner task; the 3 advisory rows of PR #418)

- rows owned (from the a02 record's Owned by section): audit:f7d2c48:3 stale-pr-description; audit:7fad835:1 threat-row-selector; audit:7fad835:2 evidence-head-mismatch (the wording). The stale-description row is realized as a pr-body.md the orchestrator applies at acceptance (gh pr edit stays off every seat).
- 2026-10-19T01:3xZ: TASK dispatched to a011 (wJ:p4, worker-d) after its #424 RESULT; sha256 65d4b24a…; counters zeros; checker OK; C-78 no overlap.
- 2026-10-19T01:50:11Z: a011 `status=alive`: the PING read 01:45:36Z; row `ci:39185982423:1` taken before any push (code head e0565b47 holds the task copy and pr-body.md); the fix in regime.yml with a red-then-green test; the three text rows done locally.
- 2026-10-19T02:27:33Z: a011 `status=alive`: final head 538a9b76 pushed (code head b65dd4c2; the evidence commit touches only the task directory); draft PR #425 open; CI and the 15-minute Bot window running, then the RESULT; the PR #418 description correction is in pr-body.md for the orchestrator to apply at acceptance.
- 2026-10-19T02:44:05Z: RESULT round 1 from a011: PR #425 (draft) head 538a9b762ff9c58202fd6f3b15f6224617c5ad62 (code head b65dd4c2) on 0e496ce7, branch `tools/regime-ci-followup-a01`; `task_copy=65d4b24a…` (the dispatched sha); rows: audit:f7d2c48:3 realized as pr-body.md (applied by the orchestrator at acceptance), audit:7fad835:1 realized in report.md (five tests close the regime-ci.py control, 9 mutations red), audit:7fad835:2 realized (bootstrap on the code head from the base tip, evidence commit touches only the task directory), ci:39185982423:1 fixed e6ea7c8d (red 6c96e10a: regime.yml checks out `refs/heads/${{ github.base_ref }}` and the verifier takes `--base $(git rev-parse HEAD)`; BASE_SHA removed; regime-ci.py unchanged); checks `test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time`, `test_the_regime_workflow_runs_base_code_only`, `test_regime_ci_accepts_a_base_that_moved_past_the_merge_base`; CI 11/11 on 538a9b76 (the regime run 39190011913 on main's workflow: ok 1 task); Bot none in 914 s; CodeRabbit auto-notice (not-applicable); caps 7/330 and 28/480; worker review 2 rounds (records round 1, P3s in b65dd4c2; the C-61 cap). Worker notes: the 4th row arrived by PING (recorded 01:50Z; the text reads rows from the record, no amendment); the a02 row text "base.sha changes only when the PR synchronizes" is imprecise (the run shows base.sha = the fork point 740772ef at the event) → corrected in the a02 record; actions/checkout's resolution of a `refs/heads/` ref is verified at the first post-merge run. `status=pending-integration` sent 02:4xZ; chain after #424.

## Owned by dotfiles-T133-regime-ci-followup-a02

- `ci:39194965216:1` lineage-directories-as-targets: on PR #412 (head 53642ace, base b22a5580) the regime check treats every `.orchestration/<task>/task.md` of the D lineage (a01, followup-a01 … a05, a followup-named lineage without `reset_of`) as a target, flags their old caps and demands preserved predecessor artifacts, and warns that the a05 dispatched text is absent at the base (records reach main only at a boundary); the check scopes its targets to the task copies the pull request adds or changes (git diff base...head under .orchestration/*/task.md) and treats an absent dispatched text as the documented warning, not a violation, until REGIME_REQUIRE_DISPATCHED (evidence: .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/ci-regime-pr412-failed.log).
- 2026-10-19T04:53Z: parallel-chain attempt: three extra review worktrees (orchestrator-review-2/3/4) were created and chains for #425, #412 and #426 launched on them; chain-integrate.sh refused each ("review worktree is not the canonical one"). The guard is the tracked script's; bypassing it by running the sub-steps by hand is not taken. Chains stay serial on the canonical worktree; the per-PR worktree is P1-6's item (C-85 amended). The extra worktrees stay for later use.

## Security review of 80e4040a (2026-10-19T05:32Z, the update-branch head): one P2, no P0/P1

- `.orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-80e4040.md`: `Verdict: incorrect` on one P2: the owner text's workflow/environment residual says "no workflow file is in allowed_files" while regime.yml is allowed and the PR changes which commit supplies the verifier (the threat-row-stale class, the orchestrator's template text; checker rule C17 is the mechanism fix, filed to the P1-12 owner). No code defect. Decision: accept when the chain reaches the gate (C-82: no P0/P1 line); the P2 is an advisory row of the regime owner a02.

security:80e4040:1	threat-row-stale

## Owned by dotfiles-T133-regime-ci-followup-a02 (continued)

- `security:80e4040:1` threat-row-stale: the regime owner text's workflow residual states the actual base-branch trust assumption (the verifier runs from the base branch tip at run time; the PR cannot select it) instead of "no workflow file is in allowed_files".
- `ci:detection:1` merge-without-record detection (D-024-23): the regime job, on a pull request that touches `.orchestration/acceptance/**`, lists the merge commits of main since the previous boundary merge and fails when one has no acceptance record whose JSON head equals the merged head and whose record states the gate passed; a fixture with one unrecorded merge is red.

## Bot round on 380e7f4 (2026-10-19T06:24Z): one P1 thread, dispositioned by refutation

- The chain update-branched #425 again (80e4040a → 380e7f4d over main 205fe85c); the sweep found the Codex Bot P1 thread 4310261909 on `task.md:33`: the workflow residual row is false (regime.yml is in allowed_files) and the row names no control for `github.base_ref`. Disposition `not-applicable` with the refutation in 425-extra.tsv: the row is the frozen template text (threat-row-stale, owner row security:80e4040:1 of followup-a02, C17); the risk is controlled by the implemented design (the workflow runs from the base branch tip; `github.base_ref` is GitHub's event field for the protected target branch, not PR-supplied; the shape test names it). The security review re-runs on 380e7f4 (the 80e4040a review is stale).

4310261909	threat-row-stale

## Security review of 380e7f4 (2026-10-19T06:27Z, the second update-branch head): one P2, one P3, no P0/P1

- `.orchestration/validation/dotfiles-T133-regime-ci-followup-a01-security-380e7f4.md`: P2 the same false workflow residual row of the owner text (threat-row-stale); P3 the in-process row claims a fake-PATH isolation the tests do not implement (they run real git and uv with the inherited environment in temporary repositories). No code defect. Decision: accept at the gate (C-82: no P0/P1 line); both are owner rows of regime-ci-followup-a02 (the residual and the in-process rows restated to the actual controls).

security:380e7f4:1	threat-row-stale
security:380e7f4:2	records-form

- `security:380e7f4:2` records-form (owner a02): the in-process threat row states the actual isolation of the regime tests (temporary repositories; real git and uv under the inherited environment) instead of a fake PATH.
- 2026-10-19T06:33Z: the chain re-run on 380e7f4 (sweep 7 items filled, 0 gaps; the Bot P1 4310261909 refuted): task-level audit `…-audit-380e7f4.md`: `Verdict: incorrect` on one P2 (orchestration): the a01 text inherited a02's Check wording 'bootstrap on the final head' that the owned row audit:7fad835:2 had reworded (code head + evidence-only commit); the worker followed the reworded rule (validation.md:123 at code head b65dd4c2; report.md:68), so the evidence is right and the text stale. No implementation or security regression; INV-6 holds (two worker fix rounds). Root cause: the a01 text was written from the a02 Check by copy before the a02 record's rows were applied to it (C-class: inherited-check-stale, the same mechanism as threat-row-stale). Disposition: advisory P2 owned by dotfiles-T133-regime-ci-followup-a02 (its Check states the reworded rule; sentence added 06:3xZ, checker OK). Gate and merge follow with the security review of 380e7f4 (P2/P3 only).
audit:380e7f4:1	evidence-head-mismatch

## Owned by dotfiles-T133-regime-ci-followup-a02 (audit row)

- `audit:380e7f4:1` evidence-head-mismatch: the owner text's Check states the reworded bootstrap evidence rule (code head; evidence commit touching only the task directory) instead of the inherited 'final head' wording; report.md names the code head it bootstrapped.

## Owned by dotfiles-T133-regime-ci-followup-a02 (records PR observation)

- `ci:39239649184:1` evidence-sync-task-dir: on the records-only PR #429 the regime job treated three task directories as task PRs (1,790 paths outside their allowed files) because the orchestrator's evidence sync (#422, the evidence-sync exemption) placed worker evidence into directories that already hold a task.md; the regime check recognises a records-only boundary PR (branch prefix `orchestration/boundary-` and no code change) and an orchestrator evidence sync, instead of applying the task-PR copy rules to it.
ci:39239649184:1	evidence-sync-task-dir
- 2026-10-20T00:25:06Z: regime job false positive on the records boundary PR #435 (run 39346975816): the job inferred the task dotfiles-T128-chain-github-scripts-followup-a02 from the restored task copy the boundary carries and then reported every other record file as `outside allowed_files` (3 warnings, 12+ allowed-files lines). A records boundary (branch `orchestration/boundary-*`, PR by the orchestrator) is not a task PR; regime-ci.py needs to recognise it (skip the allowed-files and task-copy checks, keep the secrets and home-path scans). Owned by the regime-ci owner lineage (followup-a02): row below. Non-required check; the boundary merges on the operator's approval.
local:8f7b976:1	boundary-pr-misread-as-task

