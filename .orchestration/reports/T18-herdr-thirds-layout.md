# T18 worker report

## Status

Merged, deployed, and live-repaired.

- Head: `dc79fce6bdf8b8498178dac920af7ff520ecc831`
- Squash merge: `680d65f802ec1e55c3027c8c37a1b24ed758ec9a`
- Commits:
  - `ec3526cc8c421f6a7a203f3057d880dc1ec4daa7`
  - `dc79fce6bdf8b8498178dac920af7ff520ecc831`
- PR: https://github.com/mryfmo/dotfiles/pull/78
- GitHub Actions and CodeRabbit: all executed checks passed at the final head;
  the change-filtered Nix job was skipped as expected.
- Deployed target: `~/.local/bin/common/herdr-agents`
- Operator workspace `w13`: `35/34/103` repaired to `57/57/58`
  (`claude-orchestrator | codex-worker | files`) without restarting any pane
  process.

## Changes

- Changed every files-pane split ratio from the old 40/40/20 values to
  `0.667`, producing equal-width `Claude | Codex | files` panes with files at
  the far right.
- Added attach-time ratio repair after order repair.
- Ratio repair accepts only a validated horizontal three-pane layout with two
  right splits and one recognized nested topology. Unknown, ambiguous, failed,
  or nonnumeric layouts are left untouched with a refusal warning.
- Both Herdr topologies observed in practice are supported:
  `((Claude | Codex) | files)` and `(Claude | (Codex | files))`.
- The same safe repair is reused after full mode adds a missing files pane, so
  an existing 50/50 Claude/Codex workspace does not remain 50/33/17.
- Added fake-CLI coverage for equal widths, both skewed topologies, failed
  layout queries, nonnumeric rects, and unsupported split geometry.

## Validation summary

- `python3 -m unittest tests.unit.test_herdr_agents`: 49 tests passed.
- `shellcheck home/dot_local/bin/common/executable_herdr-agents`: passed.
- `bash -n home/dot_local/bin/common/executable_herdr-agents`: passed.
- Fresh scratch E2E: widths `58/57/57`; order
  `claude-orchestrator | codex-worker | files`; Yazi became the foreground
  process in the files pane.
- Persisted scratch E2E: deliberately skewed `86/43/43` layout converged to
  `57/57/58` through the real `--attach` path while preserving order and Yazi.
- Existing-workspace scratch E2E: deleting files produced `86/86`; full-mode
  repair recreated files and converged to `57/57/58` with Yazi.
- Scratch Herdr workspaces and directories were removed.
- GitHub Actions passed on macOS client, Ubuntu client/server, bootstrap
  validation, and agent-asset validation jobs.

## Automated review follow-up

The GitHub Codex review identified that changing the existing-workspace split
ratio alone would turn a common 50/50 workspace into about 50/33/17. Added a
regression test, reused ratio repair after the missing files pane is created,
and verified the exact path live before the follow-up push.

## Deliberate scope

No dependency, Makefile, CI, hook, permission, or operator live-workspace
change was made before acceptance. After acceptance, the orchestrator
explicitly authorized deployment and ratio-only repair of operator workspace
`w13`. Local Bats and `make require-crit-review` were not run.

## Deployment result

- PR #78 was squash-merged as
  `680d65f802ec1e55c3027c8c37a1b24ed758ec9a`.
- Main fast-forwarded cleanly while preserving unrelated dirty files through
  Git autostash.
- A targeted `chezmoi apply` deployed only
  `~/.local/bin/common/herdr-agents`; the deployed file matched merged source
  and contained `repair_attach_pane_ratio`.
- The deployed `herdr-agents --attach` repaired `w13` from widths
  `35/34/103` to `57/57/58`.
- Final order is `claude-orchestrator | codex-worker | files`; all widths are
  within two columns of one third.
- Claude PID `98094`, Codex PIDs `98164`/`98188`, and Yazi PID `6955` were
  unchanged before and after repair. No pane was closed or restarted.
- Task worktree `/private/tmp/dotfiles-t18`, local branch
  `feat/herdr-thirds-layout`, and the corresponding remote branch were
  removed after deployment.
