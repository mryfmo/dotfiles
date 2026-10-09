# AGMSG-TASK dotfiles-T118-rolling-tools-single-update-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Operator decision 2026-10-09 (chat, after the analysis of the pin model): the intended shape is one host command that applies the remote repository's diff locally and then updates the local tool set to the latest safe versions through each manager's own safety features; exact pins and the committed lock go, problem tools are held back individually. This task is wave 1 of 2: the mise tool set, the single `make update` command, and the prose and tests that describe them. Wave 2 (T119) moves the release-asset installers (mise bootstrap, aws-cli, tode, terminal-browser, crit, zed, chezmoi bootstrap, agmsg) from manifest pins to latest-release-plus-publisher-verification and retires `scripts/lib/installer-pins.sh` and the `assets.*.pin` keys; do not touch those files here. Kind: mise config, Makefile, install and upgrade scripts, one CI job, prose, tests; no permission, sandbox or hook block; Claude seat allowed.

## Why (grounded in the official documentation; keep these citations in the README paragraph)

- The repository held two principles that could not both hold: `make update` "converges the machine to committed pinned state" and `make upgrade` "trust-now-and-record" (installs first, records later), so every upgrade put the host ahead of the committed state and dirtied the canonical clone (T112, T114, T117).
- Pin coverage was partial and undeclared: mise tools and the manifest assets were exact, while `brew upgrade`, `uv tool upgrade --all`, gh extensions and apt already floated to the latest version in the same command.
- `mise.lock` is not a reproducible artifact across runs (checksum algorithm choice differs between runs of the same release), so treating it as byte-exact evidence fought the tool. mise documents what replaces it: `minimum_release_age` ("Skip versions published more recently than this duration or date"), `minimum_release_age_excludes`, and verification that works without a lockfile: `aqua.cosign`, `aqua.minisign`, `aqua.slsa`, `aqua.github_attestations`, `github_attestations`, `node.verify` (mise.jdx.dev/configuration/settings). `mise upgrade` without `--bump` "keeps the range specified in mise.toml" (mise.jdx.dev/cli/upgrade), so with `latest` requests it moves to the newest allowed release and edits no file in the repository.
- Holding a tool back is each manager's own feature: an exact version in `config.toml` (mise), `brew pin` (Homebrew), `uv tool install <pkg>==<version>` (uv), `apt-mark hold` (apt).

## Target behaviour, stated once

