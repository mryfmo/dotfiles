# Sandbox: dot-orchestrator-pane-profile-args-T47-a01

- worker: claude-standard-dot-a005 (claude-code, standard profile), worktree-seated pane in
  `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- isolation: dedicated git worktree `worker-c`, branch `fix/orchestrator-pane-profile-args`
  created with `git switch --no-track -c … origin/main` (`fa5ce03`) **inside** the sandbox (no
  config write, so the T39 `.git/config.lock` stub was not hit). `fix/plain-start-visibility`
  (T45, PR #216, head 89e95e4) was left intact; the untracked
  `.orchestration/sandboxes/dot-plain-start-visibility-T45-a01.md` was not touched.
- Bash ran inside the Claude Code sandbox (bubblewrap) by default. Unsandboxed calls, each for a
  stated sandbox limit (same classes as the T45 record):
  - `make unit-test`: the socket-bind unit test (sandbox forbids `socket(AF_UNIX)`) and the default uv cache;
  - `make validate-agent-assets`: sandboxed attempts failed because `uv run --with pyyaml` could
    not reach `files.pythonhosted.org` (sandbox network deny) with a sandbox-writable scratch
    cache; the unsandboxed run used the already-warm default uv cache;
  - `git push origin fix/orchestrator-pane-profile-args` (no `-u`);
  - `gh pr create` / `gh pr checks` / `gh pr view` (keyring D-Bus socket).
- No escalation beyond the task-sanctioned classes; no Herdr pane read, created, or driven: all
  Herdr interaction in tests uses the fake CLIs in `tests/unit/test_herdr_agents.py`.
- The zero-byte deny-mount stubs (`.bashrc`, `.mcp.json`, `.claude/launch.json`, …) were never
  added; `git add` used explicit paths only. `.git/*.lock` was not removed.
- A PostToolUse formatter hook reformatted the whole test file after the Edit (783-line diff);
  the commit was amended to origin/main's file plus only the 43 added lines.
