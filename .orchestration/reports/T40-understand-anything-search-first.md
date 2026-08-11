# T40 Understand-Anything search-first integration

Completed two commits on `feat/understand-anything-search-first` in an isolated worktree:

- `49b1cdd feat(agents): route agent search through the understand-anything graph`
- `074fb41 chore(ua): commit knowledge graph baseline with auto-update`

The first commit adds fresh-graph search-first guidance for Claude, Codex, and the generated express explorer. The second commits the existing five-file graph baseline and ignores only generated intermediates and temporary graph data. The analysis was not re-run.

The original worktree remains on `main`. Git does not permit checking `main` out simultaneously in the isolated feature worktree, so that worktree remains on the committed feature branch.
