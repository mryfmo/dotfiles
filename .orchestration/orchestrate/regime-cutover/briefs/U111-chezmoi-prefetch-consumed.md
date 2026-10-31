# U111 The chezmoi externals prefetch proves on every run that chezmoi consumed it (plan P-38, research V4-10)

GOAL
U96 prefetches each single-URL archive external with bounded curl retries and writes the verified archive into chezmoi's cache at `<cacheDir>/external/<sha256 of the URL>`, a layout read from chezmoi 2.73.3 source and documented nowhere (research `03-ci-reliability.md` section 6; chezmoi documents no retry, timeout or prefetch hook). The installed chezmoi version floats ("the newest release at least 72 hours old"). If a release moves or re-keys the cache, the prefetch still succeeds and chezmoi downloads again unbounded, the exact EOF class U96 closed, with nothing to say so.

SCOPE
One branch `fix/chezmoi-prefetch-consumed` from `origin/main`. May write: `scripts/lib/chezmoi-externals.sh` and its copy inside `setup.sh` (kept byte-equal by `tests/unit/test_chezmoi_externals.py`; read that test first to see how the copy is checked), `Makefile` lines 121 to 123 (the prefetch call), the bootstrap step of `.github/workflows/remote.yaml` that runs the prefetch, and `tests/unit/test_chezmoi_externals.py`. Nothing else. Do not touch `test.yaml`.

CHANGE
1. A new function beside `prefetch_chezmoi_externals`, `assert_chezmoi_externals_cached <source dir>`, runs after the prefetch and before `chezmoi apply`: it runs `chezmoi --refresh-externals=never --source <dir> status` restricted to the externals' targets (read how the externals are declared in `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl` and what `chezmoi status` accepts as targets) under the network-denied form the repository already uses in `test.yaml` lines 385 to 394 (`unshare --net` on Linux when available, `sandbox-exec -p '(version 1)(allow default)(deny network*)'` on macOS; if neither is available the function prints that it ran unguarded and returns 0, as a named limitation). It fails with a one-line reason when chezmoi exits non-zero or prints any of a closed list of strings in a table (`unexpected EOF`, `dial tcp`, `Get "http`, `no such host`), and it prints the chezmoi version it ran under so the log names the version a layout change arrived with.
2. The function's status is read by its callers (`Makefile`, `setup.sh`, the workflow step): a failure stops the apply with the reason, never continues.
3. Tests: a stub `chezmoi` on PATH that prints `chezmoi: unexpected EOF` and exits 1 makes the function fail with the reason; a stub that exits 0 and prints nothing passes; the version line is printed in both cases; the `setup.sh` copy equals the library.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_chezmoi_externals` passes with the new cases. 2. ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` pass on the library and `setup.sh`. 3. The PR body Contract states what the check proves (chezmoi needed no network for the externals after the prefetch) and what it leaves out (a cache layout change is detected, not repaired; the unguarded fallback when no network denial tool exists). 4. The two bootstrap rows in CI are the live proof after the coordinator merges; name them.

TIMEBOX
75 minutes.

FORBIDDEN
No change to the prefetch's download, retry or verification logic. No change to the externals' declarations.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b fix/chezmoi-prefetch-consumed /tmp/dotfiles-wt/U111 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U111-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U111`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
