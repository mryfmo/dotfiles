# U306 the omp-gateway child runs in the dsh role's own omp profile

GOAL
The first real turn under the deployed dsh role (2026-11-06T18:49Z, `cd ~/Workspace/dotfiles; hcom-seat dsh --profile thak -- 'Reply with the single word pong.'`, the seat item g6 of `tests/dsh-login-route.tsv`) exited 1 in 9.7 s: the omp-gateway plugin's child `omp auth-gateway stdio` opened `~/.omp/agent/agent.db` and srt answered `SQLITE_AUTH: authorization denied`. The role sets `OMP_PROFILE=dsh` so that the child lives in `~/.omp/profiles/dsh` (U272's measured deviation: omp writes its agent.db at start, so the operator's `~/.omp/agent` stays denied), but the plugin spawns the gateway child with its own fixed list of environment names (the `h1` row of the login-route table: "the gateway child ran with the plugin's default env names"), and `OMP_PROFILE` is not among them, so the child fell back to the default profile the role denies. This unit makes the gateway child run in the profile the launcher names: the plugin passes `OMP_PROFILE` through when it is set (and nothing else new), with a test that pins the name in the child's environment, so the dsh role's real turn answers `pong` under srt.

SCOPE
A new branch `fix/omp-gateway-child-omp-profile` from `origin/main` (your tree is `/tmp/dotfiles-wt/U306`). May write: `home/dot_dsh/plugins/omp-gateway/gateway-client.mjs` (or wherever the child's env names are listed: `grep -n USER home/dot_dsh/plugins/omp-gateway/*.mjs`), `home/dot_dsh/plugins/omp-gateway/config.mjs` if the names are configuration, `home/dot_dsh/plugins/omp-gateway/test/*.test.mjs`, `tests/unit/test_hcom_seat_dsh.py` only if the role must also pass the name explicitly (read how the role's environment list reaches the shim), the plugin's README or `docs/pi-claude-bridge.md` (one sentence), and the body `../U306-pr-body.md`. Not: the role's deny or grant rows, the thak profile, the DSH pin.

CONTEXT
Read the plugin's child spawn (the env it builds for `omp auth-gateway stdio`), the `h1` and `h6` rows of `tests/dsh-login-route.tsv` (the env-name rule and why `USER` is kept), the role's environment composition in `hcom-seat` for the dsh role (`OMP_PROFILE=dsh`, U272 deviation 1; `grep -n OMP_PROFILE ~/.local/bin/common/hcom-seat`), omp's reading of `OMP_PROFILE` (`dist/cli.js`, as U272's design file quotes it). The plugin's default list is the plugin's security boundary for the child (it narrows the environment on purpose), so the change is one more name, passed only when set, documented beside the list.

DATA SHAPE
One more entry in the plugin's child-environment name list: `OMP_PROFILE`, forwarded when present in the plugin's own environment; the list stays the single source. A test with a fake `omp` recorder asserts the child's environment carries `OMP_PROFILE` when the plugin runs with it and does not when it is unset.

CHANGE
1. The name and its comment; the test.
2. Measurement on this host, read-only for the real tree: the plugin's own test suite (`node --test home/dot_dsh/plugins/omp-gateway/test/`) passes; the kit's hook coverage and profile tests still pass. The real turn under the role is the coordinator's after deploy (it writes under `~/.omp/profiles/dsh` and `~/.dsh`, which the worker may not).
3. The body: Summary (the g6 failure quoted), Contract (the child runs in the profile the launcher names; no other name added), Threat table, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `node --test home/dot_dsh/plugins/omp-gateway/test/` OK (paste the count; the new test named).
2. `uv run python -m unittest tests.unit.test_dsh_hook_coverage tests.unit.test_dsh_profile` OK (paste the count).
3. `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `make render-check` exit 0 (the plugin is a rendered asset if the generator lists it; else state so).
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. After the merge and deploy the coordinator re-runs the g6 item under the role.

CLOSURE
remove

TRUST
TRUST: the unit trusts the plugin's env-name list as the child's boundary and adds one name the launcher already sets; it reads no credential, makes no `/v1/messages` request and writes nothing under `~/.omp`.

TIMEBOX
30 minutes.

FORBIDDEN
No other environment name added; no change to the role's rows; no `/v1/messages` request; no write under `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local`, `~/Workspace`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u306/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U306` and the coordinator fetches it by path.
- Progress line at `../U306-progress.txt` after every step; final report to `../U306-report.txt` before you end; deliverables beside the worktree under `/tmp/dotfiles-wt/`, never in the store.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol: one name; Boundary Discipline: the list stays the boundary).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `tests/dsh-login-route.tsv` rows g6, h1, h6; `briefs/U272-hcom-seat-dsh-role.md` and `../U272-design.md` (deviation 1); `decisions.tsv` 2026-11-06T18:49Z.
