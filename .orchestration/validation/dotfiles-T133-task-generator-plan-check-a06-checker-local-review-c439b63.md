---
task: dotfiles-T133-task-generator-plan-check-a06-checker
head: c439b63c65285ec8180dc3e21394c87ef21115b4
pr: 440
base: e00de4e0e4158de19e2c8921e572461e7e9e4ca0
started: 2026-10-21T07:28:37Z
finished: 2026-10-21T07:40:21Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83

```text
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
Read-only reproductions confirmed a baseline-search crash, a case-aliased path crash, and an incorrectly accepted failed probe. The full unit suite and CI were not rerun.

Full review comments:

- [P1] Handle non-UTF-8 files in canonical baseline searches — scripts/orchestrator/task-consistency-check.py:225-225
  When C8 checks a new `*_EVIDENCE` name absent from Makefile and scripts, traversal reaches the existing encrypted `home/.key.txt.age`. This strict decode raises `UnicodeDecodeError`, aborting the checker even when the input has its required threat row. Handle binary canonical blobs without crashing so valid tasks can pass and uncovered inputs receive a C8 finding.

- [P2] Relativize case-aliased targets using filesystem identity — scripts/orchestrator/task-consistency-check.py:83-83
  On case-insensitive filesystems, an in-repository file symlink can resolve through a differently cased checkout root. `confined()` accepts that target via `samefile()`, but C12 subsequently passes it into `path_entry()`, where this case-sensitive `relative_to(root)` raises `ValueError`. Valid tasks consequently receive no verdict. Preserve identity-aware relativization and extend the closed case-alias fixture ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Preserve grep's failure status when no lines match — scripts/orchestrator/task-consistency-check.py:310-312
  With an authorized `--premises-sha`, a `grep -c` premise expecting `0` passes C14 when its pattern matches nothing because this branch always returns status 0. Actual grep returns status 1 for no matches, contradicting the new requirement to reject unsuccessful probes even when stdout matches. Return a nonzero status for zero matches and add that negative control.
```
