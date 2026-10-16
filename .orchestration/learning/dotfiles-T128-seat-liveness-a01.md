# Learning triage: dotfiles-T128-seat-liveness-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A dead seat (its pane gone after a restart) is told from a live one by the driver's `terminal_pane_state`. It is reached through the seat's placement record, and it reads herdr's agent list, never pane content. Only `gone` may retire a seat, and `unknown` keeps the despawn path.
2. [memory:decision] A retired placement record is moved under `run/stale/` with a timestamp, never deleted. It is evidence, and keeping it out of the `spawn.*` scan stops a later seat on the same pane id from reading it as a rival claim.
3. [memory:failure] Local unit runs in a Claude worker sandbox fail where they make signed commits: `git commit` exits 128. Set `commit.gpgsign=false` through `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0` and `GIT_CONFIG_VALUE_0`. Then compare the failure set with an `origin/main` baseline worktree before calling anything a regression.
4. [memory:failure] A mutation proof found two untested branches in my own test: the `unknown` state, and the skipped claim. Run the mutants before writing the evidence, and add the case each survivor names.
5. [memory:failure] `diff - file` fails in this sandbox (`Operation not permitted`) on stdin. Write both sides to files first.
