---
task: dotfiles-T128-chain-review-scripts-followup-a01
head: 850fc54ea58ee0952a9762d6cd64bdae2dd2c63e
pr: 364
base: 595997831afcc05b266c9f245456df54725628db
started: 2026-10-15T05:55:54Z
finished: 2026-10-15T05:57:09Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve arguments from `env -S` shebangs — scripts/orchestrator/local-review.sh:91-92

```text
The new interpreter-pinning path changes the execution semantics of supported `env -S` shebangs by discarding their arguments. Other reviewed changes appear consistent, but this can break valid review launchers.

Review comment:

- [P2] Preserve arguments from `env -S` shebangs — scripts/orchestrator/local-review.sh:91-92
  When the resolved review executable uses a shebang such as `#!/usr/bin/env -S node --no-warnings`, this branch captures only `node` and invokes it as `node <script> ...`, silently dropping `--no-warnings` and every other shebang argument. This can change behavior or prevent the reviewer from starting; preserve the tokens following the interpreter when constructing `run`.
The new interpreter-pinning path changes the execution semantics of supported `env -S` shebangs by discarding their arguments. Other reviewed changes appear consistent, but this can break valid review launchers.

Review comment:

- [P2] Preserve arguments from `env -S` shebangs — scripts/orchestrator/local-review.sh:91-92
  When the resolved review executable uses a shebang such as `#!/usr/bin/env -S node --no-warnings`, this branch captures only `node` and invokes it as `node <script> ...`, silently dropping `--no-warnings` and every other shebang argument. This can change behavior or prevent the reviewer from starting; preserve the tokens following the interpreter when constructing `run`.
```
