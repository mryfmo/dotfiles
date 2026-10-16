---
task: dotfiles-T128-chain-review-scripts-followup-a01
head: 2e3ff4940d81ea348faf0c12a4eb6a9d4e75b2ef
pr: 364
base: 907522c2ac89c2096a91e70d9effb512886df681
started: 2026-10-15T07:09:24Z
finished: 2026-10-15T07:10:34Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Preserve env -S quoting when splitting shebang arguments — scripts/orchestrator/local-review.sh:94-98

```text
The main fixes are sound, but the newly added env-shebang handling changes valid quoted or escaped `env -S` arguments and can prevent the review binary from running correctly.

Review comment:

- [P2] Preserve env -S quoting when splitting shebang arguments — scripts/orchestrator/local-review.sh:94-98
  For launchers whose `env -S` shebang contains quoted or escaped arguments, `read -a` performs whitespace splitting without the quote/escape semantics required by `env -S`. For example, `#!/usr/bin/env -S node --require 'foo bar'` becomes separate arguments `"'foo"` and `"bar'"`, so the pinned launcher fails or runs with different options. Use an `env -S`-compatible parser rather than Bash word splitting.
The main fixes are sound, but the newly added env-shebang handling changes valid quoted or escaped `env -S` arguments and can prevent the review binary from running correctly.

Review comment:

- [P2] Preserve env -S quoting when splitting shebang arguments — scripts/orchestrator/local-review.sh:94-98
  For launchers whose `env -S` shebang contains quoted or escaped arguments, `read -a` performs whitespace splitting without the quote/escape semantics required by `env -S`. For example, `#!/usr/bin/env -S node --require 'foo bar'` becomes separate arguments `"'foo"` and `"bar'"`, so the pinned launcher fails or runs with different options. Use an `env -S`-compatible parser rather than Bash word splitting.
```
