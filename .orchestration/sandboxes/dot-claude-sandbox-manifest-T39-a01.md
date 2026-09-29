# T39 sandbox record

- No container or VM isolation was used. All git work happened in
  `.claude/worktrees/worker-c` on `feat/claude-sandbox-manifest-r2` from
  origin/main d2f19ec, which was clean before the switch.
- PR #179's head was fetched read-only into `refs/remotes/origin/pr/179`.
  Nothing was pushed to `feat/claude-sandbox-manifest`, and #179 was not
  closed or commented on.
- Network use:
  - read-only `curl`/WebFetch of code.claude.com docs (settings-reference.md,
    sandboxing.md), saved in the session scratchpad;
  - `git push` of the task branch (no force);
  - `gh pr create`;
  - `gh pr checks`.
- The managed settings template was produced only by
  `uv run --with pyyaml scripts/generate-agent-configs.py`. No `sudo`,
  `make update`/`upgrade`, `chezmoi apply`, `mise install` or local Bats.
- Main's AppArmor files and `check_apparmor_userns` are unchanged, as are
  `.claude/hooks`, permgate, `.ua` and `.orchestration/tasks`. Writes outside
  the worktree were limited to the listed `.orchestration` artifacts and the
  CompactionDB `memory add`.
