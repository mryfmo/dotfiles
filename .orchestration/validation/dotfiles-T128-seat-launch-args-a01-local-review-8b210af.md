---
task: dotfiles-T128-seat-launch-args-a01
head: 8b210af3b9f151cef63776f63a74904115cef8b9
pr: 383
base: af4f1e997f78119d5994d7d7b1966894d62bbc6a
started: 2026-10-17T06:41:01Z
finished: 2026-10-17T06:45:20Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Request untruncated command lines from ps — scripts/orchestrator/seat-args.sh:57-57

```text
The new probe can misclassify correctly launched workers when Linux ps output is width-limited. ShellCheck and syntax checks passed; runtime tests were blocked by the read-only sandbox.

Review comment:

- [P2] Request untruncated command lines from ps — scripts/orchestrator/seat-args.sh:57-57
  On Linux with an exported `COLUMNS=80`, procps `ps` truncates command lines to that width even when stdout is captured. A normal Claude worker launch exceeds 80 characters before its complete `-n <team>-<identity>` value, so the selector reports a correctly launched worker as `args=unlaunched`. Request unlimited width with `-ww` and add coverage for width-limited output; the current stubs always supply complete command lines.
The new probe can misclassify correctly launched workers when Linux ps output is width-limited. ShellCheck and syntax checks passed; runtime tests were blocked by the read-only sandbox.

Review comment:

- [P2] Request untruncated command lines from ps — scripts/orchestrator/seat-args.sh:57-57
  On Linux with an exported `COLUMNS=80`, procps `ps` truncates command lines to that width even when stdout is captured. A normal Claude worker launch exceeds 80 characters before its complete `-n <team>-<identity>` value, so the selector reports a correctly launched worker as `args=unlaunched`. Request unlimited width with `-ww` and add coverage for width-limited output; the current stubs always supply complete command lines.
```
