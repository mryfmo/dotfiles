# T18 sandbox record

- Source edits and unit/static validation ran in the isolated Git worktree
  `/private/tmp/dotfiles-t18` under the workspace-write sandbox.
- The existing main worktree's unrelated mise and orchestration changes were
  not copied, modified, staged, or committed.
- Herdr socket operations required the approved unsandboxed execution path;
  every mutation targeted only scratch workspaces `w18` and `w19`.
- GitHub network operations will use approved `git`/`gh` commands.
- OpenSandbox was not available or needed; the Git worktree plus task-specific
  Herdr workspaces provided isolation.

