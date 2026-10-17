# Learning triage: dotfiles-T128-seat-liveness-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] `unittest` runs `addCleanup` callbacks after `tearDown`, so a test that removes a directory's write bit must restore it inside the test (`try`/`finally`) when `tearDown` itself removes the tree.
2. [memory:decision] In the Claude sandbox, `~/.ssh` is unreadable, so any test fixture that runs `git commit` fails on SSH commit signing (exit 128). `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false` turns it off for every child git without touching a config file. A module that still fails in the sandbox is compared against `origin/main`'s own run before any failure is attributed to the change.
