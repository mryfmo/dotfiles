---
task: dotfiles-T128-project-map-pane-open-a01-followup-a01
head: 00048df75bbeb1f85cbce0b9c6fa5fac017b2fee
pr: 379
base: 59db77bbab7fe19377bc2b94adc6ec5c576f3ebb
started: 2026-10-17T13:28:21Z
finished: 2026-10-17T13:32:52Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Compare existing map files by filesystem identity — home/dot_claude/hooks/executable_project-map-reload.sh:55-56

```text
The new comparison misses existing maps accessed through differently cased paths on macOS. Syntax checks passed; temporary-file-based unit tests were not run in the read-only sandbox.

Review comment:

- [P2] Compare existing map files by filesystem identity — home/dot_claude/hooks/executable_project-map-reload.sh:55-56
  On case-insensitive macOS filesystems, a tab opened through `/users/.../workspace/...` can display the same file that Claude reports through `/Users/.../Workspace/...`, but `os.path.realpath()` preserves those case differences. This comparison rejects the existing tab and opens another split on every write instead of reloading it. This is reproducible with an existing map whose two paths satisfy `os.path.samefile()`. Compare filesystem identity for existing paths rather than relying solely on realpath-string equality.
The new comparison misses existing maps accessed through differently cased paths on macOS. Syntax checks passed; temporary-file-based unit tests were not run in the read-only sandbox.

Review comment:

- [P2] Compare existing map files by filesystem identity — home/dot_claude/hooks/executable_project-map-reload.sh:55-56
  On case-insensitive macOS filesystems, a tab opened through `/users/.../workspace/...` can display the same file that Claude reports through `/Users/.../Workspace/...`, but `os.path.realpath()` preserves those case differences. This comparison rejects the existing tab and opens another split on every write instead of reloading it. This is reproducible with an existing map whose two paths satisfy `os.path.samefile()`. Compare filesystem identity for existing paths rather than relying solely on realpath-string equality.
```
