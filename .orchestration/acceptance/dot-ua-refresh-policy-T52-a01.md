# Acceptance: dot-ua-refresh-policy-T52-a01

Dispatched 2026-10-02T01:05:35Z (msg 671) to `claude-standard-dot-a005`
(worker-c) after the operator's T51 decision (defer rebuilds, codify).
RESULT msg 672 (01:20:14Z), head f700b14, PR #223.

## Review (orchestrator, from git objects)

- One commit, four files: `.ua/config.json` (`autoUpdate: false`),
  `home/dot_config/claude/rules/understand-anything.md`,
  `home/dot_config/codex/AGENTS.md` (Japanese), `README.md`. SKILL and
  manifest untouched — verified: neither carries "incremental" wording, so
  the generator had nothing to render.
- Hook-flag check (task item 1) pasted: plugin 2.9.7 `hooks.json`
  SessionStart gates on `grep -q '"autoUpdate".*true' $UA_DIR/config.json`
  (origin/main config exit 0 = prompt fires; this branch exit 1 = silenced);
  `post-tool-use-auto-update.mjs` `autoUpdateEnabled()` returns
  `config.autoUpdate === true` and `main()` returns early. Both prompts stop.
- Wording verified in the diff: "Re-runs are incremental and cheap" removed;
  new bullet scoped to dotfiles (full rebuild only on operator request at a
  regime boundary; incremental blocked by `validate-incremental-symbols.mjs`
  on parser-less files, named; no per-path override; `herdr-agents` changes
  in nearly every task; T51 cited; stale by design with the grep fallback);
  acceptance-gate bullet keeps the `ua-symbol-coverage` table and adds
  `--old-ref` = previous `meta.gitCommitHash` for a full rebuild. Codex
  AGENTS.md says the same in Japanese with `$understand --full`; README
  paragraph added, commit/ignore guidance unchanged.
- 705 tests OK (1 skip); render-check, validate exit 0; CI green
  Linux+macOS; CLEAN. Codex audit of f700b14: **correct** (the auditor also
  confirmed `autoUpdate: false` disables both prompts).
- Sweep on f700b14 (14 items): all `not-applicable` (11 runner notices, 1
  Homebrew tap warning, CodeRabbit skipped comment and status); no Codex
  GitHub review posted by 01:25Z.
- Gate: `AGENT_REVIEWED=1 REVIEW_EVIDENCE=…-review-receipt.md BASE=origin/main
PR_FEEDBACK_EVIDENCE=…-pr-feedback.json make require-crit-review` in
  `.claude/worktrees/orchestrator-review` at f700b14 → exit 0.
- CompactionDB: worker decision 99f9a168 in the main DB; consolidated
  orchestrator decision added at acceptance.

**Decision: ACCEPTED** — squash-merge PR #223 without `--delete-branch`
(worker-c holds the branch). Effect: the per-commit UA update prompts stop
after the merge; the graph stays stale until the operator requests a full
rebuild.

cost: n/a (docs and config only; no subagents)
