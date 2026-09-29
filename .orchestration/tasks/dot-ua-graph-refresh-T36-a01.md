# AGMSG-TASK dot-ua-graph-refresh-T36-a01 (incremental follow-up to T33c)

## Objective

Bring the Understand-Anything knowledge graph in `.ua/` up to date with
`origin/main` (stale since the T33c rebuild at 935e198: T33a–T35 changed herdr-agents, update-agent-assets.sh, validate-agent-assets.py, check-agent-runtime.py, permgate, rules and tests; the plugin core is now built by `make update`, so the incremental path should work).

- Read and execute the plugin's incremental procedure at
  `/home/moriya/.claude/plugins/cache/understand-anything/understand-anything/2.9.7/hooks/auto-update-prompt.md`
  (incremental update only; do not run a full `/understand` from scratch
  unless the procedure itself falls back to it — if it does, stop and PONG
  with the reason and the estimated size first).
- Commit `.ua/` except `.ua/intermediate/` and `.ua/diff-overlay.json`; ensure
  those two paths are in `.gitignore` (add them if missing).
- Confirm afterwards that `.ua/meta.json` `gitCommitHash` equals your branch
  HEAD's parent on origin/main or that `git diff --name-only <hash>..HEAD`
  lists only `.ua/` and `.orchestration/` paths.

[memory:decision] T36: the `.ua/` knowledge graph is refreshed incrementally
by a worker task whenever the SessionStart hook reports it stale; the
orchestrator never runs the graph update in its own session (operator
2026-09-28).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c chore/ua-graph-refresh-T36 origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `.ua/**` (except the two ignored paths)
- `.gitignore` (only the two `.ua/` ignore lines)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-graph-refresh-T36-a01.md` (main checkout)

## Forbidden actions

- Any source, script, rule, test, or manifest change; merging; force push;
  local bats; `make apply`/`chezmoi apply`; writes outside the worktree except
  the listed `.orchestration` paths; LLM calls other than those the plugin
  procedure itself performs inside your session.

## Validation commands (paste verbatim output)

```
jq -r .gitCommitHash .ua/meta.json
git rev-parse HEAD
git diff --name-only $(jq -r .gitCommitHash .ua/meta.json)..HEAD | head
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat | tail -3
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs and
   the PR number/head SHA; report the node/edge counts before and after.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
