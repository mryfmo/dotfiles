# Learning triage: dotfiles-T133-install-ppa-resilience-a01

These are candidates only; nothing is promoted.

1. [memory:decision] Bats cannot run locally here, but a fake harness written as a `bash -c` snippet can. Extract it and run it in plain bash against both installers before pushing the red. Here that caught a `set -u` bug in the fakes before the red run would have failed for the wrong reason.
2. [memory:failure] The comparison lint (R6) refuses `grep -E` on an interpolated variable, so a host check in a shell script uses `grep -F` with the fixed strings.
3. [memory:decision] The test workflow runs on pull requests only, not on branch pushes, so a red CI run needs the PR open (as a draft) before the fix commit.
