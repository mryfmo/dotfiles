# U272 DSH runs under srt as a role of hcom-seat, not as a launcher of its own

GOAL
Four audits of the hand-written launcher `dsh-srt` (PR 687, U251 to U251d) each found a new way code under the caller's or another user's control ran before srt contained anything, and the mechanism-change row of 2026-11-06T10:4xZ withdrew it. `scripts/orchestrator/hcom-seat` already composes a seat's environment, PATH, srt settings and canary and has passed its own audits (U85 and after), so the DSH control host of the goal is contained the same way the omp seats are: by a role of that lever. This unit designs the role first (what differs from the worker role and nothing else), then builds it: `hcom-seat dsh [--profile <name>] -- <dsh args>` renders the worker seat's settings with the DSH write roots, runs the same canary, and execs `dsh` under srt through the lever's own pinned srt and environment, so the pre-containment path is the lever's existing one.

SCOPE
A new branch `feat/hcom-seat-dsh-role` from `origin/main` (your tree is `/tmp/dotfiles-wt/U272`). May write: `scripts/orchestrator/hcom-seat` and its deployed copy `home/dot_local/bin/common/executable_hcom-seat` (identical; find how they are kept in step and pinned), `tests/unit/test_hcom_seat.py` (and a new `tests/unit/test_hcom_seat_dsh.py` if the module is large), the pin rows in `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (regenerated), `scripts/orchestrator/README.md` (the role paragraph), `docs/deepseek-harness.md` (the containment paragraph), and the body `../U272-pr-body.md`. Not: the plugin, the profile rows, the updater, the omp seat roles' behaviour.

CONTEXT
`hcom-seat` (`scripts/orchestrator/hcom-seat`, about 1,900 lines): roles `orchestrator` and `worker`; it pins `srt` and the tools (`pin_exec`, `:1597-1600`), builds the per-seat `srt-settings.json` (`:1684-1748`: deny read, deny write, allow write, domains), writes the `omp` shim that runs the canary and refuses to start without `write-denied read-denied ssh-denied` (`:46-49`), composes the pane's PATH and environment (`:912-918`, `:1868`), and refuses a launch from inside a seat (`:368-374`). The four verdicts of PR 687 (`verdicts/U251-aa0001bd.md`, `U251b-f46a72b8.md`, `U251c-d49a5349.md`, `U251d-cca089f8.md`) list every pre-containment hazard found in the standalone launcher: the dsh runtime executed outside srt, the srt interpreter on the caller's PATH, the mise python3 shim, group-writable helpers, non-physical PATH entries, a traversable ancestor, NODE_OPTIONS inherited, a shared settings file across concurrent launches; read them as the hazard list the role must not reopen, and for each say in the design which hcom-seat line already closes it or what the role adds. The M-21 rows of 2026-11-06T03:50:31Z hold the DSH-specific facts (cwd a scratch root, `DSH_HOME` the write root, the settings file read-denied, `~/.agents/skills` readable). The login route's child needs `USER` in its environment (the 07:13Z measurement); the omp profile and agent directories under `~/.omp` are read-denied for a worker seat (U251's finding), so the role names the one allowRead the login child needs and no more.

DATA SHAPE
A third role, `dsh`, in the lever's role table: its differences from `worker` are rows in that table, not branches in the code: the write roots (`DSH_HOME` and a per-launch scratch root under the seat's state directory, created by the lever like a seat directory, never shared between launches), the command (`<DSH_HOME>/bin/dsh` resolved and refused like the lever refuses an unpinned tool), the environment names it passes (the worker's list plus `USER`, `DSH_HOME`, `CLAUDE_CONFIG_DIR` set to a per-launch directory under the scratch root), the one allowRead row for the omp profile the login child reads, and no pane and no hcom bus (the role runs in the foreground and returns dsh's status). Everything else (pinning, settings rendering, canary, PATH composition, refusals) is the lever's existing code, unchanged.

CHANGE
1. Design first (20 minutes): write `../U272-design.md` with the role table rows, and for each hazard of the four verdicts the hcom-seat line that closes it or the row that adds the closing; stop and report if the lever's structure cannot take a role without changing the omp roles' behaviour.
2. The role per DATA SHAPE in the lever; shdoc header rows for the role; the deployed copy identical; pins regenerated.
3. Tests: the role's settings against the worker's (only the named rows differ), the per-launch scratch root (two launches never share a settings file), the environment names, the command resolution refusals, the canary refusal, the exec argv recorded by a fake srt; the existing hcom-seat tests stay.
4. Measurement on this host with a scratch `DSH_HOME` under `/tmp` holding the installed dsh tree linked (as U251 did): `hcom-seat dsh --home <scratch> -- --version` prints `0.2.1-rc.5` under srt with the canary words; a planted `bin/node`, `bin/python3` and `bin/stat` under `DSH_HOME` never run (marker files stay absent); two launches at once each get their own settings file; paste each.
5. The body: Summary (the four rounds and why the role, with the mechanism-change row), Contract, Threat table (every changed path and the role's rows as controls), Verification (ACCEPTANCE pasted), the design file's hazard table.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_scratch_git tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named; drop the module that does not exist).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0.
4. The CHANGE 4 measurements pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The real-login turn under the role is the coordinator's `seat` item in `tests/dsh-login-route.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts `hcom-seat`'s existing pinning, settings rendering, canary and environment composition as the audited containment and adds only the role's rows; it reads no credential, opens no network of its own and does not change the omp roles' behaviour.

TIMEBOX
120 minutes, the first 20 for the design file.

FORBIDDEN
No change to the omp roles' behaviour; no new launcher file; no `/v1/messages` request to the real omp; no write under `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local/state/omp-seats` or `~/Workspace` (the measurement uses a scratch copy under `/tmp` and a scratch seats root passed by the lever's existing option if it has one, else say so); no `allowNestedUserNamespaces`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line beside your tree (`../U272-progress.txt`) every ten minutes at most; first edit within ten minutes; the design file within twenty. Write your final report to `../U272-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Subtract Before You Add; Boundary Discipline; Model the Domain: the role is rows in a table).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the design's hazard table in two lines, the ACCEPTANCE result lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 35, 36, 37, 41, 44, 45, 46); `AGENTS.md:70-72`; the four verdicts of PR 687; the `decisions.tsv` mechanism-change rows for U251 (09:55Z and 10:4xZ); `briefs/U85-*.md` (the seat containment).
