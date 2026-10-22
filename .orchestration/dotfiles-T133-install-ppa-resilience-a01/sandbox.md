# Sandbox record: dotfiles-T133-install-ppa-resilience-a01

- **Producer:** worker (Claude seat), in `.claude/worktrees/worker-f`, under Worker Playbook step 4.
- **Inside the sandbox ran:**
  - `git fetch`, `git switch -c … --no-track`, commits (`git -c commit.gpgsign=false`), the push without `-u`;
  - `gh pr create --draft`, `gh pr ready` and the `gh` reads of checks and job logs;
  - `bash -n`, shellcheck, shfmt, the comparison lint, and the plain-bash smoke of the fakes.
- **Outside the sandbox:** only `agmsg-dispatch`, through `excludedCommands`. No command was refused.
- **Not run:** Bats was never run locally; red and green come from GitHub Actions.
