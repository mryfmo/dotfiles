# T28 sandbox record

- Used fresh worktree `/private/tmp/dotfiles-t28.zabX6I` on branch `chore/remove-ccgate`, based on `origin/main`.
- Repository edits were limited to the five tracked files required for ccgate lifecycle removal. The generated shdoc reference is ignored by repository design.
- No local Bats test was run.
- Managed home writes and GitHub network operations used command-specific approvals.
- The first worktree-source `chezmoi apply` exposed a symlink-management hazard: symlink targets referenced the temporary source path. It was immediately corrected with the canonical main chezmoi source, verified by target inspection, and the T28 regular-file policy was then applied narrowly.
- No deployed path references the temporary worktree.
- Because the live mise config is intentionally symlink-managed, the PR's two-line pin removal was also shadowed exactly in the canonical main source. This makes ordinary `mise ls` clean before merge without pointing live state at a disposable worktree; the related local diff must be reconciled after acceptance/merge.
- The live ccgate removal covered every installed version discovered by inventory (0.9.3, 0.9.4, 0.9.5) and ran `mise reshim`.
- No model profile was edited, neither provider was enabled, and no merge was performed before acceptance.
- After explicit acceptance, PR #93 was squash merged and the dedicated worktree plus local/remote task branches were removed.
