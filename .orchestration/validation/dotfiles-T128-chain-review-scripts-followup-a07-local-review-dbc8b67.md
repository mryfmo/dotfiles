---
task: dotfiles-T128-chain-review-scripts-followup-a07
head: dbc8b67d26257d76f26dd6871716b7943474fdec
pr: 439
base: f7ed01427a43567b9c1857d2f62953add8b97c92
started: 2026-10-20T08:04:17Z
finished: 2026-10-20T08:09:40Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Preserve Git hardening in Codex's spawned command environment — scripts/orchestrator/local-review.sh:36-36

```text
The canonical-base lookup is sound, but the new Git protections do not survive the configured Codex command-environment filtering. Static checks were performed; runtime tests were not run under the read-only constraint.

Review comment:

- [P1] Preserve Git hardening in Codex's spawned command environment — scripts/orchestrator/local-review.sh:36-36
  With the checked-in `shell_environment_policy.inherit = "core"` configuration, Codex's [shell environment policy](https://learn.chatgpt.com/docs/config-file/config-advanced#shell-environment-policy) drops these exported variables from the reviewer's commands. A worker-planted replacement giving the canonical base the head's tree is therefore ignored during the wrapper's checkout but honored by the reviewer's `git diff`, potentially producing an empty diff and a false clean review. Pass both values explicitly through `shell_environment_policy.set` overrides and test that filtering boundary; the Bash-only review stub currently bypasses it. This leaves the trust-boundary mitigation required by [AGENTS.md:78](AGENTS.md#L78) ineffective.
The canonical-base lookup is sound, but the new Git protections do not survive the configured Codex command-environment filtering. Static checks were performed; runtime tests were not run under the read-only constraint.

Review comment:

- [P1] Preserve Git hardening in Codex's spawned command environment — scripts/orchestrator/local-review.sh:36-36
  With the checked-in `shell_environment_policy.inherit = "core"` configuration, Codex's [shell environment policy](https://learn.chatgpt.com/docs/config-file/config-advanced#shell-environment-policy) drops these exported variables from the reviewer's commands. A worker-planted replacement giving the canonical base the head's tree is therefore ignored during the wrapper's checkout but honored by the reviewer's `git diff`, potentially producing an empty diff and a false clean review. Pass both values explicitly through `shell_environment_policy.set` overrides and test that filtering boundary; the Bash-only review stub currently bypasses it. This leaves the trust-boundary mitigation required by [AGENTS.md:78](AGENTS.md#L78) ineffective.
```
