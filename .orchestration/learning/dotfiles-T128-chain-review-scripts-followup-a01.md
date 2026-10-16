# Learning triage: dotfiles-T128-chain-review-scripts-followup-a01

These are candidates only; nothing is promoted. The candidates of `dotfiles-T128-orchestrator-tools-followup-a01` stand.

1. [memory:decision] Every orchestrator script that runs a host binary from a PR checkout resolves it before the checkout in the trusted root, with `mise which` under `env -i`, falling back to `command -v`. It refuses a `shims` path and runs the absolute path afterwards. orch-gate.sh does this for gh and git, and local-review.sh now does it for codex.
2. [memory:failure] A wrapper that caches a sample must not cache a failed run.
   - **The failure.** local-review.sh logged the reviewer's non-zero exit, then still wrote `findings: 0`. The next run reused it as a clean review.
   - **The fix.** On failure, write nothing and use a distinct exit code.
3. [memory:failure] A cache keyed by a prefix of an id must compare the full id it recorded before reusing.
4. [memory:failure] `/bin/bash` 3.2 (macOS) mis-parses an inline quoted pattern such as `${var//"$x/"/}`: it leaves a stray quote and slash. Put the literal in a variable and write `${var//"$p"/}`. Tests run scripts with the `bash` on PATH, which is 3.2 on macOS.
5. [memory:decision] To prove that a resolution precedes a checkout, the resolver's stub records the target worktree's HEAD at its call. A cwd check proves only where the resolution ran, not when.
