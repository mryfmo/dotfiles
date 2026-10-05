# Acceptance: dotfiles-T100-compactiondb-claude-symlink-note-a01

- **Decision:** ACCEPTED. PR #278 squash-merged to `main` as `94409ec4`; head `bc001fc7`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 07:24Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8). task_rev verified at dispatch (06:48Z).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (artifact copies from worker-e).
- **Plan reference:** follow-up to T81b (orchestrator review observation: `ensure()` refuses a symlinked `.claude` and the hooks then fail silently).

## What is under acceptance (PR #278, head `bc001fc74e672b599daf7e8a7777cd7f4e2fab7f`, one commit on main 64167825; 4 files, +19/−6)

- `vendor/compactiondb/CHANGELOG.md`: one line under `2.0.0+dotfiles.9` (no version bump; .9 is the current unreleased pin).
- `vendor/compactiondb/README.md` ("Storage directory safety"): the project's `.claude` must be a real directory; a symlinked `.claude` or storage directory is refused, the SessionEnd and compaction hooks then record nothing (no health log); remedy named.
- `vendor/compactiondb/tests/test_paths.py`: `test_storage_tree_refuses_existing_symlinks` covers `.claude` itself and the five storage directories relative to the project root; link target untouched.
- `MANIFEST.sha256` regenerated; no runtime change, project copy unaffected.

## Orchestrator re-derivation

- Read the whole diff; traced `ProjectPaths.ensure()` for the `.claude` case (`FileExistsError` on `mkdir` with `dir_fd`, then `ELOOP` from the `O_NOFOLLOW` open).
- Worker: 7 path tests and 108 vendor tests from both entry points, manifest check, assets validation and prettier pass; independent review approved.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, head bc001fc7 | correct → no findings; auditor confirmed the four allowed files, seven artifacts, unchanged runtime and version, test coverage of `.claude` with target contents and permissions preserved, 69 manifest hashes, 12 CI check runs, timestamped Bot wait |

- Sweep (head bc001fc7): `.orchestration/validation/dotfiles-T100-compactiondb-claude-symlink-note-a01-pr-feedback.json`, 5 items, all `not-applicable` (CodeRabbit summary comment and skipped status, 3 macOS capacity notices). Crit evidence `…-crit.json` and receipt `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md` copied from worker-e.

## CompactionDB

- Worker decision: none (Codex seat). Orchestrator consolidation `3e056467-b971-4a66-989b-3b4042311804`.
