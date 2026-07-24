# T19 acceptance: prefix+f file-viewer popup binding + micro editor config

- Task: `.orchestration/tasks/T19-herdr-file-viewer-popup-config.md`
- Result: accepted (first submission)
- Worktree/branch: `/Users/mryfmo/Workspace/dotfiles-t18` / `feat/herdr-file-viewer-popup`
- Commit: `968637c feat: add herdr file viewer popup`

## Adversarial review notes (orchestrator, independent re-verification)

- Diff limited to the three allowed files; the popup `[[keys.command]]` block
  matches the operator-provided binding verbatim (key/type/description/
  width/height/command), placed after the `prefix+alt+a` entry; plugin
  config is exactly `editor = "micro"`.
- Independently re-ran `uv run pytest tests/unit/test_herdr_agents.py`
  (53 passed) and parsed `config.toml` with tomllib, asserting the
  `prefix+f` entry fields directly.
- plugin_id `herdr-file-viewer` and the `<plugin_root>/target/release/`
  binary were pre-verified live by the orchestrator in Phase A3; popup
  width/height percentage syntax verified against `herdr --default-config`
  on 0.7.4 in Phase A4.

## Verdict

- status=accepted; live E2E (popup open, micro editor handoff, fresh
  2-pane workspace, legacy-session tolerance) follows in Phase C before
  merge.
