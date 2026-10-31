# U109 Every apt call in test.yaml is bounded and named, and the Azure mirror drop has a recorded re-check (plan P-31, research V4-2)

GOAL
After U102 every apt call goes to `archive.ubuntu.com`, which runner-images issue #15040 shows can go silent during `apt-get update`. No apt call in `.github/workflows/test.yaml` carries its own bound, and the steps that run them ("Install tools", the apt-get update inside "Run Python unit tests") have no `timeout-minutes`, so a stall there ends only at the job cancel (45 min) with no diagnosis, defeating the ordering U99 and U102 built so that a stalled step is named. The mirror drop also has no exit condition: #14823 was declared mirror-side and healthy on 2026-10-27 by GitHub staff, and nothing says when to retire the drop. Research: `handoff/research/03-ci-reliability.md` sections 1.4, 2.1 and proposal V4-2.

SCOPE
One branch `ci/bound-every-apt-call` from `origin/main`. May write: `.github/workflows/test.yaml`; `tests/unit/test_apt_mirror.py`; `scripts/ci/drop-azure-apt-mirror.py` (docstring only). Nothing else. Do not touch `ubuntu.yaml`, `remote.yaml`, `private-bootstrap.yaml`, `macos.yaml` or any installer (other units own them this wave).

CHANGE
1. Every `apt-get update` and `apt-get install` line in `test.yaml` runs as `timeout --kill-after=10 <N> sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 ...` where `<N>` is measured per step from the last five passing runs of `test (ubuntu-24.04, client)` on main (`gh run list --branch main --workflow 'Unit test' --limit 5` and the job logs' step durations; paste the numbers) plus a margin of at least 2x and at least 120 s. The steps "Install tools" and "Run Python unit tests" get `timeout-minutes` equal to the ceiling of the sum of their bounds plus one minute.
2. `tests/unit/test_apt_mirror.py` gains a closed-world rule in the shape the U99 scanner uses (read `decisions.tsv` row `treadmill-u99-scanner` and the test that implements it, `grep -rn 'speed-limit' tests/unit/`): every `apt-get` token in any workflow `run:` block under `.github/workflows/` must sit on a line that carries the exact bound form above, or be listed in an exemption table in the test keyed by file and the exact line text with a reason. Lines in the workflows this unit does not own are listed in that table with the reason "owned by the installer scripts, bounded by U99" or "not this unit", so the rule is green on the head and the next unit removes rows as it bounds them. `BoundOrderTest` (the 2 x bound + budget under the step) must still hold with the new step bounds; adjust the budget constants only with the measured numbers and say why.
3. The drop script's docstring and the `## Verification` of the PR body name the re-check condition: when #14823 is closed, measure three `test (ubuntu-24.04, client)` runs with the drop disabled and compare the apt step times to the runs with it; retire the drop only if they are within 20 percent.

ACCEPTANCE
1. The new rule fails on `origin/main` (show the failing output in the PR body) and passes on the head. 2. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_apt_mirror tests.unit.test_workflow_orchestration_skip` passes. 3. The PR body Contract states the bound form, the exemption table's size and its reasons, and that a stalled apt call ends inside its step with the step's name.

TIMEBOX
75 minutes.

FORBIDDEN
No apt archive cache. No change to `scripts/ci/run-bats.py` or its bound. No change to the mirror drop's behaviour.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b ci/bound-every-apt-call /tmp/dotfiles-wt/U109 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U109-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U109`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
