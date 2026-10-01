# Sandbox: dot-plain-start-visibility-T45-a01

- worker: claude-standard-dot-a005 (claude-code, standard profile), herdr pane `wP:p2`
- isolation: dedicated git worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`,
  branch `fix/plain-start-visibility` created from `origin/main` (`fa5ce03`); the previous
  branch `fix/sandbox-unix-sockets` (`c2c1f62`, PR #215) was left intact (switch, no reset).
- Bash ran inside the Claude Code sandbox (bubblewrap) by default. Unsandboxed calls, each
  for a stated sandbox limit: `git fetch`/`git switch` (writes shared `.git`), the
  socket-bind unit test (the sandbox forbids `socket(AF_UNIX)`), `git push`, and `gh`
  (keyring D-Bus socket).
- No Herdr pane was read. No pane, workspace, or agent was created; every Herdr/spawn
  interaction in tests uses the fake CLIs in `tests/unit/test_herdr_agents.py`.

## T39 follow-up evidence: sandbox deny-mount stubs

The orchestrator ruled these are Claude-sandbox deny-mount artefacts, not task dirt (PING
2026-09-29T23:27:04Z). They were never added or removed; `git add` used explicit paths only.
All were created at 2026-09-30 08:21:59 JST, the instant of this session's first sandboxed
Bash call. `stat -c '%n mode=%A size=%s ctime=%z'` output, verbatim:

```text
.bash_profile mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.569886540 +0900
.bashrc mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.569567823 +0900
.claude/agents mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.565429882 +0900
.claude/commands mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.564977393 +0900
.claude/launch.json mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.562974429 +0900
.claude/loop.md mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.564754637 +0900
.claude/output-styles mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.564318374 +0900
.claude/routines mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.564103811 +0900
.claude/skills mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.561974339 +0900
.claude/workflows mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.562974429 +0900
.gitconfig mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.567974879 +0900
.gitmodules mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.567974879 +0900
.idea mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.571468042 +0900
.mcp.json mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.564977393 +0900
.profile mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.570669827 +0900
.ripgreprc mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.570940587 +0900
.vscode mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.571205507 +0900
.zprofile mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.570411003 +0900
.zshrc mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.570152836 +0900
/home/moriya/Workspace/dotfiles/.git/config.lock mode=-r--r--r-- size=0 ctime=2026-09-30 08:21:59.565658943 +0900
```

The same instant also produced the zero-byte `.git/config.lock` in the shared `.git` (last
line above). It made `git switch -c` fail to write upstream config
(`error: could not lock config file /home/moriya/Workspace/dotfiles/.git/config: ファイルが存在します` (EEXIST));
the branch was still created at `origin/main`, and the task avoided every further config
write (`--no-track`, push without `-u`). The lock was not removed, as the task requires.

## Resume (2026-10-01)

- worker-c switched from `fix/orchestrator-delivery-sandbox` (T49, merged as 8da41c8) back to `fix/plain-start-visibility` (89e95e4, matching origin). d6b8832 merges origin/main and 0a35010 is the fix; pushed without `-u`.
- Unsandboxed for the stated limits: the make targets (uv cache; AF_UNIX test), the socket tests (AF_UNIX bind), the generator `--check` (PyPI or uv cache), `git push`, `gh`, the main-checkout CompactionDB entry, and these artifact writes. The `--attach` probe ran sandboxed. It read only agmsg identity and placement records and made no herdr call that changes anything.
- The worker-c copy of this sandbox record was left in place, as the orchestrator asked; this main-checkout file extends it.

## Resume round 2

- 51f8bc7 sits on 9eb3e43, pushed without `-u`; the same unsandboxed classes. The socket test's short HOME is a symlink under a /tmp/ha-* directory removed by addCleanup. The negative check swapped in the 9eb3e43 launcher and restored it (`cmp` exit 0).
