# T29 sandbox record

- OpenSandbox was not used. The change is config, a pin bump through the
  sanctioned `--set-asset` path, docs, and one policy-test update.
- Git work used the dedicated worker worktree `.claude/worktrees/worker-c` on
  branch `feat/version-currency`, created from `origin/main` (5b15d1e).
- `renovate-config-validator` ran as a one-off `npx --package renovate@44`.
  No dependency was added. npm's release-age guard refused the 7-day-old
  `44.115.10`, and I did not override it; it resolved `44.103.6` instead.
- I downloaded both Understand-Anything `install.sh` revisions read-only into the
  scratchpad to hash and diff them. Neither was executed.
- The policy-test baseline ran against a `git archive origin/main` export in
  the scratchpad, so no repository state was touched.
- No `make apply`/`chezmoi apply` was run. The local Bats suite was not run
  (repo policy); bats runs in CI.
