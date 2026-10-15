# Learning triage: dotfiles-T128-orchestrator-tools-followup-a02

These are candidates only; nothing is promoted.

1. [memory:decision] A mutation claim is evidence only with its commands pasted: this task's validation §6 holds the mutant script itself (the `sed` of each fix, the one test, the `git checkout` restore) and its output, which answers the P2 the audit of 39c186a raised on the previous task.
2. [memory:decision] `git show --name-status` quotes a path only for control or non-ASCII bytes (`core.quotePath`); `*` and `[` print bare, so a test can compare those names unquoted.
