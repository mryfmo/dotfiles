# Isolation

Worker: codex-standard-dot-a006
Worktree: worker-e
Branch: feat/add-worker-credential-notice
Task SHA-256: f4cc65369f181596c751bd569ee74bcab248004ff22fa9615938f3478786c420

Code edits limited to launcher, its unit tests and one README provisioning sentence. No permission/sandbox/hook sources changed; no credential file contents read or printed. Test homes and CLIs are isolated temporary fixtures. Artifacts remain untracked at exact task-relative paths in worker-e for orchestrator copy. UV cache uses /tmp. .agents/worklog is read-only and excluded, so plan/todo are maintained in report. No local bats, make update/apply, thread resolution, gh API or fallback credentials. SSH push explicitly assigned; orchestrator opens PR and checks CI/Bot. No Plan Mode or Crit server started.
