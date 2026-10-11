# AGMSG-TASK dotfiles-T120-npm-provenance-and-claude-channel-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Operator decision 2026-10-09 on the orchestrator's supply-chain research (recorded in T118 Amendment 7 and the acceptance records): the cooldown is 72 hours (T118); npm tools are verified against their registry signatures and provenance attestations after install, and Codex, whose provenance verifies, takes releases on day one; Claude Code leaves the mise npm backend for Anthropic's own distribution with the signed manifest verified by us and the update channel governed by Anthropic's `autoUpdatesChannel`; a uv tool, if one is ever added, goes through mise's `pipx:` backend. Kind: the update scripts, the mise config, the zsh helper, the doctor script, README and tests; no permission, sandbox or hook block; Claude seat allowed. Dispatched after T119 merged (file overlap on `scripts/update-agent-assets.sh` and the tests).

## Evidence the design rests on (2026-10-09, keep the citations in README)

- `@openai/codex` and `ccusage` publish npm provenance attestations and registry signatures (registry metadata `dist.attestations`, `dist.signatures`); `@anthropic-ai/claude-code` publishes registry signatures only, no provenance. The mise npm backend installs with npm, which verifies neither at install time; `npm audit signatures --include-attestations` is the documented check ("npm itself can validate registry signatures and provenance attestations", github.blog "Introducing npm package provenance"; docs.npmjs.com config `--include-attestations`).
- Anthropic's native distribution publishes per-release `manifest.json` with SHA256 checksums for every platform binary, signed with the Anthropic release key (fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`, key at `https://downloads.claude.ai/keys/claude-code.asc`, signatures from 2.1.89); the official `install.sh` verifies the binary's SHA256 against the manifest but not the manifest's GPG signature (read on 2026-10-09); native installations auto-update in the background on the `latest` or `stable` channel (`autoUpdatesChannel`; stable is "typically about one week old, skipping releases with major regressions"); macOS binaries are code-signed and notarized. Source: code.claude.com/docs/en/getting-started/installation. This host already renders `autoUpdatesChannel: stable` from the manifest (`claude.autoUpdatesChannel`).
- Provenance proves who built a release from which source; it does not catch a malicious release published through a legitimate account, which is what the 72-hour cooldown is for. Day-one is therefore granted only where provenance verification is active (Codex), per the operator.

## Target behaviour, stated once

