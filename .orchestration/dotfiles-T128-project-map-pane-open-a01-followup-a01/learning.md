---
task_id: dotfiles-T128-project-map-pane-open-a01-followup-a01
status: final
---

No promotion requested. Node resolves relative file URLs from physical cwd, while inherited shell PWD may name a symlink. Supplying Bash pwd-P to the existing jq relative-path normalization aligns that prefix without a new dependency. The focused regression explicitly supplies logical PWD and subprocess cwd through a symlink and records duplicate pane opening before the fix.

The prior tilde normalization and literal-percent controls remain covered. Path-component symlinks beyond the cwd prefix are not canonicalized. Prior optional Ruff lint/shfmt baseline observations are historical and were not rerun for this one-argument revision.
