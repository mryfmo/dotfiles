# U321 a `router` role of hcom-seat: the superagent Router under srt with the loopback grant its panel and Management API need

GOAL
U317b measured (2026-11-07T00:12Z, the unpacked prototype at pin 8c32a9dc: `src/index.ts:8` injects `webServer`, `runtime.ts:203` `registerHttp`, cordis `fiber.ts:614` leaves the Runtime inactive without it) that dsh-superagent's Runtime does not start without the `dsh-host-webserver` plugin, so the Router needs a loopback listener on `127.0.0.1:<port>`, which the dsh role of `hcom-seat` forbids (`allowLocalBinding: false`, the role's srt settings). The round-1 verdict of PR 711 (`verdicts/U317-6eac2332.md`) names this as P1 `cordis.patch.yml:27`. This unit adds a `router` role to `hcom-seat`: the dsh role's containment (per-launch slot, the write roots `DSH_HOME`, the slot, the role's omp profile, `~/.omp/run`; the denies of the checkout, the store, the hcom stores and every credential root; the four-probe canary; the `OMP_PROFILE` and the placed profile config of U310) plus two rows of its own: `allowLocalBinding: true` for that role alone, and the Router state root `$DSH_HOME/router-state` as a write root (U317b moves the state there). The role's profile is `router` (`hcom-seat router --profile router`), the only profile the role accepts. No other role's rendered settings change by a byte (the existing byte-identical test over the earlier heads holds the omp roles; add the dsh role to it).

SCOPE
Branch `feat/hcom-seat-router-role` from the U318 head named in the TASK (U318 reshapes the shim's login rows; this unit builds on it); the tree is `/tmp/dotfiles-wt/U321` (created by the coordinator). May write: `scripts/orchestrator/hcom-seat` and its generated copy `home/dot_local/bin/common/executable_hcom-seat` (byte-identical, regenerated), the lever pins by regeneration (`home/dot_agents/agent-config.yaml` `claude.levers.sha256` rows, `scripts/generated-agent-outputs.json`), `tests/unit/test_hcom_seat_dsh.py` (or a new `tests/unit/test_hcom_seat_router.py` in the same shape), `docs/deepseek-harness.md` (one paragraph), `scripts/orchestrator/README.md` (the role table), and the body `../U321-pr-body.md`. Not: the thak or router profile files (U317b owns them), the manifest beyond the pin rows, the omp roles' rows, `seat-login-preflight`.

CONTEXT
Read the dsh role whole in `hcom-seat` (the role table near `:85-127` on origin/main, `seat_write_roots`, `settings_judge` and its own-profile and overlap rules, the canary, the launch, the profile-config check and write of U310/U310b), the srt settings writer (where `allowLocalBinding` is rendered) and the `test_hcom_seat_dsh.py` fixtures (the recorder `srt`, the scratch HOME, the byte-identical settings test). The `router` role is the dsh role with a different profile name and two more rows; model it as a second row of the same table (Model the Domain), never as a copy of the dsh branch. The loopback grant is the only grant that distinguishes it; the brief's threat table must say what a Router that binds loopback can reach (other local listeners on the host: the omp gateway children bind nothing; the hcom store is sqlite; `regime-url-opener` listens on 1456 on the laptop) and why `allowLocalBinding` is still inside the goal's sandbox clause (the Management API accepts `127.0.0.1` and `localhost` hosts only with the `x-orchestrator-request` header, upstream `docs/006-deployment.md`). The port is rendered from the manifest (`assets.dsh-superagent.sources.webserver.port` if U317b adds it, else the profile's `webserver.port`); the role grants binding, not a port.

DATA SHAPE
One more row of the role table: `router` = the dsh row's containment with `profile: router`, `allow_local_binding: true`, and `write_roots + $DSH_HOME/router-state`. The rendered settings of the omp roles and the dsh role stay byte-identical to the earlier heads; the router role's rendered settings differ from the dsh role's in exactly the `allowLocalBinding` value and the one extra write root (a test asserts that diff and nothing else).

CHANGE
1. The `router` row in the role table; `hcom-seat router [--profile router] [--home <DSH_HOME>] -- <args>` accepted; any other profile name refused for the role.
2. The settings writer renders `allowLocalBinding` from the role row (true for router, false for every other role) and the extra write root; `settings_judge` treats `$DSH_HOME/router-state` like the other DSH_HOME paths.
3. Tests: the router role's rendered settings equal the dsh role's except the two rows (a structural diff test); the omp and dsh roles byte-identical to the earlier heads; a `router` launch dry run prints the launch line with `--profile router`; another profile refused; the canary still runs; the slot cleanup unchanged.
4. Docs: `docs/deepseek-harness.md` and `scripts/orchestrator/README.md` gain the role with its two differences and why.
5. The body: Summary, Contract (the router role is the dsh role plus the loopback grant and the state root; nothing else widens; Left out: the port's provenance (U317b), the Router's first real launch (the coordinator's stage A)), Threat table `row | risk | status | evidence` per changed path plus a row for the loopback grant (what it exposes, why bounded) and the orchestrator effect, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh <the router module if new> tests.unit.test_scratch_git -v` OK (counts pasted; the new tests named).
2. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0; `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
3. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. A scratch dry run `hcom-seat router --seats-root /tmp/u321/seats --home /tmp/u321/dsh-home --profile router --dry-run -- --version` exit 0 with the launch line, and the rendered settings file showing `allowLocalBinding: true` and the router-state root (pasted); the same with `--profile thak` refused (pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge and `make deploy-kit`, the coordinator runs stage A of U317 (the Router under the role: the canary line, the setup-wait lines, the listener on 127.0.0.1 only).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the dsh role's audited containment as the router role's base and the upstream Management API's loopback-only host check as the bound of the one grant it adds; it reads no credential, widens no other role, and changes nothing a seat executes.

TIMEBOX
60 minutes.

FORBIDDEN
No change to any omp role or the dsh role's rows; no `allowNestedUserNamespaces`; no new domain; no write under the real `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local/state/omp-seats`, `~/Workspace` (scratch HOME under `/tmp/u321/` only); no seat launch beyond the dry run; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u321/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U321` and the coordinator fetches it by path.
- Progress line at `../U321-progress.txt` after every step; first edit within ten minutes. Final report to `../U321-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Model the Domain: one more row of the role table; Boundary Discipline: the grant is the smallest that lets the upstream listener exist, and the upstream's host check bounds it).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the U318 head), the structural diff between the router and dsh settings, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `verdicts/U317-6eac2332.md`; `briefs/U272-hcom-seat-dsh-role.md`; `briefs/U310b-*.md`; `briefs/U318-*.md`; `briefs/U317b-*.md`; `units.tsv` row U321.
