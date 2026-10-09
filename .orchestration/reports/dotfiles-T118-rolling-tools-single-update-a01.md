# Report: dotfiles-T118-rolling-tools-single-update-a01

- Worker: `claude-standard-dot-a001` (Claude Code, `standard`), worktree `.claude/worktrees/worker-c`
- Branch: `feat/rolling-tools-single-update` from `origin/main` `b9209774`
- PR: #310, head `a9eb7f02fbf66d20083cbad9c46f01fb47fe9ca0` (round 9). Commits: 46a73f11 (main change), f999cc68 (statusline smoke, self-update cooldown, review fixes), 752e7265 (ruff format), 4ab9634e (mise ceiling, Herdr-absent bats fixture), 46cd2a88 (Amendment 6, ruff format), 0d218990 (Homebrew without its confirmation prompt, Renovate pnpm hold), 878e227c (revise round 1: offline convergence), becc8612 (Amendment 7: 72h cooldown, Homebrew attestations; bats grep fix), 9a7a6ca0 (no-gh test on runners that ship gh), 9514a3cd (revise round 2: update-tree, upgrades warn), b6e27bd7 (Codex hook-trust test reads update-tree), 94f4af69 (revise round 3: execpolicy for make update-tree, README node sentence), b621af77 (Bot threads on 94f4af69: npm reinstall after a node move, self-update --no-plugins), f25e9eaf (T121, Codex seat worker-d: the formatter hook hint), 64c6d8a6 (Bot threads on f25e9eaf: npm age gate, fd hold by dep name, Lifecycle entry points), 88e369d9 (revise round 4: node snapshot before the bare install, MISE_CONFIG_DIR pinned to the chezmoi target), 5d991b47 (revise round 5: a final bare install after the forced reinstall), d0dd981d (revise round 6: ~/.npmrc carries the npm age policy, persistent npm-tools node marker), eee788f0 (Bot threads on d0dd981d: non-destructive npm rebuild, marker write must succeed), 408727c9 (revise round 7: restore trap around the npm rebuild, leftover backup restored, one bare install in the installer), f79d7b4e (revise round 8: a killed rebuild's backup restored before any mise lookup), 61c38cd6 (Bot threads on f79d7b4e: an undeletable backup never restored over a finished rebuild, MISE_INSTALLS_DIR), a9eb7f02 (revise round 9: a restore only onto a path that is gone, naming both paths when it fails)
- CI: 16/16 checks pass on a9eb7f02 (validation §9), and on 61c38cd6 and f79d7b4e before it. On 408727c9 the first attempt of `test (ubuntu-24.04, client)` stalled in its bats step for over nine minutes (the same step took 3m21s on ubuntu-26.04); it was cancelled, rerun with `--failed`, and passed in 4m00s.
- Bot: the Codex Code Review of a9eb7f0 completed with no review and no inline comment, rechecked right before the RESULT (validation §10). Of the sixteen Bot threads on earlier heads, fifteen are fixed at their root cause (4229677547, 4229994961, 4229994970, 4231499859, 4231499867, 4231499881, 4231739043, 4231739053, 4231739066, 4231652016, 4231652027, 4233013310, 4233013323, 4234006744 and 4234006752), and the orchestrator resolved 4234006735 as `not-applicable` on its own probes (Round 8, Codex Bot threads on f79d7b4e; Revise round 9).
- Status: ready_for_review

## What changed (task items 1–8)

1. **`home/dot_mise/config.toml`.**
   - Every request is `"latest"` except the four held tools, each with a one-line reason above it: `fd` ("Held: newer fd releases lack a macOS x64 asset."), `npm:pnpm` (the existing comment now starts its reason with "Held:"), and `http:bats` / `http:gcloud` ("http backend: bumped by hand with its checksum."). The `allow_builds` and `os` table forms stay.
   - `[settings]` drops `lockfile`, `locked` and `lockfile_platforms` and adds `minimum_release_age`. Per Amendment 3, `[settings.self_update] minimum_release_age` is added too. Both were `"7d"` until Amendment 7 set them to `"72h"`.
   - The verification settings are not set; the listing shows they default to true. The top comment states the new policy in one line.
2. **Lock removal.** `home/dot_mise/mise.lock` and `home/dot_config/mise/mise.lock.tmpl` are deleted, and `.config/mise/mise.lock` is appended to the existing `home/.chezmoiremove`. For mise, `chezmoi managed` lists only `.config/mise/{config.toml,mise.lock}`, so `~/.mise` needs no entry.
3. **Manifest.** The `assets.mise-tools` entry is removed. No consumer reads it: `generate-agent-configs.py` renders only entries with `render:`, and the validator's only other use is the `"mise": {"mise-lock"}` verify kind. That kind is removed too, because no entry declares it now. Per Amendment 6, the `assets:` header comment names `generate-agent-configs.py --set-asset` instead of `make upgrade`. `make render-check` and the validator pass.
4. **One command.**
   - `Makefile`: `update` runs `./scripts/upgrade-tools.sh $(if $(filter 1 true yes,$(SYSTEM)),--system,)` in place of the two `mise install --locked` lines, and the `upgrade` target is deleted. The recipe comments now say what update does, that `SYSTEM=1` needs `sudo -v`, and that a Homebrew cask upgrade can run sudo.
   - `install/common/mise.sh`: `--locked` and `--before` are dropped from the install lines. Since revise round 7, `run_mise_install` is the config trust followed by one bare `mise install`: the per-tool lines and the agent CLIs' `npm_config_min_release_age=0` are gone (see Revise round 7). Dropping `--before` left `readonly DEFAULT_NPM_MIN_RELEASE_AGE_DAYS=7` (line 16) unused (shellcheck SC2034), so that dead constant is deleted as well, the one line outside "the install lines ~107–111".
   - `scripts/update-agent-assets.sh`: `--locked` is dropped at line 130 and in the matching `manifest_record` command string on line 133. **`--force` stays.** It sits in `ensure_mise_npm_agent_cli`, which returns early whenever the CLI already runs. So it is a repair path for a broken install (mise skips an installed version without `--force`), not a reinstall on every `make update`. The line 71 comment, which said `upgrade-tools.sh` bumps the tode/terminal-browser pins, is corrected (grep-named; the bump is gone).
   - `install/common/sheldon.sh`: per `mise exec --help`, mise's `--locked` means "Require lockfile URLs", so that flag is dropped and cargo's `--locked` stays.
   - `home/dot_zshrc`: the `claude-update` comment block (comment only). `home/dot_codex/rules/default.rules:190`: one `match` entry. The forbidden `pattern` keeps `upgrade`, since forbidding a now-missing target loosens nothing.
   - The `herdr-agents` directive and its pinned test string drop "make upgrade pin diffs included".
   - **Not edited by this seat:** `home/dot_claude/hooks/executable_format-edited-files.py:72,74` (``run `mise install --locked` `` and "make update installs only some mise tools") and `tests/unit/test_format_edited_files_hook.py:72` are a Claude-boundary source. After Codex Bot thread 4231499859 the orchestrator routed them to a Codex seat (T121, worker-d), which fixed them on this branch in f25e9eaf. The hint now says `make update`; I pulled that commit and ran its test module (see Round 3, Codex Bot threads).
