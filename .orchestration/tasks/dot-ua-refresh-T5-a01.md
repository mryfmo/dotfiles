# AGMSG-TASK dot-ua-refresh-T5-a01 — refresh the Understand-Anything knowledge graph after today's merges

`.ua/meta.json` `gitCommitHash` is stale (baseline 13079e4; main has since taken #170-#173 and 74 upstream commits). Run the incremental update exactly as the plugin's hook prescribes and commit only `.ua/` output.

## Steps

1. Work on a fresh worktree `.claude/worktrees/ua-refresh` (branch `chore/ua-refresh`) from `origin/main` AFTER PR #172 and PR #173 are merged (orchestrator will tell you in the TASK note if they are).
2. Follow `/Users/mryfmo/.claude/plugins/cache/understand-anything/understand-anything/2.9.7/hooks/auto-update-prompt.md` verbatim: prepare-incremental → plan action → (file-analyzer batches only if PARTIAL/ARCHITECTURE) → merge → finalize. If the plan says FULL_UPDATE, STOP and report (do not run `/understand --full`; that is a separate operator decision).
3. Do not hand-edit graph JSON. Do not touch `.ua/intermediate/` or `.ua/diff-overlay.json` in the commit scope (gitignored).
4. Validation: paste the plan action, files reanalyzed counts, `incremental-symbol-report.json` summary, and `git status --short .ua`.

## allowed_files

`.ua/**` (via the plugin scripts only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-refresh-T5-a01.md`.

## forbidden_actions

no git commit; no push; no PR; no source edits; no `/understand --full`.

max_turns=20. Reply with `AGMSG-RESULT v1`.