1. **npm provenance check after install.** `scripts/upgrade-tools.sh` gains a phase after the mise phase: for every `npm:` tool in the applied config, verify the installed version's registry signature and, when the registry publishes one, its provenance attestation. Establish the working command with the real binary first and paste it: candidate A, in a scratch directory, `npm install --package-lock-only --ignore-scripts <package>@<installed version>` then `npm audit signatures --include-attestations` (set `npm_config_cache` to a scratch path; the orchestrator's sandbox probe failed only on the cache permission); candidate B, if A cannot be made to work, fetch `dist.attestations.url` from the registry and verify the bundle with the sigstore tooling the repository already has. A package whose attestation fails verification, or whose registry signature fails, makes the phase a required failure (so `make update` stops and names the package); a package that publishes no attestation is reported as "registry signature only" in one summary line and does not fail. Unit-test the phase with fakes for the install and audit commands (pass, attestation failure, signature-only).
2. **Codex day-one.** With the check in place, `home/dot_mise/config.toml` gets `minimum_release_age_excludes = ["npm:@openai/codex"]` with a comment naming the reason (provenance verified after every install); `.zshrc`'s `claude-update` helper becomes a `codex-update`/agent helper only if it still has a purpose after item 3; otherwise delete it with its comment.
3. **Claude Code on Anthropic's distribution.** Remove `npm:@anthropic-ai/claude-code` from `home/dot_mise/config.toml` and from `install/common/mise.sh`'s install list; `ensure_mise_npm_agent_cli claude …` in `scripts/update-agent-assets.sh` becomes `ensure_claude_code`: run the official installer (`curl -fsSL https://claude.ai/install.sh | bash -s <channel>`, channel from the manifest's `claude.autoUpdatesChannel`, rendered into the script or read from the applied settings) only when `claude` is missing or not the native layout (`~/.local/bin/claude` → `~/.local/share/claude/versions/<v>`); after any install, verify: download `manifest.json` and `manifest.json.sig` for the installed version from `https://downloads.claude.ai/claude-code-releases/<version>/`, import the published key into a temporary GNUPGHOME, check the fingerprint equals the one above, `gpg --verify`, and compare the installed binary's SHA256 with `platforms.<platform>.checksum`; on any mismatch remove the just-installed version and fail the step. The `allow_builds` entry goes with the tool. Remove the stale mise install once (`mise uninstall npm:@anthropic-ai/claude-code` when present, after the native install verified). Update `scripts/check-tools.sh` (doctor) to report the native install and its channel, and the `manifest_record` step name. Day-to-day updates are Anthropic's auto-updater on the configured channel; `make update` re-verifies the installed binary against the signed manifest on every run (cheap: two small downloads) and reports the version and channel.
4. **uv rule.** README: a Python CLI is added as a mise `pipx:` tool, never with `uv tool install`, because the `pipx:` backend reports release dates (the cooldown applies) and uv does not verify PyPI attestations; `upgrade_uv_tools` stays for machines that already have uv tools but prints nothing when `uv tool list` is empty.
5. **README and tests.** The Tool versions paragraph gains the npm provenance sentence (which packages publish attestations, what the check does, what happens on failure), the Codex exception with its reason, and the Claude Code paragraph (native distribution, signed manifest verified by `make update`, channel from `autoUpdatesChannel`, auto-update by Anthropic). Tests: `test_supply_chain_policy.py` (excludes list, no claude-code npm tool, the provenance phase present), `test_update_agent_assets_*` for `ensure_claude_code` (fake `curl`, `gpg`, `shasum`: good signature and checksum pass; bad signature fails and removes; wrong fingerprint fails), `test_runtime_health.py` for the provenance phase, `scripts/check-tools.sh` tests if any.

Forbidden: anything else; running the real installers or `mise uninstall` against the host (scratch `HOME` and prefixes only; the orchestrator runs the live `make update`); `make update`; touching `~/.local/share/chezmoi`; thread resolution.

## Standing instruction on Bot and CI findings (operator, 2026-10-09)

Every Codex Bot finding and every CI failure on the PR is fixed at its root cause in the PR itself, not dispositioned. A `not-applicable` is reserved for a finding that is factually wrong, with the refuting command and output pasted in the reply. A finding on the task's own wording is still fixed in the PR. "Out of scope" is not a disposition for a finding on files the PR touches: report the scope gap and the orchestrator amends the allowed files. Recheck the reviews once more right before sending the RESULT.

[memory:decision] dotfiles-T120 (orchestrator 2026-10-09): npm tools are verified after install with `npm audit signatures --include-attestations` (attestation or signature failure stops `make update`; signature-only packages are reported); Codex is excluded from the cooldown because its provenance verifies; Claude Code is installed from Anthropic's native distribution with the release manifest's GPG signature and the binary checksum verified by `make update`, and updated by Anthropic's auto-updater on the `autoUpdatesChannel` channel; Python CLIs go through mise `pipx:`.

## Repo / branch

`.claude/worktrees/worker-c`; after T119 merged: `git fetch origin`; `git switch -c feat/npm-provenance-and-claude-channel --no-track origin/main`.

## Allowed files

`scripts/upgrade-tools.sh`, `home/dot_mise/config.toml`, `install/common/mise.sh` (the install list), `scripts/update-agent-assets.sh` (the agent CLI section), `scripts/check-tools.sh`, `home/dot_zshrc` (the helper), `home/dot_agents/agent-config.yaml` (only if `ensure_claude_code` reads the channel from the manifest through the renderer), `scripts/generate-agent-configs.py` (same condition), `README.md` (the Tool versions paragraph and the agent CLI sentences), `tests/unit/test_supply_chain_policy.py`, `tests/unit/test_runtime_health.py`, `tests/unit/test_update_agent_assets*.py`, plus whatever `git grep -nE 'claude-code|ensure_mise_npm_agent_cli|claude-update' -- scripts tests install home README.md` names on your branch base (report any file outside this list as a scope gap). Artifacts at the standard `dotfiles-T120-npm-provenance-and-claude-channel-a01` paths in the main checkout, masked.

## Validation commands (paste verbatim output, whole)

```
<provenance probe: the working npm audit signatures invocation on a scratch install of @openai/codex and of a signature-only package, with output>
<scratch-HOME ensure_claude_code run: install, manifest and signature download, gpg fingerprint check, checksum match; then a forged-checksum case failing and removing>
shellcheck scripts/upgrade-tools.sh scripts/update-agent-assets.sh scripts/check-tools.sh install/common/mise.sh; echo "rc=$?"
uv run python -m unittest tests.unit.test_supply_chain_policy tests.unit.test_runtime_health <the update-agent-assets modules> 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(agents): verify npm provenance after install and move Claude Code to its signed native distribution`, English body with the evidence section above and the user-visible changes: Codex updates on day one, Claude Code is no longer a mise tool and follows `autoUpdatesChannel`, a failed provenance or manifest check stops `make update`; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T120-npm-provenance-and-claude-channel-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=24.

## Amendment 1 (orchestrator, 2026-10-10) — dispatch after T119, in `.claude/worktrees/worker-e`, concurrently with T124 wave 1

T119 merged as d29ce4c1 (PR #312): the manifest's `assets:` section, `scripts/update-agent-assets.sh` and `scripts/upgrade-tools.sh` changed shape (release helper, fallback pins, every-apply wrappers; read the T119 acceptance record first). Branch from `origin/main` at or after d29ce4c1 in `.claude/worktrees/worker-e` (`git switch -c feat/npm-provenance-and-claude-channel --no-track origin/main`). Concurrent with T124 wave 1 (`feat/task-validator`): files are disjoint except README, where you edit only the Tool versions paragraph and the agent CLI sentences, never the regime section. The task is `security: true` under T124's design tier (installers, supply chain); the T124 validator is not merged yet, so this task carries no front matter; the design review requirement applies from wave 2a on, and this task's acceptance record says so. The standing instruction on Bot/CI findings and T119's sandbox-conduct rule (every command inside the sandbox except Worker Playbook step 4's cases; refusals reported, never reworked; the sandbox record lists every out-of-sandbox command with `permission_gated_commands: <n>`) apply verbatim. Under the accepted T124 design the reset rule applies by hand: after two revise rounds with implementation findings the orchestrator writes a design reset instead of a third round. One correction to the task body: the Claude Code `ensure_claude_code` verification follows T119's rule, nothing executes before an independent check passes: the installer script from `claude.ai/install.sh` is fetched, its sha256 recorded in the manifest with a reason like the other installer scripts (or, if Anthropic publishes a signature for it, verified with that), and the manifest/GPG verification of the downloaded binary runs before the binary is executed, never after.

## Amendment 2 (orchestrator, 2026-10-10) — blocked PONG answered

- **d1, d2 (probes refused by the gate).** Correct to stop and report; the admitted rework of d1 goes into the sandbox record and nothing more. The two live probes are the orchestrator's (precedent: T118 Amendment 2); their output is appended below as Amendment 3 once run. In the sandbox, use the `install/common/mise.sh` pattern (`gpg --batch --dearmor` into a scratch keyring, then `gpgv --keyring`), which needs no agent socket; if the sandbox still refuses, the unit tests use fakes and the live evidence is the orchestrator's probe plus CI.
- **q1: option A.** Never run `install.sh`: `ensure_claude_code` resolves the channel to a version (`downloads.claude.ai/claude-code-releases/<channel>` → version), fetches `manifest.json` and `manifest.json.sig`, verifies the signature with the pinned fingerprint `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE` in a scratch GNUPGHOME (the mise.sh key/fingerprint/fail-closed pattern; the key file committed under `home/` like the AWS key, with the keyserver as fallback only), fetches `platforms.<platform>/claude`, checks its sha256 against the verified manifest, and only then installs it into the native layout (`~/.local/share/claude/versions/<v>`, `~/.local/bin/claude`) and compares the installed binary's version with the verified download. Amendment 1's sentence about recording `install.sh`'s sha256 is withdrawn: no script runs. Auto-update: Anthropic's updater keeps running on the configured channel; `make update` re-verifies the active binary against the signed manifest of its version on every run and fails when the signature or checksum does not verify.
- **q2: in scope via the grep clause.** `executable_herdr-agents` (the dead claude-code shadow heal at ~2048) and `tests/unit/test_herdr_agents.py:1823`, `scripts/check-agent-runtime.py` (`ASSET_STEP_FUNCTIONS`, `MISE_STEP_IDENTITIES`, `asset_repair_action`) and `tests/unit/test_check_agent_runtime.py`, `tests/unit/test_remove_agent_asset.py`, `tests/unit/test_asset_manifest.py`, `tests/install/common/lifecycle.bats:296` join `allowed_files` for the claude-code lines only. `test_herdr_agents.py` is also touched by T124 wave 1 (one test near line 2834) and wave 3b (one hunk near 4321): keep to the claude-code hunk at 1823; the latest PR takes `gh pr update-branch`.
- **q3: npm's cooldown is separate from mise's.** `~/.npmrc` `min-release-age=3` stays the single npm policy. Confirm from the mise docs whether `minimum_release_age_excludes` reaches the npm backend's version listing and paste the doc line; independent of that, the Codex install/upgrade command (and only that command) runs with `npm_config_min_release_age=0` in its environment, with a comment naming the reason (provenance is verified after every install, Amendment 7 of T118 / this task's item 2); no other npm tool gets the override, and a test asserts the override is scoped to the Codex command.

## Amendment 3 (orchestrator, 2026-10-10) — the two live probes, run by the orchestrator outside its sandbox against scratch directories

**GPG, Claude Code release manifest (stable = 2.1.287 at run time):**
```
$ curl -fsSL https://downloads.claude.ai/keys/claude-code.asc -o key.asc
$ curl -fsSL https://downloads.claude.ai/claude-code-releases/2.1.287/manifest.json -o manifest.json
$ curl -fsSL https://downloads.claude.ai/claude-code-releases/2.1.287/manifest.json.sig -o manifest.json.sig
$ gpg --homedir gnupg --batch --with-colons --import-options show-only --import key.asc | awk -F: '$1=="fpr"{print "fpr", $10} $1=="pub"{print "pub validity", $2, "expires", $7}'
pub validity - expires
fpr 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE
$ gpg --homedir gnupg --batch --yes --dearmor --output keyring.gpg key.asc && gpgv --keyring ./keyring.gpg manifest.json.sig manifest.json
gpgv: Signature made Fri Oct  2 01:28:04 2026 JST
gpgv:                using RSA key 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE
gpgv: Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"
gpgv rc=0
$ head -c 400 manifest.json
{ "version": "2.1.287", "manifestSignatureEnforcement": "flag", "commit": "3c446a1b…", "buildDate": "2026-10-01T16:26:16Z", "platforms": { "darwin-arm64": { "binary": "claude", "checksum": "6eab8333fe2121553100d8f40bfada384a3e989b94f947e18ba6677a6fcb41ea", "size": 227827120 …
```
So the `gpg --dearmor` + `gpgv --keyring` pattern verifies without an agent; the key has no expiry; the manifest carries per-platform sha256 and size. Note `manifestSignatureEnforcement: "flag"`: Anthropic's own installer treats the signature as optional; ours does not.

**npm provenance, candidate A corrected:** `--package-lock-only` installs nothing and `npm audit signatures` then reports "found no dependencies to audit that were installed from a supported registry". A real install with scripts ignored is required:
```
$ npm install --ignore-scripts --no-audit --no-fund @openai/codex@latest @anthropic-ai/claude-code@latest ccusage@latest   (scratch dir, npm_config_cache in scratch)
added 6 packages in 4s
$ npm audit signatures --include-attestations
audited 6 packages in 1s
6 packages have verified registry signatures
4 packages have verified attestations
audit rc=0
$ npm view <pkg> --json | jq '{version, sig: (.dist.signatures|length), att: .dist.attestations.url}'
@openai/codex: {"version":"0.162.1","sig":2,"att":"https://registry.npmjs.org/-/npm/v1/attestations/@openai%2fcodex@0.162.1"}
@anthropic-ai/claude-code: {"version":"2.1.296","sig":2,"att":null}
ccusage: {"version":"20.0.28","sig":2,"att":"…/attestations/ccusage@20.0.28"}
```
**Semantics the task text must state:** `npm audit signatures` verifies the registry's signature and provenance attestation over the package's registry integrity hash (the one npm checked when it downloaded the tarball); it does not re-hash files on disk (appending a byte to `node_modules/@openai/codex/package.json` left the audit at rc=0). So the phase proves that the version installed came from a signed, attested publish, not that the installed tree is unmodified afterwards; say exactly that in README, and implement the phase as: for each `npm:` tool, in a scratch directory with `npm_config_cache` under it, `npm install --ignore-scripts --no-audit --no-fund <package>@<installed version>` then `npm audit signatures --include-attestations`, parsing the two count lines (`N packages have verified registry signatures`, `M packages have verified attestations`, and any `invalid`/`missing` lines, which are the failure case); a package with no attestation is reported as signature-only; Claude Code is no longer an npm tool after item 3, so the list is Codex, ccusage, ccstatusline, pnpm, prettier (whatever `home/dot_mise/config.toml` names). Unit tests fake `npm` for the three outcomes.

## Push form (orchestrator, 2026-10-10)

The host SSH agent holds no identity and the global git config rewrites pushes to SSH, so the authorized push form (used by every task since T118) is: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles <branch>` (gh keyring login; no config file change). Use it for every push; it is not a rework of a refusal, it is the documented form.

## Amendment 4 (orchestrator, 2026-10-10) — q4–q9 and the orchestrator's Codex probe

> **q5 of this amendment is superseded by Amendment 5** (the probe below used a scratch config without the repository's `package_manager = "npm"`; its conclusion about `install_env` and `~/.npmrc` is wrong for this repository). q4, q6–q9 stand.

- **q4 yes.** `assets.claude-code` (source `https-download`, `release: latest` resolved through the channel, `verify: gpg`, `gpg_fingerprint`, the committed key path, render into `scripts/update-agent-assets.sh` like aws-cli); `home/dot_agents/agent-config.yaml` `assets:` joins `allowed_files` for that entry and the removal of the npm claude-code lines.
- **q5, decided by a live probe (orchestrator, scratch `MISE_CONFIG_DIR`/`MISE_DATA_DIR`, mise 2026.10.3):** `minimum_release_age_excludes = ["npm:@openai/codex"]` works (`mise latest npm:@openai/codex` → 0.162.1 with the exclusion, 0.160.1 without); `install_env` is **ignored** for the npm backend: `WARN install_env (npm_config_min_release_age) is ignored for npm:@openai/codex: mise installs through the embedded aube package manager, which runs in-process rather than as a subprocess … anything else has to be set in mise's own environment`, and the install of 0.162.1 (younger than the 72 h window) succeeded, so neither `install_env` nor `~/.npmrc`'s `min-release-age=3` governs mise's npm installs: mise's own `minimum_release_age` does. Consequences: no `install_env`, no shell override anywhere; the Codex exclusion is the one line in `config.toml`; README's Tool versions paragraph states that mise's embedded package manager does not read `~/.npmrc`'s cooldown, so `minimum_release_age` is the policy for mise-installed npm tools and `~/.npmrc` `min-release-age=3` governs direct `npm`/`npx` use only (this corrects T118's "single npm policy" sentence; cite the probe). Your `MISE_DEBUG` check is therefore not needed; paste this amendment's lines as the evidence.
- **q6 yes:** the provenance phase's scratch `npm install --ignore-scripts <pkg>@<installed version>` runs with `npm_config_min_release_age=0` only for tools listed in `mise settings get minimum_release_age_excludes`, otherwise a day-one Codex version cannot be fetched for the audit; one permitted occurrence, tested.
- **q7 yes:** `install <EXACT_VERSION>` from the verified binary, then require active version == resolved and sha256(active) == signed checksum, else remove `versions/<V>` and fail. The live-run checks you list (claude doctor on stable, chezmoi status clean) are the orchestrator's after the merge.
- **q8 yes:** no gpg → install nothing, print the remedy, keep the existing install; `install/macos/common/dependencies.sh` already installs gnupg and Ubuntu ships gpgv, so the case is a fresh macOS mid-bootstrap only.
- **q9 yes:** `mise uninstall` only when the stale manifest step is absent; otherwise print the `remove-agent-asset` remedy; no `manifest_forget` helper.
- **d3** recorded as a refusal, not reworked: correct.
- **Follow-up noted for T123, not yours:** `install/common/mise.sh` runs `gpgv --keyring` without `--homedir`, so a key in the user's `trustedkeys.kbx` could also validate; your `ensure_claude_code` passes `--homedir` to a scratch directory, which is the right form.

