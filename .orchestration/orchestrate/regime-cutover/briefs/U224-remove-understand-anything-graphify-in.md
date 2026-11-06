# U224 Understand-Anything leaves the kit in one wave; graphify is the knowledge-graph capability

GOAL
The operator decided on 2026-11-02 and again on 2026-11-06 that graphify replaces Understand-Anything as the knowledge-graph capability (decisions row of phase `M-13` dated 2026-11-06T03:3xZ, `winner: graphify`). This unit removes every Understand-Anything mechanism from the tracked tree in one wave (plugin pin, installer asset and its four updater functions, validator check, standing rule, nine skill audience lines, doctor knowledge, the ua-symbol-coverage lever, the tests, the README text) and adds the `.chezmoiremove` rows that retire the installed tree on every host. graphify's existing `assets.graphify` entry stays as it is. Nothing is added.

SCOPE
A new branch `feat/remove-understand-anything-graphify-in` from `origin/main` c4195463 (your tree is positioned on it). May write: `home/dot_agents/agent-config.yaml`, `scripts/update-agent-assets.sh`, `scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`, `home/dot_config/claude/rules/understand-anything.md` (delete), `home/dot_local/bin/common/executable_ua-symbol-coverage` (delete), `home/dot_local/bin/common/executable_remove-agent-asset`, `home/.chezmoiremove`, `home/dot_mise/config.toml` (one comment sentence only), `README.md`, `tests/unit/` (the files the CHANGE names), the generated outputs `scripts/generate-agent-configs.py` rewrites under `home/` when run, and the body file beside your tree `../U224-pr-body.md`. Not: `.ua/` and `.gitignore` (the committed graph stays, task 14 default, recorded by the coordinator), `assets.graphify`, any installer between the removed functions (Codex plugin copy, superpowers, ponytail, crit), any file not named here.

CONTEXT
Measured 2026-11-06 at c4195463. The plugin pin is the `understand-anything@understand-anything` row of `assets.claude-plugins.plugins`; the installer is `assets.understand-anything-installer` with its `render.constants` (`CODEX_UNDERSTAND_ANYTHING_*`); the updater holds `update_claude_understand_anything`, `build_understand_anything_core`, `provision_codex_understand_anything_runtime`, `update_codex_understand_anything` with `CLAUDE_UNDERSTAND_ANYTHING_*` and `CODEX_UNDERSTAND_ANYTHING_*` constants and two call sites in the step list; the validator has `validate_understand_anything_assets`; the standing rule is `home/dot_config/claude/rules/understand-anything.md` plus the `understand-anything: [claude, codex]` line under `standing_rules.rules`; the nine `understand*` lines under `skills.audience` and two comments name the installer; the doctor has `UNDERSTAND_SKILL_ALLOWLIST`, `understand_anything_core_warnings` and the two step names; `executable_remove-agent-asset` names the `~/.understand-anything/repo` root; the tests are `tests/unit/test_update_agent_assets_ua_core.py`, `tests/unit/test_ua_symbol_coverage.py` (delete both) and the Understand-Anything cases in `test_asset_manifest`, `test_check_agent_runtime`, `test_network_bounds`, `test_runtime_health`, `test_update_agent_assets` and a `test_ci_workflows` comment. The `npm:pnpm` mise pin stays (M-14 and the later DSH units run pnpm); only its comment loses the Understand-Anything sentence. The generator writes the retired rule's `.chezmoiremove` rows when the rule file and its audience line are gone; run it and `make render-check` after the manifest edit.

