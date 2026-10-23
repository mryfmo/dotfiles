# U13 regime CI: program-unit marker (root-cause fix for F3) — brief

GOAL
Make the `regime` CI check accept pull requests of the pstack-orchestrate program (operator decision D-024-131) without the old regime's task copy, by one small, tested rule: a PR whose body carries the line `Program-Unit: regime-cutover/U<n>` is a program PR and skips the task-copy requirement. Everything else in the checker stays as it is.

SCOPE
Exclusive worktree on a new branch `feat/regime-ci-program-marker` from `origin/main`. May write: `scripts/orchestrator/regime-ci.py`, its unit tests (find them: `grep -rl regime-ci tests/ | head`; add `tests/unit/test_regime_ci_program_marker.py` if none fits), and the one paragraph of documentation where the task-copy rule is described (grep `no task copy` / `task copy` under `docs/`, `README.md`, `.github/workflows/regime.yml`; change text only where it states the rule). Nothing else.

CONTEXT
- The failure (verifier report for PR #458): `regime-ci: no target: 12 changed path(s) outside .orchestration/ and no task copy`, from `scripts/orchestrator/regime-ci.py:254-261`; reproduced locally by the verifier. The rule predates D-024-131 (`.orchestration/decisions.tsv`, row `D-024-131`: the agmsg regime is off for this program; PRs are authored by poteto-agent workers from briefs under `.orchestration/orchestrate/regime-cutover/briefs/`).
- Read `.github/workflows/regime.yml` to see how the checker gets the PR body (event payload, `gh api`, or env); use the same source. If the body is not available to the checker today, read it with the minimum change (the workflow already has a token for `gh api` per plan 025 P1-17) and cite the lines.
- The `regime` check is not a required status (verifier), but the program keeps its frontier green, so this fix lands before the other program PRs are merged.

ACCEPTANCE
1. A unit test with a fixture PR body containing `Program-Unit: regime-cutover/U3` and 12 changed paths outside `.orchestration/` → the checker passes that rule; the same fixture without the line → the existing refusal text, unchanged. Paste `uv run --no-project -m pytest <test file> -q`.
2. The marker regex is strict: `^Program-Unit: regime-cutover/U[0-9]+$` on its own line; anything else does not match (test).
3. `uv run --no-project scripts/orchestrator/regime-ci.py --help` (or the existing self-check) still runs; existing tests pass (`uv run --no-project -m pytest tests/unit -q`, paste the summary line).
4. PR open with the marker line in its own body (`Program-Unit: regime-cutover/U13`), title `fix(regime-ci): accept program PRs by their Program-Unit marker (D-024-131)`, English body per STANDING 14, CI green (`gh pr checks`, paste). This PR is itself the first to exercise the rule once merged; note that its own `regime` run uses the pre-fix checker and may stay red; say so in the report.

VERIFY
Commands above; `git diff --stat origin/main...HEAD` (expect a handful of files). Network: `api.github.com`, `github.com` only.

TIMEBOX
40 minutes.

FORBIDDEN
No other checker rules changed; no edits outside SCOPE; no merge; no rebase.

REPORT
≤ 150 words: branch, head sha, PR link, CI state, the diff stat, the exact regex, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` before any command.
