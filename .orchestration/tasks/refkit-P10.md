# refkit-P10: レビュー・受入・統合（オーケストレータ側の手順書。ワーカーに委任しない項目を含む）

Covers plan tasks P10-01 … P10-06 (第 2 部 §12). Prerequisite: P9 accepted and merged on `feat/references-kit-v4`.

## Orchestrator-side (never delegated)
1. **P10-01 是正マトリクス** — worker task `refkit-P10-01` (docs only): `.orchestration/reports/remediation-matrix.md` with one row per 第 1 部 finding (A-01…G-21, 91 rows): finding → task → commit → evidence path → status (済／理由付き不採用). Source of truth: acceptance records under `.orchestration/acceptance/`. Orchestrator cross-checks every row against the acceptance files (no sampling).
2. **P10-02 独立再レビュー** — orchestrator forks (fresh context) reproduce the four-slice adversarial review on the merged tree: PRD/ADR/BDD; tools/evidence (re-run check/selftest/portability/run_examples from scratch); test docs + examples; packaging. Exit criterion: zero new P1/P2. Any new P1/P2 → new refkit task, loop.
3. **P10-03 セキュリティレビュー** — Codex worker on the `security` profile (`codex-security-dot`, own worktree) audits `references/tools/` (kit.toml path resolution, Chromium launch flags, subprocess use, selftest temp dirs) and the hook change from P0-06. Findings → refkit task if any.
4. **P10-04 require-crit-review** — `make require-crit-review` on the integration worktree; if review is required: `crit status --json`, `crit comments --all --json .agents/worklog/claude/crit/refkit-v4.json`, judge inside the session, add and resolve at least one review-scope approval record, write the receipt (`review_surface: crit-data`, `reviewer: claude-code`, `review_source`, `review_outcome`), then `AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review`.
5. **P10-05 受入記録・CompactionDB** — every `refkit-*` task has an acceptance record and a `memory add --kind decision --scope project` consolidation in the MAIN worktree DB (worker DBs are disposable); `.orchestration/**` committed with zero untracked tail; `memory list` shows one decision per accepted task.
6. **P10-06 統合と CI** — merge `feat/references-kit-v4-p3` into `feat/references-kit-v4` (orchestrator, when both worktrees are idle), verify `check` on the merged tree, push, open the English PR (Conventional Commits, `🤖 Generated with [Claude Code](https://claude.com/claude-code)` footer), wait for GitHub Actions (test.yaml, ubuntu.yaml, macos.yaml, agent-assets.yml, docs.yml) all green; fix→push→repeat via workers if red. bats never runs locally.
7. **Deployment note for the user** — the formatter-hook fix (P0-06) reaches `$HOME` only after `chezmoi apply`; the `remediation` profile likewise. State this explicitly in the final report.

## Teardown
`delivery.sh set off claude-code <each worker worktree>`, `leave.sh dotfiles claude-standard-dot-a00N` for each worker, `identities.sh` shows one line per remaining project, remove worker worktrees after merge (`git worktree remove`), keep `archive/` and `.orchestration/` committed.
