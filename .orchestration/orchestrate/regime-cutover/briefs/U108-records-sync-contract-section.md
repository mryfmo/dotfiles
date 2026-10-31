# U108 The records-sync PR body carries a `## Contract` section so `pr-audit.sh` audits records PRs, and the config-status comment matches git 2.56.0 (plan P-26 and the comment part of P-03)

GOAL
`pr-audit.sh` refuses a PR body without a `## Contract` section (its own contract), so every records sync PR (U20 rows, #576, #577, #578) got an orchestrator verdict instead of a fresh-context audit. The sync lever writes the body, so the body can carry the section. Separately, `read_config` in `records-sync.sh` comments that `git config --get` exits 3 for an unparsable file; measured on git 2.56.0 on 2026-10-28 it exits 128 (and 1 for unset, 1 for an unreadable `-f` file with a warning on stderr). The reader's logic is right (any status other than 0 and 1 is a failure); the comment is wrong.

SCOPE
One branch `feat/records-sync-contract-section` from `origin/main`. May write: `scripts/orchestrator/records-sync.sh` (the `printf` block that writes the body, and the comment above `read_config`); `tests/unit/test_pr_levers.py` (`RecordsSyncTest` only); the regenerated `home/dot_agents/agent-config.yaml`, `scripts/generated-agent-outputs.json`, `home/dot_local/bin/common/executable_records-sync.sh` through the generator. Nothing else. `scripts/orchestrator/README.md` belongs to another unit this wave; leave it and list "README body description" as a follow-up in the report.

CHANGE
1. The body gains, after `## Summary`, a `## Contract` section with these bullets, in this order: the changed paths are exactly the files of `.orchestration/orchestrate/<program>/` that differ from `origin/main`, added, changed or deleted; no path lies outside that directory; every copy was masked with `--mask-secrets` and passed `--scan-identifiers` with the program's `redact-words.txt` when present; the commit was built in a repository with no user, system or checkout configuration and pushed over https with no user configuration; what the sync leaves out: the content of the records is not reviewed for truth, only for the identifier scan. The program name is interpolated, nothing else is dynamic.
2. The `read_config` comment states the measured table: 1 unset, 128 for an unparsable file on git 2.56.0 (the manual says 3), and that any status other than 0 and 1 is treated as a failure, so the reader is correct under both.
3. Tests: `test_the_body_names_the_units_and_decisions` (or a new test) asserts the `## Contract` heading is present exactly once, sits after `## Summary` and before the `Program-Unit:` line, and that the five bullets are present in order. The existing body tests keep passing.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_pr_levers.RecordsSyncTest tests.unit.test_scratch_git` passes. 2. `cmp scripts/orchestrator/records-sync.sh home/dot_local/bin/common/executable_records-sync.sh` equal, generator `--check` clean. 3. ShellCheck 0.11.0, `shfmt -i 4 -sr -d`, `scripts/ci/masked-dirname-check.sh` pass on the lever. 4. The PR body Contract (of this PR) says the sync's body now carries a Contract and that the next records PR is the live proof (the coordinator runs `pr-audit.sh` on it).

TIMEBOX
45 minutes.

FORBIDDEN
No change to what the sync copies, masks, scans, commits or pushes. No hand edit to a generated file.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 36 in the store)
- Create your worktree from the main checkout and work only there: `git -C ~/Workspace/dotfiles fetch -q origin && git -C ~/Workspace/dotfiles worktree add -b feat/records-sync-contract-section /tmp/dotfiles-wt/U108 origin/main`. Never write under `~/Workspace`, under `$HOME` config directories, or on any other host. Never `git stash`. No local Bats as evidence.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Never push, never open a PR, never merge. The coordinator pushes and opens the PR.
- Before you report, run on the committed head: the test modules your change touches plus `uv run --no-project --with pyyaml python -m unittest tests.unit.test_scratch_git`; ShellCheck 0.11.0 (`shellcheck`, the repository `.shellcheckrc` applies), `shfmt -i 4 -sr -d`, and `scripts/ci/masked-dirname-check.sh` on every touched shell file; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml python -m unittest tests.unit.test_lint_comparisons`; and `uv run --no-project --with pyyaml scripts/generate-agent-configs.py --check` (if it reports a stale output, run the generator without `--check` and commit the regenerated files; never hand-edit a generated file). CI runs the full suite.
- Shell comments are English shdoc. Python runs as `uv run --no-project`. Tests assert behaviour the user observes. Comments explain a non-obvious why only, no phase narration.
- A producer's status is read (standing order 21): a `$(...)` whose status is unchecked is a defect, a failed read is never treated as an absence, and every such decision has a failure-injection test.
- Write the PR body to `/tmp/dotfiles-wt/U108-pr-body.md` with these sections in order: `## Summary` (what and why, under 12 lines), `## Contract` (bullets: what this change guarantees, and what it leaves out), `## Threat table` (one row per touched path: what it does today, what changes, what could go wrong, how the change refuses it), `## Verification` (the commands you ran and their pasted result lines), the line `Program-Unit: regime-cutover/U108`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. No absolute home directory path anywhere (write `~/...`), no credential-shaped literal, none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt`.
- Conventions: `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Comments, Writing the reply), `~/.agents/pstack/skills/technical-writing/SKILL.md` for the PR body. Principles that apply to this unit: `~/.agents/pstack/skills/principle-model-the-domain/SKILL.md` (a table or registry over branching), `~/.agents/pstack/skills/principle-test-behavior-not-implementation/SKILL.md`, `~/.agents/pstack/skills/principle-fix-root-causes/SKILL.md`.

REPORT
Status, branch, head sha (40 hex), the files changed (`git diff --stat origin/main`), the commands you ran with their result lines, deviations from this brief, anything you could not verify, suggested follow-ups. Facts only. Under 40 lines.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`. The plan this unit implements is `handoff/05-remediation-plan.md` in the same store, with the research under `handoff/research/`.
