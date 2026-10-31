# U103 The regime workflow's safety invariants are pinned by a test (plan P-01, part 1)

GOAL
GitHub enforces a default Actions event policy that blocks `pull_request_target` in public repositories on 2026-12-02 (https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target, read 2026-10-28). The operator will create an explicit policy that allows the event for this repository (gate G-23). That allowance must be backed by code: a test that fails when `.github/workflows/regime.yml` loses any of the properties that make `pull_request_target` safe here.

SCOPE
One branch `feat/regime-workflow-invariants-test` from `origin/main`. May write: new `tests/unit/test_regime_workflow.py` only. Nothing else. Read `.github/workflows/regime.yml`, `tests/unit/test_workflow_orchestration_skip.py` (for the YAML-reading idiom the suite uses; no PyYAML outside `--with pyyaml` runs, check how that test loads YAML) and `tests/unit/test_apt_mirror.py`.

CHANGE
1. The test loads `regime.yml` and asserts, each as its own test method with a message naming the line it protects: (a) the only trigger is `pull_request_target` with `branches` exactly `[main]`; (b) top-level `permissions` is exactly `contents: read` and no job widens it; (c) every `actions/checkout` step sets `ref` to the base branch expression (`refs/heads/${{ github.base_ref }}` or the equivalent the file uses today) and `persist-credentials: false`; (d) no step text contains `allow-unsafe-pr-checkout`; (e) the only fetch of the PR head writes to `refs/regime/pr-head` and no step checks it out; (f) the PR body reaches the script through an `env:` mapping and never appears inside a `run:` string; (g) `concurrency.cancel-in-progress` is true.
2. Each assertion is also exercised negatively: a helper mutates a parsed copy of the workflow (removes `ref`, widens `permissions`, inlines the body) and asserts the check fails on the copy. This proves the test can go red.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_regime_workflow` passes on the head and each negative case fails on its mutated copy.
2. The PR body's Contract says what the test guarantees (the seven properties) and what it leaves out (the policy itself is the operator's, gate G-23).

TIMEBOX
40 minutes.

FORBIDDEN
No change to any workflow. No change to `regime-ci.py`.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b feat/regime-workflow-invariants-test /tmp/dotfiles-wt/U103 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U103-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U103`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
