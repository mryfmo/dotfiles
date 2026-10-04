# AGMSG-TASK dotfiles-T95-sandbox-placeholder-files-on-disk-a01

Drafted 2026-10-04 by the orchestrator seat; follow-up to T92. Queued for the next free seat (any kind: `.gitignore` and a header note, no boundary source).

## Objective

T92 made the stop gate ignore the Claude Code sandbox's bind-mount placeholders as seen from inside the sandbox. A second form exists: the sandbox leaves the mount targets behind on the host as real 0-byte, mode 0444 files at the protected paths (observed 2026-10-04 in the main checkout at 09:15Z and in `.claude/worktrees/worker-e`: `.bash_profile`, `.bashrc`, `.claude/agents`, `.claude/commands`, `.claude/launch.json`, `.claude/loop.md`, `.claude/output-styles`, `.claude/routines`, `.claude/skills`, `.claude/workflows`, `.gitconfig`, `.gitmodules`, `.idea`, `.mcp.json`, `.profile`, `.ripgreprc`, `.vscode`, `.zprofile`, `.zshrc`). Outside the sandbox they are ordinary untracked files, so `git status` lists them and the gate blocks; the orchestrator removed them and excluded the 19 paths in `.git/info/exclude` as a local stopgap.

1. `.gitignore` (repository root): ignore exactly these 19 paths with a comment naming the cause (Claude Code sandbox placeholder targets persisted on the host) so every clone behaves the same; keep them ignored only at the repository root (leading `/`) and never ignore `.claude/settings.json` or `.claude/settings.local.json`.
2. `scripts/agent-stop-gate.sh` header: one sentence that host-persisted placeholders are handled by `.gitignore`, not by the mount check.
3. `tests/unit/test_agent_stop_gate.py` or a small new test: `git check-ignore` of each listed path from the repository root returns 0, and `git check-ignore .claude/settings.json` returns 1.
4. Report whether the placeholders reappear on disk after a sandboxed command in your worktree (`ls -la .zshrc` before and after), so the cause is documented.

Forbidden: `.claude/settings.json`; the gate's mount logic; `.git/info/exclude` (local, not tracked).

[memory:decision] dotfiles-T95 (orchestrator 2026-10-04): the Claude Code sandbox's placeholder targets that persist on disk at the repository root are ignored through `.gitignore`, so neither `git status` nor the stop gate reports them.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/sandbox-placeholder-ignores origin/main` (f2b5c115 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `.gitignore`, `scripts/agent-stop-gate.sh` (header sentence only), `tests/unit/test_agent_stop_gate.py` or `tests/unit/test_gitignore_sandbox_placeholders.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T95-sandbox-placeholder-files-on-disk-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
for p in .bash_profile .bashrc .claude/agents .claude/commands .claude/launch.json .claude/loop.md .claude/output-styles .claude/routines .claude/skills .claude/workflows .gitconfig .gitmodules .idea .mcp.json .profile .ripgreprc .vscode .zprofile .zshrc; do git check-ignore -q "$p" && echo "ignored $p" || echo "NOT ignored $p"; done
git check-ignore .claude/settings.json ; echo "rc=$?"
make unit-test
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if a Crit plan review ran.
3. Artifacts at the exact expected paths; validation with verbatim commands and raw output, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T95` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=20.

## Dispatch

- 2026-10-04 13:30Z to `claude-standard-dot-a005` (worker-c, wT:p2) after its T93 RESULT (PR #251 pending acceptance; keep `fix/gate-masked-feedback-bodies` untouched). Branch from `origin/main` f2b5c115 or later. Disjoint from T93 (gate/validator), T88 (SKILL/rule) and T62 (manifest claude block).
