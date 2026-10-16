---
task: dotfiles-T128-chain-review-scripts-followup-a01
head: ba451c66ce0ba3f1cb5caeed42a07f2aaec1c525
pr: 364
base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
started: 2026-10-16T03:32:01Z
finished: 2026-10-16T03:33:08Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve env -S quoting when splitting arguments — scripts/orchestrator/local-review.sh:94-98

```text
The new interpreter pinning works for simple `env -S` shebangs, but changes the semantics of valid shebangs whose arguments use quoting or escapes. This can prevent the configured review binary from running.

Review comment:

- [P2] Preserve env -S quoting when splitting arguments — scripts/orchestrator/local-review.sh:94-98
  For an `env -S` shebang containing quoted or escaped whitespace, such as `#!/usr/bin/env -S node --require='foo bar'`, `read -a` splits on whitespace without applying `env -S` quoting rules. The interpreter therefore receives multiple arguments containing literal quote characters instead of the single argument produced by `env -S`, so valid review launchers fail or run with different options. Parse the split string with `env`-compatible semantics rather than shell `read` word splitting.
The new interpreter pinning works for simple `env -S` shebangs, but changes the semantics of valid shebangs whose arguments use quoting or escapes. This can prevent the configured review binary from running.

Review comment:

- [P2] Preserve env -S quoting when splitting arguments — scripts/orchestrator/local-review.sh:94-98
  For an `env -S` shebang containing quoted or escaped whitespace, such as `#!/usr/bin/env -S node --require='foo bar'`, `read -a` splits on whitespace without applying `env -S` quoting rules. The interpreter therefore receives multiple arguments containing literal quote characters instead of the single argument produced by `env -S`, so valid review launchers fail or run with different options. Parse the split string with `env`-compatible semantics rather than shell `read` word splitting.
```
