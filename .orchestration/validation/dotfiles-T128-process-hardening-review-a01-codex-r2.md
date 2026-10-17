[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:76 Adding a PR-side commit can invalidate the parent/receipt checks independently, so this negative case can pass with the patch-id comparison removed and does not close the inheritance row’s risk.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:74 Items 4–5 omit the three verdict-form cases explicitly required by stop condition 2, despite retaining the split-verdict compatibility claim.

[P3] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:72 T118’s fixture contains 10 RESULTs, not 9, although its previous revise count was 9.

📝 まとめ: Hash matched; premises returned `1 / 0 / 0`, checker passed, and masking found zero matches; the findings above remain.

Not checked: remote freshness because fetch was denied and GitHub unavailable; [PR #378](https://github.com/mryfmo/dotfiles/pull/378) used cached head `f20826e2`, and implementation tests were not run.
Task-file verdict: dotfiles-T128-process-hardening-a01: revise