#!/usr/bin/env bash
# orch-gate.sh <task id> <full head sha> <pr>: run the integration gate from the review worktree at the head with the task's evidence copied in.
set -euo pipefail
T="$1"; HEAD="$2"; PR="$3"; S7="${HEAD:0:7}"
MAIN=~/Workspace/dotfiles; R="$MAIN/.claude/worktrees/orchestrator-review"
cd "$MAIN"
[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
git -C "$R" checkout -q --detach "$HEAD"
mkdir -p "$R/.orchestration/validation" "$R/.orchestration/acceptance"
for f in ".orchestration/validation/$T-pr-feedback.json" ".orchestration/validation/$T-audit-$S7.md" ".orchestration/validation/$T-audit-$S7.md.last.md" ".orchestration/validation/$T-review-receipt.md" ".orchestration/validation/$T-crit.json" ".orchestration/acceptance/$T.md"; do cp "$f" "$R/$f"; done
set +e
( cd "$R" && AUDIT_EVIDENCE=".orchestration/validation/$T-audit-$S7.md" AUDIT_DISPOSITIONS=".orchestration/acceptance/$T.md" AGENT_REVIEWED=1 REVIEW_EVIDENCE=".orchestration/validation/$T-review-receipt.md" BASE=origin/main PR_FEEDBACK_EVIDENCE=".orchestration/validation/$T-pr-feedback.json" make require-crit-review ) 2>&1 | tail -15
rc=${PIPESTATUS[0]}
git -C "$R" checkout -q -- . 2>/dev/null; git -C "$R" clean -fdq .orchestration; git -C "$R" checkout -q --detach origin/main
echo "gate rc=$rc"; exit $rc
