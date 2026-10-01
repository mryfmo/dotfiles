# Sandbox: dot-ua-graph-refresh-T51-a01

- worker-c, branch chore/ua-graph-refresh (no commit).
- Run unsandboxed: git fetch/switch, plugin node/python helpers, writes to the main checkout .orchestration.
- Subagents: 12 understand-anything:file-analyzer dispatches, each writing only .ua/intermediate/batch-<i>*.json and .ua/tmp/ (both gitignored).
- Not run: prepare-symbol-retry, finalize-incremental, architecture/tour agents.
