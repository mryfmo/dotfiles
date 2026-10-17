# Review receipt: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 (round 4)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs in parallel)
- previous_receipt: round 3 sha256 `46251b1ce4d56eee016e9c9af373b7c52c9e9c90753b069ec52908e1aa73e33b` (confirm on `eaafb779`; rounds 1 and 2 were revise on `436d4375` and `f91f7bd2`; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02-review-a01.md` sha256 `b619ea5cc4f715abe25aecac3fb07dfda8c301e73aa873ee564b73f2d90b4c36` (the round-3 brief with one round-4 sentence in its intro; `diff` against the round-3 copy shows nothing else)
- reviewed file: `.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02.md` sha256 `5d3b78db38ea4a84b13938038258be75d2639639c55894bdb8bc3d50a00647ef` (copied from the main checkout and hashed before reading)
- origin/main at review: `907522c2` (unchanged since round 1)

## What changed since round 3 (`diff` of the two copies: line 32 and a new "Change (round 4)" section)

- The Codex half's round-3 P2 applied to the environment row: it no longer says the script "never" reads a PR checkout's files as if the script checked its paths; it now says the script reads the dispositions TSV and the sweep JSON by the two paths its caller passes, with no path check of its own (as today), the orchestrator passing its own checkout's files and the chain never passing a PR checkout's path. That matches the script on origin/main: `[[ -f ${tsv} ]]` at line 31 tests existence only, the sweep is read behind `-s` at 43, and nothing inspects where either path points. Items 1 to 3, the other rows and the premises are round 3's.

## Checks (stop condition 1 to 4)

1. As in round 3: item 1 reads as the script allows (both local sources scanned before the first query at line 34, exit 2 with the stated stderr line, nothing posted or resolved, the backtick alone refused with its reasons, the header clauses named, fail closed); the judgment that refusing beats a longer fence stands.
2. As in round 3: the test name verbatim in the closed row and item 2, two constructible cases, the empty call log under the pre-query scan, the helper form named; the lineage's tests stay.
3. 13 controls, one per `allowed_files` entry plus the GitHub-threads row; the seven generic rows byte-identical to `.orchestration/templates/task-short.md` after id substitution (compared by script); the new-scripts row says no new script; the environment row is the one row changed, within the template's slot for it; the Completion clause and the cap sentence unchanged; no in-flight task names either file.
4. `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-chain-github-scripts-followup-a02.md: OK`; `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal; the three premises (unchanged) extracted with PyYAML and replayed with `bash -c` from the main checkout after `git fetch`: `0`, `0`, `0`, equal.

## Findings

- P3 (low, no change needed) `dotfiles-T128-chain-github-scripts-followup-a02.md:32`: "gh, jq and the coreutils" covers `awk` (line 42) by loose usage; awk is not a coreutil, but the row's point (every binary by name from PATH, the stub `gh` as the seam) holds for it as well.

Task-file verdict: dotfiles-T128-chain-github-scripts-followup-a02: confirm
