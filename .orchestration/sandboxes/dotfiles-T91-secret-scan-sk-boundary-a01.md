# Sandbox: dotfiles-T91-secret-scan-sk-boundary-a01

- **Worktree and branch:** worker-c, branch `fix/secret-scan-sk-boundary` from `origin/main` 57885db1. The `git switch -c` was finished with `git symbolic-ref` and `git reset --hard HEAD`. The push landed, verified with `git ls-remote`.
- **Main-checkout scan:** I scanned the main checkout's `.orchestration` tree read-only, with both patterns, from a Python process. No evidence file was edited or masked except my own T91 validation file, masked with `--mask-secrets` on its key-shaped samples.
- **Unit tests** ran in the Claude sandbox.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks` and `gh api`;
  - the read-only main-checkout scan;
  - CompactionDB `memory add`;
  - the writes and the mask of the main checkout's T91 `.orchestration` files;
  - `agmsg-dispatch`.
