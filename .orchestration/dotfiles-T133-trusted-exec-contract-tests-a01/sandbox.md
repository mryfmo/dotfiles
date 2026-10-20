---
task_id: dotfiles-T133-trusted-exec-contract-tests-a01
seat: claude-standard-dot-a011
---

# Sandbox record: dotfiles-T133-trusted-exec-contract-tests-a01

Every command ran inside the Claude Code sandbox from `.claude/worktrees/worker-d`. No command was retried outside it, and no permission prompt was answered by an agent.

- **Branch.** `git fetch origin main` ran on its own. The branch was created with `git switch -c tools/trusted-exec-contract-tests-a01 --no-track origin/main`; `tools/chain-review-scripts-followup-a06` (PR #434) was clean and pushed, and it is untouched. Every `git add` and `git commit` was a single command with `-c commit.gpgsign=false`.
- **Isolation.**
  - Every test and probe ran on temporary fixtures under `$TMPDIR`, created and removed by the probes. Validation §5 counts the `trusted-exec-*` fixture directories, 0 before and after the run.
  - The Check ran with a temporary `HOME` and a temporary `UV_CACHE_DIR`. The temporary `HOME` was empty after the run.
  - The trusted-parent tests replace only the directory-service response, with a fixture home. No test child reads or writes the real home.
  - This repository's Git configuration hashed the same before and after the run (validation §5).
- **Measurements.** Before writing the tests, two scratch scripts measured the trusted-parent child's environment, Git's behaviour under each attack and the filesystem's case sensitivity, each in its own `$TMPDIR` directory. The first form of the first one was a single command line ending in `rm -rf`, and it was refused before running; the script form ran instead and leaves its scratch directories under `$TMPDIR`.
- **Refused commands.**
  - The `rm -rf` command line above (permission gate).
  - `ps`, to check a background read, refused with `operation not permitted` in the previous task. It was not used here.
  - Nothing else.
- **Network.** `gh` read CI job logs and job steps inside the sandbox. The log download needed GitHub's log storage hosts as allowed domains for those commands. One directory-service command ran against the real account: revise 1's live check (validation §6) ran `dscl . -read` once, which exited 70 inside the sandbox. It read no file under the home.
- **The worker review.** One read-only subagent round, which ran its tests in its own scratch worktrees.
- **Revise 1.** The branch carried the orchestrator's update-branch merge `9545e59f`. The four revise commits (`bb539aa7`, `65c81c98`, `eda9b5ee`, `7d3ecd4f`) were single `git add` and `git commit -c commit.gpgsign=false` commands. The mutants and the red runs used detached scratch worktrees under the scratchpad, each removed with `git worktree remove --force` in its own block; no `git worktree prune` ran. No command was refused in this round.
- **The revise review.** One read-only subagent round on `9545e59f..65c81c98`, with its own scratch worktrees under `$TMPDIR`.
- **After this record.** The push and the draft PR are stated in the RESULT. The push runs over an HTTPS pushurl, because the global pushInsteadOf rewrites HTTPS to SSH, which fails here.

No `@codex review` comment is posted.
