# U272c round 2 of U272: the dsh role's read grants are its own, not the worker's

GOAL
The Codex review of PR 697 (thread 4492139503, P1, `scripts/orchestrator/hcom-seat:1450` at 52873a37) finds that the `dsh` role removes the git common directory and the hcom store only from `allowWrite`, while the shared `allow_read` construction still grants `common_real`, `hcom_real` and the checkout's orchestration records to every role; because an allowRead row re-opens a path under a broader denyRead, code running in the DeepSeek harness can read host git state and the program's hcom data despite the documented containment boundary. The round-1b audit (`verdicts/U272b-52873a37.md`, correct, 0 findings) missed it. This round makes the read grants a role row too: the dsh role's allowRead names only what the dsh process needs (its own `DSH_HOME`, its scratch slot, `~/.agents/skills`, the omp profile directory `~/.omp/profiles/dsh` the login child reads and writes, the pinned tool directories the shim and srt need), and none of the git common directory, the hcom store, the orchestration records or any other seat's paths.

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at 52873a37745d8141eada2139ea2fa76e2773a60d in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `scripts/orchestrator/hcom-seat` and the deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical), the pin rows by regeneration (`uv run --with pyyaml scripts/generate-agent-configs.py`), `tests/unit/test_hcom_seat_dsh.py`, `docs/deepseek-harness.md` (the containment paragraph, one sentence), the design file `../U272-design.md` (the role table's allowRead row), and the body `../U272-pr-body.md` (a Round 2 section, the threat table row). Not: the omp roles' settings (the worker's and orchestrator's rendered `srt-settings.json` must be byte-identical before and after, proven by the existing tests and one new comparison test).

CONTEXT
Read the thread whole (`gh` is forbidden to you; the coordinator pasted its text into `../U272c-thread.txt`), `hcom-seat` around the `allow_read` construction (`:1450` and the function that builds it) and the role table in `../U272-design.md`. The settings model: denyRead is broad, allowRead re-opens paths under it, so every allowRead row is a grant. The dsh role has no git worktree (its cwd is a scratch directory in its state slot), no hcom bus and no store, so none of the worker's read grants for those are needed. What the dsh process does need to read was measured in U272 (the ACCEPTANCE 4 launches: `--version`, the planted-binary refusals, two concurrent launches) and in M-21 (`~/.agents/skills` readable, the settings file itself read-denied); the login child needs `~/.omp/profiles/dsh` read and write (U272's deviation 1).

DATA SHAPE
One more row in the role table: `allow_read` per role; `orchestrator` and `worker` keep their rows unchanged (the shared list as it is today), `dsh` gets its own list built from the role's own paths. The construction site reads the role once, as the write roots do; no branch inside the shared list.

CHANGE
1. The row per DATA SHAPE in the lever; the deployed copy identical; pins regenerated; the design file's table and `docs/deepseek-harness.md` sentence updated.
2. Tests: the dsh role's rendered settings carry no allowRead row under the git common directory, the hcom store or the orchestration records (assert on the rendered JSON with the fixture's paths); the worker's and orchestrator's rendered settings are byte-identical to the ones rendered at 52873a37 (render both heads' settings in the fixture, compare); the existing tests stay.
3. Measurement on this host with the U272 scratch `DSH_HOME` (read-only for the real tree, write only under `/tmp`): `hcom-seat dsh --home <scratch> -- --version` prints `0.2.1-rc.5` under srt with the canary words; inside the sandbox a read of the checkout's `.git` common directory and of the hcom store directory is denied (use the lever's dry-run or a probe command passed as the dsh args if the role runs an arbitrary command; else say how you proved it); paste.
4. The body's Round 2 section quoting the thread, the change, the tests and the measurement; the threat table row for the read grants; ACCEPTANCE pasted. Write the thread reply to `../U272c-thread-reply.md` (first line `fixed: <head>`, then two sentences).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `make render-check` exit 0.
4. The CHANGE 3 measurement pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator posts the thread reply at the new head and runs the audit.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts hcom-seat's settings rendering and the srt deny-then-allow model; it adds one role row for read grants, changes no omp role's rendered settings, reads no credential and opens no network.

TIMEBOX
45 minutes.

FORBIDDEN
No change to the omp roles' rendered settings; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local/state/omp-seats` or `~/Workspace`; no `/v1/messages` request; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272c-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U272c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Model the Domain: the grant is a role row; Boundary Discipline).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the dsh allowRead list in one line, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 36, 44, 46); PR 697 thread 4492139503; `verdicts/U272b-52873a37.md`; `briefs/U272-hcom-seat-dsh-role.md`; `../U272-design.md`.
