---
task: dotfiles-T133-pre-send-check-a01
head: d0679105dd1c4a498b785ce11f302b1d7b5d6192
pr: 442
base: 230b36767eec123f90dcd79edca76993d9bb9de7
started: 2026-10-20T09:57:58Z
finished: 2026-10-20T10:02:46Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Redact consistency-check diagnostics before printing them — scripts/orchestrator/pre-send.sh:35-36
- [P2] Check tilde and EOF-terminated shell fences — scripts/orchestrator/pre-send.sh:59-61
- [P2] Parse the owner task ID as YAML — scripts/orchestrator/pre-send.sh:72-73

```text
The preflight can expose secrets through diagnostics and skip required syntax and owner checks. Targeted in-memory reproductions confirmed these issues; full tests were not run in the read-only sandbox.

Full review comments:

- [P1] Redact consistency-check diagnostics before printing them — scripts/orchestrator/pre-send.sh:35-36
  When malformed YAML contains a secret, PyYAML's error includes the offending source line. This forwards that traceback to stdout with only whitespace changed, exposing the secret despite the later line-number-only secret diagnostic. Captured validation evidence can consequently retain credentials. Redact or suppress task-derived checker output before printing it; secret exposure is covered by [AGENTS.md:72](AGENTS.md#L72).

- [P2] Check tilde and EOF-terminated shell fences — scripts/orchestrator/pre-send.sh:59-61
  Shell blocks using `~~~bash` fences, or backtick fences left open at EOF, produce no matches here. Both are valid Markdown code blocks, so a task containing an invalid `if then` body in either form passes without a `bash-syntax` refusal. Recognize these fence forms and check their contents rather than treating an empty match list as success.

- [P2] Parse the owner task ID as YAML — scripts/orchestrator/pre-send.sh:72-73
  For valid front matter such as `task_id: dotfiles-T999-fixture-a01 # owner`, the consistency checker correctly reads the ID, but this extraction produces `dotfiles-T999-fixture-a01#owner`. The following grep therefore misses references to the actual owner heading and skips owner validation entirely, allowing a missing acceptance record or empty owner section to pass. Use the parsed YAML value instead of stripping characters from the source line.
The preflight can expose secrets through diagnostics and skip required syntax and owner checks. Targeted in-memory reproductions confirmed these issues; full tests were not run in the read-only sandbox.

Full review comments:

- [P1] Redact consistency-check diagnostics before printing them — scripts/orchestrator/pre-send.sh:35-36
  When malformed YAML contains a secret, PyYAML's error includes the offending source line. This forwards that traceback to stdout with only whitespace changed, exposing the secret despite the later line-number-only secret diagnostic. Captured validation evidence can consequently retain credentials. Redact or suppress task-derived checker output before printing it; secret exposure is covered by [AGENTS.md:72](AGENTS.md#L72).

- [P2] Check tilde and EOF-terminated shell fences — scripts/orchestrator/pre-send.sh:59-61
  Shell blocks using `~~~bash` fences, or backtick fences left open at EOF, produce no matches here. Both are valid Markdown code blocks, so a task containing an invalid `if then` body in either form passes without a `bash-syntax` refusal. Recognize these fence forms and check their contents rather than treating an empty match list as success.

- [P2] Parse the owner task ID as YAML — scripts/orchestrator/pre-send.sh:72-73
  For valid front matter such as `task_id: dotfiles-T999-fixture-a01 # owner`, the consistency checker correctly reads the ID, but this extraction produces `dotfiles-T999-fixture-a01#owner`. The following grep therefore misses references to the actual owner heading and skips owner validation entirely, allowing a missing acceptance record or empty owner section to pass. Use the parsed YAML value instead of stripping characters from the source line.
```
