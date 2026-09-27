# AGMSG-TASK dot-worker-advisor-fable-T26-a01

## Objective

Operator directive (2026-09-27): launching the worker (Opus 5.5 high) MUST also
apply `/advisor fable`. Codify the advisor in the manifest and enforce it:
worker launch args gain `--advisor fable`, the validator hard-requires it on
the worker profile, and docs/tests cover it.

Facts (from official Claude Code docs, v2.1.283): `claude --advisor <alias>`
sets the advisor for that single session (documented though absent from
`--help`); `advisorModel` is a supported settings.json key; opus main + fable
advisor is a valid pairing (advisor must be at least as capable as the main
model). The operator's user settings currently carry a manually-set
`advisorModel: "fable"` — this task moves advisor configuration into the
manifest so it is managed, not manual.

[memory:decision] T26: worker claude launches must include --advisor fable,
sourced from manifest `claude.advisor`; validator pins the worker profile's
advisor to fable; interactive settings render advisorModel from the manifest
(operator 2026-09-27).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then `git switch -c feat/worker-advisor-fable origin/main`.
  (Base must already contain the merged T25 branch; verify `--restart-worker`
  is present in README on your base, else stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. `home/dot_agents/agent-config.yaml`

- `standard.claude` → `{ model: claude-opus-5-5, effort: high, advisor: fable }`.
- `deep.claude` → `{ model: claude-fable-5, effort: high, advisor: fable }`
  (codifies the operator's existing manual `advisorModel` so the interactive
  setting is manifest-managed too; a fable/fable pairing is documented as
  supported).
- No advisor on express/review/security/adh (express is the cheap E2E subject;
  the others stay as-is until the operator says otherwise).

### 2. `scripts/generate-agent-configs.py`

- Accept an optional `advisor` key on the claude side of a profile (extend
  `PROFILE_AGENT_KEYS` / the profile validation so the value must match
  `PROFILE_VALUE_RE`; required keys stay model/effort).
- `render_model_profiles_env()`: append ` --advisor <value>` to
  `MODEL_PROFILE_<P>_CLAUDE_ARGS` when the profile's claude side sets advisor.
- `render_claude_settings()`: emit `"advisorModel": "<value>"` in
  `home/.chezmoitemplates/claude-settings-managed.json` when the interactive
  profile's claude side sets advisor; omit the key entirely when absent.

### 3. `scripts/validate-agent-assets.py`

- After the existing worker_profile membership check: the worker profile's
  `claude.advisor` is REQUIRED and must equal `fable` (operator pin, mirroring
  the security.codex.model pin), with a truthful failure message.
- Profile schema check accepts the optional advisor key elsewhere.

### 4. Docs

- `README.md`: in the worker-profile paragraph, state that the worker profile
  carries `advisor: fable`, rendered into the launch args as
  `--advisor fable`, and that `--restart-worker` is how a running worker picks
  it up.
- `home/dot_config/claude/rules/model-selection.md`: extend the manifest
  bullet: the advisor model also lives only in `model_profiles`
  (`claude.advisor`); never set it with ad-hoc `/advisor` or `--advisor`
  flags outside the rendered args.

### 4b. Part B — `home/dot_local/bin/common/executable_herdr-agents` restart robustness

Two gaps found in the T25 live E2E (see the T25 acceptance addendum):

- **Exit-confirmation dialog**: a claude worker with running background tasks
  (e.g. its inbox monitor) responds to the `/exit` prompt with an
  exit-confirmation dialog ("Exit and stop tasks / Move to background / Stay",
  Enter confirms the default). `restart_worker_in_pane` must handle it:
  after sending `/exit`, wait bounded for the agent to disappear; if it is
  still present, send the submit key once
  (`herdr agent send-keys <pane> Enter`, mirroring the existing trust-dialog
  handling) and wait again before starting the new worker. Keep the fail-safe
  refusal when the pane still never reaches a shell prompt.
- **Legacy label tolerance/repair**: restart mode must work when the worker
  pane still carries the legacy `claude-orchestrator` label left by the
  pre-T25 attach bug. When the registered `<kind>-worker-<ws>` agent resolves
  the pane, relabel it to the designed `<kind>-worker` via
  `herdr pane rename <pane> <kind>-worker` as part of the restart. The
  ambiguity refusal stays for genuinely ambiguous tabs (do not weaken
  `attach_panes_are_unambiguous` beyond excluding the resolved worker pane).
- Update the shdoc/README sentence for `--restart-worker` accordingly (one
  clause each; keep it short).

### 5. Tests

- `tests/unit/test_generate_agent_configs.py`: (a) profile with advisor
  renders `--advisor fable` in its CLAUDE_ARGS; (b) profile without advisor
  renders no `--advisor`; (c) invalid advisor value fails; (d) interactive
  profile advisor renders `advisorModel` in claude settings, absent otherwise.
- `tests/unit/test_validate_agent_assets.py`: worker profile without
  `claude.advisor: fable` fails validation (fixture updated to include it).
- `tests/unit/test_herdr_agents.py`: (a) claude worker start args include
  `--advisor fable` when the env file's `MODEL_PROFILE_<P>_CLAUDE_ARGS`
  carries it (env-file fixture pattern); (b) Part B: restart path sends the
  submit key when the agent survives `/exit` (fake herdr keeps the agent for
  one poll), and still refuses when the pane never reaches a shell; (c)
  Part B: a worker pane resolved via the registered agent but labeled
  `claude-orchestrator` is renamed to `claude-worker` and the restart
  proceeds.
- No local bats (repo policy).

### 6. Regenerate

```
uv run --with pyyaml scripts/generate-agent-configs.py
uv run --with pyyaml scripts/generate-agent-configs.py --check
```

Expected generated diff: `home/dot_agents/model-profiles.env`
(`MODEL_PROFILE_STANDARD_CLAUDE_ARGS="--model claude-opus-5-5 --effort high --advisor fable"`,
`MODEL_PROFILE_DEEP_CLAUDE_ARGS="--model claude-fable-5 --effort high --advisor fable"`)
and `home/.chezmoitemplates/claude-settings-managed.json`
(`"advisorModel": "fable"`). Codex outputs and `express-explorer.md`
unchanged; if anything else changes, stop and report.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents` (Part B only)
- `home/dot_agents/agent-config.yaml`
- `home/dot_agents/model-profiles.env` (generated)
- `home/.chezmoitemplates/claude-settings-managed.json` (generated)
- `scripts/generate-agent-configs.py`
- `scripts/validate-agent-assets.py`
- `README.md`
- `home/dot_config/claude/rules/model-selection.md`
- `tests/unit/test_generate_agent_configs.py`
- `tests/unit/test_validate_agent_assets.py`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-worker-advisor-fable-T26-a01.md` (main checkout)

## Forbidden actions

- Changing worker_kind/worker_profile/interactive_profile, any codex settings,
  express/review/security/adh model or effort values, herdr-agents beyond the
  Part B scope above, permgate,
  hooks configs, dependencies, or `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes outside
  the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
uv run --with pyyaml scripts/generate-agent-configs.py --check
make validate-agent-assets
make unit-test
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green.
2. Artifacts at the exact expected paths, validation with verbatim outputs and
   the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T26: worker claude launches carry --advisor fable from manifest claude.advisor; validator pins worker profile advisor to fable; interactive advisorModel rendered from the manifest (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
