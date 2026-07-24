# T22 Doctor Settings Idempotency Report

## Result

- Status: completed
- Pull request: https://github.com/mryfmo/dotfiles/pull/89
- Branch: `fix/doctor-settings-idempotency`
- Commit: `7c20c5c4cf69aa47f972db1e9c92f143c6654507`
- Merge commit: `92faa35652adb76afb65bb71f92f8d6c813438d2`
- Main synchronized: yes, fast-forward only

## Fix

- Claude hook sections keep the current key order.
- Existing hook entries keep their current relative order and serialization;
  only missing managed entries are appended.
- Managed values still win for non-runtime managed settings.
- The runtime doctor compares modifier output semantically only for Claude
  JSON; Codex/TOML and other modified targets remain byte-exact.
- Real model drift remains a failure.

## Validation

- Focused red phase reproduced hook-order replacement and missing semantic mode.
- Focused green phase: 22 tests passed.
- Full unit suite: 184 tests passed.
- Two live `make update` cycles: both exit 0.
- Both live doctor runs: no Claude settings managed-key drift.
- Known pre-existing `agmsg/db-flue-pi` runtime-state error remained the only
  doctor error and was not changed.
- Crit-data review gate passed with one resolved approval record.
- CI:
  - Agent assets: https://github.com/mryfmo/dotfiles/actions/runs/29983450259
  - Unit test: https://github.com/mryfmo/dotfiles/actions/runs/29983450248
  - Snippet install: https://github.com/mryfmo/dotfiles/actions/runs/29983450218
  - CodeRabbit: success

## Decisions

- `gh` was used first for repository, PR, diff, and CI inspection; web fallback
  was not needed.
- The implementation reuses Python dictionary/list equality and adds no
  dependency or general merge framework.
- The PR has one commit and received no post-creation commit, so its English
  description already represents the full PR.
- Local bats, `make upgrade`, and force push were not performed.

## After acceptance

- Acceptance: `status=accepted`, `next_action=merge`.
- PR #89 was squash-merged at
  `92faa35652adb76afb65bb71f92f8d6c813438d2`.
- The required four-file parity guard failed after fetching `origin/main`.
  Local main contains the pre-T22 versions while `origin/main` contains the
  accepted T22 changes.
- Per the task's explicit stop condition, local main was not reset and the
  task worktree and topic branch were not removed.
- Final worker status: blocked pending a revised synchronization instruction
  that is safe for a clean pre-T22 main worktree.

## Revised synchronization completion

- Revised acceptance confirmed the original stop was correct and replaced the
  dirty-tree parity condition with a clean-tracked-tree fast-forward.
- Main had no tracked changes and fast-forwarded from `c1bfdbd` to
  `92faa35652adb76afb65bb71f92f8d6c813438d2`.
- Main `HEAD` equals `origin/main`; tracked status is clean.
- The T22 worktree and local `fix/doctor-settings-idempotency` branch were
  removed.
- Two additional `make update` runs exited 0.
- Both subsequent doctor runs reported only the known `agmsg/db-flue-pi`
  runtime-state error and no Claude settings managed-key drift.
- Final worker status: ready for review.
