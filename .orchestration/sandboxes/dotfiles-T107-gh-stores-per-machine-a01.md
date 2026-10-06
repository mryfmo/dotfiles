# Sandbox: dotfiles-T107-gh-stores-per-machine-a01

- **Sandboxed:**
  - the inbox reads (`~/.agents/skills/agmsg/scripts/inbox.sh dotfiles claude-standard-dot-a005` from worker-c). They printed a harmless herdr pane-rename refusal and delivered the message.
  - `git switch -c`, edits and the generator run;
  - `bash -n` and shellcheck, ruff and prettier;
  - the unit tests, `make unit-test`, `make render-check` and the validator;
  - the commit.
- **Through the permission gate (Worker Playbook step 4):**
  - `git push`, `gh pr create`, `gh pr checks` and the bot-wait polling;
  - the CompactionDB `memory add` in the main checkout;
  - writing and masking these artifacts in the main checkout;
  - `agmsg-dispatch`.
- **Credentials:** no command read, listed or ran `gh` against the real `~/.config/gh` or `~/.config/gh-worker`. The doctor and script tests use fake HOMEs and a fake `gh`.
- **Not done:**
  - no `make update`/`apply`/`make gh-auth`, no `gh auth login`;
  - no edits outside the allowed files (`scripts/check-tools.sh` and `setup.sh` needed none);
  - no thread resolution, no local bats.
