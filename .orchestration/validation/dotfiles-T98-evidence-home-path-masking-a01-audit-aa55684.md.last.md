- [P3] high confidence evidence-reality `.orchestration/reports/dotfiles-T98-evidence-home-path-masking-a01.md:144` claims unresolved threads block merging, but validation line 17956 reports `clean`, and the final-head feedback JSON marks all 12 Bot threads resolved. Correct the final status.
- [P3] high confidence evidence-reality `.orchestration/learning/dotfiles-T98-evidence-home-path-masking-a01.md:4` claims masking guarantees portable scan success despite the accepted `$HOME` dependency. Reproduced: `F/home/runner/.ssh/id` survives masking under `HOME=/srv/operator` but is flagged under `HOME=~`. Update this lesson to reflect the documented limitation.

Otherwise, scope and implementation checks passed: all expected artifacts exist; all 749 evidence changes match mechanical masking (747 byte-exact, two JSON-equivalent); credential detection is unchanged. Read-only behavioral checks passed, and supplied final-head CI records show 12 successful checks.

📝 まとめ: Audited `aa556845`; two evidence corrections remain, with no additional implementation defects found within the accepted design limits.

Verdict: incorrect