# omp skills: the pstack skills inside every seat

omp 18.11.3 (`@oh-my-pi/pi-coding-agent`, installed under `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent`; paths below are relative to it) loads the skills under `~/.agents/skills` into every seat. This page names the setting that pins that, where the skills come from, how to prove what a seat loads, and how a seat's own skill coexists with the pstack set. Facts marked "measured" come from the U10 dry run of 2026-10-23 under a scratch `HOME`.

## The key

`skills.customDirectories` in `~/.omp/agent/config.yml`.

- omp registers it at `src/extensibility/settings.ts:65-69` (type `array`, default empty) and reads it in `loadSkills` at `src/extensibility/skills.ts:471-480`: each entry goes through `expandTilde`, is scanned one level deep for `*/SKILL.md`, and is admitted under the provider id `custom` at level `user` with `requireDescription: true`.
- The manifest `home/dot_agents/agent-config.yaml` holds the list as `omp.skills_directories` (default `~/.agents/skills`, the same root as `skills.canonical_dir`). `scripts/generate-agent-configs.py` validates it (`~/` or absolute, no shell characters) and renders `home/.chezmoitemplates/omp-config-managed.yml`; `make render-check` fails when the template is stale.
- `home/dot_omp/private_agent/modify_private_config.yml` merges `modelRoles.default` and `skills.customDirectories` into the live file and keeps every other key omp wrote. It writes the directories with `~` expanded to `$HOME`, because `omp skill list` resolves a non-absolute entry against the inspected directory before omp expands `~` (`src/cli/skill-list.ts:58-64`); measured, `~/.agents/skills` lists nothing through that command while the absolute path lists the skills. A second apply is a no-op (`tests/unit/test_omp_config_merge.py`).

## The directory

`~/.agents/skills` (manifest `skills.canonical_dir`). omp scans it on two routes:

- The `agents` provider (`src/discovery/agents.ts:30` and `:124-127`, loader `:158-174`) scans `~/.agent/skills` and `~/.agents/skills` at the user level and `.agent/skills` and `.agents/skills` on the walk up from the project. Its user level is on by default: `skills.enableAgentsUser` defaults to `true` (`src/extensibility/settings.ts:57`, gate at `src/extensibility/skills.ts:322`), and `.agents` is not a foreign provider, so `enabledProviders` does not apply to it (`src/capability/index.ts:363-373`; upstream `docs/skills.md`, "Source toggles and filtering"). The earlier task text that named `enabledProviders` as the switch described the foreign providers (`~/.claude`, `~/.codex`, `~/.cursor`), not `.agents`.
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

The pstack skills are the pinned sparse clone of `cursor/plugins`, path `pstack/`, that `scripts/update-agent-assets.sh#update_pstack` checks out under `~/.local/share/pstack/repo` and links into `~/.agents/skills/<name>` (plan 023 item G, task T129). The pin is `assets.pstack.pin` in `home/dot_agents/agent-config.yaml` when that entry exists; the links are recorded in `~/.local/state/pstack/skills.links`. On `main` at 34e216e9 neither the manifest entry, the clone nor the receipt exists yet, so the dry run linked two skills from the Claude Code plugin cache `~/.claude/plugins/cache/cursor-plugins/pstack/0.15.30/skills/` (`plugin.json` version 0.15.30). Once T129 lands, the same `skill list` run names every linked skill without a config change: the key names the directory, not the skills.

## A seat's skill beside the pstack skills

A seat's own skill (the planned `hcom-worker`, for example) is one more `<name>/SKILL.md` under the same `~/.agents/skills` root, or under the project's `.agents/skills`, and needs no further setting. omp resolves the two sets by name (`src/extensibility/skills.ts:120-139`; upstream `docs/skills.md`, "Collision and duplicate handling"):

- Different names coexist. This is the normal case: pstack names are `principle-*`, `correct`, `sharpen`, `unslop` and so on; a seat skill carries the seat's name.
- The same name with identical content is loaded once.
- The same name with different content keeps the bare name for the higher-precedence copy (a custom-directory skill outranks a provider skill; otherwise the first admitted) and namespaces the other as `<namespace>/<name>` with a warning in the listing. Rename the seat skill rather than rely on that.
- A seat skill the model should pick up on its own must not set `disable-model-invocation: true`; the pstack skills set it and are invoked by name, which is how poteto-mode addresses them.
