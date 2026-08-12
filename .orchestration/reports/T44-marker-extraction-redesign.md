# T44 marker extraction redesign

Completed the CompactionDB explicit-marker redesign on `fix/compactiondb-markers`.

- Enumerates every marker in prompt order with a bracket-only regular expression.
- Bounds tag-form content at the next marker and keeps bracket-form known-kind parsing.
- Removes explicit marker spans before session-scoped keyword heuristics run.
- Splits English heuristic sentences after ASCII terminators followed by whitespace.
- Adds the three required regressions, README boundary documentation, changelog entry, and regenerated manifest.

The implementation stays stdlib-only and changes only the vendored package plus T44 orchestration artifacts.
