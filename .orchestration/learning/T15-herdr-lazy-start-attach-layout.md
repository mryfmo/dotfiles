# T15 learning triage

## Validated observations

- A Claude `SessionStart` hook can safely target every Claude launch when attach mode exits before dependency checks unless all three Herdr environment identifiers are present.
- The existing Claude settings modifier is also tested with synthetic baselines that omit hooks. Appending only when the managed baseline already exposes `hooks.SessionStart` preserves that generic merge contract while wiring the real baseline.
- Creating the files split from Claude at ratio `0.8` before starting Codex preserves the previously validated Herdr ordering needed for Claude | Codex | Yazi at 40/40/20.
- Files-pane creation, duplicate detection, Yazi liveness inspection, and in-place restart can be shared between full and attach modes without changing full-mode behavior.
- Repository-wide tests caught a compatibility issue that the focused Herdr suite could not: unconditional settings-hook injection changed byte-identical output expectations for synthetic managed baselines.

## Promotion decision

No project learn file was added because T15's allowed-file boundary excludes `.agents/worklog`. The reusable findings are recorded here for orchestrator review.
