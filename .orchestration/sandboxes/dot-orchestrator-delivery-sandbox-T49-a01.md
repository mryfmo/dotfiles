# Sandbox: dot-orchestrator-delivery-sandbox-T49-a01

- worker: claude-standard-dot-a005, worktree `~/Workspace/dotfiles/.claude/worktrees/worker-c`, branch
  `fix/orchestrator-delivery-sandbox` from origin/main 9b60b4b (`git switch --no-track -c`, sandboxed).
- The herdr probes ran unsandboxed, because the herdr socket is a Unix socket and the sandbox blocks it on Linux, which is
  T44 r2's status quo. They read only the worker's own pane (`wN:p2`): `herdr agent list` (agent metadata),
  `herdr pane process-info --pane wN:p2`, and the `--help` texts. No `pane read`/`agent read`, and no other pane was inspected.
- Also unsandboxed: the make targets (uv cache; socket test), `git push` (no `-u`), `gh`, the
  main-checkout CompactionDB entry, and these artifact writes.
- Never read, claimed or touched: `run/actas.dotfiles__claude-remediation-dot.session`. Only the lock file
  names were listed. Nothing under `~/.agents/skills/agmsg/` was edited.
- Every test fake (herdr, identities.sh, actas-claim.sh, /proc, agmsg dir) lives in a temporary directory.

## Revision 2

- 50ebfdc sits on 4452516, pushed without `-u`. Unsandboxed for the stated limits: the generator write and make targets (uv cache; socket test), `git push`, `gh`, the WebFetch of the Claude Code docs (WebFetch tool), and the main-checkout CompactionDB entry and artifact appends.
- The negative check swapped in the r1 launcher and template and restored both (`cmp` exit 0).
- No live lock read and no live claim. All fakes (actas-claim.sh, lib/actas-lock.sh, herdr) live in the test temporary directory.
- r2-b/r2-c: 68ac54d, 99d734b and 1fa2a48, each pushed without `-u`; the same unsandboxed classes. The r2-c negative check swapped in the 99d734b launcher and restored it (`cmp` exit 0).

## Revisions 2-d, 2-e, 2-f

- e4903a1, 63d4e03 and 9dc4e53 sit on 1fa2a48, each pushed without `-u`; the same unsandboxed classes. Each negative check swapped in the previous launcher and restored it (`cmp` exit 0). The live-pid test uses the test process's own pid, and the dead-pid test a reaped child.

## Revisions 3 and 3-b

- 9b658a9 and 229896a sit on 9dc4e53, each pushed without `-u`; the same unsandboxed classes, plus one WebFetch of code.claude.com/docs/en/permissions to verify the quoted sentence. Each negative check swapped in the previous launcher and restored it (`cmp` exit 0).

## Revision 3-c

- 11d87f3 and 00268f1 sit on 229896a, pushed without `-u`; the same unsandboxed classes. The live-claude stand-in is a copy of `sleep` named `claude` in the test temporary directory, killed by addCleanup.
