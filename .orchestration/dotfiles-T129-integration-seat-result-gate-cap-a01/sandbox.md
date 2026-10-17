---
task_id: dotfiles-T129-integration-seat-result-gate-cap-a01
seat: claude-standard-dot-a006
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-integration-seat-result-gate-cap-a01

- Period: from the AGMSG-TASK (bus 2026-10-17T12:45:37Z) to the RESULT.
- Inside the sandbox ran: the branch and the rebase (`git rebase --no-gpg-sign`), the commits (`git -c commit.gpgsign=false`), the edits, every lint, the integration-seat tests, the two new herdr tests, the mutants, `make render-check`, `make validate-agent-assets`, the evidence, the HTTPS `git fetch`, and the HTTPS `git push` in the documented form (`GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles tools/integration-seat-result-gate-cap`).
- uv ran with `UV_OFFLINE=1`.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox, through the permission gate (`dangerouslyDisableSandbox`), and `agmsg-dispatch` through `excludedCommands`; rows 4 to 10 are planned in advance:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 status=question note=caps:…` (13:13:41Z) | `agmsg-dispatch` |
| 2 | `uv run python -m unittest tests/unit/test_integration_seat.py tests/unit/test_herdr_agents.py` and the same with `-v` (validation §7), twice: the sandbox denies the macOS `mktemp` that `--add-worker` and its tests use; the tests touch only temporary directories, stub binaries and a temporary HOME | test run |
| 3 | `test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude` with `origin/main`'s `herdr-agents` swapped in and restored (twice, the second in §7) | test run |
| 4 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/integration-seat-result-gate-cap --title … --body-file …` | `gh` |
| 5 | `gh pr ready <pr>` | `gh` |
| 6 | `gh pr checks <pr> --repo mryfmo/dotfiles --watch` (background, exit status joined) | `gh` |
| 7 | the Bot wait: `gh api` reads of the Bot's reviews, top-level comments and receipt comments on the head, at most every 30 seconds up to 15 minutes, and `gh pr comment <pr> --body '@codex review'` only at 10 minutes without one | `gh` |
| 8 | `scripts/orchestrator/result-precheck.sh run dotfiles-T129-integration-seat-result-gate-cap-a01 <pr> <head>` (its gh reads; its (i) runs `codex exec --sandbox read-only` when codex is on PATH there) | `gh`, `codex` |
| 9 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same wait | `gh` |
| 9a | used: the fix round's push (inside the sandbox, the documented HTTPS form), `gh pr comment 393 --repo mryfmo/dotfiles --body '@codex review'`, `gh run view 39037670915 --log-failed` (a read of the failed CI log), `gh api` reads of the Bot's comments, and the same wait on the new head | `gh` |
| 9b | the second question (`agmsg-dispatch … AGMSG-PONG … status=question`, 14:16:06Z), `gh run view 39039175795 --log-failed` and `gh api` reads of the re-review's comments; fix round 2's push (inside the sandbox) and the step-15 Bot wait on the new head without a further `@codex review` | `gh`, `agmsg-dispatch` |
| 10 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-integration-seat-result-gate-cap-a01 …` | `agmsg-dispatch` |
