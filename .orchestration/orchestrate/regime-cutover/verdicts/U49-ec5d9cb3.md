- **P2 · High confidence · [home/dot_agents/agent-config.yaml:34](/tmp/audit/wt-515/home/dot_agents/agent-config.yaml:34)** — Enabling the bridge for ordinary launches exposes its Task failure: a normal subagent clears provider registrations in the shared registry, removing the parent’s provider/API key and breaking subsequent turns; plain sessions lack the seat policies’ Task restriction. Traced through the installed bridge and omp sources; the added documentation also records this failure.

Reproduced:

- Six focused existing unittest cases passed using read-only fixture setup.
- Actual embedded merge preserved unrelated state, replaced managed lists, expanded `~`, remained idempotent, and preserved invalid input.
- Unsafe YAML tags were rejected; the shell wrapper preserved input without `uv`.
- Generator `--check` passed; all five seat overlays matched the base version.

📝 まとめ: U49 audited read-only; one P2 regression found. No files changed.
Not checked: CI, live model calls, full test suites, or actual chezmoi apply.

Verdict: incorrect