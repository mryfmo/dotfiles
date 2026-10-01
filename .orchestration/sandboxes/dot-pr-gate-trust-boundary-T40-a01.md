# T40 isolation history

Worker: codex-security-dot-a006; team: dotfiles; delivery: turn.
Worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-sec`.
Required branch: `fix/pr-gate-trust-boundary` from origin/main `f45cf73551c449c689a69fa931adb858d4dd08fd`.
Observed branch after setup failure/retry: `pr-gate-trust-boundary`, same HEAD.

Git metadata resides outside the writable worktree. The sandbox rejected index.lock creation; an escalated retry encountered the existing shared config.lock. No lock was deleted and no reset/clean was performed. No source changes were made; only the five explicitly permitted task artifacts were written. No local bats, network operation, external install, or CompactionDB write occurred.

The mandatory worklog location `.agents` is read-only and not listed in task allowed_files. Worklog creation is deferred pending retasking. Plan: restore the branch boundary, reproduce all three findings with unit tests, implement the minimal fixes, validate, create the authorized PR, obtain CI results and agent review, record evidence, and send RESULT. TODO: every implementation/validation step. Done: read skills/task/source/tests; verify task digest and base; report setup blockers.

## Resume update

The requested branch was restored with `git switch fix/pr-gate-trust-boundary` after its normal invocation failed with `fatal: Unable to create '/home/moriya/Workspace/dotfiles/.git/worktrees/worker-sec/index.lock': Read-only file system`. Escalated retry succeeded under revision 2. Empty .agents/worklog directories were created before the waiver arrived; no worklog files were written. Latest instructions waive plan/todo/learn and permit task review JSON and receipt under .orchestration/validation.

The five allowed files were edited and staged. A normal git add hit the same read-only index.lock denial; revision-2-authorized escalation succeeded before revision 3 was read. Revision 3 now forbids Git-write escalation. No Git metadata mutation followed receipt of revision 3; PONG requests orchestrator-assisted preservation and rebase. Network escalation was used for the required PyYAML dependency after DNS failure and for gh repository lookup. CompactionDB writer-lock escalation used the explicit main-checkout exception, and the decision ID is recorded in validation. No global settings, hooks, README, Codex rules mirror, or .ua files were edited.

## Git escalation ruling and rebase

The subsequent AGMSG-ACCEPTANCE explicitly directed this worker to request human approval for Git metadata writes, then commit and rebase. Human-approved escalations ran these commands:

- `git commit -m 'fix(gate): bind PR base and scope feedback evidence'`: exit 0, c939977.
- `git rebase origin/main`: exit 0, resulting base a5f33eede3feb15c59031c5af904bf1c3838649b and head 0dfe8230fab12a1326bca3d328bdf6d9f35d9718. The five implementation files were byte-identical before/after the rebase.
- `git push -u origin fix/pr-gate-trust-boundary`: remote push succeeded (exit 0), but local upstream-config write reported `error: could not lock config file /home/moriya/Workspace/dotfiles/.git/config: File exists`. The lock was not changed. Explicit --head/--repo arguments avoid depending on upstream configuration.

PR creation and subsequent GitHub reads used separately approved network escalation. The first feedback-collection permission prompt was cancelled before execution; the user explicitly asked to show the choice again and approved the retry. Post-rebase unit testing encountered `PermissionError: [Errno 1] Operation not permitted` at the existing test's Unix socket bind; the full suite was rerun with human approval. No permission was self-approved and no review check was disabled.

## Final state

The earlier blocked/no-source-change statements above describe the initial setup only. The later explicit Git escalation ruling superseded the temporary no-escalation instruction. Human-approved commits c67ec77 and 10dfc10 and plain `git push origin fix/pr-gate-trust-boundary` completed the allowed fixes. All network reads, PR edits, and integration-gate GitHub queries used approved escalation; all final tests passed. Eight authorized task artifacts are prepared for the permitted main-checkout sync. The worktree has only those untracked artifacts and no modified tracked source. No permission self-approval, disabled review checks, browser review, external install, or changes outside the task exceptions occurred.
