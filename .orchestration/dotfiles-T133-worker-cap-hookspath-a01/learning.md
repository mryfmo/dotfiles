# T133 learning triage

Validated: Git with multiple worktrees rejects config --worktree until extensions.worktreeConfig is enabled. Enabling it in the common config and writing core.hooksPath with --worktree gives only the seated worktree .githooks; main retains no hooksPath. The executable test and temporary proof assert this and count only one extension write across two add-worker runs.

Validated: repeated add-worker tests must reset the fake pane list between runs; spawn.sh mutates that fixture. Leaving the first fake pane can cause an unrelated attach-a-client linkage failure.

Validated: make format traverses preserved untracked evidence/caches. An initialized Git archive copy can distinguish tracked baseline failures from a task regression without editing old evidence. Base and changed snapshot format outputs are byte-identical.

Candidate reusable rule only; no rule/skill promotion. Task source SKILL edits are exactly the two dispatched cap replacements. cost: n/a

Validated in Amendment1: fcntl.flock on an inherited Bash FD locks the same open file description, so Bash retains the lock after the acquiring Python child exits. Explicit LOCK_UN releases it even if descendants retain that descriptor; then close Bash's FD. This gives native Linux/macOS flock behavior without a flock CLI dependency. Temporary proof and held-lock/concurrent launcher test pass.

Validated in connected code: ensure_worker_identity --no-join derives an identity but does not join it. The add-worker critical section must span spawn.sh, which registers the worker, rather than releasing after identity-name derivation.

Advisory follow-up: is_main_checkout compares git-dir/common-dir and accepts separate-git-dir main worktrees. A future lock path should be derived from git rev-parse --git-common-dir, rather than assuming .git is a directory. Native separate-git-dir fixture confirms the current literal task path fails; later-review P2 is owned by the named follow-up, not fixed in a third round.

Security triage (not promoted): final feedback includes automatic Security Review P1 4305769826. It reports that activating per-worktree config in worker-writable Git metadata permits host Git command execution via core.fsmonitor. Worker did not independently reproduce this exploit; final task/security audit and operator disposition are pending. One fix round is spent, so keep the finding open rather than claiming it was addressed by the unrelated concurrency fix.

## Amendment3 validated re-plan

A caller-only Git environment does not cross real herdr tab.create RPC; --env serializes it, but the installed upstream driver does not pass that option. Fake spawn-only tests would miss this transport boundary. Hooks configuration therefore leaves a01 for a02, with no Git config writes in the reduced a01. New no-config RED/GREEN checks command traces plus common/worker actual config.
