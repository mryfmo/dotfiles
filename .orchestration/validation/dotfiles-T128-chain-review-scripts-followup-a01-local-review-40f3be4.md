---
task: dotfiles-T128-chain-review-scripts-followup-a01
head: 40f3be41e3884cbf6aa2f9c89693676f032b3c89
pr: 364
base: 4775f56a9e0a5fbf695d7be04589c045b063642e
started: 2026-10-16T05:17:48Z
finished: 2026-10-16T05:18:42Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve `env -S` quoting when parsing the shebang — scripts/orchestrator/local-review.sh:94-98

```text
The new interpreter-pinning path changes the semantics of valid `env -S` shebang arguments containing quoting or escaping. Other reviewed changes appear consistent, but this can prevent the configured review binary from running correctly.

Review comment:

- [P2] Preserve `env -S` quoting when parsing the shebang — scripts/orchestrator/local-review.sh:94-98
  When the resolved review binary uses a valid `env -S` shebang containing quoted or escaped arguments (for example, `#!/usr/bin/env -S node --require "module path"`), `read -a` performs whitespace splitting without implementing `env -S` quote/escape rules and leaves quotes embedded in separate arguments. The pinned interpreter then receives different arguments from those the shebang specifies, potentially causing the local review to fail or run with incorrect options; parse according to `env -S` semantics or reject unsupported forms explicitly.
The new interpreter-pinning path changes the semantics of valid `env -S` shebang arguments containing quoting or escaping. Other reviewed changes appear consistent, but this can prevent the configured review binary from running correctly.

Review comment:

- [P2] Preserve `env -S` quoting when parsing the shebang — scripts/orchestrator/local-review.sh:94-98
  When the resolved review binary uses a valid `env -S` shebang containing quoted or escaped arguments (for example, `#!/usr/bin/env -S node --require "module path"`), `read -a` performs whitespace splitting without implementing `env -S` quote/escape rules and leaves quotes embedded in separate arguments. The pinned interpreter then receives different arguments from those the shebang specifies, potentially causing the local review to fail or run with incorrect options; parse according to `env -S` semantics or reject unsupported forms explicitly.
```
