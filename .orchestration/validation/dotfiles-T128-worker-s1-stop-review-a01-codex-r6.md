[P2] high .orchestration/tasks/dotfiles-T128-worker-s1-stop-a01.md:52 The overview still promises blocking until `status=blocked note=S1:<class>`, although item 1 preserves closure by RESULT or any blocked PONG; describe blocking while the S1 entry remains pending and leave the required response form to the rule.

[P2] high .orchestration/tasks/dotfiles-T128-worker-s1-stop-a01.md:56 Qualify “a later ACCEPTANCE” as non-revise, because origin/main’s lines 289–290 process `status=revise` by updating pending rather than closing it, which otherwise misstates when S1 remains active.

📝 まとめ: Hash matched; premises returned `0`/`0`; checker, mask and template checks passed. Implementation tests and CI were not run; the two contract inconsistencies remain.
Task-file verdict: dotfiles-T128-worker-s1-stop-a01: revise