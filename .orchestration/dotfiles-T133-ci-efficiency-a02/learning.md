# Learning triage: dotfiles-T133-ci-efficiency-a02

These are candidates only; nothing is promoted.

1. [memory:decision] A helper that reruns CI on a classification of a run's jobs must first require `status == completed`. A snapshot of a run in progress classifies jobs that are not final, and `gh run rerun --failed` acts on the run's final state, not on the snapshot (worker review P2, fixed in `492e7e28`).
2. [memory:failure] Under a matrix's default `fail-fast: true`, one real failure or flake cancels its siblings. A rule that every cancelled job needs its own flake signature (item 8) therefore refuses the very run that justified the signature. Run 39046848147's attempt 1 has two cancelled public-bootstrap jobs next to the failed one. A spec that classifies cancellations must decide fail-fast first: `fail-fast: false`, or a rule for cancellations a sibling's failure caused. That is proposed in the RESULT and left to the orchestrator.
3. [memory:failure] `grep` on zero-line input never matches, not even `.*`, while a bash here-string of an empty variable is one empty line. A test that means "an empty log never matches" has to feed `"\n"`, as the script does, or it proves only that the expression compiles (worker review P3, fixed in `72fcb93b`).
4. [memory:decision] The repository's shfmt settings are passed as flags (`make format`: `--indent 4 --space-redirects`; CI: `-i 4 -sr`). `.editorconfig` has `indent_size = 4` but no `indent_style`, so a bare `shfmt -d` asks for tabs on every tracked script. A task's Check that names bare `shfmt -d` reads as the repository form.
