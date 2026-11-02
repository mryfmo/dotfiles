# U137 the network-bounds exemption names a README paragraph by a marker, not by its whole text

GOAL
`tests/unit/test_network_bounds.py` exempts documentation lines that mention `curl`, `wget` or `codex` without running them, and keys each exemption by the line's exact text (the `Exempt(...)` tuples around lines 391 to 402). Every unit that edits one of those paragraphs in `scripts/orchestrator/README.md` breaks two tests and loses an audit round unless it also rewrites the string: U130 at ff55f3a0 (2026-10-31, run 41188836486) and U136 at fce9518b (2026-11-01, verdict P1 README.md:118) both paid it. An exemption whose key is the prose it exempts fails on every edit of that prose and never on the thing it guards. The key becomes something that identifies the paragraph and survives its edits, while the guard still refuses a documentation line that starts running the tool.

SCOPE
One branch `test/network-bounds-exemption-by-marker` from `origin/main`. May write: `tests/unit/test_network_bounds.py`, and `scripts/orchestrator/README.md` only if the marker form needs a visible anchor there (prefer none). No lever.

CHANGE
1. Read the module's exemption model first (`grep -n 'Exempt\|def test_no_exemption_is_stale\|def test_every_curl' tests/unit/test_network_bounds.py`, then bounded reads). Name the data shape in the body: today `(path, exact line text) -> Exempt(reason)`.
2. The key for a README paragraph becomes `(path, the paragraph's opening phrase)`: the line's text up to its first period (`Regime-cutover U104 (handoff R1) and U121 (standing order 37).`), matched as a prefix. The stale check stays: a prefix that matches no line is stale; a prefix that matches two lines is ambiguous and refuses. The exemption still applies only to lines whose tool mention is inside backticks or prose, exactly as the module decides today; a matched line that holds a bare `curl ` or `wget ` command outside backticks is not exempt (test it).
3. Non-README exemptions keep their current key; the body says which entries changed and which did not.
4. Tests, behaviour only: an edit after the opening phrase of an exempted README paragraph keeps the two tests green; a paragraph removed makes the exemption stale; a bare command inserted into an exempted paragraph fails the bound test; two paragraphs with the same opening phrase are refused as ambiguous.
5. Red proof on a `git archive` of `origin/main`: append one word to the end of the brief-check README paragraph in the archive and run the module; two tests fail. On this head the same edit keeps the module green.

ACCEPTANCE
1. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_network_bounds` OK (paste the Ran line) and the broader `tests.unit.test_regime_ci tests.unit.test_workflow_security` OK. 2. ruff format check; `scripts/lint-comparisons.py --changed` exit 0. 3. The PR body's Contract states the key, the two refusals (stale, ambiguous), and what is left out: the set of exempted paragraphs is unchanged, no new exemption is added.

CLOSURE
allowlist: the exemption table stays a closed list; only its key changes from the whole line to the opening phrase, matched once.

TRUST
TRUST: the unit trusts the module's existing judgement of what a documentation mention is (backticks or prose, no bare command) and trusts the README's opening phrases to stay unique per paragraph; it does not read the README's meaning.

TIMEBOX
30 minutes.

FORBIDDEN
No new exemption; no change to the network bound itself or to any workflow; no lever edit; no `gh` call; no edit outside SCOPE.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U137-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U137-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path), `## Verification` (the result lines and the red proof), the line `Program-Unit: regime-cutover/U137`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md`; ledger rows U130 2026-10-31T09:50:00Z and U136 2026-11-01 (the incorrect row at fce9518b); Encode Lessons in Structure.
