# U110 The three workflows without a `concurrency` block get one (plan P-32, research V4-3)

GOAL
`macos.yaml`, `ubuntu.yaml` and `private-bootstrap.yaml` have no `concurrency` block (measured 2026-10-28, research `03-ci-reliability.md` section 2.2). `macos.yaml` serialises rows inside one run with `max-parallel: 1` because every row pushes to the same benchmark repository, but two runs from two pushes to main can still push concurrently. The GitHub Actions workflow syntax documents `concurrency.group` and `cancel-in-progress` for exactly this (https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax, read 2026-10-28).

SCOPE
One branch `ci/concurrency-groups` from `origin/main`. May write: `.github/workflows/macos.yaml`, `.github/workflows/ubuntu.yaml`, `.github/workflows/private-bootstrap.yaml`, and `tests/unit/test_workflow_orchestration_skip.py` or whichever test pins the concurrency text of the other workflows (`grep -rn cancel-in-progress tests/unit/`). Nothing else. Do not touch `test.yaml` (another unit owns it this wave).

CHANGE
1. `macos.yaml` and `ubuntu.yaml` get the workflow-level block `test.yaml` lines 17 to 19 use (a pull request's newer head cancels its older run, a main push is grouped by commit and never cancelled); copy the expression exactly and cite the source line in a one-line comment.
2. `macos.yaml` additionally gets a job-level `concurrency` on the job that pushes the benchmark, with the fixed group `macos-benchmark` and `cancel-in-progress: false`, so runs from different main commits queue behind each other. Update the `max-parallel: 1` comment to name the run-level group.
3. `private-bootstrap.yaml` runs on push, schedule and dispatch only; it gets `group: private-bootstrap-${{ github.sha }}` with `cancel-in-progress: false`.
4. The test that pins concurrency text gains the three workflows with their expected blocks, so a later edit that drops one fails the test.

ACCEPTANCE
1. The workflow test module passes. 2. `actionlint` if present on the host (`command -v actionlint`), else the repository's own workflow tests, passes. 3. The PR body Contract states which group each workflow uses and that the benchmark push can no longer run concurrently from two main commits. 4. After the coordinator merges, one green run of each workflow is the live proof (the coordinator records it; name it in the body as the acceptance the coordinator checks).

TIMEBOX
40 minutes.

FORBIDDEN
No change to any job's steps, matrix or permissions.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b ci/concurrency-groups /tmp/dotfiles-wt/U110 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U110-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U110`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
