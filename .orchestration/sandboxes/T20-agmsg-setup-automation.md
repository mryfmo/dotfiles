# T20 sandbox record

- Implementation worktree:
  `/private/tmp/dotfiles-t20` on `feat/agmsg-setup-automation`.
- E2E repository:
  `/private/tmp/t20-agmsg-setup-automation`.
- E2E HOME:
  `/private/tmp/t20-agmsg-setup-automation/scratch-home`.
- The scratch HOME symlinked only the installed agmsg `scripts` directory;
  its teams, run state, DB, Herdr log, hook files, and watcher were isolated
  under the scratch directory.
- The first E2E attempt used the real HOME and was blocked before delivery by
  sandbox denial on the Herdr log redirection. No hook was created. Validation
  then moved to the isolated scratch HOME without requesting broader access.
- The real `/Users/mryfmo/Workspace/dotfiles` repository was never passed to
  `delivery.sh set`.
- No live Herdr workspace, chezmoi deployment, or local bats execution
  occurred.
- The scratch watcher was stopped and scratch directories were removed after
  evidence collection.
