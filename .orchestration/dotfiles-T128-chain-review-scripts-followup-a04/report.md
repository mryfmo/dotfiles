---
task_id: dotfiles-T128-chain-review-scripts-followup-a04
seat: claude-standard-dot-a007
branch: tools/chain-review-scripts-followup-a04
base: a0e8b8ad54e90f685710f114b38d48105c3dc7e1
task_sha256: d318b1ccc14d742ec51ce5c54821930d13accf600cb6ef80784b24ba45f1f078
---

# Report: dotfiles-T128-chain-review-scripts-followup-a04

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on a fresh branch `tools/chain-review-scripts-followup-a04` from `origin/main` `a0e8b8ad` (boundary (17), PR #384; the lineage's PR #381 merged as `58303c37`). The PR #375 branch stays in the worktree, committed and pushed, until its acceptance.
- Task file: sha256 `d318b1cc…`, copied byte-identical to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a04/task.md`; the task-consistency check passes on the dispatched file and both premises replay `present` (validation §1, §2). No question and no amendment.
- The owned rows, read from `origin/main` (validation §2): `audit:d3e8acf:1` and `audit:d3e8acf:2`, both `advisory-p2`, under `## Owned by dotfiles-T128-chain-review-scripts-followup-a04` in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a03.md`.

## Row 1: audit:d3e8acf:1 (the historical suffixes enter grep -E unescaped)

The audit of d3e8acf, finding 1: an earlier local review file named `t-a01-local-review-.*.md` made its id `local:.*:1` a pattern, so the repeat classing took the class and provenance of an unrelated `local:*:1` row. `scripts/orchestrator/local-advisory.sh` now does both things the row names (validation §5):

- **Seven-hex suffix:** in the loop over the task's earlier local review files, a file whose suffix after `-local-review-` is not `[0-9a-f]{7}` is skipped, so it names no earlier finding.
- **Literal id:** the earlier row is found by comparing each record line's first tab-separated field with the ids as text (`awk -F'\t'`, `$1 in s`), not through the `grep -E "^(…)\t"` alternation. Rows classed `advisory-p2` are still skipped and the last match still wins.
- The shdoc description names both. Nothing else changes: the P0/P1 stop, the heading, the owner check, the row and `local-finding:` forms, and the once-only writes are as on `origin/main`.

Test: `test_local_advisory_matches_an_earlier_review_id_literally`. There are two earlier files, `t-a01-local-review-.*.md` (the audit's reproduction) and `t-a01-local-review-notes.md` (a suffix that is not a head), each holding the same token as the current finding. The record has a `local:notes:1` and a `local:aaaaaa1:1` row with other classes. The current row must be `advisory-p2`, with no `repeat of`.

- Before the fix (origin/main's script) the test fails with `unrelated-class`, which is the audit's symptom (validation §6; the first draft of the test, with only the `.*` file, failed the same way, §4).
- After the fix it passes (§7).
- Mutation check (§6): with the seven-hex check removed, the test fails with `notes-class`, so that half is tested. With the literal match reverted to `grep -E`, it passes. That mutant survives by construction: the seven-hex check runs first and admits only `[0-9a-f]{7}`, so no id that reaches the match can hold a metacharacter. The literal match is kept because the row names it, as defence in depth.

## Row 2: audit:d3e8acf:2, the classing half (report-only)

The audit's finding 2: the class propagation of PR #381 is complete only once the consumers read the local rows. This owner keeps the row's form stable. This PR leaves both written forms as they are: `local:<sha7>:<n><TAB><class>` and the `local-finding: <sha7>:<n> not-applicable:advisory P2 owned by <owner> (…[; repeat of local:<sha7>:<n>]); evidence=shasum -a 256 .orchestration/tasks/<owner>.md (<sha256>)` line (the two `printf` lines are untouched, validation §5). `test_local_advisory_classes_a_repeat_by_the_earlier_row`, unchanged, pins the form and passes (§7). The consumer rows, both `audit:d3e8acf:2<TAB>consumer-half` on `origin/main` (validation §3):

- `.orchestration/acceptance/dotfiles-T128-chain-glue-integrate-a01.md`, under `## Owned by dotfiles-T128-chain-glue-integrate-followup-a01`: `chain-integrate.sh`'s ledger TSV keeps only thread ids and `audit:<sha7>:<n>` rows, so the `local:` rows never reach the JSON block the S6 and S1 checks read. That owner carries them into the TSV.
- `.orchestration/acceptance/dotfiles-T128-s1-replan-gate-a01.md`, under `## Owned by dotfiles-T128-s1-replan-gate-followup-a01`: `require-crit-review.py`'s `LEDGER_ID` rejects `local:<sha7>:<n>` ids. That owner widens it to the local form.

## Tests, checks and caps

- `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v`: 17 tests OK, the new one included; the other 16 are unchanged (validation §7).
- `shellcheck` and `bash -n` on `local-advisory.sh`: exit 0 (§7). CI's format checks run locally: `shfmt -i 4 -sr -d`, `ruff format --check` and `ruff check` all exit 0 (§8).
- Caps (`git diff --numstat origin/main...HEAD`, validation §9): outside `tests/` and `.orchestration/`, 7 + 3 = 10 changed lines (<= 200); under `tests/`, 20 added (<= 1000).
- `task_copy=d318b1ccc14d742ec51ce5c54821930d13accf600cb6ef80784b24ba45f1f078`.

## Not in this commit

- This report and the validation are committed with the code, in the PR's one commit, before the PR opens. CI, the Bot's review of the head and every Bot thread with its proposed disposition come after this commit, so the RESULT names them. Any P0/P1 fix round is recorded in a later commit.
- The worker replies to and resolves no thread, and does not merge. The local review, the sweep, the audit, the gate and the merge are the orchestrator's.
- No new durable decision was made, so no CompactionDB memory was added. The learning candidates are in learning.md, not promoted. AutoSkill was not used. The Understand-Anything graph was not touched (no hook prompt fired).

cost: n/a
