# omp skills: the pstack skills inside every seat

omp 18.11.3 (`@oh-my-pi/pi-coding-agent`, installed under `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent`; paths below are relative to it) loads the skills under `~/.agents/skills` into every seat. This page names the setting that pins that, where the skills come from, how to prove what a seat loads, and how a seat's own skill coexists with the pstack set. Facts marked "measured" come from the U10 dry run of 2026-10-23 under a scratch `HOME`.

## The key

`skills.customDirectories` in `~/.omp/agent/config.yml`.

- omp registers it at `src/extensibility/settings.ts:65-69` (type `array`, default empty) and reads it in `loadSkills` at `src/extensibility/skills.ts:471-480`: each entry goes through `expandTilde`, is scanned one level deep for `*/SKILL.md`, and is admitted under the provider id `custom` at level `user` with `requireDescription: true`.
- The manifest `home/dot_agents/agent-config.yaml` holds the list as `omp.skills_directories` (default `~/.agents/skills`, the same root as `skills.canonical_dir`). `scripts/generate-agent-configs.py` validates it (`~/` or absolute, no shell characters) and renders `home/.chezmoitemplates/omp-config-managed.yml`; `make render-check` fails when the template is stale.
- `home/dot_omp/private_agent/modify_private_config.yml` merges `modelRoles.default`, `skills.customDirectories` and the top-level `extensions` list (`docs/pi-claude-bridge.md`, "Plain launch") into the live file and keeps every other key omp wrote. It writes the directories with `~` expanded to `$HOME`, because `omp skill list` resolves a non-absolute entry against the inspected directory before omp expands `~` (`src/cli/skill-list.ts:58-64`); measured, `~/.agents/skills` lists nothing through that command while the absolute path lists the skills. A second apply is a no-op (`tests/unit/test_omp_config_merge.py`).
- The merge reaches the default profile only. A seat started with `omp --profile <name>` reads `~/.omp/profiles/<name>/agent/config.yml` instead (pi-utils `src/dirs.ts:312-315`), so a named profile gets the key, and its model route, from the per-role overlay below.

## Per-role overlays

`~/.agents/omp/profiles/<role>.yml`, one file per key of `omp.roles` in the manifest (`orchestrator: deep`, `worker: standard`, `audit: audit`, `review: review`, `security: security`). Each holds `modelRoles.default` from the mapped profile's `omp.model` and `skills.customDirectories` from `omp.skills_directories`; the seat launcher passes the role's file as a second `--config` beside the policy overlay (`home/dot_agents/omp/policies/<role>.yml`), so a named profile gets its model route and skill roots without a hand edit of `~/.omp/profiles/<role>/agent/config.yml`.

- `scripts/generate-agent-configs.py` renders them as `home/dot_agents/omp/profiles/<role>.yml.tmpl`; `make render-check` fails when a file is stale, and the generator fails when `omp.roles` is missing, names an unknown profile, or carries a role name that is not launcher-safe. `tests/unit/test_generate_agent_configs.py` holds the cases and checks that every policy file has an overlay.
- The committed file is a chezmoi template so that the deployed file carries the absolute home (`{{ .chezmoi.homeDir }}/.agents/skills`) while the repository stays machine-independent. The absolute form is needed because omp expands `~` in `skills.customDirectories` only on the session route (`loadSkills`, `src/extensibility/skills.ts:471-473`); `omp skill list` resolves a non-absolute entry against the inspected directory first (`src/cli/skill-list.ts:58-64`), and measured, the `~` form lists nothing there. `modelRoles.default` is a plain string copied from the layer (`src/config/model-settings.ts:109`, `src/config/settings.ts:1626-1638`) and gets no path handling.
- Each overlay also carries `setupVersion: 2` and `startup.setupWizard: false`. A seat profile has no `~/.omp/profiles/<role>/agent/config.yml`, so `setupVersion` reads its schema default 0 (`src/modes/settings.ts:28`), the cold-launch gate sees it below `CURRENT_SETUP_VERSION` 2 (`src/main.ts:668-671`, pi-tui `src/setup/setup-version.ts:11`) and runs the first-run wizard over the pane (measured 2026-10-23 on the worker and orchestrator seats: `Setup step 1 of 5 / Sign in to your providers`, where a keypress starts a provider login). `startup.setupWizard: false` (`src/modes/settings.ts:1085-1095`) empties the scene list (pi-tui `src/setup/wizard.ts:52`), and `setupVersion: 2` keeps the gate from importing the wizard at all (`src/main.ts:669-672`).
- An overlay wins over the profile's own `config.yml` key by key: `runtime override → config overlay → project → global → schema default` (`src/config/settings.ts:879`). `--config` and `PI_CONFIG_FILES` feed the same list (`src/config/settings.ts:674-676`) and the same strict loader, which refuses a missing file (`Config overlay not found`) or a non-mapping (`src/config/settings.ts:2506-2528`).
- The listing and read-back commands take the overlay through `PI_CONFIG_FILES` only: `omp skill list` (`src/cli/skill-list.ts:47`) and `omp config get` (`src/cli/config-cli.ts:164`) call `Settings.init` without the parsed `--config` list, which an interactive or `-p` session passes (`src/main.ts:1886`). Measured, `omp --profile u14test --config <overlay> --no-extensions skill list --json` returns `{"skills":[],"warnings":[]}` under a profile that turns the `agents` provider off, while the same overlay through `PI_CONFIG_FILES` lists the skills.

