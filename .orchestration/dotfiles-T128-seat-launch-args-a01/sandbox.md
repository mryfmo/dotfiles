---
task_id: dotfiles-T128-seat-launch-args-a01
status: final
revise_round: 5
result_round: 2
---

All revision commands run in the managed workspace-write sandbox without escalation, permission-gated commands or persistent Git configuration changes. Main task/acceptance/audit inputs are read only. Source/test writes stay in the allowed seat script and two test modules; production boundary remains unchanged. Other task branches and untracked evidence are preserved.

uv uses UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache. Tests execute the seat checker with temporary HOME/profile and synthetic ps/lsof data. Fixture parent PIDs come from Python os.getpid or shell PPID passed by an exec shim; no real ps/lsof query is used. The boundary integration test keeps the real copied checker bytes, existing assertions and original boundary invocation. Its initial outer-PID fixture failure is preserved, not hidden.

Fresh read-only security-profile review is the explicit AGENTS.md fallback for missing Crit data. No Crit server/web, human review request, Plan Mode, local Bats, real prompt/secret input, runtime/re-seat change, graph update, AutoSkill or memory promotion. Commit uses a per-command signing override; push uses per-command HTTPS identity rewrite without shared git config writes or -u. Nonfatal packed-refs/credential-store warnings are recorded if emitted. Authorized live writes are branch push and bounded Bot review request; worker never replies/resolves findings or integrates/merges.
