# T40 isolation

Worker: codex-security-dot-a006; team: dotfiles; delivery: turn.
Worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec`.
Required branch: `fix/pr-gate-trust-boundary` from origin/main `f45cf73551c449c689a69fa931adb858d4dd08fd`.
Observed branch after setup failure/retry: `pr-gate-trust-boundary`, same HEAD.

Git metadata resides outside the writable worktree. The sandbox rejected index.lock creation; an escalated retry encountered the existing shared config.lock. No lock was deleted and no reset/clean was performed. No source changes were made; only the five explicitly permitted task artifacts were written. No local bats, network operation, external install, or CompactionDB write occurred.

The mandatory worklog location `.agents` is read-only and not listed in task allowed_files. Worklog creation is deferred pending retasking. Plan: restore the branch boundary, reproduce all three findings with unit tests, implement the minimal fixes, validate, create the authorized PR, obtain CI results and agent review, record evidence, and send RESULT. TODO: every implementation/validation step. Done: read skills/task/source/tests; verify task digest and base; report setup blockers.

## Resume update

The requested branch was restored with `git switch fix/pr-gate-trust-boundary` after its normal invocation failed with `fatal: Unable to create '/home/moriya/Workspace/dotfiles/.git/worktrees/worker-sec/index.lock': Read-only file system`. Escalated retry succeeded under revision 2. Empty .agents/worklog directories were created before the waiver arrived; no worklog files were written. Latest instructions waive plan/todo/learn and permit task review JSON and receipt under .orchestration/validation.

The five allowed files were edited and staged. A normal git add hit the same read-only index.lock denial; revision-2-authorized escalation succeeded before revision 3 was read. Revision 3 now forbids Git-write escalation. No Git metadata mutation followed receipt of revision 3; PONG requests orchestrator-assisted preservation and rebase. Network escalation was used for the required PyYAML dependency after DNS failure and for gh repository lookup. CompactionDB writer-lock escalation used the explicit main-checkout exception, and the decision ID is recorded in validation. No global settings, hooks, README, Codex rules mirror, or .ua files were edited.