Dry run of 2026-10-23, omp 18.11.3, wrapper `HOME=$TMPDIR/u14-home`, cwd an empty directory, `~/.omp/profiles/u14test/agent/config.yml` = `skills: {enableAgentsUser: false}` (so only the overlay can supply the skills), `~/.agents/skills/{sharpen,unslop}` linked from the pstack tree, overlay = the worker template rendered by `chezmoi execute-template` under the same `HOME`.

| command                                                                             | result                                                            |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `omp --profile u14test --no-extensions skill list --json`                           | `{"skills":[],"warnings":[]}`                                     |
| `PI_CONFIG_FILES=<overlay> omp --profile u14test --no-extensions skill list --json` | `sharpen` and `unslop`, `"source":"custom:user"`, `"warnings":[]` |
| `PI_CONFIG_FILES=<overlay with ~/.agents/skills> omp … skill list --json`           | `{"skills":[],"warnings":[]}`                                     |
| `PI_CONFIG_FILES=<missing file> omp … skill list --json`                            | `skill list: Config overlay not found: <path>`                    |
| `PI_CONFIG_FILES=<overlay> omp --profile u14test config get modelRoles --json`      | `"value": {"default": "claude-bridge/claude-opus-5-5"}`           |
| `omp --profile u14test config get modelRoles --json`                                | `"value": {}`                                                     |

## The directory

`~/.agents/skills` (manifest `skills.canonical_dir`). omp scans it on two routes:

- The `agents` provider (`src/discovery/agents.ts:30` and `:124-127`, loader `:158-174`) scans `~/.agent/skills` and `~/.agents/skills` at the user level and `.agent/skills` and `.agents/skills` on the walk up from the project. Its user level is on by default: `skills.enableAgentsUser` defaults to `true` (`src/extensibility/settings.ts:57`, gate at `src/extensibility/skills.ts:322`), and `.agents` is not a foreign provider, so `enabledProviders` does not apply to it (`src/capability/index.ts:363-373`; upstream `docs/skills.md`, "Source toggles and filtering"). `enabledProviders` opts the foreign user roots in (`~/.claude`, `~/.codex`, `~/.cursor`; default off), but the `agent-plugins` provider, which reads the Claude Code marketplace registry under `~/.claude` and refused pstack's plugin copy with 56 warnings, is not one of them: the seat overlays switch it off with `disabledProviders: [agent-plugins]` (`omp.disabled_providers` in the manifest, regime-cutover U22).
- `skills.customDirectories`, the key above. It pins the root against a seat setting that turns the provider off (`skills.enableAgentsUser: false`, or `disabledProviders` naming `agents`).

With both routes on, each skill is listed once with no warning. Measured: `source` is `agents:user`, because the provider copy is admitted first and the custom copy of the same real path is skipped (`src/extensibility/skills.ts:466-467`).

## The instrument

`omp skill list [dir] [--json]` (`src/cli/skill-list.ts:94-123`) discovers skills for a directory exactly as a session would (`:27-29`) and prints one `name<TAB>description` row per skill, or the full result with `--json`. The `--mode json` session route of the pilot facts shows the same set through the system prompt, at the cost of a model turn; the listing command needs none.

Dry run of 2026-10-23, omp 18.11.3, wrapper `HOME=$TMPDIR/u10-home`, `~/.agents/skills/{sharpen,unslop}` linked from the pstack tree, cwd an empty directory. Each row is the full stdout of `omp skill list --json`.

