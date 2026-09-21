# dot-upgrade-regen-T1-a01 learning triage

[memory:decision] Validated reusable fact: on this Mac, `~/.config/mise/config.toml` and `~/.config/mise/mise.lock` symlink to the normal dotfiles checkout. Running `make upgrade` from a dedicated worktree therefore updates that active symlink target; copy the regenerated pair into the dedicated worktree before review.

Disposition: recorded in the Codex learn index and CompactionDB. No skill promotion was performed.

[memory:decision] Validated reusable fact: regenerated mise pins must be propagated to workflow install/where commands, Python smoke expectations, and exact-version tests in the same change. Otherwise CI can install one locked version while asserting another.

[memory:decision] Validated reusable fact: with mise 2026.9.12, an isolated config that installs npm tools must install its configured locked node dependency first. Mirror `run_mise_install` ordering in CI fixtures.
