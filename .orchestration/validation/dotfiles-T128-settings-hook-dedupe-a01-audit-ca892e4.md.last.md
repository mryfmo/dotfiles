[P2] high specification .orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md:66 The prescribed `shlex.split` comparison loses quoting information. A command containing `'~/.claude/hooks/format-edited-files.py'` or `\~/.claude/hooks/format-edited-files.py` invokes a relative path under a literal `~` directory, yet the predicate classifies it as managed and deletes it. Reproduced against the final head; preserve these forms and add a regression case.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md:120 The record explicitly identifies the third finding of the same class, but the ledger assigns separate classes and leaves `searches: []` at line 41. No required `search:` result precedes the next dispatch. This prevents S6 from detecting the acknowledged recurrence. The operator’s extra-round authorization does not record a waiver of that search.

INV-2: holds .orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md:75 — two non-evidence files, 20 source additions and 81 test additions satisfy the caps. No task-local invariant map is declared.

Orchestration findings: 1

For [PR #369](https://github.com/mryfmo/dotfiles/pull/369), all 27 added subcases passed an in-memory replay; the original 19 tests are unchanged. All three premises reproduced as stated. Task/report/validation/sandbox copies match the audited head.

📝 まとめ: Read-only audit completed; two P2 findings remain. No files changed.

Not checked: full subprocess tests or live CI; gh and Web access failed, so CI assessment used the supplied snapshot.
Verdict: incorrect