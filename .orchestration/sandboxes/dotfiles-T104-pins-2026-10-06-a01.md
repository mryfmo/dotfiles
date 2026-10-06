# Sandbox: dotfiles-T104-pins-2026-10-06-a01

- **Sandboxed:** `git switch -c`, `git apply --index` (reading the diff from the main checkout), `make render-check`, `make unit-test`, the validator, the test grep, and the commit.
- **Through the permission gate (Worker Playbook step 4):**
  - `git push`, `gh pr create`, `gh pr checks` and the bot-wait polling;
  - the CompactionDB `memory add` in the main checkout;
  - writing and masking these artifacts in the main checkout;
  - `agmsg-dispatch`.
- **Not done:** no `make update`/`upgrade`/`apply`, no edit outside the seven diff files, no thread resolution, no local bats.
- **Disclosed deviation, the inbox read:** `~/.agents/skills/agmsg/scripts/inbox.sh dotfiles claude-standard-dot-a005` was run from worker-c outside the sandbox, through the permission gate, for the task message (1888) and the decision message (1916).
  - Inbox reads are not a step-4 exception, and the read works inside the sandbox: the agmsg store is a writable root.
  - Running it outside was a habit carried over from earlier tasks, not a need.
  - Later inbox reads run inside the sandbox.
