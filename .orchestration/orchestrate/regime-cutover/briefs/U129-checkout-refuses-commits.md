# U129 The coordinator's checkout refuses commits: a worker who reaches for it is sent to the worker-tree lever

GOAL
Three owners in one day acted in the coordinator's checkout `~/Workspace/dotfiles` against the first line of their task: U125a committed on its local `main` (2026-10-31T01:58Z, moved to the branch and main reset by hand), U107bRound2 and U128Round2 ran `git worktree add` there to make `/private/tmp/dotfiles-wt/<unit>` and committed in those linked worktrees (05:26Z, 08:13Z). The worker tree of U123 cannot push, but nothing in the checkout refuses a commit, and the checkout's `core.hooksPath` is unset, so its `.git/hooks/` is empty and every linked worktree shares it. A rule holds when the tool refuses (U123). This unit installs, into the checkout's common `.git/hooks/`, a `pre-commit` that refuses every commit in the checkout and in any linked worktree of it while a program store exists under `.orchestration/orchestrate/`, printing the one accepted route (`worker-worktree.sh <unit> <branch> origin/main` and the resolved tree root under `$TMPDIR/dotfiles-wt/`), and a `post-checkout` that, after a `git worktree add`, prints the same route (it cannot undo the add). The coordinator never commits in the checkout (records move through `records-sync.sh`'s scratch repository, code through worker trees), so no exemption is needed; say so in the Contract.

SCOPE
One branch `feat/checkout-refuses-commits` from `origin/main`. May write: new `scripts/orchestrator/checkout-guard.sh` (the lever: `install <checkout>` writes the two hooks, `check <checkout>` reports whether they are installed and byte-equal to the lever's copies; the hook bodies live in the lever as heredocs or as files under `scripts/orchestrator/hooks/`), `scripts/orchestrator/regime-init` (calls `checkout-guard.sh install` on the repository it prepares; read its shape first), `home/dot_agents/skills/hcom-orchestration/SKILL.md` step 0 or 1 (one sentence), `scripts/orchestrator/README.md` (rows), `tests/unit/test_checkout_guard.py` (new), generated copies and pins through the generator, the omp policy allow rows for the new lever if the pattern of the other levers requires one (read `home/dot_agents/omp/policies/orchestrator.yml` and its README).

CHANGE
1. `checkout-guard.sh install <checkout>`: refuses unless `<checkout>` is the main checkout (`git rev-parse --git-common-dir` equals `--git-dir`, a linked worktree is refused), `core.hooksPath` is unset there (a set path is refused naming it, since the hooks would not run), and `.git/hooks/pre-commit` and `post-checkout` are absent or already the lever's own (any other content is refused, never overwritten). Writes both hooks (mode 0755) and reads them back. Every read's status is checked (standing order 21).
2. `pre-commit`: when the checkout's toplevel holds `.orchestration/orchestrate/*/units.tsv`, print `checkout-guard: this checkout is the coordinator's; commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one under $TMPDIR/dotfiles-wt/<unit> (standing order 29)` and exit 1; otherwise exit 0. No environment variable bypasses it (a bypass is `git commit --no-verify`, which only the operator runs by hand; say so in the Contract). `post-checkout`: when its third argument is 1 (a branch checkout, which `git worktree add` performs) and the current worktree is a linked one, print the same route as a warning and exit 0.
3. `regime-init` runs `checkout-guard.sh install` on the checkout it prepares (idempotent: a second run finds the lever's own hooks and exits 0). The SKILL names it in one sentence.
4. Tests in `tests/unit/test_checkout_guard.py` with scratch repositories: install on a main checkout succeeds and a second install is a no-op; install on a linked worktree, on a checkout with `core.hooksPath` set, and over a foreign `pre-commit` each refuses (exit 2, nothing written); a commit in the checkout with a store is refused with the message; a commit in a linked worktree of it is refused; a commit in a checkout without a store passes; `git worktree add` prints the warning and succeeds; `git -c core.hooksPath=/dev/null commit` (the isolated git of the levers) is unaffected; a read failure injected on the store glob refuses the commit (fail closed).

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_checkout_guard tests.unit.test_regime_init tests.unit.test_hcom_seat_skills tests.unit.test_lever_self_check tests.unit.test_scratch_git` OK. 2. ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` on the lever and the hooks; `scripts/ci/producer-status-check.sh` over the adopted levers exit 0; `scripts/ci/git-invocation-check.sh` exit 0 (the hooks' git reads carry `# git-isolated: allow` with a reason, since a hook runs inside the user's git and cannot isolate itself). 3. The PR body's Contract states: every commit in the checkout and its linked worktrees is refused while a store exists; what is left out: `--no-verify`, a hook path set by the operator, a worker that edits `.git/hooks` (the worker tree is a repository of its own and never sees these hooks).

CLOSURE
remove: the commit path is removed from the coordinator's checkout and its linked worktrees by a hook installed once by `regime-init`; no sentence in a task text carries the rule any more.

TRUST
TRUST: the unit trusts the coordinator as the only committer in the checkout, who commits nothing there by design, and trusts git to run `.git/hooks/pre-commit` for the checkout and every linked worktree when `core.hooksPath` is unset; it does not read the worker's identity and treats `--no-verify` as the operator's own hand.

TIMEBOX
60 minutes.

FORBIDDEN
No change to `worker-worktree.sh`; no hook that runs a network command or writes outside its own stdout and stderr; no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U129-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; the lints of ACCEPTANCE 2; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (regenerate and commit if stale).
- Write the PR body beside your tree (`../U129-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path and one per non-path control), `## Verification`, the line `Program-Unit: regime-cutover/U129`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof (a commit in a scratch checkout with a store passes on origin/main), deviations. Under 20 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; decisions rows phase-R of 2026-10-31 (01:58Z, 05:26Z, 08:13Z) on the three incidents; U123 (the worker-tree lever this one complements).
