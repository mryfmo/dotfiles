# Learning

- Candidate (not promoted): in `herdr-agents`, a lookup that keys a pair workspace on the full-mode label `<dir> agents` misses every pair built by attach mode, because attach keeps the workspace's own label. Identify a managed pair by pane evidence (a `claude-orchestrator` pane in DIR, or the registered `<kind>-worker-<ws>` agent) as well as the label.
- Candidate (not promoted): with `worker_kind=claude`, the worker is also a Claude session, so the Claude `SessionStart` hook (`herdr-agents --attach`) runs inside the worker pane. Guards that assume "any Claude pane is the orchestrator" (`has_claude_pane`, the attach rename, the layout-repair lookup) must exclude the registered worker pane.
- Candidate (not promoted): when a new test asserts "no mutation", check it against the old script. The first attach-relabel test passed on the old script only because its empty fake pane list made attach exit early. A realistic two-pane fixture made it fail on the old script as intended.

- Candidate (not promoted): in this environment `gh … --json` output carries ANSI colour codes, because `printenv CLICOLOR_FORCE` prints `1` in agent shells, so a `gh pr checks --json | jq` CI watcher silently parses nothing and emits no events. Both round-1 and round-2 watchers expired silently while checks had finished. Use `gh pr checks <n> --json name,bucket --jq …` (gh's built-in jq) or strip ANSI before jq, and treat a silent watcher expiry as a watcher bug, not "still pending".

[memory:failure] herdr-agents full mode found existing pairs only by the `<dir> agents` label, so attach-built pairs (labeled e.g. `dotfiles`) spawned a duplicate workspace; fixed in T25 by pane-evidence lookup (2026-09-27).
