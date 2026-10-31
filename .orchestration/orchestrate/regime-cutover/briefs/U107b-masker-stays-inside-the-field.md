# U107b A masked secret value never spans a tab or a newline

GOAL
U107 (merged 05597009, 2026-10-31T04:49Z) made the generic assignment rules of `scripts/validate-agent-assets.py` read a quoted value across an escaped quote (`<redacted:secret-pattern>

SCOPE
One branch `fix/masker-stays-inside-the-field` from `origin/main`. May write: `scripts/validate-agent-assets.py` (the generic assignment rules' value capture and the masker), `tests/unit/test_validate_agent_assets.py`. Nothing else.

CHANGE
1. The quoted-value capture of every generic rule excludes tab and newline characters at every position (an escaped quote stays inside the value; a tab or newline ends the match before it, so a value that is not closed on its line is no match). The masker's replacement therefore never removes a tab or newline, whatever the rule.
2. Tests: a TSV line holding `<redacted:secret-pattern>

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_scratch_git` OK. 2. ruff format check; `scripts/lint-comparisons.py --changed` exit 0. 3. The PR body's Contract states: a masked value lies inside one field and one line; what is left out: a secret that itself spans lines is not matched by the generic rules (the provider rules are unchanged).

CLOSURE
allowlist: the value capture is a closed character class that excludes tab and newline; the rule table and the allowlist table of U107 stay as they are.

TRUST
TRUST: the unit trusts the rule table of U107 as the one judgment of what a secret is and the TSV files' tab as the field boundary; it does not read the store's rows for meaning and trusts the records lever to call the masker on copies only.

TIMEBOX
30 minutes.

FORBIDDEN
No change to a provider rule, to the allowlist table or to any stored record; no `codex` or `gh` write.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is made by the coordinator with `worker-worktree.sh`; every command runs with it as cwd. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U107b-progress.txt`) every ten minutes at most; `grep -n` then bounded reads (the script is large; never whole); first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the PR body beside your tree (`../U107b-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification`, the line `Program-Unit: regime-cutover/U107`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; verdicts/U107-a7b060cd.md (the round-5 finding the row quotes).
