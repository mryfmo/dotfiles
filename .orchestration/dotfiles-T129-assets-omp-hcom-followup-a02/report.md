---
task_id: dotfiles-T129-assets-omp-hcom-followup-a02
seat: claude-standard-dot-a007
branch: tools/assets-hcom-followup-a02
base: 2b91aef95161bf1e38755a2b233094b30dca80c1 (PR #398's head; the branch rebases onto origin/main after #398 merges)
task_sha256: adef9ddfc4d3458c85340a73aca9954f2ad8210982bc868171dbd68a2d65ee76
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a02

- Seat: `claude-standard-dot-a007` in `.claude/worktrees/worker-c`, on `tools/assets-hcom-followup-a02` stacked on PR #398's head 2b91aef9 (the dispatch note: the files are shared and #398 has not merged; the branch rebases onto origin/main after it does).
- Task file: sha256 `adef9ddf…`, copied byte-identical; the task-consistency check passes (validation §1). No question and no amendment.
- The three owned rows, read from the records at dispatch (validation §1): 4303212235 (uninstall-leaves-tool-env), 4303338055 (install-receipt-repair), and local:fbbc6d9:1 (omp-non-npm-entry, re-owned from the T130 record).
- Record note: the T130 record's re-own line says local:fbbc6d9:1 and :2 were "fixed in PR #398 by 457984c9 and 1537863d". That holds for :2 (the kept wheel). :1, the omp entry, was not touched by #398 and is fixed here.

## Row 4303212235: `remove-agent-asset update_hcom` (validation §2)

- **Before:** the Bot read the removal as deleting the binary and the wheel but not uv's tool environment. On 2b91aef9 it actually removed nothing: both recorded paths, `~/.local/bin/hcom` and the kept wheel, lie outside the remover's fixed safe roots, so the preflight refused the step. The red run shows `refusing path outside allowed asset roots` (validation §3).
- **The removal now:**
  - `remove_hcom` runs `uv tool uninstall hcom` through the remover's `run_operation`, so a dry run prints it. uv owns the tool environment, the receipt and the `~/.local/bin/hcom` entry point it created.
  - It then deletes the other recorded paths, the wheel the updater kept for uv's receipt, through the existing guarded `remove_recorded_paths`.
  - `~/.local/share/agent-assets` joins the fixed safe roots: it is the updater's own managed directory, and the guard still requires a path to sit under a recorded prefix.
  - Without uv, the step fails with `uv is not installed, … nothing was removed` and the manifest entry stays (the row's "reports when it is not").
- **Test:** `test_hcom_removal_uninstalls_the_uv_tool_before_the_kept_wheel`, which covers the missing uv, a dry run that runs nothing, and the `--yes` removal.

## Row 4303338055: a failed install drops the kept wheel (validation §2)

- **The change:** when `uv tool install --force` fails after the verified wheel moved into place, `update_hcom` removes the wheel and returns 1. The next run then finds the pinned binary without its wheel and reinstalls, instead of skipping on the wheel.
- **Test:** `test_update_hcom_drops_the_kept_wheel_when_the_install_fails`. The failed run leaves no wheel; the next run downloads, installs and keeps it.

## Row local:fbbc6d9:1: an existing non-npm omp entry (validation §2)

- **The problem:** npm refuses to replace a bin entry it does not own (EEXIST), so a standalone `~/.local/bin/omp`, an external link or a dangling one aborted the update before hcom and the remaining assets.
- **The change:** after the hash check, such an entry moves aside into the run's temporary directory. An entry counts as npm's own when it is a link into `lib/node_modules/@oh-my-pi/pi-coding-agent/`. If the install fails or does not end at the pin, npm's entry is removed and the old one is put back. On success the old entry goes with the temporary directory, replaced by the pinned binary.
- **Test:** `test_update_omp_moves_a_non_npm_entry_aside_and_restores_it_on_failure`, for a standalone file, an external link and a dangling link. A drifted version restores the entry exactly; the pinned version leaves npm's link and the external target untouched.
- **The shared stub:** the fake npm now behaves like npm. It links its bin entry into the package and refuses an entry it does not own, so `test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin`, whose reset writes a standalone omp, covers the migration too. The fixture overwrote such an entry before, which is how the review says the failure was missed.

## Results

- Red on 2b91aef9's two scripts: the four row tests fail six subtests (validation §3).
- Six mutants each fail a test (validation §4): no `uv tool uninstall`, the agent-assets root not safe, no uv check, the wheel kept after a failed install, no restore, and a dangling link not treated as an entry.
- `test_remove_agent_asset.py` and `test_update_agent_assets.py` run 23 tests OK (validation §5). The updater tests run with the evidence-run `mktemp` shim of the a01 task, because macOS `mktemp` without a template fails in this sandbox.
- `shellcheck -x` and `shfmt -i 4 -sr -d` on both scripts are clean. Ruff adds no finding; the two on `test_remove_agent_asset.py` are on 2b91aef9 too (validation §6).
- `make validate-agent-assets` exits 0 (validation §7).

## Caps and what follows

- Against 2b91aef9: 56 changed lines outside `tests/` and `.orchestration/` (28 in the remover, 28 in the updater; <= 120); 142 added under `tests/` (<= 400).
- `task_copy=adef9ddfc4d3458c85340a73aca9954f2ad8210982bc868171dbd68a2d65ee76`.
- Under the night's ask rules the branch is pushed and the seat stops at `gh pr create` with `AGMSG-PONG v1 status=blocked` naming the command. After #398 merges: rebase onto origin/main, re-run the Check, then, with the morning's approval, the PR, `gh pr ready`, CI and the Bot wait, then the RESULT.
- The worker replies to and resolves no thread, and does not merge. No new durable decision was made, so no CompactionDB memory was added. AutoSkill was not used. The Understand-Anything graph was not touched.

cost: n/a
