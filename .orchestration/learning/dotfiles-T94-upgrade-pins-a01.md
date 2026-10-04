# Learning triage: dotfiles-T94-upgrade-pins-a01

Candidates only; nothing is promoted.

1. **Cross-check checksum pins against the upstream release.** A carried `make upgrade` diff with new sha256 pins should be checked against the release's own `checksums.txt`. The check is cheap and independent of the machine that produced the diff.
2. **`git worktree prune` acts on the whole shared repository.** It prunes every entry whose directory is missing, including those of other seats. A worker should only remove its own temporary worktree (`git worktree remove`) and never run the prune.