5. **`scripts/upgrade-tools.sh`.**
   - **Config.** `MISE_CONFIG_DIR` is `${HOME}/.config/mise`, the directory chezmoi applies `home/dot_config/mise/config.toml.tmpl` to, set unconditionally since revise round 4 (it first defaulted to `${XDG_CONFIG_HOME:-$HOME/.config}/mise`, see Revise round 4). It is pinned because the isolated-Git wrapper moves `XDG_CONFIG_HOME`; on this macOS host mise 2026.9.17 kept `~/.config/mise` even with `XDG_CONFIG_HOME` moved (validation §5).
   - **Ceiling.** `MISE_CEILING_PATHS` stays at the checkout root. The task allowed dropping it or setting it to `$HOME`, but Codex Bot thread 4229677547 showed that either lets a parent directory's `mise.toml` join the inventory. `mise config ls` confirms this: without a ceiling, or with `$HOME`, the parent `~/Workspace/dotfiles/mise.toml` loads; with the checkout root, only `~/.config/mise/config.toml` loads (validation §5). The pasted run through the script's own wrapper shows only the host config in use.
   - **Deleted:**
     - `require_pins_checkout`
     - `apply_upgraded_mise_config`
     - `bump_terminal_tool_pins`, with `fetch_installer_pin`, `fetch_crit_pin` and `fetch_zed_pin`
     - the `upgrade_agent_assets` phase
     - `upgrade_agent_cli_tools`, with `latest_npm_package_version`, `repair_mise_npm_package` and `upgrade_mise_npm_agent_tool`
   - **Why `upgrade_agent_cli_tools` went.** It did one thing `mise upgrade` does not: it took the newest npm release immediately (`npm_config_min_release_age=0 … use --global --pin --minimum-release-age 0s`). That writes an exact pin into the applied config and bypasses the cooldown, both against the new policy. Codex and Claude Code are now ordinary `latest` mise tools; `allow_builds` covers Claude Code's postinstall. `make update` runs `update-agent-assets.sh` right after, and its `ensure_mise_npm_agent_cli` repairs a broken CLI with `mise install --force`. **User-visible:** the two agent CLIs now trail npm by 72 hours. README says `minimum_release_age_excludes` would exempt them.
   - **Upgrade steps.** `upgrade_mise_tools` runs one bare `install --yes` (revise round 1) and `upgrade --yes` per tool, without `--bump`, `--before` or `MISE_LOCKED=0`, and keeps the `http:` and `fd` skips. `upgrade_homebrew` sets `HOMEBREW_NO_ASK=1` on both `brew upgrade` calls (Codex Bot thread 4229994970: Homebrew 7.0.8 `brew upgrade --help` says "Ask mode is the default"; an older brew without ask mode ignores the variable). `upgrade_mise_self` runs `mise self-update --yes`, which `self_update.minimum_release_age = "72h"` now bounds (validation §1c).
   - **Kept unwired per Amendment 1**, under the prescribed `# ponytail:` comment: `asset_manifest_pin`, `pick_windowed_pin`, `github_release_versions`, `crate_versions`, `aws_cli_versions` and `bump_release_asset_pins`. `tests/unit/test_release_asset_pins.py` sources none of the deleted functions (validation §3). `pick_windowed_pin`'s doc no longer cites `--before 7d`.
   - **CI skip.** `main` exits 0 with `CI=true: skipping installed-tool updates.` after argument parsing. Evidence (validation §4): no workflow runs `make update`, `make upgrade` or `upgrade-tools.sh`. CI reaches only `setup.sh`, which calls neither, and no chezmoi script does. The skip is therefore a guard for a `CI=true` environment, and the unit fixtures set `CI=false` because GitHub Actions sets `CI=true` in every job.
   - The shdoc header and `@description`s are updated, and shellcheck is clean.
6. **CI.**
   - The statusline job copies `config.toml` alone and installs without `--locked`.
   - Per Amendment 4, the smoke step compares physical paths (`pwd -P`): `mise which` answers through the `latest` symlink and `mise where` with the version directory, which made 46a73f11 fail on every runner.
   - `scripts/check-statusline-tools.py` takes `--ccstatusline-version` and `--ccusage-version`, which the job fills from `mise current` before the network is cut. Its `tomllib` config read and its "exact" docstring are gone.
   - The step names and messages no longer say "exact" or "pinned".
   - CI's ruff and prettier are now the latest versions behind the cooldown, so a formatter release can change what the format check accepts.
7. **Prose.**
   - **README lifecycle block.**
     - One command: `make update` and `make update SYSTEM=1`.
     - A **Tool versions** paragraph:
       - the policy and its trade-off
       - the cooldown, and the verification settings by name
       - the two mise citations
       - Amendment 3's backend-coverage sentence, with the 2026-10-09 node probe
       - the self-update cooldown
       - the agent-CLI cooldown
       - the change to global lockfile mode for other projects
       - the T119 note
     - A **Holding a tool back** list of the four mechanisms.
     - The operator-phase sentence names the Homebrew cask sudo exception.
     - The make update paragraph says that a required-phase failure stops `make update` before the asset refresh, and that `make apply` is the same target.
     - Gone: the `make upgrade` refusal paragraph, the pins-worktree steps and the "converges to committed pinned state" sentence.
   - **README ~1268–1271** becomes two sentences pointing at that paragraph; "a worker task carries that PR" becomes "every repository change as a PR".
   - **SKILL boundary bullet.**
     - The pins clause is deleted. The task's end marker "never leave that diff dirty across sessions" no longer exists after T117, so the clause ran to "nothing to re-apply."
     - "keeps reporting …, now as a sign" becomes "reports … as a sign".
     - "no `make upgrade`," is dropped from the canonical-clone sentence.
   - **`check-regime-boundary.sh`.** The comment and the differs line use the task's wording, and both test strings follow. The "after the pins PR merged" comment is reworded.
   - **README sentences outside the listed ranges.** Each was corrected because this change made it false, each with a minimal edit:
     - Crit: `refreshed by make upgrade` → `changed with generate-agent-configs.py --set-asset`.
     - tode/terminal-browser: the `make upgrade` trust-now-and-record sentence → "a pin changes only in `assets:`".
     - The old line 394 comment `# Tool upgrades run in the pins worktree` is removed.
     - `npm:` tools: "version, lock entry, and isolated install prefix" → "version and isolated install prefix".
     - Asset manifest: "mise tools are listed there as a pointer to … mise.lock" → "mise tools are not listed there", because item 3 removed that entry.
     - "`make upgrade` does this for tode, terminal-browser, Crit, and Zed" → "For tode, terminal-browser, Crit, and Zed, write the reviewed pins … with `--set-asset`".
     - The rest of README ~1290–1300 (installer-pins) is untouched, for T119.
   - **`renovate.json` (Amendment 6, three rules only).**
     - The lock-fidelity mise rule is deleted.
     - The manifest rule names `generate-agent-configs.py --set-asset` until T119.
     - The fd hold cites `config.toml`.
     - `jq` validates the file.
     - Codex Bot thread 4229994961 (fixed:0d218990): Renovate keeps normal updates for a concrete version, and its mise extractor keeps `npm:pnpm` as the depName, so a disabled mise rule with `matchDepNames: ["npm:pnpm"]` now sits next to the `fd` hold, and `test_supply_chain_policy` asserts it.
