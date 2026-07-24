# T16 sandbox record

- Execution environment: Codex workspace-write sandbox rooted at
  `/Users/mryfmo/Workspace/dotfiles`.
- OpenSandbox: not available or required; the repository sandbox plus fake
  Herdr CLI unit harness isolated all mutating behavior.
- Live Herdr access was read-only: `pane list`, `pane layout`, `pane edges`
  (permission-denied), and CLI usage inspection.
- No live `pane swap`, `pane resize`, `pane split`, `pane run`, or `pane rename`
  command was executed.
- Test mutations occurred only in temporary fake CLI directories created by
  `tests/unit/test_herdr_agents.py`.
