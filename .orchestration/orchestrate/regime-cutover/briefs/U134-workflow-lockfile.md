# U134 the workflows lock their actions with the GitHub Actions lockfile

GOAL
Plan P-35 deferred `.github/workflows/actions.lock` on 2026-10-29 for three reasons (`handoff/evaluations/U115-workflow-lockfile.md`, "Recommendation"): the extension rewrites every `uses: <owner>/<repo>@<40-hex> # v<n>` to `@v<x.y.z>` and three tests that assert the SHA form fail, the gain was one transitive dependency, and the feature was a public preview. GitHub's changelog of 2026-10-28 made workflow lockfiles generally available (research/06 line 216), and the Secure use reference says a lockfile "supersedes SHA pinning for repositories that adopt it" and "verifies the identity of each source repository at run time" (research/03 lines 147 to 148). The rewrite is the documented design, not a defect. The operator's grant of 2026-11-02 runs the recommendation: adopt the lockfile and move the repository's own invariant from "every `uses:` is a 40-hex sha" to "every `uses:` has a lockfile entry whose commit is a 40-hex sha and whose ref is a full semver tag". Dependabot then regenerates the entry in the same bump PR, so the pin tests that stalled #548 stop being hand-edited.

SCOPE
One branch `ci/workflow-lockfile` from `origin/main`. May write: `.github/workflows/actions.lock` (new), the `uses:` lines of every file under `.github/workflows/`, `tests/unit/test_workflow_security.py`, `tests/unit/test_regime_ci.py`, `tests/unit/test_regime_workflow.py`, `tests/unit/test_github_release.py` and any other test under `tests/unit/` that names an action sha (`grep -rln '@[0-9a-f]\{40\}' tests/unit`), `.github/dependabot.yml` if a key is needed for the lockfile (read the Dependabot options reference first; the changelog says Dependabot regenerates the entry without configuration), and `docs/` or `README` lines that describe the SHA pin rule (`grep -rn 'full-length\|40-hex\|commit SHA' docs README.md | head`).

CHANGE
1. Install the extension under a scratch data home as U115 did (`export XDG_DATA_HOME="$TMPDIR/U134-gh-data"; gh extension install github/gh-actions-lock`), paste `gh extension list`. Run `gh actions-lock --no-interactive` from the tree root (the default narrows refs to full semver tags; do not pass `--no-narrow`). Paste the run's output. Then `git status --porcelain` and `cat .github/workflows/actions.lock` in the body.
2. Read the lockfile: for every `uses:` in the workflows the entry's `commit` must equal the sha the workflow carried before the rewrite (U115 measured this true for all six on 2026-10-29; re-measure on the current pins, which U131 and U132 moved). A mismatch stops the unit with a report.
3. `tests/unit/test_workflow_security.py`: `test_external_actions_use_full_commit_shas` becomes a test that reads `actions.lock` (PyYAML is available to the tests) and asserts, for every `uses:` reference in every workflow, one entry with a 40-hex `commit`, a `ref` that is a full semver tag (`v<major>.<minor>.<patch>`) or the exact ref the workflow names, and `owner_id` and `repo_id` present; and that no lockfile entry is unused. The pin lists in `test_regime_ci.py` and the constants and fixture in `test_regime_workflow.py` name the tag form the workflow now carries; `test_github_release.py` keeps its `minimum_release_age` and `auto_update` counts.
4. A step in `regime.yml` is not added. The runner enforces the lockfile at run time (the concept page). One unit test (behaviour) asserts the lockfile covers every reference, so a workflow edit that adds an unlocked action fails CI before it runs.
5. Docs: wherever the repository text states the SHA pin rule, it states the lockfile rule instead, with the two vendor sentences quoted and their URLs.
6. Red proof on a `git archive` of `origin/main`: the new coverage test fails there (no lockfile); on this head it passes and the old SHA test is gone.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_workflow_security tests.unit.test_regime_ci tests.unit.test_regime_workflow tests.unit.test_github_release tests.unit.test_drift_watch` OK (paste the Ran line); the broader `uv run --no-project --with pyyaml python -m unittest discover -s tests/unit -p 'test_*.py'` with its Ran line and every failure named with its cause (an unrelated pre-existing failure is reported, not fixed). 2. `grep -rn '@[0-9a-f]\{40\}' .github/workflows` prints nothing; `actions.lock` parses and names every reference once. 3. prettier check on the workflows; ruff format check; `scripts/lint-comparisons.py --changed` exit 0. 4. The PR body's Contract names the new invariant, the vendor sentences, the extension version, and what is left out: the "Require lockfile" repository policy and the Actions permissions policy are the operator's (admin); no CI step installs the extension.

CLOSURE
remove: the hand-kept SHA invariant and its three pin constants are removed; the lockfile and one coverage test replace them.

TRUST
TRUST: the unit trusts `gh actions-lock` as the writer of the lockfile and GitHub's runner as its enforcer at run time, and trusts the Secure use reference's statement that the lockfile supersedes SHA pinning; it does not verify an action's build and does not set the repository's Actions policies.

TIMEBOX
60 minutes.

FORBIDDEN
No `--no-narrow`, no `--relock`, no `--accept-moved`; no change to any action's version beyond what the rewrite of the current sha to its tag produces; no change to `jobs`, `permissions`, `concurrency` or `timeout-minutes`; no `gh` write to GitHub (the extension's network reads are the only calls); no edit outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U134-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U134-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the extension output, the lockfile, the result lines and the red proof), the line `Program-Unit: regime-cutover/U134`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the lockfile entry count, the red proof, deviations. Under 15 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; decisions rows plan-P-35 (2026-10-29T06:19:30Z) and audit-loop-2026-11-02; `handoff/evaluations/U115-workflow-lockfile.md`; `handoff/research/03-ci-reliability.md` lines 147 to 149; `handoff/research/06-codex-and-actions-security.md` line 216.