8. **Tests.**
   - `test_supply_chain_policy` covers the new policy:
     - no lock files, and the `.chezmoiremove` entry
     - the retired settings absent; `minimum_release_age = "72h"` and `self_update.minimum_release_age = "72h"`
     - every non-held request `latest`; the four held tools exact, with a comment line
     - the template render of `config.toml`
     - no `--locked` in the three files; no `upgrade` target; the `update` order
     - the symlink, npm-backend and http-tool cases without the lock
     - the sheldon fake mise without `--locked`
     - the Renovate case: no lock-fidelity mise rule, and the fd hold kept
   - `test_statusline_tools` drops the lock dependency: it asserts both tools are requested as `latest` and the cooldown is set, and it follows the CI strings.
   - `test_runtime_health`:
     - The upgrade fixture is rebuilt for the host-config form: no repo config, no chezmoi, no curl, no npm, no agent-config copy, and `CI=false`.
     - Deleted: the T117 guard test, the canonical/override apply test, the live-symlink test, the agent-CLI npm test and the pin-bump test.
     - New tests prove the host `MISE_CONFIG_DIR` (with and without `XDG_CONFIG_HOME`), the checkout-root `MISE_CEILING_PATHS`, that no file is written in the checkout, and the `CI=true` skip.
     - The required-failure list drops the removed phases, and the skip test asserts no `--bump`, `--before`, `--pin` or `use`.
     - The `make update` fixture gains a fake `upgrade-tools.sh`, and the agent-CLI repair fixture drops `--locked`.
   - `test_herdr_agents` covers the Makefile test (update includes `agmsg-bootstrap`; `make -n upgrade` has no rule), the directive string and the two differs-line strings.
   - `test_validate_agent_assets` and `test_generate_agent_configs` are unchanged; their `mise` fixtures are the binary asset.
   - Grep-named (task item 8's last sentence), outside the explicit list:
     - `test_update_agent_assets_ua_core.py`: the `make -n update` pnpm assertion now checks `upgrade-tools.sh` and the held `npm:pnpm`.
     - `test_check_agent_runtime.py`: fixture strings without `--locked`.
     - `tests/install/common/mise.bats`:
       - install order without `--locked`/`--before`
       - argument positions `$3`→`$2`
       - the bare final `install`
       - the blocc `latest` grep
     - `tests/install/common/lifecycle.bats`:
       - both update fixtures fake `upgrade-tools.sh`
       - the SYSTEM tests use `make -n update`
       - no `upgrade` target
       - the README greps (`make update SYSTEM=1`, no `make upgrade`)
       - the greps for removed functions and the ceiling
     - `tests/install/ubuntu/server/sheldon.bats`: the fake mise without `--locked`.
   - Amendment 1: `tests/unit/test_aws_cli_acquisition.py` loses only the lock-reading assertion.
   - Bats were not run locally (AGENTS.md); CI is the authority, and every bats suite passes there on 46cd2a88.

## Network probes (item 1)

The Claude seat cannot complete mise TLS inside its sandbox: every host gives `OSStatus -26276`, while curl reaches the same host. I reported this as `AGMSG-PONG status=blocked`, and the orchestrator ran the probes outside the sandbox against scratch dirs (Amendment 2). They are pasted verbatim in validation §1b under an orchestrator-run heading. The worker's offline part is §1a (the setting set and read back, and the verification defaults) and §1c (`self_update.minimum_release_age`).

## CI rounds and findings (Amendment 5: each fixed at its root cause)

| Head     | Failure or finding                                                                                                                                                                                | Fix                    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| 46a73f11 | Statusline smoke: path compare through the `latest` symlink; expected version read as the literal `latest`                                                                                        | f999cc68 (Amendment 4) |
| 46a73f11 | Independent review: lifecycle.bats grep matched my comment; false self-update claim; prompt caveat; stop-on-failure note; zshrc wording; stale "exact/pinned" wording; `--locked` fixture strings | f999cc68               |
| f999cc68 | ruff format of `check-statusline-tools.py`                                                                                                                                                        | 752e7265               |
| f999cc68 | Codex Bot P2, thread 4229677547: restore the mise config-search ceiling                                                                                                                           | 4ab9634e               |
| 752e7265 | bats "update skips reload when Herdr is absent": fixture without `upgrade-tools.sh`                                                                                                               | 4ab9634e               |
| 4ab9634e | ruff format of `test_runtime_health.py`                                                                                                                                                           | 46cd2a88               |
| —        | Scope gaps reported: `agent-config.yaml:339` comment, `renovate.json` rules                                                                                                                       | 46cd2a88 (Amendment 6) |
| 46cd2a88 | Codex Bot P2s: thread 4229994961 (Renovate could bump the held `npm:pnpm`) and thread 4229994970 (`brew upgrade` asks for confirmation by default) | 0d218990 |
| 878e227c | bats lifecycle.bats:278 grep for the literal `upgrade --yes \"${mise_tool}\"` (the round-1 loop had generalised the command) | becc8612 |
| becc8612 | Python: the no-gh attestation subtest saw the runner's own `/usr/bin/gh` | 9a7a6ca0 |
| 9514a3cd | Python: `test_codex_config_merge` read `./scripts/update-agent-assets.sh` from the `update:` recipe, now in `update-tree` | b6e27bd7 |
| 64c6d8a6 | `test (ubuntu-26.04, client)` attempt 1 stalled in `Run unit test` (27 min; 3-4 min elsewhere); every other runner passed the same suite | cancelled and re-run; attempt 2 passed |

Unresolved Bot threads, with proposed dispositions (the worker resolves no thread): 4229677547 `fixed:4ab9634e`, 4229994961 `fixed:0d218990`, 4229994970 `fixed:0d218990`, 4231499867 `fixed:b621af77`, 4231499881 `fixed:b621af77`, 4231499859 `fixed:f25e9eaf` (Codex seat, T121), 4231739043 `fixed:64c6d8a6`, 4231739053 `fixed:64c6d8a6`, 4231739066 `fixed:64c6d8a6`, 4231652016 `fixed:88e369d9`, 4231652027 `fixed:88e369d9`, 4233013310 `fixed:eee788f0`, 4233013323 `fixed:eee788f0`, 4234006735 `not-applicable` (the pinned mise 2026.9.17 accepts an installed `latest` offline under `minimum_release_age = "72h"` with an empty cache and fetches nothing; validation §25), 4234006744 `fixed:61c38cd6`, 4234006752 `fixed:61c38cd6`: sixteen threads, matched one-to-one against the recheck listing in validation §10. Heads 0d218990, 9a7a6ca0, 9514a3cd, 64c6d8a6, eee788f0 and 408727c9 drew no review or comment, and b6e27bd7 drew none within its wait; the findings on 94f4af69 and f25e9eaf are the six threads named above, f79d7b4e drew three (Round 8, Codex Bot threads on f79d7b4e), and 61c38cd6 and a9eb7f02 drew none.

## Local test status

`make unit-test` in the sandbox on a9eb7f02 (the final head) fails 225 IDs against 227 on a scratch worktree of `origin/main`, and none fails only on the branch. The two that fail only on `origin/main` are the deleted pin-bump test and `test_upgrade_github_extensions_are_warning_only`, folded into the round-1 optional-phase test. The task's targeted command (93 failing IDs) adds none (validation §2, §7). These sandbox failures (herdr socket, mktemp under `/var/folders`, agmsg, crit) are environmental; CI's `validate` and `test` jobs are the authority.

## Risks and follow-ups for the orchestrator

- `make update` stops before the agent asset refresh only when a declared mise tool cannot be installed, or apt fails with `SYSTEM=1`. The network-only phases warn (revise round 1), so an offline host converges as before.
- `node`, `python` and `rust` now cross minor and major versions on their own, behind the cooldown. README names the node/npm case: a `node` major bump can leave `npm:` tool installs invalid until `mise install` reruns, which `make update` does (added in round 3).
- `home/dot_zshrc` `claude-update`: its `mise upgrade` is now bounded by mise's `minimum_release_age`, so it no longer reaches the newest release on day one. The comment says so. Restoring that needs a code change (for example `MISE_MINIMUM_RELEASE_AGE=0s` on that call), outside the comment the task allows.
- Known leftovers, not edited:
  - `scripts/check-tools.sh:8`, `scripts/lib/installer-pins.sh:9` and `tests/unit/test_aws_cli_acquisition.py:13` (T119)
  - `plans/004…` and `plans/005…` (historical)
- The release-asset pin helpers in `upgrade-tools.sh` are dead code until T119.
- `npm_config_min_release_age=0` remains in two places outside round 7's scope: `home/dot_zshrc` `claude-update` (lines 38 and 41; the task allows only its comment) and `scripts/update-agent-assets.sh:129` and its `manifest_record` string on line 133, in `ensure_mise_npm_agent_cli`, the broken-CLI repair (the task allows only line ~130's `--locked`). The round-7 argument applies to both: `~/.npmrc` carries the same 72 hours as mise, so the bypass is unneeded and only drops npm's gate on transitive dependencies. Routing them is the orchestrator's call.

