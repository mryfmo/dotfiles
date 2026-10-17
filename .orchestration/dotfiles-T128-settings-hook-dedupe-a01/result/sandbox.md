# Fresh seat sandbox record

All continuation commands ran inside the Codex workspace-write sandbox; no escalation or permission-gated command. The TASK requested outside-sandbox gh, but this seat's approval policy is never and the Worker Playbook requires Codex commands inside its sandbox; in-sandbox gh worked. Shared git config was untouched: push omitted -u and selected the normal HTTPS remote and installed gh credential helper via command-scoped -c options.

Default uv cache initialization failed because the home cache is read-only; the supported UV_CACHE_DIR override selected /tmp/dotfiles-a004-uv-cache. Tests and render-check then passed with PyYAML resolved normally. No policy, dependency manifest, installed settings, hook script or source code was changed during continuation. Herdr agmsg-dispatch now succeeds from this fresh seat. Prior seat network blockers are historical and superseded.

Canonical task read from main checkout because .orchestration/tasks/task was absent locally; its SHA matches committed task.md. All new report/validation/sandbox/learning/autoskill artifacts are untracked under this worktree's same relative task paths; the orchestrator must sync them before integration. Worklogs remain uncommitted under the task directory because .agents is read-only. Plan Mode was not used.
