[P2] high specification .orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md:66 Matching **any token’s basename** contradicts the custom-hook preservation requirement. Reproduced: `~/bin/log-hook.sh ~/.claude/hooks/format-edited-files.py` survives at the base but is deleted at the final head. The implementation follows this specification; the threat-table control at line 20 does not prevent this loss. Restrict recognition to managed command forms and test argument/name collisions.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md:24 The supplied record contains three RESULTs and three TASK dispatches, reaching INV-6’s two-revise/two-amendment thresholds even when results are blocked or continuations retain the same hash. Integration proceeds without the required counter output or a documented reset/waiver. Reconcile live history and apply the prescribed release condition before integration.

[P3] high evidence .orchestration/dotfiles-T128-settings-hook-dedupe-a01/report.md:3 The committed report still declares publication blocked and omits the published PR/head and subsequent CI results, although acceptance records a ready RESULT for [PR 369](https://github.com/mryfmo/dotfiles/pull/369). Update the final evidence to distinguish historical blockers from completed publication.

INV-2: holds .orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md:75 — named caps satisfied: two non-evidence files, 12 source additions, 29 test additions. No front-matter invariants are declared.

Orchestration findings: 1

All three premises hold; the task-copy hash matches. The adapted in-memory harness passed 20 tests; the new test produced six failures against the base. Saved CI records report success.

📝 まとめ: Read-only audit completed with three findings; no files modified.
Not checked: live GitHub/CI, original subprocess tests, or live apply; test I/O was mocked. Risk: custom hooks can be deleted.
Verdict: incorrect