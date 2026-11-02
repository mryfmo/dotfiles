# U135 checkout-guard: the store is found from the common directory, and install leaves nothing behind

GOAL
U129 merged as 89e28c2b with four findings filed under the merge threshold (`verdicts/U129-4405a071.md`). Three change behaviour a worker can observe and one is a missing pinned test: (1) `:415` when the main checkout's `.git` is a symlink to a separate git directory, the hook resolves the main checkout from `git worktree list`, which names the git directory, so a linked worktree's updates miss the store and pass; (2) `:663` an install that created the hooks directory and then fails leaves that directory; (3) `:322` the `prepared` line's values are checked for field count alone, not as object ids; (4) `:677` the staged-file `mktemp` has no failure-injection test of its own. This unit closes the four.

SCOPE
One branch `fix/checkout-guard-store-from-common-dir` from `origin/main`. May write: `scripts/orchestrator/checkout-guard.sh`, `tests/unit/test_checkout_guard.py`, `scripts/orchestrator/README.md` (the checkout-guard rows), `home/dot_agents/agent-config.yaml` (the pin, by the generator), `scripts/generated-agent-outputs.json` (by the generator), `home/dot_local/bin/common/executable_checkout-guard.sh` (by the generator).

CHANGE
1. The hook finds the main checkout as the parent of `git rev-parse --git-common-dir` resolved with `realpath` semantics the hook already uses for its other reads, never from `worktree list`; the store walk starts there. Test: a scratch main checkout whose `.git` is a symlink to a separate directory, with a store, and a linked worktree whose commit and `update-ref` are both refused.
2. `install` records whether it created the hooks directory and removes it again on any failure before the final rename; an existing directory is never removed. Test: hooks directory absent, the staged `mktemp` fails (a counted PATH shim, as the round-6 test does for the scratch call), install exits 2 and the directory does not exist afterwards.
3. The `prepared` line's `<old>` and `<new>` must each be 40 or 64 lowercase hex, else the line is refused as malformed (exit 1, naming the value). Test with `not-an-oid`.
4. One injection test aimed at the staged-file `mktemp` alone (the scratch-directory call succeeding, the second failing), asserting exit 2 and the hooks directory's listing and bytes unchanged when it pre-existed.
5. Red proof on a `git archive` of `origin/main`: the symlink case passes a linked-worktree `update-ref`; the created hooks directory remains after a failed install; `not-an-oid not-an-oid refs/heads/main` exits 0. Each flips on this head.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_checkout_guard tests.unit.test_regime_init tests.unit.test_lever_self_check tests.unit.test_scratch_git` OK (paste the Ran line). 2. ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` on the lever; `scripts/ci/git-invocation-check.sh` exit 0; `scripts/ci/producer-status-check.sh` over the adopted levers exit 0; ruff format check; `scripts/lint-comparisons.py --changed` exit 0; the generator check up to date. 3. The PR body's Contract keeps the U129 TRUST sentence word for word and adds nothing to it; the threat table has a `closed` row per finding with its test selector.

CLOSURE
remove: the `worktree list` read is removed from the hook and the one common-directory read names the checkout; the other three are tests and one refusal on a closed grammar (hex of two lengths).

TRUST
TRUST: the unit trusts the isolated git's `--git-common-dir` answer as the one name of the main checkout and trusts the worker as a non-adversarial actor whose reflex the refusal stops; git resolving its hooks to another place under the caller's configuration or environment, whenever and however set, is a standing-order breach the records catch, not a defect the hook closes.

TIMEBOX
45 minutes.

FORBIDDEN
No reopening of the install-time hooks-path check in any form (U129 rounds 2 to 4); no change to `regime-init`; no `gh` call; no edit outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U135-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules and lints named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`; `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check`.
- Write the PR body beside your tree (`../U135-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path and per finding), `## Verification` (the result lines and the red proof), the line `Program-Unit: regime-cutover/U135`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; `verdicts/U129-4405a071.md`; the U129 mechanism-change rows of 2026-10-31 (10:29:33Z and 11:11:20Z); the follow-up candidates row of 2026-10-31T12:21:10Z.
