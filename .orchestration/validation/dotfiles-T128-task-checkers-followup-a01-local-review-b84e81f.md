---
task: dotfiles-T128-task-checkers-followup-a01
head: b84e81f0d8f5b073b2728f1489d9317800eb9cf9
pr: 365
base: 595997831afcc05b266c9f245456df54725628db
started: 2026-10-15T05:40:17Z
finished: 2026-10-15T05:41:26Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Isolate imports when running the trusted checker — scripts/orchestrator/orch-audit.sh:55-55

```text
The checker-integrity hardening remains bypassable through Python module shadowing by an untracked sibling file. The checker must run in isolated mode for the claimed trust boundary to hold.

Review comment:

- [P2] Isolate imports when running the trusted checker — scripts/orchestrator/orch-audit.sh:55-55
  When the orchestrator checkout contains an untracked module beside the checker (for example `scripts/orchestrator/json.py`), the tracked/unchanged checks pass, but Python prepends that directory to `sys.path` and executes the untrusted module during the checker’s imports. Run this invocation with `-I` (as the preceding Python command does) so the new trust guarantee actually covers execution; this is required by the trust-boundary validation rule in [AGENTS.md:78](AGENTS.md#L78).
The checker-integrity hardening remains bypassable through Python module shadowing by an untracked sibling file. The checker must run in isolated mode for the claimed trust boundary to hold.

Review comment:

- [P2] Isolate imports when running the trusted checker — scripts/orchestrator/orch-audit.sh:55-55
  When the orchestrator checkout contains an untracked module beside the checker (for example `scripts/orchestrator/json.py`), the tracked/unchanged checks pass, but Python prepends that directory to `sys.path` and executes the untrusted module during the checker’s imports. Run this invocation with `-I` (as the preceding Python command does) so the new trust guarantee actually covers execution; this is required by the trust-boundary validation rule in [AGENTS.md:78](AGENTS.md#L78).
```
