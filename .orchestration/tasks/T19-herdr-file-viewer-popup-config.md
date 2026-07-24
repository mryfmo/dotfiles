# Orchestration task: T19 prefix+f file-viewer popup binding + micro editor config

## Assignment

- Task ID: `T19-herdr-file-viewer-popup-config`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- Continue on branch `feat/herdr-file-viewer-popup` in the T18 worktree
  (path reported in the T18 result; orchestrator confirms in the AGMSG-TASK
  message). Do NOT touch the main worktree except the `.orchestration/`
  artifact paths.

## Facts verified by the orchestrator (do not re-derive)

- herdr 0.7.4 is installed and its `--default-config` documents the popup
  binding: `type = "popup"` opens a session-modal terminal without changing
  the tab layout; `width`/`height` accept cells or percentages like "80%".
- The plugin is installed: `herdr plugin list --json` reports
  `plugin_id == "herdr-file-viewer"` and the built binary exists at
  `<plugin_root>/target/release/herdr-file-viewer`.
- `herdr plugin config-dir herdr-file-viewer` →
  `~/.config/herdr/plugins/config/herdr-file-viewer`. The plugin reads its
  `config.toml` from `$HERDR_PLUGIN_CONFIG_DIR`; the `editor` key wins over
  `$EDITOR`; the opened file path is appended as the final argument.
- `tests/unit/test_herdr_agents.py` already imports `tomllib` and defines
  `HERDR_CONFIG = ROOT / "home/dot_config/herdr/config.toml"`.

## Change 1: `home/dot_config/herdr/config.toml`

Append after the existing `prefix+alt+a` `[[keys.command]]` block, exactly:

```toml
# herdr-file-viewer: prefix+f opens the plugin as a session-modal popup
[[keys.command]]
key = "prefix+f"
type = "popup"
description = "File Viewer"
width = "90%"
height = "90%"
command = '''PLUGIN_DIR="$(herdr plugin list --json | jq -r '.result.plugins[] | select(.plugin_id=="herdr-file-viewer") | .plugin_root')" && CONFIG_DIR="$(herdr plugin config-dir herdr-file-viewer)" && HERDR_PLUGIN_CONFIG_DIR="$CONFIG_DIR" exec "$PLUGIN_DIR/target/release/herdr-file-viewer"'''
```

## Change 2: new file `home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml`

```toml
editor = "micro"
```

## Test requirement (same commit, `tests/unit/test_herdr_agents.py`)

- `test_herdr_prefix_f_opens_file_viewer_popup`: parse `HERDR_CONFIG` with
  `tomllib`, find the `keys.command` entry with `key == "prefix+f"`, assert
  `type == "popup"`, `width == "90%"`, `height == "90%"`, and that the
  command string contains `herdr-file-viewer` and `HERDR_PLUGIN_CONFIG_DIR`.
- `test_file_viewer_plugin_config_sets_micro_editor`: parse the new plugin
  config source file, assert it equals `{"editor": "micro"}`.

## Constraints

- Allowed files: `home/dot_config/herdr/config.toml`,
  `home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml`
  (new), `tests/unit/test_herdr_agents.py`, plus the expected artifact paths
  under `.orchestration/` in the MAIN worktree.
- Forbidden actions: editing any other file (incl. `home/dot_mise/*` — the
  orchestrator grafts the mise diff separately); dependency changes;
  `chezmoi apply`; any live herdr mutation; running `bats` locally;
  `git push`.
- Commit on `feat/herdr-file-viewer-popup` with a Conventional Commit
  message.

## Validation (record full output)

1. `uv run pytest tests/unit/test_herdr_agents.py` (green)
2. `python3 -c "import tomllib,pathlib;
tomllib.loads(pathlib.Path('home/dot_config/herdr/config.toml').read_text());
print('config.toml parses')"` (run from the worktree root)

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T19-herdr-file-viewer-popup-config.md`
- validation: `.orchestration/validation/T19-herdr-file-viewer-popup-config.md`
- sandbox: `.orchestration/sandboxes/T19-herdr-file-viewer-popup-config.md`
- learning: `.orchestration/learning/T19-herdr-file-viewer-popup-config.md`
- autoskill: `.orchestration/autoskill/runs/T19-herdr-file-viewer-popup-config.md`

## Done signal

`AGMSG-RESULT v1` with `task_id=T19-herdr-file-viewer-popup-config`,
`status=ready_for_review|blocked`, and all artifact paths. Max turns: 15.
