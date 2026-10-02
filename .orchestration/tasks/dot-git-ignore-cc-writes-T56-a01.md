# AGMSG-TASK dot-git-ignore-cc-writes-T56-a01

Drafted 2026-10-02 by the orchestrator seat (`claude-remediation-dot`); operator-approved dispatch. Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.

## Objective

`make update` is blocked on both machines (DGX Spark and the MacBook Pro): `chezmoi status` reports `MM .config/git/ignore` because the live `~/.config/git/ignore` carries the line `**/.claude/.cc-writes/` (added by Claude Code) and the source does not, so `chezmoi apply` prompts `(diff/overwrite/all-overwrite/skip/quit)?` and fails with EOF without a TTY. Add that one line to the source so the target converges without a prompt.

Change exactly one file: `home/dot_config/git/ignore`. Add the line `**/.claude/.cc-writes/` directly below the existing `**/.claude/settings.local.json` line (line 7). Nothing else: no reordering, no removal of other patterns, no template conversion.

[memory:decision] T56 (operator 2026-10-02): the global git ignore source carries `**/.claude/.cc-writes/` so that `chezmoi apply` never prompts on the Claude Code write-cache marker; both machines converge from the same line.

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c chore/git-ignore-cc-writes origin/main` (1f3bb5e1 or later). Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `home/dot_config/git/ignore`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-git-ignore-cc-writes-T56-a01.md` (main checkout)

## Forbidden actions

- Any other file; merging; force push; local bats; `make apply`/`chezmoi apply`; pushing `main`; LLM calls beyond your own session.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
git diff origin/main -- home/dot_config/git/ignore
grep -n 'cc-writes' home/dot_config/git/ignore
chezmoi execute-template < /dev/null >/dev/null 2>&1; echo "no template: $?"   # the file is not a template; this line is informational only
make render-check
make validate-agent-assets
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number and head SHA.
3. CompactionDB from the main checkout: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"`; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (run outside the sandbox; the excludedCommands entry does not take effect in this environment). `cost:` line in the report. max_turns=15.

## Decision on the PONG (orchestrator, 2026-10-02 14:50Z)

Verified: the live `~/.config/git/ignore` has `**/.claude/.cc-writes/` appended at EOF after one blank line (Claude Code's own write). Option (a): append the line at EOF after a blank line so the source is byte-identical to the live file and `chezmoi status` is empty on both machines. The "below line 7" placement in the Objective is withdrawn. Everything else in this task is unchanged.
