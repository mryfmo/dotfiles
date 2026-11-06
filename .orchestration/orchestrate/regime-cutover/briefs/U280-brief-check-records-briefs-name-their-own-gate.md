# U280 brief-check lets a records-only brief name its own check as the test gate

GOAL
`scripts/orchestrator/brief-check.py` (U249) requires, when a brief's SCOPE names a repository path, that ACCEPTANCE name one lint gate and one test gate from its `GATES` table (`make format` or a `scripts/ci/run-on-lint-files.sh` check; `python -m unittest`, `make unit-test` or `node --test`). On 2026-11-06 the records-only brief U274 (tables written under the store's `tests/`, no repository file changed) was refused by main's checker for naming no gates, and the coordinator had to add a unit-test line unrelated to the unit's work to pass. The rule is right for code briefs and wrong for a brief that changes no repository file: the gate that proves a records unit is its own check script. This unit adds a `records` test-gate term so that `python3 -I <path>/check-tables.py` (any `check-*.py` run with `python3 -I`) counts as the test gate, and keeps the lint gate requirement (store markdown is synced into the repository where prettier runs).

SCOPE
A new branch `fix/brief-check-records-gate` from `origin/main` (your tree is `/tmp/dotfiles-wt/U280`). May write: `scripts/orchestrator/brief-check.py`, `tests/unit/test_brief_check.py`, `scripts/orchestrator/README.md` (the brief-check paragraph, one sentence), and the body `../U280-pr-body.md`. Not: any brief in the store, the CI workflow.

CONTEXT
Read `brief-check.py` whole (the `GATES` table and the SCOPE path rule, with their docstring quoted in this brief's GOAL) and `tests/unit/test_brief_check.py`. The U274 brief (`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/briefs/U274-use-case-test-tables-macos-first.md`, read-only) is the case: its ACCEPTANCE 1 is `python3 -I U274-tables/check-tables.py U274-tables/*.tsv`; its lines 6 and 7 were added to pass and would be unnecessary under this rule.

DATA SHAPE
One new row in `GATES`: class `test`, name `records-check`, term a regex matching `python3 -I` followed by a path whose last component starts with `check-` and ends with `.py`. No other rule changes: SCOPE path detection, the lint class and the sweep-brief exemption stay.

CHANGE
1. The row; the docstring sentence that lists the test class gains the term.
2. Tests: a brief whose ACCEPTANCE names only `python3 -I tests/check-tables.py` and a run-on-lint-files check passes; the same brief with `python3 tests/check-tables.py` (no `-I`) is refused with the existing `names no test gate` line; the existing tests stay.
3. Measurement: run the checker on a copy of the U274 brief with its lines 6 and 7 removed and line 6's prettier check kept (so: 1 to 5 plus the prettier line); exit 0; paste. Run it on the U274 brief as it is; exit 0.
4. The body: Summary, Contract, Verification (ACCEPTANCE pasted), Threat table (one changed script).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_brief_check` OK (paste the count; two new tests named).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. The CHANGE 3 measurement pasted.
4. `python3 -I scripts/orchestrator/brief-check.py` over every brief in the store's `briefs/` directory exits 0 for every brief that passed before (paste the count of briefs checked and the count of refusals, with the refused names if any differ from a run of the origin/main checker over the same set).
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the GATES table as the single place the rule lives and adds one row; it reads the store's briefs read-only and changes no brief.

TIMEBOX
30 minutes.

FORBIDDEN
No change to any brief in the store; no change to the lint class or the SCOPE rule; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u280/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U280` and the coordinator fetches it by path.
- Progress line beside your tree (`../U280-progress.txt`) every ten minutes at most. Write your final report to `../U280-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Encode Lessons in Structure: the rule is a table row, not a new branch; Laziness Protocol).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the new GATES row, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `AGENTS.md` (Test Policy); `briefs/U249-*.md` (the gate's origin); `briefs/U274-use-case-test-tables-macos-first.md` (the case).
