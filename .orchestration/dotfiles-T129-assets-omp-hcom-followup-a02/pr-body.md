## Summary

The assets lineage's second owner task (`dotfiles-T129-assets-omp-hcom-followup-a02`): the advisory rows of PR #398, each fixed with a refusal fixture that is red before the fix and green after.

| Row | Class | Change | Tests |
|---|---|---|---|
| 4303212235 (and the #398 audit's finding 2) | uninstall-leaves-tool-env | `remove-agent-asset update_hcom` runs `uv tool uninstall hcom`, which removes uv's tool environment and its receipt, then deletes the recorded binary and the retained wheel. `~/.local/share/agent-assets` and the exact path `~/.local/bin/hcom` join the safe roots; before, both recorded paths failed the guard and nothing was removed. Without uv it reports and removes nothing, so the manifest step stays. | `test_hcom_removal_deletes_the_recorded_binary`, `…_deletes_the_retained_wheel`, `…_uninstalls_the_uv_tool_environment`, `…_uninstalls_the_uv_receipt`, `…_without_uv_reports_and_removes_nothing` |
| 4303338055 (local:9842d91:1, audit:9842d91:1) | install-receipt-repair | a failed `uv tool install --force` deletes the retained wheel, so the skip guard cannot pass on it and the next run retries | `test_update_hcom_drops_the_retained_wheel_when_uv_fails_so_the_next_run_retries` |
| local:fbbc6d9:1 | omp-non-npm-entry | any `~/.local/bin/omp` that npm does not own (a standalone file, a link outside the package, a dangling link) moves aside before the npm install and is put back when the install does not end at the pin; this generalises #405's dangling-link removal | `test_update_omp_moves_an_entry_npm_does_not_own_aside_and_puts_it_back_when_the_install_fails` |

- The fixture npm now links its own bin into `lib/node_modules/@oh-my-pi/pi-coding-agent/` and refuses with EEXIST any entry it does not own, as npm does; the earlier fixture overwrote such entries, which hid this failure.
- The hcom repair test and the new retry test share one helper; every assertion of the repair test is kept.

## Evidence

`.orchestration/dotfiles-T129-assets-omp-hcom-followup-a02/` holds the task copy, the report, the validation output (each test red at the tests commit and green at the head, shellcheck, shfmt, ruff, the caps), the sandbox record and the learning triage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
