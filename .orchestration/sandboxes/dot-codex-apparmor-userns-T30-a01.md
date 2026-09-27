# T30 sandbox record

- No container or VM isolation was used. The change is an install script,
  profile, and doctor check, covered by hermetic unit tests (fake `sudo`,
  `apparmor_parser`, `bwrap`, `codex` on PATH; the sysctl, bwrap, and profile
  target paths redirected through env seams into a temp dir).
- Git work used the dedicated worker worktree `.claude/worktrees/worker-c` on
  branch `feat/codex-apparmor-userns`, created from `origin/main` (c326c73).
- **No sudo was run, no sysctl was changed, and the profile was not activated
  on this host.** The profile was only parse-checked with the non-root
  `apparmor_parser -Q -K`, which skips the kernel load. A broken-profile
  negative control shows that check is real.
- Read-only host probes: the sysctl values, `bwrap --ro-bind / / true`
  (fails), `codex sandbox true` under `strace -e trace=execve`, and the same
  under a PATH-first logging shim in the scratchpad. `codex sandbox true` runs
  `true` inside codex's sandbox and fails at bwrap setup; nothing was written
  to the repo.
- The mutation baseline ran against a `git archive origin/main` export in the
  scratchpad.
- No `make apply`/`chezmoi apply` was run. The local Bats suite was not run
  (repo policy); bats runs in CI.
