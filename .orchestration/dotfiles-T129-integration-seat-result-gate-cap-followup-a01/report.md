---
task_id: dotfiles-T129-integration-seat-result-gate-cap-followup-a01
seat: claude-standard-dot-a007
branch: tools/integration-seat-review-body-findings
base: 087516f51b8de9ccff42a0a748c34e913af9c8d9 (PR #393's head; the branch rebases onto origin/main after #393 merges)
task_sha256: 41374b642fbee60caa431e5a73f1d413d4e7744f3941ec71ec775a0b0cde10ad
---

# Report: dotfiles-T129-integration-seat-result-gate-cap-followup-a01

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on `tools/integration-seat-review-body-findings` stacked on PR #393's head 087516f5 (code fa14b374), as the dispatch note says; it rebases onto origin/main after #393 merges.
- Task file: sha256 `41374b64…`, copied byte-identical; the task-consistency check passes (validation §1). No question and no amendment.
- The owned row: `4302959629` (class review-body-findings), the Bot's P2 on PR #393's head 3baa0003.

## The change in `scripts/orchestrator/result-precheck.sh` (validation §2: 9 added, 3 deleted)

- **The review bodies:** check (g) now also lists the Bot's reviews. A review body with a `P0` to `P3` badge is a finding named `review-<id>` and carries the body's top badge. The report must hold it as `review-<id>:<P>:<disposition>`, the form `integrate-seat.sh` already parses and the Message Contract's `open:review-<id>` names, under the same rule as an inline thread: a P0/P1 needs `fixed:<sha7>` or `open:`. A review body without a badge names no finding.
- **Scope:** the reviews are read on every head, as the inline comments already are, so a review-body finding of an earlier head still needs its disposition.
- **The left boundary:** the report token is now matched with a left boundary (`(^|[^0-9-])`). Before, an inline thread id was satisfied by the same digits inside `review-<id>` or a longer number. That matters now that both token kinds share one report.
- The header's (g) clause names the review bodies. Nothing else changes; `integrate-seat.sh` is untouched.

## Test

- `test_result_precheck_reads_the_bot_review_bodies_as_findings`. The Bot's reviews of the head are:
  - one without a body;
  - one with a P1 badge;
  - one with a header and no badge;
  - one with a P2 and a P1 badge, whose token is P1.
- (g) is `missing` without the P1 review's token or with only a `proposed` disposition for it, and `ok` with `fixed:` or `open:`.
- (g) is `missing` when the inline thread 4300000001 is present only as `review-4300000001`.
- The receipt lists `review-5550000001 P1` and `review-5550000003 P1`, and neither the badge-less review nor the body-less one.

## Results

- Red on 087516f5's script: five subtests fail (validation §3). The script saw no review body, and it accepted the `review-4300000001` collision.
- Three mutants each fail the test (validation §5): no review bodies read, the first badge instead of the top one, and no left boundary.
- `uv run python -m unittest tests/unit/test_integration_seat.py -v`: 7 tests OK (validation §4).
- `shellcheck` on both scripts, `shfmt` and Ruff are clean (validation §6).
- Caps against 087516f5: 12 changed lines outside `tests/` and `.orchestration/` (<= 120); 37 added under `tests/` (<= 400).
- `task_copy=41374b642fbee60caa431e5a73f1d413d4e7744f3941ec71ec775a0b0cde10ad`.

## Under the night's ask rules

The branch is pushed and the seat stops at `gh pr create` with `AGMSG-PONG v1 status=blocked` naming the command. After #393 merges: rebase onto origin/main, re-run the Check, then, with the morning's approval, the PR, `gh pr ready`, CI and the Bot wait, then the RESULT. The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
