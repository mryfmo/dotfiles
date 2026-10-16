[P2] high orchestration .orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md:63 D-S2-369 permits continuation by default despite documented INV-6 thresholds being reached. The named design requires an independent redesign/reset or operator waiver; an opportunity to overrule the default does not establish either release condition.

[P3] high evidence .orchestration/dotfiles-T128-settings-hook-dedupe-a01/validation.md:357 Validation is unchanged from bdefcbe: it still reports blocked render-check and the old 12/29-line diff. The amended report references amendment-specific validation supplements, but these are absent from the audited tree and supplied validation, leaving the claimed revised checks without their required command output.

INV-2: holds .orchestration/tasks/dotfiles-T128-settings-hook-dedupe-a01.md:75 — two non-evidence files; 14 source additions and 42 test additions satisfy the caps. No front-matter invariants are declared.
INV-6: violated .orchestration/acceptance/dotfiles-T128-settings-hook-dedupe-a01.md:63 — prescribed release condition is not evidenced.
INV-8: violated .orchestration/dotfiles-T128-settings-hook-dedupe-a01/report.md:8 — amendment validation supplements are not committed.

Orchestration findings: 1

All three task premises hold, and the task-copy hash matches. The wrapper regression fails against bdefcbe and passes against bf6beb5 in an adapted in-memory check; the original 19 tests remain unchanged. The saved [PR 369](https://github.com/mryfmo/dotfiles/pull/369) sweep matches the final head, reports 12 successful checks, and dispositions all ten feedback items.

📝 まとめ: Read-only audit completed with two outstanding findings; no files modified.
Not checked: live GitHub, original subprocess tests, or installed settings. Remaining risks are incomplete validation evidence and an unsupported reset-rule release.
Verdict: incorrect