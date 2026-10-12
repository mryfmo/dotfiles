# Learning triage: dotfiles-T128-process-rules-a07

These are candidates only; nothing is promoted.

1. [memory:failure] Four Bot P1s on PR 318 (4243885108, 4243923211, 4243923214, 4243975211) were one class: a task record whose threat table or `allowed_files` lagged behind a change elsewhere in the same file. A mechanical pre-dispatch check (every `allowed_files` entry has a row; the copies row and its hash name the current task) closes that class better than review rounds.
