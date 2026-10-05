# Acceptance: dotfiles-T99-nix-plans-history-a01

- **Decision:** ACCEPTED. PR #277 squash-merged to `main` as `64167825`; head `43eeb915`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 06:47Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8). task_rev verified at dispatch (06:10Z); one commit, no revise round.
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (seven artifact files copied from worker-e into the main checkout).
- **Plan reference:** follow-up to T78/T83 (Nix plans kept in place during T83 because `tests/unit/test_aws_cli_acquisition.py` pins them by path).

## What was accepted (PR #277, head `43eeb9153f54de4a03614b7edb4c6b606f312509`, one commit on main 794a80db; 5 files, +11/−3)

- `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` moved with `git mv` to `docs/history/`, each with the one-line historical header naming the move (T99) and the test that pins the AWS CLI ownership statements; `docs/plans/` no longer exists.
- `docs/history/README.md`: two sentences (historical design documents; nothing in it is a current plan).
- `plans/004-harden-and-lock-the-supply-chain.md`: drift-check path repointed; `plans/004` and `plans/README.md` otherwise unchanged (the plans index keeps its numbering).
- `tests/unit/test_aws_cli_acquisition.py`: reads the two files at the new paths; the pinned statements are unchanged (10 focused tests, 865 unit tests pass; CI 13/13).
- MkDocs/docs workflow have no nav entry for the moved files (worker check); the only remaining old-path references are archived `.orchestration` evidence and `.ua` graph records, as the task allows.

## Orchestrator re-derivation

- Read the whole diff (renames with `-M`, README, plans/004 hunk, test hunk) and the moved files' first lines at the head; `git ls-tree 43eeb915 docs/plans` is empty.
- No Bot review on the head after the worker's wait (06:25:50Z–06:41:17Z); zero review threads; mergeable `clean`.
- The task's prettier command omitted the executable after `--`; the worker corrected it to `mise x node npm:prettier -- prettier --check …` (passes) and reported the deviation. Orchestrator note for future task files.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 43eeb915 | correct → no findings; auditor confirmed allowed files, unchanged document bodies and ownership assertions, no live old-path references, all seven artifacts, 10 focused + 865 unit tests, 12 CI checks, dispositions complete |

- Sweep (head 43eeb915): `.orchestration/validation/dotfiles-T99-nix-plans-history-a01-pr-feedback.json`, 5 items, all `not-applicable` (CodeRabbit summary comment and skipped status, 3 macOS capacity notices).
- Crit evidence `…-crit.json` (one resolved review-scope record) and receipt `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` copied from worker-e.

## CompactionDB

- Worker decision: none (Codex seat). Orchestrator consolidation `360a6b92-402c-4a3d-8e72-40e9cc8156f8`.
