---
task: dotfiles-T128-chain-glue-finish-a01
head: f20826e2ee67e9006ef4d4d2dd32462b9639193b
pr: 378
base: af4f1e997f78119d5994d7d7b1966894d62bbc6a
started: 2026-10-17T07:26:40Z
finished: 2026-10-17T07:30:48Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Bind the input sweep to the audited head before resolving threads — scripts/orchestrator/chain-finish.sh:94-95

```text
The chain can reuse outdated dispositions and repackage them as current-head evidence. Shell syntax and ShellCheck passed; the full test suite was not run in the read-only sandbox.

Review comment:

- [P1] Bind the input sweep to the audited head before resolving threads — scripts/orchestrator/chain-finish.sh:94-95
  If the saved sweep belongs to an earlier head of the same PR, this check passes and `resolve-threads.sh` posts and resolves using outdated dispositions. The subsequent refresh does not correct this: `fill_sweep.py` imports those newly posted replies into the current-head evidence, allowing stale decisions through the gate. Require the sweep's `head_sha` to equal `${head}` before any GitHub writes, preserving the integration-evidence workflow in [AGENTS.md:44](AGENTS.md#L44).
The chain can reuse outdated dispositions and repackage them as current-head evidence. Shell syntax and ShellCheck passed; the full test suite was not run in the read-only sandbox.

Review comment:

- [P1] Bind the input sweep to the audited head before resolving threads — scripts/orchestrator/chain-finish.sh:94-95
  If the saved sweep belongs to an earlier head of the same PR, this check passes and `resolve-threads.sh` posts and resolves using outdated dispositions. The subsequent refresh does not correct this: `fill_sweep.py` imports those newly posted replies into the current-head evidence, allowing stale decisions through the gate. Require the sweep's `head_sha` to equal `${head}` before any GitHub writes, preserving the integration-evidence workflow in [AGENTS.md:44](AGENTS.md#L44).
```
