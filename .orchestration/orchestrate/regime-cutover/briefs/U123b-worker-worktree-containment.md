# U123b worker-worktree.sh decides containment by identity, not by string

GOAL
The audit of U123 round 5 (verdicts/U123-ee3145aa.md) left three P2/P3 findings in `scripts/orchestrator/worker-worktree.sh`: the containment check that refuses a root inside the checkout compares resolved path strings, so a case alias of the checkout path on a case-insensitive volume passes and the lever writes a repository into the checkout's hooks directory (P2 :254); the resolver reads (`cd`/`pwd -P`) have no committed failure-injection regression (P2 test:686); the resolved root is not re-checked for a newline, so a newline-free symlink to a directory whose name holds one prints a receipt split across lines (P3 :251). The lever is the coordinator's own tool and its root is the default under TMPDIR, so the findings are contained until this unit lands.

SCOPE
One branch `fix/worker-worktree-containment` from `origin/main`. May write: `scripts/orchestrator/worker-worktree.sh`, `tests/unit/test_worker_worktree.py`, `scripts/orchestrator/README.md` (rows), generated copies through the generator.

CHANGE
1. Containment by identity: the lever walks the resolved root and each of its ancestors and compares device and inode (`stat`, status read) with the checkout's worktree and git directory; a match refuses before anything is made. The string comparison is deleted. Test: a case alias of the checkout path (`<CHECKOUT>/.git/hooks` on a case-insensitive volume, or a scratch case-insensitive image when the volume is case-sensitive) is refused; red proof on origin/main.
2. The resolved root and the resolved checkout path are re-checked for a newline after resolution; a symlink to a directory whose name holds a newline is refused. Test with such a symlink.
3. Failure injection for the resolver reads: a `cd` into an inaccessible directory and a failing `stat` each refuse with exit 2 and make nothing (PATH shim or a mode-000 directory).

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_worker_worktree tests.unit.test_lever_self_check tests.unit.test_scratch_git tests.unit.test_sandbox_portability` OK. 2. The lints of the WORKER RULES. 3. The PR body's Contract states that containment is decided by device and inode and names what is left out (a bind mount or a network volume that reports changing inodes).

CLOSURE
remove: the resolved-string comparison is removed from the lever; containment is a device-and-inode walk over the resolved root's ancestors, so no spelling of a path (case, symlink, trailing slash) can name the checkout without being it.

TRUST
TRUST: the unit trusts `stat` and the kernel's path resolution as the one judge of identity and the coordinator as the only caller; it does not read the checkout's configuration, hooks or refs, and it trusts the U123 design that the worker tree is a fresh repository sharing only objects.

TIMEBOX
45 minutes.

FORBIDDEN
No change to the refusals U123 landed (pushurl, credential helper, hooks path, push shape), to `pr-audit.sh`, or to any existing worker tree. No `codex` or `gh` write.
WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never push, never open or edit a PR, never edit the live store; the coordinator pushes and sets the body. Create your tree with `~/.local/bin/common/worker-worktree.sh U123b fix/worker-worktree-containment origin/main` once U123 lands, else as the U123 brief says. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Run every test command in the foreground with a timeout and paste its result line; write a progress line to `/tmp/dotfiles-wt/U123b-progress.txt` after each step.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report, run on the committed head: the test modules your change touches plus `tests.unit.test_scratch_git`; ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/producer-status-check.sh` over the adopted levers (exit 0); `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`. CI runs the full suite.
- Shell comments are English shdoc. Tests assert behaviour the user observes. No `/tmp` literal in any tracked file.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U123b-pr-body.md` with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`), `## Verification`, the line `Program-Unit: regime-cutover/U123`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, branch, head sha (40 hex), files changed, the commands with result lines, the red proof, deviations, anything not verified. Under 30 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (orders 35 to 39); the decisions rows of phase `audit-loop-2026-10-30`; verdicts/U123-ee3145aa.md.
