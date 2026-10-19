# Learning triage: dotfiles-T129-normalised-comparison-lint-followup-a03

These are candidates only; nothing is promoted.

1. [memory:decision] A tree-wide exact-match baseline is a global invariant that every merge to main can break. Gate on the files the change touches, and report drift in other files as warnings.
   - The changed set is the guard's input, so it is computed with the isolated git (plan 024 §5.14 item 2), not the caller's.
   - CI's test job already fetches `origin/main` with full history, so the no-flag mode needs no workflow change.
2. [memory:failure] Git does not accept `-c` joined to its value (`-ccore.hooksPath=…` fails). Pass `-c` and the value as two arguments.
3. [memory:decision] With an explicit scan list, the changed set is a separate input, not inferred from the scan list.
   - Fixture calls name both, so the old tests keep their meaning: the fixture file is the change.
   - The new tests name another file to model drift.
