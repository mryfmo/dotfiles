# Report: dotfiles-T98c-claude-seat-artifact-write-exception-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `docs/claude-seat-artifact-write-exception` from `origin/main` 7f5b9b9d with `--no-track`.
- **task_rev:** `sha256:ba7cc063…6e5eca0cd`, matched in the main checkout.
- **PR:** #281, https://github.com/mryfmo/dotfiles/pull/281.
- **Commit and head:** `d1751647`. CI, the Bot wait and `mergeable_state` are in the validation file.
- **CI and Bot:** CI is green and `mergeable_state` is `clean`. Bot: no review; the Codex quota notice (issue comment, 2026-10-05T09:54:09Z; the 09:54:14Z comment is CodeRabbit's) ended the wait at its first poll (10:04:11Z).
- **Status:** ready_for_review.

## What changed

1. **SKILL Worker Playbook step 4:** "Two documented cases" becomes "Three documented cases". The new middle case is "writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, through the permission gate because the main checkout is not writable from a worktree sandbox", between the CompactionDB `memory add` and `agmsg-dispatch`. "Every other out-of-sandbox action stays a blocked PONG" is unchanged.
2. **Step 5:** "Write artifacts to the exact expected paths (a Claude seat writes them through the permission gate, step 4)." The Codex-seat convention that follows (write in the worktree, the orchestrator moves them) is unchanged.
3. **Docs test:** `test_skill_carries_the_session_lessons` pins both sentences.

The rule file is unedited (429 words), and no other file changed.

- **Checks:** the docs test (15 tests) passes, `make unit-test` (876) passes, `make validate-agent-assets` passes, and prettier is clean.
- **Process:** these five artifacts were written and masked through the permission gate: the exception this task documents.

cost: n/a

[memory:decision] dotfiles-T98c (orchestrator 2026-10-05): a Claude worker seat writes and masks its main-checkout artifacts through the permission gate as a documented Worker Playbook step 4 exception, the same class as the CompactionDB memory add.
