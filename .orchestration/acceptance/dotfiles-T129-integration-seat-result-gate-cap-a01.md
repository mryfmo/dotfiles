---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md task_sha256=40516966f5698e05ba3efb9a27212de645a81a20735ae8952de2684bff866a22 deadline=none done_signal=AGMSG-RESULT note=operator-directive-21:32-JST-item-4(approved):plan-023-PR-F4-as-one-PR(the-integration-seat-script,the-pre-RESULT-gate,the-numeric-worker-cap);you-are-the-free-Claude-seat(no-Claude-permission-boundary-file-in-allowed_files);start-now-on-a-fresh-branch-from-origin/main(your-#390-branch-stays-for-its-integration);read-the-task-file-first:items-1-to-3,Out-of-scope,the-Check-and-the-Completion-clause;run-result-precheck.sh-on-your-own-head-before-the-RESULT read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 round=1 amendment=1 previous_task_sha256=40516966f5698e05ba3efb9a27212de645a81a20735ae8952de2684bff866a22 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md task_sha256=393dcbac2155fabe1657c048ba9a34eb8dfa612e09d7e7883fe7d26006c6b813 deadline=none note=amendment-1(M-20261017-07,C-62):both-new-scripts-export-CLICOLOR_FORCE=0-FORCE_COLOR=0-NO_COLOR=1-after-set-euo-pipefail(gh-colors-JSON-when-the-shell-forces-color-and-CLICOLOR_FORCE-beats-NO_COLOR),no-step-hides-a-parser-exit-status,one-test-with-CLICOLOR_FORCE=1-and-a-coloring-stub-gh;read-the-Amendment-1-section;copy-the-amended-text-as-task.md read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 round=1 amendment=2 previous_task_sha256=393dcbac2155fabe1657c048ba9a34eb8dfa612e09d7e7883fe7d26006c6b813 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md task_sha256=4e00bf122f578a9dbbde8ac36feb025d68cb828009a2e9f009606ad760879081 deadline=none note=answer-to-your-13:13Z-caps-question:option-A,the-Check-cap-is-260-for-this-PR(D-cap-F4);your-readings-stand(worker_cap-by-sed-from-the-deployed-manifest,missing-key-means-no-cap-plus-one-stderr-line;allowed_files-by-sed;g-reads-the-report-s-thread-tokens);one-correction:precheck-h-and-i-are-three-state(ok,unavailable-with-reason,missing)and-verify-refuses-only-missing;read-Amendment-2;copy-the-amended-text-as-task.md;continue read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 round=1 amendment=3 previous_task_sha256=4e00bf122f578a9dbbde8ac36feb025d68cb828009a2e9f009606ad760879081 repo=~/Workspace/dotfiles/.claude/worktrees/worker-f task_file=.orchestration/tasks/dotfiles-T129-integration-seat-result-gate-cap-a01.md task_sha256=626823fbf25a2a48bad0ae1e05792e6ea5f25ea4d1e4c710e973da64b62d1864 deadline=none note=answer-to-your-14:16Z-question:option-A(test_agmsg_orchestration_docs.py-budget-450-to-490,tests/fixtures/regime/worker-step-15.md-follows-item-3-s-sentence;both-in-allowed_files-with-rows);fold-the-P1-4302959624-into-this-push-as-fix-round-2-of-INV-6(D-F4-round2:one-grep-for-threads=-selecting-the-newest-worker-RESULT,one-failing-test;no-round-after-it);the-P2-4302959629-is-advisory-under-dotfiles-T129-integration-seat-result-gate-cap-followup-a01(written);then-CI,the-step-15-Bot-wait-without-a-further-@codex-review,RESULT;read-Amendment-3;copy-the-amended-text-as-task.md read_at=read"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T129-integration-seat-result-gate-cap-a01"
}
---
# Acceptance record: dotfiles-T129-integration-seat-result-gate-cap-a01

plan 023 PR F4 (the operator's directive of 2026-10-17 21:32 JST, item 4, one batch, approved): the integration seat (`integrate-seat.sh`), the pre-RESULT gate (`result-precheck.sh`) and the numeric worker cap (`worker_cap: 4`, enforced by `herdr-agents --add-worker`, repeated by the texts). Task written 2026-10-17 by the orchestrator seat from the directive; seat: claude-standard-dot-a006 (worker-f; routing: no Claude permission-boundary file in allowed_files). Sequencing recorded in the task: before F3 (same rule bullets; F3 amended after this PR merges); the validator check of item 3 is a unit test because `scripts/validate-agent-assets.py` is in flight in #389 and T130.

- 2026-10-17T12:4xZ record created before the first dispatch (Orchestrator Playbook step 6). Dispositions, rounds, the sweep, the audit and the gate are appended below as they happen.

## PR #393 before its RESULT (2026-10-17T14:17Z): the two pins, the second Bot review

- a006's question (PONG 14:16:01Z): CI fails `test_word_budgets` (rule budget 450, the rule measures 488 after item 3's sentences) and `test_regime_rule_sections_are_pinned_whole` (the fixture `tests/fixtures/regime/worker-step-15.md` still carries the old step-15 sentence); option A adopted as amendment 3: both files join allowed_files, the budget becomes 490, the fixture follows item 3. The Bot's first review on PR open had three findings fixed in the one worker-side round ff9bb7c1 (4302868172, 4302868177, 4302868180); its re-review 5558148144 on 3baa0003 left P1 4302959624 (integrate-seat.sh:35, a retry reads the first run's kind=integration RESULT, which has no threads=, and refuses) and P2 4302959629 (precheck (g) reads inline comments only). Decision D-F4-round2: the P1 is fixed in the amendment's push as fix round 2 of INV-6 (one grep for threads= selecting the newest worker RESULT, one failing test), no round after it; the P2 is advisory under dotfiles-T129-integration-seat-result-gate-cap-followup-a01, written 2026-10-17T14:17Z before its row (C-51).
- finding classes: 4302868172, 4302868177, 4302868180 (the first review's three, fixed; classes read at the sweep from their bodies), 4302959624 result-selection, 4302959629 review-body-findings.

4302959624	result-selection

## Owned by dotfiles-T129-integration-seat-result-gate-cap-followup-a01 (advisory P2 of the re-review on 3baa0003; plan 020 step 1.2; rows id<TAB>class)

4302959629	review-body-findings
