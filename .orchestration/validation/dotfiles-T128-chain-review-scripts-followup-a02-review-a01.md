# Review receipt: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 (round 2)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs in parallel)
- previous_receipt: round 1 sha256 `9e0c7935566803c7f060b2535d5b72d46fe8a5ae5cff9338e08f249d7ab73468` (revise on `0e88cadd`, two P2 and three P3; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02-review-a01.md` sha256 `427d0277d6adeae267f0dd01a8786c24dc0100654ce6b215849d1daaee16edb6` (the round-1 brief with the round-2 note in its intro and stop conditions 1 and 2 reworded for the four features, the whole `-S` string, the stdout line and the five cases; `diff` against the round-1 copy shows nothing else)
- reviewed file: `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a02.md` sha256 `d76a00f9d38db75862f0bb7c3ca065c721a7b0ee92dbe7d97b3c2f50ca019c53` (copied from the main checkout and hashed before reading)
- sources: as in round 1 (`local-review.sh` and the test module at PR #364's head `2e3ff494`; the audit text and the local review of that head; the record in the main checkout); origin/main `2c9b10e9`, unchanged since round 1

## What changed since round 1 (`diff` of the two copies: lines 15, 19, 20, 54, 58, 59, 69, and a new "Change (round 2)" section)

- P2-1 applied: the refused set is a double quote, a single quote, a backslash, a dollar sign or a word starting with `#` (the four `env -S` features bash's `read -r -a` splits differently, which this seat replayed on this host's `/usr/bin/env -S` in round 1), the message names "a quote, an escape, an expansion or a comment", row 1 and row 3 say the same, and item 2 adds a `${HOMEX}/lib` case and a `one # two` case (five in all).
- P2-2 applied: the refusal is a stdout line, named as the script's convention in item 1 and as what `run_tool` returns in item 2; the brief's stop condition 2 says the same.
- P3-1 applied: the record now carries `local:2e3ff49:1<TAB>env-s-quoting` and `audit:2e3ff49:1<TAB>env-s-quoting` under the a02 owner heading (lines 72 to 73 of the record in the main checkout), the audit row also under its audit heading (47), and the intro says so.
- P3-2 applied: the check reads the whole `-S` string, regex group 2 and group 3. P3-3 applied: the Completion names every P2 thread with the disposition the worker proposes, the tools a02 wording.

## Checks (stop condition 1 to 4)

1. As in round 1 against the PR head (the shebang branch 91 to 99, the checkout at 100): the refusal of the whole `-S` string on the four features, exit 2 and a stdout line before the checkout, nothing written, the worktree untouched, plain words split as today, the parser alternative out of scope, fail closed. The regex's group 2 admits a token starting with a quote, so reading both groups is what makes a quoted interpreter token the same refusal.
2. The test name is verbatim in the closed row (16) and item 2 (59); the five first lines are constructible as the round-3 test builds its own (302 to 321); the stdout assertion matches `run_tool` (92 to 105) and the shim refusal test (295 to 297); the worktree-at-main, no-file and interpreter-never-run assertions have their precedents (221, 298 to 300); the plain-word test stays.
3. 13 controls as in round 1, the seven generic rows byte-identical to the template after id substitution (compared by script), the new-scripts row saying no new script; the Completion clause is plan 020 step 4's with the C-50 sentence qualified by INV-6's counts; the cap sentence unchanged; the two files are named only by this lineage's three task files, the overlap with PR #364 sequential by `after:` and the dispatch condition.
4. `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-chain-review-scripts-followup-a02.md: OK`; `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal; the two premises (unchanged) extracted with PyYAML and replayed with `bash -c` from the main checkout after `git fetch`: `0`, `0`, equal.

## Findings

None. A note for the worker, no change needed: a `#` that is not at the start of a word (`a#b`) is literal to `env -S` and the item's "a word starting with `#`" keeps it allowed; any `$` is refused even where env would not expand it (inside single quotes, which are refused anyway), which is the fail-closed side.

Task-file verdict: dotfiles-T128-chain-review-scripts-followup-a02: confirm
