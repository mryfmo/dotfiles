---
task: dotfiles-T128-project-map-reload-hook-a01
head: 2fb97dbfc5bf2d059e557735a4f2b4371df0d24d
pr: 353
base: c15ba668da20dc2956220077cb0f20054ab352c7
started: 2026-10-14T07:10:16Z
finished: 2026-10-14T07:11:14Z
findings: 1
engine: codex review --base main (profile review, read-only)
---

- [P2] Pin the selected tab before reloading — home/dot_claude/hooks/executable_project-map-reload.sh:26-26

```text
The reload hook has a documented tab-close race that can reload the wrong browser tab and potentially lose unsaved state. The patch acknowledges but does not fix this behavior.

Review comment:

- [P2] Pin the selected tab before reloading — home/dot_claude/hooks/executable_project-map-reload.sh:26-26
  If the map tab closes between the `tab` command and this `eval`, agent-browser falls back to another tab, so `location.reload()` may reload an unrelated page and discard its unsaved input. Use agent-browser's `--pin-tab` behavior, or combine selection and reload atomically, so a missing target fails instead of falling back. The committed evidence explicitly confirms this remains unfixed, and the closed threat-table row therefore does not close the behavior as required by [AGENTS.md lines 75–78](AGENTS.md#L75-L78).
The reload hook has a documented tab-close race that can reload the wrong browser tab and potentially lose unsaved state. The patch acknowledges but does not fix this behavior.

Review comment:

- [P2] Pin the selected tab before reloading — home/dot_claude/hooks/executable_project-map-reload.sh:26-26
  If the map tab closes between the `tab` command and this `eval`, agent-browser falls back to another tab, so `location.reload()` may reload an unrelated page and discard its unsaved input. Use agent-browser's `--pin-tab` behavior, or combine selection and reload atomically, so a missing target fails instead of falling back. The committed evidence explicitly confirms this remains unfixed, and the closed threat-table row therefore does not close the behavior as required by [AGENTS.md lines 75–78](AGENTS.md#L75-L78).
```