## Revise round 1

1. **`make update` converges offline again** (878e227c).
   - In `scripts/upgrade-tools.sh`, the network-only phases now run as `run_optional_phase`, so they warn and continue: Homebrew, `mise self-update`, uv tools, and GitHub CLI extensions (already optional).
   - `mise inventory/install/upgrade` stays `run_required_phase`. apt with `--system` also stays required, because the operator asks for it explicitly.
   - The Makefile order is unchanged: a fresh machine's `update-agent-assets.sh` needs the `npm:pnpm` this script installs.
   - **Offline finding, accepted by the orchestrator** (validation §12): a per-tool `mise install --yes <tool>` on a `"latest"` request exits 1 offline even when the tool is installed, because it re-resolves `latest` over the network. A bare `mise install --yes` exits 0 when every declared tool is installed and 1 when one is missing. Per-tool `mise upgrade --yes` exits 0 offline.
   - So the install step is now one bare `mise install --yes`, and the per-tool loop only upgrades (with the `http:` and `fd` skips). `make update` therefore fails exactly when a declared mise tool cannot be installed.
   - Tests: `test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs` covers a failing fake `brew` (Darwin), `mise self-update`, `uv` and `gh`. Each leaves exit 0, `required failures: 0; optional warnings: 1`, the bare `mise install --yes` and `mise upgrade --yes python`.
   - The required-failure test keeps the mise inventory, install and upgrade phases and apt. The skip test asserts the bare install and no per-tool install. The lifecycle.bats grep follows.
   - The header `@description` and README now say the network-only phases only warn. The README sentence claiming a failing `brew update` stops `make update` is corrected.
2. **Agent CLI cooldown:** the operator's decision is pending (task file, "Round 1, item 2 status"), so this round does not change it.

## Amendment 7 (operator decision on the cooldown)

- `minimum_release_age` and `self_update.minimum_release_age` are `"72h"`; the tests assert `"72h"`.
- README's cooldown paragraph carries the three anchors in one sentence:
  - the 24-hour default of mise and pnpm
  - pnpm's "In most cases, malicious releases are discovered and removed from the registry within an hour"
  - the several days over which the Shai-Hulud worm re-infected packages in waves, because a longer delay also holds back security fixes
- Every other README "seven days" now reads 72 hours. The 2026-10-09 node probe ran with a seven-day setting, so README describes it without the value. The `.zshrc` comment names no duration.
- `upgrade_homebrew` sets `local -x HOMEBREW_VERIFY_ATTESTATIONS=1` when `gh` is on PATH, and otherwise prints "gh not found; Homebrew bottle attestation verification is skipped.". The function-local export works on macOS `/bin/bash` 3.2 (validation §13).
- `test_upgrade_homebrew_verifies_attestations_when_gh_is_present` checks that `brew upgrade` sees `HOMEBREW_VERIFY_ATTESTATIONS=1 HOMEBREW_NO_ASK=1` with `gh`, and `unset` plus the skip line without it. lifecycle.bats greps the export.
- No `minimum_release_age_excludes` is added. The day-one exception, npm provenance and the Claude Code channel are T120.
- The same commit fixes the CI failure on 878e227c: the lifecycle.bats grep for `upgrade --yes "${mise_tool}"` rejected the round-1 loop that had generalised the command to a variable, so the loop names `upgrade` literally again. Every static grep in lifecycle.bats and mise.bats was evaluated against the tree before the push.

## Revise round 2 (orchestrator audit of 9a7a6ca0: incorrect, 2 P2 and 1 P3)

1. **P2: the first `make update` after the merge ran the old recipe** (9514a3cd).
   - make parses the Makefile before the recipe pulls, so a host at the base revision would have run the old `mise install --locked node` against the removed lock.
   - `update` now only fetches and pulls, then runs `@$(MAKE) --no-print-directory update-tree`. That second make reads the Makefile the pull fetched and does the chezmoi applies, `upgrade-tools.sh`, `update-agent-assets.sh`, the Herdr reload and `agmsg-bootstrap`.
   - `SYSTEM` reaches it through `MAKEFLAGS`, and `make apply` keeps its meaning (`make -n update SYSTEM=1` and `make -n apply` in validation §14).
   - Scratch proof (validation §14): `make -n update` at the base revision still shows the old single recipe. At the new commit it shows the pull and then the second make. A clone at the new commit whose origin carries a further recipe change pulls it and runs the changed `update-tree` recipe in the same run.
   - README and the PR body carry the one-time note: `git -C <clone> pull && make -C <clone> update`.
   - Tests: `test_supply_chain_policy` asserts the split (the update recipe ends with the second make after the pull; `update-tree` keeps the apply → upgrade-tools → assets order and `agmsg-bootstrap`). The `make -n update` tests (herdr-agents, ua-core, lifecycle.bats) read the second make's dry run and pass. Both bats update fixtures already fake `upgrade-tools.sh`.
