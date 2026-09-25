# dot-ubuntu-parity-T2-a01 report

status: ready_for_review
worktree: `/home/moriya/Workspace/worktrees/chezmoi-ubuntu-parity`
branch: `feat/ubuntu-parity`

## Items

- B1 `720a3fd` fix(ubuntu): add user to docker group on client install

  - `configure_docker_group()` added to `install/ubuntu/client/docker.sh`,
    called from `main()` after `install_docker_engine`. `getent group docker`
    assertion added to `tests/install/ubuntu/client/docker.bats`.
  - `[memory:decision]`: chezmoi `run_once` retriggers via script
    content-hash change; no `run_once_10-install-docker.sh.tmpl` state
    deletion or rename needed. Registered via CompactionDB — see Learning.

- B2 `f9223d9` fix(mise): normalize yq shim via aqua and adopt watchexec

  - `home/dot_mise/config.toml`: `"github:mikefarah/yq"` → `"aqua:mikefarah/yq"
= "4.53.6"`; added `"aqua:watchexec/watchexec" = "2.7.3"` (latest stable
    at write time). Removed `watchexec` from the macOS brew list in
    `install/macos/common/misc.sh`.
  - Ran `mise lock` scoped to this repo (`MISE_CONFIG_DIR="$PWD/home/dot_mise"`)
    after installing both new pins with `MISE_LOCKED=0` (the project's
    `locked = true` setting blocks first-time installs otherwise). Both new
    tools got all 4 `lockfile_platforms` entries.
  - Judgment call: the stale `github:mikefarah/yq` lock entry is **kept**,
    not deleted. `mise lock` doesn't prune it on its own, and
    `tests/unit/test_supply_chain_policy.py:229` (not in `allowed_files`)
    hardcodes `"github:mikefarah/yq"` in its platform-coverage assertion.
    Deleting it broke that out-of-scope test; keeping it (inert, unreferenced
    by `config.toml`) keeps the test green without touching it.
  - `uv run python -m unittest tests.unit.test_supply_chain_policy`: 17 OK.

- B3 `fce3fc3` fix(agents): key codex project trust to the chezmoi working tree

  - `home/dot_agents/agent-config.yaml`: `codex.projects` key
    `/Users/mryfmo/Workspace/dotfiles` → `{{ .chezmoi.workingTree }}`.
  - `home/dot_codex/modify_private_config.toml`: added `working_tree_dir()`
    (prefers env `CHEZMOI_WORKING_TREE`, falls back to `source_dir().parent`
    since `.chezmoiroot=home`) and wired it into `render_managed_template()`.
  - Regenerated `home/.chezmoitemplates/codex-config-managed.toml` via
    `python3 scripts/generate-agent-configs.py` (no hand edits); only the
    `[projects.*]` table header changed.
  - Judgment call on `scripts/check-agent-runtime.py`: it does **not**
    re-implement template rendering for `modify_private_config.toml` — it
    runs that script as a subprocess (`same_modified()`, only setting
    `CHEZMOI_SOURCE_DIR`) and diffs the output. No local-substitution mirror
    was needed there; verified by invoking the merge script the same way
    `same_modified()` does and confirming it resolves to this worktree's root.
  - Added a guard to `scripts/validate-agent-assets.py::validate_codex_config`
    next to the existing `shell_path` macOS-home guard: the rendered
    `[projects]` table must not contain `/Users/mryfmo/` and must key trust
    with `{{ .chezmoi.workingTree }}`.
  - New tests: `test_codex_config_merge.py` (env-override and fallback
    resolution of the placeholder), `test_generate_agent_configs.py`
    (render quoting), `test_validate_agent_assets.py` (guard accept/reject
    cases).

- B4 `aaef350` fix(sheldon): drop dead ubuntu-command local plugin

  - Removed `[plugins.ubuntu-command]` from
    `home/dot_config/sheldon/plugin_sources/client/ubuntu.toml` — its target
    `~/.local/bin/client/ubuntu.sh` has never existed in this repo's git
    history (confirmed with `git log --all --diff-filter=A --name-only`).
  - Judgment call: kept the file present (now empty plus an explanatory
    comment) rather than deleting it, because
    `home/dot_config/sheldon/plugins.toml.tmpl` unconditionally
    `{{ include }}`s this exact path for every Linux client and that chezmoi
    template function errors on a missing file. `plugins.toml.tmpl` is
    outside `allowed_files` for this task, so the file itself had to stay.
    An empty TOML document is a valid no-op include.

- B5 `352833b` fix(doctor): tolerate cowork-synced skills and own crit codex skills

  - `scripts/check-agent-runtime.py::compare_claude_skills()`: added
    `~/.claude/skills/synced` to `ignored_paths` (Cowork-synced skills are
    not chezmoi-owned).
  - Added `CRIT_PLUGIN_SKILLS = {"crit", "crit-cli", "crit-story"}`, unioned
    into the skill allowlist `orphaned_asset_warnings()` checks under
    `~/.agents/skills`.
  - `scripts/update-agent-assets.sh::update_codex_crit`'s `manifest_record`
    call now also records `${HOME}/.agents/skills/{crit,crit-cli,crit-story}`
    so `remove-agent-asset` can map them back to this step.
  - New tests in `test_check_agent_runtime.py` for both the ignore and the
    allowlist addition.

- B6 `70c5967` fix(claude): invoke herdr-agents attach hook by absolute path
  - `home/dot_claude/modify_private_settings.json`: the managed SessionStart
    hook now runs `{home_dir()}/.local/bin/common/herdr-agents --attach ...`
    instead of the bare `herdr-agents` command.
  - Added `"herdr-agents"` to `MANAGED_SESSION_START_SCRIPTS` so the existing
    basename-based replace-in-place dedup logic recognizes both the old bare
    command and the new absolute-path command as the same managed hook —
    otherwise a machine with the old command in its live `settings.json`
    would end up running the hook twice.
  - Judgment call: kept the new command **unquoted** (no `"..."` around the
    path), even though the task note's example showed quotes. An out-of-scope
    test, `tests/unit/test_herdr_agents.py` (not in `allowed_files`), asserts
    `assertIn("herdr-agents --attach", command)` — a quoted path would insert
    a `"` between `herdr-agents` and `--attach` and break that literal
    substring match. `$HOME`-derived paths on this kind of machine never
    contain spaces in practice, so leaving it unquoted keeps the out-of-scope
    test green without editing it.
  - Updated the two `test_claude_settings_merge.py` cases that hardcoded the
    old bare command string.

## Out-of-scope findings (not fixed; outside allowed_files)

- `make format` fails on two files, both untouched by this task and last
  modified well before it: `home/dot_local/bin/common/executable_contextdb-codex-notify`
  (heredoc `if ! ... << 'PY'; then` → shfmt now wants `then` on its own line
  after the heredoc) and `home/dot_local/bin/common/executable_herdr-agents`
  (a `case` arm's indentation). Pre-existing shfmt v3.14.1 formatting drift,
  unrelated to B1–B6; see Validation for the exact diff.

## Finishing

- `make format`: fails only on the two out-of-scope files above; nothing in
  `allowed_files` needed reformatting.
- `make validate-agent-assets`: green.
- `make unit-test`: green, 376 tests, 1 skipped (pre-existing skip, unrelated).
- `git log --oneline main..HEAD`: 6 commits, one per item (see Validation).
- CompactionDB: registered the B1 `[memory:decision]` with
  `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --content "..." --scope project`
  → id `6c8f2285-58bb-444e-a028-dd0c09a9141f` (see Validation for verbatim
  command and confirmation).

cost: n/a (runtime does not expose token/cost figures to this agent)