| `~/.omp/agent/config.yml`                                                                                         | result                                                            |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| absent                                                                                                            | `sharpen` and `unslop`, `"source":"agents:user"`, `"warnings":[]` |
| `skills: {enableAgentsUser: false}`                                                                               | `{"skills":[],"warnings":[]}`                                     |
| the row above, then the modify script merged the rendered key (`customDirectories: [/…/u10-home/.agents/skills]`) | `sharpen` and `unslop`, `"source":"custom:user"`, `"warnings":[]` |
| `skills: {customDirectories: [/…/u10-home/.agents/skills]}` (the deployed state)                                  | `sharpen` and `unslop`, `"source":"agents:user"`, `"warnings":[]` |

Both skills list with `"hide":true`: their front matter sets `disable-model-invocation: true`, which omp maps to `hide` (`src/extensibility/skills.ts:463`). A hidden skill is left out of the system prompt's `<skills>` listing and stays reachable through `/skill:<name>` and `skill://<name>` (`:37-42`). 56 of the 57 skills in pstack 0.15.30 set that flag.

## The pin

`assets.pstack` in `home/dot_agents/agent-config.yaml`: `pin` is a commit of `cursor/plugins` and `sha256` the digest of GitHub's source archive of that commit (`https://github.com/cursor/plugins/archive/<pin>.tar.gz`). Two chezmoi externals in `home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl` read both values from the manifest (`include` + `fromYaml`, so the pin lives in one place) and extract `harness/pstack/claude-code/skills/*` into `~/.agents/skills` and `harness/pstack/claude-code/docs/**` into `~/.agents/docs` at every `chezmoi apply`, which `make update` runs. `harness/pstack/claude-code` is the Claude Code build of the plugin, the tree the `cursor-plugins` marketplace entry points at, so a seat reads the same bytes as the Claude Code plugin install; the docs land beside the skills because every skill's first paragraph links `../../docs/harness/claude-code.md`. No installer step, clone or receipt exists. chezmoi checks the download against `sha256` and fetches the archive again only when the URL, that is the pin, changes, since `refreshPeriod` stays at its default of zero (chezmoi reference, `.chezmoiexternal` format: `checksum.sha256`, `stripComponents`, `include`, `exact`, `refreshPeriod`); `chezmoi status` reports drift in the deployed files.

Measured 2026-10-23 under `HOME=$TMPDIR/u10b-home` with the rendered externals pointed at the downloaded archive (`tests/unit/test_pstack_asset.py` repeats the run with a fixture archive): `chezmoi apply` placed the 57 skill directories beside a source skill, `~/.agents/docs/harness/claude-code.md` included; a second apply changed nothing; `omp --no-session skill list --json` from an empty directory listed 58 skills with `"warnings":[]`, `poteto-mode` among them with `"hide":true`. A pstack skill named like a skill under `home/dot_agents/skills` makes chezmoi refuse the whole apply (`inconsistent state`, both sources named) instead of overwriting either copy; the test also keeps the two name sets disjoint. `make doctor` runs `scripts/update-agent-assets.sh check_pstack`, which fails when `poteto-mode/SKILL.md` or the adapter file is missing or when `omp skill list` does not name `poteto-mode`. A skill upstream drops stays deployed until a `.chezmoiremove` entry removes it, because `~/.agents/skills` is not an exact directory (other installers own siblings there); `~/.agents/docs` is exact.

## A seat's skill beside the pstack skills

A seat's own skill (the planned `hcom-worker`, for example) is one more `<name>/SKILL.md` under the same `~/.agents/skills` root, or under the project's `.agents/skills`, and needs no further setting. omp resolves the two sets by name (`src/extensibility/skills.ts:120-139`; upstream `docs/skills.md`, "Collision and duplicate handling"):

- Different names coexist. This is the normal case: pstack names are `principle-*`, `correct`, `sharpen`, `unslop` and so on; a seat skill carries the seat's name.
- The same name with identical content is loaded once.
- The same name with different content keeps the bare name for the higher-precedence copy (a custom-directory skill outranks a provider skill; otherwise the first admitted) and namespaces the other as `<namespace>/<name>` with a warning in the listing. Rename the seat skill rather than rely on that.
- A seat skill the model should pick up on its own must not set `disable-model-invocation: true`; the pstack skills set it and are invoked by name, which is how poteto-mode addresses them.
