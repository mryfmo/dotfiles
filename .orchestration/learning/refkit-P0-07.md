# refkit-P0-07 learning

## Reusable

- **A repo-wide filesystem scanner (secret scan, banned-string search, etc.) should
  walk `git ls-files -z --cached --others --exclude-standard` instead of
  `Path.rglob("*")`** whenever "everything that could actually get committed" is the
  intent. This automatically and correctly excludes any gitignored directory
  (virtualenvs, node_modules, build output, tool caches) without needing to enumerate
  or guess those paths, and needs no change when new gitignored content appears later.
  Requires a graceful fallback (this repo's validator falls back to the old
  `rglob` walk with a stderr note) for callers that might run outside a git checkout.
- **Testing `git`-shelling-out code needs no `git commit`, only `git init` (+ optionally
  `git add`)** when the check being tested reads from the index (`--cached`) or the
  working tree filtered by `.gitignore` (`--others --exclude-standard`) — both are
  visible before any commit exists, so tests avoid the overhead/config-dependency of
  setting a commit identity.

## Not fixed (flagged, not promoted as a rule)

- `validate_no_removed_claude_skill()` in the same file has the identical
  `ROOT.rglob("*")` pattern and the same gitignored-content blind spot; left untouched
  since this task's scope named only `validate_no_obvious_secrets()`. Surfaced to the
  orchestrator in the report rather than fixed unilaterally.
