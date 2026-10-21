[P1] high specification .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md:18 The control authenticates main’s SHA but leaves review content in the worker-writable shared object store. Design §5.14 item 8 requires GitHub content or a private clone. `local-review.sh:123` checks only object existence/type; disabling replacements and grafts does not authenticate overwritten objects. The report acknowledges this gap at line 96, but the task supplies neither mitigation nor an owning prerequisite.

[P1] high orchestration .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140 The record reports one amendment despite recording three TASK messages at lines 5–7. INV-6 counts every TASK after the first, including the erroneous resend: amendments therefore equal two, reaching the reset threshold. Subsequent revise/integration actions proceed without recorded S2 handling, counter output, or a reset/waiver.

The task declares no numbered invariant set; its inherited Completion clause references INV-6.

INV-6: violated .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md:140

Orchestration findings: 1

The task hash matches. Shell syntax, Python parsing, scope and caps pass. The script/tests match the validated code head; the supplied final-head feedback lists ten successful checks and dispositions for all five items.

📝 まとめ: [PR #439](https://github.com/mryfmo/dotfiles/pull/439) の指定 head を読み取り専用で監査し、仕様と運用に各1件の指摘を確認しました。ファイルは変更していません。

Not checked: live CI (`gh` and web access failed), real Codex execution, or test reruns requiring writes. The existing checkout was dirty; source inspection used the specified commit objects. The shared-store trust gap remains.
Verdict: incorrect