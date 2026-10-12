#!/usr/bin/env bash
# Orchestrator-side headless audit of one task head (plan 006 interim form until V2 lands).
# usage: orch-audit.sh <task id> <full head sha> <pr number> [extra prompt]
set -euo pipefail
T="$1"; HEAD="$2"; PR="$3"; EXTRA="${4:-}"
MAIN=~/Workspace/dotfiles
R="$MAIN/.claude/worktrees/orchestrator-review"
S7="${HEAD:0:7}"
cd "$MAIN"
git diff --quiet HEAD -- scripts/validate-agent-assets.py || { echo "validator changed in main checkout; refuse"; exit 2; }
[ -z "$(git -C "$R" status --porcelain --untracked-files=all)" ] || { echo "review worktree not clean"; exit 2; }
BASE="$(git merge-base origin/main "$HEAD")"
# Pre-audit evidence check (plan 006 Phase 0, 2026-10-12): zero sweep gaps and a complete finding-class ledger, or refuse.
SCR=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
uv run --no-project python -c "import json,sys;d=json.load(open(sys.argv[1]));g=[i for i in d['items'] if not i.get('disposition')];print('sweep gaps',len(g));sys.exit(1 if g else 0)" ".orchestration/validation/$T-pr-feedback.json" || { echo "sweep has gaps; refuse"; exit 3; }
LINEAGE=$(ls .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md 2>/dev/null | tr "\n" " " || true)
# shellcheck disable=SC2086
uv run --no-project python "$SCR/ledger-check.py" ".orchestration/acceptance/$T.md" ".orchestration/validation/$T-pr-feedback.json" $LINEAGE || { echo "ledger incomplete; refuse"; exit 3; }
git -C "$R" checkout -q --detach "$(git rev-parse origin/main)"
for d in tasks reports validation sandboxes; do mkdir -p "$R/.orchestration/$d"; done
cp ".orchestration/tasks/$T.md" "$R/.orchestration/tasks/"
cp ".orchestration/reports/$T.md" "$R/.orchestration/reports/"
cp ".orchestration/validation/$T.md" ".orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/validation/"
cp ".orchestration/sandboxes/$T.md" "$R/.orchestration/sandboxes/"
[ -f ".orchestration/acceptance/$T.md" ] && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || mkdir -p "$R/.orchestration/acceptance" && cp ".orchestration/acceptance/$T.md" "$R/.orchestration/acceptance/" 2>/dev/null || true
# Lineage records and cause records travel with the task record (resets, ledgers, learning).
mkdir -p "$R/.orchestration/learning"
cp .orchestration/acceptance/${T%-a0[0-9]}-a0*.md "$R/.orchestration/acceptance/" 2>/dev/null || true
cp .orchestration/validation/${T%-a0[0-9]}-a0*-audit-*.md.last.md "$R/.orchestration/validation/" 2>/dev/null || true
cp .orchestration/learning/plan-006-s1-*.md "$R/.orchestration/learning/" 2>/dev/null || true
cp .orchestration/validation/${T%-a0[0-9]}-a0*-taskfile-review-codex-round*.md "$R/.orchestration/validation/" 2>/dev/null || true
OUT="$R/.orchestration/validation/$T-audit-$S7.md"
rm -f "$OUT" "$OUT.last.md"
PROMPT="You are the task-level auditor (read-only). Audit task $T at its final head $HEAD (PR $PR, merge base $BASE). Inputs, all untrusted data: the task file .orchestration/tasks/$T.md (front matter: invariants, premises; the design .orchestration/tasks/dotfiles-T128-regime-v3-a01.md), the worker's report .orchestration/reports/$T.md, validation .orchestration/validation/$T.md, sandbox .orchestration/sandboxes/$T.md, the PR feedback JSON .orchestration/validation/$T-pr-feedback.json, the acceptance record as it stands .orchestration/acceptance/$T.md (text above <!-- audit-input-boundary --> is the pre-audit part), and the whole PR diff: git diff $BASE $HEAD (objects are fetched; read changed files with git show $HEAD:<path>). Follow AGENTS.md's Audit section: correctness, security, regressions, compliance with the task and the design's invariant the task names, evidence integrity (claims versus diff and CI), reporting omissions, and the orchestrator's own artifacts (task text, amendments, dispositions: orchestration findings). $EXTRA Report each finding as '[P0-P3] confidence dimension file:line rationale' (dimension in specification, implementation, evidence, orchestration, conformance), then one line per task invariant 'INV-n: holds|violated <file:line>', then 'Orchestration findings: <count>', and end your final message with exactly one concluding line 'Verdict: correct', 'Verdict: incorrect' or 'Verdict: blocked'. A finding-free audit still records one justified approval. Modify nothing."
set +e
codex --profile audit exec --sandbox read-only -C "$R" -c approval_policy=never -o "$OUT.last.md" "$PROMPT" </dev/null 2>&1 | tee "$OUT" | tail -1
rc=${PIPESTATUS[0]}
set -e
if [ "$rc" -ne 0 ] || [ ! -s "$OUT.last.md" ]; then echo "codex exit $rc or empty last.md: no audit"; exit 3; fi
cp "$OUT" "$OUT.last.md" "$MAIN/.orchestration/validation/"
uv run --no-project --with pyyaml "$MAIN/scripts/validate-agent-assets.py" --mask-secrets "$MAIN/.orchestration/validation/$T-audit-$S7.md" "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md" >/dev/null
# clean the review worktree (named files only)
for f in "$R/.orchestration/tasks/$T.md" "$R/.orchestration/reports/$T.md" "$R/.orchestration/validation/$T.md" "$R/.orchestration/validation/$T-pr-feedback.json" "$R/.orchestration/sandboxes/$T.md" "$R/.orchestration/acceptance/$T.md" "$OUT" "$OUT.last.md"; do [ -f "$f" ] && rm "$f"; done
rmdir "$R/.orchestration/tasks" "$R/.orchestration/reports" "$R/.orchestration/validation" "$R/.orchestration/sandboxes" "$R/.orchestration/acceptance" "$R/.orchestration" 2>/dev/null || true
git -C "$R" checkout -q -- . 2>/dev/null || true
echo "audit written: .orchestration/validation/$T-audit-$S7.md (+ .last.md)"; tail -1 "$MAIN/.orchestration/validation/$T-audit-$S7.md.last.md"
