---
task: dotfiles-T133-pre-send-check-a02
head: 1d72f16978018c3d016bbc239d79d3d7d0675105
pr: 442
base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
started: 2026-10-21T06:39:14Z
finished: 2026-10-21T06:46:53Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Exclude fenced examples when counting task Items — scripts/orchestrator/pre-send.sh:91-92
- [P2] Extract checker locations from parser data, not echoed text — scripts/orchestrator/pre-send.sh:43-45
- [P2] Normalize line endings before parsing task structure — scripts/orchestrator/pre-send.sh:34-35

```text
The preflight can silently bypass required checks and still expose input-controlled numeric fragments. These issues were reproduced with read-only probes; Bash syntax passed, but the temporary-file test suite was not run.

Full review comments:

- [P2] Extract checker locations from parser data, not echoed text — scripts/orchestrator/pre-send.sh:43-45
  A multiline YAML `task_id` containing `\n  in "<unicode string>", line 1234567890, column 7\n` is echoed by the checker's C1/C2 diagnostics. This regex treats that input-derived text as a parser location and prints `line(s) 1234567891`, potentially exposing numeric secret fragments. Obtain locations from actual YAML exception marks or omit them. The threat-table claim that free-text digits cannot become locations is not closed by its current regression test ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Normalize line endings before parsing task structure — scripts/orchestrator/pre-send.sh:34-35
  For CRLF input, the checker normalizes newlines through `Path.read_text()`, but this decoding retains carriage returns. The helper therefore fails to separate YAML front matter, silently skipping owner validation. Fence closers also stop matching, allowing a non-shell fence to absorb a later invalid Bash block. Both cases can exit 0 with only a digest. Normalize the parsing text while preserving the original bytes for hashing and newline counting.

- [P2] Exclude fenced examples when counting task Items — scripts/orchestrator/pre-send.sh:91-92
  For a task with one actual Item and an existing but empty owner section, adding a fenced example containing `## Item 2` makes this expression count two Items. The preflight then exits 0 despite there being no owner-work row. Count Markdown headings outside fences, with an appropriate heading boundary, rather than matching raw line prefixes.
The preflight can silently bypass required checks and still expose input-controlled numeric fragments. These issues were reproduced with read-only probes; Bash syntax passed, but the temporary-file test suite was not run.

Full review comments:

- [P2] Extract checker locations from parser data, not echoed text — scripts/orchestrator/pre-send.sh:43-45
  A multiline YAML `task_id` containing `\n  in "<unicode string>", line 1234567890, column 7\n` is echoed by the checker's C1/C2 diagnostics. This regex treats that input-derived text as a parser location and prints `line(s) 1234567891`, potentially exposing numeric secret fragments. Obtain locations from actual YAML exception marks or omit them. The threat-table claim that free-text digits cannot become locations is not closed by its current regression test ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Normalize line endings before parsing task structure — scripts/orchestrator/pre-send.sh:34-35
  For CRLF input, the checker normalizes newlines through `Path.read_text()`, but this decoding retains carriage returns. The helper therefore fails to separate YAML front matter, silently skipping owner validation. Fence closers also stop matching, allowing a non-shell fence to absorb a later invalid Bash block. Both cases can exit 0 with only a digest. Normalize the parsing text while preserving the original bytes for hashing and newline counting.

- [P2] Exclude fenced examples when counting task Items — scripts/orchestrator/pre-send.sh:91-92
  For a task with one actual Item and an existing but empty owner section, adding a fenced example containing `## Item 2` makes this expression count two Items. The preflight then exits 0 despite there being no owner-work row. Count Markdown headings outside fences, with an appropriate heading boundary, rather than matching raw line prefixes.
```
