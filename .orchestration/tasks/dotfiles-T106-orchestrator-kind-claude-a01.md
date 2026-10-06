# AGMSG-TASK dotfiles-T106-orchestrator-kind-claude-a01 (draft; the revert of T105, dispatched after the codex legs are recorded)

Objective: `home/dot_agents/agent-config.yaml` `orchestrator_kind: codex` → `claude`; rendered `model-profiles.env` follows; `make render-check` clean; nothing else. Branch `chore/orchestrator-kind-claude` from `origin/main`; PR; CI; RESULT. After merge: `make update`, then the operator restarts the pair with `herdr-agents <DIR>`. max_turns=8.