## Amendment 5 (orchestrator, 2026-10-10) — q10: the worker was right; Amendment 4's q5 is corrected

My first probe's scratch config lacked the repository's `[settings.npm] package_manager = "npm"`, so mise took its embedded in-process path. Re-probed with that setting and the host's npm 11.20.0 on PATH (mise 2026.10.3, scratch `MISE_CONFIG_DIR`/`MISE_DATA_DIR`, `~/.npmrc` `min-release-age=3`, Codex 0.162.1 published 2026-10-09T19:50Z):

```
B: excludes only, no install_env
DEBUG $ npm install -g @openai/codex@0.162.1 --prefix <scratch>/installs/npm-openai-codex/0.162.1 --ignore-scripts=true
npm error code ETARGET
npm error notarget No matching version found for @openai/codex@0.162.1 with a date before 10/7/2026, 7:00:16 PM.
ERROR npm failed … rc=1

A: excludes + install_env = { npm_config_min_release_age = "0" }
DEBUG $ npm install -g @openai/codex@0.162.1 --prefix <scratch>/installs/npm-openai-codex/0.162.1 --ignore-scripts=true
INFO  npm:@openai/codex@0.162.1 ✓ installed   rc=0
```

So on this repository's configuration mise shells out to npm, `~/.npmrc`'s `min-release-age=3` governs mise's npm installs as well (and is consistent with mise's 72 h), `minimum_release_age_excludes` alone lets mise pick a day-one Codex that npm then refuses, and `install_env` is honoured and needed. Decisions, replacing Amendment 4's q5: `home/dot_mise/config.toml` carries both `minimum_release_age_excludes = ["npm:@openai/codex"]` and `"npm:@openai/codex" = { version = "latest", install_env = { npm_config_min_release_age = "0" } }` with one comment (provenance is verified after every install); no shell override anywhere, so the existing test forbidding `npm_config_min_release_age=` in the scripts stays; README's Tool versions paragraph says: with `package_manager = "npm"` mise runs npm as a subprocess, `~/.npmrc` `min-release-age=3` is the npm-side cooldown for mise tools and direct npm alike (equal to mise's 72 h), and Codex's day-one exception is the pair of config lines above. Paste both probe blocks as the evidence. q6 stands (the scratch provenance install of an excluded tool runs with `npm_config_min_release_age=0`). The orchestrator records this correction against itself in the acceptance record: the first probe did not reproduce the repository's configuration, and the worker's check caught it.

## Concurrency note (orchestrator, 2026-10-10)

Three in-flight tasks touch `tests/unit/test_herdr_agents.py` in disjoint hunks (wave 1 near 2834, T120 at 1823, wave 3b at 4321) and two touch `home/dot_local/bin/common/executable_herdr-agents` in disjoint regions (T120: the claude-code shadow heal near 2048; wave 3b: the audit prompt). This is an orchestrator exception to the pairwise-disjoint code-file rule, taken for throughput and recorded in each acceptance record; merge order is by readiness, and every later PR takes `gh pr update-branch` and re-runs CI, the Bot wait and the gate on the merged head. A real conflict blocks only that PR.

## Amendment 6 (orchestrator, 2026-10-10) — npm fact for the provenance phase

npm's `audit signatures` used to re-apply `min-release-age` as a `before` filter when re-resolving exact installed versions (ETARGET on versions younger than the cutoff, npm/cli#9277); the fix (npm/cli PR #9430, merged 2026-05-28) sets `before: null` in `verify-signatures.js`, so on the npm this repository runs (11.19.1 on PATH, 11.20.0 under mise's node) the audit step itself needs no cooldown override. The override of q6 therefore applies only to the scratch `npm install --ignore-scripts <pkg>@<installed version>` step for tools in `minimum_release_age_excludes`, and the README states which npm version makes the audit step independent of the cooldown. Keep the test for the override scoped to that install step.

