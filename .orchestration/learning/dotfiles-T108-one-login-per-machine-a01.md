# Learning: dotfiles-T108-one-login-per-machine-a01

- **A repository-wide validation grep scans files outside the allowed set.** Running the task's own grep on the untouched tree first showed the SKILL still named `WORKER_GH_CONFIG_DIR`. Asking about it up front (PONG decision 1) avoided a RESULT that could never pass its own check.
- **"Inverted" tests can check absence without naming what was removed.** With the removed names banned from `tests/`, the tests assert the removed mechanism's other traces instead: no token unsetting, no `--env GH_`, an inherited token kept at boot, no ruleset or bypass API in the gate.
- **zsh does not word-split `$var`.** A `for c in "...";` loop passed each command to `codex execpolicy check` as one token, and every rule looked unmatched. Run such loops under bash, and always put `--` before the command so its flags are not parsed as the checker's own.
- **A failed `git add` aborts the whole add.** One missing pathspec (an already-renamed file) left only the staged renames for the commit. Read back `git show --stat` after every commit.
