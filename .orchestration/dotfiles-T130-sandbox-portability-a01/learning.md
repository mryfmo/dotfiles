# Learning triage: dotfiles-T130-sandbox-portability-a01

These are candidates only; nothing is promoted.

1. [memory:decision] "Process substitution fails in the sandbox" was one data point (`diff <(…)`) generalised into a rule; measured, `done < <(…)`, `comm <(…) <(…)` and `cat <(…)` all work there and only `diff` fails. A guard is written to the measured predicate, and the measurement is pasted (validation §3) so the next reader need not take the rule on faith.
2. [memory:decision] A guard test over the tracked tree is run against the tree before it is specified as "the checkout, accepted": item 1's letter refused 31 lines in 11 files and item 2's two lines sat in a script outside the task's files; both were questions before any code.
3. [memory:failure] A store relocation inside one package copy was scoped without the other readers of the same path: the Codex notify receiver, its tests, the trusted upstream copy under the home directory and the installer all name `.claude/contextdb`. Before moving a path that is a trust boundary, list every reader of it with `git grep` across `home/`, `scripts/`, `tests/` and `vendor/`, not only the package.
