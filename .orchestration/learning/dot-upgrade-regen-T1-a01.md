# dot-upgrade-regen-T1-a01 learning triage

[memory:decision] Validated reusable fact: on this Mac, `~/.config/mise/config.toml` and `~/.config/mise/mise.lock` symlink to the normal dotfiles checkout. Running `make upgrade` from a dedicated worktree therefore updates that active symlink target; copy the regenerated pair into the dedicated worktree before review.

Disposition: recorded in the Codex learn index and CompactionDB. No skill promotion was performed.
