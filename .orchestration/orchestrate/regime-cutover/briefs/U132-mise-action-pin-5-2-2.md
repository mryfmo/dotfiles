# U132 mise-action pinned to v5.2.2 at the five sites, following the release like the hosts

GOAL
Plan P-35 (decisions row plan-P-35, 2026-10-29T06:19:30Z; `handoff/evaluations/U115-workflow-lockfile.md`, "#549"): adopt Dependabot #549 as a unit. The reason from the release notes, not the bot: v5.2.0 and v5.2.1 verify the mise binary against its signed packslip and refuse a missing one for mise 2026.9.3 or later, which the sites' 72 h window always reaches; v5.2.0 rolls the cache every 30 days so one cache cannot keep one mise forever. The v5.0.0 breaking default (`minimum_release_age` 24h) is already set to 72h at every site. v5.1.0 changed one thing the evaluation left to this unit: a cached mise is kept until the cache key changes, so CI's mise would lag the hosts' 72 h window by up to 30 days. The coordinator decides `auto_update: true` at every site, so CI runs the same mise the hosts get (the newest at least 72 h old), cached per version. #549 is not touched; the coordinator closes it as superseded after this unit merges.

SCOPE
One branch `ci/mise-action-5-2-2` from `origin/main`. May write: the five `uses: jdx/mise-action@` steps (the `uses:` line and the `with:` block) in `.github/workflows/docs-check.yml`, `.github/workflows/docs.yml`, `.github/workflows/macos.yaml`, `.github/workflows/test.yaml`, `.github/workflows/ubuntu.yaml`; the test in `tests/unit/test_github_release.py` that asserts every mise-action step's inputs; any other test under `tests/unit/` that names the old sha (`grep -rn c2a87611 tests/unit`). No other file.

CHANGE
1. Verify the sha before writing it: `gh api repos/jdx/mise-action/git/ref/tags/v5.2.2 --jq .object` (a read); if the object is a tag, dereference it; the commit must be `8418fedb1110381a0d3ba51a7a415d7c1b884550`. Paste the output in the body. A mismatch stops the unit with a report.
2. Every `uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4` becomes `uses: jdx/mise-action@8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2`. Each `with:` block keeps `minimum_release_age: 72h`, `install` and `cache` as they are and gains `auto_update: true` with the one comment `# CI runs the mise the hosts get: the newest at least 72 hours old, not the one a cache kept (v5.1.0)`.
3. The test in `tests/unit/test_github_release.py` that counts `minimum_release_age: 72h` per `uses: jdx/mise-action@` step also counts `auto_update: true` the same way, so a site missing either fails.
4. Red proof: on a `git archive` of `origin/main` with the extended test alone, the test fails naming each workflow without `auto_update`; on this head it passes.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_github_release tests.unit.test_workflow_security tests.unit.test_regime_ci` OK (paste the Ran line). 2. `grep -rn c2a87611 .github tests` prints nothing; `grep -rn 'mise-action@' .github/workflows | wc -l` prints 5 and every line carries `8418fedb1110381a0d3ba51a7a415d7c1b884550 # v5.2.2`; `grep -c 'auto_update: true' .github/workflows/*.y*ml` sums to 5. 3. prettier check on the five workflows; ruff format check; `scripts/lint-comparisons.py --changed` exit 0. 4. The PR body's Contract names the release-note reason, the tag read, the `auto_update` decision and its reason, the one cold cache run per scope after the bump (v5.2.0 changed the key format), and what is left out: no `version`, `cache_key`, `cache_max_age_days` or `plugins` input is added.

CLOSURE
allowlist: the five sites, one input added with one value, one test extended to count it; the sha read from the action's own tag before it is written.

TRUST
TRUST: the unit trusts the action's tag `v5.2.2` as read from `api.github.com` at the time of the change and the release notes as the reason to move and for what `auto_update` does; it does not run the action and trusts the existing `test_external_actions_use_full_commit_shas` to keep every reference a full sha.

TIMEBOX
25 minutes.

FORBIDDEN
No change to #549 (no comment, review, close, rerun or edit); no other action's pin; no `version`, `cache_key`, `cache_max_age_days` or `plugins` input; no `gh` write; no edit to any file outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U132-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U132-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines, the tag read, the red proof), the line `Program-Unit: regime-cutover/U132`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the tag verification output, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; decisions row plan-P-35 (2026-10-29T06:19:30Z); `handoff/evaluations/U115-workflow-lockfile.md` sections "#549" and "Recommendation".
