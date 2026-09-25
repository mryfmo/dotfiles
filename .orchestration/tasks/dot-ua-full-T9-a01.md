# AGMSG-TASK dot-ua-full-T9-a01 — full Understand-Anything rebuild (authorized)

T5 established that `.ua/meta.json` was re-pinned by hand past the graph's real base (d91b835) and that an incremental update selects FULL_UPDATE (743 structurally changed files). This task authorizes the full rebuild. Run it in the worker (never in the interactive Claude session).

## Steps

1. New worktree `.claude/worktrees/ua-full` (branch `chore/ua-full-rebuild`) from `origin/main`.
2. Run the plugin's full analysis exactly as its skill prescribes (`$understand --full` in Codex, i.e. the `understand` skill's full mode under `~/.understand-anything-plugin`). Do not hand-edit any JSON. Let it write `.ua/knowledge-graph.json`, `.ua/fingerprints.json`, `.ua/meta.json`, layers/tour as the skill defines.
3. Confirm `.ua/meta.json` `gitCommitHash` equals `git rev-parse HEAD` of the worktree, and that `.ua/intermediate/` and `.ua/diff-overlay.json` stay gitignored (not staged).
4. Validation (verbatim): node/edge counts before vs after; the skill's own validation output (graph-reviewer if the skill runs it); `git status --short .ua`; `git diff --stat -- .ua`.
5. Stage `.ua/` (no commit) and RESULT. Include the token/cost figures the runtime exposes in the `cost:` line.

## allowed_files

`.ua/**` (plugin output only), `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-full-T9-a01.md`.

## forbidden_actions

no source edits; no hand-edited graph JSON; no git commit/push/PR; no local bats.

max_turns=40. Reply with `AGMSG-RESULT v1`.
