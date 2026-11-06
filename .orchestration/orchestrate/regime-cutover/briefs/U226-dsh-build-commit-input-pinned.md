# U226 the DeepSeek harness build gets its commit from the manifest, not from a .git the tag archive never has

GOAL
`update_deepseek_harness` builds the pinned tag archive with `pnpm run build`, and upstream's `scripts/client-build-environment.ts:54` runs `git rev-parse HEAD` unless `DSH_CLIENT_COMMIT_HASH` is set (its doc comment calls that variable the explicit commit source for non-Git build environments). The tag archive has no `.git`, so the first host install on 2026-11-06 failed in the build (decisions row of phase `M-14` dated 2026-11-06T03:46:22Z); the same step with `DSH_CLIENT_COMMIT_HASH=b830ec950faba0a46dda564be3e2d854afed94f1` built and installed. This unit pins the tag's commit in the manifest beside the sha256, renders it into `scripts/lib/installer-pins.sh`, and makes the updater export it for the build and refuse before any download when it is absent or malformed. Nothing else changes.

SCOPE
A new branch `fix/dsh-build-commit-input` from `origin/main` c4195463 (your tree is positioned on it). May write: `home/dot_agents/agent-config.yaml` (the `assets.deepseek-harness` entry only), `scripts/lib/installer-pins.sh` (one new constant line), `scripts/update-agent-assets.sh` (`update_deepseek_harness` and its `dsh_record` only), `tests/unit/test_update_agent_assets.py`, `tests/unit/test_network_bounds.py` (the one exemption string), the generated outputs the generator rewrites when run, and the body file beside your tree `../U226-pr-body.md`. Not: any other asset, any other updater function, the validator, `hcom-seat`, the kit profile renderer.

CONTEXT
Measured 2026-11-06 at c4195463. `assets.deepseek-harness` (`agent-config.yaml:1363-1389`) has `pin: dsh-v0.2.1-rc.5`, `sha256`, and `render: {file: scripts/lib/installer-pins.sh, constants: {DSH_PIN_TAG: pin, DSH_ARCHIVE_SHA256: sha256}}`; the generator's `render_asset_constants` (`generate-agent-configs.py:325-347`) rewrites an existing `NAME="..."` line in the render file for each constant, reading the asset field the mapping names, so the constant line must exist in `installer-pins.sh` before the generator can fill it. `ref_commit` is an asset field the validator already knows (`validate-agent-assets.py:1344`, forbidden on rolling assets only). The tag's commit is `b830ec950faba0a46dda564be3e2d854afed94f1` (`gh api repos/deepseek-ai/deepseek-harness/commits/dsh-v0.2.1-rc.5`, 2026-11-06). The build line is `update-agent-assets.sh:2161`: `(cd "${tree}" && mise exec -- pnpm install --frozen-lockfile && mise exec -- pnpm run build) || return 1`. `dsh_record` (`:1955-1957`) lists the step's commands for the receipt, and `tests/unit/test_network_bounds.py:402` holds that exact string as an exemption. The DSH tests in `tests/unit/test_update_agent_assets.py` (from `:693`) stub `mise` as a shell function that appends `"mise $*"` to a calls file and build a fake archive; `BUILD_CALLS` (`:696-698`) is what they expect.

CHANGE
1. Manifest: add `ref_commit: b830ec950faba0a46dda564be3e2d854afed94f1` to `assets.deepseek-harness`, extend `render.constants` with `DSH_COMMIT: ref_commit`, and add one sentence to `note` saying the commit is the tag's commit as read from the GitHub API on 2026-11-06 and is the build's `DSH_CLIENT_COMMIT_HASH` because the tag archive carries no git metadata.
2. `scripts/lib/installer-pins.sh`: add `DSH_COMMIT="b830ec950faba0a46dda564be3e2d854afed94f1"` beside `DSH_ARCHIVE_SHA256`; run the generator so the rendered value is the manifest's.
3. Updater, `update_deepseek_harness`: as the first producer check after the `DSH_HOME` opt-in, refuse (exit 1, a line naming `DSH_COMMIT` and the manifest field) when `DSH_COMMIT` is unset, empty, or not 40 lowercase hex; run the build as `DSH_CLIENT_COMMIT_HASH="${DSH_COMMIT}" mise exec -- pnpm run build` (a prefix assignment, so the stubbed `mise` function and the receipt see the same `exec -- pnpm run build` words); add `DSH_CLIENT_COMMIT_HASH=<commit> pnpm run build` to the `dsh_record` command list in place of `pnpm run build`, and update the `test_network_bounds.py` exemption string to the new literal.
4. Tests in `test_update_agent_assets.py`: (a) the stubbed `mise` records `DSH_CLIENT_COMMIT_HASH` when the words are `exec -- pnpm run build`, and the install test asserts the recorded value equals the `DSH_COMMIT` of `installer-pins.sh`; (b) a failure-injection test runs the step with `DSH_COMMIT=` stubbed empty and asserts exit 1, a stderr line naming `DSH_COMMIT`, and no `curl` call; (c) a test with `DSH_COMMIT=not-a-sha` asserts the same refusal.
5. The body `../U226-pr-body.md`: Summary (the failed host build, the upstream variable, the pin), Contract (guarantee: the build never runs without the manifest's commit, and the commit the artifacts embed is the tag's; leaves out: the choice of tag archive over the npm package, the host install already made by hand, every other asset; `TRUST:` sentence as below), a Threat table `row | risk | status | evidence` with rows for the manifest field, the constant line, the refusal, the build line and the receipt string plus an `orchestrator effect` row, each `closed` with the ACCEPTANCE command, and `Program-Unit: regime-cutover/U226`.

ACCEPTANCE
1. `grep -n 'ref_commit: b830ec950faba0a46dda564be3e2d854afed94f1\|DSH_COMMIT: ref_commit' home/dot_agents/agent-config.yaml` prints two lines.
2. `grep -n '^DSH_COMMIT="b830ec950faba0a46dda564be3e2d854afed94f1"$' scripts/lib/installer-pins.sh` prints one line.
3. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 with no diff.
4. `make validate-agent-assets` exit 0, no ERROR line.
5. `uv run python -m unittest tests.unit.test_update_agent_assets tests.unit.test_network_bounds tests.unit.test_scratch_git` OK (paste the test count), the three new tests among them named in the paste.
6. `grep -c 'DSH_CLIENT_COMMIT_HASH' scripts/update-agent-assets.sh` prints 3 or more (the refusal, the build line, the record).
7. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0 and `make shellcheck` exit 0.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. The host proof (a real `make update` reaching the already-installed exit on this host, and a fresh install on the Ubuntu host) is the coordinator's and the operator's step after the merge, recorded in the store.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the manifest's pinned tag, sha256 and commit as reviewed values and the upstream build script's documented reading of `DSH_CLIENT_COMMIT_HASH` at that tag; it reads no network at test time, changes no other asset or installer, and does not decide between the tag archive and the npm package.

TIMEBOX
45 minutes.

FORBIDDEN
No change to any asset other than `deepseek-harness`, to the validator, to `hcom-seat` or to the profile renderer; no `git init` or other fabrication of git metadata inside the install tree; no local bats; no network read; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your TASK; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line beside your tree (`../U226-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U226-pr-body.md`) per CHANGE 5.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35, 37); `AGENTS.md` (Comment Policy, Test Policy, Audit); the decisions row of phase `M-14` dated 2026-11-06T03:46:22Z.
