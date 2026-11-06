# U249 brief-check.py refuses a brief whose ACCEPTANCE names none of CI's gates

GOAL
Standing order 44 (2026-11-06): two heads passed every ACCEPTANCE line their briefs named and failed CI minutes later, one at the prettier check (U244, d1fd54ba) and one at the shebang table of `scripts/ci/run-on-lint-files.sh` (U240, dc336b67), because the briefs named their own lines and not the gates CI runs. The lesson becomes a check, not a sentence: `scripts/orchestrator/brief-check.py` refuses a brief whose ACCEPTANCE section names none of the CI gates, so no TASK goes out without them (the `hcom-orchestration` skill sends no TASK while the checker exits non-zero, and `pr-audit.sh` runs the checker before every audit).

SCOPE
A new branch `feat/brief-check-ci-gates` from `origin/main` b49be338 (your tree is `/tmp/dotfiles-wt/U249`; if it is absent, wait 30 s and look again). May write: `scripts/orchestrator/brief-check.py`, its deployed copy `home/dot_local/bin/common/executable_brief-check.py` (byte-identical; find how the copy is kept in step before you copy by hand), `tests/unit/test_brief_check.py`, the checker's pin in `home/dot_agents/agent-config.yaml` only if the manifest pins it by sha256 (regenerate, never edit by hand), `scripts/generated-agent-outputs.json` if the generator rewrites it, the checker's paragraph in `scripts/orchestrator/README.md`, and the body `../U249-pr-body.md`. Not: any other lever, `AGENTS.md`, any brief.

CONTEXT
Measured at b49be338. `brief-check.py` reads one brief, finds sections by heading (`sections()`), and refuses on trigger terms without CLOSURE and TRUST, dressed forms, and lever counts in SCOPE (`:1-30`, the `TRIGGERS` table at `:177`, `DRESSED_PHRASES` at `:210`, the SCOPE lever rule at `:214`). The Makefile's lint target runs `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` and `scripts/ci/run-on-lint-files.sh markdown prettier --check` (`Makefile:217-220`); CI's test job runs the same three then the unit tests. Every unit brief has an ACCEPTANCE section (the `hcom-orchestration` skill step 1 names it).

DATA SHAPE
One more table in the checker: `GATES`, a tuple of (name, pattern) rows naming the gate forms a brief may paste: `run-on-lint-files.sh`, `make lint` or `make format` (whichever the Makefile target is called; read it), `python -m unittest` or `make unit-test`, `make shellcheck`, `make render-check`, `make validate-agent-assets`, `node --test`, `bats` is not one (AGENTS.md Test Policy forbids local bats). The rule: the ACCEPTANCE section exists and matches at least one lint-class gate (`run-on-lint-files.sh`, `make lint`/`make format`) and at least one test-class gate (`unittest`, `make unit-test`, `node --test`); each missing class is one reason line. A sweep brief (a brief whose GOAL names the `security-audit` skill run and whose SCOPE says no file of the repository changes) is exempt by that shape, not by a name list: the rule applies only when SCOPE names at least one backticked path under the repository (the existing SCOPE path reader at `:214` already finds them).

CHANGE
1. Add the `GATES` table and the ACCEPTANCE rule per DATA SHAPE, with one reason line per missing class in the checker's existing reason style (`ACCEPTANCE names no lint gate (run-on-lint-files.sh, make <target>)`, `ACCEPTANCE names no test gate (python -m unittest, make unit-test, node --test)`), and `no ACCEPTANCE section` when SCOPE names a path and the section is absent. Exit codes unchanged (1 with reasons, 2 for unreadable).
2. Tests in `tests/unit/test_brief_check.py`: a brief with both gates passes; one with only a lint gate fails with the test-gate reason; one with only a test gate fails with the lint-gate reason; a sweep-shaped brief (SCOPE with no repository path) passes without either; a brief with a repository path and no ACCEPTANCE fails with the section reason. Run the module plus `tests.unit.test_scratch_git`.
3. Run the new checker over every brief in the store that is still in flight today (`U240`, `U240b`, `U244`, `U249` itself, `U250` if present) and paste the results into the body; a brief that fails is the coordinator's to amend, not yours.
4. The README paragraph on the checker: one sentence on the ACCEPTANCE rule and its two classes.
5. The body `../U249-pr-body.md`: Summary, Contract (guarantee: a brief whose SCOPE names a repository path and whose ACCEPTANCE names no lint gate or no test gate is refused; leaves out: whether the gates were run, which the coordinator reads from the body's pasted lines), Verification (ACCEPTANCE pasted), the CHANGE 3 table.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_brief_check tests.unit.test_scratch_git` OK (paste the count; the five new tests named).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0.
3. `cmp scripts/orchestrator/brief-check.py home/dot_local/bin/common/executable_brief-check.py` exit 0.
4. If the manifest pins the checker: `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 with no diff; otherwise the grep showing no pin.
5. `python3 -I scripts/orchestrator/brief-check.py .orchestration/orchestrate/regime-cutover/briefs/U249-brief-check-requires-the-ci-gates-in-acceptance.md` exit 0 (this brief names both classes).
6. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the checker's existing section reader and SCOPE path reader as the places the new rule hangs on, and the Makefile's lint target as the list of gates; it reads no network, changes no other lever and does not judge whether a gate was run.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `pr-audit.sh`, `pr-merge.sh` or any brief; no new trigger term; no local bats; no network; no push; no `gh` call.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 52)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U249` and the coordinator fetches it by path.
- Progress line beside your tree (`../U249-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Encode Lessons in Structure is the principle this unit serves).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, the CHANGE 3 results in one line, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44); `AGENTS.md` (Comment Policy, Test Policy); the `decisions.tsv` frame row of 2026-11-06 for order 44.
