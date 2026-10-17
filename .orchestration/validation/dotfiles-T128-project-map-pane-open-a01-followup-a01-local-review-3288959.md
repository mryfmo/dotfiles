---
task: dotfiles-T128-project-map-pane-open-a01-followup-a01
head: 32889597f7e98018f3a744173733000d7af8ac3f
pr: 379
base: 35ab0e95a7fe27c501db3478d4f37e69a514d532
started: 2026-10-17T10:55:38Z
finished: 2026-10-17T10:59:47Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Check the map suffix before resolving its symlinks — home/dot_claude/hooks/executable_project-map-reload.sh:39-40
- [P2] Compare map identity on case-insensitive filesystems — home/dot_claude/hooks/executable_project-map-reload.sh:55-56

```text
Path normalization introduces regressions for symlinked map locations and case-only aliases on macOS. Static checks passed, but full unit tests and live-browser behavior were not exercised in the read-only sandbox.

Full review comments:

- [P2] Check the map suffix before resolving its symlinks — home/dot_claude/hooks/executable_project-map-reload.sh:39-40
  If `.project-map` links to a shared output directory, or `index.html` links to a differently named file, `realpath()` removes the expected suffix and this guard exits before listing the browser. These map paths passed the previous event-path check, so both initial pane opening and subsequent reloads now stop. Detect map events independently of the physical-path normalization used for tab matching, and add a symlinked-map regression test.

- [P2] Compare map identity on case-insensitive filesystems — home/dot_claude/hooks/executable_project-map-reload.sh:55-56
  On case-insensitive macOS filesystems, paths containing `Workspace` and `workspace` can identify the same map, but `os.path.realpath()` preserves their different capitalization. This string comparison therefore rejects an already-open map and opens another right split on every write through the alternate spelling. Compare filesystem identity for existing maps, such as with `os.path.samefile()`, and cover a case-only path alias.
Path normalization introduces regressions for symlinked map locations and case-only aliases on macOS. Static checks passed, but full unit tests and live-browser behavior were not exercised in the read-only sandbox.

Full review comments:

- [P2] Check the map suffix before resolving its symlinks — home/dot_claude/hooks/executable_project-map-reload.sh:39-40
  If `.project-map` links to a shared output directory, or `index.html` links to a differently named file, `realpath()` removes the expected suffix and this guard exits before listing the browser. These map paths passed the previous event-path check, so both initial pane opening and subsequent reloads now stop. Detect map events independently of the physical-path normalization used for tab matching, and add a symlinked-map regression test.

- [P2] Compare map identity on case-insensitive filesystems — home/dot_claude/hooks/executable_project-map-reload.sh:55-56
  On case-insensitive macOS filesystems, paths containing `Workspace` and `workspace` can identify the same map, but `os.path.realpath()` preserves their different capitalization. This string comparison therefore rejects an already-open map and opens another right split on every write through the alternate spelling. Compare filesystem identity for existing maps, such as with `os.path.samefile()`, and cover a case-only path alias.
```