2. **P2: offline convergence with cached newer metadata** (9514a3cd). `run_mise_tool_command` returns 2 when an upgrade failed for at least one tool, and `upgrade_mise_tools` turns that into `optional warning: mise upgrade failed for at least one tool; its installed version stays`. The bare `mise install --yes` and the tool listing (exit 1) stay required. `test_upgrade_failure_after_a_successful_install_only_warns` sets up a fake `mise` whose install succeeds and whose upgrade fails, and expects exit 0, the per-tool and phase warnings, and `required failures: 0; optional warnings: 1`.
3. **P3: report count.** The count above is read from the artifact (`jq length`).
4. **CI on 9514a3cd:** `tests/unit/test_codex_config_merge.py`, a Makefile test outside the round's list, still read `./scripts/update-agent-assets.sh` from the `update:` recipe. b6e27bd7 checks that `update` hands off to `update-tree` and reads the asset refresh there. My local full run on 9514a3cd had caught it, but it finished after the push; b6e27bd7 was pushed only after the full suite showed no branch-only failure (validation §7).

## Revise round 3 (orchestrator audit of b6e27bd7: incorrect, 1 P2 and 2 P3)

1. **P2: execpolicy** (94f4af69). `home/dot_codex/rules/default.rules` forbade `make update` and `make apply`, but Codex matches whole tokens, so the new `make update-tree` matched no rule (`codex execpolicy check` before the fix: `{"matchedRules":[]}`). `update-tree` joins the forbidden make targets and their `match` examples. The regression test module is `tests/unit/test_codex_execpolicy.py`, whose `REQUIRED_PREFIXES` now includes `("make", "update-tree")`. Validation §15 has `codex execpolicy check` after the fix: `make update-tree`, `make update` and `make apply` are forbidden, and `make unit-test` matches nothing.
2. **P3: scope.** `tests/unit/test_codex_config_merge.py` (b6e27bd7) was changed before an amendment allowed it. The orchestrator added it to the allowed files after the fact for that one assertion; it is named here as a scope gap reported after the fix.
3. **P3: README.** The Tool versions paragraph now says that a `node` major bump can leave `npm:` tool installs invalid until `mise install` reruns, which `make update` does (task line 25). The earlier report claimed this sentence was already there when it was not; the Risks bullet below now matches the README.

## Round 3, Codex Bot threads on 94f4af69

- **4231499867 (P2, npm tools after a node upgrade)** (fixed:b621af77). The bare `mise install --yes` runs before the per-tool upgrades, so it never reinstalled `npm:` tools that were already installed. When an upgrade then moved `node`, they stayed on the old runtime. `upgrade_mise_tools` now compares `mise current node` before and after the upgrades. When `node` moved, `reinstall_mise_npm_tools` runs `mise install --force --yes` for each `npm:` tool (since eee788f0 a non-destructive rebuild without `--force`, see Round 6). A failure is an optional warning that names the command to rerun, so offline convergence is unchanged. Since revise round 5, a final bare `mise install --yes` runs as the required step after the reinstall. `test_upgrade_reinstalls_npm_tools_only_after_node_moved` covers three cases: `node` moved (one forced reinstall of `npm:ccusage`), `node` unchanged (none), and a failed reinstall (exit 0, one warning). README says `make update` reinstalls the `npm:` tools when `node` moves.
- **4231499881 (P2, self-update moved plugins)** (fixed:b621af77). `mise self-update --help`: "--no-plugins  Disable auto-updating plugins". A plugin update is a branch move the cooldown does not cover, so `make update` runs `mise self-update --yes --no-plugins`. README says to run `mise plugins update` when wanted. The self-update tests assert the flag.
- **4231499859 (P2, the formatter hook still says `mise install --locked`)**. `home/dot_claude/hooks/executable_format-edited-files.py:74` and `tests/unit/test_format_edited_files_hook.py:72` are a Claude-boundary source, which this Claude seat does not edit. The orchestrator routed the thread to a Codex seat (T121, worker-d), which committed the fix on this branch in f25e9eaf. I pulled it into worker-c and ran its test module here (validation §16).

## Round 3, Codex Bot threads on f25e9eaf

- **4231739043 (P2, README still listed `upgrade`)** (fixed:64c6d8a6). The Lifecycle introduction now lists three entry points (`setup`, `update`, `doctor`) and says that upgrading installed tools is part of `make update`.
- **4231739053 (P2, the fd hold never applied)** (fixed:64c6d8a6). Renovate's mise extractor resolves `fd`'s package name to `sharkdp/fd`, so `matchPackageNames: ["fd"]` matched nothing. The hold now uses `matchDepNames: ["fd"]`, like the pnpm hold, and `test_supply_chain_policy` asserts it.
- **4231739066 (P2, npm's own age gate refused mise's choice)** (fixed:64c6d8a6).
  - The managed `~/.npmrc` sets `min-release-age=7` (days). npm refused any `npm:` release that mise's 72-hour cutoff chose while it was 3 to 7 days old: an upgrade then only warned and left the tool stale, and a fresh `mise install` of a missing `npm:` tool failed.
  - The Bot proposed the old `0` override for the two agent CLIs only. I fixed the root cause for every `npm:` tool instead: the script exports `npm_config_min_release_age=3`, the same window as `minimum_release_age = "72h"`. That keeps a 3-day gate on transitive dependencies, which `0` would drop. (Revise round 6 moved this policy into `~/.npmrc` and removed the export.)
  - `test_supply_chain_policy` keeps the two values equal, the host-config test asserts every mise call sees `3`, and README says so.
  - The orchestrator accepted this over the agent-only override (2026-10-09T15:36Z).

## Revise round 4 (two Bot P2 threads on b621af77 that the round-3 RESULT did not name)

- **Reporting omission.** The round-3 RESULT named nine threads and left out 4231652016 and 4231652027, both raised on b621af77. I had skipped that head's Bot wait while the Codex seat worked on the branch, and my final recheck listed both threads without my matching them to dispositions. This RESULT names all eleven, and I matched the recheck listing to the `threads=` field one-to-one before sending.
- **4231652016 (P2, the node snapshot came after the bare install)** (fixed:88e369d9). With `node = "latest"` and an older node installed, the bare `mise install --yes` installs and activates the newer node. A snapshot taken after it already held the new version, so the npm reinstall never ran. `node_before` is now taken before the bare install, so the comparison after the upgrades covers both the install and the upgrade. `test_upgrade_reinstalls_npm_tools_only_after_node_moved` gains the case where the fake `mise install` moves node. That case fails against the previous script (validation §19).
- **4231652027 (P2, mise read a config chezmoi does not apply)** (fixed:88e369d9). chezmoi applies `home/dot_config/mise/config.toml.tmpl` to `$HOME/.config/mise/config.toml` whatever `XDG_CONFIG_HOME` says. `MISE_CONFIG_DIR` is therefore `${HOME}/.config/mise` unconditionally, so neither an inherited `MISE_CONFIG_DIR` nor a nondefault `XDG_CONFIG_HOME` can point the upgrade at another config. The checkout-root ceiling stays. The host-config test covers both overrides, and both cases fail against the previous script. README names no XDG path for mise, so it needs no change. lifecycle.bats greps the new export.

