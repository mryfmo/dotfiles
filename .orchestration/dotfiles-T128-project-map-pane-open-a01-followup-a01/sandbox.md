---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: final
---

All revision commands run in the managed workspace-write sandbox without escalation, permission-gated commands or persistent configuration changes. The main checkout and task/acceptance/audit inputs are read only. Edits stay in the allowed hook, existing tests and this task directory. Other task branches and untracked logs are preserved.

uv uses UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache. Tests use temporary symlinks and stub terminal-browser/agent executables with real Bash/jq; no real browser, pane, daemon or process inventory. Independent read-only review is the explicit AGENTS.md fallback for missing Crit data; no Crit server/browser or human review request. No local Bats.

The branch was fetched/fast-forwarded to990b607 before edits. Git commits use a per-command signing override because the configured signing key is unavailable; push uses the known per-command HTTPS identity rewrite, no shared git config edit. Nonfatal packed-refs/credential-store warnings are recorded if emitted. GitHub actions are limited to this PR's authorized push and bounded Bot re-review. Orchestrator owns integration/merge.
