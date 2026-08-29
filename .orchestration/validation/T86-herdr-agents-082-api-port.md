# T86 Validation — herdr-agents 0.8.2 API port

## Local checks

- `bash -n home/dot_local/bin/common/executable_herdr-agents`: pass.
- `shellcheck home/dot_local/bin/common/executable_herdr-agents`: pass.
- `uv run python -m unittest tests.unit.test_herdr_agents tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids`: pass, 66 tests.
- `make unit-test`: pass in an isolated clean worktree, 355 tests. No bats tests were run locally.
- `git diff --check`: pass.
- `AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/20260829_135518_t86_receipt.md make require-crit-review`: pass.

## Live E2E

- Protected workspace `w1F` was inspected read-only and never mutated.
- Fresh run used scratch directory `/tmp/herdr-t86-final4.U6kr63` and created workspace `w1R` with exactly two panes: Claude `w1R:p1` and Codex `w1R:p2`.
- The registered lowercase names were `claude-orchestrator-w1r` and `codex-worker-w1r`.
- Test subjects used only generated express profile settings: Claude argv included the generated express model/effort arguments, while Codex argv included `--sandbox workspace-write --profile express`. The additional Claude permission flag only bypassed the disposable scratch-directory trust prompt.
- The successful run supplied an `FPATH` excluding the two paths reported by `compaudit` as insecure (`/usr/local/share/zsh` and `/usr/local/share/zsh/site-functions`). Both panes reported the canonical `/private/tmp/...` cwd.
- Rerunning the full command focused `w1R` in 0.84 seconds and retained exactly two panes/agents.
- Running `--attach` from `w1R:p1` returned successfully and retained exactly two panes/agents, proving idempotency.
- Scratch agmsg identity checks were empty, so no team leave was necessary.

During diagnosis, a scratch pane reproduced bracketed-paste text before zsh completed startup, followed by the `compinit` insecure-directory question. That evidence led to the combined process-info plus visible-prompt guard; a foreground shell alone is insufficient.

## Cleanup

- Closed E2E workspace `w1R` and removed `/tmp/herdr-t86-final4.U6kr63`; `herdr workspace list` then contained only protected workspace `w1F`.
- Closed every earlier diagnostic scratch workspace and removed its directory.
- Removed the isolated validation worktree and pruned its git metadata.

## GitHub Actions

- `gh pr checks 147 --watch --interval 10`: all required checks passed; `nix` was skipped by workflow conditions.
- Actions runs: bootstrap `33235033489`, tests `33235033494`, validate `33235033499`.
