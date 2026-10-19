---
task_id: dotfiles-T128-chain-review-scripts-followup-a06
row: audit:c646472:1
supersedes: .orchestration/dotfiles-T128-chain-review-scripts-followup-a05/sandbox.md lines 12 to 18 (the planned gh ledger)
---

# The gh calls of dotfiles-T128-chain-review-scripts-followup-a05 (PR #402), as they ran

The a05 sandbox record listed a plan: rows with placeholders (`<pr>`), to run "after the approval". This record lists the calls that ran, with the seat that ran each one and its outcome. The a05 record itself stays unchanged, because checker C2 keeps another task's `.orchestration/<id>/` directory out of this task's `allowed_files`.

GitHub shows one shared account (`moriya-fumio-thd`) for every action, so the seat comes from the regime records. Validation sections are cited as §.

| # | Call | Seat | Time (UTC) | Outcome | Evidence |
| --: | --- | --- | --- | --- | --- |
| 1 | `git push` of `tools/chain-review-scripts-followup-a05` over HTTPS (git, not gh) | `claude-standard-dot-a007` (worker-c), inside its sandbox | by 2026-10-17T16:46:39Z (commit `21aa36bf`, 16:46:25Z) | the branch at `21aa36bf` | §4 timeline; §5 a05 record line 128 |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T128-chain-review-scripts-followup-a05 status=blocked`, naming the PR-creation command | `claude-standard-dot-a007` | 2026-10-17T16:46:39Z | delivered. The seat ran no gh write, under D-ask-rules-night. | §5 a05 record line 128; §3 a05 report line 36 |
| 3 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/chain-review-scripts-followup-a05 …` (its exact argv is not on GitHub) | the orchestrator, `claude-deep-dot`, after the operator's morning approval | 2026-10-17T23:39:20Z (10-18 08:39 JST) | PR #402, opened as a draft. CodeRabbit posted its skipped-review summary at 23:39:29Z. | §4 `createdAt` and timeline; §5 a05 record lines 7 and 159 ("the orchestrator created PR #402") |
| 4 | `gh pr ready 402` | `claude-standard-dot-a011` (worker-d), item 0 of `dotfiles-T133-ci-efficiency-a01` | 2026-10-18T04:37:04Z | `ready_for_review`. The Codex connector posted its review summary at 04:37:15Z. | §4 timeline; §5 the ci-efficiency-a01 sandbox record, lines 10 and 19, and acceptance record, line 32 |
| 5 | `@codex review` | none | none | not posted: PR #402 has no human comment, no review comment and no review | §4 |
| 6 | `gh pr update-branch 402`, twice | the orchestrator's integration chain | 2026-10-19T12:02:36Z (`ac0a5274`, onto main `51ba5801`) and 2026-10-19T13:03:44Z (`c6464729`) | two merge commits from main | §4 timeline; §5 a05 record lines 129 and 153 |
| 7 | the chain's reads: `gh pr checks`, the feedback sweep, the task-level audit | the orchestrator's integration chain | 2026-10-19, up to 20:02:31Z | CI 7 of 7, the sweep with 0 gaps, the audit of `c6464729` with two P2 | §5 a05 record line 153 |
| 8 | `gh pr merge --squash --match-head-commit c6464729…` | the orchestrator | 2026-10-19T20:05:25Z | merged as `1eac64a8` | §4 `mergedAt` and `mergeCommit`; §5 a05 record line 160 |

After its blocked PONG, the records show no further gh call by `claude-standard-dot-a007`. The planned rows 2 to 4 of its ledger were carried out by other seats: row 3 above by the orchestrator, row 4 by a011. The `@codex review` of its row 4 never ran.

The a05 report says the seat "stops there" at the PR-creation command, and the acceptance record says "the orchestrator created PR #402". These do not contradict each other. They describe two seats: the worker stopped, and the orchestrator created the PR.

What was not read: the team-wide bus history. A whole-bus `history.sh` read was started for this record and had not finished when it was committed, since such reads take close to an hour (C-53). The seat of row 3 therefore rests on the orchestrator's own acceptance record, the authority on the orchestrator's actions, and its time on GitHub.