## Revise round 5 (orchestrator audit of 88e369d9: incorrect, 1 P2)

- **P2: a failed forced reinstall could leave a declared tool missing while `make update` succeeded.** `mise install --force` removes the install before it fetches the replacement, so a download failure in `reinstall_mise_npm_tools` left the tool absent, and the phase only warned.
- **Fix:** after the reinstall loop, `upgrade_mise_tools` runs the bare `mise install --yes` once more, as the required step. It reinstalls whatever a failed `--force` removed, because the resolved version is then missing. A reinstall failure stays a warning only because that final install decides; if the final install fails, the phase is a required failure.
- **Tests:** the fake `mise` keeps an install marker for `npm:ccusage`. `install --force` deletes it and exits 1 in the reinstall phases, and a bare `install --yes` recreates it.
  - `test_upgrade_reinstalls_npm_tools_only_after_node_moved` asserts two bare installs whenever node moved, one otherwise, and that the tool is present at the end (including after a failed reinstall).
  - `test_upgrade_fails_when_a_failed_reinstall_leaves_a_tool_that_cannot_be_restored` sets the final install to fail and expects exit 1 with the required failure.
  - Both fail against the 88e369d9 script (validation §20).
- **README:** the sentence on the npm reinstall now says that `make update` then runs `mise install` once more, so a failed reinstall cannot leave a declared tool missing without failing the update. The claim that `make update` stops only when a declared mise tool cannot be installed now holds after a reinstall too.

## Revise round 6 (orchestrator audit of 5d991b47: incorrect, 2 P2)

1. **P2: npm's own gate during bootstrap** (fixed:d0dd981d).
   - `install/common/mise.sh` runs under `chezmoi apply` before `upgrade-tools.sh`, so the managed `min-release-age=7` still refused an npm release that mise's 72 hours had already chosen. The root was two sources of truth for one policy.
   - `home/dot_npmrc` now sets `min-release-age=3`, the same 72 hours, so every npm invocation on the host agrees with the cooldown. The per-script `export npm_config_min_release_age=3` is removed. The installer's `npm_config_min_release_age=0` for the agent CLIs stayed in this round; revise round 7 removed it with the per-tool lines.
   - `test_supply_chain_policy` asserts that the npmrc days equal mise's `minimum_release_age` hours divided by 24, and that the script no longer sets the variable. README says so in one clause.
2. **P2: node moved by the installer, not by this script** (fixed:d0dd981d).
   - The in-process snapshot is gone. A persistent marker, `${XDG_STATE_HOME:-~/.local/state}/dotfiles/npm-tools-node`, records the `node` the `npm:` tools were last built on.
   - After the install and upgrade steps the marker is compared with `mise current node`. If it differs or is missing, the npm rebuild runs, then the required final bare `mise install --yes`. Since the Bot round below, the rebuild is non-destructive.
   - The marker is written only after both succeed. That is stricter than "after the final install", so a failed reinstall is retried by the next run.
   - The installer needs no change: whatever moved `node`, the next `make update` sees it.
   - `test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs` covers seven cases:
     - marker absent: rebuilt, marker written
     - marker equal: no reinstall
     - marker differs because node moved before this run: rebuilt
     - node upgraded in this run
     - node moved by the bare install
     - a failed reinstall: restored, but not recorded
     - a failed final install: marker unwritten, exit 1
   - Four of those cases fail against the 5d991b47 script (validation §21). README names the marker in its reinstall sentence.

## Round 6, Codex Bot threads on d0dd981d

- **4233013310 (P2, an offline first update could destroy working npm tools)** (fixed:eee788f0).
  - Every existing host lacks the new marker, so its first `make update` rebuilds every `npm:` tool. `mise install --force` deletes the working install before downloading its replacement, so offline the tools were left missing.
  - The root is a destructive rebuild with no fallback. `rebuild_mise_npm_tool` now moves the install directory aside (a same-filesystem rename; only an existing absolute directory that `mise where` names), installs the exact current version, deletes the backup on success, and restores it on failure.
  - A rebuild that cannot download keeps the working tool, warns, and leaves the marker unwritten for the next run. No `--force` remains.
  - Tests: marker absent with a failed rebuild keeps the tool and writes no marker; a failed rebuild with a stale marker keeps the tool and the old marker; successful rebuilds replace the install and leave no backup or partial directory.
- **4233013323 (P2, a failed marker write was ignored)** (fixed:eee788f0). A marker that cannot be written now prints `required: could not record the npm-tools node in <path>` and fails the phase. `test_upgrade_fails_when_the_node_marker_cannot_be_written` points `XDG_STATE_HOME` at a regular file and expects exit 1.
- Both kinds of test fail against the d0dd981d script (validation §22). README says the rebuild keeps the previous install until the new one succeeds, and that a marker that cannot be written fails the update.

## Revise round 7 (orchestrator audit of eee788f0: incorrect, 2 P2 and 1 P3)

