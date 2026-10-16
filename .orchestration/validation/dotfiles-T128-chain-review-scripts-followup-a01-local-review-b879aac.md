---
task: dotfiles-T128-chain-review-scripts-followup-a01
head: b879aac6c47515ccd4c15f157ae48ed5eed29b9b
pr: 364
base: 3b60d6dadc8723ede9e15ab862cfca1aa135f4ab
started: 2026-10-16T04:39:09Z
finished: 2026-10-16T04:39:53Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P1] Validate and quote the owner task ID — scripts/orchestrator/local-advisory.sh:21-21

```text
The new input validation still leaves the owner identifier unchecked and later treats it as both a regular expression and trusted record content. This can misattribute or corrupt gate evidence.

Review comment:

- [P1] Validate and quote the owner task ID — scripts/orchestrator/local-advisory.sh:21-21
  When `$owner` contains regex metacharacters (valid task IDs may contain `.`), this grep can match a different owner heading—for example, `a.b` also matches `aXb`—so advisory rows may be recorded without the required ownership section. Because `$owner` is also written verbatim, newlines can forge acceptance-record entries; validate it like `$task` and use fixed-string matching. This is trust-boundary evidence code, contrary to the validation expectations in `AGENTS.md` under “Orchestration records and trust-boundary code.”
The new input validation still leaves the owner identifier unchecked and later treats it as both a regular expression and trusted record content. This can misattribute or corrupt gate evidence.

Review comment:

- [P1] Validate and quote the owner task ID — scripts/orchestrator/local-advisory.sh:21-21
  When `$owner` contains regex metacharacters (valid task IDs may contain `.`), this grep can match a different owner heading—for example, `a.b` also matches `aXb`—so advisory rows may be recorded without the required ownership section. Because `$owner` is also written verbatim, newlines can forge acceptance-record entries; validate it like `$task` and use fixed-string matching. This is trust-boundary evidence code, contrary to the validation expectations in `AGENTS.md` under “Orchestration records and trust-boundary code.”
```
