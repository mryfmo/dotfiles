# U317b round 2 of U317: the Router's state under a dsh write root, no listener until a router role exists, the upstream build under srt, every producer read

GOAL
The round-1 audit of PR 711 (head 6eac2332, `verdicts/U317-6eac2332.md`) returned three P1 and seven lower findings:
- P1 `home/dot_dsh/profiles/router/cordis.patch.yml:30`: `stateDir` is `~/.local/state/dsh-router/state`, outside every dsh-role write root (DSH_HOME, the per-launch slot, `~/.omp/profiles/dsh`, `~/.omp/run`), so the sandboxed launch cannot create the Router store.
- P1 `:27`: the profile asks for a listener on `127.0.0.1:3082` while the dsh role sets `allowLocalBinding: false`; the panel and the Management API cannot bind.
- P1 `scripts/update-agent-assets.sh:2421`: `pnpm install` and `pnpm build` run the upstream build scripts through mise outside srt, against the TRUST sentence "the upstream code is run only inside srt" (the auditor's scratch build wrote outside the permitted roots).
- P2 `scripts/orchestrator/intake-observe.py:169`: the new lever has no startup hash self-check (an altered installed copy ran); P2 `scripts/update-agent-assets.sh:2347`: only the router leaf is link-checked, a linked `profiles/` parent redirects the pnpm writes; P2 `:2403`: only the first archive member's root is validated (a two-root archive with the matching digest installed the second root's `package.json`); P2 `intake-observe.py:185`: a created `decisions.tsv` lacks its header, which `rounds-check.py` rejects; P2 `tests/unit/test_update_agent_assets.py:5317`: no failure injection for the three `mktemp` reads; P2 the threat table omits `scripts/generated-agent-outputs.json` and the decisions.tsv orchestrator-effect row, and several closed rows carry no failing selector.
- P3 `intake-observe.py:182`: an unreadable existing table tracebacks (exit 1) instead of the documented one-line refusal (exit 2).
CI at the head fails the Ubuntu test legs (run 42314365921; the failing tests are in `/tmp/u317b/ci-failures.txt` when the coordinator has them, else read the run with the test names the coordinator pastes in the TASK). Every finding is fixed in this round (order 35).

SCOPE
The same branch `feat/dsh-superagent-asset-observe` and PR 711; the tree is `/tmp/dotfiles-wt/U317` at 6eac2332. May write: the U317 SCOPE files (`home/dot_agents/agent-config.yaml` for the asset entry only, `scripts/validate-agent-assets.py`, `scripts/generate-agent-configs.py` and the rendered `home/dot_dsh/profiles/router/*`, `scripts/update-agent-assets.sh`, `scripts/lib/installer-pins.sh`, `scripts/orchestrator/intake-observe.py` and its deployed copy, the three test modules, `docs/deepseek-harness.md`, `scripts/generated-agent-outputs.json`) and the body `../U317b-pr-body.md` (the round-1 body `/tmp/dotfiles-wt/U317-pr-body.final.md` plus a Round 2 section). Not: `hcom-seat` or any role row (a `router` role with the loopback grant is a later unit, U321), the thak profile, the omp gateway plugin.