1. **P2: an interruption during the rebuild left the tool missing** (fixed:408727c9).
   - Right after the working install is moved aside, `rebuild_mise_npm_tool` sets INT, TERM and EXIT traps. Each runs `restore_npm_install`, which deletes whatever the interrupted install left and renames the backup back. INT then exits 130 and TERM exits 143. `printf %q` bakes the paths into the trap string when the trap is set.
   - The traps are cleared as soon as the exact install returns: on success before the backup is deleted, on failure before the explicit restore. `restore_npm_install` does nothing when no backup exists, so the EXIT trap that follows an INT or TERM exit is harmless.
   - `test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted`: the fake `mise install --yes npm:ccusage@20.0.0` creates a partial directory and sends SIGTERM to the update script (`kill -TERM "$PPID"`; the wrapper runs `mise` directly, so its parent is the script's bash). It expects exit 143, `original` back, no partial directory, no backup and no marker.
   - The round text says the fake `mise install` "sends itself SIGTERM". A `mise` that kills only itself exits through the ordinary failure branch, which eee788f0 already restored. The audit's simulation (exit −15) is the script dying, and that is what this test reproduces: against eee788f0 it fails with `143 != -15` (validation §23.1).
   - **Beyond the literal ask, closing the same window.** No trap runs on SIGKILL or a power loss, and the old first step, `rm -rf "${backup}"`, would then delete the only working copy on the next run. The rebuild now first puts a leftover backup back with `restore_npm_install`, and only then checks that the install directory exists. `test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run` starts with the working install in the backup and a partial install directory; against eee788f0 it fails with `original` missing. **Incomplete, fixed in round 8:** that restore sat after `mise where`, which fails once the install directory is gone, so it never ran in exactly the state a SIGKILL leaves, and the test modelled only the partial case.
2. **P2: the installer resolved `latest` per tool** (fixed:408727c9).
   - `run_mise_install` is now `trust_mise_config || return` followed by one bare `mise install`. That installs every declared tool and skips requests already satisfied, so under `chezmoi apply` an installed `latest` needs no registry lookup. The `node`, statusline and agent-CLI lines are gone, and with them the agent CLIs' `npm_config_min_release_age=0`; `~/.npmrc` carries the same 72 hours as mise.
   - `mise.bats`:
     - The sequence test now expects `trust --yes` then `install`, and still records `npm_config_min_release_age` (expected unset).
     - The node, statusline and agent-CLI failure tests go with their lines.
     - The trust-failure and full-install-failure tests stay.
   - `mise.bats` runs only in CI, so `test_supply_chain_policy` also asserts that `install/common/mise.sh` sets no `npm_config_min_release_age=`. The eee788f0 installer fails that check (validation §23.2).
   - **Does the per-tool order still matter? No.**
     - The order came from 11d27f5e (#72): the locked statusline tools installed at mise's default 24-hour floor, before the batch under `--before 7d`. 8e25a4fa (#73) then added the agent CLIs with the npm bypass of the exact-version upgrade path. So the order encoded a *different cooldown per group*.
     - Under one `minimum_release_age` for every request, and the same window in npm, no group needs its own resolution, so nothing is moved into the config.
     - `node` before the `npm:` tools is a dependency that mise itself orders inside a bare install (its npm backend depends on `node`). The required bare install in `scripts/upgrade-tools.sh` already relies on this.
     - I could not prove that first-hand: a scratch-directory `mise install --dry-run` probe was denied in this session. The probe that would show it needs network, so it runs outside the sandbox: a scratch `MISE_CONFIG_DIR`/`MISE_DATA_DIR`/`MISE_CACHE_DIR`/`MISE_STATE_DIR` whose config holds only `node = "latest"` and `"npm:ccusage" = "latest"`, then a bare `mise install` with `PATH` reduced to the mise binary's directory and `/usr/bin:/bin`. If mise did not order `node` first, the `npm:` install would fail for lack of `node`.
3. **P3: evidence** (validation §2, §21, §22, §23.3, §23.4).
   - Why the grep was incomplete: in this session's Bash tool, `grep` is a shell function from the Claude Code shell snapshot that runs its bundled ugrep 7.8.4 with `-G`. ugrep reads `${...}` in a basic regex as an anchor and an interval, so those alternatives never matched. `/usr/bin/grep` (BSD grep 2.6.0) returns all five lines with the same pattern (validation §23.3 shows both).
   - The same defect hid line 333 (the marker write) from §21's grep. Both greps are replaced in place by fixed-string `grep -nF -e …` runs against the commit they describe, with complete output; eee788f0 returns lines 276, 286, 287, 292 and 360.
   - The truncated command at line ~159 came from a `| cut -c1-200` at the end of my validation script, which also clipped the `mise config ls` line below it. The cut is gone, and §2 is rerun on the final head.
   - Sections 19–22 abbreviated their previous-script runs as `(… at <sha>) ...`. §23.4 reruns each in full from `git archive` copies (no checkout or worktree change) and prints the complete command.

## Revise round 8 (orchestrator audit of 408727c9: incorrect, 1 P2 and 1 P3)

1. **P2: a leftover backup was never restored when the install was gone** (fixed:f79d7b4e).
   - Round 7's restore ran inside the rebuild, after `mise current` and `mise where`. After a SIGKILL no trap runs, so the install directory is gone and the backup holds the only working copy. `mise where` then fails, the rebuild returns before the restore, and the bare install before it has already tried to download the missing tool again. This matches the audit's reproduction, `rebuild_rc=1 restore_called=0`.
   - `restore_interrupted_npm_rebuilds` now runs first in the mise phase, before `mise trust`, the bare install and any `mise where`. It needs no mise lookup: it scans mise's installs directory for `*/*.before-node-rebuild` directories. That directory is `MISE_INSTALLS_DIR` when set (added after Bot thread 4234006752), else `${MISE_DATA_DIR:-${XDG_DATA_HOME:-~/.local/share}/mise}/installs`, the resolution `mise doctor` and `mise where` show on 2026.9.17 (validation §24.1, §25). The scan moves each back over whatever its install path holds.
   - The rebuild keeps one guard in place of its round-7 restore: it moves an install aside only when no backup exists, so `mv` can never move an install into a leftover backup. The INT/TERM/EXIT traps are unchanged.
   - `test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run` now models the missing-install state as the round asks: the install directory absent and the backup present, plus a partial-install case.
     - The fake `mise where` fails, like mise, when the install directory is missing.
     - The fake bare install is offline: it fails unless the working install is back in place, which asserts the restore comes before the install.
     - Both cases expect exit 0, no required failure, the original install back, and no partial directory or backup.
     - The fixture now places the fake install under `MISE_DATA_DIR/installs/npm-ccusage/20.0.0`, mise's layout.
   - Both cases fail against 408727c9 with exit 1 (validation §24.2).
2. **P3: evidence** (validation header, §5, §19).
   - The validation header now names the final head, and is to be updated in every round.
   - The §5 config-search probe block had been pasted through a `cut -c1-90` (the truncated `checkout roo` command and its output). It is replaced by a complete rerun of the same three probes on the final head.
   - I checked the published file for lines whose length equals every `cut -c1-N` width used anywhere in this session's commands (12 to 900). Besides §5 (lines 225, 228, 229, 231), that found lines 783 and 785 in §19, cut at 220 columns (`override='XDG_CO`). They are completed in place from §23.4's full rerun of the same command, with a note. Every other line at those widths ends naturally.

## Round 8, Codex Bot threads on f79d7b4e

- **4234006744 (P2, an undeletable backup could revert a finished rebuild)** (fixed:61c38cd6).
  - After a successful exact install, `rm -rf "${backup}"` could fail (an entry in a read-only directory, a filesystem error), and the rebuild still returned success, so the marker was written.
  - Round 8's leftover scan then took that partly deleted backup for an interrupted rebuild on the next run. It replaced the new install with the old, node-bound one, and the matching marker meant nothing rebuilt it again.
  - The root is a backup that still matches the leftover pattern after success. The success path now renames the backup out of the pattern, to `.<version>.discarded-after-rebuild`, before deleting it. A failed rename returns failure, so the marker stays unwritten. A failed delete only warns, because nothing reads the discarded copy.
  - The dot keeps a leftover out of mise's versions: offline on 2026.9.17, `mise ls` lists `1.8.2.discarded-after-rebuild` as an installed jq version, and lists nothing for `.1.8.2.discarded-after-rebuild` (validation §25).
  - I did not simply propagate the delete failure, because a partly deleted backup would then still be restored over the good install on the next run.
  - `test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild` makes the backup undeletable and runs the update twice. It expects the rebuilt install to survive the second run, the marker written, no `.before-node-rebuild`, only dot-named leftovers, and the warning. Against f79d7b4e it fails because the second run reverted the install (`rebuilt` missing).
- **4234006752 (P2, MISE_INSTALLS_DIR)** (fixed:61c38cd6). mise installs into `MISE_INSTALLS_DIR` when it is set: offline, `mise where jq` with it set answers under that directory (validation §25). The scan now reads `MISE_INSTALLS_DIR` first. A `custom MISE_INSTALLS_DIR` case in the killed-run test fails against f79d7b4e with exit 1.
- **4234006735 (P2, the required bare install offline under the cooldown)**: proposed `not-applicable`, and resolved `not-applicable` by the orchestrator on two probes of its own (Revise round 9).
  - The Bot cites mise 2026.5.6 (jdx/mise discussion 9859): with a release-age cutoff active, mise no longer treats an installed fuzzy match as sufficient, and fetches metadata first. The repository pins mise 2026.9.17.
  - I probed that exact case on 2026.9.17, outside the network (validation §25): `minimum_release_age = "72h"`, an empty cache, `latest` requests for two installed tools. A bare `mise install --yes` printed "2 already installed in 0ms" and exited 0.
  - It printed no fetch warning, although every real fetch in §12 printed `unable to fetch versions` or timed out after 20 s. `MISE_VERBOSE=1` added only "all tools are installed". The cache afterwards held only a lockfile and a bin_paths entry, so no metadata was fetched.
  - §12 also shows that the alternative the Bot proposes, checking locally for missing installs, has no reliable probe offline: `mise ls --current --missing` printed nothing for an uninstalled `latest` request (yq) and exited 0.
  - **The exposure I cannot test:** `mise self-update` runs before the bare install, so a host may run a newer mise by then (2026.10.4 is already offered). To check a newer binary outside the sandbox, use the same scratch recipe: that config, an empty `MISE_CACHE_DIR`, a `MISE_DATA_DIR` holding copies of the installed tools, no network, then a bare `mise install --yes`.

## Revise round 9 (orchestrator audit of 61c38cd6: incorrect, 1 P2 and 1 P3)

The orchestrator accepted round 8 on its substance and resolved the three Bot threads on f79d7b4e: 4234006744 and 4234006752 as fixed in 61c38cd6, and 4234006735 as `not-applicable`. For that one it ran two probes of its own: an empty cache, and a valid or expired cache naming a newer release.

1. **P2: a restore could bury the backup inside a partial install that survives `rm -rf`** (fixed:a9eb7f02).
   - `restore_npm_install` ran `rm -rf "$1"` unchecked. When the partial install could not be deleted (a read-only entry, an I/O error), `mv "$2" "$1"` moved the working backup *inside* the surviving directory and returned 0. The tool was gone, the backup was buried, and nothing reported it.
   - The restore now succeeds only when `rm -rf` succeeds, the old path is really gone (`[ ! -e "$1" ]`), and the move succeeds. Otherwise it prints `required failure: could not restore <install> from <backup>` and counts a required failure, so the update exits nonzero whichever caller hit it: the leftover scan, the trap, or the rebuild's failure path. The backup stays at `<install>.before-node-rebuild`, where the next run looks.
   - The leftover scan continues past a failed restore, so one stuck tool does not keep the others from being put back.
   - `test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed` models the killed-rebuild state with a partial install holding a read-only directory. It skips as root and restores the mode in `finally`. It expects:
     - the backup still at `<tool>.before-node-rebuild` with `original` in it;
     - nothing moved into the partial install;
     - exit 1, with the required failure naming both paths.
   - Against 61c38cd6 it fails because the backup had been moved inside the partial install (validation §26.1).
2. **P3: evidence** (validation §26.2, §26.3).
   - Section 17's grep pattern cannot produce the `1:min-release-age=7` line pasted under it. The session transcript shows what actually ran: the grep over `upgrade-tools.sh` and `config.toml`, then `grep -n 'min-release-age' home/dot_npmrc`, which the paste never printed. §26.2 reruns the shown command exactly at its head, 64c6d8a6, then prints the npmrc grep as its own command.
   - Section 14 piped both `make -n` runs through a `grep -E` filter it never printed. §26.3 reruns the same scratch-repository script with the filters removed and pastes the complete transcripts. Sections 14 and 17 point to section 26.

## Decisions

[memory:decision] dotfiles-T118 (worker 2026-10-09): `scripts/upgrade-tools.sh` pins `MISE_CONFIG_DIR` to the chezmoi-applied host config (`${HOME}/.config/mise`, unconditionally) and keeps `MISE_CEILING_PATHS` at the checkout root, so only the host config's tools are installed and upgraded; Codex and Claude Code are ordinary `latest` mise tools behind the 72-hour cooldown, `mise self-update` waits through `self_update.minimum_release_age = "72h"`, and `update-agent-assets.sh`'s `mise install --force` stays as the broken-CLI repair path.

[memory:failure] dotfiles-T118 (worker 2026-10-09): `mise settings ls --all` omits a setting that is unset and has no default (`self_update.minimum_release_age` on 2026.9.17), so its absence from the listing is not evidence that the key does not exist; probe with `mise settings set <key> <value>` against an unknown-key control.

[memory:failure] dotfiles-T118 revise 1 (worker 2026-10-09): offline, `mise install --yes <tool>` on a `latest` request exits 1 even when the tool is installed (it re-resolves `latest` remotely); `scripts/upgrade-tools.sh` therefore installs with one bare `mise install --yes` (exit 0 offline when every declared tool is installed, 1 when one is missing) and upgrades per tool, which exits 0 offline.

[memory:decision] dotfiles-T118 Amendment 7 (operator 2026-10-09): the mise cooldown is 72h (`minimum_release_age` and `self_update.minimum_release_age`), superseding 7d; Homebrew upgrades verify bottle attestations through gh when present; the day-one exception, npm provenance and the Claude Code channel are T120.

[memory:failure] dotfiles-T118 revise 2 (worker 2026-10-09): make parses the Makefile before a recipe runs, so a `make update` recipe that pulls its own checkout ran the pre-pull recipe; `update` now pulls and then runs `$(MAKE) update-tree`, a second make that reads the fetched Makefile, and a clone that predates the split needs one `git -C <clone> pull && make -C <clone> update`.

[memory:failure] dotfiles-T118 revise 3 (worker 2026-10-09): Codex execpolicy matches whole tokens, so forbidding `make update` did not cover the new `make update-tree`; every host-mutating make target needs its own entry in `home/dot_codex/rules/default.rules` and a required prefix in `tests/unit/test_codex_execpolicy.py`.

[memory:failure] dotfiles-T118 revise 4 (worker 2026-10-09): a RESULT must reconcile every top-level Bot comment on the PR, including those on heads whose Bot wait was skipped; two P2 threads on b621af77 went unnamed in round 3.

## CompactionDB

Run from the main checkout through the permission gate (validation §8):

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '<the task file [memory:decision] line, verbatim>'
```

Memory ids `046ed7da-dea2-40eb-8de3-95259960d507` (the task decision) and `724cad0d-3812-43a1-a733-bb15ac37d64e` (Amendment 7: 72h supersedes 7d).

## Hooks

- The Understand-Anything stale-graph hook did not fire in this task.
- No Plan Mode and no Crit plan review server were started (`plan-mode-used` does not apply).

## Review evidence

`.orchestration/validation/dotfiles-T118-rolling-tools-single-update-a01-worker-crit.json` and `-worker-review-receipt.md`. Crit data was unavailable, so an independent read-only subagent review of 46a73f11 was recorded in the Crit JSON shape, together with the Bot, CI and orchestrator-audit findings that followed: 52 records (`jq length`), all resolved.

cost: n/a
