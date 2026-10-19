# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a03

These are candidates only; nothing is promoted.

1. [memory:decision] When a statement-local lint flags a comparison of values a caller normalised on an earlier line, move the normaliser into the comparing helper rather than adding allow markers.
   - `path_has_prefix` now folds both operands itself. Its callers' rows go, and the helper is safe for a caller that forgets to normalise.
   - The lint's LIMIT asks for a cross-line data-flow once a second marker is needed, so three markers would have pushed the work into the lint.
2. [memory:failure] A hand-rolled path fold must fold both sides of the comparison. `update_omp` folded the link target but compared it against `${HOME}/…` as spelled, so a HOME with a trailing slash moved npm's own link aside.
   - The test fixture npm already folded both sides (`os.path.normpath`), so the fixture and the script disagreed. Only a HOME spelled differently showed the gap.
3. [memory:decision] A path-shaped spelling of something that is not a path is a false positive to fix at its spelling, not through a normaliser. The `uname -s`/`uname -m` pair joined by `/` reads as a path; joined by `-` it does not.
   - A normaliser there would be wrong: `realpath Darwin/arm64` resolves against the working directory.
   - The red-then-green test for such a row can only be the lint itself, because behaviour does not change.
4. [memory:failure] Round 1 ran the updater's tests outside the sandbox after macOS `mktemp -d` without a template was refused inside it. That was the audit's P1: a refusal is a blocked PONG, never an escape, tests included, fakes or not.
   - The fix that keeps work inside the sandbox is a `${TMPDIR:-/tmp}/<name>.XXXXXX` template on each `mktemp` the tests reach (round 2, `92d39f00`).
   - A red proof at a base without the template then needs the template hunk applied to that base, so the row's assertion is reached.
5. [memory:failure] `gh` was run outside the sandbox on an assumption. Inside the sandbox, `gh pr view`, `gh pr checks` and `gh api` work. Try the sandbox first, and leave it only after a recorded refusal.
6. [memory:failure] A Bot wait on a draft PR is no Bot wait, because the Codex Bot reviews when a draft is marked ready. Check `isDraft` before claiming the window, and report the draft state instead.
