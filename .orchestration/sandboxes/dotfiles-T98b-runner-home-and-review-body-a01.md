# Sandbox: dotfiles-T98b-runner-home-and-review-body-a01

- **Sandboxed:** edits, unit tests, `make unit-test`, the validator (also with `HOME` set to the runner home), the re-mask run over the worktree's tracked `.orchestration`, prettier, ruff, and the commit.
- **Unsandboxed:**
  - push, `gh pr create`, `gh pr checks --watch`, and the bot-wait polling (reviews, inline comments, issue comments for the quota notice);
  - CompactionDB `memory add` and readback;
  - writing and masking these five artifacts in the main checkout's `.orchestration/`, through the permission gate. The main checkout is not writable from a worktree sandbox, so this is the same class of gated write as the CompactionDB `memory add` that Worker Playbook step 4 documents. The SKILL does not yet list the artifact writes; the orchestrator records that as a follow-up;
  - `agmsg-dispatch`.
- **No scratch worktrees**, and no `git worktree prune`.
- **Not done:**
  - no change to `SECRET_PATTERN` or the credential scan;
  - no edit to the rule file or `home/dot_local/bin/**`;
  - no `make update`/`apply`;
  - no thread resolution;
  - no local bats.
