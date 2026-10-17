---
task_id: dotfiles-T129-assets-omp-hcom-followup-a01
seat: claude-standard-dot-a007
branch: tools/assets-hcom-receipt
base: b49da6dd3c9e9a93301af4c0d3dd62b058852abf (PR #388's head; the branch rebases onto origin/main after #388 merges)
task_sha256: abd85d3295bfc03b738c765409aaea695ce51c8cb4f9ebbc758eddad5f398777
code_commit: ad57e280104e71069352e128a2758551b7ca6316
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a01

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on `tools/assets-hcom-receipt` from PR #388's head b49da6dd. The task says no PR opens before the rebase onto origin/main after #388 merges. The PR #389, #396 and #386 branches stay in the worktree, committed and pushed.
- Task file: sha256 `abd85d32…`, copied byte-identical; the task-consistency check passes (validation §1). No question and no amendment.
- The owned row, read from the record at dispatch: `local:b49da6d:1` (PR #388's local review, `scripts/update-agent-assets.sh:989`, class install-receipt-artifact).

## The change (validation §2: 8 added and 3 deleted in the script, 19 and 4 in the test)

- `update_hcom` downloads and verifies the wheel in a temporary directory as before. After the hash check, the verified wheel now moves to `~/.local/share/agent-assets/hcom/<wheel name>`, a managed path outside the run, and uv installs it from there.
- uv's receipt records that path as hcom's source, and `uv tool upgrade --all` (`scripts/upgrade-tools.sh`) re-reads it. Before this change the EXIT trap removed the wheel with its directory.
- The asset manifest's `update_hcom` step lists the wheel beside the binary, so `remove-agent-asset` reverses it too.
- A wheel that fails its hash never leaves the temporary directory. omp's tarball still goes with its run.
- The directory follows the `~/.local/share/<name>/` form of the terminal-browser install, named after the updater (`agent-assets`), so it is neither hcom's nor uv's own state.

## Test

- `test_update_hcom_keeps_the_wheel_uv_records_as_its_source`, plus the shared `exercise_update`, which every hcom case runs on four platforms and with a shadowed PATH. For hcom it now asserts:
  - the wheel uv installs is under the managed path and holds the pinned hash;
  - the manifest's paths are the binary and the wheel;
  - after a hash mismatch the managed path holds no wheel;
  - after a version mismatch the installed wheel is still there.

  The omp branch keeps its old assertions.
- Red on b49da6dd's script: seven hcom cases fail, omp's pass (validation §3).
- Three mutants each fail the test (validation §4): the wheel copied and uv installing the temporary file, the manifest leaving the wheel out, and the wheel moved before its hash check.

## Results and their environment

- The Check's three modules, `test_update_agent_assets`, `test_asset_manifest` and `test_runtime_health`, run 71 tests (validation §5).
  - All of the updater and manifest tests pass.
  - Eight agmsg tests in `test_runtime_health` fail in this Claude macOS sandbox. They fail identically on b49da6dd's script: §5 pastes the baseline run, and the failing sets match.
  - The cause is that macOS `mktemp` without a template ignores TMPDIR and the sandbox denies its default directory. These tests set PATH to `{bin}:/usr/bin:/bin`, so no shim reaches them.
  - CI's Linux runners are the authority for them, and nothing in this change touches agmsg.
- For the updater tests, an evidence-run `mktemp` shim (pasted in the validation file, not in the repository) gives the two template-less forms a TMPDIR template, and the same tests then run in the sandbox.
- `shellcheck -x scripts/update-agent-assets.sh` (as CI runs it), `shfmt -i 4 -sr -d` and Ruff on the test module are clean (validation §6).

## Limits

- An older pinned wheel left in the managed directory after a pin change is not removed. Only the current one is referenced by uv's receipt and the manifest.

## Caps and what follows

- Against b49da6dd: 11 changed lines outside `tests/` and `.orchestration/` (<= 120); 19 added under `tests/` (<= 400). The caps against origin/main are pasted after the rebase.
- `task_copy=abd85d3295bfc03b738c765409aaea695ce51c8cb4f9ebbc758eddad5f398777`.
- After #388 merges: rebase onto origin/main, re-run the Check, open the PR, CI and the Bot wait, then the RESULT. The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
