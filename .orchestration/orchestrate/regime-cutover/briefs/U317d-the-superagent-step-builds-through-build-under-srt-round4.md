# U317d round 4 of U317: the superagent step builds through `build_under_srt`; its own settings builder is deleted

GOAL
The round-3 audit of PR 711 (verdicts/U317c-41af8592.md, class sandbox-boundary) found three P1s in `update_dsh_superagent`'s own srt run (`dsh_superagent_srt_settings` and `dsh_superagent_srt_run`, scripts/update-agent-assets.sh:2626-2673 at 41af8592): `/usr/bin/env -i` runs inside srt and drops the HTTP_PROXY and HTTPS_PROXY srt injects, so a cold pnpm install cannot reach the registry (:2667); `denyRead` omits `~/.claude`, `~/.config/gh` and `~/.omp/profiles` (:2634); `denyWrite` is empty, so srt's implicit roots stay writable (:2639). Three P2s follow from the same builder: the settings file is opened with truncation through a link (:2663), the pnpm store has no physical-path check (:2797), and the fake-run test dictionary calls `real_srt()` eagerly (tests:6439). Every one of these is what U322 fixed in `build_under_srt` (same file, :1830 at this head, merged into the branch by U317c): env -i outside srt, the dsh role's full read-deny list plus the checkout, the write denies in every spelling, the settings created 0600 under noclobber at a path that must be absent and not a link, the store resolved physically. The fix is not a fourth settings builder; it is one builder. The superagent step calls `build_under_srt` for its two pnpm runs, and its own builder, runner and the environment variables only they read are deleted.

The third P1 is docs: `docs/deepseek-harness.md` names a Router launch under the dsh row with `allowLocalBinding: false` (the audit's :141; the step's comment at :2678 says the same, `hcom-seat dsh --profile router`), while main's router role (U321) is the launch that grants the listener. Both sentences name `hcom-seat router`.

SCOPE
The same branch `feat/dsh-superagent-asset-observe` and PR 711; the tree is `/tmp/dotfiles-wt/U317` at 41af8592 (clean). May write: `scripts/update-agent-assets.sh` (the superagent step only: `update_dsh_superagent`, `dsh_superagent_srt_run`, `dsh_superagent_srt_settings`, `dsh_superagent_clean_path` if nothing else reads it, the `DSH_SUPERAGENT_SRT`, `DSH_SUPERAGENT_PNPM`, `DSH_SUPERAGENT_PATH`, `DSH_SUPERAGENT_STORE` plumbing if nothing else reads it; `build_under_srt` itself is not touched), `tests/unit/test_update_agent_assets.py` (the `DshSuperagentTest` group), `docs/deepseek-harness.md` (the one sentence), `scripts/orchestrator/README.md` only if it repeats the dsh-row launch sentence, and the body `../U317d-pr-body.md` (the round-3 body `/tmp/dotfiles-wt/U317c-pr-body.final.md` plus `## Round 4`). Not: `build_under_srt`, the harness step, hcom-seat, the manifest beyond what the generator rewrites.

CONTEXT
`build_under_srt <dir> <settings> [host...] -- <command...>` (header :1786-1829): `<dir>` is the directory the command runs in and may write (not a link), `<settings>` an absent path it creates 0600 and removes, the hosts the allowed domains, then the command, which srt starts from a sanitised environment with TMPDIR and the XDG and pnpm variables already pointed under `${DSH_HOME}/.pnpm-store` (the store is the second write root, made by the function). The harness step calls it three times (:2408 canary, :2420 install, :2424 build, :2443 profile install) and the test at tests:3760 counts those lines. The superagent step's two runs today are `dsh_superagent_srt_run "${settings}" "${tree}" '"$PNPM" install --frozen-lockfile ...' <roots>` and the profile install; each becomes `build_under_srt "${tree}" "${settings}" "${DSH_SUPERAGENT_REGISTRY_HOST}" -- pnpm install --frozen-lockfile` (pnpm by name: build_under_srt's PATH holds the mise pnpm and node directories), and the profile run the same with the profile directory. The canary: run the U272 canary through build_under_srt before the first build as the harness step does (:2400-2412), one write beside the tree refused. If the step needs a write root build_under_srt does not grant (it grants `<dir>` and the store), the run is restructured so the directory that must be written is `<dir>`; build_under_srt gains no argument. The registry host stays the manifest's (`DSH_SUPERAGENT_REGISTRY_HOST`); lockfile `tarball:` hosts, if the fork's lockfile has any, are read as the harness step reads them (:2413-2419) or the step refuses naming the host.

