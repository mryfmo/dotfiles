---
task: dotfiles-T133-pre-send-check-a01
head: 09e2e95628fb3665e59b1b10b08f2cdac65b2ffb
pr: 442
base: f7f3806749815ba9dfd90e7ff9ee390ca6079014
started: 2026-10-20T13:59:53Z
finished: 2026-10-20T14:06:20Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Suppress checker excerpts that can expose secret fragments — scripts/orchestrator/pre-send.sh:43-46
- [P2] Match secrets across the complete task text — scripts/orchestrator/pre-send.sh:47-49
- [P2] Parse complete Markdown fences before selecting shell blocks — scripts/orchestrator/pre-send.sh:56-58

```text
The preflight can expose credential fragments, miss multiline secrets, and misclassify shell fences. These cases were reproduced with in-memory inputs; the full test suite was not run in the read-only environment.

Full review comments:

- [P1] Suppress checker excerpts that can expose secret fragments — scripts/orchestrator/pre-send.sh:43-46
  When malformed YAML contains a long quoted credential with an invalid escape, PyYAML emits clipped source excerpts. A later excerpt can contain credential fragments without the assignment name or opening quote, so applying `SECRET_PATTERN` to the rendered diagnostic leaves those fragments visible. This was reproduced through the helper. Suppress raw YAML source excerpts and tracebacks rather than relying on regex replacement to sanitize them.

- [P2] Match secrets across the complete task text — scripts/orchestrator/pre-send.sh:47-49
  For an assignment split after `=` or a quoted value containing a newline, the validator's `SECRET_PATTERN` matches the complete text but no individual line matches. Consequently, this preflight exits successfully for content that `validate_no_obvious_secrets()` rejects. Match against the complete text and derive reported line numbers from match offsets.

- [P2] Parse complete Markdown fences before selecting shell blocks — scripts/orchestrator/pre-send.sh:56-58
  The fence matching both skips real shell blocks and checks literal examples: an opener such as ` ```bash title=example` is ignored, allowing `if then` to pass, while a ` ```bash` example inside a larger four-backtick Markdown fence is incorrectly checked and refused. Both cases were reproduced. Track enclosing fences regardless of language, then select shell blocks using the first info-string word.
The preflight can expose credential fragments, miss multiline secrets, and misclassify shell fences. These cases were reproduced with in-memory inputs; the full test suite was not run in the read-only environment.

Full review comments:

- [P1] Suppress checker excerpts that can expose secret fragments — scripts/orchestrator/pre-send.sh:43-46
  When malformed YAML contains a long quoted credential with an invalid escape, PyYAML emits clipped source excerpts. A later excerpt can contain credential fragments without the assignment name or opening quote, so applying `SECRET_PATTERN` to the rendered diagnostic leaves those fragments visible. This was reproduced through the helper. Suppress raw YAML source excerpts and tracebacks rather than relying on regex replacement to sanitize them.

- [P2] Match secrets across the complete task text — scripts/orchestrator/pre-send.sh:47-49
  For an assignment split after `=` or a quoted value containing a newline, the validator's `SECRET_PATTERN` matches the complete text but no individual line matches. Consequently, this preflight exits successfully for content that `validate_no_obvious_secrets()` rejects. Match against the complete text and derive reported line numbers from match offsets.

- [P2] Parse complete Markdown fences before selecting shell blocks — scripts/orchestrator/pre-send.sh:56-58
  The fence matching both skips real shell blocks and checks literal examples: an opener such as ` ```bash title=example` is ignored, allowing `if then` to pass, while a ` ```bash` example inside a larger four-backtick Markdown fence is incorrectly checked and refused. Both cases were reproduced. Track enclosing fences regardless of language, then select shell blocks using the first info-string word.
```
