# Sandbox: dotfiles-T76-ineffective-settings-a01

- **Sandboxed:** edits, the generator run, render-check, validate, unit tests, the migration simulation and the commit.
- **Unsandboxed:** the push, `gh pr create`, `gh api` and `gh pr checks`, CompactionDB `memory add` from the main checkout, and these artifact writes.
- **Phantom `.git/config.lock`:** it blocked the upstream config on `switch -c` and `push -u`. I finished with `git symbolic-ref` plus `reset --hard origin/main`, and `git ls-remote` confirmed the push.
- **Untouched:** no home/ file outside the five allowed ones (`modify_private_config.toml` is forbidden; see the report), and nothing in the main checkout besides these artifacts.
- **Not done:** no merge, force push, push to main, thread resolution, local bats, or `make update`/`apply`/`upgrade`.

## Revise round 1

- **Sandboxed:** the merge-script edit, tests, the simulation and the commit.
- **Unsandboxed:** the push, `gh pr update-branch`, `gh` polling, and these artifact writes.
- The merge script's file mode was kept: `cp` onto the existing file, and no mode change appears in the diff summary.

## Revise round 2

- **Sandboxed:** edits, tests, checks and the commit.
- **Unsandboxed:** the push, `gh` polling, and these artifact writes.
