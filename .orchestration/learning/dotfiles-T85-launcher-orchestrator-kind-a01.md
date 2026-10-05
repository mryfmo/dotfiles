# Learning: dotfiles-T85-launcher-orchestrator-kind-a01

- **Put a guard where every path passes through.** `--attach` has an early plain-shell exit inside the argument parser, so the orchestrator-kind guard sits before the parser, keyed on `$1`.
- **Write a no-dependency mode before its dependencies are required.** `--directive` sits before `require_command herdr`, so it works from a plain shell and serves a Codex orchestrator.
- **Run a scratch-mise tool with an absolute path.** `mise -C <dir> x shfmt` runs from that directory, so a relative path fails with lstat.
