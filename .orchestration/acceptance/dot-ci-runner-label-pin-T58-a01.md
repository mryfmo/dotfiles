# Acceptance: dot-ci-runner-label-pin-T58-a01

status: accepted
pr: #229 (squash-merged to main as 750cc4a9; branch chore/ci-runner-label-pin left in place because the worker worktree holds it)
reviewed_head: 88f797360b3d7b590e5e5d1e56f9c0b1b842d88e
worker: claude-standard-dot-a005 (worker-c)

## Review

- Worker raised three scope questions as a blocked PONG before editing (an uncovered label assertion in tests/unit/test_supply_chain_policy.py, exact-label shell checks that would block the canary, the annotation-text fixture). The orchestrator answered all three (add the test file with a one-line change; match the ubuntu-* family in shell checks; keep the fixture). The missed test file was an orchestrator grounding gap.
- Diff (9 files, +30/-23): every ubuntu-latest runner label is explicit ubuntu-24.04; shell OS checks match ubuntu-*; Codecov pinned to ubuntu-24.04; non-required ubuntu-26.04 client canary via matrix include with continue-on-error keyed on matrix.os; README ruleset payload and test fixtures carry the renamed contexts.
- Orchestrator verified: no ubuntu-latest remains except the GitHub annotation text fixture; CI contexts report as test (ubuntu-24.04, ...) and public-bootstrap (ubuntu-24.04, ...), all required green; the ubuntu-latest migration notices are gone (3 remaining notices are macOS arm64 capacity); the canary fails on scripts/check-statusline-tools.py (ccstatusline --version timeout under sudo unshare --net on the ubuntu-26.04 image) while the workflow run concludes success. Worker: 718 unit tests OK.
- Audit: Verdict: correct, no findings. Codex code review (Bot): no review posted.

## PR feedback dispositions (head 88f79736, 7 items)

- 1 check_run failure + 1 annotation failure (canary test (ubuntu-26.04, client)): not-applicable with the concrete reason (non-required continue-on-error cell added on purpose; first Ubuntu 26.04 finding, tracked for a follow-up task before the label moves)
- 3 annotation:notice (macOS arm64 capacity): not-applicable
- 1 CodeRabbit comment + 1 status: not-applicable (review disabled by operator decision)

## Gate

BASE=origin/main PR_FEEDBACK_EVIDENCE=... AGENT_REVIEWED=1 REVIEW_EVIDENCE=... make require-crit-review -> exit 0 at 88f79736 in .claude/worktrees/orchestrator-review.

## Follow-ups

- No live ruleset exists yet, so nothing to re-apply now; when the operator applies the README payload it already carries the new context names.
- The canary will stay red on every PR until the ccstatusline hang on Ubuntu 26.04 is fixed; a root-cause task (proposed T59) awaits operator approval so that failure is not dispositioned repeatedly.

## Learning candidates (worker, not promoted)

A canary needs label-agnostic branches; grounding greps for workflow-text changes must include tests that assert workflow strings; first Ubuntu 26.04 data point recorded.

cost: n/a (worker: no subagents reported; orchestrator session totals not exposed)
