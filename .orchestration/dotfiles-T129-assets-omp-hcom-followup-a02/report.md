---
task_id: dotfiles-T129-assets-omp-hcom-followup-a02
seat: claude-standard-dot-a008
branch: tools/assets-omp-hcom-followup-a02
base: de3b73cc
pr: 416
test_commit: 0bf9469e
fix_commit: b387d3f1
review_test_commit: 91653681
review_fix_commit: 5f1f3846
rereview_test_commit: c47f5c7a
rereview_fix_commit: 8ea9bf8a
task_sha256: 4d2f30139cf6a4a738c6b5b6ef05d1574d083a5dc39a53c09f5dae34f4761bb5
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a02

- Seat: `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. AGMSG-TASK arrived at 2026-10-18T11:18:07Z with `task_sha256=4d2f3013…`. The dispatched file and the branch copy `task.md` match it byte for byte (validation §1), and the task-consistency check passes on it (§1a).
- Branch: a fresh `tools/assets-omp-hcom-followup-a02`, made with `git switch -c … --no-track origin/main` at `de3b73cc`, as the TASK note asks. The lint branch of PR #415 is untouched.
- Owned rows, read from the records at dispatch:
  - `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md` gives 4303212235 (uninstall-leaves-tool-env), 4303338055 (install-receipt-repair), local:fbbc6d9:1 (omp-non-npm-entry, re-owned from the T130 record), local:9842d91:1 and audit:9842d91:1 (the same defect as 4303338055), and audit:9842d91:2 (records-form; its code part is the task's Scope note).
  - The two Bot comments were read with `gh api repos/mryfmo/dotfiles/pulls/comments/<id>`. The text of local:fbbc6d9:1 comes from `.orchestration/validation/dotfiles-T130-claude-sandbox-integration-a01-local-review-fbbc6d9.md`.
- Prior art: a007's branch `tools/assets-hcom-followup-a02` (04abf29c, on PR #398's head 2b91aef9, from before the Scope note and before #405) fixed the same three rows. The record names it at 17:04Z. I read it. This branch starts again from `origin/main`, as the TASK note asks, and covers the Scope note's four paths and #405's omp code.

## The owned rows

| Row | Change | Tests (red and green: validation §3, §3a, §3b, §4, §8, §8a, §9) |
|---|---|---|
| 4303212235 and the Scope note (audit:9842d91:2) | `remove-agent-asset update_hcom` runs `uv tool uninstall hcom`, which removes uv's tool environment and its receipt. It then deletes the recorded binary `~/.local/bin/hcom` and the retained wheel under `~/.local/share/agent-assets/hcom/`. `~/.local/share/agent-assets` (strict descendants) and the exact path `~/.local/bin/hcom` join the safe roots, and every path still has to lie under a recorded manifest prefix and pass the preflight before uv runs. When `uv tool dir --color never` has no `hcom`, the uninstall is skipped with a SKIP line and the rest is removed. Only `--yes` requires uv; without it the step reports and removes nothing, so the manifest step stays. | `test_hcom_removal_deletes_the_recorded_binary`, `…_deletes_the_retained_wheel`, `…_uninstalls_the_uv_tool_environment`, `…_uninstalls_the_uv_receipt`, `…_without_uv_reports_and_removes_nothing`, `…_skips_the_uninstall_when_uv_has_no_hcom_and_removes_the_rest`, `test_hcom_dry_run_without_uv_prints_the_plan` |
| 4303338055, local:9842d91:1, audit:9842d91:1 | `update_hcom`: a failed `uv tool install --force` deletes the retained wheel and returns 1, so the skip guard (version at the pin and the wheel present) cannot pass on it, and the next run downloads and installs again | `test_update_hcom_drops_the_retained_wheel_when_uv_fails_so_the_next_run_retries` |
| local:fbbc6d9:1 | `update_omp`: a `~/.local/bin/omp` that npm does not own (a standalone file, a link outside this prefix's package, or a dangling link) moves to `~/.local/share/agent-assets/omp/omp.previous`, and the output names it. It comes back when the install does not end at the pin. npm's own link (`../lib/node_modules/@oh-my-pi/pi-coding-agent/…` or the same path in absolute form) and a directory stay for npm to judge, which is #405's contract. This generalises #405's dangling-link removal. | `test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails` (dangling, external, foreign, file, npm, directory, none; at the pin and at a wrong version) |

- The fixture npm now links its own bin into `lib/node_modules/@oh-my-pi/pi-coding-agent/` and, like npm, refuses with EEXIST any entry it does not own. The earlier fixture overwrote such entries, which is how the failure stayed hidden (the finding's own words). With the faithful fixture, `test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin` is red at the tests commit (its reset leaves a standalone file at the omp path) and green after the fix.
- The hcom repair test (4303212227, #398) and the new retry test share one helper, `update_pinned_hcom`. Every assertion of the repair test is kept.
- The test that replaced #405's dangling-only test keeps #405's assertion that a link's former target is printed.

## Worker review (three rounds; the record and the receipt name every finding)

An independent read-only reviewer was used: a fresh general-purpose subagent of this seat, given the task file, the three findings and the commit range, but not my conclusions.

1. Round 1 on `de3b73cc..b387d3f1` returned `Verdict: correct` with two P2 and three P3. All five were fixed in 5f1f3846, with tests in 91653681 that are red at b387d3f1 (§3a, §8a):
   - The uninstall stopped when uv no longer had hcom.
   - The moved omp entry was deleted with the temporary directory, including on SIGTERM, and a directory got moved.
   - The npm-owned glob was looser than npm's own rule.
   - A dry run without uv printed no plan.
   - #405's printed-target assertion had been dropped.
2. Round 2 on `b387d3f1..5f1f3846` returned `Verdict: incorrect` with one P1 and two P3.
   - The P1: `uv tool dir` was read with colour on. herdr-agents exports `FORCE_COLOR` and `CLICOLOR_FORCE`, so uv wrapped the path in colour codes, the hcom check never matched, and `--yes` left uv's environment and receipt behind.
   - Fixed in 8ea9bf8a with `uv tool dir --color never`, the remedy #405 applied to `uv tool list`. The uv stub in c47f5c7a colours its output unless it gets `--color never`, and the environment and receipt tests are red at 5f1f3846 (§3b). The real uv is checked in §3c.
   - The two P3 are residuals, listed below.
3. Round 3 on `c47f5c7a..8ea9bf8a`, same reviewer: `Verdict: correct`, no new finding. It confirmed the P1 is closed with the real uv under forced colour and the regression test red without the fix. It agreed with both residuals and asked that the kept `omp.previous` be named here; the Residuals section names it.

## Residuals (for the orchestrator's disposition)

- `update_omp` keeps one generation: an earlier `omp.previous` is replaced before the install, so a failed install restores the new entry and the earlier kept copy is gone.
- `~/.local/share/agent-assets/omp/omp.previous` has no manifest record. `remove-agent-asset update_omp` already refuses the recorded `~/.local/bin/omp`, which is outside the safe roots before and after this PR, so the omp step has no working reverse path either way. That is outside the owned rows.
- If `uv tool uninstall hcom` itself fails (for example an I/O error), `--yes` stops before the recorded paths and the step are removed, and the next run retries. Only the case where hcom is absent is skipped.
- No real npm or real `uv tool install`/`uninstall` ran. The tests use stubs: a fixture npm that follows npm's bin-link ownership rule and a uv stub that answers like uv 0.13.1 (`tool dir`, coloured unless `--color never`; ``error: `hcom` is not installed``, exit 2).

## Red before this task, not this task's

- `tests/unit/test_update_agent_assets.py` cannot run inside this seat's sandbox. macOS `mktemp -d` without a template ignores `TMPDIR`, and the sandbox denies the user temp directory, the same on `origin/main` (§5). Its red and green runs (§8, §8a, §9) ran outside the sandbox, which is the sandbox record's row 3. CI runs it on every OS.
- `ruff check` reports two errors in `tests/unit/test_remove_agent_asset.py`: EXE001 (shebang without the executable bit) and I001 (import block). Both are in the file's header, which this PR does not touch, and both appear the same on `origin/main` (§6).

## Caps (§7)

- Outside `tests/` and `.orchestration/`: 60 changed lines of 120 (the remover 30 added and 3 deleted; the updater 18 and 9).
- Under `tests/`: 256 changed lines of 400 (test_remove_agent_asset.py 72; test_update_agent_assets.py 113 and 71).

## PR

PR #416 was opened as a draft from this worktree with the plain create command and `--body-file .orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/pr-body.md`, then marked ready after CI. The Bot's automatic review at ready is the only one; no `@codex review` comment is posted.

CompactionDB (main checkout, through the permission gate): `cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T129 assets-omp-hcom followup a02 (PR 416): …'` printed `e79d449c-0758-4295-b5a2-dbf1d9fe35e2`.

cost: n/a