CONTEXT
The archive is unpacked at `/tmp/u317/work/dsh-superagent-prototype-8c32a9dc5d72c033816c6a8110b37f40cf94fba4/`; the webserver lives in `src/app/http.ts` and is wired from `src/index.ts`, and `@deepseek-ai/dsh-host-webserver` is a dependency of the prototype's `package.json`. Measure first (read the two files, then run the profile's `--dump-config` on a scratch `DSH_HOME` if the stub harness allows): whether the Runtime (Sources polling, Policy, the Store) starts when the `dsh-host-webserver` plugin row is disabled in the profile patch, or whether `src/index.ts` requires the HTTP server to construct the app. The two outcomes decide CHANGE 2. Lever self-check precedent: every pinned lever under `home/dot_local/bin/common/` verifies its own sha256 against the manifest at startup (`lever_self_check` in `hcom-seat`; the Python levers do the same through the manifest's `claude.levers.sha256` block, see `scripts/orchestrator/brief-check.py` and `rounds-check.py` for the Python form). The updater's existing containment precedent: none builds under srt today (`update_deepseek_harness` builds in place under `make update`); this round makes the new step the first to run its build inside `srt --settings <scratch settings>` with writes limited to the build directory and a scratch pnpm store under `$DSH_HOME`, network to the registry hosts the lockfile names, and names the harness build as a residual (U322) in the body. `rounds-check.py` reads `decisions.tsv` with the header `ts\tphase\tdecision\twhy\tevidence\tresult`.

DATA SHAPE
The Router's state is `$DSH_HOME/router-state` (a dsh write root), rendered from the manifest. The profile declares no listener until a `router` role exists (the webserver plugin disabled by id in the patch when the measurement allows; the Management API and panel are stage-B items on U321). The build is one `srt` invocation with a settings file the updater writes beside the build directory (allowWrite: the build directory and `$DSH_HOME/.pnpm-store`; denyRead: the credential roots the dsh role denies; network: the registry hosts). Every archive member's first path component equals the one root. The lever verifies its own digest at startup like its peers. A created `decisions.tsv` carries the header; a failed read of the table is the one-line refusal, exit 2.

CHANGE
1. `stateDir` to `$DSH_HOME/router-state` (rendered; the test asserts it is under a dsh write root by string).
2. Outcome A (the Runtime starts without the webserver): disable the `dsh-host-webserver` row by id in the router patch, drop the `webserver {host, port}` block, and name the Management API and panel as stage B on U321 in the body. Outcome B (the webserver is required): keep the rows, hold the PR, and write the measurement into the report; the coordinator opens U321 first.
3. `update_dsh_superagent`: resolve `$DSH_HOME` and `profiles/` physically and refuse a link anywhere on the path (the `settings_judge` physical-path rule); validate every archive member's first component against the one root before unpacking; run `pnpm install --frozen-lockfile` and `pnpm build` inside `srt --settings <file>` as DATA SHAPE says, refuse when `srt` is absent (the kit pins it in mise) with the exit status read; failure-injection tests for the three `mktemp` reads, the link refusal, the two-root archive, and a build that writes outside its directory (denied by srt, the step fails).
4. `intake-observe.py`: startup digest self-check against the manifest's `claude.levers.sha256` entry in the form the other Python levers use; a created `decisions.tsv` gets the six-column header; a table that cannot be read refuses with one line and exit 2 (test for each).
5. Tests: as named above, plus the CI failures of the round-1 head fixed (the coordinator names them in the TASK).
6. The body: the round-1 body plus `## Round 2` (the findings quoted with their fixes, the webserver measurement), the threat table gaining `scripts/generated-agent-outputs.json` and the decisions.tsv orchestrator-effect row, a failing selector on every closed row, the TRUST sentence true of the code (the build inside srt, the Router inside the role).

ACCEPTANCE
1. `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
2. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0; `grep -c 'router-state' home/dot_dsh/profiles/router/cordis.patch.yml` prints 1 or more; `grep -c 'dsh-router' home/dot_dsh/profiles/router/cordis.patch.yml` prints 0.
3. `uv run python -m unittest tests.unit.test_dsh_profile tests.unit.test_update_agent_assets tests.unit.test_intake_observe tests.unit.test_generate_agent_configs tests.unit.test_scratch_git` OK (count pasted; the new tests named); plus the module(s) of the CI failures the TASK names.
4. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. `cmp scripts/orchestrator/intake-observe.py home/dot_local/bin/common/executable_intake-observe.py` exit 0; an altered copy of the deployed lever refuses at startup naming the digest (pasted).
6. The auditor's three reproductions re-run against the new head on a scratch tree: the two-root archive refused before unpack; the linked `profiles/` parent refused; the build fixture that writes outside its directory fails the step under srt (pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section; the coordinator re-runs item 6 on the pushed head.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts `hcom-seat`'s dsh role as the Router's containment, srt as the build's containment, and the updater's digest and single-root checks as the supply-chain gate; it writes only under `$DSH_HOME` (the plugin, the profile, the router state, the pnpm store) and reads no credential; the upstream code runs only inside srt.

TIMEBOX
90 minutes.

FORBIDDEN
No change to `hcom-seat` or any role row; no `allowLocalBinding`, `allowNestedUserNamespaces` or new domain outside the registry hosts the lockfile names; no model id outside `model_profiles`; no API key row; no token or `GH_CONFIG_DIR` content in any tracked file or the body; no edited copy of upstream code; no `scripts/dsh-superagent` or tmux launch; no write under the real `~/.dsh`, `~/.omp`, `~/.local/state`, `~/Workspace`; no network except the srt-contained scratch build if you run one; no push; no `gh` call; no pipe `|` in any bash command (order 46: output to a file under `/tmp/u317b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; stop at a committed head in `/tmp/dotfiles-wt/U317`.
- Progress line at `../U317b-progress.txt` after every step; first edit within ten minutes; final report to `../U317b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`; every message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline: srt is the boundary for every upstream execution; Fix Root Causes: the state moves inside the roots instead of a new grant).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against 6eac2332), the webserver measurement and the outcome taken, the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (orders 7, 21, 27, 29, 33, 34, 35, 36, 41, 42, 44, 46); `verdicts/U317-6eac2332.md`; `briefs/U317-dsh-superagent-asset-github-source-observe-router-under-the-dsh-role.md`; `briefs/U272-hcom-seat-dsh-role.md` (the write roots and the physical-path rule).