1. **`home/dot_mise/config.toml`.** Every tool request becomes `"latest"`, except tools held back for a stated reason, each with a one-line comment naming the reason: `fd` (newer releases lack a macOS x64 asset; existing comment), `npm:pnpm` (plugin lockfile compatibility; existing comment), and the `http:` tools `bats` and `gcloud`, whose backend needs an explicit URL and checksum per version (comment: `http backend: bumped by hand with its checksum`). Keep the `allow_builds` and `os` table forms where present. `[settings]`: remove `lockfile`, `locked` and `lockfile_platforms`; add `minimum_release_age = "7d"` (the cooldown the old `--before 7d` flags applied per command) and keep the rest. Do not set the verification settings explicitly: they default to true (verify with `mise settings ls --all | grep -E 'aqua\.(cosign|slsa|github_attestations|minisign)|^github_attestations|node\.verify'` and paste it); README names them. Verify the cooldown with the real binary before committing, in a scratch `MISE_CONFIG_DIR` (and `MISE_DATA_DIR`): `mise settings set minimum_release_age 7d`, read it back, then `mise latest <tool>` with and without the setting for one tool per backend in the config: core `node`, `aqua:mikefarah/yq`, `github:x-motemen/ghq`, `npm:ccusage`, `cargo:eza` (paste all ten results). A backend that ignores the setting is named in the README as not covered by the cooldown. Then prove the update mechanism once: in the scratch config request `jq = "latest"`, install an older jq explicitly (`mise install jq@1.7.1`, `mise use`-free), and show that `mise upgrade --dry-run` names the newest allowed jq without rewriting `config.toml` (paste the dry run and `git diff --stat` or a checksum of the scratch config before and after).
2. **Delete** `home/dot_mise/mise.lock` and `home/dot_config/mise/mise.lock.tmpl`. Hosts keep a stale `~/.config/mise/mise.lock` otherwise, so add `.config/mise/mise.lock` to `home/.chezmoiremove` (create the file if absent; chezmoi removes listed targets on apply). Update the comment at the top of `config.toml` (`Versions are reviewed and updated only by make upgrade with the lock diff`) to the new policy in one line.
3. **Manifest.** `home/dot_agents/agent-config.yaml` `assets.mise-tools` (around line 342–348: `pin: home/dot_mise/mise.lock`, `files: [config.toml, mise.lock]`): make it describe the config file alone, or remove the entry if `scripts/validate-agent-assets.py` and `scripts/update-agent-assets.sh` accept that; read the validator's `assets` rules (around lines 580–700) first and change only what the entry needs; `make render-check` and the validator must pass. The other `assets.*` entries are T119's.
4. **One command.** `Makefile`: the `update` target replaces its two `mise install --locked …` lines with `./scripts/upgrade-tools.sh $(if $(filter 1 true yes,$(SYSTEM)),--system,)` at the same position (after the chezmoi applies, before `update-agent-assets.sh`); the `upgrade` target is deleted. `SYSTEM=1` keeps its meaning (apt). `install/common/mise.sh` lines ~107–111: drop `--locked` and the per-command `--before` flags (the setting covers them); keep the npm `min_release_age` handling as it is otherwise. `scripts/update-agent-assets.sh:130`: drop `--locked`. (`home/dot_claude/hooks/executable_format-edited-files.py:74` still says `mise install --locked`; it is a Claude hook source, so a Claude seat does not edit it: leave it, name it in the report, and the orchestrator routes that one string to a Codex seat.) `home/dot_zshrc:37` comment: pins are no longer committed. `home/dot_codex/rules/default.rules:190`: remove `"make upgrade"` from the allowed make targets. `install/common/sheldon.sh:30` runs `mise exec --locked -- cargo install --locked …`: check `mise exec --help`; without a lockfile mise's own `--locked` may refuse, so drop mise's flag and keep cargo's. `scripts/update-agent-assets.sh:130` is `mise install --force --locked`: dropping only `--locked` leaves `--force`, which with `latest` would reinstall Claude Code and Codex on every `make update`; read why `--force` is there, keep it only if that reason survives, and say so in the report. `home/dot_local/bin/common/executable_herdr-agents:692` (the `agmsg-orchestration:` directive) says `make upgrade pin diffs included`: drop those words, and update the test that pins the directive text (`tests/unit/test_herdr_agents.py` ~1553). `tests/unit/test_agmsg_orchestration_docs.py` pins SKILL phrases; update whatever the deleted pins clause pinned.
5. **`scripts/upgrade-tools.sh`** becomes the host-side update of installed tools, run by `make update`: `MISE_CONFIG_DIR` is no longer forced to the repository (`~/.config/mise`, the applied config, is the host's config; drop the `MISE_CEILING_PATHS` override too, or set it to `$HOME`, and prove with `mise config ls` in the pasted run that the host config is the one in use); delete `require_pins_checkout` (T117), `apply_upgraded_mise_config`, `bump_terminal_tool_pins`, `bump_release_asset_pins` and the `upgrade_agent_assets` phase (T119 handles release assets; `make update` already runs `update-agent-assets.sh` right after); `upgrade_mise_tools` runs `mise upgrade --yes` without `--bump` (ranges stay, nothing is rewritten), keeping the `http:` and `fd` skips; `upgrade_mise_self` runs `mise self-update --yes` to the latest release (no manifest pin); `upgrade_agent_cli_tools` stays only if it does something `mise upgrade` does not (read it; if it only re-installs the two npm tools mise already upgrades, delete it); Homebrew, uv tool, gh extension and apt phases stay. Because `make update` now updates installed tools, the script exits 0 immediately when `CI=true` (the same key the run_before guard uses), printing one line; first establish which CI path reaches `make update` (`setup.sh`, the bootstrap jobs in `.github/workflows/*.yml`) and paste the grep, so the skip is justified by evidence. Update the shdoc header and `@description`s; `shellcheck` clean.
6. **CI.** `.github/workflows/test.yaml` statusline job (~lines 200–245): it copies `home/dot_mise/mise.lock` and installs `--locked`; make it install from `config.toml` alone (`mise -C … install`), and reword the comments that say "pinned in mise.lock". Confirm with green CI; the `validate` and `test` jobs are the authority for the Python and bats suites.
7. **Prose, each rule once.** README lifecycle block (~lines 143–215): one host command, `make update` (and `SYSTEM=1`), which pulls, applies, updates installed tools with each manager's safety features, and refreshes agent assets; `make upgrade`, the pins worktree procedure, the canonical-clone refusal text and the `installer-pins` sentences T117 wrote in that block go; a short "Holding a tool back" list with the four mechanisms; one paragraph stating the policy and its trade-off (no exact pins and no committed lock, so machines may differ in tool versions and CI tests the latest safe versions; cooldown `minimum_release_age = 7d`; mise verification settings relied on, by name; T119 will do the same for the release-asset installers). README ~1268–1271 (`Tool versions … are exact and backed by mise.lock`, the pins-worktree sentence, the applied-copy sentence): replace with two sentences pointing at the lifecycle paragraph; lines ~1290–1300 about `installer-pins.sh` stay for T119. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` boundary bullet: delete the pins clause entirely (from `The operator runs make upgrade in the pins worktree …` through `… never leave that diff dirty across sessions.`); the sentence `The canonical clone is otherwise untouched by any seat …` and the rest stay. `scripts/check-regime-boundary.sh`: the canonical-clone section comment and the differs line lose the pins-worktree wording (`… ; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <canon> restore -SW --source=<ref> -- <files> and drop its autostash`); update the two test strings. `tests/install/common/lifecycle.bats` ~457–458 greps `make upgrade` in the README: change the assertions to `make update` and `make update SYSTEM=1` (bats runs in CI only; do not run it locally).
8. **Tests** (Python, `make unit-test` = `uv run python -m unittest discover -s tests/unit -v`): `tests/unit/test_supply_chain_policy.py` asserts the lock exists, `locked = true` and related facts (lines ~189, 254–347): rewrite those cases to the new policy (no `mise.lock` in the tree, `lockfile`/`locked` absent, `minimum_release_age = "7d"` present, every non-exempt tool request `"latest"`, the four exempt tools exact with a comment, no `--locked` in `install/common/mise.sh`, `Makefile` or `scripts/update-agent-assets.sh`, no `upgrade` target, the `update` recipe runs `upgrade-tools.sh`); `tests/unit/test_statusline_tools.py` reads `mise.lock` (line 18): read the versions it needs from the installed tools or drop the lock dependency; `tests/unit/test_runtime_health.py`: delete the T117 guard cases and the `canonical=True` override subtests, adapt the upgrade fixture to the host-config form; `tests/unit/test_herdr_agents.py`: the Makefile test (update includes `agmsg-bootstrap`; no `upgrade` target) and the two differs-line strings; `tests/unit/test_validate_agent_assets.py` and `tests/unit/test_generate_agent_configs.py` only if the manifest change in item 3 moves an assertion. Ground the list first: `git grep -nE 'mise\.lock|--locked|make upgrade|lockfile|locked = true|upgrade-tools' -- tests scripts Makefile install home .github README.md` on your branch base; everything it names outside T119's files is in scope.

Forbidden: anything else; T119's files (`scripts/lib/installer-pins.sh`, `install/common/mise.sh` download/verify part, `install/ubuntu/common/aws_cli.sh`, `install/ubuntu/client/zed.sh`, `home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl`, the `assets.*` entries other than `mise-tools`, `tests/unit/test_release_asset_pins.py`, `tests/unit/test_aws_cli_acquisition.py`, `tests/unit/test_asset_manifest.py`, `scripts/check-tools.sh`); `make update`; `make upgrade`; touching `~/.local/share/chezmoi`; thread resolution; running `mise upgrade` or `brew upgrade` against the host (scratch `MISE_CONFIG_DIR` probes only).

User-visible change for the PR body and the README paragraph: removing `lockfile`/`locked` from the global `[settings]` changes mise's behaviour for every other project on the host that relied on the global lockfile mode (a project with its own `mise.lock` keeps it only if it sets the setting locally); a `node` major bump can leave `npm:` tool installs invalid until `mise install` reruns (`make update` runs it); the `.zshrc` change is a comment only (AGENTS.md dotfiles-safety); `make upgrade` is gone; `make update` now also updates installed tools to the latest versions older than seven days (mise, Homebrew, uv tools, gh extensions; apt with `SYSTEM=1`); tool versions are no longer committed, so machines may differ; held-back tools are listed in `config.toml` with their reason.

[memory:decision] dotfiles-T118 (orchestrator 2026-10-09): tool versions are not committed; `home/dot_mise/config.toml` requests `latest` with `minimum_release_age = "7d"` and mise's default signature and checksum verification, held-back tools carry an exact version and a reason; `mise.lock` and `make upgrade` are gone; `make update` is the one host command (pull, apply, update installed tools through each manager, refresh agent assets); problem tools are held with the manager's own feature (exact version, brew pin, uv tool install ==, apt-mark hold). Supersedes T37/T53/T96 exact-pin decisions and the T117 pins-worktree procedure.

## Repo / branch

`.claude/worktrees/worker-c` seated by `herdr-agents --add-worker`; `git fetch origin`; `git switch -c feat/rolling-tools-single-update --no-track origin/main` (main is `b9209774` or later).

## Allowed files

`home/dot_mise/config.toml`, `home/dot_mise/mise.lock` (delete), `home/dot_config/mise/mise.lock.tmpl` (delete), `home/.chezmoiremove` (new or edit), `home/dot_agents/agent-config.yaml` (the `assets.mise-tools` entry only), `scripts/validate-agent-assets.py` (only what that entry needs), `Makefile`, `install/common/mise.sh` (the install lines ~107–111 only), `scripts/update-agent-assets.sh` (line ~130 only), `scripts/upgrade-tools.sh`, `home/dot_zshrc` (one comment), `home/dot_codex/rules/default.rules` (one list entry), `.github/workflows/test.yaml` (the statusline job), `README.md` (the lifecycle block and lines ~1268–1271), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (the boundary bullet's pins clause), `scripts/check-regime-boundary.sh` (comment and differs line), `tests/install/common/lifecycle.bats` (two greps), `tests/unit/test_supply_chain_policy.py`, `tests/unit/test_statusline_tools.py`, `tests/unit/test_runtime_health.py`, `tests/unit/test_herdr_agents.py`, `tests/unit/test_validate_agent_assets.py` and `tests/unit/test_generate_agent_configs.py` (only if item 3 moves an assertion). Artifacts at `.orchestration/{reports,validation,sandboxes,learning}/dotfiles-T118-rolling-tools-single-update-a01.md`, `.orchestration/autoskill/runs/dotfiles-T118-rolling-tools-single-update-a01.md`, worker-side review evidence `-worker-crit.json` / `-worker-review-receipt.md` under `.orchestration/validation/`, all in the main checkout through the permission gate, masked.

## Push

As before: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles feat/rolling-tools-single-update`; `gh pr create --base main --head feat/rolling-tools-single-update …`.

## Validation commands (paste verbatim output, whole)

```
<scratch MISE_CONFIG_DIR probe: minimum_release_age set and read back; mise latest node with and without it; mise settings ls --all | grep -E 'aqua\.(cosign|slsa|github_attestations|minisign)|^github_attestations|node\.verify|minimum_release_age|lockfile|locked'>
shellcheck scripts/upgrade-tools.sh install/common/mise.sh; echo "rc=$?"
make -n update | grep -nE 'upgrade-tools|mise install|agmsg-bootstrap'; make -n upgrade; echo "rc=$?"
git ls-files | grep -c 'mise\.lock'; echo "(expected 0)"
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
uv run python -m unittest tests.unit.test_supply_chain_policy tests.unit.test_statusline_tools tests.unit.test_runtime_health tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test 2>&1 | tail -3
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(tools): one make update that applies the repo and updates installed tools, no committed pins`, English body with the user-visible change above and the four documentation citations; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T118-rolling-tools-single-update-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=24.

## Amendment 1 (orchestrator, 2026-10-09) — two T119 tests that the lock deletion and the helper removal would break

1. `tests/unit/test_aws_cli_acquisition.py` lines ~377–380 (the assertion that reads `home/dot_mise/mise.lock`) are added to the allowed files for that one change: drop the lock-reading assertion (and only it), since the lock no longer exists; the rest of that test and file is T119's.
2. Your default for `tests/unit/test_release_asset_pins.py` is accepted: keep `bump_release_asset_pins`, `pick_windowed_pin`, `asset_manifest_pin`, `github_release_versions`, `crate_versions` and `aws_cli_versions` in `scripts/upgrade-tools.sh`, unwired from `main()`, with one comment above the block: `# ponytail: dead until T119 deletes them with tests/unit/test_release_asset_pins.py; nothing calls these from main().` Delete `bump_terminal_tool_pins`, `require_pins_checkout` and `apply_upgraded_mise_config` as the task says, unless that test also sources them (say which in the report).

Continue, including the `mise.lock` deletion.

## Amendment 2 (orchestrator, 2026-10-09) — the network probes of item 1, run by the orchestrator

The Claude seat sandbox cannot complete mise TLS (Security framework, OSStatus -26276), so the orchestrator ran item 1's network probes outside the sandbox against scratch `MISE_CONFIG_DIR`/`MISE_DATA_DIR`/`MISE_CACHE_DIR`/`MISE_STATE_DIR` only (no host config or data touched; machine-hygiene exemption, no repository involved). Paste the block below verbatim into your validation file under a heading that names it as orchestrator-run, and cite it in the report. Reading of the results: `minimum_release_age = "7d"` is accepted, read back and listed; the verification settings default to true; the cooldown changed the answer for core `node` (26.11.1 → 26.10.0); for `aqua:`, `github:`, `npm:` and `cargo:` the plain and cooldown answers were equal because no release younger than seven days existed at probe time, so those backends are not falsified rather than proven; the README sentence must say exactly that, naming the one backend verified live and the date. `mise upgrade --dry-run` on a `latest` request with an older jq installed names the newest allowed version (`Would install jq@1.8.2`) and the config file hash is unchanged before and after.

```
## orchestrator-run probe, 2026-10-09T10:46:03Z, 2026.9.17 macos-arm64 (2026-09-29), scratch MISE_CONFIG_DIR/DATA/CACHE/STATE under the session scratchpad (<scratch>)

$ mise settings get minimum_release_age  (cooldown config)
7d

$ mise settings ls --all | grep keys (cooldown config)
github_attestations                             true
locked                                          false
lockfile                                        false
minimum_release_age                             "7d"
aqua.cosign                                     true
aqua.github_attestations                        true
aqua.minisign                                   true
aqua.slsa                                       true
node.verify                                     true
lockfile                                        false                                                                                                                          <scratch>/cfg-cooldown/config.toml
minimum_release_age                             "7d"                                                                                                                           <scratch>/cfg-cooldown/config.toml

$ mise latest node   # plain / cooldown 7d
plain:    26.11.1
cooldown: 26.10.0

$ mise latest aqua:mikefarah/yq   # plain / cooldown 7d
plain:    4.54.1
cooldown: 4.54.1

$ mise latest github:x-motemen/ghq   # plain / cooldown 7d
plain:    1.11.2
cooldown: 1.11.2

$ mise latest npm:ccusage   # plain / cooldown 7d
plain:    20.0.26
cooldown: 20.0.26

$ mise latest cargo:eza   # plain / cooldown 7d
plain:    0.23.5
cooldown: 0.23.5

$ mise install jq@1.7.1  (scratch data dir)
mise ✓ jq@1.7.1  2.2s  jq-macos-arm64
mise ████████████████ 1/1 · installed 1 tool in 2.2s

$ mise ls jq
jq  1.7.1  <scratch>/cfg-plain/config.toml  latest

$ shasum -a 256 config.toml (before)
903c8b9738d393f5e3721157093c69f1190a264f161ba457653cfb0244ec625a  <scratch>/cfg-plain/config.toml

$ mise upgrade --dry-run jq
Would schedule jq@1.7.1 for pruning after 24h
Would install jq@1.8.2

$ mise outdated jq
jq  latest  1.7.1  1.8.2 <scratch>/cfg-plain/config.toml

$ shasum -a 256 config.toml (after)
903c8b9738d393f5e3721157093c69f1190a264f161ba457653cfb0244ec625a  <scratch>/cfg-plain/config.toml
$ cat config.toml
[tools]
jq = "latest"
[settings]
lockfile = false
```

## Amendment 3 (orchestrator, 2026-10-09) — backend coverage of the cooldown is documented; cite it instead of inferring from the probes

mise.jdx.dev/configuration/settings, `minimum_release_age`: "Skip versions published more recently than this duration or date." Format: "a duration such as `7d`, `6mo` or `1y`, or a cutoff date such as `2024-06-01` or `2024-06-01T12:00:00Z`; `0s` turns the delay off." Default `"24h"`, env `MISE_MINIMUM_RELEASE_AGE`. Coverage: "The `24h` default applies to aqua, cargo, core, forgejo, gem, github, gitlab, go, npm, packslip, pypi, spm and ubi tools. Tools from asdf, vfox (including vfox plugin backends), conda, dotnet, http, s3 and spinel get no default cutoff." "The cutoff applies when mise resolves a version request such as `node@22` or `latest`, for backends that report release dates." `minimum_release_age_excludes`: "Tools and backends that the configured and default `minimum_release_age` do not apply to." (default `[]`). There is also a `self_update.minimum_release_age` setting.

So the README coverage sentence is: the cooldown covers every backend this config uses except `http:` (`bats`, `gcloud`, which are exact anyway), per the documentation quoted above; the live probe of 2026-10-09 showed it acting on core `node`. Check `mise settings ls --all | grep self_update` and, if `self_update.minimum_release_age` exists on 2026.9.17, set it to `"7d"` as well so `mise self-update` follows the same cooldown; paste the listing either way.

## Amendment 4 (orchestrator, 2026-10-09) — the statusline smoke compares against what mise resolved

`scripts/check-statusline-tools.py` is added to the allowed files: with `latest` requests the expected version is no longer a literal in `config.toml`, so the script takes `--ccstatusline-version` and `--ccusage-version` (the statusline job fills them from `mise current` before the network is cut), drops its `tomllib` read of the config and the exact-version docstring, and keeps its other checks. Your other in-scope fixes are accepted as described: `pwd -P` path comparison in the smoke step, `[settings.self_update] minimum_release_age = "7d"` in `config.toml` with the README corrected, the lifecycle.bats grep, the brew-cask prompt caveat. Push the script with the rest.

## Amendment 5 (orchestrator, 2026-10-09) — operator standing instruction on Bot and CI findings

Every Codex Bot finding and every CI failure on this PR is fixed at its root cause in the PR itself, not dispositioned. A `not-applicable` is reserved for a finding that is factually wrong, and then the reply states the evidence (a pasted command and its output) that refutes it. A finding on the task's own wording is still fixed in the PR (the orchestrator's text is not exempt). "Out of scope" is not a disposition for a finding on files this PR touches: report it as a scope gap, and the orchestrator amends the allowed files. Apply this to the Bot wait of every head, including a review that lands after your 15-minute wait: recheck the reviews once more right before sending the RESULT.

## Amendment 6 (orchestrator, 2026-10-09) — two leftovers this PR owns, one routed away

1. `home/dot_agents/agent-config.yaml` lines ~339–340 (the `assets:` header comment): your one-line fix is accepted: pins change through `generate-agent-configs.py --set-asset` (no `make upgrade`); T119 replaces the mechanism itself.
2. `renovate.json` is added to the allowed files for its three mise-related and manifest rules only: the rule "Notification-only until lock fidelity is proven …" (mise manager, `mise.lock`, `make upgrade`) is deleted, because `latest` requests leave the mise manager nothing to bump and the lock is gone; the rule "Hold fd …" stays (fd is exact and held; its description loses the `scripts/upgrade-tools.sh` reference); the manifest rule's description says `generate-agent-configs.py --set-asset` recomputes the paired fields until T119 retires the pins, with no `make upgrade`. Nothing else in the file changes; keep it valid JSON (`jq . renovate.json`).
3. The Claude hook pair (`home/dot_claude/hooks/executable_format-edited-files.py:72,74`, `tests/unit/test_format_edited_files_hook.py:72`) stays out: Claude-boundary source, routed to a Codex seat by the orchestrator after this PR. Name it in the report as a known leftover.

Continue to the RESULT.

## Revise round 1 (orchestrator, 2026-10-09) — one regression you listed under risks is a finding under Amendment 5

1. **`make update` must still converge offline.** The old recipe had no network-only phase: a machine with its declared tools installed converged without a connection. Now `brew update`, `mise self-update`, `uv tool upgrade --all` and `gh extension upgrade --all` run as *required* phases, so an offline or transient failure exits nonzero before `update-agent-assets.sh`, the Herdr reload and `agmsg-bootstrap`. Fix it inside `scripts/upgrade-tools.sh`, not by reordering the Makefile step (a fresh machine's `update-agent-assets.sh` needs the `npm:pnpm` that only this script installs now): the network-only phases (Homebrew, mise self-update, uv tools, gh extensions) become `run_optional_phase` (warn and continue), while the mise install and upgrade of the declared tools stays `run_required_phase`, so `make update` fails exactly when the host cannot install its declared tool set, as before. Update the summary line wording if needed, add one assertion in `test_runtime_health.py` (a failing fake `brew` leaves the exit status 0 and the mise phase still runs), and correct the README sentence that says a failing `brew update` stops `make update`.
2. **Agent CLI cooldown.** The deleted `upgrade_agent_cli_tools` existed to take Claude Code and Codex releases on day one, and the `.zshrc` `claude-update` helper now waits seven days too. Whether `minimum_release_age_excludes = ["npm:@anthropic-ai/claude-code", "npm:@openai/codex"]` restores day-one for those two is the operator's call; the orchestrator is asking now and will answer by a one-line amendment. Do item 1 first; if the amendment has not arrived when item 1 is pushed, push anyway and expect at most one more one-line commit.

Then shellcheck, the test modules, prettier on README, push, CI, Bot wait on the final diff head (recheck right before the RESULT), `AGMSG-RESULT v1 … round=1`.

### Round 1, item 2 status (orchestrator, 2026-10-09)

The operator is deciding the cooldown policy on the orchestrator's research (cooldown length, Homebrew attestation verification, npm provenance checks, the Claude Code channel). Do not wait: finish round 1 with item 1 as pushed (878e227c), CI, the Bot wait and the RESULT. The policy decision lands either as a one-line follow-up commit on this PR (if it is only the `minimum_release_age` value or an `excludes` list) or as a separate task (if it changes installers). Your offline finding (one bare `mise install --yes` for the install step, per-tool `mise upgrade --yes`) is accepted; paste the offline probe.

## Amendment 7 (orchestrator, 2026-10-09) — the operator's cooldown decision, the part that fits this PR

Operator decision 2026-10-09 on the orchestrator's research (pnpm 11 and mise default 24h; pnpm: "In most cases, malicious releases are discovered and removed from the registry within an hour"; the Shai-Hulud worm re-infected packages in waves over several days; a longer delay also delays security fixes): the cooldown is 72 hours, not seven days. The provenance checks for npm tools, the day-one exception for Codex and the Claude Code channel move are a separate task (T120) after this one; do not add `minimum_release_age_excludes` here.

1. `home/dot_mise/config.toml`: `minimum_release_age = "72h"` and `[settings.self_update] minimum_release_age = "72h"`. Update every test that asserts `"7d"` and the config comment.
2. `scripts/upgrade-tools.sh`, Homebrew phase: export `HOMEBREW_VERIFY_ATTESTATIONS=1` for the `brew upgrade` calls when `gh` is on PATH (Homebrew Manpage: "If set, Homebrew will use the `gh` tool to verify cryptographic attestations of build provenance for bottles from `homebrew/core` or supported third-party taps."); without `gh`, print one line that attestation verification is skipped. Add one assertion to the existing Homebrew phase test.
3. README: the cooldown paragraph says 72 hours and carries the three anchors above in one sentence (pnpm "within an hour", the 24-hour ecosystem defaults, the multi-day Shai-Hulud waves), plus one sentence that Homebrew bottles are verified against their build attestations when `gh` is present. Replace every remaining "seven days" / "7d" in README with 72 hours. The `.zshrc` comment follows if it names seven days.

One commit on top of 878e227c; CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=1`.

## Revise round 2 (orchestrator, 2026-10-09) — audit of 9a7a6ca0: `incorrect` (2 P2, 1 P3); all three fixed at root cause

1. **P2, the first `make update` after this merge runs the old recipe.** `make` parses the Makefile before the recipe pulls, so on a host at the base revision the old `update` still executes `mise install --locked node` after chezmoi has removed the lock, and fails before the asset refresh. The cause is structural (a recipe that pulls its own Makefile), so fix the structure: split `update` into the pull step followed by `$(MAKE) update-tree` (a second make invocation that reads the Makefile the pull just fetched), and move everything after the pull (chezmoi applies, `upgrade-tools.sh`, `update-agent-assets.sh`, the Herdr reload, `agmsg-bootstrap`) into `update-tree`; `make apply` keeps its meaning; `SYSTEM` passes through. Document in README (one sentence: the pull runs first in its own step, so a recipe change lands in the same run) and in the PR body the one-time note for hosts still on the old Makefile: `git -C <clone> pull && make -C <clone> update` once. Verify with a scratch repository at the base revision and the new commit: paste `make -n update` from both and the scratch run that pulls then applies. Update the Makefile tests (`test_herdr_agents.py`, `test_update_agent_assets_ua_core.py`, `test_runtime_health.py` update fixture, `lifecycle.bats` if it greps the recipe).
2. **P2, offline convergence with cached newer metadata.** The per-tool `mise upgrade --yes` is a network operation; when cached metadata names a newer release whose archive is unreachable, it fails and is a required failure. Converging means the declared tools are installed and usable, not that they are the newest, so the per-tool upgrade loop becomes a warn-and-continue step inside the mise phase (the bare `mise install --yes` stays the required part). Add the test the auditor asked for: a fake `mise` whose `install` succeeds and whose `upgrade` fails leaves the phase and the script at exit 0 with a warning line.
3. **P3, report count.** The report says 15 worker review records; the worker crit JSON holds 20. Correct the report to the artifact.

Then shellcheck, the test modules, `make -n update`, prettier on README, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=2`.

## Revise round 3 (orchestrator, 2026-10-09) — audit of b6e27bd7: `incorrect` (1 P2, 2 P3); all at root cause

1. **P2, execpolicy.** `home/dot_codex/rules/default.rules` ~187 forbids the host-mutating make targets for a Codex seat (`make setup`, `make init`, `make update`, `make apply`, …), and the new `update-tree` target runs the same host applies and upgrades without that refusal (`codex execpolicy check` returns no matched rule). Add `"make update-tree"` to that list and extend its regression test (the execpolicy tests under `tests/unit`, already in the allowed files through `default.rules`; name the test module in the report).
2. **P3, scope.** `tests/unit/test_codex_config_merge.py` was changed in b6e27bd7 (a Makefile test that CI broke) without an amendment. It is added to the allowed files now, retroactively, for that one assertion; the acceptance record names it as a scope gap reported after the fact. Under Amendment 5 the report-then-fix order was right; the amendment should have come first, and it is the orchestrator's miss.
3. **P3, README.** Task line 25 requires the README to state that a `node` major bump can leave `npm:` tool installs invalid until `mise install` reruns (`make update` runs it); the report claims it is there and it is not. Add the sentence to the Tool versions paragraph and align the report.

Then shellcheck, the execpolicy and README checks, prettier, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=3`.

## Round 3, Bot threads on 94f4af69 (orchestrator, 2026-10-09)

Fix 4231499867 (npm tools reinstalled after a node upgrade) and 4231499881 (`mise self-update --no-plugins`) in this PR as you proposed, push, and then stop before the Bot wait: thread 4231499859 (the Claude hook message `mise install --locked` and its test) is fixed on this same branch by a Codex seat (task T121, worker-d), because a Claude seat does not edit a Claude hook source. When the orchestrator tells you the Codex commit is on `origin/feat/rolling-tools-single-update`, `git pull --ff-only` it into worker-c, run the hook test module once, then CI, the Bot wait on the final diff head (recheck before the RESULT) and `AGMSG-RESULT v1 … round=3` naming all three threads.

## Revise round 4 (orchestrator, 2026-10-09) — two open Bot P2 threads on b621af77 that the round-3 RESULT did not name

Both are valid and are fixed at root cause; the RESULT listed nine threads and left these two unresolved and unnamed, which is a reporting omission to avoid in round 4 (list every open thread, resolved or not).

1. **4231652016, snapshot node before the bare install.** With `node = "latest"` and an older node installed, the bare `mise install --yes` installs and activates the newer node (the resolved version is not installed yet), so `node_before` taken afterwards already holds the new version and the npm reinstall never runs. Capture `node_before` before the bare install; the comparison after the upgrade loop then covers both the install and the upgrade. Extend `test_upgrade_reinstalls_npm_tools_only_after_node_moved` with the case where the fake `mise install` (not `upgrade`) moves node.
2. **4231652027, the config chezmoi actually applies.** `home/dot_config/mise/config.toml.tmpl` is applied to `$HOME/.config/mise/config.toml` whatever `XDG_CONFIG_HOME` says, so `MISE_CONFIG_DIR` must be exactly `$HOME/.config/mise` and must not inherit an environment value (an inherited `MISE_CONFIG_DIR` or a nondefault `XDG_CONFIG_HOME` would inventory another config). Set it unconditionally to `${HOME}/.config/mise`, keep the checkout-root ceiling, and update the host-config tests (the `XDG_CONFIG_HOME` case now asserts the chezmoi target, and an inherited `MISE_CONFIG_DIR` is overridden). One README clause if it names XDG.

Then shellcheck, the test module, prettier on README, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=4` naming all eleven threads with their fix commits.

## Revise round 5 (orchestrator, 2026-10-09) — audit of 88e369d9: `incorrect` (1 P2), fixed at root cause

**P2, a failed forced reinstall can leave a declared tool missing while `make update` succeeds.** `mise install --force` removes the existing install before fetching its replacement, so a download failure in `reinstall_mise_npm_tools` leaves the tool absent, and the phase only warns (the auditor's read-only simulation: `optional_warnings=1 ccusage_installed=no`, exit 0). "Converged" means every declared tool is installed, so: after the reinstall loop, run the bare `mise install --yes` once more as the required step (it reinstalls whatever a failed `--force` removed, since the resolved version is then missing); a reinstall failure stays a warning only because that final install is what decides; if the final install fails, the phase is a required failure. Test both: a fake `mise` whose `install --force <tool>` deletes the tool's install directory and exits 1 while the following bare `install --yes` recreates it → exit 0 and the tool present; the same with the final install failing → exit 1. Align the README sentence and the report's claim that an unavailable declared tool fails the update.

Then shellcheck, the test module, prettier, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=5` naming every thread.

## Revise round 6 (orchestrator, 2026-10-09) — audit of 5d991b47: `incorrect` (2 P2); both fixed at the real root

1. **P2, npm's own gate during bootstrap.** `install/common/mise.sh` runs under `chezmoi apply` before `upgrade-tools.sh` sets `npm_config_min_release_age=3`, so `home/dot_npmrc`'s `min-release-age=7` refuses an npm release that mise (72h) already chose. The root is two sources of truth for one policy. Fix at the source: `home/dot_npmrc` (added to the allowed files) sets `min-release-age=3`, equal to mise's 72 hours, so every npm invocation on the host agrees with the cooldown; remove the per-script `export npm_config_min_release_age=3` from `upgrade-tools.sh` (no longer needed; keep the `npm_config_min_release_age=0` bypass only where the installer deliberately takes a release mise already vetted, if that line still exists), and make `test_supply_chain_policy` assert that `dot_npmrc`'s days equal mise's `minimum_release_age` in hours divided by 24. README: one clause.
2. **P2, node moved by the installer, not by this script.** The in-process snapshot cannot see a node that `install/common/mise.sh` installed during the preceding `chezmoi apply`. The root is detecting a node move by comparing two points inside one process. Replace it with a persistent marker: `upgrade-tools.sh` reads `${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles/npm-tools-node` (the node version the `npm:` tools were last built for), compares it with `mise current node` after the install and upgrade steps, and when it differs or the marker is missing runs the forced reinstall of every `npm:` tool, then the final required bare `mise install --yes`, and writes the marker only after that succeeds. The installer needs no change: whatever moved node, the next `make update` sees it. Tests: marker absent → reinstall and marker written; marker equal → no reinstall; marker differs → reinstall; a failed final install leaves the marker unwritten. Name the marker in README's reinstall sentence.

Then shellcheck, the test modules, prettier, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=6` naming every thread.

## Revise round 7 (orchestrator, 2026-10-09) — audit of eee788f0: `incorrect` (2 P2, 1 P3); all at root cause

1. **P2, interruption during the rebuild.** The non-destructive rebuild moves the working install aside and has no cleanup trap, so a SIGTERM/SIGINT between the move and the restore leaves the tool missing (read-only simulation: exit −15, not restored). Install a `trap` in the rebuild function that restores the moved-aside install on INT/TERM/EXIT until the new install has succeeded (then clear it), and test the interrupted path (the fake `mise install` sends itself SIGTERM; the tool directory is back afterwards).
2. **P2, the installer resolves `latest` per tool.** `install/common/mise.sh` (a `run_once` installer under `chezmoi apply`) still runs per-tool `mise install <tool>`, which re-resolves a `latest` request over the network and fails during a registry outage even when the tool is installed, the exact case validation 12 showed. The installer becomes one bare `mise install` (it installs every declared tool and skips satisfied requests); the agent-CLI line with `npm_config_min_release_age=0` goes, because `~/.npmrc` now carries the same 3 days as mise and no bypass is needed; `mise.bats` follows. Say in the report whether any ordering the per-tool lines encoded (statusline tools first) still matters; if it does, keep the order inside the bare install's config, not as separate resolutions.
3. **P3, evidence.** Validation line ~846: the pasted grep omits matches (the final head returns lines 276, 286, 287, 292 and 360); line ~159 is a truncated command. Replace both with the complete command and its complete output.

Then shellcheck, the test modules (runtime-health, supply-chain; `mise.bats` runs in CI only), prettier, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=7` naming every thread.

## Revise round 8 (orchestrator, 2026-10-09) — audit of 408727c9: `incorrect` (1 P2, 1 P3)

1. **P2, a leftover backup is never restored when the install is gone.** The rebuild looks the tool up with `mise where` before it considers a backup, so after a SIGKILL (no trap runs) the original install is missing, `mise where` fails, and the restore never happens although the backup is intact (read-only reproduction: `rebuild_rc=1 restore_called=0`). Order the rebuild as: if a backup directory for the tool exists, move it back first (before any `mise where` or install); then look the tool up, move it aside, install, and restore on failure or interruption as now. Make the regression test model the missing-install state (install directory absent, backup present) and assert the restore before the install.
2. **P3, evidence.** Validation ~line 228 (the config-search probe) still holds a truncated command ending `checkout roo` and truncated output; validation line 3 still names `eee788f0` as the final head. Replace the probe block with the complete command and output, and keep the header's "final head" equal to the RESULT's head (update it in each round).

Then shellcheck, the test module, prettier, push, CI, Bot wait on the final diff head (recheck before the RESULT), `AGMSG-RESULT v1 … round=8` naming every thread.

## Revise round 9 (orchestrator, 2026-10-09) — audit of 61c38cd6: `incorrect` (1 P2, 1 P3)

Round 8 is accepted on its substance: `restore_interrupted_npm_rebuilds` first, `MISE_INSTALLS_DIR` honoured, the dot-named discard. Bot threads 4234006744 and 4234006752 are resolved as fixed in 61c38cd6; 4234006735 is resolved `not-applicable` on two orchestrator probes pasted in the thread (empty cache, and a valid or expired cache naming a newer release than the installed one: the bare install says "already installed", rc=0; only a tool with no install fails offline). Two findings remain.

1. **P2, `scripts/upgrade-tools.sh` `restore_npm_install`.** `rm -rf "$1"` runs unchecked, so when the partial install cannot be deleted (a read-only entry inside it, an I/O error) `mv "$2" "$1"` moves the working backup *inside* the surviving partial directory and the function returns 0: the tool is gone, the backup is buried, and nothing reports it. Fix at the root: the restore succeeds only when the old path is gone before the move (`rm -rf "$1" || return 1`, then `[ ! -e "$1" ] || return 1`, then `mv`), and every caller already propagates the failure (`restore_interrupted_npm_rebuilds` returns 1 → `failed=1`; the trap's restore prints and the phase fails). The phase must name the paths in its failure line (`could not restore <install> from <backup>`), so the operator sees what to repair. Test: in `test_runtime_health.py`, model the killed-rebuild state with a partial install that holds a read-only directory (`chmod 0o555`, skip as root, restore the mode in `finally` like the undeletable-backup test); assert the run fails with the required failure naming both paths, that the backup directory is still at `<tool>.before-node-rebuild` with `original` inside it, and that nothing was moved into the partial directory. The test fails against 61c38cd6 (show it, as in 25.4).
2. **P3, validation evidence.** (a) Around line 763: the pasted output of `grep -n 'npm_config_min_release_age\|minimum_release_age' …` contains a `min-release-age=7` line that this pattern cannot match. Re-run the command exactly as shown and paste its complete output; if the intent was to show the npmrc line too, extend the pattern (`-e 'min-release-age'`) and paste that run. (b) Section 14: the `make -n … update` transcripts are abbreviated without a visible filter. Re-run each and paste the whole output, or show the exact `| grep …`/`| sed -n …` that produced what is pasted. Section 1 of the file still carries the rule: every command printed in full before its complete output.

Then: full local suite (`make unit-test 2>&1 | tail -3`, no branch-only failure), shellcheck, push, CI 16 of 16, Bot wait on the new head, recheck every thread, `AGMSG-RESULT … round=9 head=<sha>` with the same fields as round 8. The evidence sections renumber nothing; add `## 26. Revise round 9` for the new test and the re-pasted transcripts. max_turns stays 24 in total across rounds; this is the last round the budget allows before the orchestrator reconsiders the task shape.
