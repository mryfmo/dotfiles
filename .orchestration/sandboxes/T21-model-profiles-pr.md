# T21 Sandbox Record

OpenSandbox was not available in this session. The documented fallback was an
isolated git worktree at `../dotfiles-model-profiles`, created from
`origin/main` on `feat/model-profiles`.

Only the T21 allowlisted 34 paths were transferred. A mechanical comparison of
the actual changed-path set against `/tmp/T21-expected-paths.txt` returned exit
code 0 before commit. The original main worktree's product changes and git
state were not modified.

Network and adjacent-worktree writes used the managed permission gate. No
runtime state under `~/.claude`, `~/.codex`, or `~/.agents` was edited.

After acceptance, the isolated worktree was removed only after the main
worktree passed the empty 27-path parity check and synchronized to the verified
merge commit. Final worktree and branch presence checks all returned `no`.
