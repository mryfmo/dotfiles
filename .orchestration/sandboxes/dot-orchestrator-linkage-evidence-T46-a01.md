# Sandbox: dot-orchestrator-linkage-evidence-T46-a01

- worker: claude-standard-dot-a005, worktree `~/Workspace/dotfiles/.claude/worktrees/worker-c`, branch
  `fix/orchestrator-linkage-evidence` from origin/main 119fdc3 (`git switch --no-track -c`, sandboxed).
- Unsandboxed, each for a stated limit:
  - the make targets (uv cache; AF_UNIX test);
  - `make check-regime-boundary` (herdr socket, pgrep, agmsg run directory);
  - the `git worktree` commands, plus the commit and pushes in env-converge-T10 (the shared `.git` and the main checkout's worktrees);
  - `git push` and `gh` (keyring);
  - `kill` on the two crit servers;
  - the main-checkout CompactionDB entry and these artifact writes.
- Destructive steps, each preceded by a look:
  - worker-b: removed only after `cmp` proved its untracked files were on main;
  - env-converge-T10: removed only after its dirty change was committed (0c12c6a) and pushed to a new branch;
  - the crit servers: identified by plan directory and start time as this session's T47 plan reviews before SIGTERM.
- Never touched: worker-sec, orchestrator-review, and remote `feat/pr-feedback-gate` (no force push).
- No pane read; `herdr workspace list` is metadata only. All test fakes live in temporary directories.

## Revisions 3 and 3-b

- 91cc85f and 63c993b sit on b91f949, pushed without `-u`; the same unsandboxed classes. Each negative check swapped in the previous launcher and restored it (`cmp` exit 0). The resolver runs in a separate read-only bash; nothing under ~/.agents/skills/agmsg was edited.

## Revisions 4 and 4-b

- 00573f3 and b29ef04 sit on 63c993b, pushed without `-u`; the same unsandboxed classes. Each negative check swapped in the previous launcher and restored it (`cmp` exit 0).

## Revision 5

- 9e36e63 sits on b29ef04, pushed without `-u`; the same unsandboxed classes. The negative check swapped in the r4-b launcher and boundary script and restored both (`cmp` exit 0). The boundary tests build throwaway git repositories and worktrees in the test temporary directory.

## Revision 6

- 2721f0c sits on 9e36e63, pushed without `-u`; the same unsandboxed classes. The negative check swapped in the r5 boundary script and restored it (`cmp` exit 0). The workspace test writes a per-workspace fake `herdr` into the test temporary directory.

## Revision 7

- d806a3d sits on 2721f0c, pushed without `-u`, using the same unsandboxed classes: `make` gates, `git commit` and `git push`, and `gh`.
- A temporary `git worktree add` for the negative check was denied by the permission gate. Instead I swapped the 2721f0c scripts into worker-c and restored them (`cmp` exit 0 for both).
- The new tests write their fakes (`identities.sh`, `model-profiles.env`, `check-agent-runtime.py`) only under the test temporary directory.

## Revision 8

- 98ea49f sits on d806a3d, pushed without `-u`, using the same unsandboxed classes: `make` gates, `git commit`/`git push`, and `gh`.
- The negative check swapped in the d806a3d `herdr-agents` and restored it (`cmp` exit 0).
- The fakes live only under the test temporary directory.

## Revision 9

- a71e78d sits on 98ea49f, pushed without `-u`. The change is documentation only.
- The commands run unsandboxed were `make render-check`, `make validate-agent-assets`, `git commit`, `git push` and `gh`.
