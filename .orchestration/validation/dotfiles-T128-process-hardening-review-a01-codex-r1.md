SHA-256 verified: `16675d7efa5596519c92e59b4323389393402d8da8cac75318ba18582dc26194`.

[P1] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:77 The specified split receipt fails downstream because `acceptance-front-matter.py` and `require-crit-review.py` accept only a final `Verdict:` line, yet neither consumer is covered by this task.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:78 Preserving existing revise assertions contradicts item 1: T118’s fixture contains 20 authored revise ACCEPTANCEs while its test expects 9, and synthetic histories without revise ACCEPTANCEs still expect positive counts.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:79 Checking that stub codex receives no call cannot prove audit inheritance skips auditing because the harness’s stub `orch-audit.sh` never invokes codex; assert the audit wrapper’s calls directly.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:79 “Stops as today’s `Verdict: incorrect`” misstates PR #378, whose existing test successfully finishes an incorrect audit after complete dispositions, and the proposed rejection lacks an explicit exit code.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:83 The named `dotfiles-T128-audit-s1-report-a01` task adds ledger/class reporting without implementing split verdicts, leaving the claimed receipt producer unassigned.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:47 The generic update-branch row adds an inheritance exception absent from `task-short.md`, violating stop condition 3’s verbatim requirement.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:95 “No other merge is a precondition” contradicts `after: [dotfiles-T128-chain-glue-finish-a01]` and premise 3’s requirement to wait for PR #378.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:95 The RESULT’s `task_copy` path duplicates `-a01`, pointing outside the declared evidence directory instead of its required `task.md`.

[P3] high .orchestration/tasks/dotfiles-T128-process-hardening-a01.md:91 The task lacks the pasted checker `OK` required by stop condition 4, although independent checking passes and masking reports zero matches.

Not checked: remote freshness—fetch was denied and GitHub unavailable; [PR #378](https://github.com/mryfmo/dotfiles/pull/378) used cached head `f20826e2`. Implementation tests were not run.
Task-file verdict: dotfiles-T128-process-hardening-a01: revise