# U131 setup-uv pinned to v10.3.2 at the six sites, with the regime test's pin

GOAL
Plan P-35 (decisions row plan-P-35, 2026-10-29T06:19:30Z; `handoff/evaluations/U115-workflow-lockfile.md`, "#548"): adopt Dependabot #548 as a unit. The reason from the release notes, not the bot: setup-uv 10.3.0 to 10.3.2 embed the known checksums for uv 0.13.0 to 0.13.5 and the action's own build verifies its npm dependency signatures; the six sites set no `version`, so the pin that knows the current checksums is the one to run. The Dependabot head cannot go green on its own because `tests/unit/test_regime_ci.py:193` hard-codes the old sha; this unit carries the pin and the test together. #548 is not touched; the coordinator closes it as superseded after this unit merges.

SCOPE
One branch `ci/setup-uv-10-3-2` from `origin/main`. May write: the six `uses: astral-sh/setup-uv@` lines in `.github/workflows/agent-assets.yml`, `.github/workflows/docs-check.yml`, `.github/workflows/docs.yml`, `.github/workflows/drift-watch.yml`, `.github/workflows/regime.yml`, `.github/workflows/test.yaml`; the pin constant in `tests/unit/test_regime_ci.py`; and any other test under `tests/unit/` that names the old sha (`grep -rn c18668ad tests/unit`). No other file.

CHANGE
1. Verify the sha before writing it: `gh api repos/astral-sh/setup-uv/git/ref/tags/v10.3.2 --jq .object` (a read); if the object is a tag, dereference it (`git/tags/<sha>` `--jq .object.sha`); the commit must be `07a047e608db84b3d8c06cd9a7c7dcc9c355c18e`. Paste the output in the body. A mismatch stops the unit with a report.
2. Every `uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0` becomes `uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2`, the indentation and the `with:` block of each site unchanged (`regime.yml` keeps `enable-cache: false`).
3. `tests/unit/test_regime_ci.py` names the new sha in its pin list. No other assertion changes.
4. Red proof: on a `git archive` of `origin/main` with only the six workflow lines changed, `tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_runs_base_code_only` fails naming the old sha; on this head it passes.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_regime_ci tests.unit.test_regime_workflow tests.unit.test_workflow_security tests.unit.test_github_release` OK (paste the Ran line); `tests/unit/test_regime_workflow.py` names the sha twice (a fixture workflow and `SETUP_UV_ACTION`), both move. 2. `grep -rn c18668ad .github tests` prints nothing; `grep -rn 'setup-uv@' .github/workflows | wc -l` prints 6 and every line carries `07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2`. 3. ruff format check; prettier check on the six workflows; `scripts/lint-comparisons.py --changed` exit 0. 4. The PR body's Contract names the release-note reason, the tag verification output, and what is left out: no `version` input is added, the cooldown rule stays the Dependabot-side 3 days.

CLOSURE
allowlist: the six sites and one test constant, the sha read from the action's own tag before it is written; no new input, no new rule.

TRUST
TRUST: the unit trusts the action's tag `v10.3.2` as read from `api.github.com` at the time of the change and the release notes as the reason to move; it does not verify the action's build and trusts the existing `test_external_actions_use_full_commit_shas` to keep every reference a full sha.

TIMEBOX
25 minutes.

FORBIDDEN
No change to #548 (no comment, review, close, rerun or edit); no other action's pin; no `version` or cache input added; no `gh` write; no edit to any file outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U131-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U131-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines, the tag read, the red proof), the line `Program-Unit: regime-cutover/U131`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the tag verification output, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; decisions row plan-P-35 (2026-10-29T06:19:30Z); `handoff/evaluations/U115-workflow-lockfile.md` sections "#548" and "Recommendation".
