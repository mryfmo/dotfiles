---
{
  "audit_findings": [],
  "dispatch": [
    "AGMSG-TASK v1 task_id=dotfiles-T130-codex-local-review-exclusion-a01 round=1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md task_sha256=ad11722e9a8923d80a8f353927b310f60cf0ddeaf4f5917c6e8c02629dfdbfea deadline=none done_signal=AGMSG-RESULT note=queued,not-now:the-operator-s-20:59-JST-approval-item-(e),a-narrow-sandbox-exclusion-through-a-codex-local-review-wrapper;Claude-s-execution-boundary,so-your-seat;start-only-after-PR-392-merges(it-shares-its-files),before-F3;read-the-task-file-then read_at=unread",
    "AGMSG-TASK v1 task_id=dotfiles-T130-codex-local-review-exclusion-a01 round=1 amendment=1 previous_task_sha256=ad11722e9a8923d80a8f353927b310f60cf0ddeaf4f5917c6e8c02629dfdbfea repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md task_sha256=f137436dc56d91da3d6375ebe9b71d49e37e7b6d0d84919991c9bdafcd67edd6 deadline=none note=the-monitor-s-23:45-JST-correction:do-not-wait-for-392-s-merge;start-now-from-PR-392-s-head-85547ca5(a-stacked-branch),rebase-onto-origin/main-after-392-merges,no-PR-before-the-rebase;read-Amendment-1;copy-the-amended-text-as-task.md read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T130-codex-local-review-exclusion-a01 round=1 amendment=2 previous_task_sha256=f137436dc56d91da3d6375ebe9b71d49e37e7b6d0d84919991c9bdafcd67edd6 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md task_sha256=1e4671ba1da997135e3430a403d69508e2305f1a1c6f6e7addbab4cd1195d9f1 deadline=none note=answer-to-your-14:57Z-blocked-PONG,authorized:tests/unit/test_claude_settings_merge.py-joins-allowed_files-with-its-row;the-one-common-expected-list-becomes-agmsg-dispatch-plus-codex-local-review,every-other-assertion-kept;fix-the-two-Ruff-lints-in-the-same-push;read-Amendment-2;copy-the-amended-text-as-task.md;continue read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T130-codex-local-review-exclusion-a01 round=1 amendment=3 previous_task_sha256=1e4671ba1da997135e3430a403d69508e2305f1a1c6f6e7addbab4cd1195d9f1 repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md task_sha256=aafd30b243bbbde318dd730d35e173100b86176facf88dde48812f0432b10a8a deadline=none note=the-Bot-s-review-of-boundary-PR-397-on-this-task-text(P1-4303199830,P2-4303199832),both-adopted:the-wrapper-runs-only-from-the-primary-checkout(git-common-dir-is-its-own-.git)with-local-review.sh-tracked-and-unchanged-against-HEAD,and-requires-a-full-40-hex-head;the-wrapper-test-covers-each-refusal;apply-on-your-stacked-branch-now,before-the-rebase;read-Amendment-3;copy-the-amended-text-as-task.md read_at=read",
    "AGMSG-TASK v1 task_id=dotfiles-T130-codex-local-review-exclusion-a01 round=1 amendment=4 previous_task_sha256=aafd30b243bbbde318dd730d35e173100b86176facf88dde48812f0432b10a8a repo=~/Workspace/dotfiles/.claude/worktrees/worker-e task_file=.orchestration/tasks/dotfiles-T130-codex-local-review-exclusion-a01.md task_sha256=8d9dae7861735852eef7a035bb1aac5c3e069412431310fba90ee08d82eb5ece deadline=none note=answer-to-your-16:34Z-operator-decision-PONG(D-399-round2,the-orchestrator-by-default-under-the-night-s-directives):the-surviving-P1-4303494614-is-fixed-by-a-re-plan-of-the-anchor-as-fix-round-2-of-INV-6:the-deployed-wrapper-carries-EXPECTED_SHA256-rendered-by-scripts/generate-agent-configs.py-from-the-tracked-local-review.sh(render-check-keeps-them-equal;make-update-deploys-both;fail-closed-until-then),the-HEAD-blob-and-git-diff-checks-leave;the-generator-joins-allowed_files;one-push,the-two-tests-red-then-green,@codex-review-once,CI,RESULT;no-third-round;read-Amendment-4;copy-the-amended-text-as-task.md read_at=unread"
  ],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": null,
  "searches": [],
  "task": "dotfiles-T130-codex-local-review-exclusion-a01"
}
---
# Acceptance record: dotfiles-T130-codex-local-review-exclusion-a01

A narrow sandbox exclusion (codex-local-review wrapper) for the orchestrator's local review (the operator's 20:59 JST approval, item e); Claude's execution boundary, so a Codex seat: codex-standard-dot-a004 (worker-e), queued after PR #392.

- 2026-10-17T13:46Z record created before the first dispatch (Orchestrator Playbook step 6). Dispositions, rounds, the sweep, the audit and the gate are appended below as they happen.

## PR #399 before its RESULT (2026-10-17T16:36Z): the second Bot review's surviving P1

- a004's PONGs 16:25Z and 16:34Z: head 22e15c0c on a8a747af; the first review's P1 4303419130 (the wrapper's `git diff` could run a repository-configured core.fsmonitor helper; a004's own review added the promisor helper) fixed:22e15c0c in the sole worker-side round; the second review 5558794743 leaves P1 4303494614: the primary checkout's `.git` is sandbox-writable, so a committed replacement of local-review.sh with HEAD moved to it passes Amendment 3's HEAD-blob and `git diff` checks, and the row's test never moves a ref. The finding is right: HEAD, every local ref and the index are inside the sandbox's `.` allowWrite; no local ref is an anchor.
re-plan: mutable-trust-anchor -> specification: the excluded command execs only a script whose content matches an anchor that sandboxed code cannot write; design: the anchor is the deployed wrapper itself (chezmoi writes `~/.local/bin/common/` at `make update`, outside the sandbox's write set), which carries `EXPECTED_SHA256` rendered by the generator from the tracked script, render-check keeping them equal and the wrapper refusing a mismatch (fail-closed until the next `make update`); implementation: amendment 4 and one revise round on PR #399 (fix round 2 of INV-6, D-399-round2); verification: a fixture that commits a modified script and moves HEAD to it is refused, the matching script accepted, and render-check fails on a stale hash line. Written 2026-10-17T16:36Z by the orchestrator (default under the night's directives; the operator may stop the round and hold the PR instead).
- finding classes: 4303419130 helper-execution-in-git (fixed), 4303494614 mutable-trust-anchor (the row below; fixed in round 2 or the PR stops).
- 2026-10-17T16:36Z acceptance action: TASK amendment 4 to a004 (the line in the dispatch list of the block above); no ACCEPTANCE yet (no RESULT).

4303419130	helper-execution-in-git
4303494614	mutable-trust-anchor
