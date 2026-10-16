# Learning triage: dotfiles-T128-chain-glue-finish-a01

These are candidates only; nothing is promoted.

1. [memory:decision] macOS `/bin/bash` is 3.2, where expanding an empty array under `set -u` is an unbound-variable error. A chain script that may hold an empty optional-argument array writes `${a[@]+"${a[@]}"}`, and a test suite that runs it with `bash` from `/bin` exercises that case.
2. [memory:decision] One order log that every stub appends its name to lets a test assert the exact order of calls across several stubs, which separate per-stub logs cannot.
