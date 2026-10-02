# Learning: dot-ua-refresh-policy-T52-a01

1. **Check which flag a hook reads before relying on it.** Both UA 2.9.7 hooks gate on `.ua/config.json` `autoUpdate` (SessionStart: grep for `"autoUpdate".*true`; PostToolUse: `config.autoUpdate === true`), so one flag silences both. Status: validated (read-only gate checks).
2. **Policy follows the tool's real limits.** When a documented cheap path (incremental re-runs) cannot work for a repository, the rule names the limitation and the replacement procedure instead of keeping the generic claim. Status: applied.