CHANGE
1. Manifest: remove the plugin row, the installer block with its constants, the `standing_rules.rules` line, the nine audience lines and the two installer comments.
2. Updater: remove the four functions, their constants and both call sites; the neighbouring installers keep their order and text.
3. Validator and doctor: remove `validate_understand_anything_assets` and its call; remove `UNDERSTAND_SKILL_ALLOWLIST`, `understand_anything_core_warnings` and the two step names.
4. Delete the rule file and the ua-symbol-coverage lever; drop the `~/.understand-anything/repo` root from `executable_remove-agent-asset`.
5. `home/.chezmoiremove`: add `.understand-anything`, `.claude/plugins/cache/understand-anything`, `.claude/plugins/marketplaces/understand-anything` and the nine `.agents/skills/understand*` rows (12 rows).
6. README: remove the Understand-Anything paragraph and the two later mentions. `home/dot_mise/config.toml`: the pin line stays, its comment loses the Understand-Anything sentence.
7. Tests: delete the two files, remove the cases named in CONTEXT.
8. Run `uv run --with pyyaml scripts/generate-agent-configs.py` and commit the regenerated outputs.
9. The body `../U224-pr-body.md`: Summary (one-wave removal on the operator's replacement decision, graphify unchanged, `.ua/` kept), Contract (guarantee: no token of the plugin or installer in `home`, `scripts`, `README.md`, `docs`, `tests`, `AGENTS.md`; the installed tree retires on every host through `.chezmoiremove`; leaves out: the `.ua/` graph and `.gitignore`, graphify's asset entry, the host uninstall step; `TRUST:` sentence as below), a Threat table `row | risk | status | evidence` with one row per removed mechanism class (manifest, updater, validator and doctor, lever, tests, chezmoiremove) and an `orchestrator effect` row, each status `closed` with the ACCEPTANCE command that proves it, plus `Program-Unit: regime-cutover/U224`.

ACCEPTANCE
1. `grep -rli 'understand-anything\|understand_anything\|UNDERSTAND_ANYTHING' home scripts README.md docs tests AGENTS.md; echo "exit=$?"` prints nothing then `exit=1`.
2. `grep -c '^\.understand-anything$\|^\.claude/plugins/cache/understand-anything$\|^\.claude/plugins/marketplaces/understand-anything$\|^\.agents/skills/understand' home/.chezmoiremove` prints 12.
3. `grep -n '^"npm:pnpm" = ' home/dot_mise/config.toml` prints the pin line; `grep -c 'Understand-Anything' home/dot_mise/config.toml` prints 0.
4. `grep -c 'update_codex_ponytail\|update_codex_superpowers\|update_codex_crit' scripts/update-agent-assets.sh` prints the same number before and after (paste both).
5. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 and `home/dot_claude/rules/understand-anything.md.tmpl` is absent.
6. `make validate-agent-assets` exit 0 with no ERROR line.
7. `uv run python -m unittest tests.unit.test_asset_manifest tests.unit.test_check_agent_runtime tests.unit.test_network_bounds tests.unit.test_runtime_health tests.unit.test_update_agent_assets tests.unit.test_scratch_git` OK.
8. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0; `scripts/ci/lint-retired-terms.py` (as `make lint` runs it) exit 0.
9. `test ! -e .ua || git diff --quiet origin/main -- .ua .gitignore` exit 0 (the graph and `.gitignore` unchanged).

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. CI's full suite on the head is the full-suite evidence (standing order 34); the coordinator reads it.

CLOSURE
remove

TRUST
TRUST: the unit trusts the manifest, the updater and the generator at c4195463 as the single source of the agent assets and the generated outputs; it removes one capability's mechanisms and adds twelve `.chezmoiremove` rows, changes no other installer, reads no network, and leaves the `.ua/` graph, `.gitignore` and `assets.graphify` as they are.

TIMEBOX
60 minutes.

FORBIDDEN
No change to `assets.graphify`, `.ua/`, `.gitignore` or any installer other than the four removed functions; no new mechanism, no renamed function, no comment beyond a why the code cannot show; no local bats; no network read; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your TASK; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line beside your tree (`../U224-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U224-pr-body.md`) per CHANGE 9.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35, 37); `AGENTS.md` (Comment Policy, Test Policy, Audit); the decisions row of phase `M-13` dated 2026-11-06T03:3xZ.
