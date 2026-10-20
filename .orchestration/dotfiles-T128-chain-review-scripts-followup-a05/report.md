---
task_id: dotfiles-T128-chain-review-scripts-followup-a05
seat: claude-standard-dot-a007
branch: tools/chain-review-scripts-followup-a05
base: a8a747af06b32ff1d0d1720467892f34d9465ae4
task_sha256: b1b9cea0cc5ae47361fb6fef9d9c6f4c6d431e87ab61b85a122121eb736e15b6
---

# Report: dotfiles-T128-chain-review-scripts-followup-a05

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on a fresh branch `tools/chain-review-scripts-followup-a05` from origin/main a8a747af (PR #386 merged). The PR #396 and #398 branches stay in the worktree, committed and pushed.
- Task file: sha256 `b1b9cea0…`, copied byte-identical; the task-consistency check passes (validation §1). No question and no amendment.
- The owned row: `audit:000c5c6:1` (class filename-suffix-parse), from the audit of PR #386's head 000c5c6. The task's item 1 names the a04 acceptance record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a05` section as the source, but that section does not exist in the a04 record, either in the main checkout or on origin/main (validation §1: grep count 0). The row is read from the task's item 1 and the audit receipt, which state it the same way, and from the a05 record's first line.

## The change (validation §3: 3 added and 1 deleted in the script, 23 added in the test)

- `scripts/orchestrator/local-advisory.sh`: in the loop over a task's earlier local review files, the suffix is now the file name with the exact prefix `.orchestration/validation/<task>-local-review-` and the `.md` stripped (`${e#…}`), instead of the text after the last `-local-review-` (`${e##*-local-review-}`).
- The seven-hex check from PR #386 then validates the whole rest of the name. So `<task>-local-review-notes-local-review-aaaaaa1.md` is skipped, and its findings no longer pick up an unrelated `local:aaaaaa1:1` row's class and provenance.
- Nothing else changes.

## Test

- `test_local_advisory_reads_the_whole_suffix_after_the_task_prefix`. An earlier file `t-a01-local-review-notes-local-review-aaaaaa1.md` holds the same token as the current finding, and the record holds `local:aaaaaa1:1<TAB>unrelated-class`. The current row must be `advisory-p2` with no `repeat of`.
- The second half guards against over-correction: with a real earlier review `t-a01-local-review-aaaaaa1.md` and the row `local:aaaaaa1:1<TAB>quoting`, the repeat still takes `quoting`.
- On origin/main's script the test fails with the audit's symptom (`unrelated-class`, validation §2); after the fix it passes.

## Results

- `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`: 18 tests OK (validation §4).
- `shellcheck`, `shfmt -i 4 -sr -d` and Ruff on the test module are clean (validation §5).
- Caps (`git diff --numstat origin/main`, validation §5): 4 changed lines outside `tests/` and `.orchestration/` (<= 200); 23 added under `tests/` (<= 1000).
- `task_copy=b1b9cea0cc5ae47361fb6fef9d9c6f4c6d431e87ab61b85a122121eb736e15b6`.

## Under the night's ask rules (the operator's notice of 01:1x JST)

The branch is pushed. `gh pr create` is a gh write that now prompts a human, so the seat stops there with `AGMSG-PONG v1 status=blocked` naming the exact command, and does not run it or route around it. The PR, `gh pr ready`, CI and the Bot wait follow the morning's approval, and the RESULT names them then. The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
