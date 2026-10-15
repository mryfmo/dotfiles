[P1] high .orchestration/tasks/dotfiles-T128-task-checkers-a01.md:112 `swept_finding_ids()` counts badged `review` bodies but not `issue_comment` bodies, so the amended rule would diverge from the gate.

[P1] high .orchestration/tasks/dotfiles-T128-task-checkers-a01.md:26 The ledger threat row still cites the pre-fix 36-gap test, which expressly contains neither amended input, instead of the new test that closes badged-review and bulleted-audit behavior.

[P1] high .orchestration/tasks/dotfiles-T128-task-checkers-a01.md:22 The C4 boundary behavior lacks its own threat row and a test explicitly proving `scripts/foo.py.bak` cannot cover `scripts/foo.py`, contrary to stop condition 2.

[P1] high .orchestration/tasks/dotfiles-T128-task-checkers-a01.md:24 The new closed row claims to cover the pass path, but its sole named test covers only six failing-check cases; the pass-path test on line 116 is not cited.

Amendment verdict: dotfiles-T128-task-checkers-a01: revise