## Amendment 7 (orchestrator, 2026-10-10) — q11: remove-agent-asset must be able to remove the native Claude Code install

Default accepted. `home/dot_local/bin/common/executable_remove-agent-asset` and `tests/unit/test_remove_agent_asset.py` join `allowed_files` for this change only: `path_is_in_safe_root` gains two narrowly scoped roots, the exact path `~/.local/bin/claude` (removed as a symlink, never followed) and the `~/.local/share/claude` prefix; one test asserts `remove-agent-asset ensure_claude_code --yes` removes both and the manifest step, and that a path outside those roots is still refused. Record the Bot threads 4237392848 and 4237392853 as fixed in the commit that carries this.

## Amendment 8 (orchestrator, 2026-10-10) — q12: `make update` moves Claude Code on its channel; Anthropic's updater stays off

**Option B.** The task premise was wrong: `claude.autoUpdates: false` is rendered into the managed settings on these hosts (a deliberate T118-era choice: nothing on the host updates outside `make update`), so Anthropic's updater never runs. The corrected design is consistent with the regime's principle (nothing executes before our own verification): `ensure_claude_code` resolves the channel head (`autoUpdatesChannel`, `stable` here) on every `make update`, and when it is newer than the active version installs it through the same verified path (signed manifest and sha256 checked before anything runs, then the post-install check); `autoUpdates` stays `false`; README states that Claude Code moves only through `make update`, on the configured channel, verified by us. Record the Bot thread 4237365212 as `fixed:<sha>`.

**The "also" (the old claude leaves mise's PATH at apply before the native install exists).** Accepted as a documented gap, narrowed: the order inside `make update` is apply → `ensure_claude_code` in the same run, so the window is one run; on a host where the native install cannot run (first run offline, or a fresh macOS before gnupg is installed) `ensure_claude_code` prints the remedy (`run make update again once online` / `once gnupg is present`), exits 0, and `scripts/check-tools.sh` reports `claude` missing with the same hint. The `mise uninstall` of the old npm tool still happens only after a verified native install (Amendment 2). README names the gap.

**Process note, recorded for the operator.** This is T120's eighth amendment. Under T126 INV-6 (four amendments) a task reaches the reset count; T120 predates T126 and T126 says it continues under V2 applied by hand. Amendments 1–4 and 6–7 answered scope and evidence questions; Amendment 5 corrected the orchestrator's own probe; this one corrects a premise of the task text. The orchestrator judges that a reset would discard a near-complete, CI-green, Bot-clean implementation of an unchanged threat model, proceeds, and records this as an exception visible in the acceptance record; the operator may overrule it.