DATA SHAPE
One sandbox builder in the file. The superagent step is three `build_under_srt` lines (canary, tree install, profile install) and no settings JSON of its own; the deleted functions leave no caller (`grep -c dsh_superagent_srt_ scripts/update-agent-assets.sh` is 0).

CHANGE
1. The reproducing tests first, red at 41af8592: in `DshSuperagentTest`, (a) a fake srt that injects `HTTP_PROXY=http://127.0.0.1:1/` into its child's environment and a fake pnpm that records its environment: the recorded environment holds HTTP_PROXY (today it does not); (b) the settings file the fake srt receives holds `~/.claude`, `~/.config/gh` and `~/.omp/profiles` in denyRead and a non-empty denyWrite (today neither); (c) the step's pnpm lines are `build_under_srt` lines, the shape of tests:3760 for the harness step, and `dsh_superagent_srt_settings` is absent from the file. The existing test at tests:6489 that pins the old settings shape is replaced by (b); the dictionary at tests:6439 stops calling `real_srt()` for fake runs (the P2). 2. The step: the two runs through `build_under_srt`, the canary before the first, the two functions and the dead variables deleted, the comment at :2678 and the docs sentence naming `hcom-seat router`. 3. `uv run --with pyyaml python -m unittest tests.unit.test_update_agent_assets tests.unit.test_sandbox_portability tests.unit.test_network_bounds tests.unit.test_asset_manifest tests.unit.test_runtime_health -v` OK. 4. `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`; `make render-check`. 5. Commit `fix(dsh): the superagent step builds through build_under_srt and its own settings builder is deleted (regime-cutover U317d)` with the trailer. 6. The body: `## Round 4` names the three P1s and that one builder remains; the Threat table rows for the superagent build cite the new tests as selectors; `Program-Unit: regime-cutover/U317` once and the footer; under 65536 bytes.

ACCEPTANCE
1. The three new tests named with their red run at 41af8592 (`FAIL`/`ERROR` lines pasted) and their green run at the head. 2. `grep -c 'dsh_superagent_srt_' scripts/update-agent-assets.sh` is 0; `grep -c 'build_under_srt ' scripts/update-agent-assets.sh` is pasted (the harness step's 4 plus the superagent step's 3). 3. The five test modules OK with counts. 4. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0; render-check 0. 5. `git diff --stat 41af8592 HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the round-4 audit, the sweep and CI are the coordinator's (order 49: this is the one fix round the P1s earn; P2s left over become residual rows).

CLOSURE
remove

TRUST
TRUST: the unit trusts `build_under_srt` (U322, five audit rounds, four sweeps) as the one sandbox builder of the updater and adds no second; it trusts srt 0.0.81's settings grammar as that function writes it.

TIMEBOX
60 minutes.

FORBIDDEN
No change to `build_under_srt` or the harness step; no new settings JSON anywhere; no pin edited by hand; no rebase; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u317d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U317`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U317d-progress.txt`; final report to `../U317d-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the three tests (names, red line, green line), the grep counts, the ACCEPTANCE lines. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); `verdicts/U317c-41af8592.md`; the U322 and U322b briefs (why build_under_srt is shaped as it is); `scripts/update-agent-assets.sh:1786-1829` (the contract).
