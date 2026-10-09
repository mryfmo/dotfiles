# Learning: dotfiles-T114-canonical-clone-reconcile-a01

Candidates only; nothing promoted.

1. A worker seat's GitHub credential is not verified at seating: worker-c's pane had an empty SSH agent and no gh login, so the task blocked only at push time, after all the work. Candidate check: `herdr-agents --add-worker`/pair seating (or the pre-dispatch PING) probes `git ls-remote` on the push URL and `gh auth status` from the worker pane and reports `github=unauthenticated`.
2. `make unit-test` cannot run clean inside the Claude worker sandbox on macOS (83 pre-existing failures: mktemp under /var/folders, pty exhaustion, global SSH commit signing). Task files that list it as a validation command should either say "CI is authoritative" or name the sandbox-safe subset; a worker proves no regression by rerunning the failing ids on origin/main.
3. Running mise inside the sandbox needs `MISE_STATE_DIR` redirected (the trust symlink under ~/.local/state/mise is write-denied); `MISE_TRUSTED_CONFIG_PATHS` alone does not avoid the write.
4. A skip-case test must make the skipped condition otherwise reportable (dirty file inside the scanned trees), or it cannot fail; checked here by removing the skip.

## Round 1

5. An explicit HTTPS URL is not enough to avoid SSH on this machine: the global `url.git@github.com:.pushInsteadOf https://github.com/` rewrites it. Task text that prescribes an HTTPS push for a seat with no SSH identity should use `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/<repo> <branch>`, or the seat's environment should supply `GIT_CONFIG_*` pairs that cancel the rewrite. Candidate: the pre-dispatch PING checks `git push --dry-run` from the worker pane.
