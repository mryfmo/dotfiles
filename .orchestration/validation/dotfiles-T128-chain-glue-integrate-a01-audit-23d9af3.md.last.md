[P2] high implementation scripts/orchestrator/chain-integrate.sh:120 The post-wait check refreshes only the base. A push during the CI/Bot wait leaves the review on the old head while the sweep reads the new head; the record step then rejects the mismatch. Recheck the PR head and restart before local review.

[P2] high implementation scripts/orchestrator/chain-integrate.sh:88 Fetching `origin/main` does not advance an independent review clone’s local `main`, which `local-review.sh --base main` uses. After a base update, the review includes unrelated base changes. Align that reference or require a linked worktree.

[P2] high specification .orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md:127 Treating every nonzero checks result as failure includes GitHub’s transient “no checks reported” response immediately after update-branch. Specify a bounded retry for that condition; the current implementation aborts otherwise healthy integrations.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-chain-glue-integrate-a01.md:99 The evidence commands here and at line 101 reference an owner task absent from `origin/main`, so both fail. The owner exists in the main working tree; cite that actual artifact and paste successful evidence instead.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-chain-glue-integrate-a01.md:67 The only pasted counter output is truncated, predates later revise actions, and leaves Bot/audit counts `unknown` without the required source readings. The recorded operator waivers authorize additional revise rounds but do not supply the missing counter evidence.

[P3] high evidence .orchestration/dotfiles-T128-chain-glue-integrate-a01/validation.md:13 The comparison narrative says the canonical task differs only by an appended note, but its own output at lines 24–26 shows a front-matter threat-table insertion. Correct the narrative and retain the complete comparison.

INV-2: holds scripts/orchestrator/chain-integrate.sh:180 — two non-record files, 180 implementation lines and 420 test lines satisfy the caps.
INV-6: violated .orchestration/acceptance/dotfiles-T128-chain-glue-integrate-a01.md:67 — required counter accounting is incomplete despite the recorded revise-limit waivers.

Orchestration findings: 2

Premises 1–5 hold when replayed against the specified base. Submitted report, validation and sandbox files match the audited commit; the task-copy hash matches its recorded value.

📝 まとめ: 指定 head の読み取り専用監査を完了し、6 件の指摘を確認しました。ファイルは変更していません。

Not rerun: unit tests require filesystem writes. Live [PR/CI verification](https://github.com/mryfmo/dotfiles/pull/372) failed through both `gh` and web; saved evidence reports 12 successful checks.
Verdict: incorrect