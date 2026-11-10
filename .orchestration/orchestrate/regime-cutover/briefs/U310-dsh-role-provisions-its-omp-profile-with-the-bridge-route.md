# U310 the dsh role's omp profile carries the kit's bridge route

GOAL
After PR 707 the real turn under the deployed dsh role (`cd ~/Workspace/dotfiles; hcom-seat dsh --profile thak -- 'Reply with the single word pong.'`, seat item g6, 2026-11-06T19:22Z) reached the gateway child in the role's own omp profile (`~/.omp/profiles/dsh` was created, the denies held) and failed with `omp-gateway: HTTP 404: No available model matches "claude-bridge/claude-opus-5-5"`. Measured cause: the operator's default profile carries `~/.omp/agent/config.yml` with `extensions: [~/.local/lib/omp-extensions/pi-claude-bridge]` and `modelRoles.default: claude-bridge/...`, and the omp seats get the same route through their rendered overlays (`~/.agents/omp/profiles/<role>.yml`) and the `-e` extension list hcom-seat passes; the dsh profile's `agent/` directory holds only `agent.db` and `models.db`, so the `omp auth-gateway stdio` child in it has no claude-bridge provider. This unit gives the dsh role's profile the kit's bridge route the same way the seats get theirs: a rendered overlay for the role (`dsh.yml`, generated from the manifest like `worker.yml`, with the bridge model route and the providers disabled as for the seats) that the lever places as the profile's `agent/config.yml` before the launch (the profile is the role's own write root), with the extension path taken from the manifest's `claude.levers.extensions` allow-list exactly as `omp_inputs_check` does for the omp roles. The alternative, passing `-e <bridge>` through the plugin's `args`, is the fallback only if omp's `auth-gateway stdio` does not read the profile's `config.yml`; measure which before writing (one `omp --profile dsh auth-gateway stdio` request with the config in place, as the `d11` row of `tests/dsh-login-route.tsv` does for the default profile).

SCOPE
A new branch `feat/dsh-role-profile-route` from `origin/main` (your tree is `/tmp/dotfiles-wt/U310`). May write: `home/dot_agents/agent-config.yaml` (the dsh profile rows beside the seat profiles) and `scripts/generate-agent-configs.py` with the rendered `home/dot_agents/omp/profiles/dsh.yml` (or wherever the generator writes the seat overlays; find by `grep -rn 'profiles/worker.yml' scripts home`), `scripts/orchestrator/hcom-seat` and its deployed copy (the dsh role's profile provisioning step, placed after the write-root judge and before the launch; the omp roles untouched), the pin rows by regeneration, `tests/unit/test_hcom_seat_dsh.py`, `tests/unit/test_generate_agent_configs.py`, `docs/deepseek-harness.md` (one sentence), and the body `../U310-pr-body.md`. Not: the plugin's env list (U306), the thak profile, the operator's default profile, the omp roles' rendered settings (byte-identical, the comparison test extended).

CONTEXT
Read `omp_inputs_check` and the role table in `hcom-seat` (`~/.local/bin/common/hcom-seat` is the deployed copy of main), the generator's seat-overlay rendering, `~/.agents/omp/profiles/worker.yml` as the shape (a kit overlay the generator renders; the dsh overlay carries `modelRoles.default` from the manifest's dsh route, the same `disabledProviders` and `startup` rows, `skills.enabled: false` unless the manifest says the gateway child needs skills: it does not, DSH reads `~/.agents/skills` itself), the `d11` and `h1` rows of `tests/dsh-login-route.tsv` (how the default profile's gateway child was measured), and omp's documented profile layout (`--profile=<value>  Use an isolated profile for auth, sessions, settings, and caches`; the profile's `agent/config.yml`). The provisioning writes only inside `~/.omp/profiles/dsh/agent/` (the role's write root), compares before writing (idempotent: a config already equal to the rendered overlay is left alone; a different one is replaced and the launch says so), and refuses if the profile path is a link or outside the root (the judge's rules already cover the root).

DATA SHAPE
One more row in the role table: `profile_config` for the dsh role, the rendered overlay path `~/.agents/omp/profiles/dsh.yml` placed as `~/.omp/profiles/dsh/agent/config.yml` with the extension entry set to the canonical allow-list path; the omp roles' row stays "none" (their overlays ride the launch flags as today). The overlay is one generator row set like the seats'. Idempotent placement (`cmp` before copy), refusal on a link.

CHANGE
1. The overlay row in the manifest and generator; the rendered `dsh.yml`; the provisioning step in the lever; the deployed copy identical; pins regenerated; the docs sentence.
2. Tests: the rendered `dsh.yml` carries the bridge route and the disabled providers; the lever places it when absent and when different, leaves it when equal (recorder shows no write), refuses a linked `agent/` or `config.yml`; the extension path equals the allow-list entry; the omp roles byte-identical to main.
3. Measurement on this host, read-only for the real tree except the one scratch run: with a scratch `HOME` and `DSH_HOME` under `/tmp` as U272 did, a dry run prints the provisioning line; then the measurement of CONTEXT's last sentence (does `omp --profile <scratch profile> auth-gateway stdio` with the config in place list the claude-bridge route: one `/v1/messages` request as `d11` does, expecting status 200 or the documented auth line, not 404); paste. The real g6 turn under the role is the coordinator's after deploy.
4. The body: Summary (the 404 quoted, the measured cause), Contract, Threat table per changed path, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0; `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
4. The CHANGE 3 measurements pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge and deploy the coordinator re-runs the g6 item under the role.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the manifest's extension allow-list and the seat overlays' shape; it writes only inside the role's own profile at launch, makes at most one `/v1/messages` request in a scratch profile for the measurement, reads no credential and changes no omp role's rendered settings.

TIMEBOX
60 minutes.

FORBIDDEN
No write under the real `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local/state/omp-seats` or `~/Workspace`; no change to the omp roles' rendered settings or launch flags; no change to the plugin's env list; no local bats; no network beyond the one measured request; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u310/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U310` and the coordinator fetches it by path.
- Progress line at `../U310-progress.txt` after every step; first edit within ten minutes. Final report to `../U310-report.txt` before you end; deliverables beside the worktree under `/tmp/dotfiles-wt/`, never in the store.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Model the Domain: the profile config is a role-table row rendered like the seat overlays; Make Operations Idempotent).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), the mechanism measured (profile config read by the gateway child, or the `-e` fallback), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `tests/dsh-login-route.tsv` rows g6, d11, h1; `briefs/U272-hcom-seat-dsh-role.md`; `decisions.tsv` 2026-11-06T19:22Z.
