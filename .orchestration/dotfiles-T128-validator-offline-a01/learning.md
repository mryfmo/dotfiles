# Learning triage: dotfiles-T128-validator-offline-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A Makefile `$(shell …)` probe resolves its command on the environment's PATH, as the recipe does, so a stub first on PATH serves both, and one test sees the probe and the run in order. The probe's own argv (`-c import yaml`) is what the stub keys on, so no flag is needed to tell the two apart.
2. [memory:decision] Evidence that should not move the head after the Bot's review can be planned in advance. This task's sandbox table lists the post-ready `gh` calls before they run, and the RESULT carries the Bot's threads and CI, so no evidence update follows the review. That saves one CI round on a seven-line change.
