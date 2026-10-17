# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a02

These are candidates only; nothing is promoted.

1. [memory:decision] A test double for an installer should refuse what the real tool refuses: the fake npm overwrote any `~/.local/bin/omp`, so npm's EEXIST on a foreign entry was never exercised; a fixture that models the refusal (link into the package, refuse an entry it does not own) turns the shared install test into a migration test.
2. [memory:failure] Before trusting a review's description of a removal path, run it: `remove-agent-asset update_hcom` did not delete the binary and wheel as the review assumed; it refused both paths as outside its safe roots and removed nothing.
