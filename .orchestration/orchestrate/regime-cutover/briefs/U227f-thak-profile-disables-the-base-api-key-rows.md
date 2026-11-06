# U227f the thak profile disables the two base rows that name a DeepSeek API key

GOAL
The goal sentence's DSH clause is measured as "the model route is claude-bridge; no API key row and no Ollama row" (`handoff/08-purpose-and-goal.md` §1). The first host judgment (U288, `tests/ng-u288.md`, row `d20`) ran `DSH_HOME=$HOME/.dsh ~/.dsh/bin/dsh --profile thak --dump-config` on the deployed kit: the omp-gateway row is on claude-bridge, `llm-deepseek` is disabled and no key value appears, but two `@deepseek-ai/dsh-base` rows, `web-search-deepseek` and `web-deepseek-api`, carry `apiKeyEnv: DEEPSEEK_API_KEY` and the thak profile's `cordis.patch.yml` leaves them enabled. The operator's route decision (login only, U242) covers DeepSeek's web search too: a row that would read a DeepSeek key from the environment is an API-key route, enabled or not reachable today. This unit disables the two rows in the thak profile patch and pins the measurement.

SCOPE
A new branch `fix/thak-profile-no-api-key-rows` from `origin/main` (your tree is `/tmp/dotfiles-wt/U227f`). May write: `home/dot_dsh/profiles/thak/cordis.patch.yml` (and `package.json` beside it if a row's removal needs it), the tests that pin the profile (`tests/unit/test_dsh_profile*.py` or where U227's tests live; find them by `grep -rl cordis.patch tests/unit`), `tests/dsh-login-route.tsv` only if a row there states the API-key expectation, `docs/deepseek-harness.md` (the profile paragraph, one sentence), and the body `../U227f-pr-body.md`. Not: the plugin, the updater, the DSH pin.

CONTEXT
Read `cordis.patch.yml` and the DSH architecture document at the pinned commit (`docs/architecture.md` "Profiles and bundles": a patch replaces a row by id, `--dump-config` prints the resolved rows) as the kit's `docs/deepseek-harness.md` quotes it; the U227 body (PR 686) for how the profile rows and their tests were built; the d20 entry of `tests/ng-u288.md` for the measured output. A disabled row stays in the dump with `enabled: false`; the test asserts, on the dumped config of the fixture profile, that no enabled row carries `apiKeyEnv`, and names the two ids.

DATA SHAPE
Two patch rows by id (`web-search-deepseek`, `web-deepseek-api`) with `enabled: false`, beside the existing patch rows; one assertion over the dumped config: every row with an `apiKeyEnv` key is disabled.

CHANGE
1. The two patch rows; the test; the docs sentence.
2. Measurement on this host, read-only for the real tree: with a scratch `DSH_HOME` under `/tmp` holding the installed dsh tree linked (as U251 and U272 did) and the profile from your tree, `dsh --profile thak --dump-config` shows the two rows `enabled: false` and no enabled row with `apiKeyEnv`; paste the relevant lines.
3. The body: Summary, Contract, Threat table, Verification (ACCEPTANCE pasted), the d20 row quoted.

ACCEPTANCE
1. `uv run python -m unittest <the profile test module>` OK (paste the count; the new test named).
2. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `make render-check` exit 0 (if the profile is rendered).
3. The CHANGE 2 lines pasted.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge and the deploy, the coordinator re-runs `tests/run-host-rows.py` and the d20 row reads OK.

CLOSURE
remove

TRUST
TRUST: the unit trusts the profile patch mechanism as DSH documents it and the operator's route decision; it changes two rows and a test, reads no credential and makes no `/v1/messages` request.

TIMEBOX
30 minutes.

FORBIDDEN
No `/v1/messages` request; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local`, `~/Workspace`; no change to the DSH pin or the plugin; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u227f/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U227f` and the coordinator fetches it by path.
- Progress line at `../U227f-progress.txt`; first edit within ten minutes. Final report to `../U227f-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol: two rows and one assertion).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `tests/ng-u288.md` d20; PR 686 (U227) as the profile's origin; the frame row of 2026-11-06T03:31:38Z.
