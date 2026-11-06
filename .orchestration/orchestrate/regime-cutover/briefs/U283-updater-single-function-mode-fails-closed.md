# U283 the asset updater's single-function mode fails closed and stays inside its destination

GOAL
`scripts/update-agent-assets.sh` runs one function when called with its name (`main`'s `case "$#:$1"` whitelist: `update_pi_claude_bridge`, `update_security_audit_skill`, `update_deepseek_harness`, `check_pi_claude_bridge`, `check_pstack`, the retire functions). The round-2 audit of PR 698 (`verdicts/U276b-837d5996.md`) measured, with the real updater, that this mode fails open: `update_compactiondb` exits 0 after `rsync` exits 77 and after `manifest_record` fails, because `record_claude_failure` only increments `PIN_FAILURES`, which only `main`'s full run checks at its end (`fail_on_pin_failures`); `manifest_prune_retired` prints a warning and exits 0 after pruning fails; `update_compactiondb` with `~/.agents/compactiondb` linked outside `~/.agents` ran `rsync --delete` through the link and removed a file outside; `update_deepseek_harness` runs `mise exec` without disabling automatic tool installation, so a missing Node or pnpm would modify mise's tool trees. The coordinator will run the updater per function after a merged unit changes a pin (standing order 48, the deploy of pinned assets), so this mode must carry the whole run's contract: a function's failure is the run's failure, and a destination is written only when it is a real directory under the asset root.

SCOPE
A new branch `fix/updater-single-function-fails-closed` from `origin/main` (your tree is `/tmp/dotfiles-wt/U283`). May write: `scripts/update-agent-assets.sh`, `tests/unit/test_update_agent_assets.py`, `docs/` only where the updater's single-function mode is already described, and the body `../U283-pr-body.md`. Not: the manifest, any `home/` file, the `update` target.

CONTEXT
Read `main` and `fail_on_pin_failures`, `record_claude_failure`, `update_compactiondb`, `manifest_prune_retired`, `update_deepseek_harness` and the `rsync` destinations of every `update_*` function. The single-function path must end with the same `fail_on_pin_failures` the full run ends with (or an equivalent check that the function recorded no failure), so an exit 0 means the function did what it says. Destinations: before an `rsync --delete` or a `rm -rf` into a destination under `~/.agents` or `~/.local`, the function (or one shared helper every function calls) proves the destination's parent is a real directory (not a link, `pwd -P` equal to its spelling) under the asset root; a link refuses naming the path. `mise exec`: pass `MISE_NOT_FOUND_AUTO_INSTALL=false` (confirm the variable name in `mise --help` or its documentation at the pinned version on this host) or an equivalent so a missing tool refuses instead of installing.

DATA SHAPE
One shared helper for destinations (`assert_asset_destination <path>`: real directory parent under the asset root, else refuse) called by every function that deletes or syncs into a destination; one exit rule for the single-function path (`"$1"; fail_on_pin_failures`), so the contract lives in `main` once. The whitelist gains the functions the coordinator needs for pin deploys (`update_omp`, `update_hcom`, `update_security_audit_skill`, `update_deepseek_harness`, `update_pi_claude_bridge`, `update_compactiondb`, `update_graphify` if it exists; read `main` for the exact names) with the same contract.

CHANGE
1. The exit rule and the helper per DATA SHAPE; the whitelist; the mise variable.
2. Tests (the existing module has fixtures for the updater with fakes): single-function `update_compactiondb` with `rsync` exiting 77 exits non-zero; with a failing `manifest_record` exits non-zero; `manifest_prune_retired` with a corrupt manifest exits non-zero; a linked destination refuses before `rsync` runs (the recorder shows no rsync call); `mise exec` receives the no-auto-install setting; the full `main` run's behaviour is unchanged (existing tests stay).
3. Measurement on this host, read-only: `scripts/update-agent-assets.sh --help`-like misuse prints the usage with the new names (exit 2); no function is run.
4. The body: Summary, Contract, Threat table (one row per changed path), Verification (ACCEPTANCE pasted), the four findings quoted with their fixes.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_update_agent_assets` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
4. The CHANGE 3 output pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator's first per-function deploy after the merge records the function, its exit status and the manifest record in `decisions.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the updater's existing fakes and fixtures as the test bed and changes the single-function exit rule, one destination helper and one mise setting; it runs no function on this host, reads no credential and opens no network.

TIMEBOX
60 minutes.

FORBIDDEN
No run of any `update_*` function on this host; no change to the manifest; no edit under `home/`; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u283/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U283` and the coordinator fetches it by path.
- Progress line at `../U283-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U283-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Boundary Discipline; Fix Root Causes: the exit rule lives in main once, not per function).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the whitelist, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 34, 44, 46, 48); `verdicts/U276b-837d5996.md`; the mechanism-change row of 2026-11-06T12:5xZ; `AGENTS.md` (Test Policy).
